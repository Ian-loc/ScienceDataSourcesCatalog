#!/usr/bin/env python3
"""Valida objetivos, portões de DOI e o estado real de DATA1-BR/EXT."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "migration" / "data1b_migration_matrix.csv"
REGISTRY_PATH = ROOT / "migration" / "br_batch_registry.json"
QUEUE_PATH = ROOT / "migration" / "external_review_queue.csv"
EVIDENCE_PATH = ROOT / "migration" / "external_review_evidence.csv"
READINESS_PATH = ROOT / "release" / "doi_readiness.json"
OBJECTIVES_PATH = ROOT / "FINAL_OBJECTIVES_AND_DOI_GATES.md"
EXPECTED_GATES = [f"G{i}" for i in range(1, 13)]
ALLOWED_GATE_STATUS = {"implementado_pendente_integracao", "parcial", "bloqueado", "concluído"}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


_, matrix_rows = read_csv(MATRIX_PATH)
registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
queue_header, queue_rows = read_csv(QUEUE_PATH)
evidence_header, evidence_rows = read_csv(EVIDENCE_PATH)
readiness = json.loads(READINESS_PATH.read_text(encoding="utf-8"))
objectives = OBJECTIVES_PATH.read_text(encoding="utf-8")

manual_ids = {row["resource_id"] for row in matrix_rows if row["migration_status"] == "revisão_manual"}
ready_ids = {row["resource_id"] for row in matrix_rows if row["migration_status"] == "pronto_para_migração"}
if len(manual_ids) != 35 or len(ready_ids) != 16:
    fail("DATA1-B deve preservar 35 casos manuais e 16 prontos")

active = registry.get("active_batches", [])
if [entry.get("batch") for entry in active] != ["BR1", "BR2", "BR3", "BR4", "BR5"]:
    fail("registro real deve conter BR1–BR5 ativos e ordenados")
planned_ids: list[str] = []
for entry in active:
    contract = json.loads((ROOT / entry["contract"]).read_text(encoding="utf-8"))
    ids = contract.get("expected_resource_ids", [])
    if len(ids) != 7:
        fail(f"{entry['batch']}: contrato deve conter sete IDs")
    planned_ids.extend(ids)
if len(planned_ids) != 35 or len(set(planned_ids)) != 35 or set(planned_ids) != manual_ids:
    fail("contratos BR1–BR5 não correspondem exatamente aos 35 casos manuais")

if "resource_id" not in queue_header or len(queue_rows) != 35:
    fail("fila externa deve conter 35 fontes")
queue_ids = {row["resource_id"] for row in queue_rows}
if queue_ids != manual_ids:
    fail("fila externa não corresponde aos 35 casos manuais")
if "resource_id" not in evidence_header:
    fail("tabela de evidências sem resource_id")
if any(row["resource_id"] not in queue_ids for row in evidence_rows):
    fail("tabela de evidências contém fonte fora da fila")

if readiness.get("catalog_current_version") != "0.7.0":
    fail("contrato deve preservar a versão formal 0.7.0")
if readiness.get("target_stable_release") != "1.0.0":
    fail("target_stable_release deve ser 1.0.0")
if readiness.get("archive_type") != "Dataset":
    fail("depósito final deve ser classificado como Dataset")
if readiness.get("doi_allowed") is not False:
    fail("DOI deve permanecer bloqueado")

gates = readiness.get("gates", [])
if [gate.get("id") for gate in gates] != EXPECTED_GATES:
    fail("contrato deve conter G1–G12 em ordem")
for gate in gates:
    if gate.get("status") not in ALLOWED_GATE_STATUS:
        fail(f"{gate.get('id')}: status inválido")
    if not str(gate.get("evidence", "")).strip():
        fail(f"{gate.get('id')}: evidência vazia")
if all(gate.get("status") == "concluído" for gate in gates):
    fail("estado atual não pode declarar todos os portões concluídos")

required_phrases = [
    "Objetivo geral", "Objetivos específicos finais", "Limites deliberados",
    "Definição mínima de completude científica", "Critérios de qualidade da versão 1.0.0",
    "Portões obrigatórios para DOI", "Regra de decisão",
]
for phrase in required_phrases:
    if phrase not in objectives:
        fail(f"documento de objetivos sem seção obrigatória: {phrase}")
for gate_id in EXPECTED_GATES:
    if gate_id not in objectives:
        fail(f"documento de objetivos não menciona {gate_id}")

print(
    "OK: objetivos e prontidão para DOI validados — registro real BR1–BR5, "
    f"fila externa com 35 fontes, {len(evidence_rows)} evidência(s), DOI bloqueado e versão 0.7.0 preservada"
)
