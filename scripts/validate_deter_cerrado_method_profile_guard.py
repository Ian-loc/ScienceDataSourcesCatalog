#!/usr/bin/env python3
"""Validate the 2024 DETER Cerrado method profile and its unresolved release state."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_method_profile_guard_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def trusted_url(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    host = parsed.hostname or ""
    return parsed.scheme == "https" and (
        host.endswith("doi.org") or host.endswith("inpe.br")
    )


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
    if data.get("status") != "cerrado_specific_2024_method_profile_resolved_release_and_accuracy_metrics_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    document = data.get("method_document")
    if not isinstance(document, dict):
        fail("method_document deve ser objeto")
    if document.get("title") != "Metodologia dos sistemas PRODES e DETER para o bioma Cerrado":
        fail("título metodológico divergente")
    if document.get("publisher") != "Instituto Nacional de Pesquisas Espaciais — INPE":
        fail("produtor metodológico divergente")
    if document.get("publication_year") != 2024 or document.get("updated_date") != "2024-03-28":
        fail("data ou ano metodológico divergente")
    if document.get("doi") != "10.13140/RG.2.2.24196.49281":
        fail("DOI metodológico divergente")
    if document.get("document_type") != "technical_methodology":
        fail("tipo documental divergente")
    if document.get("method_version_resolved_for_document") is not True:
        fail("edição metodológica deve estar resolvida")
    for key in ("document_is_current_release_identifier", "document_is_asset_identifier"):
        if document.get(key) is not False:
            fail(f"documento promovido indevidamente: {key}")

    purpose = data.get("scientific_purpose_and_boundaries")
    if not isinstance(purpose, dict):
        fail("scientific_purpose_and_boundaries deve ser objeto")
    outputs = purpose.get("represented_outputs")
    if not isinstance(outputs, list) or len(outputs) != 2:
        fail("saídas científicas do DETER devem conter supressão total e alteração estrutural")
    purpose_text = json.dumps(purpose, ensure_ascii=False).casefold()
    for token in ("daily operational alerts", "suppression", "alteration", "enforcement", "prodes cerrado"):
        if token not in purpose_text:
            fail(f"fronteira científica ausente: {token}")
    for key in ("is_prodes_proxy", "is_monthly_deforestation_rate", "is_annual_inventory", "alert_area_supports_precise_area_estimation"):
        if purpose.get(key) is not False:
            fail(f"uso científico prematuro: {key}")
    if purpose.get("alert_area_supports_enforcement_prioritization") is not True:
        fail("finalidade operacional ausente")

    sensor = data.get("sensor_and_detection_profile")
    if not isinstance(sensor, dict):
        fail("sensor_and_detection_profile deve ser objeto")
    satellites = sensor.get("satellites")
    if not isinstance(satellites, list) or len(satellites) != 3:
        fail("perfil deve conter exatamente três satélites")
    observed = {
        (item.get("name"), item.get("sensor"), item.get("nominal_spatial_resolution_m"))
        for item in satellites if isinstance(item, dict)
    }
    expected = {
        ("Amazônia-1", "WFI", 64),
        ("CBERS-4A", "WFI", 55),
        ("CBERS-4", "AWFI", 64),
    }
    if observed != expected:
        fail(f"perfil satélite/sensor/resolução divergente: {observed ^ expected}")
    if sensor.get("nominal_resolution_range_m") != [55, 64]:
        fail("faixa de resolução divergente")
    if sensor.get("revisit_interval_approx_days") != 5:
        fail("revisita aproximada divergente")
    if sensor.get("minimum_detectable_alert_area_ha") != 3:
        fail("área mínima detectável divergente")
    if sensor.get("minimum_detectable_alert_area_is_complete_detection_guarantee") is not False:
        fail("limiar não pode ser garantia de detecção completa")
    if sensor.get("monitoring_continuity_supported_by_daily_biome_strip_coverage") is not True:
        fail("cobertura diária do bioma deve estar documentada")

    mapping = data.get("mapping_method")
    if not isinstance(mapping, dict):
        fail("mapping_method deve ser objeto")
    if mapping.get("detection_approach") != "manual visual interpretation":
        fail("abordagem de detecção divergente")
    if mapping.get("digitization_mode") != "manual polygon digitization":
        fail("modo de digitalização divergente")
    if mapping.get("digitization_scale_denominator") != 100000:
        fail("escala de digitalização divergente")
    if mapping.get("digitization_scale_is_sensor_resolution") is not False:
        fail("escala de digitalização não pode ser resolução do sensor")
    if set(mapping.get("interpretation_elements", [])) != {"tonality", "color", "shape", "texture", "context"}:
        fail("elementos de fotointerpretação divergentes")
    if mapping.get("standardized_legend_documented") is not True:
        fail("legenda padronizada deve estar documentada")
    if mapping.get("complete_operational_legend_extracted") is not False:
        fail("legenda operacional completa ainda não foi extraída")

    temporal = data.get("temporal_semantics")
    if not isinstance(temporal, dict):
        fail("temporal_semantics deve ser objeto")
    if temporal.get("alert_assigned_date") != "acquisition date of the image used for detection":
        fail("semântica da data atribuída divergente")
    if temporal.get("assigned_date_is_exact_event_date") is not False:
        fail("data da imagem não pode ser data exata do evento")
    if temporal.get("real_event_date_may_be_unknown") is not True:
        fail("data real desconhecida deve permanecer possível")
    if temporal.get("public_update_frequency") != "daily" or temporal.get("public_update_period") != "night":
        fail("frequência/período de publicação divergente")
    if temporal.get("public_data_lag_statement") != "validated data from the previous day":
        fail("latência pública divergente")
    if temporal.get("enforcement_access_frequency") != "real time as alerts are produced":
        fail("acesso de fiscalização divergente")
    if temporal.get("enforcement_access_controlled") is not True:
        fail("acesso de fiscalização deve permanecer controlado")
    if temporal.get("monthly_consolidation_published_after_month_end") is not True:
        fail("consolidação mensal pós-mês ausente")
    if temporal.get("monthly_consolidation_is_monthly_rate") is not False:
        fail("consolidação mensal não pode ser taxa mensal")

    comparison = data.get("comparison_guidance")
    if not isinstance(comparison, dict):
        fail("comparison_guidance deve ser objeto")
    for key in ("consecutive_month_comparison_recommended", "same_month_across_years_unconditionally_recommended"):
        if comparison.get(key) is not False:
            fail(f"comparação indevida: {key}")
    if comparison.get("minimum_comparison_interval_months") != 3:
        fail("intervalo mínimo de comparação divergente")
    for key in (
        "compare_same_interval_across_years_with_caution",
        "image_availability_variability_must_be_considered",
        "cloud_and_observation_opportunity_must_be_considered",
    ):
        if comparison.get(key) is not True:
            fail(f"cautela comparativa ausente: {key}")

    validation = data.get("validation_process")
    if not isinstance(validation, dict):
        fail("validation_process deve ser objeto")
    for key in (
        "all_alert_polygons_validated",
        "validated_alerts_sent_to_ibama_daily",
        "validation_platform_documented",
    ):
        if validation.get(key) is not True:
            fail(f"processo de validação ausente: {key}")
    if validation.get("validation_frequency") != "daily":
        fail("frequência de validação divergente")
    objectives = set(validation.get("validation_objectives", []))
    expected_objectives = {
        "calculate accuracy statistics",
        "eliminate detection errors and false alerts",
        "identify system improvement opportunities",
    }
    if objectives != expected_objectives:
        fail("objetivos de validação divergentes")
    for key in ("accuracy_metrics_extracted", "accuracy_values_resolved", "confusion_matrix_resolved", "validation_class_domain_extracted"):
        if validation.get(key) is not False:
            fail(f"métrica de validação promovida prematuramente: {key}")

    timeline = data.get("timeline_semantics")
    if not isinstance(timeline, dict):
        fail("timeline_semantics deve ser objeto")
    if timeline.get("operational_start_or_creation_year_documented_elsewhere") != 2018:
        fail("ano de criação/série divergente")
    if timeline.get("method_document_launch_year") != 2019:
        fail("ano de lançamento metodológico divergente")
    if timeline.get("distribution_label_since_year") != 2018:
        fail("ano do rótulo de distribuição divergente")
    if timeline.get("years_are_same_event") is not False:
        fail("2018 e 2019 não podem ser colapsados")
    if timeline.get("current_release_year_resolved") is not False:
        fail("ano da release atual não está resolvido")
    timeline_text = str(timeline.get("timeline_interpretation", "")).casefold()
    for token in ("2018", "2019", "creation", "launch"):
        if token not in timeline_text:
            fail(f"interpretação temporal incompleta: {token}")

    divergence = data.get("documentation_context_divergence")
    if not isinstance(divergence, dict):
        fail("documentation_context_divergence deve ser objeto")
    if divergence.get("specific_metadata_image_source_statement") != "Landsat or similar":
        fail("declaração do metadado específico divergente")
    method_statement = str(divergence.get("method_document_operational_sensor_statement", ""))
    for token in ("WFI", "Amazônia-1", "CBERS-4A", "AWFI", "CBERS-4"):
        if token not in method_statement:
            fail(f"declaração metodológica incompleta: {token}")
    for key in ("statements_are_silently_equivalent", "metadata_statement_is_overwritten", "method_statement_is_current_release_proof"):
        if divergence.get(key) is not False:
            fail(f"divergência documental apagada indevidamente: {key}")

    evidence = data.get("official_and_primary_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidências primárias insuficientes")
    for item in evidence:
        if not isinstance(item, dict):
            fail("item de evidência inválido")
        url = item.get("doi") or item.get("url")
        if not trusted_url(url):
            fail(f"URL de evidência não confiável: {url}")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (
        "55–64", "five-day", "three-hectare", "1:100,000", "validation process",
        "nightly", "2019 launch", "visual interpretation", "precise quantification", "2018",
    ):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "specific_2024_method_document_resolved",
        "method_purpose_resolved",
        "sensor_resolution_and_threshold_profile_resolved_for_2024_method",
        "mapping_method_resolved_for_2024_method",
        "temporal_semantics_resolved_for_2024_method",
        "comparison_guidance_resolved_for_2024_method",
        "validation_process_documented",
        "public_and_restricted_latency_documented",
        "timeline_divergence_documented",
        "metadata_method_context_divergence_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato metodológico verificado ausente: {key}")
    for key in (
        "current_release_resolved",
        "current_release_method_profile_verified",
        "complete_operational_legend_extracted",
        "accuracy_metrics_resolved",
        "validation_class_domain_resolved",
        "current_sensor_history_verified_from_asset",
    ):
        if state.get(key) is not False:
            fail(f"estado metodológico prematuro: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 16:
        fail("regras metodológicas insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "proxy", "monthly", "image acquisition date", "three months", "55–64",
        "three hectares", "1:100,000", "nightly", "monthly consolidation",
        "accuracy", "2018", "2019", "landsat", "wfi/awfi", "current product release",
    ):
        if token not in rules_text:
            fail(f"regra metodológica ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"current_release_resolved": true',
        '"current_release_method_profile_verified": true',
        '"complete_operational_legend_extracted": true',
        '"accuracy_metrics_resolved": true',
        '"validation_class_domain_resolved": true',
        '"current_sensor_history_verified_from_asset": true',
    ):
        if forbidden in serialized:
            fail(f"promoção metodológica prematura: {forbidden}")

    print(
        "OK: método DETER Cerrado 2024 preserva sensores, limiar, interpretação visual, "
        "semântica temporal, validação e divergências documentais sem resolver release"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
