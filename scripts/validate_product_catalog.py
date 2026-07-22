#!/usr/bin/env python3
"""Valida a camada fonte → produto → distribuição sem alterar o CSV canônico."""
from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data" / "data_resources.csv"
PRODUCT_PATH = ROOT / "data" / "data_products.csv"
DISTRIBUTION_PATH = ROOT / "data" / "product_distributions.csv"
SCHEMA_PATH = ROOT / "schema" / "product-catalog-v0.1.json"

PRODUCT_COLUMNS = [
    "product_id","resource_id","product_name","product_acronym","product_family",
    "product_kind","product_description","research_areas","keywords",
    "geographic_coverage","covers_brazil","spatial_support","spatial_resolution",
    "temporal_coverage","temporal_resolution","update_frequency","product_status",
    "version_or_collection","enumeration_scope","product_page_url","methodology_url",
    "primary_or_derived","limitations","last_verified",
]
DISTRIBUTION_COLUMNS = [
    "distribution_id","product_id","distribution_name","access_url","format",
    "access_protocol","access_tool","free_download","authentication_required",
    "access_conditions","license","provider_attribution_required","subset_support",
    "notes","last_verified",
]

PRODUCT_ID = re.compile(r"^DP\d{6}$")
DISTRIBUTION_ID = re.compile(r"^DD\d{6}$")
RESOURCE_ID = re.compile(r"^DR\d{4}$")

def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")

def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)

def is_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return len(value) == 10

def is_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)

if not SCHEMA_PATH.exists():
    fail("contrato de produtos ausente")
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

source_columns, sources = read_csv(SOURCE_PATH)
product_columns, products = read_csv(PRODUCT_PATH)
distribution_columns, distributions = read_csv(DISTRIBUTION_PATH)

if len(source_columns) != 34 or len(sources) != 51:
    fail("piloto de produtos não pode alterar o CSV canônico 51 × 34")
if product_columns != PRODUCT_COLUMNS:
    fail("cabeçalho de data_products.csv diverge do contrato")
if distribution_columns != DISTRIBUTION_COLUMNS:
    fail("cabeçalho de product_distributions.csv diverge do contrato")
if not products or not distributions:
    fail("piloto precisa conter produtos e distribuições")

controlled = schema["controlled_values"]
source_ids = {row["resource_id"].strip() for row in sources}
product_ids: set[str] = set()

required_product_text = [
    "product_name","product_family","product_description","research_areas","keywords",
    "geographic_coverage","spatial_support","spatial_resolution","temporal_coverage",
    "temporal_resolution","update_frequency","version_or_collection",
    "product_page_url","methodology_url","limitations",
]

for line, row in enumerate(products, start=2):
    pid = row["product_id"].strip()
    rid = row["resource_id"].strip()
    if not PRODUCT_ID.fullmatch(pid):
        fail(f"linha {line}: product_id inválido: {pid}")
    if pid in product_ids:
        fail(f"linha {line}: product_id duplicado: {pid}")
    product_ids.add(pid)
    if not RESOURCE_ID.fullmatch(rid) or rid not in source_ids:
        fail(f"linha {line} ({pid}): resource_id inexistente: {rid}")
    for field in required_product_text:
        if not row[field].strip():
            fail(f"linha {line} ({pid}): campo obrigatório vazio: {field}")
    for field in ("product_page_url", "methodology_url"):
        if not is_https(row[field].strip()):
            fail(f"linha {line} ({pid}): {field} deve ser HTTPS")
    if row["product_kind"].strip() not in controlled["product_kind"]:
        fail(f"linha {line} ({pid}): product_kind inválido")
    if row["enumeration_scope"].strip() not in controlled["enumeration_scope"]:
        fail(f"linha {line} ({pid}): enumeration_scope inválido")
    if row["product_status"].strip() not in controlled["product_status"]:
        fail(f"linha {line} ({pid}): product_status inválido")
    if row["covers_brazil"].strip() not in controlled["covers_brazil"]:
        fail(f"linha {line} ({pid}): covers_brazil inválido")
    if row["primary_or_derived"].strip() not in controlled["primary_or_derived"]:
        fail(f"linha {line} ({pid}): primary_or_derived inválido")
    if not is_iso_date(row["last_verified"].strip()):
        fail(f"linha {line} ({pid}): last_verified inválido")
    if row["product_kind"].strip() in {"catalog", "federated_catalog"}:
        if row["enumeration_scope"].strip() != "external_index":
            fail(f"linha {line} ({pid}): catálogos amplos exigem external_index")

distribution_ids: set[str] = set()
product_distribution_count = {pid: 0 for pid in product_ids}
required_distribution_text = [
    "distribution_name","access_url","format","access_protocol","access_tool",
    "access_conditions","license","subset_support","notes",
]

for line, row in enumerate(distributions, start=2):
    did = row["distribution_id"].strip()
    pid = row["product_id"].strip()
    if not DISTRIBUTION_ID.fullmatch(did):
        fail(f"linha {line}: distribution_id inválido: {did}")
    if did in distribution_ids:
        fail(f"linha {line}: distribution_id duplicado: {did}")
    distribution_ids.add(did)
    if pid not in product_ids:
        fail(f"linha {line} ({did}): product_id inexistente: {pid}")
    product_distribution_count[pid] += 1
    for field in required_distribution_text:
        if not row[field].strip():
            fail(f"linha {line} ({did}): campo obrigatório vazio: {field}")
    if not is_https(row["access_url"].strip()):
        fail(f"linha {line} ({did}): access_url deve ser HTTPS")
    if row["free_download"].strip() not in controlled["free_download"]:
        fail(f"linha {line} ({did}): free_download inválido")
    if row["authentication_required"].strip() not in controlled["authentication_required"]:
        fail(f"linha {line} ({did}): authentication_required inválido")
    if row["provider_attribution_required"].strip() not in controlled["provider_attribution_required"]:
        fail(f"linha {line} ({did}): provider_attribution_required inválido")
    if not is_iso_date(row["last_verified"].strip()):
        fail(f"linha {line} ({did}): last_verified inválido")

missing = [pid for pid, count in product_distribution_count.items() if count == 0]
if missing:
    fail(f"produto(s) sem distribuição: {', '.join(missing)}")

print(
    "OK: catálogo de produtos validado — "
    f"{len(products)} produtos, {len(distributions)} distribuições, "
    f"{len({row['resource_id'] for row in products})} fontes piloto; "
    "CSV canônico 51 × 34 preservado"
)
