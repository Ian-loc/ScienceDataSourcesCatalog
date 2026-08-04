#!/usr/bin/env python3
"""Promote the resolved Instance 1 pilot from staging into the normalized catalog."""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
SOURCE_MAPPING = ROOT / "database" / "mappings" / "pilot_sources.csv"
FAMILY_MAPPING = ROOT / "database" / "mappings" / "pilot_families.csv"
PRODUCT_MAPPING = ROOT / "database" / "mappings" / "pilot_products.csv"

DISTRIBUTION_ROLES = {
    "DD000006": "direct_download",
    "DD000016": "api",
    "DD000017": "catalog_record",
    "DD000018": "visualizer",
    "DD000019": "code_repository",
}

CAPABILITIES = {
    "DD000006": (
        ("discover", "available"),
        ("download", "available"),
    ),
    "DD000016": (
        ("discover", "available"),
        ("query_attributes", "conditional"),
        ("spatial_subset", "conditional"),
        ("temporal_subset", "conditional"),
        ("process", "conditional"),
        ("export", "conditional"),
        ("open_in_earth_engine", "conditional"),
        ("open_in_python", "conditional"),
    ),
    "DD000017": (
        ("discover", "available"),
        ("preview", "available"),
    ),
    "DD000018": (
        ("preview", "available"),
        ("visualize", "available"),
    ),
    "DD000019": (
        ("discover", "available"),
        ("download", "available"),
        ("open_in_python", "conditional"),
    ),
}


def import_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "psycopg não instalado. Execute: "
            "python -m pip install -r database/requirements.txt"
        ) from exc
    return psycopg


