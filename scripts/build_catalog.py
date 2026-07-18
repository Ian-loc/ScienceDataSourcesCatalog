#!/usr/bin/env python3
"""Valida o CSV canônico e gera o JSON consumido pelo site."""
from __future__ import annotations
import csv
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "data_resources.csv"
JSON_PATH = ROOT / "data" / "data_resources.json"

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
DATE_RE = re.compile(r"^20\d{2}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^DR\d{4}$")

def is_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)

def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")

def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]

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

    name_key = row["resource_name"].strip().casefold()
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

    if not DATE_RE.fullmatch(row["last_verified"]):
        fail(f"linha {line}: last_verified deve usar AAAA-MM-DD")

expected_ids = [f"DR{i:04d}" for i in range(1, len(rows) + 1)]
if sorted(seen_ids) != expected_ids:
    fail("IDs devem ser contínuos de DR0001 até o último registro")

JSON_PATH.write_text(
    json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"OK: {len(rows)} fontes e {len(REQUIRED_COLUMNS)} variáveis validadas; JSON gerado")
