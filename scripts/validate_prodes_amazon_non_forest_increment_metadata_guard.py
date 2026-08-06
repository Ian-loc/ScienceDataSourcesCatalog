#!/usr/bin/env python3
"""Validate the scientific and operational guard for PRODES Amazon non-forest suppression increments."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_non_forest_increment_metadata_guard_2026.json")
EXPECTED_UUID = "a8208a12-679b-432a-8a47-fc42d2279f9a"
EXPECTED_IBI = "sid.inpe.br/mtc-m21d/2022/08.25.11.46-NTC"


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

    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado à família PF000001")
    if data.get("target_id") != "PRODES-ASSET-NON-FOREST-INCREMENT-SHP":
        fail("alvo operacional inesperado")
    if data.get("candidate_scientific_product_id") != "PD-PRODES-AMZ-NON-FOREST-SUPPRESSION-INCREMENTS":
        fail("candidato a produto inesperado")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "metadata_identity_temporal_profile_and_base_method_verified_endpoint_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")
    if data.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado foi alterado")
    if not official_https(data.get("metadata_url")) or EXPECTED_UUID not in data["metadata_url"]:
        fail("metadata_url oficial inválida")
    if not official_https(data.get("catalog_url")):
        fail("catalog_url deve apontar para fonte oficial do INPE")

    identity = data.get("scientific_identity")
    if not isinstance(identity, dict):
        fail("scientific_identity deve ser objeto")
    if identity.get("product_boundary_state") != "candidate_distinct_scientific_product":
        fail("fronteira científica deve permanecer explícita")
    if identity.get("must_not_inherit_identity_from") != "PD-PRODES-AMZ-ANNUAL-MAP":
        fail("proibição de herança científica ausente")
    identity_text = " ".join(str(value) for value in identity.values()).casefold()
    for token in ("não florestais", "bioma amazônia", "adaptações metodológicas"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    method = data.get("methodological_profile")
    if not isinstance(method, dict):
        fail("methodological_profile deve ser objeto")
    if method.get("method_reference_in_metadata") != "Almeida et al. 2022":
        fail("referência metodológica declarada divergente")
    if method.get("base_method_reference_resolved") is not True:
        fail("metodologia-base Almeida et al. 2022 deve permanecer resolvida")
    if method.get("adaptations_specific_method_document_resolved") is not False:
        fail("adaptações específicas ainda não podem ser consideradas resolvidas")
    if method.get("base_method_ibi") != EXPECTED_IBI:
        fail("IBI da metodologia-base divergente")
    if "Metodologia utilizada nos sistemas Prodes e Deter" not in str(method.get("base_method_citation", "")):
        fail("citação completa da metodologia-base ausente")
    if not official_https(method.get("base_method_evidence_url")):
        fail("evidência oficial da metodologia-base deve usar HTTPS do INPE")
    base_method_url = urlparse(str(method.get("base_method_url", "")))
    if base_method_url.scheme not in {"http", "https"} or base_method_url.hostname != "urlib.net":
        fail("URL persistente da metodologia-base inválida")
    if method.get("validation_profile_resolved") is not False:
        fail("validação não pode ser promovida prematuramente")
    if method.get("uncertainty_profile_resolved") is not False:
        fail("incerteza não pode ser promovida prematuramente")

    temporal = data.get("temporal_profile")
    if not isinstance(temporal, dict) or temporal.get("base_map_year") != 2000:
        fail("mapa base de 2000 deve permanecer registrado")
    phases = temporal.get("increment_phases")
    if not isinstance(phases, list) or len(phases) != 2:
        fail("duas fases temporais são obrigatórias")
    first, second = phases
    if (first.get("start_year"), first.get("end_year"), first.get("cadence")) != (2002, 2018, "biennial"):
        fail("fase bienal 2002–2018 divergente")
    if "2013" not in str(first.get("exception", "")) or "2012" not in str(first.get("exception", "")):
        fail("exceção temporal 2012/2013 ausente")
    if second.get("start_year") != 2018 or second.get("cadence") != "annual":
        fail("fase anual a partir de 2018 divergente")
    if temporal.get("current_release_resolved") is not False:
        fail("release vigente não pode estar resolvida")
    if temporal.get("publication_or_file_update_date_is_scientific_period") is not False:
        fail("data de atualização não pode virar período científico")

    sensors = data.get("sensor_profile")
    if not isinstance(sensors, list) or len(sensors) != 2:
        fail("dois blocos de sensores são obrigatórios")
    sensors_text = " ".join(json.dumps(item, ensure_ascii=False) for item in sensors).casefold()
    for token in ("landsat 5 tm", "landsat 7 etm+", "landsat 8 oli", "sentinel-2a msi", "sentinel-2b msi"):
        if token not in sensors_text:
            fail(f"sensor obrigatório ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "catalog_presence",
        "metadata_identifier_verified",
        "component_relation_to_geopackage_verified",
        "scientific_object_distinguished",
        "historical_temporal_phases_documented",
        "base_method_reference_resolved",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "adaptations_specific_method_document_resolved",
        "current_release_resolved",
        "direct_download_url_verified",
        "redirect_chain_verified",
        "asset_bytes_inspected",
        "checksum_computed",
        "license_resolved_for_asset",
        "citation_resolved_for_product",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 10:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("não herdar", "bienal", "data de atualização", "metodologia-base", "adaptações específicas", "uuid", "endpoint_state", "asset_state", "produto", "release"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    product_required = data.get("required_before_product_promotion")
    asset_required = data.get("required_before_asset_promotion")
    if not isinstance(product_required, list) or len(product_required) < 8:
        fail("requisitos de promoção do produto incompletos")
    if not isinstance(asset_required, list) or len(asset_required) < 8:
        fail("requisitos de promoção do ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"adaptations_specific_method_document_resolved": true',
        '"current_release_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: incrementos PRODES em não floresta preservam identidade, temporalidade, método-base e bloqueios próprios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
