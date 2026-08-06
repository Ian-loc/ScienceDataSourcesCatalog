#!/usr/bin/env python3
"""Validate negative endpoint discovery and source-page anomaly handling for DETER Cerrado."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_endpoint_discovery_guard_2026.json")
EXPECTED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_inpe_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith("inpe.br")


def external_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.hostname)


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    expected_top = {
        "contract_version": "1.0.0",
        "package_id": "I1-M2A-DETER-CERRADO",
        "family_stable_id": "PF000003",
        "candidate_scientific_product_id": "PD-DETER-CER-ALERTS",
        "metadata_identifier": EXPECTED_UUID,
        "status": "current_listing_verified_specific_download_href_and_vector_wfs_layer_not_safely_resolved",
        "timezone": "America/Sao_Paulo",
        "promotion_authorized": False,
    }
    for key, value in expected_top.items():
        if data.get(key) != value:
            fail(f"campo superior divergente: {key}")

    listing = data.get("current_download_listing")
    if not isinstance(listing, dict):
        fail("current_download_listing deve ser objeto")
    if not official_inpe_https(listing.get("official_page_url")):
        fail("página oficial de downloads inválida")
    if listing.get("section_label") != "Bioma Cerrado - DETER (Avisos)":
        fail("seção de download divergente")
    if listing.get("item_label") != "Avisos de supressão da vegetação nativa - Shapefile (desde 2018)":
        fail("item de download divergente")
    if listing.get("displayed_last_updated") != "2026-07-28":
        fail("data exibida divergente")
    if listing.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID do listing divergente")
    for key in ("listing_present", "metadata_record_resolved", "download_action_visible"):
        if listing.get(key) is not True:
            fail(f"fato do listing ausente: {key}")
    for key in (
        "direct_download_href_exposed_in_indexed_content",
        "direct_download_url_resolved",
        "displayed_update_date_is_release_identifier",
        "download_action_visibility_proves_asset_identity",
    ):
        if listing.get(key) is not False:
            fail(f"listing promovido indevidamente: {key}")

    wfs = data.get("official_wfs_documentation")
    if not isinstance(wfs, dict):
        fail("official_wfs_documentation deve ser objeto")
    if wfs.get("generic_wfs_capability_documented") is not True:
        fail("capacidade WFS genérica deve estar documentada")
    if not official_inpe_https(wfs.get("generic_wfs_base_url")):
        fail("URL WFS genérica inválida")
    if wfs.get("documented_example_workspace") != "deter-amz":
        fail("workspace de exemplo divergente")
    if wfs.get("documented_example_feature_type") != "deter_public":
        fail("feature type de exemplo divergente")
    if wfs.get("example_scope") != "DETER Amazônia":
        fail("escopo do exemplo divergente")
    for key in (
        "example_is_deter_cerrado_layer",
        "deter_cerrado_workspace_resolved",
        "deter_cerrado_feature_type_resolved",
        "deter_cerrado_describe_feature_type_verified",
        "deter_cerrado_get_feature_verified",
        "generic_capability_can_be_inherited_as_specific_layer",
    ):
        if wfs.get(key) is not False:
            fail(f"WFS específico promovido indevidamente: {key}")

    historical = data.get("historical_external_trace")
    if not isinstance(historical, dict):
        fail("historical_external_trace deve ser objeto")
    if historical.get("trace_present") is not True:
        fail("rastro histórico deve estar documentado")
    if historical.get("trace_date_context") != "2020":
        fail("data do rastro histórico divergente")
    if historical.get("trace_service_type") != "WCS imagery":
        fail("tipo do rastro histórico divergente")
    if historical.get("trace_workspace_or_coverage_prefix") != "deter-cerrado":
        fail("prefixo histórico divergente")
    if "CBERS-4_AWFI" not in str(historical.get("trace_example", "")):
        fail("exemplo histórico incompleto")
    if historical.get("trace_should_not_be_promoted") is not True:
        fail("rastro histórico deve permanecer não promovível")
    for key in (
        "trace_is_current_vector_wfs_evidence",
        "trace_is_official_current_documentation",
        "trace_resolves_current_workspace",
        "trace_resolves_current_feature_type",
        "trace_resolves_current_release",
    ):
        if historical.get(key) is not False:
            fail(f"rastro histórico promovido indevidamente: {key}")

    instrumental = data.get("instrumental_state")
    if not isinstance(instrumental, dict):
        fail("instrumental_state deve ser objeto")
    if instrumental.get("web_index_confirmed_listing_and_official_wfs_example") is not True:
        fail("resultado do índice web ausente")
    for key in (
        "web_parser_exposed_dynamic_download_href",
        "container_dns_resolution_succeeded",
        "container_dns_failure_means_source_unavailable",
        "live_http_status_for_specific_download_verified",
        "live_get_capabilities_for_specific_cerrado_workspace_verified",
    ):
        if instrumental.get(key) is not False:
            fail(f"estado instrumental incorreto: {key}")
    if "name resolution" not in str(instrumental.get("container_dns_error", "")).casefold():
        fail("erro DNS instrumental não documentado")

    anomaly = data.get("source_page_content_anomaly")
    if not isinstance(anomaly, dict):
        fail("source_page_content_anomaly deve ser objeto")
    if anomaly.get("unexpected_unrelated_external_content_observed_in_indexed_html") is not True:
        fail("anomalia de conteúdo deve estar documentada")
    if anomaly.get("unexpected_external_link_followed") is not False:
        fail("link externo inesperado não deve ter sido seguido")
    if anomaly.get("dynamic_download_links_may_be_trusted_without_independent_validation") is not False:
        fail("links dinâmicos não podem ser promovidos sem validação")
    for key in (
        "security_compromise_confirmed",
        "search_index_injection_confirmed",
        "source_page_integrity_status_resolved",
    ):
        if anomaly.get(key) is not False:
            fail(f"interpretação de segurança prematura: {key}")
    anomaly_text = json.dumps(anomaly, ensure_ascii=False).casefold()
    for token in ("pharmaceutical", "independent", "headers", "bytes"):
        if token not in anomaly_text:
            fail(f"tratamento da anomalia incompleto: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) != 3:
        fail("três evidências oficiais são esperadas")
    for item in evidence:
        if not isinstance(item, dict) or not official_inpe_https(item.get("url")):
            fail("evidência oficial deve usar URL INPE HTTPS")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("2026-07-28", "deter-amz", "deter_public", "getcapabilities", EXPECTED_UUID):
        if token.casefold() not in evidence_text:
            fail(f"cobertura de evidência oficial ausente: {token}")

    external = data.get("external_context")
    if not isinstance(external, list) or len(external) != 1:
        fail("um contexto externo histórico é esperado")
    item = external[0]
    if not isinstance(item, dict) or not external_https(item.get("url")):
        fail("contexto externo inválido")
    if item.get("authority_for_current_vector_service") is not False:
        fail("contexto externo não pode autorizar serviço atual")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "current_download_listing_verified",
        "metadata_record_verified",
        "download_action_visible",
        "generic_wfs_documentation_verified",
        "amazon_example_scope_verified",
        "historical_wcs_trace_documented",
        "source_page_content_anomaly_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "direct_download_url_resolved",
        "specific_vector_workspace_resolved",
        "specific_vector_feature_type_resolved",
        "specific_describe_feature_type_verified",
        "specific_get_feature_verified",
        "live_http_status_verified",
        "current_release_resolved",
        "asset_identity_resolved",
        "source_page_integrity_status_resolved",
    ):
        if state.get(key) is not False:
            fail(f"estado específico promovido indevidamente: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 12:
        fail("regras de descoberta insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "visible download action", "2026-07-28", "deter-amz", "2020 external wcs",
        "wcs imagery", "generic wfs", "dns failure", "unrelated external links",
        "compromise", "headers", "getcapabilities", "promotion",
    ):
        if token not in rules_text:
            fail(f"regra de descoberta ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"direct_download_url_resolved": true',
        '"deter_cerrado_workspace_resolved": true',
        '"deter_cerrado_feature_type_resolved": true',
        '"live_http_status_verified": true',
        '"current_release_resolved": true',
        '"asset_identity_resolved": true',
        '"security_compromise_confirmed": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print(
        "OK: listing atual, exemplo WFS genérico, rastro WCS histórico e anomalia de conteúdo "
        "preservados sem inventar endpoint, ativo ou comprometimento"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
