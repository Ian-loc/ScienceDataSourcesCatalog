#!/usr/bin/env python3
"""Validate the DETER Amazon WFS capability guard without asserting live availability."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_amazon_wfs_capability_guard_2026.json")


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

    if data.get("family_stable_id") != "PF000002":
        fail("gate deve permanecer vinculado a PF000002")
    if data.get("parent_product_candidate_id") != "PD-DETER-AMZ-ALERTS":
        fail("produto candidato inesperado")
    if data.get("status") != "official_wfs_access_pattern_and_partial_schema_documented_live_state_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    capability = data.get("service_capability")
    if not isinstance(capability, dict):
        fail("service_capability deve ser objeto")
    expected = {
        "service_type": "OGC WFS",
        "workspace": "deter-amz",
        "service_url": "https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/wfs",
        "documented_version": "2.0.0",
        "documented_feature_type": "deter_public",
        "documented_request_crs": "EPSG:4674",
        "documented_output_format": "SHAPE-ZIP",
    }
    for key, value in expected.items():
        if capability.get(key) != value:
            fail(f"capacidade WFS divergente: {key}")
    if not official_https(capability.get("service_url")):
        fail("service_url deve apontar para fonte oficial HTTPS")
    for key in (
        "supports_get_capabilities_documented", "supports_describe_feature_type_documented",
        "supports_get_feature_documented", "supports_cql_temporal_filter_documented",
    ):
        if capability.get(key) is not True:
            fail(f"operação oficial documentada ausente: {key}")
    for key in ("service_is_scientific_product", "service_is_release", "service_is_distribution_asset"):
        if capability.get(key) is not False:
            fail(f"capacidade promovida indevidamente: {key}")

    example = data.get("documented_query_example")
    if not isinstance(example, dict) or example.get("filter_attribute") != "date":
        fail("exemplo temporal oficial ausente")
    if example.get("example_start") != "2019-01-01" or example.get("example_end") != "2019-02-01":
        fail("intervalo do exemplo oficial divergente")
    if example.get("example_is_current_release_definition") is not False:
        fail("exemplo não pode definir release atual")
    if example.get("example_is_complete_product_period") is not False:
        fail("exemplo não pode definir período integral")

    schema = data.get("partial_schema_from_current_metadata_search")
    if not isinstance(schema, dict):
        fail("perfil parcial de esquema ausente")
    expected_fields = {
        "fid", "class_name", "area_km", "view_date", "create_date", "audit_date",
        "sensor", "satellite", "path_row", "uuid",
    }
    if set(schema.get("fields", [])) != expected_fields:
        fail("campos parciais documentados divergentes")
    if schema.get("fid_current_history_suffixes_documented") != ["_curr", "_hist"]:
        fail("sufixos de fid divergentes")
    if schema.get("shapefile_column_name_truncation_documented") is not True:
        fail("truncamento Shapefile deve permanecer documentado")
    if schema.get("example_truncation") != "create_date -> create_dat":
        fail("exemplo de truncamento divergente")
    for key in ("schema_verified_by_live_describe_feature_type", "complete_schema_verified_from_bytes"):
        if schema.get(key) is not False:
            fail(f"esquema promovido prematuramente: {key}")

    live = data.get("live_verification_attempt")
    if not isinstance(live, dict) or live.get("attempted") is not True:
        fail("tentativa de verificação viva deve ser registrada")
    for key in ("get_capabilities_verified", "describe_feature_type_verified", "get_feature_hits_verified"):
        if live.get(key) is not False:
            fail(f"estado vivo prematuro: {key}")
    if live.get("result") != "instrumental_failure_or_bad_request_without_authoritative_service_response":
        fail("resultado instrumental divergente")
    live_text = json.dumps(live, ensure_ascii=False).casefold()
    if "não prova indisponibilidade" not in live_text or "working" not in live_text or "unavailable" not in live_text:
        fail("interpretação conservadora da falha instrumental ausente")

    boundaries = data.get("scientific_and_operational_boundaries")
    if not isinstance(boundaries, dict):
        fail("fronteiras operacionais ausentes")
    for key in (
        "source_capability_must_be_separate_from_product",
        "feature_type_must_be_linked_to_correct_distribution_and_release_before_promotion",
        "historical_documentation_does_not_prove_current_service_state",
        "wfs_export_does_not_replace_shapefile_release_identity",
        "shapefile_truncated_fields_must_not_replace_canonical_field_names",
        "forest_and_non_forest_wfs_layers_resolved_separately",
    ):
        if boundaries.get(key) is not True:
            fail(f"fronteira obrigatória ausente: {key}")
    if boundaries.get("date_filter_does_not_prove_exact_event_date") is not True:
        fail("limitação temporal do filtro ausente")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL oficial HTTPS")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("getcapabilities", "describefeaturetype", "getfeature", "deter_public", "epsg:4674", "shape-zip", "_curr", "_hist"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 9:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("capacidade da fonte", "release", "working", "unavailable", "2019", "data exata", "truncamentos", "não florestal", "crs"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    required = data.get("required_before_operational_promotion")
    if not isinstance(required, list) or len(required) < 8:
        fail("requisitos de promoção operacional incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"get_capabilities_verified": true',
        '"describe_feature_type_verified": true',
        '"get_feature_hits_verified": true',
        '"schema_verified_by_live_describe_feature_type": true',
        '"complete_schema_verified_from_bytes": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: WFS DETER Amazônia permanece capacidade documentada, com esquema parcial e estado vivo não resolvido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
