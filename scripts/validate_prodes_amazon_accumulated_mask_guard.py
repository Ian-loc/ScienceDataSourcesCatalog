#!/usr/bin/env python3
"""Validate the scientific and temporal guard for the PRODES Amazon accumulated mask through 2007."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_accumulated_mask_guard_2026.json")
EXPECTED_UUID = "c6748fdf-a18e-41b9-a523-ea14bae92602"


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
    if data.get("target_id") != "PRODES-ASSET-ACCUMULATED-SUPPRESSION-MASK-2007-SHP":
        fail("alvo operacional inesperado")
    if data.get("candidate_scientific_product_id") != "PD-PRODES-AMZ-ACCUMULATED-MASK-2007":
        fail("candidato a produto inesperado")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "metadata_identity_temporal_boundary_and_partial_schema_verified_endpoint_unresolved":
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
    if identity.get("product_boundary_state") != "candidate_distinct_baseline_scientific_product":
        fail("fronteira científica da linha de base deve permanecer explícita")
    collapsed = identity.get("must_not_be_collapsed_into")
    if not isinstance(collapsed, list) or set(collapsed) != {
        "PD-PRODES-AMZ-ANNUAL-MAP",
        "PD-PRODES-AMZ-ANNUAL-RATE",
        "PD-PRODES-AMZ-SMALL-POLYGON-INCREMENTS",
    }:
        fail("proibição de colapso científico está incompleta")
    identity_text = " ".join(str(value) for value in identity.values()).casefold()
    for token in ("acumulada", "até 2007", "bioma amazônia", "incrementos iniciada em 2008"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    method = data.get("methodological_profile")
    if not isinstance(method, dict):
        fail("methodological_profile deve ser objeto")
    if method.get("minimum_mapped_area_ha") != 6.25:
        fail("área mínima documentada deve permanecer 6,25 ha")
    method_text = " ".join(str(value) for value in method.values()).casefold()
    for token in ("landsat", "interpretação visual", "independentemente do uso subsequente"):
        if token not in method_text:
            fail(f"perfil metodológico incompleto: {token}")
    for key in ("base_method_reference_resolved", "validation_profile_resolved", "uncertainty_profile_resolved"):
        if method.get(key) is not False:
            fail(f"estado metodológico prematuro: {key}")

    temporal = data.get("temporal_and_release_profile")
    if not isinstance(temporal, dict):
        fail("temporal_and_release_profile deve ser objeto")
    if temporal.get("scientific_cutoff_year") != 2007:
        fail("corte científico deve permanecer 2007")
    if temporal.get("temporal_semantics") != "accumulated_baseline_through_2007":
        fail("semântica temporal acumulada ausente")
    if temporal.get("annual_increment_series_starts_after_cutoff_year") != 2008:
        fail("fronteira com incrementos anuais deve permanecer 2008")
    if temporal.get("current_release_resolved") is not False:
        fail("release foi resolvida prematuramente")
    if temporal.get("publication_or_file_update_date_is_scientific_period") is not False:
        fail("data de atualização não pode virar período científico")

    schema = data.get("documented_partial_schema")
    if not isinstance(schema, list) or len(schema) < 11:
        fail("esquema parcial documentado insuficiente")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    expected_fields = {"uuid", "uid", "state", "path_row", "main_class", "class_name", "year", "area_km", "source", "geom", "pub_date"}
    if not expected_fields.issubset(fields):
        fail("campos documentados obrigatórios ausentes")
    schema_text = " ".join(json.dumps(item, ensure_ascii=False) for item in schema).casefold()
    for token in ("pode mudar", "desmatamento", "d2007", "2007", "não é período científico"):
        if token not in schema_text:
            fail(f"qualificação crítica do esquema ausente: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("acumulado", "2007", "6,25 ha", "shapefile", "geopackage"):
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
        "annual_increment_boundary_documented",
        "partial_schema_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
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
    if not isinstance(rules, list) or len(rules) < 13:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("até 2007", "desde 2008", "6,25 ha", "uid", "uuid", "pub_date", "release", "endpoint_state", "asset_state"):
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
        '"current_release_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
        '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: máscara PRODES Amazônia preserva acumulado até 2007, fronteira com incrementos e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
