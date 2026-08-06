#!/usr/bin/env python3
"""Validate DETER Cerrado quality, validation and non-inheritance boundaries."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_quality_validation_guard_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith("inpe.br")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000003":
        fail("família deve permanecer DETER Cerrado PF000003")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "quality_framework_documented_quantitative_cerrado_validation_unresolved":
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
    for key in (
        "minimum_area_is_detection_probability",
        "minimum_area_is_completeness_guarantee",
        "alert_area_is_precise_annual_inventory",
        "exact_event_date_observed",
        "latency_is_accuracy_metric",
    ):
        if scope.get(key) is not False:
            fail(f"interpretação prematura de qualidade: {key}")

    controls = data.get("documented_quality_controls", {})
    if controls.get("interpretation_scale") != "1:100.000":
        fail("escala de interpretação divergente")
    if controls.get("nominal_spatial_resolution_m") != [55, 64]:
        fail("resolução nominal divergente")
    if controls.get("minimum_comparison_window_months") != 3:
        fail("janela comparativa mínima divergente")
    if controls.get("comparison_window_is_validation_design") is not False:
        fail("janela comparativa não pode ser tratada como validação")

    validation = data.get("quantitative_validation_state", {})
    expected_false = (
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
    )
    for key in expected_false:
        if validation.get(key) is not False:
            fail(f"métrica ou estado resolvido prematuramente: {key}")

    inheritance = data.get("non_inheritance_rules", {})
    for key in (
        "amazon_deter_validation_metrics_inherited",
        "prodes_accuracy_metrics_inherited",
        "general_deter_program_description_is_cerrado_validation",
        "methodological_controls_are_accuracy_statistics",
        "manual_interpretation_implies_ground_truth",
    ):
        if inheritance.get(key) is not False:
            fail(f"herança científica indevida: {key}")

    limitations = data.get("known_biases_and_limitations")
    if not isinstance(limitations, list) or len(limitations) < 6:
        fail("limitações insuficientes")
    limitations_text = " ".join(limitations).casefold()
    for token in ("limiar", "nuvens", "data", "prodes", "latência", "incerteza"):
        if token not in limitations_text:
            fail(f"limitação obrigatória ausente: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar fonte oficial HTTPS do INPE")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("3 ha", "bioma", "amazônia", "cerrado"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state", {})
    for key in (
        "quality_framework_documented",
        "operational_limitations_documented",
        "non_inheritance_boundary_documented",
    ):
        if state.get(key) is not True:
            fail(f"estado verificado ausente: {key}")
    for key in (
        "cerrado_specific_quantitative_accuracy_resolved",
        "current_release_validation_resolved",
        "current_release_uncertainty_resolved",
        "quality_profile_complete",
    ):
        if state.get(key) is not False:
            fail(f"perfil de qualidade concluído prematuramente: {key}")

    requirements = data.get("required_before_quality_profile_completion")
    if not isinstance(requirements, list) or len(requirements) < 8:
        fail("requisitos de completude insuficientes")
    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 8:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(rules).casefold()
    for token in ("deter amazônia", "prodes", "3 ha", "verdade de campo", "48–72", "três meses", "incerteza", "release"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    print("OK: DETER Cerrado preserva qualidade operacional, validação quantitativa não resolvida e não herança interbiomas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
