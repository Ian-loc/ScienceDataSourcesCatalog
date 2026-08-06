#!/usr/bin/env python3
"""Validate the pre-promotion PRODES asset and endpoint inspection contract."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_asset_endpoint_contract_2026.json")
REGISTRY_PATH = Path("database/mappings/prodes_geonetwork_metadata_registry_2026.json")
EXPECTED_ROLES = {
    "annual_increment_vector": "Shapefile",
    "small_polygon_increment_vector": "Shapefile",
    "complete_map_raster": "GeoTIFF",
    "complete_map_vector": "GeoPackage",
}
VERIFIED_METADATA_ROLES = {
    "annual_increment_vector",
    "small_polygon_increment_vector",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_metadata_url(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    parsed = urlparse(value)
    return (
        parsed.scheme == "https"
        and (parsed.hostname or "").endswith("inpe.br")
        and "/geonetwork/" in parsed.path
        and "/metadata/" in value
    )


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    if not REGISTRY_PATH.is_file():
        fail(f"registro GeoNetwork ausente: {REGISTRY_PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000001":
        fail("contrato deve permanecer vinculado a PF000001")
    if data.get("status") != "pre_promotion_asset_resolution":
        fail("status deve permanecer pre_promotion_asset_resolution")
    if data.get("promotion_authorized") is not False:
        fail("contrato não pode autorizar promoção")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")

    if registry.get("family_stable_id") != "PF000001":
        fail("registro GeoNetwork deve permanecer vinculado a PF000001")
    registry_by_role = {
        record.get("expected_distribution_role"): record.get("metadata_url")
        for record in registry.get("records", [])
        if record.get("expected_distribution_role") in VERIFIED_METADATA_ROLES
    }
    if set(registry_by_role) != VERIFIED_METADATA_ROLES:
        fail("registro GeoNetwork não contém os dois metadados exigidos pelos alvos")

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
        if target.get("direct_download_url") is not None:
            fail(f"{target_id}: download direto não pode ser preenchido sem verificação")

        metadata_url = target.get("metadata_url")
        metadata_state = target.get("metadata_state")
        if role in VERIFIED_METADATA_ROLES:
            expected_metadata_url = registry_by_role[role]
            if metadata_url != expected_metadata_url:
                fail(f"{target_id}: URL de metadado diverge do registro GeoNetwork")
            if metadata_state != "verified_metadata_identifier":
                fail(f"{target_id}: estado de metadado verificado divergente")
            if not official_metadata_url(metadata_url):
                fail(f"{target_id}: URL de metadado oficial inválida")
        else:
            if metadata_url is not None or metadata_state != "unresolved":
                fail(f"{target_id}: metadado do pacote completo permanece não resolvido")

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
    if not isinstance(rules, list) or len(rules) < 6:
        fail("regras de normalização devem ser explícitas")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for term in ("catálogo", "metadado", "download", "uuid", "checksums", "verified", "inspected"):
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

    print("OK: contrato PRODES distingue metadados verificados de endpoints e ativos não resolvidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
