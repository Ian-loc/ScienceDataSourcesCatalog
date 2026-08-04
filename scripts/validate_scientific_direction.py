#!/usr/bin/env python3
"""Validate Instance 1 direction, relational contracts, and preserved N0 safeguards."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIRECTION = ROOT / "docs" / "PROJECT_SCIENTIFIC_DIRECTION.md"
INSTANCE1 = ROOT / "docs" / "INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md"
DECISION = ROOT / "docs" / "decisions" / "DEC-INSTANCE1-RELATIONAL-CORE.md"
POLICY = ROOT / "docs" / "policies" / "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md"
AUDIT = ROOT / "docs" / "audits" / "INSTANCE_1_CONSOLIDATION_AUDIT_2026-08-04.md"
ROADMAP = ROOT / "docs" / "roadmap" / "SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md"
CURATION = ROOT / "docs" / "roadmap" / "INSTANCE_1_CURATION_WORKFLOW.md"
DATABASE_README = ROOT / "database" / "README.md"
CORE_SQL = ROOT / "database" / "schema" / "001_instance1_core.sql"
STAGING_SQL = ROOT / "database" / "schema" / "002_legacy_staging.sql"
REGISTRY = ROOT / "data" / "federated_layers.json"
EXPLORER = ROOT / "explorer.html"
README = ROOT / "README.md"
GOVERNANCE = ROOT / "docs" / "GOVERNANCE.md"
METHODOLOGY = ROOT / "METHODOLOGY.md"
PRODUCT_MODEL = ROOT / "PRODUCT_CATALOG_MODEL.md"
CODEBOOK = ROOT / "CODEBOOK.md"

SCHEMAS = (
    ROOT / "schema" / "scientific-variable-passport-v0.1.json",
    ROOT / "schema" / "comparability-assessment-v0.1.json",
    ROOT / "schema" / "scientific-relation-evidence-v0.1.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def require_tokens(path: Path, tokens: tuple[str, ...], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            fail(f"{label} sem requisito obrigatório: {token}")


required_files = (
    DIRECTION,
    INSTANCE1,
    DECISION,
    POLICY,
    AUDIT,
    ROADMAP,
    CURATION,
    DATABASE_README,
    CORE_SQL,
    STAGING_SQL,
    REGISTRY,
    EXPLORER,
    README,
    GOVERNANCE,
    METHODOLOGY,
    PRODUCT_MODEL,
    CODEBOOK,
    *SCHEMAS,
)
for path in required_files:
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")

require_tokens(
    DIRECTION,
    (
        "Instância 1 — Catálogo relacional científico-operacional",
        "Symbiotrama",
        "PostgreSQL",
        "Instância 2 — composição geográfica",
        "Instância 3 — contexto científico",
    ),
    "direção científica",
)

require_tokens(
    INSTANCE1,
    (
        "Produto científico",
        "mensagem informacional",
        "PostgreSQL com PostGIS",
        "metadata_assertions",
        "Instâncias 2 e 3 — registro somente para leitura",
    ),
    "documento da Instância 1",
)

require_tokens(
    POLICY,
    (
        "guardrail futuro",
        "Sobreposição cartográfica não constitui harmonização",
        "N0 — composição visual",
        "N5 — inferência causal condicionada",
        "A Instância 1 não atribui nenhum desses níveis",
    ),
    "política futura",
)

roadmap = ROADMAP.read_text(encoding="utf-8")
for phase in ("I1.0", "I1.1", "I1.2", "I1.3", "I1.4", "I1.5"):
    if f"Fase {phase}" not in roadmap:
        fail(f"roadmap sem Fase {phase}")
for token in ("Instância 2 — backlog de longo prazo", "Instância 3 — backlog de longo prazo"):
    if token not in roadmap:
        fail(f"roadmap sem limite futuro: {token}")

require_tokens(
    CURATION,
    (
        "um produto integralmente inspecionado",
        "Etapa A — resolução do objeto",
        "Etapa I — auditoria",
        "não tratar serviço ou catálogo como produto científico",
    ),
    "workflow de curadoria",
)

require_tokens(
    CORE_SQL,
    (
        "CREATE SCHEMA IF NOT EXISTS catalog",
        "CREATE TABLE catalog.sources",
        "CREATE TABLE catalog.products",
        "CREATE TABLE catalog.product_releases",
        "CREATE TABLE catalog.variables",
        "CREATE TABLE catalog.product_variables",
        "CREATE TABLE catalog.metadata_assertions",
        "CREATE TABLE catalog.curation_reviews",
        "CREATE VIEW catalog.v_product_catalog",
    ),
    "schema relacional",
)

require_tokens(
    STAGING_SQL,
    (
        "CREATE SCHEMA IF NOT EXISTS staging",
        "CREATE TABLE staging.legacy_resources",
        "CREATE TABLE staging.legacy_products",
        "CREATE TABLE staging.legacy_distributions",
        "CREATE TABLE staging.migration_issues",
        "resolved_entity_type",
    ),
    "schema de staging",
)

for schema_path in SCHEMAS:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"JSON inválido em {schema_path.relative_to(ROOT)}: {exc}")
    for field in ("$schema", "$id", "title", "type", "required", "properties"):
        if field not in schema:
            fail(f"{schema_path.name}: campo de contrato ausente: {field}")
    if schema["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{schema_path.name}: draft JSON Schema inesperado")
    if schema["type"] != "object":
        fail(f"{schema_path.name}: raiz deve ser objeto")
    if not schema["required"] or not isinstance(schema["required"], list):
        fail(f"{schema_path.name}: required deve ser lista não vazia")

# The current explorer remains a restricted N0 prototype while Instance 1 is consolidated.
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
if registry.get("registry_version") != "0.2.0":
    fail("registro federado deve permanecer na versão 0.2.0")
if registry.get("operation_mode") != "visual_composition_only":
    fail("explorador atual deve permanecer em visual_composition_only")
if registry.get("inference_ceiling") != "N0":
    fail("explorador atual deve declarar teto N0")
if registry.get("analytical_use_allowed") is not False:
    fail("explorador atual deve proibir uso analítico")

policy_reference = registry.get("scientific_policy", {})
if policy_reference.get("document_path") != "docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md":
    fail("registro não referencia a política científica")

layers = registry.get("layers", [])
if not layers:
    fail("registro federado sem camadas")
for layer in layers:
    if layer.get("compatibility_class") != "C":
        fail(f"{layer.get('layer_id')}: camada atual deve permanecer em classe C")
    if layer.get("inference_ceiling") != "N0":
        fail(f"{layer.get('layer_id')}: teto deve ser N0")
    if layer.get("analytical_use_allowed") is not False:
        fail(f"{layer.get('layer_id')}: uso analítico deve permanecer proibido")
    if layer.get("evidence_status") != "not_assessed":
        fail(f"{layer.get('layer_id')}: evidência deve permanecer not_assessed")
    if layer.get("operation_scope") != ["visual_overlay"]:
        fail(f"{layer.get('layer_id')}: escopo atual deve ser somente visual_overlay")

require_tokens(
    EXPLORER,
    (
        "N0 — composição visual",
        "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
        "nenhuma inferência estatística ou causal",
    ),
    "explorer.html",
)

require_tokens(
    README,
    (
        "docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md",
        "database/schema/001_instance1_core.sql",
        "docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md",
        "Instância 2 — composição geográfica",
        "Instância 3 — contexto científico",
    ),
    "README",
)

require_tokens(
    METHODOLOGY,
    (
        "Instância 1 — Catálogo relacional científico-operacional",
        "metadata_assertions",
        "Produto",
        "Release",
        "Instâncias futuras",
    ),
    "metodologia",
)

require_tokens(
    PRODUCT_MODEL,
    (
        "Produto científico",
        "Release, versão ou edição",
        "Mensagem informacional",
        "Evidência de metadados",
        "Instâncias futuras",
    ),
    "modelo de produtos",
)

require_tokens(
    CODEBOOK,
    (
        "Banco relacional da Instância 1",
        "product_releases",
        "metadata_assertions",
        "curation_reviews",
    ),
    "codebook",
)

# Governance must continue recognizing the active direction and the future guardrail.
governance = GOVERNANCE.read_text(encoding="utf-8")
if "PROJECT_SCIENTIFIC_DIRECTION.md" not in governance:
    fail("governança não reconhece a direção científica")
if "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md" not in governance:
    fail("governança não reconhece a política científica")

print(
    "OK: Instância 1 validada — direção relacional, contratos, staging, "
    "curadoria e explorador legado preservado em N0/classe C"
)
