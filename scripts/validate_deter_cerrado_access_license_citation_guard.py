#!/usr/bin/env python3
"""Validate DETER Cerrado access, license, citation, and negative asset state."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_access_license_citation_guard_2026.json")
EXPECTED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith(("inpe.br", "creativecommons.org"))


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
    if data.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado divergente")
    if data.get("status") != "citation_program_license_and_access_channels_resolved_release_asset_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    citation = data.get("citation_state")
    if not isinstance(citation, dict):
        fail("citation_state deve ser objeto")
    if citation.get("recommended_dataset_citation_resolved") is not True:
        fail("citação recomendada deve estar resolvida")
    if citation.get("recommended_citation_year") != 2024:
        fail("ano da citação recomendada divergente")
    if citation.get("citation_access_date_example") != "2024-09-02":
        fail("data exemplar divergente")
    citation_text = str(citation.get("recommended_dataset_citation", ""))
    for token in ("INSTITUTO NACIONAL DE PESQUISAS ESPACIAIS", "Bioma Cerrado", "desde 2018", EXPECTED_UUID):
        if token not in citation_text:
            fail(f"citação específica incompleta: {token}")
    for key in (
        "citation_year_is_release_identifier",
        "citation_access_date_example_is_current_access_date",
        "current_release_citation_resolved",
    ):
        if citation.get(key) is not False:
            fail(f"citação promovida prematuramente: {key}")
    if citation.get("citation_should_be_refreshed_with_actual_access_date") is not True:
        fail("citação futura deve exigir data real de acesso")

    license_state = data.get("license_state")
    if not isinstance(license_state, dict):
        fail("license_state deve ser objeto")
    if license_state.get("program_level_license_resolved") is not True:
        fail("licença do programa deve estar resolvida")
    if license_state.get("program_level_license_identifier") != "CC-BY-SA-4.0":
        fail("identificador de licença divergente")
    if not official_https(license_state.get("program_level_license_url")):
        fail("URL da licença inválida")
    for key in ("source_attribution_required", "share_alike_required_for_program_level_licensed_work"):
        if license_state.get(key) is not True:
            fail(f"obrigação de licença ausente: {key}")
    for key in (
        "current_release_license_resolved",
        "asset_specific_license_resolved",
        "redistribution_terms_for_download_package_resolved",
        "derived_product_terms_for_download_package_resolved",
    ):
        if license_state.get(key) is not False:
            fail(f"licença do ativo promovida prematuramente: {key}")

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
    for url_key in ("download_catalog_url", "specific_metadata_url", "generic_wfs_base_url"):
        if not official_https(access.get(url_key)):
            fail(f"URL oficial inválida: {url_key}")
    if EXPECTED_UUID not in str(access.get("specific_metadata_url", "")):
        fail("URL específica sem UUID esperado")
    if access.get("registered_download_field_example") != "areatotkm":
        fail("campo de canal cadastrado divergente")
    for key in (
        "specific_wfs_workspace_resolved",
        "specific_wfs_layer_name_resolved",
        "describe_feature_type_verified",
        "direct_download_url_verified",
        "http_status_verified_for_direct_download",
        "redirect_chain_verified",
    ):
        if access.get(key) is not False:
            fail(f"canal promovido prematuramente: {key}")

    restricted = data.get("restricted_advance_access")
    if not isinstance(restricted, dict):
        fail("restricted_advance_access deve ser objeto")
    if restricted.get("advance_credentials_documented") is not True:
        fail("credenciais antecipadas devem estar documentadas")
    if restricted.get("restricted_advance_access_should_not_be_inherited_as_public_download_authentication") is not True:
        fail("fronteira de autenticação ausente")
    for key in ("advance_access_is_general_public_access", "advance_access_credentials_publicly_available"):
        if restricted.get(key) is not False:
            fail(f"acesso antecipado generalizado indevidamente: {key}")
    restricted_text = json.dumps(restricted, ensure_ascii=False).casefold()
    for token in ("antecipado", "controle", "fiscalização"):
        if token not in restricted_text:
            fail(f"escopo restrito incompleto: {token}")

    asset = data.get("asset_state")
    if not isinstance(asset, dict):
        fail("asset_state deve ser objeto")
    for key, value in asset.items():
        if value is not False:
            fail(f"estado de ativo deve permanecer negativo: {key}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (
        "citação recomendada", "2024", "cc", "atribuição-compartilhaigual",
        "wfs", "credenciais", "fiscalização", "areatotkm", "publish_month",
    ):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "recommended_dataset_citation_resolved",
        "program_level_license_resolved",
        "download_catalog_resolved",
        "specific_metadata_record_resolved",
        "generic_wfs_capability_documented",
        "registered_download_channel_documented",
        "restricted_advance_access_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "current_release_resolved",
        "current_release_citation_resolved",
        "current_release_license_resolved",
        "asset_specific_license_resolved",
        "specific_wfs_layer_name_resolved",
        "direct_download_url_verified",
        "asset_bytes_inspected",
        "checksum_computed",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 13:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "2024", "data real de acesso", "cc-by-sa-4.0", "release vigente",
        "catálogo de downloads", "uuid geonetwork", "wfs", "areatotkm",
        "publish_month", "acesso antecipado", "content-type", "checksum",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
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
        "OK: DETER Cerrado preserva citação específica, licença no nível do programa, "
        "canais de acesso e estado negativo de release/ativo"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
