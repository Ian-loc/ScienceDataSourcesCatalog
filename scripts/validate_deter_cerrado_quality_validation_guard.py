#!/usr/bin/env python3
"""Validate DETER Cerrado quality evidence and accuracy non-equivalence boundaries."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_quality_validation_guard_2026.json")
DOI = "10.1080/25726838.2023.2265242"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_inpe_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith("inpe.br")


def peer_reviewed_url(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").casefold() == "doi.org" and DOI in parsed.path


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
    if data.get("family_stable_id") != "PF000003":
        fail("família deve permanecer DETER Cerrado PF000003")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "quantitative_operational_proximity_evidence_documented_accuracy_and_release_validation_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    scope = data.get("quality_scope", {})
    if scope.get("minimum_mapped_alert_area_ha") != 3:
        fail("limiar geral atual deve permanecer 3 ha")
    if scope.get("typical_publication_latency_hours") != [48, 72]:
        fail("latência típica deve permanecer 48–72 h")
    require_false(
        scope,
        (
            "minimum_area_is_detection_probability",
            "minimum_area_is_completeness_guarantee",
            "alert_area_is_precise_annual_inventory",
            "exact_event_date_observed",
            "latency_is_accuracy_metric",
        ),
        "interpretação de qualidade",
    )

    controls = data.get("documented_quality_controls", {})
    if controls.get("interpretation_scale") != "1:100.000":
        fail("escala de interpretação divergente")
    if controls.get("nominal_spatial_resolution_m") != [55, 64]:
        fail("resolução nominal divergente")
    if controls.get("minimum_comparison_window_months") != 3:
        fail("janela comparativa mínima divergente")
    if controls.get("comparison_window_is_validation_design") is not False:
        fail("janela comparativa não pode ser tratada como validação")

    operational = data.get("peer_reviewed_operational_evidence")
    if not isinstance(operational, dict):
        fail("peer_reviewed_operational_evidence deve ser objeto")
    if operational.get("evidence_found") is not True:
        fail("evidência operacional quantitativa deve estar registrada")
    if operational.get("study_doi") != DOI:
        fail("DOI do estudo divergente")
    if operational.get("study_year") != 2023:
        fail("ano do estudo divergente")
    if operational.get("study_system_scope") != "DETER Cerrado":
        fail("escopo do estudo divergente")
    if operational.get("reported_proximity_percentage") != 80:
        fail("percentual de proximidade divergente")
    if operational.get("reported_buffer_radius_km") != 10:
        fail("raio do buffer divergente")
    if operational.get("supports_operational_surveillance_capability") is not True:
        fail("utilidade operacional deve estar documentada")
    if operational.get("prodes_is_reference_inventory_not_ground_truth_for_all_alert_semantics") is not True:
        fail("papel do PRODES deve permanecer limitado")
    if operational.get("buffer_proximity_is_not_exact_coincidence") is not True:
        fail("proximidade não pode virar coincidência exata")
    require_false(
        operational,
        (
            "is_confusion_matrix",
            "is_precision",
            "is_recall",
            "is_sensitivity",
            "is_specificity",
            "is_omission_error",
            "is_commission_error",
            "is_area_adjusted_accuracy",
            "is_geometry_uncertainty",
            "is_current_release_validation",
        ),
        "resultado de proximidade",
    )
    operational_text = json.dumps(operational, ensure_ascii=False).casefold()
    for token in (">1 ha", "<10 ha", "80", "10", "prodes cerrado", "proximidade"):
        if token not in operational_text:
            fail(f"evidência operacional incompleta: {token}")

    validation = data.get("quantitative_validation_state", {})
    if validation.get("cerrado_specific_operational_proximity_evidence_found") is not True:
        fail("evidência operacional não consolidada")
    require_false(
        validation,
        (
            "cerrado_specific_accuracy_assessment_found",
            "cerrado_specific_confusion_matrix_found",
            "cerrado_specific_precision_found",
            "cerrado_specific_recall_found",
            "cerrado_specific_omission_error_found",
            "cerrado_specific_commission_error_found",
            "cerrado_specific_area_adjusted_accuracy_found",
            "current_release_validation_sample_resolved",
            "current_release_validation_protocol_resolved",
            "uncertainty_quantified_for_alert_geometry",
            "absence_means_no_uncertainty",
        ),
        "métrica de acurácia",
    )

    inheritance = data.get("non_inheritance_rules", {})
    require_false(
        inheritance,
        (
            "amazon_deter_validation_metrics_inherited",
            "prodes_accuracy_metrics_inherited",
            "prodes_cerrado_accuracy_assessment_reclassified_as_deter_accuracy",
            "general_deter_program_description_is_cerrado_validation",
            "methodological_controls_are_accuracy_statistics",
            "manual_interpretation_implies_ground_truth",
            "ten_km_buffer_result_is_precision_or_recall",
        ),
        "herança científica",
    )

    limitations = data.get("known_biases_and_limitations")
    if not isinstance(limitations, list) or len(limitations) < 8:
        fail("limitações insuficientes")
    limitations_text = " ".join(limitations).casefold()
    for token in ("limiar", "nuvens", "data", "prodes", "latência", "10 km", "80%", "incerteza"):
        if token not in limitations_text:
            fail(f"limitação obrigatória ausente: {token}")

    official = data.get("official_evidence")
    if not isinstance(official, list) or len(official) < 3:
        fail("evidências oficiais insuficientes")
    for item in official:
        if not isinstance(item, dict) or not official_inpe_https(item.get("url")):
            fail("toda evidência oficial deve usar fonte HTTPS do INPE")
    official_text = json.dumps(official, ensure_ascii=False).casefold()
    for token in ("3 ha", "bioma", "amazônia", "cerrado"):
        if token not in official_text:
            fail(f"cobertura de evidência oficial ausente: {token}")

    peer = data.get("peer_reviewed_evidence")
    if not isinstance(peer, list) or len(peer) != 1:
        fail("uma evidência revisada por pares é obrigatória")
    item = peer[0]
    if not isinstance(item, dict) or not peer_reviewed_url(item.get("url")):
        fail("evidência revisada por pares deve usar o DOI esperado")
    peer_text = json.dumps(peer, ensure_ascii=False).casefold()
    for token in ("80%", "10 km", ">1 ha", "<10 ha", "fiscalização", "e6e15388"):
        if token not in peer_text:
            fail(f"cobertura de evidência revisada por pares ausente: {token}")

    state = data.get("verified_state", {})
    for key in (
        "quality_framework_documented",
        "operational_limitations_documented",
        "non_inheritance_boundary_documented",
        "cerrado_specific_operational_proximity_evidence_resolved",
    ):
        if state.get(key) is not True:
            fail(f"estado verificado ausente: {key}")
    require_false(
        state,
        (
            "cerrado_specific_quantitative_accuracy_resolved",
            "current_release_validation_resolved",
            "current_release_uncertainty_resolved",
            "quality_profile_complete",
        ),
        "perfil de qualidade",
    )

    requirements = data.get("required_before_quality_profile_completion")
    if not isinstance(requirements, list) or len(requirements) < 8:
        fail("requisitos de completude insuficientes")
    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 11:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(rules).casefold()
    for token in (
        "80%", "10 km", "proximidade", "precisão", "revocação", "prodes", "deter amazônia",
        "3 ha", "verdade de campo", "48–72", "três meses", "incerteza", "release",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"cerrado_specific_quantitative_accuracy_resolved": true',
        '"current_release_validation_resolved": true',
        '"current_release_uncertainty_resolved": true',
        '"quality_profile_complete": true',
        '"is_precision": true',
        '"is_recall": true',
        '"is_current_release_validation": true',
        '"ten_km_buffer_result_is_precision_or_recall": true',
    ):
        if forbidden in serialized:
            fail(f"promoção indevida detectada: {forbidden}")

    print(
        "OK: evidência quantitativa de proximidade operacional do DETER Cerrado documentada; "
        "acurácia, incerteza e validação da release permanecem não resolvidas"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
