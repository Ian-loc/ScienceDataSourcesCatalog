#!/usr/bin/env python3
"""Validate the normalized Instance 1 pilot after promotion and enrichment."""
from __future__ import annotations

import argparse
import os
import sys

DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)


def import_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "psycopg não instalado. Execute: python -m pip install -r database/requirements.txt"
        ) from exc
    return psycopg


def scalar(connection, query: str, params: tuple[object, ...] = ()) -> int:
    return int(connection.execute(query, params).fetchone()[0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    args = parser.parse_args()
    psycopg = import_psycopg()

    expected = {
        "sources": 2,
        "families": 5,
        "products": 2,
        "releases": 2,
        "distributions": 5,
        "capabilities": 17,
        "base_product_assertions": 6,
        "reviews": 2,
        "migrated_product_rows": 7,
        "mapped_product_rows": 4,
        "migrated_distribution_rows": 5,
        "mapped_distribution_rows": 14,
        "pending_distribution_rows": 0,
        "dynamic_world_variables": 10,
        "dynamic_world_product_variables": 10,
        "dynamic_world_methods": 1,
        "dynamic_world_spatial_profiles": 1,
        "dynamic_world_temporal_profiles": 1,
        "dynamic_world_quality_profiles": 1,
        "dynamic_world_assertions": 6,
        "dynamic_world_citations": 1,
    }

    with psycopg.connect(args.database_url) as connection:
        actual = {
            "sources": scalar(connection, "SELECT count(*) FROM catalog.sources WHERE stable_id IN ('DR0011','DR0019')"),
            "families": scalar(connection, "SELECT count(*) FROM catalog.product_families WHERE stable_id IN ('PF000001','PF000002','PF000003','PF000004','PF000005')"),
            "products": scalar(connection, "SELECT count(*) FROM catalog.products WHERE stable_id IN ('DP000005','DP000011')"),
            "releases": scalar(connection, "SELECT count(*) FROM catalog.product_releases WHERE stable_id IN ('PR000005','PR000011')"),
            "distributions": scalar(connection, "SELECT count(*) FROM catalog.distributions WHERE stable_id IN ('DD000006','DD000016','DD000017','DD000018','DD000019')"),
            "capabilities": scalar(connection, """
                SELECT count(*) FROM catalog.access_capabilities ac
                JOIN catalog.distributions d ON d.distribution_id=ac.distribution_id
                WHERE d.stable_id IN ('DD000006','DD000016','DD000017','DD000018','DD000019')
            """),
            "base_product_assertions": scalar(connection, "SELECT count(*) FROM catalog.metadata_assertions WHERE entity_type='product' AND entity_stable_id IN ('DP000005','DP000011')"),
            "reviews": scalar(connection, "SELECT count(*) FROM catalog.curation_reviews WHERE entity_type='product' AND entity_stable_id IN ('DP000005','DP000011')"),
            "migrated_product_rows": scalar(connection, "SELECT count(*) FROM staging.v_latest_products WHERE migration_status='migrated'"),
            "mapped_product_rows": scalar(connection, "SELECT count(*) FROM staging.v_latest_products WHERE migration_status='mapped'"),
            "migrated_distribution_rows": scalar(connection, "SELECT count(*) FROM staging.v_latest_distributions WHERE migration_status='migrated'"),
            "mapped_distribution_rows": scalar(connection, "SELECT count(*) FROM staging.v_latest_distributions WHERE migration_status='mapped'"),
            "pending_distribution_rows": scalar(connection, "SELECT count(*) FROM staging.v_latest_distributions WHERE migration_status='pending'"),
            "dynamic_world_variables": scalar(connection, "SELECT count(*) FROM catalog.variables WHERE stable_id BETWEEN 'VR000001' AND 'VR000010'"),
            "dynamic_world_product_variables": scalar(connection, """
                SELECT count(*) FROM catalog.product_variables pv
                JOIN catalog.product_releases pr ON pr.release_id=pv.release_id
                WHERE pr.stable_id='PR000011'
            """),
            "dynamic_world_methods": scalar(connection, "SELECT count(*) FROM catalog.methods WHERE stable_id='MT-DW-V1'"),
            "dynamic_world_spatial_profiles": scalar(connection, "SELECT count(*) FROM catalog.spatial_profiles WHERE stable_id='SP-DW-V1'"),
            "dynamic_world_temporal_profiles": scalar(connection, "SELECT count(*) FROM catalog.temporal_profiles WHERE stable_id='TP-DW-V1'"),
            "dynamic_world_quality_profiles": scalar(connection, "SELECT count(*) FROM catalog.quality_profiles WHERE stable_id='QP-DW-V1'"),
            "dynamic_world_assertions": scalar(connection, "SELECT count(*) FROM catalog.metadata_assertions WHERE entity_stable_id IN ('PR000011','QP-DW-V1','MT-DW-V1')"),
            "dynamic_world_citations": scalar(connection, "SELECT count(*) FROM catalog.citations WHERE doi='10.1038/s41597-022-01307-4'"),
        }

        failures = [
            f"{key}: atual={actual[key]} esperado={expected[key]}"
            for key in expected if actual[key] != expected[key]
        ]

        prohibited = scalar(connection, "SELECT count(*) FROM catalog.products WHERE stable_id IN ('DP000007','DP000008','DP000009','DP000010')")
        if prohibited:
            failures.append(f"{prohibited} serviço(s), catálogo(s) ou infraestrutura(s) promovidos como produto")

        incomplete_products = scalar(connection, """
            SELECT count(*) FROM catalog.products
            WHERE stable_id IN ('DP000005','DP000011') AND (
              scientific_object IS NULL OR btrim(scientific_object)=''
              OR information_message IS NULL OR btrim(information_message)=''
              OR non_representations IS NULL OR btrim(non_representations)=''
            )
        """)
        if incomplete_products:
            failures.append(f"{incomplete_products} produto(s) sem significado científico mínimo")

        incomplete_dw = scalar(connection, """
            SELECT count(*) FROM catalog.product_variables pv
            JOIN catalog.product_releases pr ON pr.release_id=pv.release_id
            WHERE pr.stable_id='PR000011' AND (
              pv.method_id IS NULL OR pv.spatial_profile_id IS NULL
              OR pv.temporal_profile_id IS NULL OR pv.quality_profile_id IS NULL
              OR pv.interpretation IS NULL OR btrim(pv.interpretation)=''
              OR pv.non_interpretations IS NULL OR btrim(pv.non_interpretations)=''
            )
        """)
        if incomplete_dw:
            failures.append(f"{incomplete_dw} variável(is) Dynamic World sem perfil completo")

        wrong_probability_units = scalar(connection, """
            SELECT count(*) FROM catalog.product_variables pv
            JOIN catalog.product_releases pr ON pr.release_id=pv.release_id
            WHERE pr.stable_id='PR000011' AND pv.variable_role='probability'
              AND pv.unit <> '1'
        """)
        if wrong_probability_units:
            failures.append(f"{wrong_probability_units} probabilidade(s) sem unidade adimensional '1'")

        unresolved_distribution_issues = scalar(connection, """
            SELECT count(*) FROM staging.migration_issues mi
            JOIN staging.v_latest_successful_batch b ON b.batch_id=mi.load_batch_id
            WHERE mi.entity_type='distribution' AND mi.resolution_status='open'
        """)
        if unresolved_distribution_issues:
            failures.append(f"{unresolved_distribution_issues} problema(s) aberto(s) de distribuição")

        if failures:
            print("ERRO: piloto normalizado inválido", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 1

        print(f"OK: piloto normalizado e perfil Dynamic World íntegros — {actual}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
