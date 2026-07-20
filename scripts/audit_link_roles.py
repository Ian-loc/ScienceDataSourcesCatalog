#!/usr/bin/env python3
"""Audita a separação entre página institucional e página efetiva de acesso aos dados."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "data_resources.csv"
REPORT_PATH = ROOT / "data" / "link_role_audit.json"
BUILD_META_PATH = ROOT / "data" / "build-meta.json"
INDEX_PATH = ROOT / "index.html"
BUILD_META_JS_PATH = ROOT / "assets" / "build-meta.js"
METHODOLOGY_PATH = ROOT / "METHODOLOGY.md"
CODEBOOK_PATH = ROOT / "CODEBOOK.md"

REQUIRED_FIELDS = {"resource_id", "resource_name", "homepage_url", "data_access_url"}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def normalize_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def build_report() -> dict:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        if not REQUIRED_FIELDS.issubset(fields):
            fail("CSV sem os campos necessários para auditar papéis dos links")
        rows = list(reader)

    records: list[dict[str, str]] = []
    counts = {
        "separate_destinations": 0,
        "same_destination_pending_review": 0,
        "data_access_not_applicable": 0,
    }

    for row in rows:
        homepage = row["homepage_url"].strip()
        data_access = row["data_access_url"].strip()

        if data_access == "não se aplica":
            status = "data_access_not_applicable"
        elif normalize_url(homepage) == normalize_url(data_access):
            status = "same_destination_pending_review"
        else:
            status = "separate_destinations"

        counts[status] += 1
        records.append({
            "resource_id": row["resource_id"].strip(),
            "resource_name": row["resource_name"].strip(),
            "status": status,
            "homepage_url": homepage,
            "data_access_url": data_access,
        })

    return {
        "records": len(records),
        "standard": {
            "homepage_url": "Página institucional principal ou página oficial sobre a fonte.",
            "data_access_url": "Página onde os dados podem ser pesquisados, visualizados, solicitados ou baixados.",
            "same_destination": "Pendência de revisão; somente pode ser mantida como exceção documentada após inspeção oficial.",
            "not_applicable": "Usado quando o recurso não oferece dados para consulta ou download, como software de publicação.",
        },
        "counts": counts,
        "records_requiring_review": [
            record for record in records if record["status"] == "same_destination_pending_review"
        ],
        "interpretation": "A igualdade entre os dois links não prova erro, mas indica que os papéis institucional e de acesso ainda não foram demonstrados separadamente.",
    }


def validate_documentation() -> None:
    for path in (INDEX_PATH, BUILD_META_JS_PATH, METHODOLOGY_PATH, CODEBOOK_PATH):
        if not path.exists():
            fail(f"arquivo obrigatório ausente: {path.relative_to(ROOT)}")

    index_text = INDEX_PATH.read_text(encoding="utf-8")
    build_meta_js = BUILD_META_JS_PATH.read_text(encoding="utf-8")
    methodology = METHODOLOGY_PATH.read_text(encoding="utf-8")
    codebook = CODEBOOK_PATH.read_text(encoding="utf-8")

    if 'id="q-link-role-pending"' not in index_text:
        fail("index.html não exibe o indicador de URLs iguais pendentes")
    if '"q-link-role-pending":quality.link_role_pending_records' not in build_meta_js:
        fail("assets/build-meta.js não conecta o indicador aos metadados do build")
    for token in ("Site oficial", "Acessar dados", "homepage_url", "data_access_url"):
        if token not in methodology or token not in codebook:
            fail(f"regra dos links sem documentação completa: {token}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="atualiza o relatório versionado")
    args = parser.parse_args()

    validate_documentation()
    report = build_report()
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"

    if args.write:
        REPORT_PATH.write_text(serialized, encoding="utf-8")
    elif not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != serialized:
        fail("data/link_role_audit.json diverge do CSV; execute scripts/audit_link_roles.py --write")

    if BUILD_META_PATH.exists():
        meta = json.loads(BUILD_META_PATH.read_text(encoding="utf-8"))
        quality = meta.setdefault("quality", {})
        quality["link_role_pending_records"] = report["counts"]["same_destination_pending_review"]
        BUILD_META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = report["counts"]
    print(
        "OK: papéis dos links auditados — "
        f"{counts['separate_destinations']} destinos separados; "
        f"{counts['same_destination_pending_review']} URLs iguais pendentes; "
        f"{counts['data_access_not_applicable']} não aplicáveis"
    )


if __name__ == "__main__":
    main()
