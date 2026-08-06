#!/usr/bin/env python3
"""Validate DETER Cerrado operational legend, validation classes, latency and cycle mask."""
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


def require_false(mapping: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) is not False:
            fail(f"{label} resolvido prematuramente: {key}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("contract_version") != "1.1.0":
        fail("versão do contrato inesperada")
    if data.get("package_id") != "I1-M2A-DETER-CERRADO":
        fail("pacote inesperado")
    if data.get("family_stable_id") != "PF000003":
        fail("família inesperada")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "operational_legend_validation_domain_latency_and_cycle_mask_resolved_release_crosswalk_unresolved":
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
        "Figura 15 — Interface da plataforma de validação dos Avisos",
        "Figura 16 — Visualização da acurácia dos polígonos validados",
        "Figura 17 — Classes de validação do Sistema DETER",
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
    if {item.get("class") for item in classes if isinstance(item, dict)} != {"Alerta_cb4", "Alerta_amz1", "Alerta_cba"}:
        fail("classes operacionais divergentes")
    class_text = json.dumps(classes, ensure_ascii=False).casefold()
    for token in ("cbers-4", "amazônia-1", "cbers-4a"):
        if token not in class_text:
            fail(f"semântica de classe ausente: {token}")

    types = legend.get("documented_types")
    if not isinstance(types, list) or len(types) != 4:
        fail("quatro tipos documentados são esperados")
    if {item.get("type") for item in types if isinstance(item, dict)} != {
        "corte_raso",
        "alteracao_recorrente_estrutura_vegetal",
        "contextos_antropizados_ou_outros",
        "queimada_origem_antropica",
    }:
        fail("tipos operacionais divergentes")
    third = next(item for item in types if item.get("type") == "contextos_antropizados_ou_outros")
    if set(third.get("documented_examples", [])) != {
        "planted forest", "agriculture and livestock", "urban areas", "mining", "reservoir"
    }:
        fail("exemplos do terceiro tipo divergentes")
    for key in ("listed_in_operational_types_column", "examples_are_not_native_vegetation_suppression_classes", "must_not_map_to_desmatamento_cr"):
        if third.get(key) is not True:
            fail(f"fronteira do terceiro tipo ausente: {key}")
    if third.get("role_as_positive_final_alert_semantics_resolved") is not False:
        fail("papel positivo do terceiro tipo permanece não resolvido")

    if legend.get("final_class") != "Aviso":
        fail("classe final divergente")
    for key in ("complete_operational_legend_extracted", "validation_class_domain_extracted"):
        if legend.get(key) is not True:
            fail(f"extração da legenda incompleta: {key}")
    require_false(legend, ("operational_class_is_metadata_classname", "operational_class_is_validation_class"), "crosswalk operacional")

    validation = data.get("validation_workflow")
    if not isinstance(validation, dict):
        fail("validation_workflow deve ser objeto")
    if validation.get("performed_by_specialists") is not True:
        fail("validação por especialistas deve estar registrada")
    sources = validation.get("comparison_sources")
    if not isinstance(sources, list) or len(sources) != 4:
        fail("quatro fontes de comparação são esperadas")
    sources_text = " ".join(sources).casefold()
    for token in ("base image", "prodes cerrado", "planet", "modis ndvi"):
        if token not in sources_text:
            fail(f"fonte de validação ausente: {token}")

    vclasses = validation.get("validation_classes")
    if not isinstance(vclasses, list) or len(vclasses) != 5:
        fail("cinco classes de validação são obrigatórias")
    expected_validation_classes = {"Alerta", "Falso Positivo", "Resíduo", "Não Observado", "Sem condições de avaliação"}
    if {item.get("class") for item in vclasses if isinstance(item, dict)} != expected_validation_classes:
        fail("domínio das classes de validação divergente")
    validation_text = json.dumps(vclasses, ensure_ascii=False).casefold()
    for token in (
        "corte raso", "alteration", "without anthropogenic disturbance", "previous years",
        "cloud", "cloud shadow", "seasonality", "suitable imagery",
    ):
        if token not in validation_text:
            fail(f"semântica de validação ausente: {token}")
    alerta = next(item for item in vclasses if item.get("class") == "Alerta")
    if alerta.get("is_same_as_final_operational_aviso") is not False or alerta.get("automatic_crosswalk_to_desmatamento_cr") is not False:
        fail("Alerta de validação não pode ser colapsado com Aviso ou DESMATAMENTO_CR")
    false_positive = next(item for item in vclasses if item.get("class") == "Falso Positivo")
    if false_positive.get("is_accuracy_statistic") is not False:
        fail("classe Falso Positivo não é estatística agregada de acurácia")
    residue = next(item for item in vclasses if item.get("class") == "Resíduo")
    require_false(residue, ("is_prodes_annual_residual_product", "is_release_identifier"), "classe Resíduo")
    not_observed = next(item for item in vclasses if item.get("class") == "Não Observado")
    if not_observed.get("is_missing_observation_state") is not True:
        fail("Não Observado deve permanecer estado de observação")
    no_conditions = next(item for item in vclasses if item.get("class") == "Sem condições de avaliação")
    if no_conditions.get("complete_source_definition_extracted") is not False:
        fail("definição integral de Sem condições permanece incompleta")
    if validation.get("validation_class_domain_complete_for_method_edition") is not True:
        fail("domínio metodológico deve estar resolvido")
    require_false(
        validation,
        (
            "validation_class_domain_verified_in_current_release_schema",
            "validation_class_values_verified_in_asset_bytes",
            "confusion_matrix_reconstructed",
            "class_counts_resolved",
            "accuracy_statistics_resolved",
        ),
        "validação quantitativa/release",
    )

    crosswalk = data.get("crosswalk_boundaries")
    if not isinstance(crosswalk, dict):
        fail("crosswalk_boundaries deve ser objeto")
    require_false(
        crosswalk,
        (
            "operational_aviso_to_validation_alerta_resolved",
            "validation_alerta_to_metadata_desmatamento_cr_resolved",
            "validation_residuo_to_prodes_residual_product_resolved",
            "validation_classes_are_public_distribution_classname_values",
            "method_edition_classes_are_current_release_schema",
        ),
        "crosswalk",
    )
    crosswalk_text = json.dumps(crosswalk, ensure_ascii=False).casefold()
    for token in ("operational", "validation", "metadata", "workflow stages", "semantic domains"):
        if token not in crosswalk_text:
            fail(f"justificativa de crosswalk ausente: {token}")

    patterns = data.get("interpretation_patterns")
    if not isinstance(patterns, dict) or len(patterns.get("documented_patterns_include", [])) < 5:
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
    require_false(patterns, ("patterns_are_deterministic_classification_rules", "patterns_replace_expert_interpretation"), "padrões")

    latency = data.get("processing_latency")
    if not isinstance(latency, dict) or latency.get("typical_latency_hours_range") != [48, 72]:
        fail("latência típica divergente")
    if latency.get("pipeline_start_event") != "satellite passage and image acquisition":
        fail("evento inicial da latência divergente")
    if latency.get("pipeline_end_event") != "audited alert inserted into the database":
        fail("evento final da latência divergente")
    for key in ("calendar_and_team_work_variation_documented", "nightly_publication_of_validated_data_remains_compatible", "controlled_enforcement_access_context_remains_distinct"):
        if latency.get(key) is not True:
            fail(f"qualificador de latência ausente: {key}")
    require_false(latency, ("latency_is_publication_sla", "latency_is_release_identifier", "latency_is_identical_for_every_alert"), "latência")

    cycle = data.get("cycle_mask_semantics")
    if not isinstance(cycle, dict):
        fail("cycle_mask_semantics deve ser objeto")
    for key in ("daily_alerts_form_exclusion_mask", "mapped_alert_areas_are_not_rechecked_in_current_observation_cycle", "polygons_remain_until_end_of_deter_observation_cycle", "deter_alerts_not_confirmed_by_prodes_may_be_analyzed_next_mapping_year"):
        if cycle.get(key) is not True:
            fail(f"semântica da máscara ausente: {key}")
    require_false(cycle, ("mask_is_permanent_land_cover_class", "mask_is_prodes_accumulated_deforestation_mask", "nonconfirmation_by_prodes_means_deter_false_positive"), "máscara operacional")

    boundaries = data.get("comparison_and_output_boundaries")
    if not isinstance(boundaries, dict):
        fail("comparison_and_output_boundaries deve ser objeto")
    for key in ("daily_count_varies_with_viable_image_availability", "daily_count_varies_with_season", "operational_types_should_not_be_mapped_directly_to_metadata_classname_without_crosswalk"):
        if boundaries.get(key) is not True:
            fail(f"limite operacional ausente: {key}")
    require_false(boundaries, ("operational_legend_final_class_is_precise_annual_area", "operational_legend_final_class_is_monthly_rate", "sensor_specific_class_labels_are_scientific_releases"), "saída operacional")

    evidence = data.get("primary_evidence")
    if not isinstance(evidence, list) or len(evidence) != 2:
        fail("duas evidências primárias são esperadas")
    for item in evidence:
        if not isinstance(item, dict) or not trusted_doi(item.get("doi")):
            fail("evidência deve usar DOI HTTPS")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("five validation classes", "48–72 hour", "exclusion mask", "not confirmed by prodes", "expert visual interpretation", "precise annual source"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "sensor_specific_operational_classes_resolved",
        "documented_operational_types_resolved",
        "third_type_table_placement_resolved",
        "final_operational_class_resolved",
        "validation_class_domain_resolved_for_method_edition",
        "interpretation_patterns_documented",
        "processing_latency_range_resolved",
        "cycle_mask_semantics_resolved",
    ):
        if state.get(key) is not True:
            fail(f"fato operacional verificado ausente: {key}")
    require_false(
        state,
        (
            "third_type_positive_alert_semantics_resolved",
            "validation_class_domain_resolved_for_current_release",
            "crosswalk_to_metadata_classname_resolved",
            "crosswalk_to_release_schema_resolved",
            "current_release_resolved",
            "current_asset_verified",
        ),
        "estado operacional/release",
    )

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 16:
        fail("regras operacionais insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "alerta_cb4", "aviso", "falso positivo", "resíduo", "não observado", "sem condições",
        "prodes annual-residual", "desmatamento_cr", "third documented type", "planted forest",
        "deterministic", "48–72", "nightly", "exclusion mask", "prodes accumulated",
        "false positive", "image availability", "crosswalks",
    ):
        if token not in rules_text:
            fail(f"regra operacional ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"third_type_positive_alert_semantics_resolved": true',
        '"validation_class_domain_resolved_for_current_release": true',
        '"crosswalk_to_metadata_classname_resolved": true',
        '"crosswalk_to_release_schema_resolved": true',
        '"current_release_resolved": true',
        '"current_asset_verified": true',
        '"is_prodes_annual_residual_product": true',
    ):
        if forbidden in serialized:
            fail(f"promoção operacional prematura: {forbidden}")

    print(
        "OK: legenda operacional, cinco classes de validação, latência e máscara de ciclo "
        "resolvidas no método sem crosswalk ou promoção de release"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
