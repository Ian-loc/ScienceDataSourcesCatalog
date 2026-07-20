#!/usr/bin/env python3
"""Valida a fila DATA1-BR-CLOSE sem usar contagens incomparáveis entre lotes."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "migration" / "external_review_queue_contract.json"
SEPARATOR = " | "
EXPECTED_HEADER = [
    "execution_rank", "review_track", "execution_wave", "scientific_priority_tier",
    "resource_id", "resource_name", "source_batch", "batch_rank", "impact_level",
    "scientific_risk_level", "link_role_status", "access_documentation_status",
    "review_focus", "queue_status", "evidence_record_count", "decision", "decision_notes",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(SEPARATOR) if item.strip()]


def scientific_tier(impact: str, risk: str) -> str:
    if impact == "muito_alta" and risk == "muito_alto":
        return "P0"
    if (impact, risk) in {("muito_alta", "alto"), ("alta", "muito_alto")}:
        return "P1"
    if impact == "alta" and risk == "alto":
        return "P2"
    return "P3"


def execution_wave(tier: str, link_status: str, access_status: str, scope: bool) -> str:
    if scope:
        return "G0"
    if tier == "P0" and link_status == "same_destination_pending_review":
        return "W1"
    if tier == "P0" and (link_status == "role_review_required" or access_status == "ausente"):
        return "W2"
    if tier == "P0":
        return "W3"
    if tier == "P1":
        return "W4"
    return "W5"


def main() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if contract.get("phase") != "DATA1-BR-CLOSE" or contract.get("expected_records") != 35:
        fail("contrato DATA1-BR-CLOSE inválido")

    registry = json.loads((ROOT / contract["batch_registry"]).read_text(encoding="utf-8"))
    active = registry.get("active_batches", [])
    if [entry.get("batch") for entry in active] != contract["expected_source_batches"]:
        fail("fila somente fecha com BR1–BR5 ativos na ordem planejada")

    source_rows: dict[str, dict[str, str]] = {}
    for entry in active:
        _, rows = read_csv(ROOT / entry["review_matrix"])
        if len(rows) != 7:
            fail(f"{entry['batch']}: matriz deve conter sete linhas")
        for row in rows:
            resource_id = row["resource_id"]
            if resource_id in source_rows:
                fail(f"ID repetido entre lotes: {resource_id}")
            item = dict(row)
            item["source_batch"] = entry["batch"]
            source_rows[resource_id] = item

    _, data1b_rows = read_csv(ROOT / registry["data1b_matrix"])
    manual_ids = {row["resource_id"] for row in data1b_rows if row["migration_status"] == "revisão_manual"}
    if set(source_rows) != manual_ids or len(manual_ids) != 35:
        fail("BR1–BR5 devem corresponder aos 35 casos revisão_manual")

    audit = json.loads((ROOT / contract["link_role_audit"]).read_text(encoding="utf-8"))
    same_pending_ids = {
        item["resource_id"] for item in audit.get("records_requiring_review", [])
        if item.get("status") == "same_destination_pending_review"
    }
    role_flags = set(contract["role_review_flags"])
    scope_ids = set(contract["scope_decision_required_ids"])
    wave_order = {wave: index for index, wave in enumerate(contract["wave_order"])}

    evidence_header, evidence_rows = read_csv(ROOT / contract["evidence_table"])
    if "resource_id" not in evidence_header:
        fail("tabela de evidências sem resource_id")
    evidence_counts = Counter(row["resource_id"] for row in evidence_rows)

    expected: list[dict[str, str]] = []
    for resource_id, source in source_rows.items():
        flags = set(split_values(source["risk_flags"]))
        if resource_id in same_pending_ids:
            link_status = "same_destination_pending_review"
        elif role_flags.intersection(flags):
            link_status = "role_review_required"
        else:
            link_status = "separate_destinations"
        access_status = "documentada" if source["existing_access_documentation_url"].strip() else "ausente"
        tier = scientific_tier(source["impact_level"], source["scientific_risk_level"])
        scope = resource_id in scope_ids
        wave = execution_wave(tier, link_status, access_status, scope)
        expected.append({
            "review_track": "scope_decision" if scope else "external_evidence",
            "execution_wave": wave,
            "scientific_priority_tier": tier,
            "resource_id": resource_id,
            "resource_name": source["resource_name"],
            "source_batch": source["source_batch"],
            "batch_rank": source["selection_rank"],
            "impact_level": source["impact_level"],
            "scientific_risk_level": source["scientific_risk_level"],
            "link_role_status": link_status,
            "access_documentation_status": access_status,
        })

    expected.sort(key=lambda item: (
        wave_order[item["execution_wave"]],
        0 if item["access_documentation_status"] == "ausente" else 1,
        item["source_batch"], int(item["batch_rank"]), item["resource_id"],
    ))

    queue_header, queue_rows = read_csv(ROOT / contract["queue"])
    if queue_header != EXPECTED_HEADER:
        fail("cabeçalho da fila diverge do contrato")
    if len(queue_rows) != 35 or len({row["resource_id"] for row in queue_rows}) != 35:
        fail("fila deve conter 35 IDs únicos")

    compare_fields = [
        "review_track", "execution_wave", "scientific_priority_tier", "resource_id",
        "resource_name", "source_batch", "batch_rank", "impact_level",
        "scientific_risk_level", "link_role_status", "access_documentation_status",
    ]
    allowed_status = set(contract["queue_status_values"])
    allowed_decisions = set(contract["decision_values"])

    for rank, (row, expected_row) in enumerate(zip(queue_rows, expected), start=1):
        if row["execution_rank"] != str(rank):
            fail(f"linha {rank + 1}: execution_rank incorreto")
        for field in compare_fields:
            if row[field] != expected_row[field]:
                fail(f"linha {rank + 1}: {field} diverge das fontes versionadas")
        if len([item for item in row["review_focus"].split(";") if item.strip()]) < 4:
            fail(f"linha {rank + 1}: review_focus insuficiente")
        if row["queue_status"] not in allowed_status:
            fail(f"linha {rank + 1}: queue_status inválido")
        if row["decision"] not in allowed_decisions or not row["decision_notes"].strip():
            fail(f"linha {rank + 1}: decisão inválida ou sem justificativa")

        evidence_count = evidence_counts.get(row["resource_id"], 0)
        if row["evidence_record_count"] != str(evidence_count):
            fail(f"linha {rank + 1}: evidence_record_count divergente")
        if row["queue_status"].startswith("aguardando_") and evidence_count != 0:
            fail(f"linha {rank + 1}: status de espera não aceita evidência registrada")
        if row["queue_status"] in {"em_revisão", "revisada"} and evidence_count == 0:
            fail(f"linha {rank + 1}: revisão exige evidência")
        if row["review_track"] == "scope_decision" and "escopo" not in row["decision_notes"].casefold() and "elegibilidade" not in row["decision_notes"].casefold():
            fail(f"linha {rank + 1}: portão de escopo sem justificativa")

    tier_counts = Counter(row["scientific_priority_tier"] for row in queue_rows)
    for tier in ("P0", "P1", "P2", "P3"):
        tier_counts.setdefault(tier, 0)
    if dict(tier_counts) != contract["expected_tier_counts"]:
        fail(f"contagem científica divergente: {dict(tier_counts)}")
    wave_counts = Counter(row["execution_wave"] for row in queue_rows)
    if dict(wave_counts) != contract["expected_wave_counts"]:
        fail(f"contagem por onda divergente: {dict(wave_counts)}")

    canonical_header, canonical_rows = read_csv(ROOT / contract["canonical_csv"])
    if len(canonical_header) != 34 or len(canonical_rows) != 51:
        fail("DATA1-BR-CLOSE não pode alterar o CSV canônico 51 × 34")

    print(
        "OK: DATA1-BR-CLOSE validado — prioridade científica separada da onda operacional; "
        "G0=1, W1=7, W2=9, W3=7, W4=8, W5=3; evidência longa vinculada; CSV preservado"
    )


if __name__ == "__main__":
    main()
