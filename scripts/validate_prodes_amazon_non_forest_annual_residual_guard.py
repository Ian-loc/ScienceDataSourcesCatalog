#!/usr/bin/env python3
"""Validate the scientific boundary guard for the PRODES Amazon non-forest annual residual product."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_non_forest_annual_residual_guard_2026.json")
EXPECTED_UUID = "63751b72-3e6a-4d15-8fc0-740e57bbc346"


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

    expected = {
        "family_stable_id": "PF000001",
        "target_id": "PRODES-ASSET-ANNUAL-NON-FOREST-SUPPRESSION-RESIDUAL-SHP",
        "candidate_scientific_product_id": "PD-PRODES-AMZ-NON-FOREST-ANNUAL-RESIDUAL",
        "parent_package_asset_id": "PRODES-ASSET-AMAZON-GEOPACKAGE",
        "status": "metadata_identity_non_forest_retrospective_revision_method_and_partial_schema_verified_endpoint_unresolved",
        "timezone": "America/Sao_Paulo",
        "metadata_identifier": EXPECTED_UUID,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            fail(f"valor inesperado para {key}")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")
    if not official_https(data.get("metadata_url")) or EXPECTED_UUID not in data["metadata_url"]:
        fail("metadata_url oficial inválida")
    if not official_https(data.get("catalog_url")):
        fail("catalog_url deve apontar para fonte oficial do INPE")

    identity = data.get("scientific_identity")
    if not isinstance(identity, dict):
        fail("scientific_identity deve ser objeto")
    if identity.get("product_boundary_state") != "candidate_distinct_non_forest_retrospective_revision_scientific_product":
        fail("fronteira científica não florestal deve permanecer explícita")
    if identity.get("interpretation_type") != "retrospective_revision_polygons_non_forest":
        fail("tipo interpretativo inesperado")
    for key in ("is_statistical_residual", "is_uncertainty_estimate", "is_current_period_increment"):
        if identity.get(key) is not False:
            fail(f"interpretação proibida detectada: {key}")
    expected_collapsed = {
        "PD-PRODES-AMZ-ANNUAL-RESIDUAL",
        "PD-PRODES-AMZ-NON-FOREST-SUPPRESSION-INCREMENTS",
        "PD-PRODES-AMZ-NON-FOREST-ACCUMULATED-MASK-2000",
        "PD-PRODES-AMZ-ANNUAL-MAP",
        "PD-PRODES-AMZ-ANNUAL-RATE",
    }
    collapsed = identity.get("must_not_be_collapsed_into")
    if not isinstance(collapsed, list) or set(collapsed) != expected_collapsed:
        fail("proibição de colapso científico está incompleta")
    identity_text = " ".join(str(value) for value in identity.values()).casefold()
    for token in ("não florestais", "revisão retrospectiva", "não incremento", "erro estatístico"):
        if token not in identity_text:
            fail(f"identidade científica incompleta: {token}")

    method = data.get("methodological_profile")
    if not isinstance(method, dict):
        fail("methodological_profile deve ser objeto")
    if method.get("base_method_reference_resolved") is not True:
        fail("metodologia-base resolvida foi perdida")
    if method.get("specific_adaptations_documented_as_required") is not True:
        fail("necessidade de adaptações específicas deve permanecer explícita")
    if method.get("specific_adaptations_version_resolved") is not False:
        fail("versão das adaptações foi resolvida prematuramente")
    if method.get("minimum_mapped_area_ha") != 1.0:
        fail("área mínima documentada deve permanecer 1 ha")
    method_text = " ".join(json.dumps(value, ensure_ascii=False) for value in method.values()).casefold()
    for token in ("landsat 5 tm", "landsat 7 etm+", "landsat 8 oli", "sentinel-2a msi", "sentinel-2b msi", "interpretação visual", "auditores seniores", "menores que 1 ha"):
        if token not in method_text:
            fail(f"perfil metodológico incompleto: {token}")
    if method.get("future_land_use_independent") is not True:
        fail("definição de supressão independente do uso posterior foi perdida")
    for key in ("validation_profile_resolved", "uncertainty_profile_resolved"):
        if method.get(key) is not False:
            fail(f"estado metodológico prematuro: {key}")

    temporal = data.get("temporal_and_release_profile")
    if not isinstance(temporal, dict):
        fail("temporal_and_release_profile deve ser objeto")
    expected_temporal = {
        "systematic_monitoring_operation_announced_from_year": 2023,
        "historical_series_objective_start_year": 2000,
        "base_map_year": 2000,
        "biennial_increment_start_year": 2002,
        "biennial_increment_end_year": 2018,
        "year_2012_replaced_by": 2013,
        "annual_mapping_from_year": 2018,
        "temporal_semantics": "retrospective_revision_within_non_forest_series",
        "operation_start_is_series_start": False,
        "current_release_resolved": False,
        "last_scientific_year_resolved": False,
        "publication_or_file_update_date_is_scientific_period": False,
        "pub_date_is_scientific_period": False,
    }
    for key, value in expected_temporal.items():
        if temporal.get(key) != value:
            fail(f"perfil temporal divergente: {key}")
    examples = temporal.get("class_name_examples")
    if not isinstance(examples, list) or set(examples) != {"residuo", "r2022"}:
        fail("exemplos de class_name divergentes")

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
    for token in ("pode mudar", "r2022", "preenchimento conforme aplicabilidade", "não constitui por si só release", "não é período científico"):
        if token not in schema_text:
            fail(f"qualificação crítica do esquema ausente: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("2023", "série desde 2000", "2012/2013", "auditoria sênior", "1 ha", "shapefile", "resíduo anual geral"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "catalog_presence", "metadata_identifier_verified", "component_relation_to_geopackage_verified",
        "scientific_object_distinguished", "non_forest_domain_documented",
        "retrospective_revision_semantics_documented", "operation_and_series_start_distinguished",
        "methodological_sensor_transition_documented", "senior_audit_and_minimum_area_rule_documented",
        "partial_schema_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "current_release_resolved", "direct_download_url_verified", "redirect_chain_verified",
        "asset_bytes_inspected", "checksum_computed", "complete_schema_verified_from_bytes",
        "license_resolved_for_asset", "citation_resolved_for_data_release",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 13:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("erro estatístico", "resíduo anual geral", "máscara-base", "2023", "2000", "2002–2018", "2013", "1 ha", "uid", "uuid", "main_class", "pub_date", "endpoint_state"):
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
        '"promotion_authorized": true', '"current_release_resolved": true',
        '"direct_download_url_verified": true', '"asset_bytes_inspected": true',
        '"checksum_computed": true', '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: resíduo não florestal PRODES preserva domínio, método, temporalidade e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
