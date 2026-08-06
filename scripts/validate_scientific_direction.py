#!/usr/bin/env python3
"""Validate Simbiotrama Instance 1 scope, authority, and legacy safeguards."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    "scope_contract": ROOT / "config" / "instance1_scope_contract.json",
    "project_state": ROOT / "docs" / "PROJECT_STATE.md",
    "direction": ROOT / "docs" / "PROJECT_SCIENTIFIC_DIRECTION.md",
    "instance1": ROOT / "docs" / "INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md",
    "scope_policy": ROOT / "docs" / "policies" / "INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md",
    "decision_minimum": ROOT / "docs" / "decisions" / "DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md",
    "decision_deep": ROOT / "docs" / "decisions" / "DEC-INSTANCE1-RELATIONAL-CORE.md",
    "roadmap": ROOT / "docs" / "roadmap" / "SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md",
    "roadmap_alias": ROOT / "docs" / "roadmap" / "SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md",
    "curation": ROOT / "docs" / "roadmap" / "INSTANCE_1_CURATION_WORKFLOW.md",
    "migration_plan": ROOT / "docs" / "roadmap" / "INSTANCE_1_MINIMUM_SCHEMA_MIGRATION_PLAN.md",
    "golden_cases": ROOT / "docs" / "audits" / "INSTANCE_1_MINIMUM_MODEL_GOLDEN_CASES_2026-08-06.md",
    "realignment_audit": ROOT / "docs" / "audits" / "INSTANCE_1_SCOPE_REALIGNMENT_AUDIT_2026-08-06.md",
    "future_policy": ROOT / "docs" / "policies" / "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
    "readme": ROOT / "README.md",
    "governance": ROOT / "docs" / "GOVERNANCE.md",
    "methodology": ROOT / "METHODOLOGY.md",
    "product_model": ROOT / "PRODUCT_CATALOG_MODEL.md",
    "codebook": ROOT / "CODEBOOK.md",
    "selection": ROOT / "SELECTION_AND_COVERAGE_POLICY.md",
    "database_readme": ROOT / "database" / "README.md",
    "pr_template": ROOT / ".github" / "pull_request_template.md",
    "core_sql": ROOT / "database" / "schema" / "001_instance1_core.sql",
    "staging_sql": ROOT / "database" / "schema" / "002_legacy_staging.sql",
    "registry": ROOT / "data" / "federated_layers.json",
    "explorer": ROOT / "explorer.html",
    "milestone_status": ROOT / "docs" / "milestones" / "MILESTONE_STATUS.json",
}

BACKLOG_SCHEMAS = (
    ROOT / "schema" / "scientific-variable-passport-v0.1.json",
    ROOT / "schema" / "comparability-assessment-v0.1.json",
    ROOT / "schema" / "scientific-relation-evidence-v0.1.json",
)

EXPECTED_ENTRY_TYPES = [
    "source",
    "platform",
    "collection",
    "data_product",
    "data_service",
]
EXPECTED_CORE_ENTITIES = [
    "organizations",
    "catalog_entries",
    "entry_variables",
    "entry_evidence",
]
EXPECTED_OPTIONAL_ENTITIES = ["connector_profiles"]
EXPECTED_SCOPE_USES = [
    "catalog_discovery",
    "minimum_interpretation",
    "website_filter_or_display",
    "selected_connector",
]
EXPECTED_STATUSES = [
    "needs_review",
    "partially_verified",
    "verified",
    "not_found",
    "not_applicable",
]
EXPECTED_GOLDEN_CASES = ["GEDI", "DETER Cerrado", "IBGE", "ANA/SNIRH"]
EXPECTED_NON_MATERIAL_SPLITS = {
    "file",
    "format",
    "layer",
    "band",
    "endpoint",
    "internal_table",
    "directory",
    "technical_update",
}
EXPECTED_FORBIDDEN_ROUTINE_REQUIREMENTS = {
    "complete_release_resolution",
    "asset_inventory",
    "byte_inspection",
    "checksum",
    "complete_physical_schema",
    "all_layers_inventory",
    "all_endpoints_validation",
    "file_level_license",
    "file_level_citation",
    "forensic_evidence_package",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def text(name: str) -> str:
    path = PATHS[name]
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def json_object(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size == 0:
        fail(f"JSON ausente ou vazio: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"JSON inválido em {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON raiz não é objeto: {path.relative_to(ROOT)}")
    return value


def require_tokens(name: str, required: tuple[str, ...]) -> None:
    value = text(name)
    missing = [token for token in required if token not in value]
    if missing:
        fail(f"{PATHS[name].relative_to(ROOT)} sem requisitos: {missing}")


def forbid_tokens(name: str, forbidden: tuple[str, ...]) -> None:
    value = text(name)
    present = [token for token in forbidden if token in value]
    if present:
        fail(f"{PATHS[name].relative_to(ROOT)} contém direção aposentada: {present}")


# 1. Machine-readable scope contract.
for name in PATHS:
    text(name)
contract = json_object(PATHS["scope_contract"])

if contract.get("contract_version") != "1.0.0":
    fail("versão inesperada do contrato de escopo")
if contract.get("project") != "Simbiotrama":
    fail("projeto inconsistente no contrato de escopo")
if contract.get("central_unit") != "catalog_entry":
    fail("unidade central deve ser catalog_entry")
if contract.get("entry_types") != EXPECTED_ENTRY_TYPES:
    fail("entry_types divergentes do contrato aprovado")
if contract.get("core_entities") != EXPECTED_CORE_ENTITIES:
    fail("core_entities divergentes do núcleo mínimo")
if contract.get("optional_entities") != EXPECTED_OPTIONAL_ENTITIES:
    fail("optional_entities divergentes")
if contract.get("scope_gate_use_cases") != EXPECTED_SCOPE_USES:
    fail("gate de escopo divergente")
if contract.get("curation_statuses") != EXPECTED_STATUSES:
    fail("estados curatoriais divergentes")
if contract.get("golden_cases") != EXPECTED_GOLDEN_CASES:
    fail("casos dourados divergentes")
if set(contract.get("non_material_split_reasons", [])) != EXPECTED_NON_MATERIAL_SPLITS:
    fail("razões não materiais de subdivisão divergentes")
if set(contract.get("routine_requirements_forbidden", [])) != EXPECTED_FORBIDDEN_ROUTINE_REQUIREMENTS:
    fail("requisitos rotineiros proibidos divergentes")
for flag in (
    "external_dataset_storage",
    "external_catalog_replication",
    "full_genealogy_required",
):
    if contract.get(flag) is not False:
        fail(f"{flag} deve permanecer false")
if contract.get("merge_requires_exact_sha_authorization") is not True:
    fail("merge deve exigir autorização do SHA exato")
if contract.get("instance_2_status") != "backlog" or contract.get("instance_3_status") != "backlog":
    fail("Instâncias 2 e 3 devem permanecer em backlog")

# 2. Active authority must reflect the contract.
require_tokens(
    "project_state",
    (
        "entrada de catálogo de granularidade mínima suficiente",
        "I1-S1 — simplificação governada da Instância 1",
        "PR #57",
        "`ACTIVE`",
        "`BACKLOG`",
        "`LEGACY_OPERATIONAL`",
        "`RETIRED`",
        "`HISTORICAL_EVIDENCE`",
    ),
)
require_tokens(
    "direction",
    (
        "entrada de catálogo",
        "metadados essenciais",
        "Instância 2",
        "Instância 3",
        "PostgreSQL/PostGIS",
    ),
)
require_tokens(
    "instance1",
    tuple(EXPECTED_CORE_ENTITIES + EXPECTED_OPTIONAL_ENTITIES)
    + ("catalog_entry", "Critério de completude"),
)
require_tokens(
    "scope_policy",
    (
        "granularidade mínima suficiente",
        "Gate para expansão do esquema",
        "Não se cria nova entrada apenas",
        "O Simbiotrama não é",
    ),
)
require_tokens(
    "decision_minimum",
    (
        "catálogo de granularidade mínima suficiente",
        "catalog_entry",
        "não será apagada de forma destrutiva",
        "PR #57",
    ),
)
require_tokens(
    "decision_deep",
    (
        "**Estado atual:** `SUPERSEDED`",
        "DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md",
        "legado técnico",
    ),
)

# 3. Roadmap, workflow, migration, and golden cases.
roadmap = text("roadmap")
for milestone in ("I1-M1", "I1-S1", "I1-S2", "I1-S3", "I1-S4", "I1-S5", "I1-S6", "I1-S7"):
    if milestone not in roadmap:
        fail(f"roadmap sem marco: {milestone}")
for case_name in EXPECTED_GOLDEN_CASES:
    if case_name not in roadmap:
        fail(f"roadmap sem caso dourado: {case_name}")

require_tokens(
    "curation",
    (
        "entrada de catálogo suficientemente descrita",
        "Critério de parada",
        "não reconstruir o catálogo da fonte",
        "não criar entrada apenas por formato, arquivo, layer, banda ou endpoint",
        "Uma entrada pode ser `verified`",
    ),
)
require_tokens(
    "migration_plan",
    tuple(f"catalog.{entity}" for entity in EXPECTED_CORE_ENTITIES[1:] + EXPECTED_OPTIONAL_ENTITIES)
    + ("migração sem perda, idempotente e reversível", "não promovido ao núcleo"),
)
require_tokens(
    "golden_cases",
    tuple(EXPECTED_GOLDEN_CASES) + ("inventário integral", "Testes adversariais"),
)
require_tokens(
    "realignment_audit",
    (
        "Ocorrência operacional",
        "criação da branch",
        "Controle preventivo",
        "PR #57",
        "PR #58",
    ),
)

# 4. Public and operational documents use the same minimal target.
for name in (
    "readme",
    "governance",
    "methodology",
    "product_model",
    "codebook",
    "selection",
    "database_readme",
):
    require_tokens(name, ("entrada", "catálogo"))

require_tokens("readme", tuple(EXPECTED_CORE_ENTITIES + EXPECTED_OPTIONAL_ENTITIES))
require_tokens(
    "governance",
    (
        "Gate de escopo",
        "CI verde antes do término da revisão não libera merge",
        "autorização é válida apenas para o SHA exato",
    ),
)
require_tokens("methodology", ("Regra de granularidade", "Critério de parada", "não é rotina da Instância 1"))
require_tokens("product_model", ("Entrada de catálogo", "Perfil de conector", "Não criar nova entrada somente por"))
require_tokens("codebook", tuple(EXPECTED_CORE_ENTITIES + EXPECTED_OPTIONAL_ENTITIES) + ("Estruturas profundas legadas",))
require_tokens("database_readme", ("legado técnico/extensão futura", "Núcleo mínimo proposto", "Comando destrutivo"))
require_tokens(
    "pr_template",
    (
        "Gate de escopo",
        "não reconstrói catálogo ou genealogia de terceiros",
        "critério de parada explícito",
        "nenhuma thread acionável aberta",
    ),
)

# 5. Canonical documents cannot reactivate retired completeness rules.
retired_phrases = (
    "A unidade de trabalho é **um produto ou release integralmente inspecionado**",
    "A unidade de progresso é um produto ou release integralmente inspecionado",
    "Cada produto deve possuir um perfil organizado em seis blocos",
    "uma base relacional profunda de produtos de dados",
)
for name in (
    "project_state",
    "direction",
    "instance1",
    "roadmap",
    "curation",
    "readme",
    "governance",
    "methodology",
    "product_model",
    "codebook",
    "selection",
):
    forbid_tokens(name, retired_phrases)

# 6. Preserve Milestone 1 SQL and staging until the additive migration exists.
require_tokens(
    "core_sql",
    (
        "CREATE SCHEMA IF NOT EXISTS catalog",
        "CREATE TABLE catalog.sources",
        "CREATE TABLE catalog.products",
        "CREATE TABLE catalog.product_releases",
        "CREATE TABLE catalog.data_assets",
        "CREATE TABLE catalog.metadata_assertions",
    ),
)
require_tokens(
    "staging_sql",
    (
        "CREATE SCHEMA IF NOT EXISTS staging",
        "CREATE TABLE staging.legacy_resources",
        "CREATE TABLE staging.legacy_products",
        "CREATE TABLE staging.legacy_distributions",
        "CREATE TABLE staging.migration_issues",
    ),
)

# 7. Backlog schemas remain valid JSON Schema contracts, but not active authority.
for schema_path in BACKLOG_SCHEMAS:
    schema = json_object(schema_path)
    for field in ("$schema", "$id", "title", "type", "required", "properties"):
        if field not in schema:
            fail(f"{schema_path.name}: campo ausente: {field}")
    if schema["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{schema_path.name}: draft inesperado")
    if schema["type"] != "object":
        fail(f"{schema_path.name}: raiz deve ser objeto")

require_tokens("roadmap_alias", ("`RETIRED_ALIAS`", "SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md"))
require_tokens(
    "future_policy",
    (
        "guardrail futuro",
        "Sobreposição cartográfica não constitui harmonização",
        "N0 — composição visual",
        "N5 — inferência causal condicionada",
    ),
)

# 8. The published explorer remains legacy N0.
registry = json_object(PATHS["registry"])
if registry.get("registry_version") != "0.2.0":
    fail("registro federado legado deve permanecer na versão 0.2.0")
if registry.get("operation_mode") != "visual_composition_only":
    fail("explorador legado deve permanecer em visual_composition_only")
if registry.get("inference_ceiling") != "N0":
    fail("explorador legado deve declarar teto N0")
if registry.get("analytical_use_allowed") is not False:
    fail("explorador legado deve proibir uso analítico")

layers = registry.get("layers")
if not isinstance(layers, list) or not layers:
    fail("registro federado sem camadas")
for layer in layers:
    layer_id = layer.get("layer_id", "sem_id")
    if layer.get("compatibility_class") != "C":
        fail(f"{layer_id}: classe legado deve ser C")
    if layer.get("inference_ceiling") != "N0":
        fail(f"{layer_id}: teto deve ser N0")
    if layer.get("analytical_use_allowed") is not False:
        fail(f"{layer_id}: uso analítico deve permanecer proibido")
    if layer.get("operation_scope") != ["visual_overlay"]:
        fail(f"{layer_id}: escopo deve permanecer visual_overlay")

require_tokens(
    "explorer",
    (
        "N0 — composição visual",
        "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
        "nenhuma inferência estatística ou causal",
    ),
)

# 9. Milestone 1 remains incorporated; future instances remain inactive.
milestone_status = json_object(PATHS["milestone_status"])
if milestone_status.get("project") != "Simbiotrama":
    fail("estado do Marco 1 com nome inconsistente")
if milestone_status.get("status") != "INCORPORATED":
    fail("Marco 1 deve permanecer INCORPORATED")
if milestone_status.get("instances_2_3_active") is not False:
    fail("Instâncias 2 e 3 não podem estar ativas")
if milestone_status.get("legacy_n0_explorer_active_development") is not False:
    fail("explorador legado não pode estar em desenvolvimento ativo")

print(
    "OK: contrato da Instância 1 mínima validado — autoridade, granularidade, "
    "critério de parada, migração sem perda e legado N0 coerentes"
)
