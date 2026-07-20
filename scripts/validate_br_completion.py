#!/usr/bin/env python3
"""Confirma que BR1–BR5 cobrem exatamente todos os casos de revisão manual."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "migration" / "br_batch_registry.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    planned = registry.get("planned_batches", [])
    active = registry.get("active_batches", [])
    active_names = [entry.get("batch") for entry in active]

    if active_names != planned or planned != ["BR1", "BR2", "BR3", "BR4", "BR5"]:
        fail("a revisão manual somente fecha com BR1–BR5 ativos na ordem planejada")

    selected_ids: list[str] = []
    for entry in active:
        contract_path = ROOT / entry["contract"]
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        selected_ids.extend(contract.get("expected_resource_ids", []))

    if len(selected_ids) != 35 or len(set(selected_ids)) != 35:
        fail("os cinco lotes devem reunir exatamente 35 IDs únicos")

    data1b_path = ROOT / registry["data1b_matrix"]
    with data1b_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    manual_ids = {
        row["resource_id"]
        for row in rows
        if row["migration_status"] == "revisão_manual"
    }
    ready_ids = {
        row["resource_id"]
        for row in rows
        if row["migration_status"] == "pronto_para_migração"
    }

    if len(manual_ids) != 35 or len(ready_ids) != 16:
        fail("DATA1-B deve preservar 35 casos manuais e 16 prontos")
    if set(selected_ids) != manual_ids:
        missing = sorted(manual_ids - set(selected_ids))
        unexpected = sorted(set(selected_ids) - manual_ids)
        fail(f"cobertura BR divergente; ausentes={missing}; indevidos={unexpected}")

    print(
        "OK: DATA1-BR concluído — BR1–BR5 cobrem exatamente os 35 casos manuais; "
        "16 registros prontos permanecem fora dos lotes"
    )


if __name__ == "__main__":
    main()
