#!/usr/bin/env python3
"""Validate the guard for PRODES Amazon deforestation polygons between 1 and 6.25 ha."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_small_polygon_increment_guard_2026.json")
EXPECTED_UUID = "5f5cfb4c-e207-4932-9c93-2d51cea8adbc"


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
    if data.get("target_id") != "PRODES-ASSET-ANNUAL-INCREMENT-1-TO-6-25-HA-SHP":
        fail("alvo operacional inesperado")
    if data.get("candidate_scientific_product_id") != "PD-PRODES-AMZ-SMALL-POLYGON-INCREMENTS":
        fail("candidato a produto inesperado")
    if data.get("parent_package_asset_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("pacote agregador inesperado")
    if data.get("status") != "metadata_identity_methodological_boundary_and_release_semantics_verified_endpoint_unresolved":
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
    if identity.get("product_boundary_state") != "candidate_distinct_supplementary_scientific_product":
        fail("fronteira científica suplementar deve permanecer explícita")
    collapsed = identity.get("must_not_be_collapsed_into")
    if not isinstance(collapsed, list) or set(collapsed) != {"PD-PRODES-AMZ-ANNUAL-MAP", "PD-PRODES-AMZ-ANNUAL-RATE"}:
        fail("proibição de colapso no mapa e na taxa anual está incompleta")
    identity_text = " ".join(str(value) for value in identity.values()).casefold()
    for token in ("1 e 6,25", "bioma amazônia", "limiar de área", "substituição integral"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    method = data.get("methodological_boundary")
    if not isinstance(method, dict):
        fail("methodological_boundary deve ser objeto")
    if method.get("historical_minimum_mappable_area_ha") != 6.25:
        fail("área mínima histórica deve permanecer 6,25 ha")
    if method.get("digital_mapping_scale") != "1:75.000":
        fail("escala declarada do mapeamento digital divergente")
    if method.get("small_polygon_storage_start_year") != 2016:
        fail("início do armazenamento dos pequenos polígonos deve permanecer 2016")
    if method.get("small_polygon_area_min_ha") != 1.0 or method.get("small_polygon_area_max_ha") != 6.25:
        fail("intervalo de área 1–6,25 ha divergente")
    if method.get("included_in_annual_rate_before_exceeding_6_25_ha") is not False:
        fail("pequenos polígonos não podem ser incluídos prematuramente na taxa")
    if "ultrapassarem 6,25 ha" not in str(method.get("rate_inclusion_rule", "")):
        fail("regra explícita de inclusão na taxa ausente")
    for key in ("base_method_reference_resolved", "validation_profile_resolved", "uncertainty_profile_resolved"):
        if method.get(key) is not False:
            fail(f"estado metodológico prematuro: {key}")

    temporal = data.get("temporal_and_release_profile")
    if not isinstance(temporal, dict):
        fail("temporal_and_release_profile deve ser objeto")
    if temporal.get("storage_start_year") != 2016:
        fail("ano inicial temporal divergente")
    if temporal.get("cadence_label_in_catalog") != "annual":
        fail("cadência declarada no catálogo deve permanecer anual")
    if temporal.get("publication_replacement_semantics") != "integral_replacement_each_publication":
        fail("semântica de substituição integral ausente")
    if temporal.get("current_release_resolved") is not False or temporal.get("last_scientific_year_resolved") is not False:
        fail("release ou último ano foram resolvidos prematuramente")
    if temporal.get("publication_or_file_update_date_is_scientific_period") is not False:
        fail("data de atualização não pode virar período científico")

    schema = data.get("documented_partial_schema")
    if not isinstance(schema, list) or len(schema) < 7:
        fail("esquema parcial documentado insuficiente")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    expected_fields = {"uuid", "uid", "state", "path_row", "main_class", "class_name", "def_cloud"}
    if not expected_fields.issubset(fields):
        fail("campos documentados obrigatórios ausentes")
    schema_text = " ".join(json.dumps(item, ensure_ascii=False) for item in schema).casefold()
    if "pode mudar" not in schema_text or "não há distinção de classe" not in schema_text:
        fail("qualificações críticas de uid ou class_name ausentes")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("nota técnica", "substituição integral", "esquema parcial", "shapefile"):
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
        "historical_minimum_mapping_rule_documented",
        "small_polygon_storage_start_year_documented",
        "rate_exclusion_rule_documented",
        "integral_replacement_semantics_documented",
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
    if not isinstance(rules, list) or len(rules) < 12:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("taxa anual", "resolução espacial", "uid", "uuid", "substituição integral", "esquema", "endpoint_state", "asset_state", "release"):
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

    print("OK: polígonos PRODES de 1–6,25 ha preservam fronteira científica, regra da taxa e semântica de release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
