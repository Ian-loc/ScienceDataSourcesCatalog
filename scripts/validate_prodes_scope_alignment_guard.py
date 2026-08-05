#!/usr/bin/env python3
"""Block linkage between PRODES Amazônia-biome metadata and Amazônia Legal targets."""
from __future__ import annotations

import json
from pathlib import Path

GUARD_PATH = Path("database/mappings/prodes_scope_alignment_guard_2026.json")
TARGET_PATH = Path("database/mappings/prodes_product_targets.json")
REGISTRY_PATH = Path("database/mappings/prodes_geonetwork_metadata_registry_2026.json")


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    for path in (GUARD_PATH, TARGET_PATH, REGISTRY_PATH):
        if not path.is_file():
            fail(f"arquivo ausente: {path}")

    guard = json.loads(GUARD_PATH.read_text(encoding="utf-8"))
    targets = json.loads(TARGET_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    if guard.get("family_stable_id") != "PF000001":
        fail("portão territorial deve permanecer vinculado a PF000001")
    if guard.get("status") != "scope_mismatch_blocked":
        fail("divergência territorial deve permanecer explicitamente bloqueada")
    if guard.get("promotion_authorized") is not False:
        fail("portão territorial não pode autorizar promoção")

    target_domains = {
        target.get("resolved_fields", {}).get("monitoring_domain")
        for target in targets.get("targets", [])
    }
    if target_domains != {"Amazônia Legal"}:
        fail("produtos-alvo atuais devem declarar explicitamente Amazônia Legal")

    metadata = guard.get("metadata_registry") or {}
    if metadata.get("interpreted_domain") != "Bioma Amazônia":
        fail("registros atuais devem permanecer identificados como Bioma Amazônia")
    if metadata.get("compatibility_with_target_contract") is not False:
        fail("registros do Bioma Amazônia não podem ser vinculados aos alvos da Amazônia Legal")

    packages = guard.get("distinct_official_packages") or []
    scopes = {package.get("scope") for package in packages}
    if scopes != {"Bioma Amazônia", "Amazônia Legal"}:
        fail("os dois domínios oficiais distintos devem estar representados")

    package_uuids = {package.get("example_increment_uuid") for package in packages}
    if package_uuids != {
        "b75b83db-8026-43f9-9537-ee1dfa308158",
        "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830",
    }:
        fail("UUIDs exemplares dos dois pacotes divergiram")

    registry_uuids = {record.get("uuid") for record in registry.get("records", [])}
    if "b75b83db-8026-43f9-9537-ee1dfa308158" not in registry_uuids:
        fail("registro do incremento do Bioma Amazônia ausente")
    if "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830" in registry_uuids:
        fail("registro da Amazônia Legal não deve ser misturado ao registro atual do Bioma Amazônia")

    prohibited = " ".join(str(item) for item in guard.get("prohibited_inferences", [])).casefold()
    for term in ("sinônimos", "uuid", "endpoint", "release", "amazônia legal"):
        if term not in prohibited:
            fail(f"inferência territorial proibida ausente: {term}")

    residual = " ".join(str(item) for item in guard.get("residual_work", [])).casefold()
    for term in ("uuid", "amazônia legal", "ambiguidade", "checksums"):
        if term not in residual:
            fail(f"trabalho residual obrigatório ausente: {term}")

    print("OK: PRODES Bioma Amazônia separado dos produtos-alvo da Amazônia Legal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
