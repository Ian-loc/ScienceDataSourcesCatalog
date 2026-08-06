#!/usr/bin/env python3
"""Validate the scientific boundary and dated operational profiles for DETER Amazon."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from validate_deter_amazon_access_snapshot_guard import main as validate_access_snapshot
from validate_deter_amazon_distribution_boundary_guard import main as validate_distribution_boundary

PATH = Path("database/mappings/deter_amazon_scientific_boundary_guard_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith(("inpe.br", "gov.br"))


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000002":
        fail("gate deve permanecer vinculado à família DETER Amazônia PF000002")
    if data.get("candidate_scientific_product_id") != "PD-DETER-AMZ-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "family_product_boundary_and_dated_operational_profiles_verified_release_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    identity = data.get("scientific_identity")
    if not isinstance(identity, dict):
        fail("scientific_identity deve ser objeto")
    if identity.get("product_boundary_state") != "candidate_operational_alert_product":
        fail("fronteira de produto operacional ausente")
    for key in ("is_annual_deforestation_rate", "is_monthly_deforestation_rate", "is_complete_annual_inventory", "is_prodes_release"):
        if identity.get(key) is not False:
            fail(f"estado científico prematuro: {key}")
    collapsed = identity.get("must_not_be_collapsed_into")
    if not isinstance(collapsed, list) or len(collapsed) < 5:
        fail("fronteiras de não colapso insuficientes")
    identity_text = json.dumps(identity, ensure_ascii=False).casefold()
    for token in ("avisos", "supressão", "degradação", "fiscalização", "amazônia legal"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    classes = data.get("documented_classes")
    if not isinstance(classes, dict):
        fail("documented_classes deve ser objeto")
    if len(classes.get("level_1", [])) != 3 or len(classes.get("level_2", [])) < 7:
        fail("hierarquia de classes insuficiente")
    class_text = json.dumps(classes, ensure_ascii=False).casefold()
    for token in ("desmatamento", "degradação", "exploração madeireira", "mineração", "cicatriz de incêndio"):
        if token not in class_text:
            fail(f"classe documentada ausente: {token}")
    if classes.get("complete_release_class_domain_verified_from_bytes") is not False:
        fail("domínio integral de classes foi resolvido prematuramente")

    profiles = data.get("dated_operational_profiles")
    if not isinstance(profiles, list) or len(profiles) != 2:
        fail("dois perfis operacionais datados são obrigatórios")
    by_id = {item.get("profile_id"): item for item in profiles if isinstance(item, dict)}
    historical = by_id.get("historical_deter_b_public_profile")
    current = by_id.get("current_biomasbr_general_deter_profile")
    if not isinstance(historical, dict) or not isinstance(current, dict):
        fail("perfis histórico e atual ausentes")
    if historical.get("public_minimum_polygon_area_ha") != 6.25:
        fail("limiar público histórico deve permanecer 6,25 ha")
    if historical.get("public_release_latency_days") != 5:
        fail("latência pública histórica deve permanecer cinco dias")
    if historical.get("documented_nominal_spatial_resolutions_m") != [64, 56]:
        fail("resoluções históricas divergentes")
    if historical.get("current_release_profile") is not False:
        fail("perfil histórico não pode ser tratado como release atual")
    if current.get("minimum_mapped_alert_area_ha") != 3:
        fail("área mínima atual declarada deve permanecer 3 ha")
    if current.get("monitoring_cadence_label") != "diário":
        fail("cadência atual deve permanecer diária")
    for key in ("current_release_identifier_resolved", "product_specific_spatial_resolution_resolved", "public_release_latency_resolved"):
        if current.get(key) is not False:
            fail(f"perfil atual resolvido prematuramente: {key}")
    current_text = json.dumps(current, ensure_ascii=False).casefold()
    for token in ("amazônia-1", "cbers-4", "cbers-4a", "wfi"):
        if token not in current_text:
            fail(f"sensor atual ausente: {token}")

    temporal = data.get("temporal_and_interpretive_limitations")
    if not isinstance(temporal, dict):
        fail("limitações temporais devem ser objeto")
    if temporal.get("alert_detection_time_is_exact_event_time") is not False:
        fail("tempo de detecção não pode ser tratado como ocorrência exata")
    if temporal.get("cloud_cover_affects_detection_opportunity") is not True:
        fail("efeito de nuvens deve permanecer explícito")
    if temporal.get("alerts_may_include_processes_from_earlier_periods") is not True:
        fail("processos anteriores devem permanecer possíveis")
    if temporal.get("monthly_comparison_recommended_by_producer") is not False:
        fail("comparação mensal não pode ser recomendada")
    if temporal.get("monthly_area_is_official_deforestation_rate") is not False:
        fail("área mensal não pode virar taxa oficial")
    if temporal.get("official_annual_rate_source") != "PRODES":
        fail("fonte da taxa anual oficial deve permanecer PRODES")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve apontar para fonte oficial HTTPS")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("3 ha", "6,25 ha", "cinco dias", "taxa mensal", "prodes", "amazônia-1"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "family_identity_verified", "operational_alert_product_boundary_verified",
        "alert_vs_rate_boundary_documented", "detection_vs_occurrence_time_boundary_documented",
        "historical_and_current_operational_profiles_separated", "class_hierarchy_partially_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "current_release_resolved", "current_distribution_resolved", "direct_download_url_verified",
        "asset_bytes_inspected", "checksum_computed", "complete_schema_verified_from_bytes",
        "license_resolved_for_release", "citation_resolved_for_release",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 12:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("taxa mensal", "prodes", "data exata", "nuvens", "6,25 ha", "3 ha", "sensores históricos", "latência", "release"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    product_required = data.get("required_before_product_promotion")
    asset_required = data.get("required_before_asset_promotion")
    if not isinstance(product_required, list) or len(product_required) < 9:
        fail("requisitos de promoção do produto incompletos")
    if not isinstance(asset_required, list) or len(asset_required) < 8:
        fail("requisitos de promoção do ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true', '"current_release_resolved": true',
        '"direct_download_url_verified": true', '"asset_bytes_inspected": true',
        '"checksum_computed": true', '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    validate_distribution_boundary()
    validate_access_snapshot()
    print("OK: DETER Amazônia preserva alerta versus taxa, distribuições distintas e acesso datado sem promoção prematura")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
