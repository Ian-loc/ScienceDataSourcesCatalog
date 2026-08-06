#!/usr/bin/env python3
"""Validate DETER Cerrado operational legend, latency, and cycle-mask semantics."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_operational_legend_latency_guard_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def trusted_doi(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "") == "doi.org"


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("contract_version") != "1.0.0":
        fail("versão do contrato inesperada")
    if data.get("package_id") != "I1-M2A-DETER-CERRADO":
        fail("pacote inesperado")
    if data.get("family_stable_id") != "PF000003":
        fail("família inesperada")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "operational_legend_processing_latency_and_cycle_mask_resolved_validation_classes_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    source = data.get("method_source")
    if not isinstance(source, dict):
        fail("method_source deve ser objeto")
    if source.get("title") != "Metodologia dos sistemas PRODES e DETER para o bioma Cerrado":
        fail("título metodológico divergente")
    if source.get("publisher") != "Instituto Nacional de Pesquisas Espaciais — INPE":
        fail("produtor divergente")
    if source.get("publication_year") != 2024 or source.get("updated_date") != "2024-03-28":
        fail("data metodológica divergente")
    if source.get("doi") != "10.13140/RG.2.2.24196.49281":
        fail("DOI divergente")
    expected_sections = {
        "6.1 Metodologia DETER Cerrado",
        "Tabela 2 — Legenda operacional utilizada no DETER Cerrado",
        "Tabela 3 — Exemplos de padrões comuns detectados como Avisos pelo Sistema DETER Cerrado",
        "Tabela 4 — Critérios para diferenciar queimada antrópica e fogo natural no DETER Cerrado",
    }
    if set(source.get("source_sections", [])) != expected_sections:
        fail("seções metodológicas divergentes")
    if source.get("method_source_is_current_release_identifier") is not False:
        fail("fonte metodológica não pode identificar release")

    legend = data.get("operational_legend")
    if not isinstance(legend, dict):
        fail("operational_legend deve ser objeto")
    classes = legend.get("sensor_specific_operational_classes")
    if not isinstance(classes, list) or len(classes) != 3:
        fail("legenda deve conter três classes por satélite")
    observed_classes = {item.get("class") for item in classes if isinstance(item, dict)}
    if observed_classes != {"Alerta_cb4", "Alerta_amz1", "Alerta_cba"}:
        fail("classes operacionais divergentes")
    class_text = json.dumps(classes, ensure_ascii=False).casefold()
    for token in ("cbers-4", "amazônia-1", "cbers-4a"):
        if token not in class_text:
            fail(f"semântica de classe ausente: {token}")

    types = legend.get("documented_types")
    if not isinstance(types, list) or len(types) != 4:
        fail("quatro tipos documentados são esperados")
    observed_types = {item.get("type") for item in types if isinstance(item, dict)}
    expected_types = {
        "corte_raso",
        "alteracao_recorrente_estrutura_vegetal",
        "contextos_antropizados_ou_outros",
        "queimada_origem_antropica",
    }
    if observed_types != expected_types:
        fail("tipos operacionais divergentes")
    third = next(item for item in types if item.get("type") == "contextos_antropizados_ou_outros")
    if set(third.get("documented_examples", [])) != {
        "planted forest", "agriculture and livestock", "urban areas", "mining", "reservoir"
    }:
        fail("exemplos do terceiro tipo divergentes")
    if third.get("role_in_final_alert_semantics_resolved") is not False:
        fail("papel do terceiro tipo não está resolvido")

    if legend.get("final_class") != "Aviso":
        fail("classe final divergente")
    if legend.get("complete_operational_legend_extracted") is not True:
        fail("legenda operacional deve estar extraída")
    for key in (
        "operational_class_is_metadata_classname",
        "operational_class_is_validation_class",
        "validation_class_domain_extracted",
    ):
        if legend.get(key) is not False:
            fail(f"crosswalk prematuro: {key}")

    patterns = data.get("interpretation_patterns")
    if not isinstance(patterns, dict):
        fail("interpretation_patterns deve ser objeto")
    if len(patterns.get("documented_patterns_include", [])) < 5:
        fail("padrões de interpretação insuficientes")
    anthropogenic = patterns.get("anthropogenic_burn_pattern")
    natural = patterns.get("natural_fire_pattern")
    if not isinstance(anthropogenic, dict) or not isinstance(natural, dict):
        fail("padrões de fogo devem ser objetos")
    if anthropogenic.get("shape") != "regular" or natural.get("shape") != "irregular":
        fail("formas de fogo divergentes")
    if anthropogenic.get("texture") != "smooth" or natural.get("texture") != "rough":
        fail("texturas de fogo divergentes")
    if natural.get("complete_context_extracted") is not False:
        fail("contexto de fogo natural permanece incompleto")
    for key in ("patterns_are_deterministic_classification_rules", "patterns_replace_expert_interpretation"):
        if patterns.get(key) is not False:
            fail(f"padrões promovidos a regra determinística: {key}")

    latency = data.get("processing_latency")
    if not isinstance(latency, dict):
        fail("processing_latency deve ser objeto")
    if latency.get("typical_latency_hours_range") != [48, 72]:
        fail("latência típica divergente")
    if latency.get("pipeline_start_event") != "satellite passage and image acquisition":
        fail("evento inicial da latência divergente")
    if latency.get("pipeline_end_event") != "audited alert inserted into the database":
        fail("evento final da latência divergente")
    for key in (
        "calendar_and_team_work_variation_documented",
        "nightly_publication_of_validated_data_remains_compatible",
        "controlled_enforcement_access_context_remains_distinct",
    ):
        if latency.get(key) is not True:
            fail(f"qualificador de latência ausente: {key}")
    for key in ("latency_is_publication_sla", "latency_is_release_identifier", "latency_is_identical_for_every_alert"):
        if latency.get(key) is not False:
            fail(f"latência promovida indevidamente: {key}")

    cycle = data.get("cycle_mask_semantics")
    if not isinstance(cycle, dict):
        fail("cycle_mask_semantics deve ser objeto")
    for key in (
        "daily_alerts_form_exclusion_mask",
        "mapped_alert_areas_are_not_rechecked_in_current_observation_cycle",
        "polygons_remain_until_end_of_deter_observation_cycle",
        "deter_alerts_not_confirmed_by_prodes_may_be_analyzed_next_mapping_year",
    ):
        if cycle.get(key) is not True:
            fail(f"semântica da máscara ausente: {key}")
    for key in (
        "mask_is_permanent_land_cover_class",
        "mask_is_prodes_accumulated_deforestation_mask",
        "nonconfirmation_by_prodes_means_deter_false_positive",
    ):
        if cycle.get(key) is not False:
            fail(f"máscara operacional colapsada indevidamente: {key}")

    boundaries = data.get("comparison_and_output_boundaries")
    if not isinstance(boundaries, dict):
        fail("comparison_and_output_boundaries deve ser objeto")
    for key in (
        "daily_count_varies_with_viable_image_availability",
        "daily_count_varies_with_season",
        "operational_types_should_not_be_mapped_directly_to_metadata_classname_without_crosswalk",
    ):
        if boundaries.get(key) is not True:
            fail(f"limite operacional ausente: {key}")
    for key in (
        "operational_legend_final_class_is_precise_annual_area",
        "operational_legend_final_class_is_monthly_rate",
        "sensor_specific_class_labels_are_scientific_releases",
    ):
        if boundaries.get(key) is not False:
            fail(f"saída operacional promovida indevidamente: {key}")

    evidence = data.get("primary_evidence")
    if not isinstance(evidence, list) or len(evidence) != 2:
        fail("duas evidências primárias são esperadas")
    for item in evidence:
        if not isinstance(item, dict) or not trusted_doi(item.get("doi")):
            fail("evidência deve usar DOI HTTPS")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (
        "sensor-specific operational classes", "48–72 hour", "exclusion mask",
        "not confirmed by prodes", "expert visual interpretation", "precise annual source",
    ):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "sensor_specific_operational_classes_resolved",
        "documented_operational_types_resolved",
        "final_operational_class_resolved",
        "interpretation_patterns_documented",
        "processing_latency_range_resolved",
        "cycle_mask_semantics_resolved",
    ):
        if state.get(key) is not True:
            fail(f"fato operacional verificado ausente: {key}")
    for key in (
        "validation_class_domain_resolved",
        "crosswalk_to_metadata_classname_resolved",
        "crosswalk_to_release_schema_resolved",
        "current_release_resolved",
        "current_asset_verified",
    ):
        if state.get(key) is not False:
            fail(f"estado operacional prematuro: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 12:
        fail("regras operacionais insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "alerta_cb4", "aviso", "validation classes", "third documented type",
        "deterministic", "48–72", "nightly", "exclusion mask", "prodes accumulated",
        "false positive", "image availability", "crosswalks",
    ):
        if token not in rules_text:
            fail(f"regra operacional ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"validation_class_domain_resolved": true',
        '"crosswalk_to_metadata_classname_resolved": true',
        '"crosswalk_to_release_schema_resolved": true',
        '"current_release_resolved": true',
        '"current_asset_verified": true',
    ):
        if forbidden in serialized:
            fail(f"promoção operacional prematura: {forbidden}")

    print(
        "OK: legenda operacional, latência 48–72 h e máscara de ciclo do DETER Cerrado "
        "preservadas sem crosswalk ou promoção de release"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
