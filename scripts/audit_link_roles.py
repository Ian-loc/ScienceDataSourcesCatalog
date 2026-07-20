#!/usr/bin/env python3
"""Audita a separação entre página institucional e página efetiva de acesso aos dados."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "data_resources.csv"
REPORT_PATH = ROOT / "data" / "link_role_audit.json"
BUILD_META_PATH = ROOT / "data" / "build-meta.json"

REQUIRED_FIELDS = {"resource_id", "resource_name", "homepage_url", "data_access_url"}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def normalize_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


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

report = {
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
REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if BUILD_META_PATH.exists():
    meta = json.loads(BUILD_META_PATH.read_text(encoding="utf-8"))
    quality = meta.setdefault("quality", {})
    quality["link_role_pending_records"] = counts["same_destination_pending_review"]
    BUILD_META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(
    "OK: papéis dos links auditados — "
    f"{counts['separate_destinations']} destinos separados; "
    f"{counts['same_destination_pending_review']} URLs iguais pendentes; "
    f"{counts['data_access_not_applicable']} não aplicáveis"
)
