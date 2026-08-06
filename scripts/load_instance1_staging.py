#!/usr/bin/env python3
"""Validate and load the current catalog CSVs into the Instance 1 staging schema."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
SCHEMA_FILES = (
    ROOT / "database" / "schema" / "001_instance1_core.sql",
    ROOT / "database" / "schema" / "002_legacy_staging.sql",
    ROOT / "database" / "schema" / "003_staging_batches.sql",
)
DEFAULT_MAPPING = ROOT / "database" / "mappings" / "pilot_entity_resolution.csv"


@dataclass(frozen=True)
class CsvSpec:
    name: str
    path: Path
    table: str
    id_field: str
    columns: tuple[str, ...]


SPECS = (
    CsvSpec(
        name="resources",
        path=ROOT / "data" / "data_resources.csv",
        table="staging.legacy_resources",
        id_field="resource_id",
        columns=(
            "resource_id", "resource_name", "acronym", "official_identity",
            "description", "homepage_url", "data_access_url", "research_areas",
            "keywords", "data_product_types", "data_formats", "visualization_types",
            "geographic_coverage", "covers_brazil", "spatial_resolution",
            "temporal_coverage", "temporal_resolution", "data_sources",
            "free_download", "access_conditions", "programmatic_access",
            "access_protocols", "authentication_required",
            "access_documentation_url", "license", "institutional_status",
            "owner_or_manager", "academic_uses", "limitations",
            "academic_evidence_type", "academic_evidence_url",
            "academic_evidence_note", "verification_url", "last_verified",
        ),
    ),
    CsvSpec(
        name="products",
        path=ROOT / "data" / "data_products.csv",
        table="staging.legacy_products",
        id_field="product_id",
        columns=(
            "product_id", "resource_id", "product_name", "product_acronym",
            "product_family", "product_kind", "product_description",
            "research_areas", "keywords", "geographic_coverage", "covers_brazil",
            "spatial_support", "spatial_resolution", "temporal_coverage",
            "temporal_resolution", "update_frequency", "product_status",
            "version_or_collection", "enumeration_scope", "product_page_url",
            "methodology_url", "primary_or_derived", "limitations", "last_verified",
        ),
    ),
    CsvSpec(
        name="distributions",
        path=ROOT / "data" / "product_distributions.csv",
        table="staging.legacy_distributions",
        id_field="distribution_id",
        columns=(
            "distribution_id", "product_id", "distribution_name", "access_url",
            "format", "access_protocol", "access_tool", "free_download",
            "authentication_required", "access_conditions", "license",
            "provider_attribution_required", "subset_support", "notes",
            "last_verified",
        ),
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(spec: CsvSpec) -> list[dict[str, str]]:
    if not spec.path.exists():
        raise ValueError(f"arquivo ausente: {spec.path.relative_to(ROOT)}")
    with spec.path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        actual = tuple(reader.fieldnames or ())
        if actual != spec.columns:
            missing = [field for field in spec.columns if field not in actual]
            extra = [field for field in actual if field not in spec.columns]
            raise ValueError(
                f"{spec.path.name}: cabeçalho divergente; "
                f"ausentes={missing or 'nenhum'} extras={extra or 'nenhum'}"
            )
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]

    ids = [row[spec.id_field] for row in rows]
    empty = [index + 2 for index, value in enumerate(ids) if not value]
    if empty:
        raise ValueError(f"{spec.path.name}: IDs vazios nas linhas {empty}")
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        raise ValueError(f"{spec.path.name}: IDs duplicados: {duplicates}")
    return rows


def validate_relations(data: dict[str, list[dict[str, str]]]) -> None:
    resources = {row["resource_id"] for row in data["resources"]}
    products = {row["product_id"] for row in data["products"]}
    orphan_products = sorted(
        row["product_id"] for row in data["products"]
        if row["resource_id"] not in resources
    )
    orphan_distributions = sorted(
        row["distribution_id"] for row in data["distributions"]
        if row["product_id"] not in products
    )
    if orphan_products:
        raise ValueError(f"produtos com resource_id inexistente: {orphan_products}")
    if orphan_distributions:
        raise ValueError(
            f"distribuições com product_id inexistente: {orphan_distributions}"
        )


def read_mapping(path: Path, product_ids: set[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"mapeamento ausente: {path.relative_to(ROOT)}")
    expected = (
        "legacy_product_id", "resolved_entity_type", "canonical_name",
        "target_model_action", "resolution_rationale",
    )
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected:
            raise ValueError(f"{path.name}: cabeçalho esperado {expected}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]

    mapped = [row["legacy_product_id"] for row in rows]
    duplicates = sorted({value for value in mapped if mapped.count(value) > 1})
    if duplicates:
        raise ValueError(f"{path.name}: product_ids duplicados: {duplicates}")
    unknown = sorted(set(mapped) - product_ids)
    missing = sorted(product_ids - set(mapped))
    if unknown or missing:
        raise ValueError(
            f"{path.name}: cobertura inválida; desconhecidos={unknown or 'nenhum'} "
            f"ausentes={missing or 'nenhum'}"
        )
    allowed = {
        "product", "product_family", "source", "distribution",
        "access_capability", "unknown",
    }
    invalid = sorted(
        row["legacy_product_id"] for row in rows
        if row["resolved_entity_type"] not in allowed
    )
    if invalid:
        raise ValueError(f"{path.name}: tipos inválidos para {invalid}")
    return rows


def build_manifest(
    data: dict[str, list[dict[str, str]]],
    hashes: dict[str, str],
    mapping: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "loader_version": "1.0.0",
        "files": {
            spec.name: {
                "path": str(spec.path.relative_to(ROOT)),
                "sha256": hashes[spec.name],
                "rows": len(data[spec.name]),
            }
            for spec in SPECS
        },
        "relations": {
            "resource_ids": len({row["resource_id"] for row in data["resources"]}),
            "product_ids": len({row["product_id"] for row in data["products"]}),
            "distribution_ids": len(
                {row["distribution_id"] for row in data["distributions"]}
            ),
            "orphan_products": 0,
            "orphan_distributions": 0,
        },
        "pilot_resolution": {
            "mapped_rows": len(mapping),
            "by_type": {
                entity_type: sum(
                    row["resolved_entity_type"] == entity_type for row in mapping
                )
                for entity_type in sorted(
                    {row["resolved_entity_type"] for row in mapping}
                )
            },
        },
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


def apply_schema(connection) -> None:
    for path in SCHEMA_FILES:
        if not path.exists():
            raise ValueError(f"migration ausente: {path.relative_to(ROOT)}")
        connection.execute(path.read_text(encoding="utf-8"))


def same_successful_batch(connection, hashes: dict[str, str]) -> int | None:
    row = connection.execute(
        """
        SELECT batch_id
        FROM staging.load_batches
        WHERE status = 'successful'
          AND resource_file_hash = %s
          AND product_file_hash = %s
          AND distribution_file_hash = %s
        ORDER BY batch_id DESC
        LIMIT 1
        """,
        (
            hashes["resources"],
            hashes["products"],
            hashes["distributions"],
        ),
    ).fetchone()
    return int(row[0]) if row else None


def create_batch(
    connection,
    data: dict[str, list[dict[str, str]]],
    hashes: dict[str, str],
    repository_sha: str | None,
) -> int:
    row = connection.execute(
        """
        INSERT INTO staging.load_batches (
            status, loader_version, repository_sha,
            resource_file_name, resource_file_hash, resource_row_count,
            product_file_name, product_file_hash, product_row_count,
            distribution_file_name, distribution_file_hash,
            distribution_row_count
        )
        VALUES (
            'loading', '1.0.0', %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s
        )
        RETURNING batch_id
        """,
        (
            repository_sha,
            str(SPECS[0].path.relative_to(ROOT)), hashes["resources"],
            len(data["resources"]),
            str(SPECS[1].path.relative_to(ROOT)), hashes["products"],
            len(data["products"]),
            str(SPECS[2].path.relative_to(ROOT)), hashes["distributions"],
            len(data["distributions"]),
        ),
    ).fetchone()
    return int(row[0])


def copy_rows(
    connection,
    spec: CsvSpec,
    rows: Sequence[dict[str, str]],
    batch_id: int,
    source_hash: str,
) -> None:
    columns = (
        "load_batch_id",
        *spec.columns,
        "source_filename",
        "source_file_hash",
    )
    sql = f"COPY {spec.table} ({', '.join(columns)}) FROM STDIN"
    with connection.cursor().copy(sql) as copy:
        for row in rows:
            copy.write_row(
                (
                    batch_id,
                    *(row[column] for column in spec.columns),
                    str(spec.path.relative_to(ROOT)),
                    source_hash,
                )
            )


def apply_mapping(
    connection,
    batch_id: int,
    mapping: Sequence[dict[str, str]],
) -> None:
    for row in mapping:
        updated = connection.execute(
            """
            UPDATE staging.legacy_products
            SET resolved_entity_type = %s,
                resolution_rationale = %s,
                migration_status = 'mapped',
                migration_notes = %s
            WHERE load_batch_id = %s
              AND product_id = %s
            """,
            (
                row["resolved_entity_type"],
                row["resolution_rationale"],
                row["target_model_action"],
                batch_id,
                row["legacy_product_id"],
            ),
        ).rowcount
        if updated != 1:
            raise ValueError(
                f"mapeamento não encontrou exatamente uma linha: "
                f"{row['legacy_product_id']}"
            )
        if row["resolved_entity_type"] != "product":
            connection.execute(
                """
                INSERT INTO staging.migration_issues (
                    load_batch_id, entity_type, legacy_id, issue_code,
                    severity, field_name, current_value, issue_description,
                    proposed_action
                )
                VALUES (
                    %s, 'product', %s, 'ENTITY_RECLASSIFICATION_REQUIRED',
                    'warning', 'product_kind', %s, %s, %s
                )
                ON CONFLICT (
                    load_batch_id, entity_type, legacy_id, issue_code
                ) DO NOTHING
                """,
                (
                    batch_id,
                    row["legacy_product_id"],
                    row["resolved_entity_type"],
                    row["resolution_rationale"],
                    row["target_model_action"],
                ),
            )


def verify_batch(connection, batch_id: int, expected: dict[str, int]) -> None:
    checks = {
        "resources": "staging.legacy_resources",
        "products": "staging.legacy_products",
        "distributions": "staging.legacy_distributions",
    }
    for name, table in checks.items():
        count = connection.execute(
            f"SELECT count(*) FROM {table} WHERE load_batch_id = %s",
            (batch_id,),
        ).fetchone()[0]
        if count != expected[name]:
            raise ValueError(
                f"batch {batch_id}: {name}={count}; esperado={expected[name]}"
            )

    orphan_products = connection.execute(
        """
        SELECT count(*)
        FROM staging.legacy_products p
        LEFT JOIN staging.legacy_resources r
          ON r.load_batch_id = p.load_batch_id
         AND r.resource_id = p.resource_id
        WHERE p.load_batch_id = %s
          AND r.resource_id IS NULL
        """,
        (batch_id,),
    ).fetchone()[0]
    orphan_distributions = connection.execute(
        """
        SELECT count(*)
        FROM staging.legacy_distributions d
        LEFT JOIN staging.legacy_products p
          ON p.load_batch_id = d.load_batch_id
         AND p.product_id = d.product_id
        WHERE d.load_batch_id = %s
          AND p.product_id IS NULL
        """,
        (batch_id,),
    ).fetchone()[0]
    unresolved = connection.execute(
        """
        SELECT count(*)
        FROM staging.legacy_products
        WHERE load_batch_id = %s
          AND (resolved_entity_type IS NULL OR resolved_entity_type = 'unknown')
        """,
        (batch_id,),
    ).fetchone()[0]
    if orphan_products or orphan_distributions or unresolved:
        raise ValueError(
            f"batch {batch_id}: órfãos_produtos={orphan_products}, "
            f"órfãos_distribuições={orphan_distributions}, "
            f"produtos_não_resolvidos={unresolved}"
        )


def load_database(
    database_url: str,
    data: dict[str, list[dict[str, str]]],
    hashes: dict[str, str],
    mapping: list[dict[str, str]],
    initialize: bool,
    repository_sha: str | None,
) -> dict[str, object]:
    psycopg = import_psycopg()
    expected = {name: len(rows) for name, rows in data.items()}
    with psycopg.connect(database_url) as connection:
        if initialize:
            apply_schema(connection)
        existing = same_successful_batch(connection, hashes)
        if existing is not None:
            connection.rollback()
            return {
                "status": "no_op",
                "batch_id": existing,
                "reason": "os três hashes já constam em lote bem-sucedido",
            }

        batch_id = create_batch(
            connection, data, hashes, repository_sha=repository_sha
        )
        for spec in SPECS:
            copy_rows(
                connection,
                spec,
                data[spec.name],
                batch_id,
                hashes[spec.name],
            )
        apply_mapping(connection, batch_id, mapping)
        verify_batch(connection, batch_id, expected)
        connection.execute(
            """
            UPDATE staging.load_batches
            SET status = 'successful',
                completed_at = now()
            WHERE batch_id = %s
            """,
            (batch_id,),
        )
        connection.commit()
        return {"status": "loaded", "batch_id": batch_id}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="valida os arquivos, relações e mapeamento sem acessar PostgreSQL",
    )
    parser.add_argument(
        "--database-url",
        default=DEFAULT_DATABASE_URL,
        help="DSN PostgreSQL; padrão: variável DATABASE_URL ou banco local",
    )
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="aplica 001, 002 e 003 antes da carga",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=DEFAULT_MAPPING,
        help="CSV de resolução das linhas piloto",
    )
    parser.add_argument(
        "--repository-sha",
        default=os.environ.get("GITHUB_SHA"),
        help="SHA de origem registrado no lote",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = {spec.name: read_csv(spec) for spec in SPECS}
        validate_relations(data)
        hashes = {spec.name: sha256_file(spec.path) for spec in SPECS}
        mapping = read_mapping(
            args.mapping,
            {row["product_id"] for row in data["products"]},
        )
        manifest = build_manifest(data, hashes, mapping)
        if args.check_only:
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
            return 0

        result = load_database(
            args.database_url,
            data,
            hashes,
            mapping,
            initialize=args.initialize,
            repository_sha=args.repository_sha,
        )
        print(
            json.dumps(
                {"validation": manifest, "database": result},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
