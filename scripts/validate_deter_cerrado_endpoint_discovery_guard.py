#!/usr/bin/env python3
"""Validate DETER Cerrado endpoint discovery without inventing a service or asset."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_endpoint_discovery_guard_2026.json")
CURRENT_UUID = "e6e15388-4ca9-49b9-aec9-03891339a35e"
STALE_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"
REGISTRY_COMMIT = "2f39a2e164d6a180aaf4559d93a162e2c6c56cf1"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_inpe_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith("inpe.br")


def official_terrabrasilis_github(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    host = (parsed.hostname or "").casefold()
    path = parsed.path.casefold()
    return parsed.scheme == "https" and (
        (host == "github.com" and path.startswith("/terrabrasilis/terrabrasilis_datasource"))
        or (
            host == "raw.githubusercontent.com"
            and path.startswith("/terrabrasilis/terrabrasilis_datasource/")
        )
    )


def external_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.hostname)


def require_false(mapping: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) is not False:
            fail(f"{label} promovido indevidamente: {key}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    expected_top = {
        "contract_version": "1.1.0",
        "package_id": "I1-M2A-DETER-CERRADO",
        "family_stable_id": "PF000003",
        "candidate_scientific_product_id": "PD-DETER-CER-ALERTS",
        "metadata_identifier": CURRENT_UUID,
        "superseded_citation_identifier": STALE_UUID,
        "status": "current_listing_metadata_and_official_wms_registry_inspected_specific_download_and_vector_wfs_layer_unresolved",
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
    if listing.get("metadata_identifier") != CURRENT_UUID:
        fail("UUID corrente do listing divergente")
    for key in ("listing_present", "metadata_record_resolved", "download_action_visible"):
        if listing.get(key) is not True:
            fail(f"fato do listing ausente: {key}")
    require_false(
        listing,
        (
            "direct_download_href_exposed_in_indexed_content",
            "direct_download_url_resolved",
            "displayed_update_date_is_release_identifier",
            "download_action_visibility_proves_asset_identity",
        ),
        "listing",
    )

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
    require_false(
        wfs,
        (
            "example_is_deter_cerrado_layer",
            "deter_cerrado_workspace_resolved",
            "deter_cerrado_feature_type_resolved",
            "deter_cerrado_describe_feature_type_verified",
            "deter_cerrado_get_feature_verified",
            "generic_capability_can_be_inherited_as_specific_layer",
        ),
        "WFS específico",
    )

    registry = data.get("official_qgis_wms_registry")
    if not isinstance(registry, dict):
        fail("official_qgis_wms_registry deve ser objeto")
    if not official_terrabrasilis_github(registry.get("repository_url")):
        fail("repositório oficial do plugin inválido")
    if not official_terrabrasilis_github(registry.get("registry_url")):
        fail("URL do registro WMS inválida")
    if registry.get("repository_owner") != "terrabrasilis":
        fail("owner do registro oficial divergente")
    if registry.get("repository_name") != "terrabrasilis_datasource":
        fail("repositório do registro oficial divergente")
    if registry.get("latest_registry_update_commit") != REGISTRY_COMMIT:
        fail("commit inspecionado divergente")
    if registry.get("latest_registry_update_date") != "2026-04-24":
        fail("data do registro inspecionado divergente")
    if registry.get("prodes_cerrado_workspace_observed") != "prodes-cerrado-nb":
        fail("workspace PRODES Cerrado observado divergente")
    for key in (
        "registry_file_retrieved",
        "registry_json_inspected",
        "superseded_deter_citation_uuid_present_only_as_prodes_metadata",
    ):
        if registry.get(key) is not True:
            fail(f"inspeção do registro WMS incompleta: {key}")
    require_false(
        registry,
        (
            "current_deter_cerrado_metadata_uuid_present",
            "deter_text_entry_present",
            "deter_cerrado_workspace_present",
            "deter_cerrado_layer_present",
            "registry_is_wfs_get_capabilities",
            "registry_is_complete_geoserver_catalog",
            "registry_absence_proves_layer_nonexistence",
            "prodes_cerrado_workspace_can_be_inherited_for_deter",
            "registry_resolves_current_deter_wfs_workspace",
            "registry_resolves_current_deter_wfs_feature_type",
        ),
        "registro WMS",
    )
    registry_text = json.dumps(registry, ensure_ascii=False).casefold()
    for token in ("qgis", "wms", "prodes-cerrado-nb", REGISTRY_COMMIT):
        if token.casefold() not in registry_text:
            fail(f"registro WMS incompleto: {token}")

    historical = data.get("historical_external_trace")
    if not isinstance(historical, dict):
        fail("historical_external_trace deve ser objeto")
    if historical.get("trace_present") is not True or historical.get("trace_should_not_be_promoted") is not True:
        fail("rastro histórico deve estar documentado e não promovível")
    if historical.get("trace_date_context") != "2020":
        fail("data do rastro histórico divergente")
    if historical.get("trace_service_type") != "WCS imagery":
        fail("tipo do rastro histórico divergente")
    if historical.get("trace_workspace_or_coverage_prefix") != "deter-cerrado":
        fail("prefixo histórico divergente")
    if "CBERS-4_AWFI" not in str(historical.get("trace_example", "")):
        fail("exemplo histórico incompleto")
    require_false(
        historical,
        (
            "trace_is_current_vector_wfs_evidence",
            "trace_is_official_current_documentation",
            "trace_resolves_current_workspace",
            "trace_resolves_current_feature_type",
            "trace_resolves_current_release",
        ),
        "rastro histórico",
    )

    instrumental = data.get("instrumental_state")
    if not isinstance(instrumental, dict):
        fail("instrumental_state deve ser objeto")
    for key in ("web_index_confirmed_listing_and_official_wfs_example", "official_github_registry_retrieved"):
        if instrumental.get(key) is not True:
            fail(f"fato instrumental ausente: {key}")
    require_false(
        instrumental,
        (
            "web_parser_exposed_dynamic_download_href",
            "container_dns_resolution_succeeded",
            "container_dns_failure_means_source_unavailable",
            "live_http_status_for_specific_download_verified",
            "live_get_capabilities_for_specific_cerrado_workspace_verified",
        ),
        "estado instrumental",
    )
    if "name resolution" not in str(instrumental.get("container_dns_error", "")).casefold():
        fail("erro DNS instrumental não documentado")

    anomaly = data.get("source_page_content_anomaly")
    if not isinstance(anomaly, dict):
        fail("source_page_content_anomaly deve ser objeto")
    if anomaly.get("unexpected_unrelated_external_content_observed_in_indexed_html") is not True:
        fail("anomalia de conteúdo deve estar documentada")
    require_false(
        anomaly,
        (
            "security_compromise_confirmed",
            "search_index_injection_confirmed",
            "source_page_integrity_status_resolved",
            "unexpected_external_link_followed",
            "dynamic_download_links_may_be_trusted_without_independent_validation",
        ),
        "interpretação da anomalia",
    )

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) != 4:
        fail("quatro evidências oficiais são esperadas")
    roles = {item.get("role") for item in evidence if isinstance(item, dict)}
    if roles != {
        "current_download_listing",
        "generic_wfs_documentation_and_amazon_example",
        "current_cerrado_metadata_record",
        "official_qgis_wms_registry",
    }:
        fail("papéis de evidência oficial divergentes")
    for item in evidence:
        url = item.get("url") if isinstance(item, dict) else None
        if not (official_inpe_https(url) or official_terrabrasilis_github(url)):
            fail(f"evidência oficial inválida: {url}")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (
        "2026-07-28",
        "deter-amz",
        "deter_public",
        CURRENT_UUID,
        "prodes-cerrado-nb",
        REGISTRY_COMMIT,
        "does not prove",
    ):
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
        "metadata_identifier_reconciled",
        "download_action_visible",
        "generic_wfs_documentation_verified",
        "amazon_example_scope_verified",
        "official_qgis_wms_registry_inspected",
        "deter_absent_from_official_qgis_wms_registry",
        "historical_wcs_trace_documented",
        "source_page_content_anomaly_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    require_false(
        state,
        (
            "registry_absence_interpreted_as_service_nonexistence",
            "direct_download_url_resolved",
            "specific_vector_workspace_resolved",
            "specific_vector_feature_type_resolved",
            "specific_describe_feature_type_verified",
            "specific_get_feature_verified",
            "live_http_status_verified",
            "current_release_resolved",
            "asset_identity_resolved",
            "source_page_integrity_status_resolved",
        ),
        "estado específico",
    )

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 16:
        fail("regras de descoberta insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "visible download action",
        "2026-07-28",
        CURRENT_UUID,
        STALE_UUID,
        "deter-amz",
        "prodes-cerrado-nb",
        "official qgis wms registry",
        "does not prove",
        "complete wfs getcapabilities",
        "2020 external wcs",
        "wcs imagery",
        "generic wfs",
        "dns failure",
        "unrelated external links",
        "headers",
        "promotion",
    ):
        if token.casefold() not in rules_text:
            fail(f"regra de descoberta ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"direct_download_url_resolved": true',
        '"deter_cerrado_workspace_resolved": true',
        '"deter_cerrado_feature_type_resolved": true',
        '"registry_absence_proves_layer_nonexistence": true',
        '"prodes_cerrado_workspace_can_be_inherited_for_deter": true',
        '"live_http_status_verified": true',
        '"current_release_resolved": true',
        '"asset_identity_resolved": true',
        '"security_compromise_confirmed": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print(
        "OK: listing, metadado, documentação WFS e registro WMS oficial inspecionados; "
        "endpoint, release e ativo permanecem não resolvidos sem inferência de inexistência"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
