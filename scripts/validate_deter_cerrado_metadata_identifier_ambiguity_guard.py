#!/usr/bin/env python3
"""Validate reconciliation of the published DETER Cerrado metadata reference drift."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_cerrado_metadata_identifier_ambiguity_guard_2026.json")
PUBLISHED_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"
CURRENT_UUID = "e6e15388-4ca9-49b9-aec9-03891339a35e"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def trusted_url(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    host = (parsed.hostname or "").casefold()
    return parsed.scheme == "https" and (host.endswith("inpe.br") or host == "doi.org")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("contract_version") != "1.1.0":
        fail("versão do contrato inesperada")
    if data.get("family_stable_id") != "PF000003":
        fail("família inesperada")
    if data.get("candidate_scientific_product_id") != "PD-DETER-CER-ALERTS":
        fail("produto candidato inesperado")
    if data.get("published_deter_citation_identifier") != PUBLISHED_UUID:
        fail("UUID publicado divergente")
    if data.get("current_deter_cerrado_metadata_identifier") != CURRENT_UUID:
        fail("UUID corrente divergente")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone divergente")
    if data.get("promotion_authorized") is not False:
        fail("reconciliação não autoriza promoção")
    if data.get("status") != "published_deter_citation_identifier_reconciled_as_prodes_reference_current_deter_record_resolved":
        fail("status curatorial inesperado")

    contexts = data.get("reconciled_official_contexts")
    if not isinstance(contexts, list) or len(contexts) != 3:
        fail("três contextos reconciliados são obrigatórios")
    roles = {item.get("role") for item in contexts if isinstance(item, dict)}
    expected_roles = {
        "published_deter_cerrado_citation_reference",
        "current_prodes_amazon_legal_increment_reference",
        "current_deter_cerrado_metadata_reference",
    }
    if roles != expected_roles:
        fail("papéis dos contextos reconciliados divergentes")
    for item in contexts:
        if not trusted_url(item.get("url")):
            fail("contexto deve usar URL confiável")
        if not str(item.get("observed_claim", "")).strip():
            fail("contexto sem afirmação observada")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "published_identifier_reused_in_distinct_official_contexts",
        "published_identifier_current_subject_resolved",
        "current_deter_cerrado_metadata_record_resolved",
        "current_deter_cerrado_metadata_identifier_matches_peer_reviewed_data_availability",
        "product_promotion_blocked_by_other_incomplete_components",
    ):
        if state.get(key) is not True:
            fail(f"reconciliação incompleta: {key}")
    if state.get("published_identifier_current_subject") != "incrementos no desmatamento do PRODES Amazônia Legal":
        fail("assunto corrente do UUID publicado divergente")
    for key in (
        "published_identifier_is_current_deter_cerrado_metadata_record",
        "current_deter_cerrado_identifier_is_product_id",
        "current_deter_cerrado_identifier_is_release_id",
        "current_deter_cerrado_identifier_is_asset_id",
        "product_promotion_blocked_by_identifier_ambiguity",
    ):
        if state.get(key) is not False:
            fail(f"estado de identificador incorreto: {key}")

    interpretation = data.get("interpretation")
    if not isinstance(interpretation, dict):
        fail("interpretation deve ser objeto")
    if interpretation.get("collision_type") != "published_citation_reference_drift":
        fail("tipo de divergência inesperado")
    for key in ("compromise_claimed", "intentional_record_reuse_claimed", "root_cause_of_drift_resolved"):
        if interpretation.get(key) is not False:
            fail(f"conclusão não sustentada: {key}")
    safe = str(interpretation.get("safe_conclusion", "")).casefold()
    for token in ("desatualizada", CURRENT_UUID, "produto", "release", "ativo"):
        if token.casefold() not in safe:
            fail(f"conclusão segura incompleta: {token}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 8:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (PUBLISHED_UUID, CURRENT_UUID, "prodes amazônia legal", "produto", "release", "ativo", "data real de acesso"):
        if token.casefold() not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) != 4:
        fail("quatro evidências são obrigatórias")
    for item in evidence:
        if not trusted_url(item.get("url")):
            fail("evidência deve usar URL confiável")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (PUBLISHED_UUID, CURRENT_UUID, "prodes amazônia legal", "deter cerrado"):
        if token.casefold() not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"published_identifier_is_current_deter_cerrado_metadata_record": true',
        '"current_deter_cerrado_identifier_is_product_id": true',
        '"current_deter_cerrado_identifier_is_release_id": true',
        '"current_deter_cerrado_identifier_is_asset_id": true',
        '"root_cause_of_drift_resolved": true',
    ):
        if forbidden in serialized:
            fail(f"conclusão prematura detectada: {forbidden}")

    print(
        "OK: referência publicada DETER Cerrado reconciliada como deriva; UUID corrente do "
        "metadado resolvido sem promover produto/release/ativo"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
