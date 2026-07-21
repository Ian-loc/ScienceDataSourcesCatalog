#!/usr/bin/env python3
"""Valida workflow, documentação crítica e estados protegidos."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / "QUALITY_CORRECTION_WORKFLOW.md"
IMPLEMENTATION_PATH = ROOT / "IMPLEMENTATION_WORKFLOW.md"
STATUS_PATH = ROOT / "WORKFLOW_STATUS.md"
MIRROR_PATH = ROOT / "DRIVE_MIRROR_CONTRACT.md"
SELECTION_PATH = ROOT / "SELECTION_AND_COVERAGE_POLICY.md"
AUDIT_PATH = ROOT / "DOCUMENTATION_CONSISTENCY_AUDIT.md"
SCHEMA_PATH = ROOT / "schema" / "v0.8.0-draft.json"
CSV_PATH = ROOT / "data" / "data_resources.csv"
CITATION_PATH = ROOT / "CITATION.cff"
READINESS_PATH = ROOT / "release" / "doi_readiness.json"
REGISTRY_PATH = ROOT / "migration" / "br_batch_registry.json"
QUEUE_PATH = ROOT / "migration" / "external_review_queue.csv"
EVIDENCE_PATH = ROOT / "migration" / "external_review_evidence.csv"
OBSOLETE_BATCHES_PATH = ROOT / "migration" / "data1br_review_batches.csv"

EXPECTED_RULES = {
    "publishing_software_requires_not_applicable_geography",
    "global_scope_normally_covers_brazil",
    "not_applicable_scope_requires_not_applicable_brazil",
    "programmatic_yes_requires_protocol_or_tool",
    "programmatic_no_forbids_positive_protocol_without_exception",
    "authentication_yes_requires_access_condition",
    "free_download_yes_requires_data_access_url",
    "formats_must_not_contain_protocols_or_visualizations",
    "visualizations_must_not_contain_formats_or_protocols",
    "protocols_must_not_contain_client_tools",
    "citation_guidance_url_must_be_https",
    "multivalued_items_must_be_unique_and_trimmed",
    "academic_evidence_doi_is_not_source_identifier",
    "placeholders_must_not_coexist_with_positive_values",
}
REQUIRED_CYCLES = [
    "QC0", "SELECT1", "DATA1-BX", "DATA1-BR", "DATA1-BR-CLOSE", "STATE-SYNC",
    "MIRROR-XLSX", "DATA1-EXT", "DATA1-C", "DATA1-D", "DATA2", "UX5", "RELEASE2",
    "DOI", "RES1", "EDU1",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def require_cycle_order(text: str, filename: str) -> None:
    positions: list[int] = []
    for cycle in REQUIRED_CYCLES:
        match = re.search(rf"\|\s*{re.escape(cycle)}\s*\|", text)
        if not match:
            fail(f"{filename} não contém ciclo obrigatório: {cycle}")
        positions.append(match.start())
    if positions != sorted(positions):
        fail(f"ordem operacional divergente em {filename}")


for path in (
    WORKFLOW_PATH, IMPLEMENTATION_PATH, STATUS_PATH, MIRROR_PATH, SELECTION_PATH, AUDIT_PATH,
    SCHEMA_PATH, CSV_PATH, CITATION_PATH, READINESS_PATH, REGISTRY_PATH, QUEUE_PATH, EVIDENCE_PATH,
):
    if not path.exists():
        fail(f"arquivo obrigatório ausente: {path.relative_to(ROOT)}")
if OBSOLETE_BATCHES_PATH.exists():
    fail("plano antigo data1br_review_batches.csv deve permanecer removido")

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
rules = schema.get("cross_validation_rules", [])
if len(rules) != 14 or len(set(rules)) != 14 or set(rules) != EXPECTED_RULES:
    fail("contrato 0.8.0 não contém exatamente as 14 regras aprovadas")

workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
implementation = IMPLEMENTATION_PATH.read_text(encoding="utf-8")
status = STATUS_PATH.read_text(encoding="utf-8")
for text, filename in (
    (workflow, "QUALITY_CORRECTION_WORKFLOW.md"),
    (implementation, "IMPLEMENTATION_WORKFLOW.md"),
    (status, "WORKFLOW_STATUS.md"),
):
    require_cycle_order(text, filename)

workflow_folded = workflow.casefold()
for token in (
    "não bloqueante para v1.0.0 e doi",
    "data/product_resolution_examples.csv",
    "não é cientificamente seguro inferir resolução",
    "página didática",
    "checkpoints de reordenação",
    "nenhuma nova fonte entra diretamente no catálogo",
    "planilha nativa e `.xlsx` não substituem o csv canônico",
):
    if token.casefold() not in workflow_folded:
        fail(f"workflow sem requisito: {token}")

implementation_folded = implementation.casefold()
for token in (
    "| data1-br-close | concluído |",
    "| state-sync | concluído |",
    "| mirror-xlsx | bloqueado por upload |",
    "| data1-ext | ativo |",
    "w1a",
    "w1b",
    "w1c",
    "drive_mirror_contract.md",
    "proxy `407`",
):
    if token.casefold() not in implementation_folded:
        fail(f"IMPLEMENTATION_WORKFLOW.md sem estado crítico: {token}")

status_folded = status.casefold()
for token in (
    "revisão externa bloqueada",
    "novas fontes permanecem fora do csv",
    "| data1-br-close | concluído |",
    "| state-sync | concluído |",
    "| mirror-xlsx | bloqueado por upload |",
    "| data1-ext | ativo |",
    "planilha nativa: **51 × 34**",
    "`.xlsx`: **51 × 22**",
    "res1 e edu1",
):
    if token.casefold() not in status_folded:
        fail(f"WORKFLOW_STATUS.md sem estado crítico: {token}")

mirror = MIRROR_PATH.read_text(encoding="utf-8").casefold()
for token in (
    "data/data_resources.csv",
    "única fonte canônica",
    "source_commit",
    "generated_at",
    "planilha nativa: aba `data_resources` verificada com 51 recursos e os 34 campos canônicos",
    "arquivo `.xlsx`: download bruto verificado com 51 recursos e 22 campos históricos",
    "proxy `407`",
    "igualdade célula a célula",
    "project_changelog",
):
    if token.casefold() not in mirror:
        fail(f"DRIVE_MIRROR_CONTRACT.md sem requisito: {token}")

selection = SELECTION_PATH.read_text(encoding="utf-8").casefold()
for section in (
    "critérios mínimos de inclusão", "critérios de exclusão",
    "duplicidade e relação entre recursos", "candidatos", "matriz de lacunas",
    "critérios de prioridade para expansão", "recursos bibliométricos e editoriais",
):
    if section not in selection:
        fail(f"política de seleção sem seção: {section}")

with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.reader(handle)
    header = next(reader)
    rows = list(reader)
if len(header) != 34 or len(rows) != 51:
    fail("workflow crítico não pode alterar o CSV 0.7.0 de 51 × 34")

citation = CITATION_PATH.read_text(encoding="utf-8")
match = re.search(r'^version:\s*["\']?([^"\'\s]+)', citation, re.MULTILINE)
if not match or match.group(1) != "0.7.0":
    fail("versão formal deve permanecer 0.7.0")

readiness = json.loads(READINESS_PATH.read_text(encoding="utf-8"))
if readiness.get("doi_allowed") is not False:
    fail("DOI deve permanecer bloqueado")

print(
    "OK: STATE-SYNC concluído; planilha nativa 51 × 34 e XLSX 51 × 22 registrados separadamente; "
    "MIRROR-XLSX bloqueado por upload, DATA1-EXT ativo, CSV 51 × 34 e versão 0.7.0 preservados"
)
