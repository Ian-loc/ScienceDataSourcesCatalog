#!/usr/bin/env python3
"""Resolve all legacy pilot distributions without premature promotion."""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "database" / "mappings" / "pilot_distribution_resolution.csv"
DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
EXPECTED_HEADER = (
    "distribution_id", "legacy_product_id", "resolved_entity_type",
    "target_stable_id", "disposition", "resolution_rationale",
)
ALLOWED_TYPES = {
    "family_distribution", "family_metadata", "product_distribution",
    "source_access_capability", "source_catalog_record",
}
ALLOWED_DISPOSITIONS = {"migrated", "mapped", "deferred"}


def import_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "psycopg não instalado. Execute: "
            "python -m pip install -r database/requirements.txt"
        ) from exc
    return psycopg


def read_mapping() -> list[dict[str, str]]:
    with MAPPING.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != EXPECTED_HEADER:
            raise ValueError(f"cabeçalho inválido em {MAPPING.name}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    ids = [row["distribution_id"] for row in rows]
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        raise ValueError(f"distribution_id duplicado: {duplicates}")
    invalid_types = sorted(
        row["distribution_id"] for row in rows
        if row["resolved_entity_type"] not in ALLOWED_TYPES
    )
    invalid_dispositions = sorted(
        row["distribution_id"] for row in rows
        if row["disposition"] not in ALLOWED_DISPOSITIONS
    )
    if invalid_types or invalid_dispositions:
        raise ValueError(
            f"mapeamento inválido; tipos={invalid_types or 'nenhum'} "
            f"disposições={invalid_dispositions or 'nenhuma'}"
        )
    return rows


def latest_batch(connection) -> int:
    row = connection.execute(
        "SELECT batch_id FROM staging.v_latest_successful_batch"
    ).fetchone()
    if not row:
        raise ValueError("nenhum lote bem-sucedido no staging")
    return int(row[0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    args = parser.parse_args()
    rows = read_mapping()
    psycopg = import_psycopg()

    with psycopg.connect(args.database_url) as connection:
        batch_id = latest_batch(connection)
        staged = connection.execute(
            """
            SELECT distribution_id, product_id, migration_status
            FROM staging.legacy_distributions
            WHERE load_batch_id = %s
            """,
            (batch_id,),
        ).fetchall()
        staged_by_id = {row[0]: (row[1], row[2]) for row in staged}
        mapping_ids = {row["distribution_id"] for row in rows}
        staged_ids = set(staged_by_id)
        if mapping_ids != staged_ids:
            raise ValueError(
                f"cobertura divergente; ausentes={sorted(staged_ids - mapping_ids)} "
                f"desconhecidos={sorted(mapping_ids - staged_ids)}"
            )

        counts = {"migrated": 0, "mapped": 0, "deferred": 0}
        for row in rows:
            distribution_id = row["distribution_id"]
            product_id, current_status = staged_by_id[distribution_id]
            if product_id != row["legacy_product_id"]:
                raise ValueError(
                    f"{distribution_id}: product_id={product_id}; "
                    f"esperado={row['legacy_product_id']}"
                )
            disposition = row["disposition"]
            counts[disposition] += 1
            if disposition == "migrated":
                if current_status != "migrated":
                    raise ValueError(
                        f"{distribution_id}: deveria estar migrada, status={current_status}"
                    )
                continue

            note = (
                f"{row['resolved_entity_type']} -> {row['target_stable_id']}; "
                f"disposição={disposition}. {row['resolution_rationale']}"
            )
            connection.execute(
                """
                UPDATE staging.legacy_distributions
                SET migration_status = 'mapped', migration_notes = %s
                WHERE load_batch_id = %s AND distribution_id = %s
                """,
                (note, batch_id, distribution_id),
            )
            connection.execute(
                """
                INSERT INTO staging.migration_issues (
                    load_batch_id, entity_type, legacy_id, issue_code,
                    severity, field_name, current_value, issue_description,
                    proposed_action, resolution_status
                )
                VALUES (
                    %s, 'distribution', %s, %s,
                    'info', 'distribution_id', %s, %s, %s, 'accepted'
                )
                ON CONFLICT (
                    load_batch_id, entity_type, legacy_id, issue_code
                ) DO UPDATE SET
                    current_value = EXCLUDED.current_value,
                    issue_description = EXCLUDED.issue_description,
                    proposed_action = EXCLUDED.proposed_action,
                    resolution_status = 'accepted'
                """,
                (
                    batch_id, distribution_id,
                    "DEFERRED_UNTIL_FAMILY_RESOLUTION" if disposition == "deferred"
                    else "RECLASSIFIED_OUTSIDE_PRODUCT",
                    row["resolved_entity_type"], row["resolution_rationale"], note,
                ),
            )

        unresolved = connection.execute(
            """
            SELECT count(*)
            FROM staging.legacy_distributions
            WHERE load_batch_id = %s AND migration_status = 'pending'
            """,
            (batch_id,),
        ).fetchone()[0]
        if unresolved:
            raise ValueError(f"{unresolved} distribuições permanecem pendentes")

    print(f"OK: 19 distribuições resolvidas — {counts}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
