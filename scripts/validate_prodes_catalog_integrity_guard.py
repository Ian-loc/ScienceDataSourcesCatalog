#!/usr/bin/env python3
"""Validate the PRODES catalogue-integrity guard before endpoint resolution."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_catalog_integrity_guard_2026.json")
OFFICIAL_SUFFIX = "inpe.br"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_https(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith(OFFICIAL_SUFFIX)


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado a PF000001")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")

    affected = data.get("affected_entrypoint")
    if not isinstance(affected, dict):
        fail("affected_entrypoint deve ser objeto")
    if not official_https(str(affected.get("url", ""))):
        fail("entrypoint afetado deve continuar sendo URL HTTPS oficial do INPE")
    if affected.get("role") != "download_catalog":
        fail("entrypoint afetado deve permanecer download_catalog")
    if affected.get("integrity_state") != "suspended_for_automatic_extraction":
        fail("extração automática deve permanecer suspensa")
    if affected.get("may_confirm_catalog_labels") is not True:
        fail("rótulos visuais podem ser usados apenas como confirmação limitada")
    for key in ("may_supply_direct_asset_urls", "may_supply_license_or_citation"):
        if affected.get(key) is not False:
            fail(f"{key} deve permanecer falso")
    external_domain = str(affected.get("observed_external_domain", ""))
    if not external_domain or external_domain.endswith(OFFICIAL_SUFFIX):
        fail("domínio externo observado deve permanecer explícito e não oficial")

    alternatives = data.get("trusted_alternative_entrypoints")
    if not isinstance(alternatives, list) or len(alternatives) < 2:
        fail("ao menos GeoNetwork e índice de geosserviços são obrigatórios")
    roles = set()
    for item in alternatives:
        url = str(item.get("url", ""))
        if not official_https(url):
            fail(f"alternativa não oficial: {url}")
        role = item.get("role")
        roles.add(role)
        if item.get("verification_state") != "official_entrypoint_confirmed":
            fail(f"{role}: estado de verificação inesperado")
        if not (item.get("per_record_verification_required") is True or item.get("per_layer_verification_required") is True):
            fail(f"{role}: verificação específica obrigatória ausente")
    if roles != {"metadata_catalog", "geoservices_index"}:
        fail(f"papéis alternativos incompletos: {sorted(roles)}")

    controls = data.get("mandatory_controls")
    if not isinstance(controls, list) or len(controls) < 6:
        fail("controles obrigatórios insuficientes")
    controls_text = " ".join(str(item) for item in controls).casefold()
    for term in ("não seguir", "geonetwork", "endpoint", "checksum", "unresolved", "not_inspected"):
        if term not in controls_text:
            fail(f"controle obrigatório ausente: {term}")

    criteria = data.get("resumption_criteria")
    if not isinstance(criteria, list) or len(criteria) < 4:
        fail("critérios de retomada insuficientes")
    criteria_text = " ".join(str(item) for item in criteria).casefold()
    for term in ("removido", "inspeção", "geonetwork", "http"):
        if term not in criteria_text:
            fail(f"critério de retomada ausente: {term}")

    print("OK: portão de integridade do catálogo PRODES mantém extração automática suspensa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
