#!/usr/bin/env python3
"""Validate aggregate-search safeguards for the PRODES Amazon GeoPackage record."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_geopackage_search_facet_guard_2026.json")


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
    if data.get("scientific_target") != "PD-PRODES-AMZ-ANNUAL-MAP":
        fail("alvo científico inesperado")
    if data.get("target_id") != "PRODES-ASSET-AMAZON-GEOPACKAGE":
        fail("alvo operacional inesperado")
    if data.get("status") != "aggregate_search_facets_verified_record_download_unresolved":
        fail("estado agregado deve permanecer explicitamente não resolvido")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")

    evidence = data.get("official_search_evidence")
    if not isinstance(evidence, dict):
        fail("official_search_evidence deve ser objeto")
    if not official_https(evidence.get("search_url")):
        fail("search_url deve apontar para fonte HTTPS oficial do INPE")
    if evidence.get("provider") != "TerraBrasilis catalogue":
        fail("provedor oficial inesperado")
    if evidence.get("format_filter") != "GeoPackage":
        fail("filtro de formato deve permanecer GeoPackage")
    if evidence.get("record_count") != 8:
        fail("contagem auditada de registros GeoPackage divergente")
    if evidence.get("resource_type_count") != {"Dataset": 8}:
        fail("contagem de tipos de recurso divergente")
    if evidence.get("available_action_count") != {"Downloadable": 1}:
        fail("contagem agregada de ações divergente")
    if evidence.get("status_count") != {"Planned": 8}:
        fail("contagem agregada de status divergente")
    if evidence.get("representation_type_count") != {"Vector": 8}:
        fail("contagem de representação divergente")
    if evidence.get("target_record_title") != "GeoPackage - PRODES Amazônia":
        fail("título do registro-alvo divergente")
    if evidence.get("target_record_present") is not True:
        fail("presença do registro-alvo deve permanecer verificada")
    for key in (
        "target_record_direct_download_identified",
        "target_record_downloadable_action_attributed",
        "target_record_status_resolved",
    ):
        if evidence.get(key) is not False:
            fail(f"atribuição prematura detectada: {key}")

    assessment = data.get("assessment")
    if not isinstance(assessment, dict):
        fail("assessment deve ser objeto")
    if assessment.get("blocker_type") != "aggregate_facet_attribution":
        fail("tipo de bloqueio inesperado")
    if assessment.get("severity") != "medium" or assessment.get("state") != "accepted_limitation":
        fail("severidade ou estado da limitação divergente")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 9:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        "faceta agregada",
        "downloadable",
        "planned",
        "bytes",
        "byte_size",
        "direct_download_url",
        "endpoint_state",
        "asset_state",
        "release_id",
    ):
        if token.casefold() not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    record_required = data.get("required_before_record_level_resolution")
    asset_required = data.get("required_before_asset_promotion")
    if not isinstance(record_required, list) or len(record_required) < 7:
        fail("requisitos de resolução individual incompletos")
    if not isinstance(asset_required, list) or len(asset_required) < 8:
        fail("requisitos de promoção do ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"target_record_direct_download_identified": true',
        '"target_record_downloadable_action_attributed": true',
        '"target_record_status_resolved": true',
    ):
        if forbidden in serialized:
            fail(f"promoção ou atribuição prematura detectada: {forbidden}")

    print("OK: facetas GeoPackage permanecem agregadas sem atribuir download, status ou release ao registro Amazônia")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
