#!/usr/bin/env python3
"""Apply evidence-backed, field-level enrichment to minimum-core catalog entries.

The enrichment layer is intentionally small and additive. It does not create new
catalog entities, does not enumerate external assets, and updates only explicitly
listed essential-profile fields backed by proportional evidence.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
DEFAULT_INPUT = Path("data/instance1_entry_enrichment_batch01.json")

ALLOWED_FIELDS = {
    "update_frequency_text",
    "free_access",
    "authentication_required",
    "metadata_url",
    "methodology_url",
    "citation_text",
    "citation_url",
}
ALLOWED_EVIDENCE_FIELDS = ALLOWED_FIELDS | {"citation"}
ALLOWED_EVIDENCE_ROLES = {
    "official_page", "official_metadata", "methodology", "license",
    "citation", "access", "other",
}
ALLOWED_STATUSES = {
    "needs_review", "partially_verified", "verified", "not_found", "not_applicable",
}


def import_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "psycopg não instalado. Execute: python -m pip install -r database/requirements.txt"
        ) from exc
    return psycopg


def load_records(path: Path) -> list[dict[str, object]]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("arquivo de enriquecimento deve conter uma lista JSON")
    return records


def validate_record(record: dict[str, object]) -> None:
    stable_id = record.get("stable_id")
    if not isinstance(stable_id, str) or not stable_id.startswith("DR"):
        raise ValueError(f"stable_id inválido: {stable_id!r}")

    fields = record.get("fields", {})
    if not isinstance(fields, dict):
        raise ValueError(f"fields inválido para {stable_id}")
    unsupported = sorted(set(fields) - ALLOWED_FIELDS)
    if unsupported:
        raise ValueError(f"campos não permitidos para {stable_id}: {unsupported}")
    if any(value is None for value in fields.values()):
        raise ValueError(f"campos explícitos não podem receber null em {stable_id}")

    evidence = record.get("evidence", [])
    if not isinstance(evidence, list) or not evidence:
        raise ValueError(f"evidência proporcional ausente para {stable_id}")
    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError(f"evidência inválida para {stable_id}")
        field_name = item.get("field_name")
        role = item.get("evidence_role")
        status = item.get("verification_status")
        url = item.get("evidence_url")
        if field_name not in ALLOWED_EVIDENCE_FIELDS:
            raise ValueError(f"campo de evidência inválido em {stable_id}: {field_name!r}")
        if role not in ALLOWED_EVIDENCE_ROLES:
            raise ValueError(f"papel de evidência inválido em {stable_id}: {role!r}")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"status de evidência inválido em {stable_id}: {status!r}")
        if url is None and status not in {"not_found", "not_applicable"}:
            raise ValueError(
                f"evidence_url só pode ser null para not_found/not_applicable em {stable_id}"
            )


def apply(connection, records: list[dict[str, object]]) -> dict[str, int]:
    updated_entries = 0
    inserted_evidence = 0
    updated_evidence = 0
    preserved_evidence = 0

    for record in records:
        validate_record(record)
        stable_id = str(record["stable_id"])
        fields = dict(record.get("fields", {}))
        selected = ["entry_id", *fields.keys()]
        row = connection.execute(
            f"SELECT {', '.join(selected)} FROM catalog.catalog_entries WHERE stable_id = %s",
            (stable_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"catalog_entry não localizada: {stable_id}")
        current = dict(zip(selected, row, strict=True))
        entry_id = int(current["entry_id"])

        changed_fields = {
            field: expected
            for field, expected in fields.items()
            if current.get(field) != expected
        }
        if changed_fields:
            assignments = ", ".join(f"{field} = %s" for field in changed_fields)
            values = list(changed_fields.values())
            values.append(stable_id)
            connection.execute(
                f"UPDATE catalog.catalog_entries SET {assignments}, updated_at = now() WHERE stable_id = %s",
                values,
            )
            updated_entries += 1

        for evidence in record.get("evidence", []):
            item = dict(evidence)
            existing = connection.execute(
                """
                SELECT evidence_id, support_note, verification_status
                FROM catalog.entry_evidence
                WHERE entry_id = %s
                  AND COALESCE(field_name, '') = COALESCE(%s, '')
                  AND evidence_role = %s
                  AND COALESCE(evidence_url, '') = COALESCE(%s, '')
                """,
                (
                    entry_id,
                    item.get("field_name"),
                    item.get("evidence_role"),
                    item.get("evidence_url"),
                ),
            ).fetchone()

            if not existing:
                connection.execute(
                    """
                    INSERT INTO catalog.entry_evidence (
                        entry_id, field_name, evidence_url, evidence_role,
                        support_note, verification_status, retrieved_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    """,
                    (
                        entry_id,
                        item.get("field_name"),
                        item.get("evidence_url"),
                        item.get("evidence_role"),
                        item.get("support_note"),
                        item.get("verification_status"),
                    ),
                )
                inserted_evidence += 1
                continue

            evidence_id, support_note, verification_status = existing
            if (
                support_note != item.get("support_note")
                or verification_status != item.get("verification_status")
            ):
                connection.execute(
                    """
                    UPDATE catalog.entry_evidence
                    SET support_note = %s,
                        verification_status = %s,
                        retrieved_at = CURRENT_DATE,
                        updated_at = now()
                    WHERE evidence_id = %s
                    """,
                    (
                        item.get("support_note"),
                        item.get("verification_status"),
                        evidence_id,
                    ),
                )
                updated_evidence += 1
            else:
                preserved_evidence += 1

    return {
        "records": len(records),
        "updated_entries": updated_entries,
        "inserted_evidence": inserted_evidence,
        "updated_evidence": updated_evidence,
        "preserved_evidence": preserved_evidence,
    }


def validate_materialized(connection, records: list[dict[str, object]]) -> dict[str, object]:
    verified: dict[str, dict[str, object]] = {}
    for record in records:
        validate_record(record)
        stable_id = str(record["stable_id"])
        fields = dict(record.get("fields", {}))
        selected = ", ".join(["stable_id", *fields.keys()])
        row = connection.execute(
            f"SELECT {selected} FROM catalog.catalog_entries WHERE stable_id = %s",
            (stable_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"catalog_entry ausente após enriquecimento: {stable_id}")
        values = dict(zip(["stable_id", *fields.keys()], row, strict=True))
        mismatches = {
            key: {"expected": expected, "actual": values.get(key)}
            for key, expected in fields.items()
            if values.get(key) != expected
        }
        if mismatches:
            raise ValueError(f"enriquecimento não materializado em {stable_id}: {mismatches}")

        entry_id = int(connection.execute(
            "SELECT entry_id FROM catalog.catalog_entries WHERE stable_id = %s",
            (stable_id,),
        ).fetchone()[0])
        evidence_expected = list(record.get("evidence", []))
        matched_evidence = 0
        for expected in evidence_expected:
            item = dict(expected)
            evidence_row = connection.execute(
                """
                SELECT support_note, verification_status
                FROM catalog.entry_evidence
                WHERE entry_id = %s
                  AND COALESCE(field_name, '') = COALESCE(%s, '')
                  AND evidence_role = %s
                  AND COALESCE(evidence_url, '') = COALESCE(%s, '')
                """,
                (
                    entry_id,
                    item.get("field_name"),
                    item.get("evidence_role"),
                    item.get("evidence_url"),
                ),
            ).fetchone()
            if not evidence_row:
                raise ValueError(
                    f"evidência esperada ausente em {stable_id}: "
                    f"{item.get('field_name')} / {item.get('evidence_role')} / {item.get('evidence_url')}"
                )
            support_note, verification_status = evidence_row
            if support_note != item.get("support_note") or verification_status != item.get("verification_status"):
                raise ValueError(
                    f"evidência divergente em {stable_id}: "
                    f"{item.get('field_name')} / {item.get('evidence_role')}"
                )
            matched_evidence += 1

        verified[stable_id] = {
            "fields": len(fields),
            "evidence_expected": len(evidence_expected),
            "evidence_matched_exactly": matched_evidence,
        }
    return verified


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = load_records(args.input)
    psycopg = import_psycopg()
    with psycopg.connect(args.database_url) as connection:
        if args.validate_only:
            result = validate_materialized(connection, records)
        else:
            result = apply(connection, records)
            connection.commit()
            result["materialized"] = validate_materialized(connection, records)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
