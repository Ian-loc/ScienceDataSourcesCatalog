#!/usr/bin/env python3
"""Validate normalized Dynamic World operational semantics after reconciliation."""
from __future__ import annotations

import argparse
import os
import sys

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)

EXPECTED_DISTRIBUTIONS = {
    "DD000016": ("api", "yes", "CC BY 4.0"),
    "DD000017": ("catalog_record", "no", "CC BY 4.0"),
    "DD000018": ("visualizer", "no", "CC BY 4.0"),
    "DD000019": ("code_repository", "no", "Apache-2.0 (software); dataset remains CC BY 4.0"),
}


def psycopg_module():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit("Instale database/requirements.txt") from exc
    return psycopg


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DATABASE_URL)
    args = parser.parse_args()
    psycopg = psycopg_module()
    failures: list[str] = []

    with psycopg.connect(args.database_url) as connection:
        rows = connection.execute(
            """
            SELECT stable_id, distribution_role, authentication_required,
                   license, access_status, last_access_tested_at
            FROM catalog.distributions
            WHERE stable_id IN ('DD000016','DD000017','DD000018','DD000019')
            """
        ).fetchall()
        if len(rows) != 4:
            failures.append(f"distribuições encontradas={len(rows)}; esperado=4")
        by_id = {str(row[0]): row for row in rows}
        for stable_id, expected in EXPECTED_DISTRIBUTIONS.items():
            row = by_id.get(stable_id)
            if row is None:
                failures.append(f"{stable_id}: ausente")
                continue
            actual = tuple(row[1:4])
            if actual != expected:
                failures.append(f"{stable_id}: {actual}; esperado={expected}")
            if row[4] != "working":
                failures.append(f"{stable_id}: access_status={row[4]}; esperado=working")
            if row[5] is None:
                failures.append(f"{stable_id}: last_access_tested_at ausente")

        asset = connection.execute(
            """
            SELECT d.stable_id, a.asset_identifier, a.asset_url, a.asset_role,
                   a.machine_readable, a.supports_spatial_subset,
                   a.supports_temporal_subset, a.crs
            FROM catalog.data_assets a
            JOIN catalog.distributions d ON d.distribution_id=a.distribution_id
            WHERE a.stable_id='AS-DW-EE-V1'
            """
        ).fetchone()
        if not asset:
            failures.append("AS-DW-EE-V1 ausente")
        else:
            expected_asset = (
                "DD000016",
                "GOOGLE/DYNAMICWORLD/V1",
                "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1",
                "data",
                True,
                True,
                True,
                None,
            )
            if tuple(asset) != expected_asset:
                failures.append(f"AS-DW-EE-V1 divergente: {tuple(asset)}")

        capability_count = int(connection.execute(
            """
            SELECT count(*)
            FROM catalog.access_capabilities ac
            JOIN catalog.distributions d ON d.distribution_id=ac.distribution_id
            WHERE d.stable_id IN ('DD000016','DD000017','DD000018','DD000019')
            """
        ).fetchone()[0])
        if capability_count != 15:
            failures.append(f"capacidades={capability_count}; esperado=15")

        required_assertions = {
            ("asset", "AS-DW-EE-V1", "asset_identifier"),
            ("distribution", "DD000016", "access_model"),
            ("distribution", "DD000016", "license"),
            ("release", "PR000011", "required_attribution"),
            ("release", "PR000011", "upstream_notice"),
        }
        assertions = {
            (str(row[0]), str(row[1]), str(row[2]))
            for row in connection.execute(
                """
                SELECT entity_type, entity_stable_id, field_name
                FROM catalog.metadata_assertions
                WHERE (entity_type='asset' AND entity_stable_id='AS-DW-EE-V1')
                   OR (entity_type='distribution' AND entity_stable_id='DD000016')
                   OR (entity_type='release' AND entity_stable_id='PR000011'
                       AND field_name IN ('required_attribution','upstream_notice'))
                """
            ).fetchall()
        }
        missing = sorted(required_assertions - assertions)
        if missing:
            failures.append(f"afirmações operacionais ausentes: {missing}")

        review = connection.execute(
            """
            SELECT review_status, completeness_score,
                   scientific_precision_score, operational_precision_score,
                   corrections_required
            FROM catalog.curation_reviews
            WHERE entity_type='product' AND entity_stable_id='DP000011'
            """
        ).fetchone()
        if not review:
            failures.append("revisão DP000011 ausente")
        else:
            if review[0] != "reviewed":
                failures.append(f"review_status={review[0]}; esperado=reviewed")
            for name, value in zip(
                ("completeness", "scientific_precision", "operational_precision"),
                review[1:4],
            ):
                if value is None or float(value) < 0.9:
                    failures.append(f"{name}={value}; esperado>=0.9")
            if not review[4] or "human authorization" not in review[4]:
                failures.append("gate humano final não preservado em corrections_required")

    if failures:
        print("ERRO: reconciliação operacional Dynamic World inválida", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("OK: distribuições, ativo, capacidades, evidências e revisão Dynamic World coerentes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
