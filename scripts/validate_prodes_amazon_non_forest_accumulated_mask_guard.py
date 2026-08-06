#!/usr/bin/env python3
"""Validate the scientific guard for the PRODES Amazon non-forest accumulated mask through 2000."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_non_forest_accumulated_mask_guard_2026.json")
EXPECTED_UUID = "215be904-3828-41a9-a1bd-c7daa0133944"


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
    if data.get("target_id") != "PRODES-ASSET-NON-FOREST-ACCUMULATED-MASK-2000-SHP":
        fail("alvo operacional inesperado")
    if data.get("candidate_scientific_product_id") != "PD-PRODES-AMZ-NON-FOREST-ACCUMULATED-MASK-2000":
        fail("candidato a produto inesperado")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "catalog_identity_temporal_boundary_and_method_relation_verified_endpoint_unresolved":
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
    if identity.get("product_boundary_state") != "candidate_distinct_non_forest_baseline_scientific_product":
        fail("fronteira científica da linha de base não florestal deve permanecer explícita")
    collapsed = identity.get("must_not_be_collapsed_into")
    if not isinstance(collapsed, list) or set(collapsed) != {
        "PD-PRODES-AMZ-ACCUMULATED-MASK-2007",
        "PD-PRODES-AMZ-NON-FOREST-SUPPRESSION-INCREMENTS",
        "PD-PRODES-AMZ-ANNUAL-MAP",
        "PD-PRODES-AMZ-ANNUAL-RATE",
    }:
        fail("proibição de colapso científico está incompleta")
    identity_text = " ".join(str(value) for value in identity.values()).casefold()
    for token in ("acumulada", "não florestais", "até o ano 2000", "incrementos não florestais"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    method = data.get("methodological_profile")
    if not isinstance(method, dict):
        fail("methodological_profile deve ser objeto")
    if method.get("base_method_reference_resolved") is not True:
        fail("referência metodológica-base deve permanecer resolvida")
    if method.get("adaptations_specific_method_document_resolved") is not False:
        fail("adaptações específicas foram resolvidas prematuramente")
    method_text = " ".join(str(value) for value in method.values()).casefold()
    for token in ("adaptações", "não florestais", "almeida", "2022", "interpretação"):
        if token not in method_text:
            fail(f"perfil metodológico incompleto: {token}")
    for key in ("validation_profile_resolved", "uncertainty_profile_resolved"):
        if method.get(key) is not False:
            fail(f"estado metodológico prematuro: {key}")

    temporal = data.get("temporal_and_release_profile")
    if not isinstance(temporal, dict):
        fail("temporal_and_release_profile deve ser objeto")
    if temporal.get("scientific_cutoff_year") != 2000:
        fail("corte científico deve permanecer 2000")
    if temporal.get("temporal_semantics") != "accumulated_non_forest_baseline_through_2000":
        fail("semântica temporal acumulada não florestal ausente")
    if temporal.get("subsequent_increment_series_starts_after_cutoff_year") != 2002:
        fail("fronteira com incrementos não florestais deve permanecer 2002")
    if temporal.get("subsequent_increment_initial_cadence") != "biennial":
        fail("cadência inicial posterior deve permanecer bienal")
    if temporal.get("current_release_resolved") is not False:
        fail("release foi resolvida prematuramente")
    if temporal.get("publication_or_file_update_date_is_scientific_period") is not False:
        fail("data de atualização não pode virar período científico")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("shapefile", "não florestal", "2000", "geopackage", "2002"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "catalog_presence",
        "metadata_identifier_verified",
        "component_relation_to_geopackage_verified",
        "scientific_object_distinguished",
        "scientific_cutoff_year_documented",
        "boundary_with_non_forest_increments_documented",
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
        "complete_schema_verified_from_bytes",
        "license_resolved_for_asset",
        "citation_resolved_for_data_release",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 10:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("até 2000", "2007", "incrementos", "almeida", "uuid", "release", "endpoint_state", "asset_state"):
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
        '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: máscara PRODES não florestal preserva linha de base até 2000, fronteira com incrementos e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
