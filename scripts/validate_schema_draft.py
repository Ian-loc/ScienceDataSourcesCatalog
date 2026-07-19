#!/usr/bin/env python3
"""Valida a proposta de esquema 0.8.0 sem migrar o CSV 0.7.0."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "v0.8.0-draft.json"
CSV_PATH = ROOT / "data" / "data_resources.csv"
AUDIT_PATH = ROOT / "DATA1_SCHEMA_AUDIT.md"

CURRENT_FIELDS = [
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
NEW_FIELDS = {
    "resource_type", "geographic_scope", "access_tools", "citation_guidance_url"
}
EXPECTED_RESOURCE_TYPES = {
    "database", "repository", "catalog", "portal", "platform",
    "information_system", "monitoring_system", "data_service",
    "data_network", "publishing_software",
}
EXPECTED_SCOPES = {
    "local", "subnational", "national", "regional", "continental",
    "global", "variable", "not_applicable",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


if not SCHEMA_PATH.exists():
    fail("schema/v0.8.0-draft.json ausente")
if not AUDIT_PATH.exists():
    fail("DATA1_SCHEMA_AUDIT.md ausente")

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
if schema.get("schema_version") != "0.8.0-draft":
    fail("schema_version deve ser 0.8.0-draft")
if schema.get("status") != "proposal":
    fail("status deve permanecer proposal durante a auditoria")
if schema.get("record_unit") != "source":
    fail("a unidade de registro deve permanecer source")

field_order = schema.get("field_order")
if not isinstance(field_order, list) or len(field_order) != 38:
    fail("field_order deve conter exatamente 38 campos")
if len(field_order) != len(set(field_order)):
    fail("field_order contém campos duplicados")
if not set(CURRENT_FIELDS).issubset(field_order):
    missing = sorted(set(CURRENT_FIELDS).difference(field_order))
    fail(f"campos atuais ausentes da proposta: {', '.join(missing)}")
if set(field_order).difference(CURRENT_FIELDS) != NEW_FIELDS:
    fail("a proposta deve acrescentar somente os quatro campos aprovados")

new_fields = schema.get("new_fields", {})
if set(new_fields) != NEW_FIELDS:
    fail("new_fields não corresponde aos quatro campos propostos")
if set(new_fields["resource_type"].get("values", [])) != EXPECTED_RESOURCE_TYPES:
    fail("vocabulário de resource_type divergente")
if "dataset" in new_fields["resource_type"].get("values", []):
    fail("dataset não pode ser resource_type na unidade source")
if set(new_fields["geographic_scope"].get("values", [])) != EXPECTED_SCOPES:
    fail("vocabulário de geographic_scope divergente")
if new_fields["citation_guidance_url"].get("format") != "https_url":
    fail("citation_guidance_url deve exigir HTTPS")

controlled = schema.get("controlled_values", {})
for required in (
    "free_download", "programmatic_access", "authentication_required",
    "covers_brazil", "academic_evidence_type", "institutional_status",
    "data_formats", "access_protocols", "data_sources",
):
    values = controlled.get(required)
    if not isinstance(values, list) or not values or len(values) != len(set(values)):
        fail(f"vocabulário inválido ou duplicado: {required}")

rules = schema.get("cross_validation_rules", [])
if len(rules) < 10 or len(rules) != len(set(rules)):
    fail("regras cruzadas insuficientes ou duplicadas")

policy = schema.get("migration_policy", {})
if policy.get("automatic_migration_allowed") is not False:
    fail("migração automática deve permanecer bloqueada")
if policy.get("preserve_all_51_resource_ids") is not True:
    fail("política deve preservar os 51 IDs")
if policy.get("target_release") != "0.8.0":
    fail("target_release deve ser 0.8.0")
if policy.get("doi_allowed") is not False:
    fail("DOI deve permanecer bloqueado na versão 0.8.0")

with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.reader(handle)
    current_header = next(reader)
    rows = list(reader)

if current_header != CURRENT_FIELDS:
    fail("o CSV foi alterado prematuramente durante o ciclo de auditoria")
if len(rows) != 51:
    fail(f"o CSV deve manter 51 registros durante a auditoria; encontrados {len(rows)}")

text = AUDIT_PATH.read_text(encoding="utf-8")
for token in (
    "38 campos", "resource_type", "geographic_scope", "access_tools",
    "citation_guidance_url", "0.8.0", "51 IDs preservados",
):
    if token not in text:
        fail(f"auditoria não documenta requisito: {token}")

print("OK: proposta 0.8.0 válida; CSV 0.7.0 preservado com 51 fontes e 34 campos")
