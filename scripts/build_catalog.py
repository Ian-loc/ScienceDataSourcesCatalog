#!/usr/bin/env python3
"""Valida o CSV canônico e gera os artefatos consumidos pelo site."""
from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "data_resources.csv"
JSON_PATH = ROOT / "data" / "data_resources.json"
BUILD_META_PATH = ROOT / "data" / "build-meta.json"
QUALITY_REPORT_PATH = ROOT / "data" / "data_quality_report.json"
CITATION_PATH = ROOT / "CITATION.cff"

REQUIRED_COLUMNS = [
    "resource_id", "resource_name", "acronym", "official_identity", "description",
    "homepage_url", "data_access_url", "research_areas", "keywords",
    "data_product_types", "data_formats", "visualization_types",
    "geographic_coverage", "covers_brazil", "spatial_resolution",
    "temporal_coverage", "temporal_resolution", "data_sources", "free_download",
    "access_conditions", "programmatic_access", "access_protocols",
    "authentication_required", "access_documentation_url", "license",
    "institutional_status", "owner_or_manager", "academic_uses", "limitations",
    "academic_evidence_type", "academic_evidence_url", "academic_evidence_note",
    "verification_url", "last_verified",
]
OPTIONAL_VALUES = {"acronym", "access_documentation_url"}
ENUM_VALUES = {
    "free_download": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
    "programmatic_access": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
    "authentication_required": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
    "covers_brazil": {"sim", "parcial", "não", "desconhecido", "não se aplica"},
    "academic_evidence_type": {
        "artigo revisado por pares", "artigo técnico",
        "documentação técnica oficial", "documentação oficial",
    },
}
RESEARCH_AREAS = {
    "Ciências Ambientais e Ecologia",
    "Biodiversidade e Conservação",
    "Clima e Ciências Atmosféricas",
    "Geociências, Solos e Geografia Física",
    "Recursos Hídricos e Oceanografia",
    "Agricultura, Florestas e Uso da Terra",
    "Sensoriamento Remoto e Geoinformação",
    "Infraestruturas e Ciência de Dados",
    "Planejamento Territorial e Políticas Públicas",
}
MULTIVALUE_FIELDS = {
    "research_areas", "keywords", "data_product_types", "data_formats",
    "visualization_types", "data_sources", "access_protocols",
}
ACCESS_QUALITY_FIELDS = {
    "free_download", "access_conditions", "programmatic_access",
    "access_protocols", "authentication_required", "access_documentation_url", "license",
}
DATE_RE = re.compile(r"^20\d{2}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^DR\d{4}$")
VERSION_RE = re.compile(r"^version:\s*[\"']?([^\"'\s]+)", re.MULTILINE)
UNCERTAINTY_MARKERS = (
    "desconhecido", "não localizada", "não documentado", "varia conforme",
    "depende do", "consultar produto", "consultar versão",
)


def is_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def read_version() -> str:
    if not CITATION_PATH.exists():
        fail("CITATION.cff ausente")
    match = VERSION_RE.search(CITATION_PATH.read_text(encoding="utf-8"))
    if not match:
        fail("versão não localizada em CITATION.cff")
    return match.group(1)


def has_uncertainty(value: str) -> bool:
    normalized = value.strip().casefold()
    return any(marker in normalized for marker in UNCERTAINTY_MARKERS)


with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    if reader.fieldnames != REQUIRED_COLUMNS:
        fail("cabeçalho diferente do esquema documentado")
    rows = list(reader)

if not rows:
    fail("CSV sem registros")

