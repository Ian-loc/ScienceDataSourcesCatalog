#!/usr/bin/env python3
"""Promote canonical source rows into the minimum-sufficient Instance 1 core.

The promotion is additive and deliberately conservative: it maps the current
source records to catalog entries, preserves source terminology, does not split
technical assets into entries, and never overwrites an existing entry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Iterable

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


def clean(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def split_pipe(value: object) -> list[str]:
    text = clean(value)
    if not text:
        return []
    return [part.strip() for part in text.split("|") if part.strip()]


def normalized_flag(value: object, *, authentication: bool = False) -> str:
    text = (clean(value) or "").casefold()
    if not text:
        return "unknown"
    if "não se aplica" in text or "nao se aplica" in text:
        return "not_applicable"
    if text in {"sim", "yes"}:
        return "yes"
    if text in {"não", "nao", "no"}:
        return "no"
    if "parcial" in text:
        return "partial"
    if authentication and ("cadastro" in text or "conta" in text or "chave" in text):
        return "yes"
    return "unknown"


def access_level(value: object) -> str:
    text = (clean(value) or "").casefold()
    if not text:
        return "unknown"
    if "restrit" in text or "mediante" in text:
        return "restricted"
    if "parcial" in text or "cadastro" in text or "solicita" in text:
        return "partial"
    if "aberto" in text or "públic" in text or "public" in text:
        return "open"
    return "unknown"


def organization_stable_id(name: str) -> str:
    digest = hashlib.sha1(name.casefold().encode("utf-8")).hexdigest()[:12]
    return f"ORG-MIG-{digest}"


def latest_successful_batch(connection) -> int:
    row = connection.execute(
        """
        SELECT batch_id
        FROM staging.load_batches
        WHERE status = 'successful'
        ORDER BY batch_id DESC
        LIMIT 1
        """
    ).fetchone()
    if not row:
        raise ValueError("nenhum lote staging bem-sucedido disponível")
    return int(row[0])


def ensure_organization(connection, name: str | None) -> int | None:
    if not name:
        return None
    row = connection.execute(
        """
        SELECT organization_id
        FROM catalog.organizations
        WHERE lower(official_name) = lower(%s)
        ORDER BY organization_id
        LIMIT 1
        """,
        (name,),
    ).fetchone()
    if row:
        return int(row[0])
    stable_id = organization_stable_id(name)
    row = connection.execute(
        """
        INSERT INTO catalog.organizations (stable_id, official_name, organization_type)
        VALUES (%s, %s, 'legacy_source_label')
        ON CONFLICT (stable_id) DO UPDATE
        SET official_name = EXCLUDED.official_name
        RETURNING organization_id
        """,
        (stable_id, name),
    ).fetchone()
    return int(row[0])


def resource_rows(connection, batch_id: int) -> Iterable[dict[str, object]]:
    columns = (
        "resource_id", "resource_name", "acronym", "official_identity", "description",
        "homepage_url", "data_access_url", "research_areas", "keywords",
        "data_product_types", "data_formats", "visualization_types",
        "geographic_coverage", "spatial_resolution", "temporal_coverage",
        "temporal_resolution", "data_sources", "free_download", "access_conditions",
        "programmatic_access", "access_protocols", "authentication_required",
        "access_documentation_url", "license", "institutional_status",
        "owner_or_manager", "academic_uses", "limitations", "verification_url",
        "last_verified",
    )
    sql = (
        f"SELECT {', '.join(columns)} FROM staging.legacy_resources "
        "WHERE load_batch_id = %s ORDER BY resource_id"
    )
    for row in connection.execute(sql, (batch_id,)).fetchall():
        yield dict(zip(columns, row, strict=True))


def promote(connection, batch_id: int) -> dict[str, int]:
    inserted_entries = 0
    preserved_entries = 0
    inserted_themes = 0
    inserted_evidence = 0

    for source in resource_rows(connection, batch_id):
        resource_id = str(source["resource_id"])
        organization_id = ensure_organization(connection, clean(source["owner_or_manager"]))
        modalities = split_pipe(source["data_product_types"])
        verification_url = clean(source["verification_url"]) or clean(source["homepage_url"])
        verified_at = clean(source["last_verified"])
        status = "partially_verified" if verification_url and verified_at else "needs_review"
        additional_metadata = {
            key: value
            for key, value in {
                "migration_source": "staging.legacy_resources",
                "official_identity": clean(source["official_identity"]),
                "research_areas": split_pipe(source["research_areas"]),
                "data_formats": split_pipe(source["data_formats"]),
                "visualization_types": split_pipe(source["visualization_types"]),
                "temporal_resolution": clean(source["temporal_resolution"]),
                "data_sources": split_pipe(source["data_sources"]),
                "access_conditions": clean(source["access_conditions"]),
                "programmatic_access": clean(source["programmatic_access"]),
                "access_protocols": split_pipe(source["access_protocols"]),
                "access_documentation_url": clean(source["access_documentation_url"]),
                "institutional_status": clean(source["institutional_status"]),
                "academic_uses": clean(source["academic_uses"]),
                "limitations": clean(source["limitations"]),
            }.items()
            if value not in (None, [], "")
        }
        inserted = connection.execute(
            """
            INSERT INTO catalog.catalog_entries (
                stable_id, organization_id, entry_type, official_name, acronym, summary,
                scientific_scope, data_modalities, geographic_coverage_text,
                temporal_coverage_text, spatial_resolution_text, access_level,
                free_access, authentication_required, official_page_url,
                primary_access_url, license_text, curation_status, last_verified_at,
                additional_metadata, source_record_ids
            )
            VALUES (
                %s, %s, 'source', %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s,
                %s::jsonb, %s::jsonb
            )
            ON CONFLICT (stable_id) DO NOTHING
            RETURNING entry_id
            """,
            (
                resource_id, organization_id, clean(source["resource_name"]),
                clean(source["acronym"]), clean(source["description"]) or clean(source["resource_name"]),
                clean(source["research_areas"]), modalities,
                clean(source["geographic_coverage"]), clean(source["temporal_coverage"]),
                clean(source["spatial_resolution"]), access_level(source["access_conditions"]),
                normalized_flag(source["free_download"]),
                normalized_flag(source["authentication_required"], authentication=True),
                clean(source["homepage_url"]), clean(source["data_access_url"]),
                clean(source["license"]), status, verified_at,
                json.dumps(additional_metadata, ensure_ascii=False),
                json.dumps([{
                    "table": "staging.legacy_resources",
                    "id": resource_id,
                    "load_batch_id": batch_id,
                }], ensure_ascii=False),
            ),
        ).fetchone()
        if inserted:
            entry_id = int(inserted[0])
            inserted_entries += 1
        else:
            entry_id = int(connection.execute(
                "SELECT entry_id FROM catalog.catalog_entries WHERE stable_id = %s",
                (resource_id,),
            ).fetchone()[0])
            preserved_entries += 1

        for theme in split_pipe(source["keywords"]):
            row = connection.execute(
                """
                INSERT INTO catalog.entry_variables (
                    entry_id, term_role, source_label, search_label, verification_status
                )
                VALUES (%s, 'theme', %s, %s, %s)
                ON CONFLICT (entry_id, term_role, source_label) DO NOTHING
                RETURNING entry_variable_id
                """,
                (entry_id, theme, theme.casefold(), status),
            ).fetchone()
            inserted_themes += int(row is not None)

        if verification_url:
            row = connection.execute(
                """
                INSERT INTO catalog.entry_evidence (
                    entry_id, field_name, evidence_url, evidence_role,
                    support_note, verification_status, retrieved_at
                )
                VALUES (
                    %s, 'essential_profile', %s, 'official_page',
                    'Evidência proporcional migrada da ficha pública atual; lacunas não são inferidas.',
                    %s, %s
                )
                ON CONFLICT DO NOTHING
                RETURNING evidence_id
                """,
                (entry_id, verification_url, status, verified_at),
            ).fetchone()
            inserted_evidence += int(row is not None)

    return {
        "inserted_entries": inserted_entries,
        "preserved_entries": preserved_entries,
        "inserted_themes": inserted_themes,
        "inserted_evidence": inserted_evidence,
    }


def validate(connection, batch_id: int) -> dict[str, object]:
    expected = int(connection.execute(
        "SELECT count(*) FROM staging.legacy_resources WHERE load_batch_id = %s", (batch_id,)
    ).fetchone()[0])
    entries = int(connection.execute(
        "SELECT count(*) FROM catalog.catalog_entries WHERE stable_id ~ '^DR[0-9]{4,}$'"
    ).fetchone()[0])
    missing = int(connection.execute(
        """
        SELECT count(*)
        FROM staging.legacy_resources r
        LEFT JOIN catalog.catalog_entries e ON e.stable_id = r.resource_id
        WHERE r.load_batch_id = %s AND e.entry_id IS NULL
        """, (batch_id,)
    ).fetchone()[0])
    duplicate_names = int(connection.execute(
        """
        SELECT count(*) FROM (
            SELECT stable_id FROM catalog.catalog_entries
            WHERE stable_id ~ '^DR[0-9]{4,}$'
            GROUP BY stable_id HAVING count(*) > 1
        ) d
        """
    ).fetchone()[0])
    unlinked_org = int(connection.execute(
        """
        SELECT count(*) FROM catalog.catalog_entries
        WHERE stable_id ~ '^DR[0-9]{4,}$' AND organization_id IS NULL
        """
    ).fetchone()[0])
    theme_count = int(connection.execute(
        "SELECT count(*) FROM catalog.entry_variables WHERE term_role = 'theme'"
    ).fetchone()[0])
    evidence_count = int(connection.execute(
        "SELECT count(*) FROM catalog.entry_evidence WHERE field_name = 'essential_profile'"
    ).fetchone()[0])
    connector_exists = bool(connection.execute(
        "SELECT to_regclass('catalog.connector_profiles') IS NOT NULL"
    ).fetchone()[0])

    essential_fields = {
        "organization": "organization_id",
        "name": "official_name",
        "summary": "summary",
        "scope": "scientific_scope",
        "modalities": "data_modalities",
        "spatial_coverage": "geographic_coverage_text",
        "temporal_coverage": "temporal_coverage_text",
        "spatial_resolution": "spatial_resolution_text",
        "access": "primary_access_url",
        "official_page": "official_page_url",
        "license": "license_text",
        "verification_date": "last_verified_at",
    }
    coverage: dict[str, int] = {}
    for label, column in essential_fields.items():
        if column == "data_modalities":
            sql = (
                "SELECT count(*) FROM catalog.catalog_entries "
                "WHERE stable_id ~ '^DR[0-9]{4,}$' AND cardinality(data_modalities) > 0"
            )
        else:
            sql = (
                "SELECT count(*) FROM catalog.catalog_entries "
                f"WHERE stable_id ~ '^DR[0-9]{{4,}}$' AND {column} IS NOT NULL"
            )
        coverage[label] = int(connection.execute(sql).fetchone()[0])

    failures = {
        "expected_entries_mismatch": (entries != expected),
        "missing_entries": (missing != 0),
        "duplicate_stable_ids": (duplicate_names != 0),
        "unlinked_organizations": (unlinked_org != 0),
        "themes_absent": (theme_count == 0),
        "evidence_below_entries": (evidence_count < expected),
        "connector_profile_created_without_selected_use_case": connector_exists,
    }
    active_failures = [name for name, failed in failures.items() if failed]
    if active_failures:
        raise ValueError(f"núcleo mínimo inválido: {', '.join(active_failures)}")

    return {
        "batch_id": batch_id,
        "catalog_entries": entries,
        "expected_from_sources": expected,
        "themes": theme_count,
        "evidence_rows": evidence_count,
        "connector_profiles_present": connector_exists,
        "essential_field_coverage": coverage,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    psycopg = import_psycopg()
    try:
        with psycopg.connect(args.database_url) as connection:
            batch_id = latest_successful_batch(connection)
            promotion = None
            if not args.validate_only:
                promotion = promote(connection, batch_id)
                connection.commit()
            result = validate(connection, batch_id)
            print(json.dumps({"promotion": promotion, "validation": result}, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
