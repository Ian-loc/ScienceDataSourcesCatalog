#!/usr/bin/env python3
"""Validate the initial scientific and operational boundary for DETER Cerrado."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_scientific_boundary_guard_2026.json")
EXPECTED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


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

    if data.get("family_stable_id") != "PF000003":
        fail("gate deve permanecer vinculado à família DETER Cerrado PF000003")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "family_product_distribution_identity_and_alert_boundary_verified_release_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    identity = data.get("scientific_identity")
    if not isinstance(identity, dict):
        fail("scientific_identity deve ser objeto")
    if identity.get("product_boundary_state") != "candidate_operational_alert_product":
        fail("fronteira operacional ausente")
    if identity.get("operational_start_year_documented") != 2018:
        fail("início operacional do DETER Cerrado deve permanecer 2018")
    for key in (
        "is_annual_deforestation_rate", "is_monthly_deforestation_rate",
        "is_complete_annual_inventory", "is_prodes_release", "is_deter_amazon_distribution",
    ):
        if identity.get(key) is not False:
            fail(f"estado científico prematuro: {key}")
    identity_text = json.dumps(identity, ensure_ascii=False).casefold()
    for token in ("avisos", "supressão", "vegetação nativa", "cerrado", "fiscalização"):
        if token not in identity_text:
            fail(f"identidade incompleta: {token}")

    distribution = data.get("distribution_identity")
    if not isinstance(distribution, dict):
        fail("distribution_identity deve ser objeto")
    if distribution.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado divergente")
    if EXPECTED_UUID not in str(distribution.get("metadata_url", "")) or not official_https(distribution.get("metadata_url")):
        fail("metadata_url oficial inválida")
    if not official_https(distribution.get("catalog_url")):
        fail("catalog_url oficial inválida")
    if distribution.get("declared_format") != "ESRI Shapefile":
        fail("formato declarado divergente")
    if distribution.get("catalog_last_updated_displayed") != "2026-07-28":
        fail("snapshot de data da interface divergente")
    for key in (
        "catalog_display_date_is_release_identifier", "metadata_identifier_is_asset_identifier",
        "direct_download_url_verified", "http_status_verified", "redirect_chain_verified",
        "asset_bytes_inspected", "checksum_computed",
    ):
        if distribution.get(key) is not False:
            fail(f"estado operacional prematuro: {key}")

    context = data.get("current_general_deter_context")
    if not isinstance(context, dict):
        fail("current_general_deter_context deve ser objeto")
    if context.get("monitoring_cadence_label") != "diário":
        fail("cadência geral atual deve permanecer diária")
    if context.get("minimum_mapped_alert_area_ha") != 3:
        fail("área mínima geral atual deve permanecer 3 ha")
    if context.get("sensor_documented") != "WFI":
        fail("sensor geral atual deve permanecer WFI")
    context_text = json.dumps(context, ensure_ascii=False).casefold()
    for token in ("amazônia-1", "cbers-4", "cbers-4a"):
        if token not in context_text:
            fail(f"satélite geral atual ausente: {token}")
    for key in (
        "cerrado_specific_method_version_resolved", "cerrado_specific_spatial_resolution_resolved",
        "cerrado_specific_public_latency_resolved", "current_release_identifier_resolved",
    ):
        if context.get(key) is not False:
            fail(f"perfil Cerrado resolvido prematuramente: {key}")

    temporal = data.get("temporal_and_interpretive_limitations")
    if not isinstance(temporal, dict):
        fail("limitações temporais devem ser objeto")
    for key in (
        "alert_detection_time_is_exact_event_time", "monthly_area_is_official_deforestation_rate",
        "alert_area_is_precise_annual_inventory", "operational_start_year_is_release_identifier",
        "catalog_update_date_is_scientific_period",
    ):
        if temporal.get(key) is not False:
            fail(f"limitação temporal violada: {key}")
    if temporal.get("official_annual_inventory_source") != "PRODES Cerrado":
        fail("inventário anual oficial deve permanecer PRODES Cerrado")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar fonte oficial HTTPS")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("2018", "3 ha", "wfi", "shapefile", "prodes", "fiscalização"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "family_identity_verified", "operational_alert_product_boundary_verified",
        "alert_vs_annual_inventory_boundary_documented", "cerrado_operational_start_year_documented",
        "distribution_catalog_presence_verified", "metadata_identifier_verified",
        "current_general_deter_context_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "cerrado_specific_method_profile_resolved", "current_release_resolved",
        "direct_download_url_verified", "asset_bytes_inspected", "checksum_computed",
        "complete_schema_verified_from_bytes", "license_resolved_for_release",
        "citation_resolved_for_current_release",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 12:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "taxa mensal", "prodes cerrado", "deter amazônia", "2018", "28/07/2026",
        "uuid de metadado", "endpoint", "incerteza", "licença", "release",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    if len(data.get("required_before_product_promotion", [])) < 9:
        fail("requisitos de promoção do produto incompletos")
    if len(data.get("required_before_asset_promotion", [])) < 8:
        fail("requisitos de promoção do ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true', '"current_release_resolved": true',
        '"direct_download_url_verified": true', '"asset_bytes_inspected": true',
        '"checksum_computed": true', '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: DETER Cerrado preserva alerta versus inventário, identidade da distribuição e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
