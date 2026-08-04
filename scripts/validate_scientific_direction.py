#!/usr/bin/env python3
"""Validate the project's scientific direction, contracts, and current N0 safeguards."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIRECTION = ROOT / "docs" / "PROJECT_SCIENTIFIC_DIRECTION.md"
POLICY = ROOT / "docs" / "policies" / "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md"
AUDIT = ROOT / "docs" / "audits" / "SCIENTIFIC_DIRECTION_TRANSITION_AUDIT_2026-08-04.md"
ROADMAP = ROOT / "docs" / "roadmap" / "SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md"
REGISTRY = ROOT / "data" / "federated_layers.json"
EXPLORER = ROOT / "explorer.html"
README = ROOT / "README.md"
GOVERNANCE = ROOT / "docs" / "GOVERNANCE.md"
METHODOLOGY = ROOT / "METHODOLOGY.md"
PRODUCT_MODEL = ROOT / "PRODUCT_CATALOG_MODEL.md"

SCHEMAS = (
    ROOT / "schema" / "scientific-variable-passport-v0.1.json",
    ROOT / "schema" / "comparability-assessment-v0.1.json",
    ROOT / "schema" / "scientific-relation-evidence-v0.1.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


required_files = (
    DIRECTION,
    POLICY,
    AUDIT,
    ROADMAP,
    REGISTRY,
    EXPLORER,
    README,
    GOVERNANCE,
    METHODOLOGY,
    PRODUCT_MODEL,
    *SCHEMAS,
)
for path in required_files:
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")

policy = POLICY.read_text(encoding="utf-8")
for token in (
    "Sobreposição não é harmonização",
    "Semáforo de comparabilidade",
    "Bússola de evidências",
    "Teto de inferência",
    "N0 — composição visual",
    "N5 — inferência causal condicionada",
):
    if token not in policy:
        fail(f"política sem requisito obrigatório: {token}")

direction = DIRECTION.read_text(encoding="utf-8")
for token in (
    "Simbioscópio",
    "A vida acontece em relação",
    "sociedade, saúde, economia, governança, território e natureza",
    "A versão atual do Explorador Federado constitui o fundamento técnico inicial",
):
    if token not in direction:
        fail(f"direção científica incompleta: {token}")

roadmap = ROADMAP.read_text(encoding="utf-8")
for phase in range(0, 8):
    if f"Fase {phase}" not in roadmap:
        fail(f"roadmap sem Fase {phase}")
if "Laboratório de Nexos" not in roadmap or "Saúde Única" not in roadmap:
    fail("roadmap não cobre laboratório de nexos e Saúde Única")

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

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
if registry.get("registry_version") != "0.2.0":
    fail("registro federado deve usar versão 0.2.0 após incorporação dos controles")
if registry.get("operation_mode") != "visual_composition_only":
    fail("explorador atual deve permanecer em visual_composition_only")
if registry.get("inference_ceiling") != "N0":
    fail("explorador atual deve declarar teto N0")
if registry.get("analytical_use_allowed") is not False:
    fail("explorador atual deve proibir uso analítico")
policy_reference = registry.get("scientific_policy", {})
if policy_reference.get("document_path") != "docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md":
    fail("registro não referencia a política científica normativa")
if policy_reference.get("comparability_model") != "A-E" or policy_reference.get("inference_model") != "N0-N5":
    fail("registro não declara modelos A-E e N0-N5")

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
        fail(f"{layer.get('layer_id')}: evidência deve permanecer not_assessed no MVP")
    if layer.get("operation_scope") != ["visual_overlay"]:
        fail(f"{layer.get('layer_id')}: escopo atual deve ser somente visual_overlay")

explorer = EXPLORER.read_text(encoding="utf-8")
for token in (
    "Simbioscópio",
    "N0 — composição visual",
    "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
    "nenhuma inferência estatística ou causal",
):
    if token not in explorer:
        fail(f"explorer.html não comunica controle obrigatório: {token}")

readme = README.read_text(encoding="utf-8")
for path in (
    "docs/PROJECT_SCIENTIFIC_DIRECTION.md",
    "docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
    "docs/roadmap/SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md",
    "docs/audits/SCIENTIFIC_DIRECTION_TRANSITION_AUDIT_2026-08-04.md",
):
    if path not in readme:
        fail(f"README não referencia {path}")

governance = GOVERNANCE.read_text(encoding="utf-8")
if "PROJECT_SCIENTIFIC_DIRECTION.md" not in governance:
    fail("governança não reconhece a direção científica")
if "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md" not in governance:
    fail("governança não reconhece a política de comparabilidade")

methodology = METHODOLOGY.read_text(encoding="utf-8")
if "camada de variáveis e passaportes científicos" not in methodology:
    fail("metodologia não delimita a nova camada científica")

product_model = PRODUCT_MODEL.read_text(encoding="utf-8")
for token in ("Passaporte científico", "Avaliação de comparabilidade", "Relação e evidência"):
    if token not in product_model:
        fail(f"modelo de produtos não incorpora extensão: {token}")

print(
    "OK: direção científica validada — política normativa, contratos v0.1, "
    "roadmap, auditoria e explorador atual restrito a N0/classe C"
)
