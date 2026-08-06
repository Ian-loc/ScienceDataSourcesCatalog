#!/usr/bin/env python3
"""Validate the scientific boundary guard for the PRODES Amazon annual residual product."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_annual_residual_guard_2026.json")
EXPECTED_UUID = "00a728cb-8577-458a-9c38-082c1f3bca9e"


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
    if data.get("target_id") != "PRODES-ASSET-ANNUAL-NATIVE-VEGETATION-SUPPRESSION-RESIDUAL-SHP":
        fail("alvo operacional inesperado")
    if data.get("candidate_scientific_product_id") != "PD-PRODES-AMZ-ANNUAL-RESIDUAL":
        fail("candidato a produto inesperado")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "metadata_identity_retrospective_revision_semantics_and_partial_schema_verified_endpoint_unresolved":
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
    if identity.get("product_boundary_state") != "candidate_distinct_retrospective_revision_scientific_product":
        fail("fronteira científica retrospectiva deve permanecer explícita")
    if identity.get("interpretation_type") != "retrospective_revision_polygons":
        fail("tipo interpretativo inesperado")
    for key in ("is_statistical_residual", "is_uncertainty_estimate", "is_current_year_increment"):
        if identity.get(key) is not False:
            fail(f"interpretação proibida detectada: {key}")
    collapsed = identity.get("must_not_be_collapsed_into")
    expected_collapsed = {
        "PD-PRODES-AMZ-ANNUAL-MAP",
        "PD-PRODES-AMZ-ANNUAL-RATE",
        "PD-PRODES-AMZ-ACCUMULATED-MASK-2007",
        "PD-PRODES-AMZ-SMALL-POLYGON-INCREMENTS",
        "PD-PRODES-AMZ-NON-FOREST-ANNUAL-RESIDUAL",
    }
    if not isinstance(collapsed, list) or set(collapsed) != expected_collapsed:
        fail("proibição de colapso científico está incompleta")
    identity_text = " ".join(str(value) for value in identity.values()).casefold()
    for token in ("revisão", "anos anteriores", "não incremento", "erro estatístico", "incerteza"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    method = data.get("methodological_profile")
    if not isinstance(method, dict):
        fail("methodological_profile deve ser objeto")
    if method.get("minimum_mapped_area_ha") != 6.25:
        fail("área mínima documentada deve permanecer 6,25 ha")
    method_text = " ".join(str(value) for value in method.values()).casefold()
    for token in ("landsat", "supressão", "ibge", "2019"):
        if token not in method_text:
            fail(f"perfil metodológico incompleto: {token}")
    if method.get("future_land_use_independent") is not True:
        fail("definição de supressão independente do uso posterior foi perdida")
    if method.get("biome_boundary_adjustment_documented") is not True:
        fail("ajuste ao limite de bioma não está documentado")
    for key in (
        "base_method_reference_resolved",
        "residual_detection_procedure_version_resolved",
        "validation_profile_resolved",
        "uncertainty_profile_resolved",
    ):
        if method.get(key) is not False:
            fail(f"estado metodológico prematuro: {key}")

    temporal = data.get("temporal_and_release_profile")
    if not isinstance(temporal, dict):
        fail("temporal_and_release_profile deve ser objeto")
    if temporal.get("temporal_semantics") != "retrospective_revision_of_surveys_prior_to_current_mapping_year":
        fail("semântica temporal retrospectiva ausente")
    if temporal.get("class_name_pattern") != "rYYYY" or temporal.get("documented_example") != "r2020":
        fail("padrão temporal documentado de class_name foi alterado")
    for key in (
        "class_year_is_release_identifier",
        "current_release_resolved",
        "last_scientific_year_resolved",
        "publication_or_file_update_date_is_scientific_period",
        "pub_date_is_scientific_period",
    ):
        if temporal.get(key) is not False:
            fail(f"estado temporal prematuro: {key}")
    if temporal.get("catalog_cadence_label") != "annual":
        fail("cadência declarada no catálogo deve permanecer anual")
    if "exportação" not in str(temporal.get("pub_date_semantics", "")).casefold():
        fail("semântica de pub_date deve permanecer explícita")

    schema = data.get("documented_partial_schema")
    if not isinstance(schema, list) or len(schema) < 18:
        fail("esquema parcial documentado insuficiente")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    expected_fields = {
        "uuid", "uid", "state", "path_row", "main_class", "class_name", "def_cloud",
        "julian_day", "image_date", "year", "area_km", "scene_id", "publish_year",
        "source", "satellite", "sensor", "geom", "pub_date",
    }
    if not expected_fields.issubset(fields):
        fail("campos documentados obrigatórios ausentes")
    schema_text = " ".join(json.dumps(item, ensure_ascii=False) for item in schema).casefold()
    for token in ("pode mudar", "ryyyy", "r2020", "não constitui por si só release", "não é período científico"):
        if token not in schema_text:
            fail(f"qualificação crítica do esquema ausente: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("revisão", "6,25 ha", "landsat", "ryyyy", "shapefile", "geopackage", "resíduo não florestal"):
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
        "retrospective_revision_semantics_documented",
        "not_statistical_residual_documented",
        "minimum_mapped_area_documented",
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
    for token in (
        "erro estatístico", "incremento do ano corrente", "máscara acumulada", "não florestais",
        "6,25 ha", "uid", "uuid", "ryyyy", "pub_date", "endpoint_state", "asset_state", "release",
    ):
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

    print("OK: resíduo anual PRODES Amazônia preserva revisão retrospectiva, fronteiras científicas e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
