#!/usr/bin/env python3
"""Valida evidências externas em formato longo sem alterar o CSV canônico."""
from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "migration" / "external_review_evidence_contract.json"
EXPECTED_HEADER = [
    "evidence_id", "resource_id", "review_dimension", "claim_reviewed",
    "current_catalog_value", "observed_official_value", "evidence_url",
    "evidence_source_type", "official_source", "accessed_at", "reviewer",
    "supports_current_value", "proposed_action", "proposed_value", "notes",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def valid_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def valid_date(value: str) -> bool:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return len(value) == 10 and parsed <= date.today()


def main() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    header, rows = read_csv(ROOT / contract["table"])
    if header != EXPECTED_HEADER:
        fail("cabeçalho da tabela de evidências diverge do contrato")

    queue_header, queue_rows = read_csv(ROOT / contract["queue"])
    if "resource_id" not in queue_header:
        fail("fila externa sem resource_id")
    queue_ids = {row["resource_id"] for row in queue_rows}
    if len(queue_ids) != 35:
        fail("fila externa deve conter 35 IDs antes da revisão")

    if not rows:
        if contract.get("allow_empty_initial_table") is not True:
            fail("tabela de evidências vazia não permitida")
        print("OK: tabela de evidências externa criada e vazia; revisão factual ainda não iniciada")
        return

    dimensions = set(contract["review_dimensions"])
    source_types = set(contract["evidence_source_types"])
    supports = set(contract["support_values"])
    actions = set(contract["proposed_actions"])
    seen_ids: set[str] = set()

    for line, row in enumerate(rows, start=2):
        evidence_id = row["evidence_id"].strip()
        if not re.fullmatch(r"EVID\d{5}", evidence_id):
            fail(f"linha {line}: evidence_id deve usar EVID00001")
        if evidence_id in seen_ids:
            fail(f"linha {line}: evidence_id duplicado")
        seen_ids.add(evidence_id)

        if row["resource_id"] not in queue_ids:
            fail(f"linha {line}: resource_id fora da fila externa")
        if row["review_dimension"] not in dimensions:
            fail(f"linha {line}: review_dimension inválida")
        if row["evidence_source_type"] not in source_types:
            fail(f"linha {line}: evidence_source_type inválido")
        if row["supports_current_value"] not in supports:
            fail(f"linha {line}: supports_current_value inválido")
        if row["proposed_action"] not in actions:
            fail(f"linha {line}: proposed_action inválida")
        if not valid_https(row["evidence_url"].strip()):
            fail(f"linha {line}: evidence_url deve ser HTTPS")
        if not valid_date(row["accessed_at"].strip()):
            fail(f"linha {line}: accessed_at deve ser data ISO não futura")

        for field in (
            "claim_reviewed", "observed_official_value", "official_source",
            "reviewer", "notes",
        ):
            if not row[field].strip():
                fail(f"linha {line}: {field} obrigatório")
        if row["proposed_action"] == "corrigir" and not row["proposed_value"].strip():
            fail(f"linha {line}: correção exige proposed_value")

    print(f"OK: {len(rows)} evidência(s) externa(s) válidas em formato longo")


if __name__ == "__main__":
    main()
