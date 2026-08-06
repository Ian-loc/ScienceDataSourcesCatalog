#!/usr/bin/env python3
"""Validate reconciled DETER Cerrado access, license, citation, and negative asset state."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_access_license_citation_guard_2026.json")
CURRENT_UUID = "e6e15388-4ca9-49b9-aec9-03891339a35e"
STALE_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def trusted_url(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").casefold()
    return parsed.scheme == "https" and (
        hostname.endswith("inpe.br")
        or hostname.endswith("creativecommons.org")
        or hostname == "doi.org"
    )


def require_false(mapping: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) is not False:
            fail(f"{label} promovido prematuramente: {key}")


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
    if data.get("metadata_identifier") != CURRENT_UUID:
        fail("UUID corrente divergente")
    if data.get("superseded_citation_identifier") != STALE_UUID:
        fail("UUID histórico não preservado")
    if data.get("status") != "current_metadata_access_reconciled_program_license_documented_release_asset_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone divergente")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    citation = data.get("citation_state")
    if not isinstance(citation, dict):
        fail("citation_state deve ser objeto")
    if citation.get("published_dataset_citation_guidance_documented") is not True:
        fail("orientação de citação publicada não documentada")
    if citation.get("published_guidance_metadata_identifier") != STALE_UUID:
        fail("UUID histórico da orientação divergente")
    if citation.get("published_guidance_identifier_is_current") is not False:
        fail("UUID histórico não pode permanecer corrente")
    if citation.get("current_metadata_record_identifier") != CURRENT_UUID:
        fail("UUID do registro corrente divergente")
    if CURRENT_UUID not in str(citation.get("current_metadata_record_url", "")):
        fail("URL do registro corrente sem UUID esperado")
    if citation.get("peer_reviewed_data_availability_reference_matches_current_identifier") is not True:
        fail("referência primária do identificador corrente ausente")
    if citation.get("recommended_citation_year") != 2024:
        fail("ano da orientação de citação divergente")
    if citation.get("citation_access_date_example") != "2024-09-02":
        fail("data exemplar divergente")
    require_false(
        citation,
        ("citation_year_is_release_identifier", "citation_access_date_example_is_current_access_date", "current_release_citation_resolved"),
        "citação",
    )
    if citation.get("citation_should_be_refreshed_with_current_metadata_url_and_actual_access_date") is not True:
        fail("citação atual deve exigir URL corrente e data real")

    license_state = data.get("license_state")
    if not isinstance(license_state, dict):
        fail("license_state deve ser objeto")
    if license_state.get("program_level_license_resolved") is not True:
        fail("licença do programa deve estar resolvida")
    if license_state.get("program_level_license_identifier") != "CC-BY-SA-4.0":
        fail("identificador de licença divergente")
    if not trusted_url(license_state.get("program_level_license_url")):
        fail("URL da licença inválida")
    for key in ("source_attribution_required", "share_alike_required_for_program_level_licensed_work"):
        if license_state.get(key) is not True:
            fail(f"obrigação de licença ausente: {key}")
    require_false(
        license_state,
        (
            "current_release_license_resolved",
            "asset_specific_license_resolved",
            "redistribution_terms_for_download_package_resolved",
            "derived_product_terms_for_download_package_resolved",
        ),
        "licença do ativo",
    )

    access = data.get("public_access_channels")
    if not isinstance(access, dict):
        fail("public_access_channels deve ser objeto")
    for key in (
        "download_catalog_resolved",
        "specific_metadata_record_resolved",
        "generic_wfs_capability_documented",
        "registered_download_channel_documented",
    ):
        if access.get(key) is not True:
            fail(f"canal público ausente: {key}")
    for url_key in ("download_catalog_url", "specific_metadata_url", "specific_metadata_api_url", "generic_wfs_base_url"):
        if not trusted_url(access.get(url_key)):
            fail(f"URL inválida: {url_key}")
    for url_key in ("specific_metadata_url", "specific_metadata_api_url"):
        if CURRENT_UUID not in str(access.get(url_key, "")):
            fail(f"{url_key} sem UUID corrente")
    if access.get("specific_metadata_api_fetch_succeeded") is not False:
        fail("falha de recuperação da API deve permanecer explícita")
    if access.get("registered_download_field_example") != "areatotkm":
        fail("campo do canal cadastrado divergente")
    require_false(
        access,
        (
            "specific_wfs_workspace_resolved",
            "specific_wfs_layer_name_resolved",
            "describe_feature_type_verified",
            "direct_download_url_verified",
            "http_status_verified_for_direct_download",
            "redirect_chain_verified",
        ),
        "canal",
    )

    restricted = data.get("restricted_advance_access")
    if not isinstance(restricted, dict):
        fail("restricted_advance_access deve ser objeto")
    if restricted.get("advance_credentials_documented") is not True:
        fail("credenciais antecipadas devem estar documentadas")
    if restricted.get("restricted_advance_access_should_not_be_inherited_as_public_download_authentication") is not True:
        fail("fronteira de autenticação ausente")
    require_false(restricted, ("advance_access_is_general_public_access", "advance_access_credentials_publicly_available"), "acesso antecipado")

    asset = data.get("asset_state")
    if not isinstance(asset, dict) or not asset:
        fail("asset_state deve ser objeto não vazio")
    for key, value in asset.items():
        if value is not False:
            fail(f"estado de ativo deve permanecer negativo: {key}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 5:
        fail("evidências insuficientes")
    roles = {item.get("role") for item in evidence if isinstance(item, dict)}
    expected_roles = {
        "current_specific_metadata_record",
        "peer_reviewed_data_availability_identifier",
        "published_citation_guidance_with_superseded_identifier",
        "program_license",
        "wfs_and_advance_access_policy",
    }
    if roles != expected_roles:
        fail("papéis de evidência divergentes")
    for item in evidence:
        if not trusted_url(item.get("url")):
            fail(f"evidência com URL não confiável: {item.get('url')}")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (
        CURRENT_UUID, STALE_UUID, "areatotkm", "publish_month", "2024", "cc", "wfs", "credenciais", "fiscalização",
    ):
        if token.casefold() not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "current_metadata_identifier_reconciled",
        "published_citation_guidance_documented",
        "program_level_license_resolved",
        "download_catalog_resolved",
        "specific_metadata_record_resolved",
        "generic_wfs_capability_documented",
        "registered_download_channel_documented",
        "restricted_advance_access_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    if state.get("published_guidance_identifier_current") is not False:
        fail("UUID da orientação publicada não pode ser corrente")
    require_false(
        state,
        (
            "current_release_resolved",
            "current_release_citation_resolved",
            "current_release_license_resolved",
            "asset_specific_license_resolved",
            "specific_wfs_layer_name_resolved",
            "direct_download_url_verified",
            "asset_bytes_inspected",
            "checksum_computed",
        ),
        "estado científico-operacional",
    )

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 17:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        CURRENT_UUID, STALE_UUID, "registro de metadados", "release vigente", "data real de acesso",
        "cc-by-sa-4.0", "catálogo de downloads", "uuid geonetwork", "wfs", "areatotkm",
        "publish_month", "acesso antecipado", "content-type", "checksum",
    ):
        if token.casefold() not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"published_guidance_identifier_is_current": true',
        '"current_release_resolved": true',
        '"current_release_citation_resolved": true',
        '"current_release_license_resolved": true',
        '"asset_specific_license_resolved": true',
        '"specific_wfs_layer_name_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print(
        "OK: DETER Cerrado usa o registro de metadados corrente, preserva a referência publicada "
        "como histórica e mantém release/ativo negativos"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
