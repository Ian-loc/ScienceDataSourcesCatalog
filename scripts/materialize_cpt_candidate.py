#!/usr/bin/env python3
"""Register Cerrado Plant Traits in the governed candidate queue.

This one-time materializer preserves the 51-source canonical CSV while recording
an evidence-backed, approved candidate for the next authorized expansion cycle.
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "candidates" / "source_candidates.csv"
CHANGELOG = ROOT / "CHANGELOG.md"

DOI = "https://doi.org/10.6084/m9.figshare.32895932"
ARTICLE_DOI = "https://doi.org/10.1093/aob/mcag176"


def main() -> None:
    with QUEUE.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if any(DOI in row.get("homepage_url", "") or row.get("acronym") == "CPT" for row in rows):
        print("OK: CPT already registered in candidate queue")
        return

    numeric_ids = [
        int(match.group(1))
        for row in rows
        if (match := re.fullmatch(r"CAND(\d{4})", row.get("candidate_id", "")))
    ]
    candidate_id = f"CAND{max(numeric_ids, default=0) + 1:04d}"

    rows.append({
        "candidate_id": candidate_id,
        "official_name": "Cerrado Plant Traits (CPT): a database of functional traits across vegetation types in a global biodiversity hotspot",
        "acronym": "CPT",
        "homepage_url": DOI,
        "candidacy_reason": "Dataset brasileiro aberto que compila, harmoniza e documenta traços funcionais de plantas do Cerrado, reduzindo uma lacuna crítica de representação de savanas tropicais em bases globais de traços.",
        "presumed_research_areas": "Biodiversity | Functional ecology | Plant ecology | Conservation | Ecological restoration",
        "presumed_geographic_coverage": "Cerrado — Brasil",
        "presumed_resource_type": "trait_database | scientific_dataset",
        "possible_duplication": "Complementa, mas não duplica, infraestruturas globais de traços como TRY e BIEN: é um dataset temático brasileiro, versionado e citável, hospedado no Figshare.",
        "initial_evidence": (
            "DOI do dataset no Figshare e artigo oficial em Annals of Botany revisados em 2026-08-03. "
            "A versão descrita integra 148 datasets, 113.859 registros curados de traços, "
            "2.134 espécies taxonomicamente verificadas e 150 famílias, abrangendo órgãos da planta inteira, "
            "raízes, caules, folhas, flores, frutos e sementes. Artigo: " + ARTICLE_DOI
        ),
        "evidence_status": "official_documentation_reviewed",
        "priority": "alta",
        "decision": "incluir",
        "review_status": "decisão_registrada",
        "added_date": "2026-08-03",
        "notes": (
            "Registrar como dataset específico brasileiro, não como representação genérica do repositório Figshare. "
            "O depósito informa arquivos CSV e licença CC BY 4.0. A migração canônica deve preencher os 34 campos, "
            "classificar o recurso como P0 e atualizar matrizes e validadores no mesmo pull request."
        ),
    })

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    QUEUE.write_text(buffer.getvalue(), encoding="utf-8")

    changelog = CHANGELOG.read_text(encoding="utf-8")
    entry = "- registrado Cerrado Plant Traits (CPT) como candidato brasileiro P0 de alta prioridade, com decisão de inclusão e evidência científica;\n"
    if entry not in changelog:
        anchor = "### Adicionado\n\n"
        if anchor not in changelog:
            raise SystemExit("ERRO: seção Adicionado não localizada no CHANGELOG")
        CHANGELOG.write_text(changelog.replace(anchor, anchor + entry, 1), encoding="utf-8")

    print(f"OK: {candidate_id} registrado para CPT; fila agora contém {len(rows)} candidatos")


if __name__ == "__main__":
    main()
