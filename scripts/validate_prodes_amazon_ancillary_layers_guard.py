#!/usr/bin/env python3
"""Validate scientific boundaries for PRODES Amazon ancillary cartographic layers."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_ancillary_layers_guard_2026.json")
EXPECTED = {
    "PRODES-ASSET-AMAZON-HYDROGRAPHY-SHP": (
        "PD-PRODES-AMZ-HYDROGRAPHY",
        "1df78632-68e7-4e91-bca0-25305d3f831e",
    ),
    "PRODES-ASSET-AMAZON-NON-FOREST-HYDROGRAPHY-SHP": (
        "PD-PRODES-AMZ-NON-FOREST-HYDROGRAPHY",
        "87fb6a32-01c1-4421-b7d0-a93568e1b079",
    ),
    "PRODES-ASSET-AMAZON-NON-FOREST-DOMAIN-MASK-SHP": (
        "PD-PRODES-AMZ-NON-FOREST-DOMAIN-MASK",
        "bed1276c-aa3d-4f5b-b560-1879617ef13d",
    ),
}


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
        fail("portão deve permanecer vinculado a PF000001")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "ancillary_cartographic_layer_identities_and_boundaries_verified_endpoints_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")

    layers = data.get("layers")
    if not isinstance(layers, list) or len(layers) != 3:
        fail("três camadas auxiliares são obrigatórias")
    targets: set[str] = set()
    products: set[str] = set()
    uuids: set[str] = set()
    by_target: dict[str, dict] = {}
    for layer in layers:
        if not isinstance(layer, dict):
            fail("cada camada deve ser objeto")
        target = layer.get("target_id")
        if target not in EXPECTED:
            fail(f"alvo inesperado: {target}")
        product, uuid = EXPECTED[target]
        if layer.get("candidate_scientific_product_id") != product:
            fail(f"produto candidato divergente para {target}")
        if layer.get("metadata_identifier") != uuid:
            fail(f"UUID divergente para {target}")
        if not official_https(layer.get("metadata_url")) or uuid not in layer["metadata_url"]:
            fail(f"metadata_url inválida para {target}")
        targets.add(target)
        products.add(product)
        uuids.add(uuid)
        by_target[target] = layer
    if targets != set(EXPECTED) or len(products) != 3 or len(uuids) != 3:
        fail("identidades das camadas auxiliares incompletas ou duplicadas")

    hydro = by_target["PRODES-ASSET-AMAZON-HYDROGRAPHY-SHP"]
    if hydro.get("product_type") != "ancillary_cartographic_water_body_layer":
        fail("tipo da hidrografia geral divergente")
    if hydro.get("declared_cadence") != "annual":
        fail("cadência anual declarada da hidrografia geral foi perdida")
    hydro_text = json.dumps(hydro, ensure_ascii=False).casefold()
    for token in ("rios", "lagos", "barramentos", "represamentos", "hidrografia", "2019"):
        if token not in hydro_text:
            fail(f"hidrografia geral incompleta: {token}")
    spatial = hydro.get("spatial_context", {})
    if spatial.get("biome_boundary_adjustment_documented") is not True:
        fail("ajuste de limite da hidrografia geral deve permanecer documentado")
    if spatial.get("biome_boundary_reference_year") != 2019:
        fail("ano de referência do limite de bioma divergente")

    nf_hydro = by_target["PRODES-ASSET-AMAZON-NON-FOREST-HYDROGRAPHY-SHP"]
    if nf_hydro.get("product_type") != "ancillary_cartographic_water_body_layer_within_non_forest_domain":
        fail("tipo da hidrografia não florestal divergente")
    context = nf_hydro.get("non_forest_program_context", {})
    expected_context = {
        "systematic_operation_announced_from_year": 2023,
        "historical_series_objective_start_year": 2000,
        "approximate_domain_area_km2": 280000,
        "approximate_domain_share_percent": 6.6,
        "specific_adaptations_version_resolved": False,
        "sensor_history_belongs_to_non_forest_monitoring_program_not_automatically_to_hydrography_asset": True,
    }
    for key, value in expected_context.items():
        if context.get(key) != value:
            fail(f"contexto não florestal divergente: {key}")
    if nf_hydro.get("spatial_context", {}).get("non_forest_domain_metadata_reference") != "bed1276c-aa3d-4f5b-b560-1879617ef13d":
        fail("referência à máscara de não floresta ausente")

    mask = by_target["PRODES-ASSET-AMAZON-NON-FOREST-DOMAIN-MASK-SHP"]
    if mask.get("product_type") != "domain_mask_and_classification_support_layer":
        fail("tipo da máscara de não floresta divergente")
    mask_text = json.dumps(mask, ensure_ascii=False).casefold()
    for token in ("não enquadradas na classe de floresta", "nao_floresta", "nao_floresta2", "não significa área sem vegetação", "ausência de dado"):
        if token not in mask_text:
            fail(f"semântica da máscara de não floresta incompleta: {token}")

    for target, layer in by_target.items():
        boundary = layer.get("scientific_boundary")
        if not isinstance(boundary, dict):
            fail(f"scientific_boundary ausente para {target}")
        collapsed = boundary.get("must_not_be_collapsed_into")
        if not isinstance(collapsed, list) or len(collapsed) < 5:
            fail(f"fronteira de colapso insuficiente para {target}")
        boundary_text = json.dumps(boundary, ensure_ascii=False).casefold()
        if "false" not in boundary_text:
            fail(f"estados científicos negativos ausentes para {target}")

    schema = data.get("shared_documented_partial_schema")
    expected_schema = {
        "uuid", "uid", "state", "path_row", "main_class", "class_name", "def_cloud",
        "julian_day", "image_date", "year", "area_km", "scene_id", "publish_year",
        "source", "satellite", "sensor", "geom", "pub_date",
    }
    if not isinstance(schema, list) or set(schema) != expected_schema:
        fail("esquema parcial compartilhado divergente")

    identifiers = data.get("identifier_and_temporal_rules")
    if not isinstance(identifiers, dict):
        fail("identifier_and_temporal_rules deve ser objeto")
    for key in (
        "uid_is_persistent_identifier", "feature_uuid_is_metadata_uuid", "year_is_release_identifier",
        "publish_year_is_scientific_period", "pub_date_is_scientific_period",
        "catalog_update_date_is_release_identifier",
    ):
        if identifiers.get(key) is not False:
            fail(f"regra temporal ou de identificador prematura: {key}")
    if "exportação" not in str(identifiers.get("pub_date_semantics", "")).casefold():
        fail("semântica de pub_date ausente")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 5:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("hidrografia", "não floresta", "2019", "aplicabilidade", "shapefile", "camadas auxiliares"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "all_three_catalog_entries_present", "all_three_metadata_identifiers_verified",
        "all_three_component_relations_to_geopackage_verified", "ancillary_layer_role_documented",
        "hydrography_object_documented", "non_forest_domain_mask_semantics_documented",
        "general_and_non_forest_hydrography_distinguished", "partial_schema_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "individual_current_releases_resolved", "direct_download_urls_verified", "asset_bytes_inspected",
        "checksums_computed", "complete_schemas_verified_from_bytes", "licenses_resolved_for_assets",
        "citations_resolved_for_data_releases",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 13:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "observação de supressão", "ausência de vegetação", "hidrografia geral", "sensores",
        "facetas agregadas", "2019", "2023", "uid", "uuid", "pub_date", "endpoint_state", "asset_state",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    product_required = data.get("required_before_product_promotion")
    asset_required = data.get("required_before_asset_promotion")
    if not isinstance(product_required, list) or len(product_required) < 8:
        fail("requisitos de promoção de produto incompletos")
    if not isinstance(asset_required, list) or len(asset_required) < 8:
        fail("requisitos de promoção de ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true', '"individual_current_releases_resolved": true',
        '"direct_download_urls_verified": true', '"asset_bytes_inspected": true',
        '"checksums_computed": true', '"complete_schemas_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: camadas auxiliares PRODES Amazônia preservam identidades, domínios e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
