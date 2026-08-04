#!/usr/bin/env python3
"""Validate the Phase 1 scientific-variable registry and pilot passports."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIABLES_PATH = ROOT / "data" / "scientific_variables.csv"
RELATIONS_PATH = ROOT / "data" / "product_variables.csv"
PASSPORTS_PATH = ROOT / "data" / "scientific_variable_passports.json"
PRODUCTS_PATH = ROOT / "data" / "data_products.csv"
SCHEMA_PATH = ROOT / "schema" / "scientific-variable-passport-v0.1.json"

VARIABLE_FIELDS = {
    "variable_id", "passport_id", "display_name", "domain_tags", "data_type", "unit",
    "object_observed", "resource_id", "product_id", "version_or_release",
    "source_variable_name", "review_status", "reviewed_at",
}
RELATION_FIELDS = {
    "product_id", "variable_id", "relationship_role", "source_field_or_band", "notes", "last_verified",
}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            fail(f"cabeçalho ausente: {path.relative_to(ROOT)}")
        rows = list(reader)
        return reader.fieldnames, rows


variable_header, variables = read_csv(VARIABLES_PATH)
relation_header, relations = read_csv(RELATIONS_PATH)
_, products = read_csv(PRODUCTS_PATH)

if set(variable_header) != VARIABLE_FIELDS:
    fail("scientific_variables.csv diverge do contrato inicial de campos")
if set(relation_header) != RELATION_FIELDS:
    fail("product_variables.csv diverge do contrato inicial de campos")
if len(variables) < 2:
    fail("o piloto deve conter ao menos duas variáveis verificáveis")

product_index = {row["product_id"]: row for row in products}
if len(product_index) != len(products):
    fail("data_products.csv contém product_id duplicado")

variable_ids: set[str] = set()
passport_ids: set[str] = set()
for row_number, row in enumerate(variables, start=2):
    variable_id = row["variable_id"]
    passport_id = row["passport_id"]
    if not re.fullmatch(r"VR\d{6}", variable_id):
        fail(f"scientific_variables.csv linha {row_number}: variable_id inválido")
    if not re.fullmatch(r"SP\d{6}", passport_id):
        fail(f"scientific_variables.csv linha {row_number}: passport_id inválido")
    if variable_id in variable_ids or passport_id in passport_ids:
        fail(f"scientific_variables.csv linha {row_number}: identificador duplicado")
    variable_ids.add(variable_id)
    passport_ids.add(passport_id)
    if row["product_id"] not in product_index:
        fail(f"{variable_id}: product_id não existe no catálogo de produtos")
    if product_index[row["product_id"]]["resource_id"] != row["resource_id"]:
        fail(f"{variable_id}: resource_id não coincide com o produto")
    if row["review_status"] not in {"draft", "reviewed", "approved", "deprecated"}:
        fail(f"{variable_id}: review_status inválido")
    if not DATE_PATTERN.fullmatch(row["reviewed_at"]):
        fail(f"{variable_id}: reviewed_at deve usar AAAA-MM-DD")
    if not row["display_name"].strip() or not row["object_observed"].strip():
        fail(f"{variable_id}: nome e objeto observado são obrigatórios")

relation_pairs: set[tuple[str, str]] = set()
related_variables: set[str] = set()
for row_number, row in enumerate(relations, start=2):
    pair = (row["product_id"], row["variable_id"])
    if pair in relation_pairs:
        fail(f"product_variables.csv linha {row_number}: relação duplicada")
    relation_pairs.add(pair)
    if row["product_id"] not in product_index:
        fail(f"product_variables.csv linha {row_number}: produto inexistente")
    if row["variable_id"] not in variable_ids:
        fail(f"product_variables.csv linha {row_number}: variável inexistente")
    if not row["relationship_role"].strip() or not row["source_field_or_band"].strip():
        fail(f"product_variables.csv linha {row_number}: papel e campo de origem são obrigatórios")
    if not DATE_PATTERN.fullmatch(row["last_verified"]):
        fail(f"product_variables.csv linha {row_number}: last_verified inválido")
    related_variables.add(row["variable_id"])

if related_variables != variable_ids:
    missing = sorted(variable_ids - related_variables)
    fail(f"variáveis sem vínculo de produto: {', '.join(missing)}")

if not PASSPORTS_PATH.exists() or PASSPORTS_PATH.stat().st_size == 0:
    fail("scientific_variable_passports.json ausente ou vazio")
passports = json.loads(PASSPORTS_PATH.read_text(encoding="utf-8"))
if not isinstance(passports, list) or len(passports) != len(variables):
    fail("scientific_variable_passports.json deve conter uma ficha por variável piloto")

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
required = set(schema["required"])
properties = schema["properties"]
domain_enum = set(properties["domain_tags"]["items"]["enum"])
data_type_enum = set(properties["data_type"]["enum"])
method_enum = set(properties["method_type"]["enum"])
sensitivity_enum = set(properties["sensitivity_class"]["enum"])
support_enum = set(properties["spatial_support"]["properties"]["support_type"]["enum"])
temporal_enum = set(properties["temporal_support"]["properties"]["representation"]["enum"])
review_enum = set(properties["review"]["properties"]["status"]["enum"])
allowed_keys = set(properties)

passport_by_variable: dict[str, dict] = {}
for index, passport in enumerate(passports, start=1):
    if not isinstance(passport, dict):
        fail(f"passaporte {index}: objeto JSON inválido")
    missing = sorted(required - set(passport))
    extra = sorted(set(passport) - allowed_keys)
    if missing:
        fail(f"passaporte {index}: campos obrigatórios ausentes: {', '.join(missing)}")
    if extra:
        fail(f"passaporte {index}: campos não permitidos: {', '.join(extra)}")
    variable_id = passport["variable_id"]
    passport_id = passport["passport_id"]
    if variable_id not in variable_ids or passport_id not in passport_ids:
        fail(f"passaporte {index}: IDs não constam do registro CSV")
    if variable_id in passport_by_variable:
        fail(f"passaporte duplicado para {variable_id}")
    if not set(passport["domain_tags"]).issubset(domain_enum):
        fail(f"{variable_id}: domain_tags fora do vocabulário")
    if passport["data_type"] not in data_type_enum:
        fail(f"{variable_id}: data_type inválido")
    if passport["method_type"] not in method_enum:
        fail(f"{variable_id}: method_type inválido")
    if passport.get("sensitivity_class", "public") not in sensitivity_enum:
        fail(f"{variable_id}: sensitivity_class inválida")
    if passport["spatial_support"].get("support_type") not in support_enum:
        fail(f"{variable_id}: suporte espacial inválido")
    if passport["temporal_support"].get("representation") not in temporal_enum:
        fail(f"{variable_id}: suporte temporal inválido")
    review = passport["review"]
    if review.get("status") not in review_enum or not DATE_PATTERN.fullmatch(review.get("reviewed_at", "")):
        fail(f"{variable_id}: revisão inválida")
    provenance = passport["provenance"]
    product_id = provenance.get("product_id")
    resource_id = provenance.get("resource_id")
    if product_id not in product_index:
        fail(f"{variable_id}: produto de proveniência inexistente")
    if product_index[product_id]["resource_id"] != resource_id:
        fail(f"{variable_id}: proveniência fonte–produto inconsistente")
    if not passport["limitations"] or any(len(item.strip()) < 5 for item in passport["limitations"]):
        fail(f"{variable_id}: limitações insuficientes")
    passport_by_variable[variable_id] = passport

for row in variables:
    passport = passport_by_variable[row["variable_id"]]
    if passport["passport_id"] != row["passport_id"]:
        fail(f"{row['variable_id']}: passport_id diverge entre CSV e JSON")
    if passport["display_name"] != row["display_name"]:
        fail(f"{row['variable_id']}: display_name diverge entre CSV e JSON")
    if passport["data_type"] != row["data_type"]:
        fail(f"{row['variable_id']}: data_type diverge entre CSV e JSON")
    if passport["provenance"]["product_id"] != row["product_id"]:
        fail(f"{row['variable_id']}: product_id diverge entre CSV e JSON")
    if passport["provenance"]["source_variable_name"] != row["source_variable_name"]:
        fail(f"{row['variable_id']}: variável de origem diverge entre CSV e JSON")

print(
    "OK: registro científico de variáveis validado — "
    f"{len(variables)} variáveis, {len(passports)} passaportes e {len(relations)} vínculos produto–variável"
)
