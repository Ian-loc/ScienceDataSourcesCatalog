#!/usr/bin/env python3
"""Validate the reconciled specific metadata profile for DETER Cerrado."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_metadata_profile_guard_2026.json")
CURRENT_UUID = "e6e15388-4ca9-49b9-aec9-03891339a35e"
STALE_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"
EXPECTED_FIELDS = {
    "fid", "classname", "quadrant", "path_row", "view_date", "sensor", "satellite",
    "areauckm", "uc", "areamunkm", "municipality", "geocodibge", "uf",
    "areatotkm", "publish_month",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def trusted_url(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").casefold()
    return parsed.scheme == "https" and (
        hostname.endswith("inpe.br")
        or hostname.endswith("ibge.gov.br")
        or hostname == "doi.org"
    )


def require_false(mapping: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) is not False:
            fail(f"{label} promovido prematuramente: {key}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("contract_version") != "1.2.0":
        fail("versão do contrato inesperada")
    if data.get("family_stable_id") != "PF000003":
        fail("família inesperada")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("metadata_identifier") != CURRENT_UUID:
        fail("UUID corrente do metadado divergente")
    if data.get("superseded_citation_identifier") != STALE_UUID:
        fail("UUID histórico da citação não preservado")
    if data.get("status") != "cerrado_specific_metadata_record_reconciled_schema_verified_release_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone divergente")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    profile = data.get("specific_metadata_profile")
    if not isinstance(profile, dict):
        fail("specific_metadata_profile deve ser objeto")
    if profile.get("documented_class_name") != "DESMATAMENTO_CR":
        fail("classe específica divergente")
    if profile.get("class_domain_complete_for_metadata_record_verified") is not True:
        fail("domínio do registro específico deve estar documentado")
    require_false(
        profile,
        (
            "class_domain_complete_for_current_release_verified",
            "cerrado_specific_method_version_resolved",
            "cerrado_specific_minimum_area_resolved",
            "cerrado_specific_spatial_resolution_resolved",
        ),
        "perfil específico",
    )

    schema = data.get("documented_metadata_schema")
    if not isinstance(schema, list) or len(schema) != 15:
        fail("inventário do metadado deve conter quinze campos")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    if fields != EXPECTED_FIELDS:
        fail(f"campos documentados divergentes: {sorted(fields ^ EXPECTED_FIELDS)}")
    schema_text = json.dumps(schema, ensure_ascii=False).casefold()
    for token in (
        "desmatamento_cr", "corrente", "histórica", "cbers", "órbita",
        "data da imagem", "operações de soma", "ibge", "não deve ser somada", "geoserver",
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
    require_false(channels, ("schema_verified_from_asset_bytes", "geoserver_specific_layer_resolved"), "canal")

    reconciliation = data.get("identifier_reconciliation")
    if not isinstance(reconciliation, dict):
        fail("identifier_reconciliation deve ser objeto")
    for key in (
        "current_geonetwork_record_uuid_resolved",
        "current_record_discovered_from_official_search_result_link",
        "peer_reviewed_data_availability_reference_matches_current_uuid",
        "published_biomasbr_citation_contains_superseded_uuid",
        "superseded_uuid_may_identify_another_official_record",
    ):
        if reconciliation.get(key) is not True:
            fail(f"reconciliação incompleta: {key}")
    if reconciliation.get("current_geonetwork_record_uuid") != CURRENT_UUID:
        fail("UUID reconciliado divergente")
    if CURRENT_UUID not in str(reconciliation.get("current_record_api_url", "")):
        fail("URL da API sem UUID corrente")
    require_false(
        reconciliation,
        (
            "current_record_api_fetch_succeeded",
            "superseded_uuid_is_current_deter_cerrado_metadata_record",
            "root_cause_of_published_citation_drift_resolved",
        ),
        "reconciliação",
    )

    identifiers = data.get("identifier_and_table_semantics")
    if not isinstance(identifiers, dict):
        fail("identifier_and_table_semantics deve ser objeto")
    if identifiers.get("current_suffix") != "_curr" or identifiers.get("historical_suffix") != "_hist":
        fail("sufixos corrente/histórico divergentes")
    if identifiers.get("current_and_historical_tables_are_distinct_operational_partitions") is not True:
        fail("partições operacionais não preservadas")
    require_false(
        identifiers,
        ("suffix_identifies_scientific_release", "fid_is_persistent_cross_release_identifier", "metadata_uuid_is_feature_identifier"),
        "identificador",
    )

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
        fail("ajuste ao recorte de 2019 ausente")
    require_false(spatial, ("scale_denominator_is_spatial_resolution", "current_crs_resolved", "geometry_verified_from_bytes"), "perfil espacial")

    temporal = data.get("temporal_and_method_boundaries")
    if not isinstance(temporal, dict):
        fail("temporal_and_method_boundaries deve ser objeto")
    if temporal.get("since_year_documented") != 2018 or temporal.get("maintenance_frequency_documented") != "daily":
        fail("perfil temporal específico divergente")
    require_false(
        temporal,
        (
            "since_year_is_release_identifier",
            "detection_date_is_exact_suppression_date",
            "landsat_or_similar_is_complete_sensor_history",
            "general_current_deter_3ha_threshold_inherited_as_cerrado_specific_metadata_fact",
            "general_current_wfi_profile_replaces_specific_metadata_statement",
            "publish_month_is_scientific_release",
        ),
        "fronteira temporal/metodológica",
    )

    citation = data.get("citation_context")
    if not isinstance(citation, dict):
        fail("citation_context deve ser objeto")
    if citation.get("published_citation_guidance_documented") is not True:
        fail("orientação de citação publicada não documentada")
    if citation.get("published_citation_guidance_year") != 2024:
        fail("ano da orientação de citação divergente")
    if citation.get("published_citation_guidance_metadata_identifier") != STALE_UUID:
        fail("UUID histórico da orientação divergente")
    if citation.get("published_citation_guidance_identifier_is_current") is not False:
        fail("UUID histórico não pode permanecer corrente")
    if CURRENT_UUID not in str(citation.get("current_metadata_record_url", "")):
        fail("URL do registro corrente divergente")
    require_false(
        citation,
        ("citation_year_is_current_release_identifier", "access_date_example_is_current_access_date", "citation_for_current_release_resolved"),
        "citação",
    )

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidências insuficientes")
    roles = {item.get("role") for item in evidence if isinstance(item, dict)}
    expected_roles = {
        "current_cerrado_specific_metadata_record",
        "peer_reviewed_data_availability_identifier",
        "published_program_citation_guidance_with_stale_identifier",
        "biome_boundary_change",
    }
    if roles != expected_roles:
        fail("papéis de evidência divergentes")
    for item in evidence:
        if not trusted_url(item.get("url")):
            fail(f"URL de evidência não confiável: {item.get('url')}")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (CURRENT_UUID, STALE_UUID, "desmatamento_cr", "areamunkm", "areatotkm", "publish_month", "2019"):
        if token.casefold() not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "specific_metadata_record_resolved",
        "current_metadata_identifier_reconciled",
        "specific_documented_class_resolved",
        "class_domain_complete_for_metadata_record_verified",
        "metadata_schema_inventory_documented",
        "channel_specific_field_semantics_documented",
        "current_historical_partition_semantics_documented",
        "published_citation_guidance_documented",
        "biome_boundary_adjustment_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    if state.get("published_citation_identifier_current") is not False:
        fail("identificador da citação publicada não pode ser corrente")
    require_false(
        state,
        (
            "complete_current_release_class_domain_verified",
            "current_release_resolved",
            "direct_download_url_verified",
            "geoserver_specific_layer_resolved",
            "asset_bytes_inspected",
            "complete_schema_verified_from_bytes",
            "license_resolved_for_release",
            "citation_resolved_for_current_release",
        ),
        "estado científico-operacional",
    )

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 19:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        CURRENT_UUID, STALE_UUID, "registro de metadados", "produto", "release", "ativo",
        "desmatamento_cr", "deter amazônia", "_curr", "_hist", "fid", "2018", "2024",
        "landsat", "3 ha", "1:250.000", "areamunkm", "areatotkm", "publish_month", "incerteza",
    ):
        if token.casefold() not in rules_text:
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
        '"published_citation_guidance_identifier_is_current": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print(
        "OK: metadado DETER Cerrado reconciliado no UUID corrente; referência histórica, "
        "esquema e estados negativos preservados"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
