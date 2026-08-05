#!/usr/bin/env python3
"""Validate the pre-promotion PRODES asset and endpoint inspection contract."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_asset_endpoint_contract_2026.json")
EXPECTED_ROLES = {
    "annual_increment_vector": "Shapefile",
    "small_polygon_increment_vector": "Shapefile",
    "complete_map_raster": "GeoTIFF",
    "complete_map_vector": "GeoPackage",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000001":
        fail("contrato deve permanecer vinculado a PF000001")
    if data.get("status") != "pre_promotion_asset_resolution":
        fail("status deve permanecer pre_promotion_asset_resolution")
    if data.get("promotion_authorized") is not False:
        fail("contrato não pode autorizar promoção")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")

    entry = data.get("catalog_entrypoint")
    if not isinstance(entry, dict):
        fail("catalog_entrypoint deve ser objeto")
    parsed = urlparse(str(entry.get("url", "")))
    if parsed.scheme != "https" or not (parsed.hostname or "").endswith("inpe.br"):
        fail("entrypoint deve usar URL HTTPS oficial do INPE")
    if entry.get("role") != "download_catalog":
        fail("entrypoint deve permanecer classificado como download_catalog")
    if entry.get("is_direct_asset") is not False or entry.get("is_release_identifier") is not False:
        fail("catálogo não pode ser tratado como ativo direto ou identificador de release")

    targets = data.get("asset_targets")
    if not isinstance(targets, list) or len(targets) != 4:
        fail("quatro alvos de ativo são obrigatórios")

    target_ids: set[str] = set()
    roles: set[str] = set()
    for target in targets:
        target_id = target.get("target_id")
        if not isinstance(target_id, str) or not target_id:
            fail("todo alvo deve possuir target_id")
        if target_id in target_ids:
            fail(f"target_id duplicado: {target_id}")
        target_ids.add(target_id)

        if target.get("scientific_target") != "PD-PRODES-AMZ-ANNUAL-MAP":
            fail(f"{target_id}: alvo científico inesperado")
        role = target.get("distribution_role")
        expected_format = EXPECTED_ROLES.get(role)
        if expected_format is None:
            fail(f"{target_id}: papel operacional inesperado: {role}")
        roles.add(role)
        if target.get("expected_format") != expected_format:
            fail(f"{target_id}: formato incompatível com o papel")
        if target.get("catalog_presence") != "confirmed":
            fail(f"{target_id}: presença no catálogo deve estar confirmada")
        if target.get("endpoint_state") != "unresolved":
            fail(f"{target_id}: endpoint não verificado deve permanecer unresolved")
        if target.get("asset_state") != "not_inspected":
            fail(f"{target_id}: ativo não inspecionado deve permanecer not_inspected")
        if target.get("direct_download_url") is not None or target.get("metadata_url") is not None:
            fail(f"{target_id}: URL específica não pode ser preenchida sem verificação direta")
        checks = target.get("required_direct_checks")
        if not isinstance(checks, list) or len(checks) < 8:
            fail(f"{target_id}: checklist direto insuficiente")
        checks_text = " ".join(str(item) for item in checks).casefold()
        for required in ("checksum", "crs", "licença", "citação"):
            if required not in checks_text:
                fail(f"{target_id}: verificação obrigatória ausente: {required}")

    if roles != set(EXPECTED_ROLES):
        fail(f"papéis incompletos: {sorted(roles)}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 5:
        fail("regras de normalização devem ser explícitas")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for term in ("catálogo", "metadado", "download", "checksums", "verified", "inspected"):
        if term not in rules_text:
            fail(f"regra estrutural ausente: {term}")

    unresolved = data.get("unresolved_before_asset_promotion")
    if not isinstance(unresolved, list) or len(unresolved) < 6:
        fail("pendências de ativos devem permanecer explícitas")
    unresolved_text = " ".join(str(item) for item in unresolved).casefold()
    for term in ("urls", "crs", "checksums", "versionamento", "licença", "citação"):
        if term not in unresolved_text:
            fail(f"pendência obrigatória ausente: {term}")

    serialized = PATH.read_text(encoding="utf-8")
    for token in ('"promotion_authorized": true', '"endpoint_state": "verified"', '"asset_state": "inspected"'):
        if token in serialized:
            fail(f"promoção ou verificação prematura detectada: {token}")

    print("OK: contrato de ativos e endpoints PRODES validado sem promoção prematura")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
