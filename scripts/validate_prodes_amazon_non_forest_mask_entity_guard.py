#!/usr/bin/env python3
"""Validate entity resolution for the PRODES Amazon non-forest auxiliary mask."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_non_forest_mask_entity_guard_2026.json")
EXPECTED_UUID = "bed1276c-aa3d-4f5b-b560-1879617ef13d"


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
    if data.get("target_id") != "PRODES-ASSET-NON-FOREST-MASK-SHP":
        fail("alvo operacional inesperado")
    if data.get("candidate_entity_id") != "AX-PRODES-AMZ-NON-FOREST-DOMAIN-MASK":
        fail("identificador da entidade auxiliar inesperado")
    if data.get("candidate_entity_type") != "auxiliary_domain_mask":
        fail("papel da entidade deve permanecer auxiliary_domain_mask")
    if data.get("candidate_scientific_product_id") is not None:
        fail("máscara auxiliar não pode receber produto científico sem nova decisão evidenciada")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "metadata_identity_auxiliary_domain_role_and_partial_schema_verified_endpoint_unresolved":
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

    resolution = data.get("entity_resolution")
    if not isinstance(resolution, dict):
        fail("entity_resolution deve ser objeto")
    if resolution.get("resolved_role") != "auxiliary_spatial_domain_and_classification_mask":
        fail("papel espacial auxiliar foi alterado")
    if resolution.get("standalone_scientific_product_supported") is not False:
        fail("produto científico autônomo foi sustentado prematuramente")
    if resolution.get("scientific_product_promotion_blocked") is not True:
        fail("bloqueio de promoção científica deve permanecer ativo")
    resolution_text = " ".join(str(value) for value in resolution.values()).casefold()
    for token in ("tipologias", "não enquadradas", "floresta", "máscara auxiliar", "não uma observação anual"):
        if token not in resolution_text:
            fail(f"resolução de entidade incompleta: {token}")

    boundaries = data.get("semantic_boundaries")
    if not isinstance(boundaries, dict):
        fail("semantic_boundaries deve ser objeto")
    for key in ("producer_defined_class", "amazon_legal_specific_class_in_prodes"):
        if boundaries.get(key) is not True:
            fail(f"fronteira positiva ausente: {key}")
    for key in (
        "is_native_vegetation_remainder_inventory",
        "is_forest_extent_product",
        "is_annual_suppression_increment",
        "is_non_forest_suppression_increment",
        "is_accumulated_non_forest_suppression",
        "is_annual_non_forest_residual",
        "is_deforestation_rate",
    ):
        if boundaries.get(key) is not False:
            fail(f"interpretação proibida detectada: {key}")
    collapsed = boundaries.get("must_not_be_collapsed_into")
    expected = {
        "PD-PRODES-AMZ-NON-FOREST-ACCUMULATED-MASK-2000",
        "PD-PRODES-AMZ-NON-FOREST-SUPPRESSION-INCREMENTS",
        "PD-PRODES-AMZ-NON-FOREST-ANNUAL-RESIDUAL",
        "PD-PRODES-AMZ-ANNUAL-MAP",
        "PD-PRODES-AMZ-ANNUAL-RATE",
    }
    if not isinstance(collapsed, list) or set(collapsed) != expected:
        fail("proibição de colapso científico está incompleta")

    classes = data.get("documented_class_profile")
    if not isinstance(classes, dict):
        fail("documented_class_profile deve ser objeto")
    if classes.get("main_class_documented_value") != "NAO_FLORESTA":
        fail("main_class documentada foi alterada")
    if set(classes.get("class_name_documented_values", [])) != {"NAO_FLORESTA", "NAO_FLORESTA2"}:
        fail("valores documentados de class_name foram alterados")
    if "revisão" not in str(classes.get("nao_floresta2_interpretation", "")).casefold():
        fail("NAO_FLORESTA2 deve permanecer qualificada como revisão")
    for key in (
        "class_values_are_complete_domain_verified_from_bytes",
        "class_temporal_semantics_resolved",
        "class_method_version_resolved",
    ):
        if classes.get(key) is not False:
            fail(f"estado prematuro de classe detectado: {key}")

    schema = data.get("documented_partial_schema")
    if not isinstance(schema, list) or len(schema) < 7:
        fail("esquema parcial documentado insuficiente")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    expected_fields = {"uuid", "uid", "state", "path_row", "main_class", "class_name", "def_cloud"}
    if not expected_fields.issubset(fields):
        fail("campos documentados obrigatórios ausentes")
    schema_text = " ".join(json.dumps(item, ensure_ascii=False) for item in schema).casefold()
    for token in ("nao_floresta", "nao_floresta2", "rastreabilidade", "landsat"):
        if token not in schema_text:
            fail(f"qualificação de esquema ausente: {token}")

    method = data.get("methodological_and_temporal_profile")
    if not isinstance(method, dict):
        fail("methodological_and_temporal_profile deve ser objeto")
    for key in (
        "classification_method_version_resolved",
        "creation_or_revision_period_resolved",
        "current_release_resolved",
        "validation_profile_resolved",
        "uncertainty_profile_resolved",
        "publication_or_file_update_date_is_scientific_period",
    ):
        if method.get(key) is not False:
            fail(f"estado metodológico ou temporal prematuro: {key}")
    warning = str(method.get("warning", "")).casefold()
    for token in ("não herdar", "1 ha", "sensores", "supressão"):
        if token not in warning:
            fail(f"advertência metodológica incompleta: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("no_forest_biome", "tipologias", "nao_floresta2", "shapefile", "geopackage"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "catalog_presence",
        "metadata_identifier_verified",
        "component_relation_to_geopackage_verified",
        "auxiliary_domain_role_verified",
        "producer_defined_class_documented",
        "partial_schema_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "standalone_scientific_product_supported",
        "class_method_version_resolved",
        "class_temporal_semantics_resolved",
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
    if not isinstance(rules, list) or len(rules) < 14:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "máscara auxiliar", "vegetação remanescente", "nao_floresta2", "supressão", "1 ha",
        "deter", "data de atualização", "uuid", "uid", "endpoint_state", "asset_state",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    auxiliary_required = data.get("required_before_auxiliary_asset_promotion")
    asset_required = data.get("required_before_asset_promotion")
    if not isinstance(auxiliary_required, list) or len(auxiliary_required) < 8:
        fail("requisitos curatoriais da camada auxiliar incompletos")
    if not isinstance(asset_required, list) or len(asset_required) < 8:
        fail("requisitos de promoção do ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"candidate_scientific_product_id": "',
        '"standalone_scientific_product_supported": true',
        '"class_method_version_resolved": true',
        '"class_temporal_semantics_resolved": true',
        '"current_release_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
        '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção ou interpretação prematura detectada: {forbidden}")

    print("OK: máscara Não Floresta permanece camada auxiliar de domínio, com classes originais e promoção científica bloqueada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
