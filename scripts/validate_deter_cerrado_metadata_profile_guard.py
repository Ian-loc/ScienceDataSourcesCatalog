#!/usr/bin/env python3
"""Validate the specific metadata profile for DETER Cerrado."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_metadata_profile_guard_2026.json")
EXPECTED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


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

    if data.get("family_stable_id") != "PF000003":
        fail("gate deve permanecer vinculado a PF000003")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado divergente")
    if data.get("status") != "cerrado_specific_class_partial_schema_and_identifier_semantics_verified_release_unresolved":
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
    profile_text = json.dumps(profile, ensure_ascii=False).casefold()
    for token in ("cerrado", "solo exposto", "landsat ou similares", "supressão completa"):
        if token not in profile_text:
            fail(f"perfil específico incompleto: {token}")
    for key in (
        "class_domain_complete_for_current_release_verified",
        "cerrado_specific_method_version_resolved",
        "cerrado_specific_minimum_area_resolved",
        "cerrado_specific_spatial_resolution_resolved",
    ):
        if profile.get(key) is not False:
            fail(f"estado específico prematuro: {key}")

    schema = data.get("documented_partial_schema")
    if not isinstance(schema, list) or len(schema) != 3:
        fail("esquema parcial deve conter exatamente três campos documentados")
    fields = {item.get("field") for item in schema if isinstance(item, dict)}
    if fields != {"fid", "classname", "quadrant"}:
        fail("campos específicos documentados divergentes")
    schema_text = json.dumps(schema, ensure_ascii=False).casefold()
    for token in ("corrente", "histórica", "desmatamento_cr", "fora de uso", "cbers"):
        if token not in schema_text:
            fail(f"semântica do esquema ausente: {token}")

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

    temporal = data.get("temporal_and_method_boundaries")
    if not isinstance(temporal, dict):
        fail("temporal_and_method_boundaries deve ser objeto")
    if temporal.get("since_year_documented") != 2018:
        fail("início documentado deve permanecer 2018")
    for key in (
        "since_year_is_release_identifier",
        "detection_date_is_exact_suppression_date",
        "landsat_or_similar_is_complete_sensor_history",
        "general_current_deter_3ha_threshold_inherited_as_cerrado_specific_metadata_fact",
        "general_current_wfi_profile_replaces_specific_metadata_statement",
    ):
        if temporal.get(key) is not False:
            fail(f"fronteira temporal ou metodológica violada: {key}")

    citation = data.get("citation_context")
    if not isinstance(citation, dict):
        fail("citation_context deve ser objeto")
    if citation.get("recommended_dataset_citation_year") != 2024:
        fail("ano da citação recomendada divergente")
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
    if not isinstance(evidence, list) or len(evidence) < 2:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("desmatamento_cr", "fid", "classname", "quadrant", "_curr", "_hist", "2024"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "specific_metadata_record_resolved",
        "specific_documented_class_resolved",
        "partial_schema_documented",
        "current_historical_partition_semantics_documented",
        "citation_context_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "complete_current_class_domain_verified",
        "current_release_resolved",
        "direct_download_url_verified",
        "asset_bytes_inspected",
        "complete_schema_verified_from_bytes",
        "license_resolved_for_release",
        "citation_resolved_for_current_release",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 13:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "desmatamento_cr", "deter amazônia", "_curr", "_hist", "fid", "uuid",
        "2018", "2024", "landsat", "3 ha", "incerteza", "release",
    ):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"current_release_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: metadado DETER Cerrado preserva classe específica, esquema parcial e promoção negativa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
