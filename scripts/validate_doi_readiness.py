#!/usr/bin/env python3
"""Valida o contrato de objetivos finais, os portões de DOI e o plano DATA1-BR."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "migration" / "data1b_migration_matrix.csv"
BATCHES_PATH = ROOT / "migration" / "data1br_review_batches.csv"
READINESS_PATH = ROOT / "release" / "doi_readiness.json"
OBJECTIVES_PATH = ROOT / "FINAL_OBJECTIVES_AND_DOI_GATES.md"

BATCH_COLUMNS = [
    "batch_id",
    "resource_id",
    "review_priority",
    "review_focus",
    "evidence_required",
    "current_blocker",
    "review_status",
]
EXPECTED_GATES = [f"G{i}" for i in range(1, 13)]
ALLOWED_GATE_STATUS = {
    "implementado_pendente_integracao",
    "parcial",
    "bloqueado",
    "concluído",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


_, matrix_rows = read_csv(MATRIX_PATH)
batch_columns, batch_rows = read_csv(BATCHES_PATH)
readiness = json.loads(READINESS_PATH.read_text(encoding="utf-8"))
objectives = OBJECTIVES_PATH.read_text(encoding="utf-8")

if batch_columns != BATCH_COLUMNS:
    fail("cabeçalho do plano DATA1-BR diferente do contrato")

pending_ids = [
    row["resource_id"]
    for row in matrix_rows
    if row["migration_status"] == "revisão_manual"
]
planned_ids = [row["resource_id"] for row in batch_rows]

if len(pending_ids) != 35:
    fail(f"matriz deve conter 35 registros em revisão manual; encontrados {len(pending_ids)}")
if len(batch_rows) != 35:
    fail(f"plano DATA1-BR deve conter 35 registros; encontrados {len(batch_rows)}")
if len(set(planned_ids)) != 35:
    fail("plano DATA1-BR contém resource_id duplicado")
if set(planned_ids) != set(pending_ids):
    missing = sorted(set(pending_ids) - set(planned_ids))
    extra = sorted(set(planned_ids) - set(pending_ids))
    fail(f"plano não corresponde aos casos pendentes; ausentes={missing}; extras={extra}")

batch_counts = Counter(row["batch_id"] for row in batch_rows)
if set(batch_counts) != {"BR1", "BR2", "BR3", "BR4", "BR5"}:
    fail("plano deve conter exatamente os lotes BR1-BR5")
if any(count != 7 for count in batch_counts.values()):
    fail(f"cada lote deve conter sete registros; contagens={dict(batch_counts)}")

for line, row in enumerate(batch_rows, start=2):
    if row["review_priority"] not in {"P1", "P2"}:
        fail(f"linha {line}: prioridade inválida")
    if row["review_status"] != "pendente":
        fail(f"linha {line}: o ciclo de planejamento não pode declarar revisão concluída")
    for field in ("review_focus", "evidence_required", "current_blocker"):
        if not row[field].strip():
            fail(f"linha {line}: {field} vazio")

if readiness.get("catalog_current_version") != "0.7.0":
    fail("contrato deve preservar a versão formal 0.7.0 nesta etapa")
if readiness.get("target_stable_release") != "1.0.0":
    fail("target_stable_release deve ser 1.0.0")
if readiness.get("archive_type") != "Dataset":
    fail("depósito final deve ser classificado como Dataset")
if readiness.get("doi_allowed") is not False:
    fail("DOI deve permanecer bloqueado")

gates = readiness.get("gates", [])
gate_ids = [gate.get("id") for gate in gates]
if gate_ids != EXPECTED_GATES:
    fail("contrato deve conter G1-G12 em ordem")
for gate in gates:
    if gate.get("status") not in ALLOWED_GATE_STATUS:
        fail(f"{gate.get('id')}: status inválido")
    if not str(gate.get("evidence", "")).strip():
        fail(f"{gate.get('id')}: evidência vazia")

if all(gate.get("status") == "concluído" for gate in gates):
    fail("estado atual não pode declarar todos os portões concluídos")

required_phrases = [
    "Objetivo geral",
    "Objetivos específicos finais",
    "Limites deliberados",
    "Definição mínima de completude científica",
    "Critérios de qualidade da versão 1.0.0",
    "Portões obrigatórios para DOI",
    "Regra de decisão",
]
for phrase in required_phrases:
    if phrase not in objectives:
        fail(f"documento de objetivos sem seção obrigatória: {phrase}")
for gate_id in EXPECTED_GATES:
    if gate_id not in objectives:
        fail(f"documento de objetivos não menciona {gate_id}")

print(
    "OK: objetivos e prontidão para DOI validados — "
    f"12 portões; 35 revisões pendentes em 5 lotes; DOI bloqueado; versão 0.7.0 preservada"
)