seen_ids: set[str] = set()
seen_names: set[str] = set()
for line, row in enumerate(rows, start=2):
    missing = [field for field in REQUIRED_COLUMNS if field not in OPTIONAL_VALUES and not row[field].strip()]
    if missing:
        fail(f"linha {line}: campos obrigatórios vazios: {', '.join(missing)}")

    resource_id = row["resource_id"].strip()
    if not ID_RE.fullmatch(resource_id):
        fail(f"linha {line}: resource_id inválido: {resource_id}")
    if resource_id in seen_ids:
        fail(f"linha {line}: resource_id duplicado: {resource_id}")
    seen_ids.add(resource_id)

    name = row["resource_name"].strip()
    if name != row["resource_name"]:
        fail(f"linha {line}: resource_name contém espaços externos")
    name_key = name.casefold()
    if name_key in seen_names:
        fail(f"linha {line}: nome duplicado: {row['resource_name']}")
    seen_names.add(name_key)

    for field in ("homepage_url", "academic_evidence_url", "verification_url"):
        if not is_https(row[field].strip()):
            fail(f"linha {line}: {field} deve ser URL HTTPS")
    for field in ("data_access_url", "access_documentation_url"):
        value = row[field].strip()
        if value and value != "não se aplica" and not is_https(value):
            fail(f"linha {line}: {field} deve ser URL HTTPS, vazio ou 'não se aplica'")

    for field, allowed in ENUM_VALUES.items():
        if row[field] not in allowed:
            fail(f"linha {line}: {field} inválido: {row[field]}")

    areas = set(split_values(row["research_areas"]))
    if not areas or not areas.issubset(RESEARCH_AREAS):
        fail(f"linha {line}: research_areas contém categoria desconhecida")

    for field in MULTIVALUE_FIELDS:
        values = split_values(row[field])
        if len(values) != len(set(values)):
            fail(f"linha {line}: {field} contém valores duplicados")
        if any(value != value.strip() for value in values):
            fail(f"linha {line}: {field} contém item sem trim")

    if not DATE_RE.fullmatch(row["last_verified"]):
        fail(f"linha {line}: last_verified deve usar AAAA-MM-DD")
    try:
        date.fromisoformat(row["last_verified"])
    except ValueError:
        fail(f"linha {line}: last_verified não é uma data válida")

expected_ids = [f"DR{i:04d}" for i in range(1, len(rows) + 1)]
if sorted(seen_ids) != expected_ids:
    fail("IDs devem ser contínuos de DR0001 até o último registro")

JSON_PATH.write_text(
    json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

unknown_by_field = {
    field: sum(1 for row in rows if has_uncertainty(row[field]))
    for field in REQUIRED_COLUMNS
    if field not in {"resource_id", "resource_name", "acronym"}
}
quality = {
    "records": len(rows),
    "official_documentation_records": sum(
        row["academic_evidence_type"] in {"documentação técnica oficial", "documentação oficial"}
        for row in rows
    ),
    "peer_reviewed_evidence_records": sum(
        row["academic_evidence_type"] == "artigo revisado por pares" for row in rows
    ),
    "access_uncertainty_records": sum(
        any(has_uncertainty(row[field]) for field in ACCESS_QUALITY_FIELDS) for row in rows
    ),
    "license_uncertainty_records": sum(has_uncertainty(row["license"]) for row in rows),
    "brazil_applicable_records": sum(row["covers_brazil"] in {"sim", "parcial"} for row in rows),
    "verification_date_min": min(row["last_verified"] for row in rows),
    "verification_date_max": max(row["last_verified"] for row in rows),
    "evidence_type_counts": dict(sorted(Counter(row["academic_evidence_type"] for row in rows).items())),
    "unknown_or_variable_by_field": dict(sorted(unknown_by_field.items())),
    "interpretation": "Indicadores de qualidade descrevem o preenchimento do catálogo; não certificam todos os datasets de cada fonte.",
}
QUALITY_REPORT_PATH.write_text(
    json.dumps(quality, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

build_meta = {
    "version": read_version(),
    "commit": os.environ.get("GITHUB_SHA", "local"),
    "built_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "records": len(rows),
    "fields": len(REQUIRED_COLUMNS),
    "quality": {
        "official_documentation_records": quality["official_documentation_records"],
        "peer_reviewed_evidence_records": quality["peer_reviewed_evidence_records"],
        "access_uncertainty_records": quality["access_uncertainty_records"],
        "license_uncertainty_records": quality["license_uncertainty_records"],
    },
}
BUILD_META_PATH.write_text(
    json.dumps(build_meta, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(
    f"OK: {len(rows)} fontes e {len(REQUIRED_COLUMNS)} variáveis validadas; "
    f"JSON, relatório de qualidade e metadados de build gerados para a versão {build_meta['version']}"
)