def read_mapping(path: Path, expected: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected:
            raise ValueError(f"{path.name}: cabeçalho esperado {expected}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError(f"{path.name}: mapeamento vazio")
    return rows


def to_bool(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"sim", "yes", "true", "1"}:
        return True
    if normalized in {"não", "nao", "no", "false", "0"}:
        return False
    return None


def access_value(value: str) -> str:
    normalized = value.strip().lower()
    mapping = {
        "sim": "yes",
        "não": "no",
        "nao": "no",
        "parcial": "partial",
        "desconhecido": "unknown",
        "não se aplica": "not_applicable",
        "nao se aplica": "not_applicable",
    }
    return mapping.get(normalized, "unknown")


def require_latest_batch(connection) -> int:
    row = connection.execute(
        "SELECT batch_id FROM staging.v_latest_successful_batch"
    ).fetchone()
    if not row:
        raise ValueError("nenhum lote bem-sucedido no staging")
    return int(row[0])


def verify_resolution(
    connection,
    batch_id: int,
    mapping_rows: Sequence[dict[str, str]],
    expected_type: str,
) -> None:
    for row in mapping_rows:
        legacy_id = row["legacy_product_id"]
        resolved = connection.execute(
            """
            SELECT resolved_entity_type
            FROM staging.legacy_products
            WHERE load_batch_id = %s AND product_id = %s
            """,
            (batch_id, legacy_id),
        ).fetchone()
        if not resolved or resolved[0] != expected_type:
            raise ValueError(
                f"{legacy_id}: esperado resolved_entity_type={expected_type}; "
                f"encontrado={resolved[0] if resolved else 'ausente'}"
            )


def promote_sources(connection, batch_id: int, rows: Sequence[dict[str, str]]) -> None:
    for row in rows:
        legacy = connection.execute(
            """
            SELECT resource_id, resource_name, acronym, official_identity,
                   description, homepage_url, data_access_url,
                   access_documentation_url, institutional_status,
                   owner_or_manager, geographic_coverage, covers_brazil,
                   limitations
            FROM staging.legacy_resources
            WHERE load_batch_id = %s AND resource_id = %s
            """,
            (batch_id, row["resource_id"]),
        ).fetchone()
        if not legacy:
            raise ValueError(f"fonte ausente no staging: {row['resource_id']}")
        connection.execute(
            """
            INSERT INTO catalog.sources (
                stable_id, source_name, acronym, source_type,
                official_identity, description, homepage_url,
                primary_data_access_url, access_documentation_url,
                institutional_status, owner_or_manager,
                geographic_scope, covers_brazil, enumeration_strategy,
                notes
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s, %s,
                %s, %s, %s,
                %s
            )
            ON CONFLICT (stable_id) DO UPDATE SET
                source_name = EXCLUDED.source_name,
                acronym = EXCLUDED.acronym,
                source_type = EXCLUDED.source_type,
                official_identity = EXCLUDED.official_identity,
                description = EXCLUDED.description,
                homepage_url = EXCLUDED.homepage_url,
                primary_data_access_url = EXCLUDED.primary_data_access_url,
                access_documentation_url = EXCLUDED.access_documentation_url,
                institutional_status = EXCLUDED.institutional_status,
                owner_or_manager = EXCLUDED.owner_or_manager,
                geographic_scope = EXCLUDED.geographic_scope,
                covers_brazil = EXCLUDED.covers_brazil,
                enumeration_strategy = EXCLUDED.enumeration_strategy,
                notes = EXCLUDED.notes,
                updated_at = now()
            """,
            (
                legacy[0], legacy[1], legacy[2] or None, row["source_type"],
                legacy[3] or None, legacy[4], legacy[5] or None,
                legacy[6] or None, legacy[7] or None,
                legacy[8] or None, legacy[9] or None,
                legacy[10] or None, to_bool(legacy[11]),
                row["enumeration_strategy"], legacy[12] or None,
            ),
        )


def promote_families(connection, batch_id: int, rows: Sequence[dict[str, str]]) -> None:
    verify_resolution(connection, batch_id, rows, "product_family")
    for row in rows:
        legacy = connection.execute(
            """
            SELECT resource_id, product_name, product_acronym,
                   product_description, enumeration_scope
            FROM staging.legacy_products
            WHERE load_batch_id = %s AND product_id = %s
            """,
            (batch_id, row["legacy_product_id"]),
        ).fetchone()
        source_id = connection.execute(
            "SELECT source_id FROM catalog.sources WHERE stable_id = %s",
            (legacy[0],),
        ).fetchone()
        if not source_id:
            raise ValueError(f"fonte normalizada ausente: {legacy[0]}")
        connection.execute(
            """
            INSERT INTO catalog.product_families (
                source_id, stable_id, family_name, acronym,
                description, scientific_scope, enumeration_scope
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (stable_id) DO UPDATE SET
                source_id = EXCLUDED.source_id,
                family_name = EXCLUDED.family_name,
                acronym = EXCLUDED.acronym,
                description = EXCLUDED.description,
                scientific_scope = EXCLUDED.scientific_scope,
                enumeration_scope = EXCLUDED.enumeration_scope,
                updated_at = now()
            """,
            (
                source_id[0], row["family_stable_id"],
                row["family_name"] or legacy[1],
                legacy[2] or None,
                legacy[3] or None,
                row["scientific_scope"],
                legacy[4] if legacy[4] in {
                    "complete", "family_level", "external_index",
                    "representative_sample", "selective"
                } else "family_level",
            ),
        )
        connection.execute(
            """
            UPDATE staging.legacy_products
            SET migration_status = 'migrated',
                migrated_at = now(),
                migration_notes = %s
            WHERE load_batch_id = %s AND product_id = %s
            """,
            (
                f"Promovido para catalog.product_families/{row['family_stable_id']}",
                batch_id,
                row["legacy_product_id"],
            ),
        )


def promote_products(connection, batch_id: int, rows: Sequence[dict[str, str]]) -> None:
    verify_resolution(connection, batch_id, rows, "product")
    for row in rows:
        legacy = connection.execute(
            """
            SELECT product_name, product_acronym, product_description,
                   geographic_coverage, covers_brazil, product_page_url,
                   methodology_url, limitations
            FROM staging.legacy_products
            WHERE load_batch_id = %s AND product_id = %s
            """,
            (batch_id, row["legacy_product_id"]),
        ).fetchone()
        source_id = connection.execute(
            "SELECT source_id FROM catalog.sources WHERE stable_id = %s",
            (row["source_stable_id"],),
        ).fetchone()
        if not source_id:
            raise ValueError(f"fonte normalizada ausente: {row['source_stable_id']}")

        connection.execute(
            """
            INSERT INTO catalog.products (
                stable_id, source_id, product_name, acronym, product_kind,
                product_description, scientific_object, information_message,
                intended_uses, non_representations, primary_or_derived,
                geographic_coverage_text, covers_brazil, product_status,
                official_product_page_url, methodology_url,
                limitations_summary
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s
            )
            ON CONFLICT (stable_id) DO UPDATE SET
                source_id = EXCLUDED.source_id,
                product_name = EXCLUDED.product_name,
                acronym = EXCLUDED.acronym,
                product_kind = EXCLUDED.product_kind,
                product_description = EXCLUDED.product_description,
                scientific_object = EXCLUDED.scientific_object,
                information_message = EXCLUDED.information_message,
                intended_uses = EXCLUDED.intended_uses,
                non_representations = EXCLUDED.non_representations,
                primary_or_derived = EXCLUDED.primary_or_derived,
                geographic_coverage_text = EXCLUDED.geographic_coverage_text,
                covers_brazil = EXCLUDED.covers_brazil,
                product_status = EXCLUDED.product_status,
                official_product_page_url = EXCLUDED.official_product_page_url,
                methodology_url = EXCLUDED.methodology_url,
                limitations_summary = EXCLUDED.limitations_summary,
                updated_at = now()
            """,
            (
                row["legacy_product_id"], source_id[0],
                legacy[0], legacy[1] or None, row["product_kind"],
                legacy[2], row["scientific_object"], row["information_message"],
                row["intended_uses"] or None, row["non_representations"] or None,
                row["primary_or_derived"], legacy[3] or None,
                to_bool(legacy[4]) or False, row["product_status"],
                legacy[5] or None, legacy[6] or None, legacy[7] or None,
            ),
        )
        product_id = connection.execute(
            "SELECT product_id FROM catalog.products WHERE stable_id = %s",
            (row["legacy_product_id"],),
        ).fetchone()[0]
        connection.execute(
            """
            INSERT INTO catalog.product_releases (
                product_id, stable_id, version_label, release_status,
                is_current, temporal_coverage_text
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (stable_id) DO UPDATE SET
                product_id = EXCLUDED.product_id,
                version_label = EXCLUDED.version_label,
                release_status = EXCLUDED.release_status,
                is_current = EXCLUDED.is_current,
                temporal_coverage_text = EXCLUDED.temporal_coverage_text,
                updated_at = now()
            """,
            (
                product_id, row["release_stable_id"], row["version_label"],
                row["release_status"], row["is_current"].lower() == "true",
                row["temporal_coverage_text"] or None,
            ),
        )
        connection.execute(
            """
            INSERT INTO catalog.curation_reviews (
                entity_type, entity_stable_id, review_status,
                findings, corrections_required
            )
            SELECT 'product', %s, 'in_progress', %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM catalog.curation_reviews
                WHERE entity_type = 'product' AND entity_stable_id = %s
            )
            """,
            (
                row["legacy_product_id"],
                "Produto promovido do piloto; perfil científico ainda incompleto.",
                "Completar variáveis, método, perfis espacial/temporal, qualidade e evidências.",
                row["legacy_product_id"],
            ),
        )
        evidence_url = legacy[6] or legacy[5]
        if evidence_url:
            for field_name, value, support_note in (
                ("scientific_object", row["scientific_object"],
                 "Síntese curatorial baseada na documentação oficial do produto."),
                ("information_message", row["information_message"],
                 "Formulação pública do significado científico do produto."),
                ("non_representations", row["non_representations"],
                 "Limites de interpretação derivados da documentação e do escopo do produto."),
            ):
                connection.execute(
                    """
                    INSERT INTO catalog.metadata_assertions (
                        entity_type, entity_stable_id, field_name,
                        asserted_value, evidence_url, evidence_type,
                        support_note, confidence, retrieved_at
                    )
                    SELECT 'product', %s, %s, %s, %s, 'curatorial_inference',
                           %s, 'medium', now()
                    WHERE NOT EXISTS (
                        SELECT 1 FROM catalog.metadata_assertions
                        WHERE entity_type = 'product'
                          AND entity_stable_id = %s
                          AND field_name = %s
                          AND evidence_url = %s
                    )
                    """,
                    (
                        row["legacy_product_id"], field_name, value,
                        evidence_url, support_note,
                        row["legacy_product_id"], field_name, evidence_url,
                    ),
                )
        connection.execute(
            """
            UPDATE staging.legacy_products
            SET migration_status = 'migrated',
                migrated_at = now(),
                migration_notes = %s
            WHERE load_batch_id = %s AND product_id = %s
            """,
            (
                f"Promovido para catalog.products/{row['legacy_product_id']} "
                f"e release {row['release_stable_id']}",
                batch_id,
                row["legacy_product_id"],
            ),
        )


def promote_distributions(connection, batch_id: int) -> None:
    placeholders = ", ".join(["%s"] * len(DISTRIBUTION_ROLES))
    rows = connection.execute(
        f"""
        SELECT distribution_id, product_id, distribution_name,
               access_url, format, access_protocol, access_tool,
               free_download, authentication_required, access_conditions,
               license, provider_attribution_required, subset_support, notes
        FROM staging.legacy_distributions
        WHERE load_batch_id = %s
          AND distribution_id IN ({placeholders})
        ORDER BY distribution_id
        """,
        (batch_id, *DISTRIBUTION_ROLES.keys()),
    ).fetchall()
    if len(rows) != len(DISTRIBUTION_ROLES):
        raise ValueError(
            f"distribuições piloto encontradas={len(rows)}; "
            f"esperado={len(DISTRIBUTION_ROLES)}"
        )
    release_by_product = {
        row[0]: row[1]
        for row in connection.execute(
            """
            SELECT p.stable_id, pr.release_id
            FROM catalog.products p
            JOIN catalog.product_releases pr ON pr.product_id = p.product_id
            WHERE pr.is_current
            """
        ).fetchall()
    }
    for row in rows:
        if row[1] not in release_by_product:
            raise ValueError(f"release atual ausente para {row[1]}")
        connection.execute(
            """
            INSERT INTO catalog.distributions (
                stable_id, release_id, distribution_name,
                distribution_role, access_url, format,
                access_protocol, access_tool, free_access,
                authentication_required, access_conditions,
                license, attribution_required, subset_support,
                service_level_notes
            )
            VALUES (
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s, %s, %s,
                %s
            )
            ON CONFLICT (stable_id) DO UPDATE SET
                release_id = EXCLUDED.release_id,
                distribution_name = EXCLUDED.distribution_name,
                distribution_role = EXCLUDED.distribution_role,
                access_url = EXCLUDED.access_url,
                format = EXCLUDED.format,
                access_protocol = EXCLUDED.access_protocol,
                access_tool = EXCLUDED.access_tool,
                free_access = EXCLUDED.free_access,
                authentication_required = EXCLUDED.authentication_required,
                access_conditions = EXCLUDED.access_conditions,
                license = EXCLUDED.license,
                attribution_required = EXCLUDED.attribution_required,
                subset_support = EXCLUDED.subset_support,
                service_level_notes = EXCLUDED.service_level_notes,
                updated_at = now()
            """,
            (
                row[0], release_by_product[row[1]], row[2],
                DISTRIBUTION_ROLES[row[0]], row[3], row[4] or None,
                row[5] or None, row[6] or None, access_value(row[7]),
                access_value(row[8]), row[9] or None,
                row[10] or None, to_bool(row[11]), row[12] or None,
                row[13] or None,
            ),
        )
        distribution_pk = connection.execute(
            "SELECT distribution_id FROM catalog.distributions WHERE stable_id = %s",
            (row[0],),
        ).fetchone()[0]
        for capability_type, status in CAPABILITIES[row[0]]:
            connection.execute(
                """
                INSERT INTO catalog.access_capabilities (
                    distribution_id, capability_type, capability_status,
                    requirements, documentation_url
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (distribution_id, capability_type) DO UPDATE SET
                    capability_status = EXCLUDED.capability_status,
                    requirements = EXCLUDED.requirements,
                    documentation_url = EXCLUDED.documentation_url
                """,
                (
                    distribution_pk, capability_type, status,
                    row[9] or None, row[3],
                ),
            )
        connection.execute(
            """
            UPDATE staging.legacy_distributions
            SET migration_status = 'migrated',
                migrated_at = now(),
                migration_notes = %s
            WHERE load_batch_id = %s AND distribution_id = %s
            """,
            (
                f"Promovida para catalog.distributions/{row[0]}",
                batch_id,
                row[0],
            ),
        )


def verify_promoted_catalog(connection) -> dict[str, int]:
    counts = {
        "sources": int(connection.execute(
            "SELECT count(*) FROM catalog.sources WHERE stable_id IN ('DR0011','DR0019')"
        ).fetchone()[0]),
        "families": int(connection.execute(
            "SELECT count(*) FROM catalog.product_families "
            "WHERE stable_id LIKE 'PF00000%'"
        ).fetchone()[0]),
        "products": int(connection.execute(
            "SELECT count(*) FROM catalog.products "
            "WHERE stable_id IN ('DP000005','DP000011')"
        ).fetchone()[0]),
        "releases": int(connection.execute(
            "SELECT count(*) FROM catalog.product_releases "
            "WHERE stable_id IN ('PR000005','PR000011')"
        ).fetchone()[0]),
        "distributions": int(connection.execute(
            "SELECT count(*) FROM catalog.distributions "
            "WHERE stable_id IN ('DD000006','DD000016','DD000017','DD000018','DD000019')"
        ).fetchone()[0]),
    }
    expected = {
        "sources": 2,
        "families": 5,
        "products": 2,
        "releases": 2,
        "distributions": 5,
    }
    if counts != expected:
        raise ValueError(f"contagens normalizadas divergentes: {counts} != {expected}")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    args = parser.parse_args()

    source_rows = read_mapping(
        SOURCE_MAPPING,
        ("resource_id", "source_type", "enumeration_strategy"),
    )
    family_rows = read_mapping(
        FAMILY_MAPPING,
        (
            "legacy_product_id", "family_stable_id",
            "family_name", "scientific_scope",
        ),
    )
    product_rows = read_mapping(
        PRODUCT_MAPPING,
        (
            "legacy_product_id", "source_stable_id", "product_kind",
            "scientific_object", "information_message", "intended_uses",
            "non_representations", "primary_or_derived", "product_status",
            "release_stable_id", "version_label", "release_status",
            "is_current", "temporal_coverage_text",
        ),
    )

    psycopg = import_psycopg()
    try:
        with psycopg.connect(args.database_url) as connection:
            batch_id = require_latest_batch(connection)
            promote_sources(connection, batch_id, source_rows)
            promote_families(connection, batch_id, family_rows)
            promote_products(connection, batch_id, product_rows)
            promote_distributions(connection, batch_id)
            counts = verify_promoted_catalog(connection)
            connection.commit()
            print(
                "OK: piloto promovido ao catálogo normalizado — "
                f"batch={batch_id}; {counts}"
            )
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
