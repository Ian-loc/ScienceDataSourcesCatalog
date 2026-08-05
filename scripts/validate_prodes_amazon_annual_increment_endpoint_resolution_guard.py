#!/usr/bin/env python3
"""Validate endpoint-resolution safeguards for the PRODES Amazon annual increment asset."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_annual_increment_endpoint_resolution_guard_2026.json")
EXPECTED_UUID = "b75b83db-8026-43f9-9537-ee1dfa308158"


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

    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado à família PF000001")
    if data.get("target_id") != "PRODES-ASSET-ANNUAL-INCREMENT-SHP":
        fail("alvo operacional inesperado")
    if data.get("scientific_target") != "PD-PRODES-AMZ-ANNUAL-MAP":
        fail("alvo científico inesperado")
    if data.get("status") != "metadata_resolved_direct_endpoint_blocked":
        fail("estado de resolução deve permanecer explicitamente bloqueado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")
    if data.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado foi alterado")
    if not official_https(data.get("metadata_url")) or EXPECTED_UUID not in data["metadata_url"]:
        fail("metadata_url oficial inválida")
    if not official_https(data.get("catalog_url")):
        fail("catalog_url deve apontar para fonte oficial do INPE")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in ("catalog_presence", "metadata_identifier_verified", "metadata_ui_url_resolved"):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "metadata_api_response_verified",
        "direct_download_url_verified",
        "redirect_chain_verified",
        "http_asset_status_verified",
        "asset_bytes_inspected",
        "checksum_computed",
        "release_resolved",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    attempts = data.get("resolution_attempts")
    if not isinstance(attempts, list) or len(attempts) < 3:
        fail("tentativas de resolução insuficientes")
    roles = {item.get("endpoint_role") for item in attempts if isinstance(item, dict)}
    required_roles = {"geonetwork_record_api", "metadata_user_interface", "official_download_catalog"}
    if not required_roles.issubset(roles):
        fail("papéis de tentativa incompletos")
    if not any("500" in str(item.get("observed_result", "")) for item in attempts if isinstance(item, dict)):
        fail("falha HTTP 500 observada deve permanecer registrada")
    for attempt in attempts:
        if not isinstance(attempt, dict) or not official_https(attempt.get("endpoint")):
            fail("toda tentativa deve usar endpoint HTTPS oficial")
        if attempt.get("canonical_asset_evidence") is not False:
            fail("tentativa não pode ser tratada como evidência canônica do ativo")

    assessment = data.get("assessment")
    if not isinstance(assessment, dict):
        fail("assessment deve ser objeto")
    if assessment.get("blocker_type") != "external_endpoint_resolution":
        fail("tipo de bloqueio inesperado")
    if assessment.get("severity") != "medium" or assessment.get("state") != "accepted_limitation":
        fail("severidade ou estado da limitação divergente")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 8:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("uuid", "http 500", "adivinhação", "endpoint_state", "asset_state", "release_id"):
        if token.casefold() not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    endpoint_required = data.get("required_before_endpoint_resolution")
    asset_required = data.get("required_before_asset_promotion")
    if not isinstance(endpoint_required, list) or len(endpoint_required) < 7:
        fail("requisitos de resolução do endpoint incompletos")
    if not isinstance(asset_required, list) or len(asset_required) < 7:
        fail("requisitos de promoção do ativo incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
        '"release_resolved": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: endpoint PRODES anual permanece não resolvido sem inferir URL, bytes ou release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
