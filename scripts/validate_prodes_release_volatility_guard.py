#!/usr/bin/env python3
"""Validate the PRODES release-volatility guard."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_release_volatility_guard_2026.json")
EXPECTED_ROLES = {
    "annual_increment_vector",
    "small_polygon_increment_vector",
    "complete_map_raster",
    "complete_map_vector",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado a PF000001")
    if data.get("status") != "observed_catalog_state_pre_promotion":
        fail("estado deve permanecer pre_promotion")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone inválido")

    source = data.get("source", {})
    parsed = urlparse(str(source.get("url", "")))
    if parsed.scheme != "https" or not (parsed.hostname or "").endswith("inpe.br"):
        fail("fonte deve ser URL HTTPS oficial do INPE")
    if source.get("role") != "download_catalog":
        fail("fonte deve permanecer classificada como download_catalog")

    observations = data.get("observations")
    if not isinstance(observations, list) or len(observations) != 4:
        fail("quatro distribuições observadas são obrigatórias")
    roles = {item.get("distribution_role") for item in observations}
    if roles != EXPECTED_ROLES:
        fail(f"papéis inesperados: {sorted(roles)}")
    dates = set()
    for item in observations:
        if item.get("release_identity_state") != "unresolved":
            fail("identidade de release deve permanecer não resolvida")
        if item.get("direct_asset_state") != "not_verified":
            fail("ativo direto deve permanecer não verificado")
        date = item.get("catalog_last_update")
        if not isinstance(date, str) or len(date) != 10:
            fail("data de catálogo deve usar YYYY-MM-DD")
        dates.add(date)
    if len(dates) < 2:
        fail("portão deve preservar datas operacionais distintas")

    required = " ".join(data.get("required_before_release_promotion", [])).casefold()
    for term in ("checksum", "release", "url direta", "licença", "citação"):
        if term not in required:
            fail(f"requisito pré-promoção ausente: {term}")

    prohibited = " ".join(data.get("prohibited_inferences", [])).casefold()
    for term in ("release_id", "data única", "catálogo agregador", "outros biomas"):
        if term not in prohibited:
            fail(f"inferência proibida ausente: {term}")

    print("OK: volatilidade operacional PRODES preservada sem release ou ativo inventado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
