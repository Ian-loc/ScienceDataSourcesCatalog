#!/usr/bin/env python3
"""Validate the semantic invariants of the Simbiotrama Instance 1 minimum contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "instance1_scope_contract.json"

EXPECTED_ESSENTIAL_PROFILE_FIELDS = [
    "organization",
    "official_name",
    "entry_type",
    "summary",
    "scientific_scope",
    "data_modalities",
    "themes_or_main_variables",
    "geographic_coverage",
    "temporal_coverage",
    "material_resolution_or_support",
    "update_frequency_if_available",
    "access_conditions",
    "free_access_or_authentication",
    "official_page",
    "metadata_page",
    "primary_access",
    "methodology_if_available",
    "license_if_available",
    "citation_if_available",
    "curation_status",
    "last_verified_at",
]

EXPECTED_MATERIAL_GRANULARITY_DIFFERENCES = [
    "scientific_meaning",
    "data_modality",
    "geographic_or_temporal_coverage",
    "method_or_purpose",
    "primary_audience_or_use",
    "primary_access_path",
]

EXPECTED_ENTRY_STATUSES = ["needs_review", "partially_verified", "verified"]
EXPECTED_FIELD_STATUSES = [
    "needs_review",
    "partially_verified",
    "verified",
    "not_found",
    "not_applicable",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


if not CONTRACT_PATH.exists():
    fail("contrato mínimo ausente")

try:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    fail(f"contrato JSON inválido: {exc}")

if not isinstance(contract, dict):
    fail("contrato deve ser um objeto JSON")

if contract.get("central_unit") != "catalog_entry":
    fail("central_unit deve permanecer catalog_entry")

if contract.get("essential_profile_fields") != EXPECTED_ESSENTIAL_PROFILE_FIELDS:
    fail("ficha essencial divergiu; alteração exige decisão explícita de escopo")

if contract.get("material_granularity_differences") != EXPECTED_MATERIAL_GRANULARITY_DIFFERENCES:
    fail("critérios de diferença material de granularidade divergiram")

if contract.get("entry_curation_statuses") != EXPECTED_ENTRY_STATUSES:
    fail("domínio global de curadoria da entrada divergiu")

if contract.get("field_evidence_statuses") != EXPECTED_FIELD_STATUSES:
    fail("domínio de evidência por campo divergiu")

if {"not_found", "not_applicable"} & set(contract.get("entry_curation_statuses", [])):
    fail("not_found/not_applicable não podem ser estados globais da entrada")

non_material = set(contract.get("non_material_split_reasons", []))
required_non_material = {"file", "format", "layer", "band", "endpoint", "technical_update"}
if not required_non_material.issubset(non_material):
    fail("razões técnicas proibidas de subdivisão foram enfraquecidas")

for key in ("external_dataset_storage", "external_catalog_replication", "full_genealogy_required"):
    if contract.get(key) is not False:
        fail(f"{key} deve permanecer false")

if contract.get("merge_requires_exact_sha_authorization") is not True:
    fail("merge deve continuar exigindo autorização do SHA exato")

print(
    "OK: ficha essencial, granularidade material, estados curatoriais e limites "
    "do contrato mínimo da Instância 1 estão íntegros"
)
