#!/usr/bin/env python3
"""Validate the minimum-sufficient scope of Simbiotrama Instance 1.

This gate protects the active catalog direction without deleting the deep relational
schema incorporated in Milestone 1. It validates active authority, scope boundaries,
legacy classification, and the N0 explorer safeguards.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "project_state": ROOT / "docs" / "PROJECT_STATE.md",
    "direction": ROOT / "docs" / "PROJECT_SCIENTIFIC_DIRECTION.md",
    "instance1": ROOT / "docs" / "INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md",
    "decision_minimum": ROOT / "docs" / "decisions" / "DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md",
    "decision_deep": ROOT / "docs" / "decisions" / "DEC-INSTANCE1-RELATIONAL-CORE.md",
    "scope_policy": ROOT / "docs" / "policies" / "INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md",
    "future_policy": ROOT / "docs" / "policies" / "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
    "roadmap": ROOT / "docs" / "roadmap" / "SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md",
    "roadmap_alias": ROOT / "docs" / "roadmap" / "SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md",
    "curation": ROOT / "docs" / "roadmap" / "INSTANCE_1_CURATION_WORKFLOW.md",
    "migration_plan": ROOT / "docs" / "roadmap" / "INSTANCE_1_MINIMUM_SCHEMA_MIGRATION_PLAN.md",
    "golden_cases": ROOT / "docs" / "audits" / "INSTANCE_1_MINIMUM_MODEL_GOLDEN_CASES_2026-08-06.md",
    "database_readme": ROOT / "database" / "README.md",
    "core_sql": ROOT / "database" / "schema" / "001_instance1_core.sql",
    "staging_sql": ROOT / "database" / "schema" / "002_legacy_staging.sql",
    "registry": ROOT / "data" / "federated_layers.json",
    "explorer": ROOT / "explorer.html",
    "readme": ROOT / "README.md",
    "governance": ROOT / "docs" / "GOVERNANCE.md",
    "methodology": ROOT / "METHODOLOGY.md",
    "product_model": ROOT / "PRODUCT_CATALOG_MODEL.md",
    "codebook": ROOT / "CODEBOOK.md",
    "selection": ROOT / "SELECTION_AND_COVERAGE_POLICY.md",
    "pr_template": ROOT / ".github" / "pull_request_template.md",
    "milestone_status": ROOT / "docs" / "milestones" / "MILESTONE_STATUS.json",
}

BACKLOG_SCHEMAS = (
    ROOT / "schema" / "scientific-variable-passport-v0.1.json",
    ROOT / "schema" / "comparability-assessment-v0.1.json",
    ROOT / "schema" / "scientific-relation-evidence-v0.1.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read(name: str) -> str:
    path = FILES[name]
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_all(name: str, required: tuple[str, ...]) -> None:
    text = read(name)
    missing = [token for token in required if token not in text]
    if missing:
        fail(f"{FILES[name].relative_to(ROOT)} sem requisitos: {missing}")


def forbid_any(name: str, forbidden: tuple[str, ...]) -> None:
    text = read(name)
    present = [token for token in forbidden if token in text]
    if present:
        fail(f"{FILES[name].relative_to(ROOT)} contém direção aposentada: {present}")


# Every declared contract must exist before semantic checks run.
for file_name in FILES:
    read(file_name)
for path in BACKLOG_SCHEMAS:
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")

# Active authority and lifecycle.
require_all(
    "project_state",
    (
        "Simbiotrama — Catálogo de Dados Científicos do Brasil",
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
require_all(
    "direction",
    (
        "entrada de catálogo",
        "granularidade",
        "Organização",
        "metadados essenciais",
        "Instância 2",
        "Instância 3",
        "PostgreSQL/PostGIS",
    ),
)
require_all(
    "instance1",
    (
        "catalog_entry",
        "organizations",
        "catalog_entries",
        "entry_variables",
        "entry_evidence",
        "connector_profiles",
        "Critério de completude",
    ),
)
require_all(
    "scope_policy",
    (
        "granularidade mínima suficiente",
        "Não se cria nova entrada apenas",
        "Gate para expansão do esquema",
        "descoberta no catálogo",
        "configuração de um conector selecionado",
        "O Simbiotrama não é",
    ),
)
require_all(
    "decision_minimum",
    (
        "catálogo de granularidade mínima suficiente",
        "catalog_entry",
        "não será apagada de forma destrutiva",
        "PR #57",
        "superseded",
    ),
)
require_all(
    "decision_deep",
    (
        "**Estado atual:** `SUPERSEDED`",
        "DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md",
        "legado técnico",
    ),
)

# Work plan and stopping rule.
roadmap = read("roadmap")
for milestone in ("I1-M1", "I1-S1", "I1-S2", "I1-S3", "I1-S4", "I1-S5", "I1-S6", "I1-S7"):
    if milestone not in roadmap:
        fail(f"roadmap sem marco vigente: {milestone}")
for case_name in ("GEDI", "DETER Cerrado", "IBGE", "ANA/SNIRH"):
    if case_name not in roadmap:
        fail(f"roadmap sem caso de validação: {case_name}")

require_all(
    "curation",
    (
        "entrada de catálogo suficientemente descrita",
        "Critério de parada",
        "não reconstruir o catálogo da fonte",
        "não criar entrada apenas por formato, arquivo, layer, banda ou endpoint",
        "Uma entrada pode ser `verified`",
    ),
)
require_all(
    "migration_plan",
    (
        "migração sem perda, idempotente e reversível",
        "catalog.catalog_entries",
        "catalog.entry_variables",
        "catalog.entry_evidence",
        "catalog.connector_profiles",
        "data_assets",
        "não promovido ao núcleo",
    ),
)
require_all(
    "golden_cases",
    (
        "GEDI",
        "DETER Cerrado",
        "IBGE",
        "ANA/SNIRH",
        "inventário integral",
        "Testes adversariais",
    ),
)

# Public and operational documents must present the same target.
for name in (
    "readme",
    "governance",
    "methodology",
    "product_model",
    "codebook",
    "selection",
    "database_readme",
):
    require_all(name, ("entrada", "catálogo"))

require_all(
    "readme",
    (
        "catalog_entries",
        "entry_variables",
        "entry_evidence",
        "connector_profiles",
        "O que não é requisito universal",
    ),
)
require_all(
    "governance",
    (
        "Gate de escopo",
        "CI verde antes do término da revisão não libera merge",
        "autorização é válida apenas para o SHA exato",
    ),
)
require_all(
    "methodology",
    (
        "Regra de granularidade",
        "Critério de parada",
        "não é rotina da Instância 1",
    ),
)
require_all(
    "product_model",
    (
        "Entrada de catálogo",
        "Perfil de conector",
        "Não criar nova entrada somente por",
    ),
)
require_all(
    "codebook",
    (
        "Núcleo mínimo proposto",
        "catalog_entries",
        "entry_variables",
        "entry_evidence",
        "connector_profiles",
        "Estruturas profundas legadas",
    ),
)
require_all(
    "database_readme",
    (
        "legado técnico/extensão futura",
        "Núcleo mínimo proposto",
        "não promover automaticamente",
        "Comando destrutivo",
    ),
)
require_all(
    "pr_template",
    (
        "Gate de escopo",
        "não reconstrói catálogo ou genealogia de terceiros",
        "critério de parada explícito",
        "nenhuma thread acionável aberta",
    ),
)

# Canonical documents may mention the deep model as retired history, but cannot
# present its former completeness rule as active policy.
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
    forbid_any(
        name,
        (
            "A unidade de trabalho é **um produto ou release integralmente inspecionado**",
            "A unidade de progresso é um produto ou release integralmente inspecionado",
            "Cada produto deve possuir um perfil organizado em seis blocos",
            "release vigente e vínculo metodológico" if name != "project_state" else "__never__",
        ),
    )

# Preserve the executable Milestone 1 schema and staging until the additive
# migration is implemented and authorized.
require_all(
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
require_all(
    "staging_sql",
    (
        "CREATE SCHEMA IF NOT EXISTS staging",
        "CREATE TABLE staging.legacy_resources",
        "CREATE TABLE staging.legacy_products",
        "CREATE TABLE staging.legacy_distributions",
        "CREATE TABLE staging.migration_issues",
    ),
)

# Backlog schemas remain syntactically valid but do not become active authority.
for schema_path in BACKLOG_SCHEMAS:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"JSON inválido em {schema_path.relative_to(ROOT)}: {exc}")
    for field in ("$schema", "$id", "title", "type", "required", "properties"):
        if field not in schema:
            fail(f"{schema_path.name}: campo ausente: {field}")
    if schema["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{schema_path.name}: draft inesperado")
    if schema["type"] != "object":
        fail(f"{schema_path.name}: raiz deve ser objeto")

require_all(
    "roadmap_alias",
    ("`RETIRED_ALIAS`", "SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md"),
)
require_all(
    "future_policy",
    (
        "guardrail futuro",
        "Sobreposição cartográfica não constitui harmonização",
        "N0 — composição visual",
        "N5 — inferência causal condicionada",
    ),
)

# The currently published explorer remains legacy N0.
registry = json.loads(FILES["registry"].read_text(encoding="utf-8"))
if registry.get("registry_version") != "0.2.0":
    fail("registro federado legado deve permanecer na versão 0.2.0")
if registry.get("operation_mode") != "visual_composition_only":
    fail("explorador legado deve permanecer em visual_composition_only")
if registry.get("inference_ceiling") != "N0":
    fail("explorador legado deve declarar teto N0")
if registry.get("analytical_use_allowed") is not False:
    fail("explorador legado deve proibir uso analítico")

layers = registry.get("layers", [])
if not layers:
    fail("registro federado sem camadas")
for layer in layers:
    layer_id = layer.get("layer_id", "sem_id")
    if layer.get("compatibility_class") != "C":
        fail(f"{layer_id}: artefato legado deve preservar classe C")
    if layer.get("inference_ceiling") != "N0":
        fail(f"{layer_id}: teto deve ser N0")
    if layer.get("analytical_use_allowed") is not False:
        fail(f"{layer_id}: uso analítico deve permanecer proibido")
    if layer.get("operation_scope") != ["visual_overlay"]:
        fail(f"{layer_id}: escopo deve permanecer visual_overlay")

require_all(
    "explorer",
    (
        "N0 — composição visual",
        "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
        "nenhuma inferência estatística ou causal",
    ),
)

milestone_status = json.loads(FILES["milestone_status"].read_text(encoding="utf-8"))
if milestone_status.get("project") != "Simbiotrama":
    fail("estado do Marco 1 com nome inconsistente")
if milestone_status.get("status") != "INCORPORATED":
    fail("Marco 1 deve permanecer INCORPORATED")
if milestone_status.get("instances_2_3_active") is not False:
    fail("Instâncias 2 e 3 não podem estar ativas")
if milestone_status.get("legacy_n0_explorer_active_development") is not False:
    fail("explorador legado não pode estar em desenvolvimento ativo")

print(
    "OK: direção mínima da Instância 1 validada — autoridade, granularidade, "
    "critério de parada, migração sem perda e legado N0 coerentes"
)
