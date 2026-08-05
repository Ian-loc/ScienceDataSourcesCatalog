#!/usr/bin/env python3
"""Validate the PRODES Amazon GeoPackage composition guard."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from validate_prodes_amazon_annual_increment_catalog_snapshot_guard import main as validate_annual_increment_snapshot
from validate_prodes_amazon_annual_increment_endpoint_resolution_guard import main as validate_annual_increment_endpoint
from validate_prodes_amazon_non_forest_increment_metadata_guard import main as validate_non_forest_increment

PATH = Path("database/mappings/prodes_amazon_geopackage_composition_guard_2026.json")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
EXPECTED_ROLES = {
    "accumulated_native_vegetation_suppression_mask",
    "accumulated_non_forest_suppression_mask",
    "annual_deforestation_increment",
    "annual_non_forest_suppression_increment",
    "annual_deforestation_increment_1_to_6_25_ha",
    "annual_native_vegetation_suppression_residual",
    "annual_non_forest_suppression_residual",
    "hydrography",
    "non_forest_hydrography",
    "non_forest_mask",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000001":
        fail("contrato deve permanecer vinculado a PF000001")
    if data.get("scientific_target") != "PD-PRODES-AMZ-ANNUAL-MAP":
        fail("alvo científico inesperado")
    if data.get("status") != "catalog_package_composition_verified":
        fail("status inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("o contrato não pode autorizar promoção")

    evidence = data.get("official_catalog_evidence")
    if not isinstance(evidence, dict):
        fail("official_catalog_evidence deve ser objeto")
    parsed = urlparse(str(evidence.get("catalog_url", "")))
    if parsed.scheme != "https" or not (parsed.hostname or "").endswith("inpe.br"):
        fail("catálogo deve usar URL HTTPS oficial do INPE")
    if evidence.get("record_title") != "GeoPackage - PRODES Amazônia":
        fail("título oficial divergente")
    if evidence.get("format") != "GeoPackage":
        fail("formato deve permanecer GeoPackage")
    if evidence.get("representation_type") != "Vector":
        fail("tipo de representação deve permanecer Vector")
    if evidence.get("direct_download_url") is not None:
        fail("URL direta não pode ser preenchida sem verificação")
    if evidence.get("checksum") is not None:
        fail("checksum não pode ser preenchido sem recuperação dos bytes")
    if evidence.get("asset_inspected") is not False:
        fail("ativo ainda não foi inspecionado")

    components = data.get("declared_components")
    if not isinstance(components, list) or len(components) != 10:
        fail("dez componentes declarados são obrigatórios")
    roles: set[str] = set()
    uuids: set[str] = set()
    for component in components:
        if not isinstance(component, dict):
            fail("componente deve ser objeto")
        role = component.get("role")
        uuid = component.get("metadata_uuid")
        if role not in EXPECTED_ROLES:
            fail(f"papel inesperado: {role}")
        if role in roles:
            fail(f"papel duplicado: {role}")
        roles.add(role)
        if not isinstance(uuid, str) or not UUID_RE.fullmatch(uuid):
            fail(f"UUID inválido para {role}")
        if uuid in uuids:
            fail(f"UUID duplicado: {uuid}")
        uuids.add(uuid)
    if roles != EXPECTED_ROLES:
        fail("conjunto de componentes incompleto")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 7:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for term in ("distribuição", "uuid", "bytes", "url direta", "crs", "checksum", "release", "ativo inspecionado"):
        if term not in rules_text:
            fail(f"regra obrigatória ausente: {term}")

    required = data.get("required_before_asset_promotion")
    if not isinstance(required, list) or len(required) < 7:
        fail("requisitos de promoção insuficientes")
    required_text = " ".join(str(item) for item in required).casefold()
    for term in ("url direta", "checksum", "crs", "atributos", "territorial", "temporal", "licença", "release"):
        if term not in required_text:
            fail(f"requisito obrigatório ausente: {term}")

    serialized = PATH.read_text(encoding="utf-8")
    for token in ('"promotion_authorized": true', '"asset_inspected": true'):
        if token in serialized:
            fail(f"promoção prematura detectada: {token}")

    validate_annual_increment_snapshot()
    validate_annual_increment_endpoint()
    validate_non_forest_increment()
    print("OK: pacote GeoPackage PRODES Amazônia preserva composição e fronteiras científicas sem promoção prematura")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
