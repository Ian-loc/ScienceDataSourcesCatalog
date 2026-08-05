#!/usr/bin/env python3
"""Validate the pre-promotion resolution contract for the PRODES family."""
from __future__ import annotations

import json
from pathlib import Path

PATH = Path("database/mappings/prodes_product_targets.json")
EXPECTED_TYPES = {"map_series", "indicator_series"}
REQUIRED_TARGET_FIELDS = {
    "candidate_stable_id",
    "name_pt",
    "product_type",
    "scientific_object",
    "support_type",
    "required_evidence_before_promotion",
    "unknown_fields",
    "non_representations",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("family_stable_id") != "PF000001":
        fail("família PRODES deve permanecer PF000001")
    if data.get("resolution_status") != "pre_promotion":
        fail("contrato deve permanecer em pre_promotion")
    if data.get("promotion_authorized") is not False:
        fail("promoção não pode estar autorizada neste estágio")

    targets = data.get("targets")
    if not isinstance(targets, list) or len(targets) != 2:
        fail("devem existir exatamente dois produtos-alvo iniciais")

    ids: set[str] = set()
    types: set[str] = set()
    for target in targets:
        missing = REQUIRED_TARGET_FIELDS - set(target)
        if missing:
            fail(f"campos ausentes em produto-alvo: {sorted(missing)}")
        candidate_id = target["candidate_stable_id"]
        if candidate_id in ids:
            fail(f"candidate_stable_id duplicado: {candidate_id}")
        ids.add(candidate_id)
        types.add(target["product_type"])
        for field in (
            "required_evidence_before_promotion",
            "unknown_fields",
            "non_representations",
        ):
            value = target[field]
            if not isinstance(value, list) or not value:
                fail(f"{candidate_id}: {field} deve ser lista não vazia")

    if types != EXPECTED_TYPES:
        fail(f"tipos esperados {sorted(EXPECTED_TYPES)}, encontrados {sorted(types)}")

    serialized = PATH.read_text(encoding="utf-8")
    forbidden = ("release_id\"", "promotion_authorized\": true")
    for token in forbidden:
        if token in serialized:
            fail(f"promoção prematura detectada: {token}")

    print("OK: PRODES resolvido em mapa anual e taxa anual, sem promoção prematura")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
