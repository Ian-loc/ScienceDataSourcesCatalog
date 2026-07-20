#!/usr/bin/env python3
"""Valida a fila de fontes candidatas sem alterar o catálogo canônico."""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = ROOT / "candidates" / "source_candidates.csv"
CANONICAL_PATH = ROOT / "data" / "data_resources.csv"

EXPECTED_COLUMNS = [
    "candidate_id",
    "official_name",
    "acronym",
    "homepage_url",
    "candidacy_reason",
    "presumed_research_areas",
    "presumed_geographic_coverage",
    "presumed_resource_type",
    "possible_duplication",
    "initial_evidence",
    "evidence_status",
    "priority",
    "decision",
    "review_status",
    "added_date",
    "notes",
]
EVIDENCE_STATUS = {
    "user_submitted_url_only",
    "official_page_located",
    "official_documentation_reviewed",
    "insufficient_evidence",
}
PRIORITY = {"alta", "média", "baixa"}
DECISIONS = {"aguardar_evidência", "incluir", "excluir", "fundir"}
REVIEW_STATUS = {
    "triagem_inicial",
    "revisão_de_elegibilidade",
    "revisão_de_completude",
    "decisão_registrada",
}
FINAL_DECISIONS = {"incluir", "excluir", "fundir"}
ID_PATTERN = re.compile(r"^CAND\d{4}$")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def https_hostname(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"URL deve ser HTTPS: {value}")
    return parsed.netloc.casefold().removeprefix("www.")


def iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return len(value) == 10


if not CANDIDATE_PATH.exists():
    fail("fila de candidatos ausente")
if not CANONICAL_PATH.exists():
    fail("CSV canônico ausente")

candidate_columns, candidates = read_csv(CANDIDATE_PATH)
canonical_columns, canonical_rows = read_csv(CANONICAL_PATH)

if candidate_columns != EXPECTED_COLUMNS:
    fail("cabeçalho da fila de candidatos diverge do contrato")
if len(canonical_columns) != 34 or len(canonical_rows) != 51:
    fail("a fila de candidatos não pode alterar o CSV canônico 51 × 34")
if not candidates:
    fail("fila de candidatos deve conter ao menos uma indicação")

candidate_ids = [row["candidate_id"].strip() for row in candidates]
if len(candidate_ids) != len(set(candidate_ids)):
    fail("candidate_id duplicado")
if any(not ID_PATTERN.fullmatch(value) for value in candidate_ids):
    fail("candidate_id fora do padrão CAND0001")

canonical_hosts = {
    https_hostname(row["homepage_url"].strip())
    for row in canonical_rows
    if row.get("homepage_url", "").strip()
}
candidate_hosts: set[str] = set()

required_text = [
    "official_name",
    "homepage_url",
    "candidacy_reason",
    "presumed_research_areas",
    "presumed_geographic_coverage",
    "presumed_resource_type",
    "possible_duplication",
    "initial_evidence",
    "notes",
]

for line, row in enumerate(candidates, start=2):
    cid = row["candidate_id"].strip()

    for field in required_text:
        if not row[field].strip():
            fail(f"linha {line} ({cid}): campo obrigatório vazio: {field}")

    host = https_hostname(row["homepage_url"].strip())
    if host in candidate_hosts:
        fail(f"linha {line} ({cid}): domínio duplicado na fila")
    if host in canonical_hosts:
        fail(f"linha {line} ({cid}): fonte já representada no CSV canônico")
    candidate_hosts.add(host)

    evidence = row["evidence_status"].strip()
    priority = row["priority"].strip()
    decision = row["decision"].strip()
    review = row["review_status"].strip()

    if evidence not in EVIDENCE_STATUS:
        fail(f"linha {line} ({cid}): evidence_status inválido")
    if priority not in PRIORITY:
        fail(f"linha {line} ({cid}): prioridade inválida")
    if decision not in DECISIONS:
        fail(f"linha {line} ({cid}): decisão inválida")
    if review not in REVIEW_STATUS:
        fail(f"linha {line} ({cid}): review_status inválido")
    if not iso_date(row["added_date"].strip()):
        fail(f"linha {line} ({cid}): added_date deve usar YYYY-MM-DD")

    if evidence == "user_submitted_url_only":
        if decision != "aguardar_evidência" or review != "triagem_inicial":
            fail(
                f"linha {line} ({cid}): URL submetida pelo usuário exige "
                "aguardar_evidência e triagem_inicial"
            )

    if decision in FINAL_DECISIONS:
        if review != "decisão_registrada":
            fail(f"linha {line} ({cid}): decisão final exige decisão_registrada")
        if evidence != "official_documentation_reviewed":
            fail(f"linha {line} ({cid}): decisão final exige documentação oficial revisada")

print(
    "OK: fila de candidatos validada — "
    f"{len(candidates)} candidato(s); IDs e URLs únicos; "
    "separação do CSV 51 × 34 preservada; nenhuma inclusão automática autorizada"
)
