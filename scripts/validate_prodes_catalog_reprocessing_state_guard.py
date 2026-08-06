#!/usr/bin/env python3
"""Validate the operational guard for the TerraBrasilis PRODES reprocessing notice."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_catalog_reprocessing_state_guard_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_inpe_https(url: object) -> bool:
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
    if data.get("status") != "catalog_reprocessing_notice_active_operational_resolution_blocked":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")
    if not official_inpe_https(data.get("official_catalog_url")):
        fail("catálogo oficial HTTPS do INPE obrigatório")

    notice = data.get("official_update_notice")
    if not isinstance(notice, dict):
        fail("official_update_notice deve ser objeto")
    if notice.get("announcement_date") != "2026-03-03":
        fail("data do aviso oficial divergente")
    if notice.get("applies_to_all_native_vegetation_suppression_files") is not True:
        fail("abrangência do aviso oficial foi perdida")
    if "atualize" not in str(notice.get("statement", "")).casefold():
        fail("recomendação oficial de atualização ausente")

    warning = data.get("current_catalog_warning")
    if not isinstance(warning, dict):
        fail("current_catalog_warning deve ser objeto")
    if "reprocessado" not in str(warning.get("statement", "")).casefold():
        fail("aviso de reprocessamento ausente")
    for key in (
        "target_file_unambiguously_identified",
        "warning_is_release_identifier",
        "warning_is_permanent_unavailability_evidence",
    ):
        if warning.get(key) is not False:
            fail(f"inferência prematura no aviso: {key}")

    snapshots = data.get("observed_snapshot_variation")
    if not isinstance(snapshots, dict):
        fail("observed_snapshot_variation deve ser objeto")
    if snapshots.get("non_www_snapshot_date") != "2026-06-16":
        fail("snapshot sem www divergente")
    if snapshots.get("www_snapshot_date") != "2026-07-20":
        fail("snapshot com www divergente")
    if snapshots.get("same_catalog_entries_observed") is not True:
        fail("identidade das entradas observadas deve permanecer registrada")
    if snapshots.get("dates_define_distinct_scientific_releases") is not False:
        fail("datas de interface não podem definir releases distintas")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "official_update_notice_present",
        "catalog_reprocessing_warning_present",
        "catalog_entries_discoverable",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "individual_direct_download_urls_verified",
        "individual_endpoint_states_verified",
        "individual_current_releases_resolved",
        "asset_bytes_inspected",
        "checksums_computed",
    ):
        if state.get(key) is not False:
            fail(f"estado operacional prematuro: {key}")

    rules = data.get("normalization_rules")
    required = data.get("required_before_operational_promotion")
    if not isinstance(rules, list) or len(rules) < 9:
        fail("regras de normalização insuficientes")
    if not isinstance(required, list) or len(required) < 7:
        fail("requisitos de promoção insuficientes")
    text = " ".join(str(item) for item in rules).casefold()
    for token in ("release_id", "reprocessamento", "www", "working", "unavailable", "endpoint_state", "asset_state", "checksum"):
        if token not in text:
            fail(f"regra obrigatória ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"individual_direct_download_urls_verified": true',
        '"individual_endpoint_states_verified": true',
        '"asset_bytes_inspected": true',
        '"checksums_computed": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: aviso de reprocessamento PRODES permanece contextual, sem resolver release, endpoint ou ativo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
