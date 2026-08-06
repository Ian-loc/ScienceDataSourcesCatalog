#!/usr/bin/env python3
"""Validate the DETER Cerrado metadata identifier ambiguity boundary."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_metadata_identifier_ambiguity_guard_2026.json")
EXPECTED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


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

    if data.get("family_stable_id") != "PF000003":
        fail("família inesperada")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("metadata_identifier_under_review") != EXPECTED_UUID:
        fail("UUID sob revisão divergente")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone divergente")
    if data.get("promotion_authorized") is not False:
        fail("ambiguidade não pode autorizar promoção")
    if data.get("status") != "official_index_context_conflict_detected_identifier_not_stable_for_product_or_release":
        fail("status curatorial inesperado")

    contexts = data.get("conflicting_official_contexts")
    if not isinstance(contexts, list) or len(contexts) != 2:
        fail("dois contextos oficiais conflitantes são obrigatórios")
    roles = {item.get("role") for item in contexts if isinstance(item, dict)}
    if roles != {"deter_cerrado_metadata_reference", "prodes_amazon_geopackage_component_reference"}:
        fail("papéis dos contextos conflitantes divergentes")
    for item in contexts:
        if not official_https(item.get("url")):
            fail("contexto deve usar URL oficial HTTPS do INPE")
        if not str(item.get("observed_claim", "")).strip():
            fail("contexto sem afirmação observada")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    if state.get("same_uuid_observed_in_distinct_official_contexts") is not True:
        fail("conflito contextual não registrado")
    if state.get("product_promotion_blocked_by_identifier_ambiguity") is not True:
        fail("ambiguidade deve bloquear promoção dependente")
    for key in (
        "direct_geonetwork_record_reconciled",
        "identifier_uniqueness_verified",
        "identifier_stability_verified",
        "identifier_is_product_id",
        "identifier_is_release_id",
        "identifier_is_asset_id",
        "metadata_record_current_subject_resolved",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro: {key}")

    interpretation = data.get("interpretation")
    if not isinstance(interpretation, dict):
        fail("interpretation deve ser objeto")
    if interpretation.get("collision_type") != "contextual_reference_conflict_or_indexing_drift":
        fail("tipo de conflito divergente")
    for key in ("compromise_claimed", "record_reuse_claimed", "root_cause_resolved"):
        if interpretation.get(key) is not False:
            fail(f"conclusão não sustentada: {key}")
    safe = str(interpretation.get("safe_conclusion", "")).casefold()
    for token in ("não pode", "sozinho", "produto", "release", "ativo", "geonetwork"):
        if token not in safe:
            fail(f"conclusão segura incompleta: {token}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 8:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("uuid", "produto", "release", "ativo", "comprometimento", "evidência", "inspeção direta"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    steps = data.get("required_resolution_steps")
    if not isinstance(steps, list) or len(steps) < 6:
        fail("passos de resolução insuficientes")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) != 2:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not official_https(item.get("url")):
            fail("evidência deve usar URL oficial HTTPS do INPE")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"identifier_stability_verified": true',
        '"identifier_is_product_id": true',
        '"identifier_is_release_id": true',
        '"identifier_is_asset_id": true',
        '"metadata_record_current_subject_resolved": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: UUID DETER Cerrado permanece ambíguo entre contextos oficiais e não identifica produto/release/ativo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
