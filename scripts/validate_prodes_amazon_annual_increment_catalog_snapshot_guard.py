#!/usr/bin/env python3
"""Validate catalog-snapshot volatility safeguards for PRODES Amazônia annual increments."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_annual_increment_catalog_snapshot_guard_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado à família PF000001")
    if data.get("target_id") != "PRODES-ASSET-ANNUAL-INCREMENT-SHP":
        fail("portão deve proteger o alvo anual Shapefile")
    if data.get("scientific_target") != "PD-PRODES-AMZ-ANNUAL-MAP":
        fail("alvo científico inesperado")
    if data.get("status") != "catalog_snapshot_volatility_detected":
        fail("estado de volatilidade do catálogo deve permanecer explícito")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")

    uuid = data.get("metadata_identifier")
    if uuid != "b75b83db-8026-43f9-9537-ee1dfa308158":
        fail("UUID de metadado do incremento anual foi alterado")
    metadata_url = data.get("metadata_url")
    if not isinstance(metadata_url, str) or uuid not in metadata_url:
        fail("metadata_url deve preservar o UUID verificado")

    facts = data.get("verified_facts")
    if not isinstance(facts, dict):
        fail("verified_facts deve ser objeto")
    required_false = (
        "direct_download_url_verified",
        "asset_bytes_inspected",
        "checksum_computed",
        "release_resolved",
    )
    for field in required_false:
        if facts.get(field) is not False:
            fail(f"{field} deve permanecer false")
    if facts.get("catalog_presence") is not True:
        fail("presença no catálogo deve permanecer confirmada")

    snapshots = data.get("official_catalog_snapshots")
    if not isinstance(snapshots, list) or len(snapshots) < 2:
        fail("devem existir ao menos dois snapshots oficiais")
    dates: set[str] = set()
    hosts: set[str] = set()
    for snapshot in snapshots:
        url = snapshot.get("url")
        if not isinstance(url, str) or urlparse(url).scheme != "https":
            fail("snapshot deve usar URL HTTPS")
        host = (urlparse(url).hostname or "").lower()
        if not host.endswith("terrabrasilis.dpi.inpe.br"):
            fail(f"snapshot fora do domínio oficial: {host}")
        hosts.add(host)
        date = snapshot.get("observed_catalog_date")
        if not isinstance(date, str) or len(date) != 10:
            fail("snapshot deve registrar data ISO")
        dates.add(date)
        if snapshot.get("canonical_for_release") is not False:
            fail("snapshot de catálogo não pode ser canônico para release")

    if len(dates) < 2:
        fail("o portão deve preservar a divergência entre datas observadas")
    if hosts != {"terrabrasilis.dpi.inpe.br", "www.terrabrasilis.dpi.inpe.br"}:
        fail("o portão deve preservar a comparação entre hosts oficial com e sem www")

    assessment = data.get("catalog_snapshot_assessment")
    if not isinstance(assessment, dict) or assessment.get("dates_conflict") is not True:
        fail("a divergência de datas deve permanecer registrada")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 6:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(rules).casefold()
    for token in ("release", "uuid", "endpoint_state", "asset_state"):
        if token.casefold() not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    required = data.get("required_before_resolution")
    if not isinstance(required, list) or len(required) < 10:
        fail("checagens diretas antes da resolução estão incompletas")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in ('"promotion_authorized": true', '"direct_download_url_verified": true', '"asset_bytes_inspected": true'):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: volatilidade dos snapshots PRODES preservada sem promover data, endpoint, bytes ou release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
