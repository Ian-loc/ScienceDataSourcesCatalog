#!/usr/bin/env python3
"""Validate the pre-promotion resolution contracts for the PRODES family."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from validate_prodes_amazon_geopackage_composition_guard import main as validate_geopackage_composition
from validate_prodes_operational_evidence import main as validate_operational_evidence

PATH = Path("database/mappings/prodes_product_targets.json")
TEMPORAL_GUARD_PATH = Path("database/mappings/prodes_current_temporal_cycle_guard_2026.json")
EXPECTED_TYPES = {"map_series", "indicator_series"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", "historical_only"}
REQUIRED_TARGET_FIELDS = {
    "candidate_stable_id", "name_pt", "product_type", "scientific_object",
    "support_type", "resolved_fields", "evidence_findings",
    "required_evidence_before_promotion", "unknown_fields", "non_representations",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def require_non_empty_list(candidate_id: str, target: dict, field: str) -> list:
    value = target[field]
    if not isinstance(value, list) or not value:
        fail(f"{candidate_id}: {field} deve ser lista não vazia")
    return value


def validate_current_temporal_cycle_guard(targets: list[dict]) -> None:
    if not TEMPORAL_GUARD_PATH.is_file():
        fail(f"portão temporal vigente ausente: {TEMPORAL_GUARD_PATH}")

    guard = json.loads(TEMPORAL_GUARD_PATH.read_text(encoding="utf-8"))
    if guard.get("family_stable_id") != "PF000001":
        fail("portão temporal deve permanecer vinculado à família PF000001")
    if guard.get("status") != "current_method_confirmation_required":
        fail("portão temporal deve exigir confirmação da metodologia vigente")
    if guard.get("promotion_authorized") is not False:
        fail("portão temporal não pode autorizar promoção")
    if guard.get("timezone") != "America/Sao_Paulo":
        fail("timezone do portão temporal deve ser America/Sao_Paulo")

    affected = guard.get("affected_targets")
    if not isinstance(affected, list) or len(affected) != 2:
        fail("portão temporal deve abranger exatamente os dois produtos-alvo iniciais")

    target_ids = {target["candidate_stable_id"] for target in targets}
    guarded_ids: set[str] = set()
    for item in affected:
        candidate_id = item.get("candidate_stable_id")
        if candidate_id not in target_ids:
            fail(f"portão temporal referencia produto-alvo inexistente: {candidate_id}")
        if candidate_id in guarded_ids:
            fail(f"produto-alvo duplicado no portão temporal: {candidate_id}")
        guarded_ids.add(candidate_id)
        if item.get("field") != "temporal_cycle":
            fail(f"{candidate_id}: portão deve atuar sobre temporal_cycle")
        if item.get("current_evidence_state") != "historical_only":
            fail(f"{candidate_id}: evidência atual deve permanecer historical_only")
        if item.get("promotion_state") != "blocked_pending_current_method_confirmation":
            fail(f"{candidate_id}: temporal_cycle deve permanecer bloqueado para promoção")

    if guarded_ids != target_ids:
        fail("portão temporal deve cobrir mapa anual e taxa anual")

    evidence = guard.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        fail("portão temporal deve registrar evidência")
    for record in evidence:
        if record.get("supports_current_method_contract") is not False:
            fail("evidência histórica não pode declarar suporte ao método vigente")

    for field in ("required_resolution", "normalization_rules", "prohibited_inferences"):
        value = guard.get(field)
        if not isinstance(value, list) or not value:
            fail(f"portão temporal deve possuir {field} não vazio")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("family_stable_id") != "PF000001":
        fail("família PRODES deve permanecer PF000001")
    if data.get("resolution_status") != "pre_promotion":
        fail("contrato deve permanecer em pre_promotion")
    if data.get("promotion_authorized") is not False:
        fail("promoção não pode estar autorizada neste estágio")

    policy = data.get("evidence_policy")
    if not isinstance(policy, dict) or policy.get("official_sources_required") is not True:
        fail("política deve exigir fontes oficiais")
    if policy.get("historical_evidence_does_not_define_current_method") is not True:
        fail("evidência histórica não pode definir automaticamente o método vigente")
    if policy.get("timezone") != "America/Sao_Paulo":
        fail("timezone do contrato deve ser America/Sao_Paulo")

    sources = data.get("evidence_sources")
    if not isinstance(sources, list) or len(sources) < 4:
        fail("contrato deve conter ao menos quatro registros de evidência oficial")
    source_ids: set[str] = set()
    for source in sources:
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            fail("toda evidência deve possuir source_id")
        if source_id in source_ids:
            fail(f"source_id duplicado: {source_id}")
        source_ids.add(source_id)
        url = source.get("url")
        if not isinstance(url, str) or urlparse(url).scheme != "https":
            fail(f"{source_id}: URL oficial HTTPS obrigatória")
        host = (urlparse(url).hostname or "").lower()
        if not (host.endswith("gov.br") or host.endswith("inpe.br")):
            fail(f"{source_id}: domínio não reconhecido como oficial: {host}")
        supports = source.get("supports")
        if not isinstance(supports, list) or not supports:
            fail(f"{source_id}: supports deve ser lista não vazia")

    targets = data.get("targets")
    if not isinstance(targets, list) or len(targets) != 2:
        fail("devem existir exatamente dois produtos-alvo iniciais")

    ids: set[str] = set()
    types: set[str] = set()
    for target in targets:
        missing = REQUIRED_TARGET_FIELDS - set(target)
        if missing:
            fail(f"campos ausentes em produto-alvo: {sorted(missing)}")
        candidate_id = target["candidate_stable_id"]
        if candidate_id in ids:
            fail(f"candidate_stable_id duplicado: {candidate_id}")
        ids.add(candidate_id)
        types.add(target["product_type"])

        resolved = target["resolved_fields"]
        if not isinstance(resolved, dict) or not resolved:
            fail(f"{candidate_id}: resolved_fields deve ser objeto não vazio")
        unknown = require_non_empty_list(candidate_id, target, "unknown_fields")
        require_non_empty_list(candidate_id, target, "required_evidence_before_promotion")
        require_non_empty_list(candidate_id, target, "non_representations")
        findings = require_non_empty_list(candidate_id, target, "evidence_findings")

        overlap = set(resolved).intersection(unknown)
        if overlap:
            fail(f"{candidate_id}: campos simultaneamente resolvidos e desconhecidos: {sorted(overlap)}")

        finding_fields: set[str] = set()
        for finding in findings:
            field = finding.get("field")
            confidence = finding.get("confidence")
            cited = finding.get("source_ids")
            if not isinstance(field, str) or not field:
                fail(f"{candidate_id}: finding sem field")
            if field in finding_fields:
                fail(f"{candidate_id}: finding duplicado para {field}")
            finding_fields.add(field)
            if confidence not in ALLOWED_CONFIDENCE:
                fail(f"{candidate_id}/{field}: confidence inválida: {confidence}")
            if not isinstance(cited, list) or not cited:
                fail(f"{candidate_id}/{field}: source_ids deve ser lista não vazia")
            missing_sources = set(cited) - source_ids
            if missing_sources:
                fail(f"{candidate_id}/{field}: fontes inexistentes: {sorted(missing_sources)}")
            if confidence == "historical_only" and finding.get("promotion_status") != "requires_current_method_confirmation":
                fail(f"{candidate_id}/{field}: evidência histórica deve manter portão de confirmação vigente")

    if types != EXPECTED_TYPES:
        fail(f"tipos esperados {sorted(EXPECTED_TYPES)}, encontrados {sorted(types)}")

    by_type = {target["product_type"]: target for target in targets}
    map_target = by_type["map_series"]
    rate_target = by_type["indicator_series"]
    if map_target["resolved_fields"].get("historical_availability") != "incrementos anuais individualizados a partir de 2008; 1988–2007 agregados":
        fail("contrato cartográfico deve preservar a descontinuidade histórica 1988–2007/2008+")
    if "current_minimum_mapping_unit" not in map_target["unknown_fields"]:
        fail("unidade mínima vigente deve permanecer desconhecida até metodologia atual")

    rate_fields = rate_target["resolved_fields"]
    if rate_fields.get("measurement_unit") != "km²/ano":
        fail("taxa anual deve registrar unidade km²/ano")
    if rate_fields.get("territorial_levels") != ["Amazônia Legal", "estado"]:
        fail("níveis territoriais da taxa devem ser Amazônia Legal e estado")
    if rate_fields.get("series_start") != 1988:
        fail("série de taxas deve iniciar em 1988")

    non_representations_text = " ".join(rate_target["non_representations"]).casefold()
    if not any(term in non_representations_text for term in ("município", "municipio", "municipal")):
        fail("taxa deve excluir interpretação como indicador municipal direto")

    serialized = PATH.read_text(encoding="utf-8")
    for token in ("release_id\"", "promotion_authorized\": true"):
        if token in serialized:
            fail(f"promoção prematura detectada: {token}")

    validate_current_temporal_cycle_guard(targets)
    validate_operational_evidence()
    validate_geopackage_composition()
    print("OK: PRODES separado em mapa e taxa, com evidências oficiais, portões temporal e de pacote, operação validada e promoção bloqueada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
