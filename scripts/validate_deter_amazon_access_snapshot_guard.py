#!/usr/bin/env python3
"""Validate DETER Amazon official access evidence and dated operational snapshot boundaries."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_amazon_access_snapshot_guard_2026.json")
FOREST_UUID = "f2153c4a-915b-48a6-8658-963bdce7366c"


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
        fail("gate deve permanecer vinculado à família DETER Amazônia")
    if data.get("parent_product_candidate_id") != "PD-DETER-AMZ-ALERTS":
        fail("produto pai inesperado")
    if data.get("status") != "official_access_channel_and_dated_operational_snapshot_verified_assets_unresolved":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("gate não pode autorizar promoção")

    access = data.get("access_channel")
    if not isinstance(access, dict):
        fail("access_channel deve ser objeto")
    if not official_https(access.get("official_download_page")):
        fail("página oficial de download inválida")
    if access.get("declared_format") != "ESRI Shapefile":
        fail("formato declarado divergente")
    if access.get("non_forest_public_availability_since") != "2023-11-08":
        fail("data oficial de disponibilização não florestal divergente")
    for key in (
        "direct_download_url_verified", "http_status_verified", "redirect_chain_verified",
        "authentication_requirement_resolved", "asset_bytes_inspected", "checksum_computed",
    ):
        if access.get(key) is not False:
            fail(f"estado operacional prematuro: {key}")

    snapshot = data.get("dated_operational_snapshot")
    if not isinstance(snapshot, dict):
        fail("dated_operational_snapshot deve ser objeto")
    if not official_https(snapshot.get("report_url")):
        fail("relatório operacional deve usar fonte oficial")
    if snapshot.get("report_scope") != "DETER Amazônia - Não Floresta":
        fail("escopo do relatório divergente")
    if snapshot.get("series_start_date") != "2023-08-01":
        fail("início da série operacional divergente")
    if snapshot.get("snapshot_end_date") != "2026-07-20":
        fail("corte do snapshot divergente")
    if snapshot.get("reported_accumulated_suppression_alert_area_km2") != 1356.46:
        fail("total agregado de supressão divergente")
    if snapshot.get("reported_accumulated_degradation_alert_area_km2") != 56823.45:
        fail("total agregado de degradação divergente")
    for key in (
        "snapshot_is_scientific_release", "snapshot_is_download_asset_identity",
        "snapshot_is_complete_distribution_schema",
    ):
        if snapshot.get(key) is not False:
            fail(f"snapshot promovido indevidamente: {key}")

    metadata = data.get("metadata_resolution")
    if not isinstance(metadata, dict):
        fail("metadata_resolution deve ser objeto")
    if metadata.get("forest_metadata_identifier") != FOREST_UUID:
        fail("UUID florestal divergente")
    if metadata.get("non_forest_metadata_record_discoverable") is not True:
        fail("descoberta do registro não florestal deve permanecer documentada")
    if metadata.get("non_forest_metadata_identifier_verified") is not False:
        fail("UUID não florestal não pode ser considerado verificado")
    if metadata.get("non_forest_metadata_identifier") is not None:
        fail("UUID não florestal não pode ser inferido")

    boundaries = data.get("scientific_and_operational_boundaries")
    if not isinstance(boundaries, dict):
        fail("scientific_and_operational_boundaries deve ser objeto")
    for key in (
        "report_detection_period_is_exact_event_period", "report_area_is_canonical_release_total",
        "report_summary_can_replace_polygon_distribution", "download_page_presence_proves_endpoint_working",
    ):
        if boundaries.get(key) is not False:
            fail(f"fronteira negativa ausente: {key}")
    for key in ("experimental_non_forest_status_preserved", "forest_and_non_forest_assets_must_be_resolved_separately"):
        if boundaries.get(key) is not True:
            fail(f"fronteira positiva ausente: {key}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL oficial HTTPS do INPE")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in ("08/11/2023", "experimental", "20 de julho de 2026", "shapefile"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    rules = data.get("normalization_rules")
    required = data.get("required_before_asset_promotion")
    if not isinstance(rules, list) or len(rules) < 8:
        fail("regras de normalização insuficientes")
    if not isinstance(required, list) or len(required) < 8:
        fail("requisitos de promoção insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("release", "evento", "http", "uuid", "relatório", "shapefile", "experimental", "bytes"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true', '"direct_download_url_verified": true',
        '"http_status_verified": true', '"asset_bytes_inspected": true',
        '"checksum_computed": true', '"non_forest_metadata_identifier_verified": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: acesso e snapshot DETER Amazônia permanecem datados, separados de release e sem promoção de ativo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
