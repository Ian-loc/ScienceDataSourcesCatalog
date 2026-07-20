#!/usr/bin/env python3
"""Valida todos os lotes ativos de revisão DATA1-BR."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "migration" / "br_batch_registry.json"
SEPARATOR = " | "

EXPECTED_HEADER = [
    "resource_id",
    "resource_name",
    "selection_rank",
    "impact_level",
    "scientific_risk_level",
    "risk_flags",
    "selection_rationale",
    "internal_consistency_status",
    "internal_findings",
    "existing_verification_url",
    "existing_access_documentation_url",
    "review_dimensions",
    "external_review_status",
    "evidence_url_used",
    "reviewer",
    "reviewed_at",
    "decision",
    "notes",
]

EXPECTED_CONTRACT_RULES = {
    "exactly_seven_records_in_fixed_order",
    "all_records_must_exist_in_canonical_csv",
    "all_records_must_be_manual_review_in_data1b",
    "all_records_must_preserve_unknown_field_confidence_in_data1bx_until_external_review",
    "existing_evidence_urls_must_match_canonical_csv",
    "blocked_external_review_forbids_evidence_reviewer_and_date",
    "blocked_external_review_requires_hold_current_csv",
    "no_canonical_csv_changes_without_current_official_evidence",
    "selection_does_not_equal_validation",
}

EXPECTED_REGISTRY_RULES = {
    "active_batches_follow_planned_order",
    "resource_ids_are_unique_across_batches",
    "every_active_batch_has_exactly_seven_records",
    "every_active_batch_uses_the_same_canonical_inputs",
    "internal_audit_does_not_raise_external_confidence",
    "canonical_csv_changes_remain_forbidden_without_current_official_evidence",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        fail(f"arquivo CSV ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(SEPARATOR) if item.strip()]


def valid_https_or_blank(value: str) -> bool:
    if not value:
        return True
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def valid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return len(value) == 10


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"arquivo JSON ausente: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_batches(selected_batch: str | None = None) -> tuple[int, int]:
    registry = load_json(REGISTRY_PATH)
    if registry.get("phase") != "DATA1-BR":
        fail("registro deve identificar a fase DATA1-BR")
    if set(registry.get("rules", [])) != EXPECTED_REGISTRY_RULES:
        fail("regras do registro de lotes estão incompletas ou divergentes")

    expected_per_batch = registry.get("expected_records_per_batch")
    if expected_per_batch != 7:
        fail("cada lote DATA1-BR deve conter exatamente sete fontes")

    planned = registry.get("planned_batches", [])
    active = registry.get("active_batches", [])
    active_names = [item.get("batch") for item in active]
    if not planned or len(planned) != len(set(planned)):
        fail("planned_batches deve ser uma lista ordenada e sem duplicatas")
    if not active_names or len(active_names) != len(set(active_names)):
        fail("active_batches deve conter lotes únicos")
    if active_names != planned[: len(active_names)]:
        fail("lotes ativos devem seguir a ordem planejada sem saltos")
    if selected_batch and selected_batch not in active_names:
        fail(f"lote solicitado não está ativo: {selected_batch}")

    canonical_path = ROOT / registry["canonical_csv"]
    data1b_path = ROOT / registry["data1b_matrix"]
    data1bx_path = ROOT / registry["data1bx_matrix"]
    canonical_header, canonical_rows = read_csv(canonical_path)
    _, data1b_rows = read_csv(data1b_path)
    _, data1bx_rows = read_csv(data1bx_path)

    if len(canonical_header) != 34 or len(canonical_rows) != 51:
        fail("CSV canônico deve permanecer em 51 fontes × 34 campos")

    canonical = {row["resource_id"]: row for row in canonical_rows}
    data1b = {row["resource_id"]: row for row in data1b_rows}
    data1bx = {row["resource_id"]: row for row in data1bx_rows}
    if len(canonical) != 51 or len(data1b) != 51 or len(data1bx) != 51:
        fail("CSV, DATA1-B e DATA1-BX devem preservar 51 IDs únicos")

    selected_ids: set[str] = set()
    validated_batches = 0
    validated_records = 0

    for entry in active:
        batch = entry["batch"]
        if selected_batch and batch != selected_batch:
            continue

        contract_path = ROOT / entry["contract"]
        review_path = ROOT / entry["review_matrix"]
        contract = load_json(contract_path)

        if contract.get("phase") != "DATA1-BR" or contract.get("batch") != batch:
            fail(f"{batch}: contrato identifica fase ou lote incorreto")
        if contract.get("status") != "internal_audit_complete_external_review_blocked":
            fail(f"{batch}: contrato deve registrar auditoria interna concluída e revisão externa bloqueada")
        if entry.get("internal_audit_status") != "concluída":
            fail(f"{batch}: registro deve marcar auditoria interna concluída")
        if entry.get("external_review_status") != "bloqueada_sem_web":
            fail(f"{batch}: revisão externa deve permanecer bloqueada sem web")
        if contract.get("expected_records") != expected_per_batch:
            fail(f"{batch}: expected_records deve ser {expected_per_batch}")
        if contract.get("automatic_csv_changes_allowed") is not False:
            fail(f"{batch}: alteração automática do CSV deve permanecer proibida")
        if set(contract.get("rules", [])) != EXPECTED_CONTRACT_RULES:
            fail(f"{batch}: regras do contrato estão incompletas ou divergentes")

        for key, registry_value in (
            ("canonical_csv", registry["canonical_csv"]),
            ("data1b_matrix", registry["data1b_matrix"]),
            ("data1bx_matrix", registry["data1bx_matrix"]),
            ("review_matrix", entry["review_matrix"]),
        ):
            if contract.get(key) != registry_value:
                fail(f"{batch}: {key} diverge do registro de lotes")

        expected_ids = contract.get("expected_resource_ids", [])
        if len(expected_ids) != expected_per_batch or len(set(expected_ids)) != expected_per_batch:
            fail(f"{batch}: expected_resource_ids deve conter sete IDs únicos")
        overlap = selected_ids.intersection(expected_ids)
        if overlap:
            fail(f"{batch}: IDs já usados em outro lote: {sorted(overlap)}")
        selected_ids.update(expected_ids)

        review_header, review_rows = read_csv(review_path)
        if review_header != EXPECTED_HEADER:
            fail(f"{batch}: cabeçalho da matriz diverge do contrato comum")
        if len(review_rows) != expected_per_batch:
            fail(f"{batch}: matriz deve conter sete linhas")
        if [row["resource_id"] for row in review_rows] != expected_ids:
            fail(f"{batch}: matriz deve preservar IDs e ordem definidos no contrato")

        allowed_flags = set(contract.get("risk_flags", []))
        allowed_dimensions = set(contract.get("review_dimensions", []))
        allowed_impact = set(contract.get("impact_levels", []))
        allowed_risk = set(contract.get("scientific_risk_levels", []))
        allowed_internal = set(contract.get("internal_consistency_values", []))
        allowed_external = set(contract.get("external_review_status_values", []))
        allowed_decisions = set(contract.get("decision_values", []))
        if not all((allowed_flags, allowed_dimensions, allowed_impact, allowed_risk, allowed_internal, allowed_external, allowed_decisions)):
            fail(f"{batch}: vocabulários controlados não podem ficar vazios")

        for expected_rank, row in enumerate(review_rows, start=1):
            line = expected_rank + 1
            resource_id = row["resource_id"].strip()
            prefix = f"{batch} linha {line} ({resource_id})"

            if resource_id not in canonical or resource_id not in data1b or resource_id not in data1bx:
                fail(f"{prefix}: ID ausente em uma matriz de origem")
            if row["resource_name"].strip() != canonical[resource_id]["resource_name"].strip():
                fail(f"{prefix}: nome não corresponde ao CSV canônico")
            if row["selection_rank"].strip() != str(expected_rank):
                fail(f"{prefix}: selection_rank deve seguir a ordem do contrato")
            if row["impact_level"] not in allowed_impact:
                fail(f"{prefix}: impact_level inválido")
            if row["scientific_risk_level"] not in allowed_risk:
                fail(f"{prefix}: scientific_risk_level inválido")
            if row["internal_consistency_status"] not in allowed_internal:
                fail(f"{prefix}: internal_consistency_status inválido")
            if row["external_review_status"] not in allowed_external:
                fail(f"{prefix}: external_review_status inválido")
            if row["decision"] not in allowed_decisions:
                fail(f"{prefix}: decision inválida")

            flags = split_values(row["risk_flags"])
            dimensions = split_values(row["review_dimensions"])
            if len(flags) < 2 or len(flags) != len(set(flags)) or not set(flags).issubset(allowed_flags):
                fail(f"{prefix}: risk_flags inválidos ou insuficientes")
            if len(dimensions) < 5 or len(dimensions) != len(set(dimensions)) or not set(dimensions).issubset(allowed_dimensions):
                fail(f"{prefix}: review_dimensions inválidas ou insuficientes")

            for field in ("selection_rationale", "internal_findings", "notes"):
                if not row[field].strip():
                    fail(f"{prefix}: {field} não pode ficar vazio")

            verification_url = row["existing_verification_url"].strip()
            access_url = row["existing_access_documentation_url"].strip()
            if not valid_https_or_blank(verification_url) or not valid_https_or_blank(access_url):
                fail(f"{prefix}: URLs existentes devem ser HTTPS ou vazias")
            if verification_url != canonical[resource_id]["verification_url"].strip():
                fail(f"{prefix}: existing_verification_url diverge do CSV")
            if access_url != canonical[resource_id]["access_documentation_url"].strip():
                fail(f"{prefix}: existing_access_documentation_url diverge do CSV")

            if data1b[resource_id]["migration_status"] != "revisão_manual":
                fail(f"{prefix}: fonte deve estar em revisão_manual na DATA1-B")
            if data1bx[resource_id]["bx_review_status"] != "carregado_do_csv":
                fail(f"{prefix}: fonte deve permanecer carregada do CSV na DATA1-BX")
            if data1bx[resource_id]["bx_evidence_basis"] != "canonical_csv":
                fail(f"{prefix}: DATA1-BX deve manter base canonical_csv")

            confidence_fields = [field for field in data1bx[resource_id] if field.endswith("_confidence")]
            if not confidence_fields or any(data1bx[resource_id][field] != "desconhecida" for field in confidence_fields):
                fail(f"{prefix}: DATA1-BX deve preservar confiança desconhecida")

            if row["external_review_status"] == "bloqueada_sem_web":
                if any(row[field].strip() for field in ("evidence_url_used", "reviewer", "reviewed_at")):
                    fail(f"{prefix}: revisão bloqueada não aceita evidência, revisor ou data")
                if row["decision"] != "manter_csv_atual":
                    fail(f"{prefix}: revisão bloqueada deve manter o CSV atual")
            else:
                evidence_url = row["evidence_url_used"].strip()
                reviewed_at = row["reviewed_at"].strip()
                if evidence_url and not valid_https_or_blank(evidence_url):
                    fail(f"{prefix}: evidence_url_used deve ser HTTPS")
                if reviewed_at and not valid_iso_date(reviewed_at):
                    fail(f"{prefix}: reviewed_at deve usar YYYY-MM-DD")

        validated_batches += 1
        validated_records += len(review_rows)

    print(
        f"OK: DATA1-BR validado — {validated_batches} lote(s), "
        f"{validated_records} fonte(s), sem sobreposição; auditorias internas registradas; "
        "revisão externa bloqueada; CSV 51 × 34 e confiança DATA1-BX preservados"
    )
    return validated_batches, validated_records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", help="valida somente um lote ativo, por exemplo BR1")
    args = parser.parse_args()
    validate_batches(args.batch)


if __name__ == "__main__":
    main()
