#!/usr/bin/env python3
"""Validate the expanded specific metadata profile for DETER Cerrado."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_metadata_profile_guard_2026.json")
EXPECTED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"
EXPECTED_FIELDS = {
    "fid", "classname", "quadrant", "path_row", "view_date", "sensor", "satellite",
    "areauckm", "uc", "areamunkm", "municipality", "geocodibge", "uf",
    "areatotkm", "publish_month",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    return parsed.scheme == "https" and hostname.endswith(("inpe.br", "ibge.gov.br"))


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("contract_version") != "1.1.0":
        fail("versão do contrato inesperada")
    if data.get("family_stable_id") != "PF000003":
        fail("gate deve permanecer vinculado a PF000003")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado divergente")
    if data.get("status") != "cerrado_specific_class_and_metadata_schema_verified_release_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    profile = data.get("specific_metadata_profile")
    if not isinstance(profile, dict):
        fail("specific_metadata_profile deve ser objeto")
    if profile.get("documented_class_name") != "DESMATAMENTO_CR":
        fail("classe específica documentada divergente")
    if profile.get("class_domain_complete_for_metadata_record_verified") is not True:
        fail("domínio do registro específico deve estar documentado")
    if profile.get("class_domain_complete_for_current_release_verified") is not False:
        fail("domínio da release atual não pode ser promovido")
    profile_text = json.dumps(profile, ensure_ascii=False).casefold()
    for token in ("cerrado", "solo exposto", "landsat ou similares", "supressão completa"):
        if token not in profile_text:
            fail(f"perfil específico incompleto: {token}")
    for key in (
        "cerrado_specific_method_version_resolved",
        "cerrado_specific_minimum_area_resolved",
        "cerrado_specific_spatial_resolution_resolved",
    ):
        if profile.get(key) is not False:
            fail(f"estado específico prematuro: {key}")

    schema = data.get("documented_metadata_schema")
    if not isinstance(schema, list) or len(schema) != len(EXPECTED_FIELDS):
        fail("inventário do esquema do metadado deve conter exatamente quinze campos")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    if fields != EXPECTED_FIELDS:
        fail(f"campos documentados divergentes: {sorted(fields ^ EXPECTED_FIELDS)}")
    schema_text = json.dumps(schema, ensure_ascii=False).casefold()
    for token in (
        "desmatamento_cr", "corrente", "histórica", "fora de uso", "cbers",
        "órbita", "data da imagem", "sensor", "satélite", "unidade de conservação",
        "operações de soma", "ibge", "não deve ser somada", "geoserver",
    ):
        if token not in schema_text:
            fail(f"semântica do esquema ausente: {token}")

    channels = data.get("schema_and_channel_semantics")
    if not isinstance(channels, dict):
        fail("schema_and_channel_semantics deve ser objeto")
    for key in (
        "metadata_record_schema_inventory_complete",
        "shapefile_field_names_truncated_to_ten_characters",
        "areamunkm_is_recommended_sum_field",
        "areatotkm_must_not_be_summed",
        "areatotkm_registered_download_only",
        "publish_month_geoserver_only",
        "registered_download_channel_documented",
    ):
        if channels.get(key) is not True:
            fail(f"semântica de canal ausente: {key}")
    for key in ("schema_verified_from_asset_bytes", "geoserver_specific_layer_resolved"):
        if channels.get(key) is not False:
            fail(f"canal promovido prematuramente: {key}")

    identifiers = data.get("identifier_and_table_semantics")
    if not isinstance(identifiers, dict):
        fail("identifier_and_table_semantics deve ser objeto")
    if identifiers.get("current_suffix") != "_curr" or identifiers.get("historical_suffix") != "_hist":
        fail("sufixos corrente/histórico divergentes")
    if identifiers.get("current_and_historical_tables_are_distinct_operational_partitions") is not True:
        fail("partições operacionais não foram preservadas")
    for key in (
        "suffix_identifies_scientific_release",
        "fid_is_persistent_cross_release_identifier",
        "metadata_uuid_is_feature_identifier",
    ):
        if identifiers.get(key) is not False:
            fail(f"semântica de identificador prematura: {key}")

    spatial = data.get("spatial_context")
    if not isinstance(spatial, dict):
        fail("spatial_context deve ser objeto")
    if spatial.get("geographic_domain") != "bioma Cerrado":
        fail("domínio geográfico divergente")
    if spatial.get("representation_type") != "vector":
        fail("representação deve permanecer vetorial")
    if spatial.get("metadata_scale_denominator_observed") != 250000:
        fail("escala declarada divergente")
    if spatial.get("dataset_adjusted_to_2019_ibge_biome_boundary") is not True:
        fail("ajuste ao recorte de 2019 deve estar documentado")
    for key in (
        "scale_denominator_is_spatial_resolution",
        "current_crs_resolved",
        "geometry_verified_from_bytes",
    ):
        if spatial.get(key) is not False:
            fail(f"perfil espacial promovido prematuramente: {key}")

    temporal = data.get("temporal_and_method_boundaries")
    if not isinstance(temporal, dict):
        fail("temporal_and_method_boundaries deve ser objeto")
    if temporal.get("since_year_documented") != 2018:
        fail("início documentado deve permanecer 2018")
    if temporal.get("maintenance_frequency_documented") != "daily":
        fail("frequência de manutenção deve permanecer daily")
    for key in (
        "since_year_is_release_identifier",
        "detection_date_is_exact_suppression_date",
        "landsat_or_similar_is_complete_sensor_history",
        "general_current_deter_3ha_threshold_inherited_as_cerrado_specific_metadata_fact",
        "general_current_wfi_profile_replaces_specific_metadata_statement",
        "publish_month_is_scientific_release",
    ):
        if temporal.get(key) is not False:
            fail(f"fronteira temporal ou metodológica violada: {key}")

    citation = data.get("citation_context")
    if not isinstance(citation, dict):
        fail("citation_context deve ser objeto")
    if citation.get("recommended_dataset_citation_resolved") is not True:
        fail("orientação de citação específica deve estar resolvida")
    if citation.get("recommended_dataset_citation_year") != 2024:
        fail("ano da citação recomendada divergente")
    if EXPECTED_UUID not in str(citation.get("recommended_dataset_citation", "")):
        fail("citação recomendada deve preservar o UUID do metadado")
    if citation.get("citation_access_date_example") != "2024-09-02":
        fail("data de acesso exemplar divergente")
    for key in (
        "citation_year_is_current_release_identifier",
        "access_date_example_is_current_access_date",
        "citation_for_current_release_resolved",
    ):
        if citation.get(key) is not False:
            fail(f"citação promovida prematuramente: {key}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (
        "desmatamento_cr", "fid", "classname", "publish_month", "areamunkm",
        "areatotkm", "_curr", "_hist", "2024", "250.000", "2019",
    ):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "specific_metadata_record_resolved",
        "specific_documented_class_resolved",
        "class_domain_complete_for_metadata_record_verified",
        "metadata_schema_inventory_documented",
        "channel_specific_field_semantics_documented",
        "current_historical_partition_semantics_documented",
        "citation_guidance_documented",
        "biome_boundary_adjustment_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "complete_current_release_class_domain_verified",
        "current_release_resolved",
        "direct_download_url_verified",
        "geoserver_specific_layer_resolved",
        "asset_bytes_inspected",
        "complete_schema_verified_from_bytes",
        "license_resolved_for_release",
        "citation_resolved_for_current_release",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 17:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "desmatamento_cr", "deter amazônia", "_curr", "_hist", "fid", "uuid",
        "2018", "2024", "landsat", "3 ha", "1:250.000", "areamunkm",
        "areatotkm", "publish_month", "incerteza", "release",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"current_release_resolved": true',
        '"direct_download_url_verified": true',
        '"geoserver_specific_layer_resolved": true',
        '"asset_bytes_inspected": true',
        '"complete_schema_verified_from_bytes": true',
        '"citation_resolved_for_current_release": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print(
        "OK: metadado DETER Cerrado preserva classe específica, inventário de esquema, "
        "semântica de canais e promoção negativa"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
