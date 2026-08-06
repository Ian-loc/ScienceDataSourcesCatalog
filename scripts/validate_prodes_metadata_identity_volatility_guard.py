#!/usr/bin/env python3
"""Validate the PRODES metadata identity volatility guard."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_metadata_identity_volatility_guard_2026.json")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
EXPECTED_ROLES = {
    "accumulated_suppression_mask_vector",
    "annual_increment_vector",
    "hydrography_reference_vector",
    "annual_residue_vector",
    "nonforest_domain_mask_vector",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado a PF000001")
    if data.get("status") != "observed_metadata_identity_conflict_pre_promotion":
        fail("estado de conflito pré-promoção obrigatório")
    if data.get("promotion_authorized") is not False:
        fail("conflito de identidade não pode autorizar promoção")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")

    source = data.get("source")
    if not isinstance(source, dict):
        fail("source deve ser objeto")
    parsed = urlparse(str(source.get("url", "")))
    if parsed.scheme != "https" or not (parsed.hostname or "").endswith("inpe.br"):
        fail("fonte deve usar URL HTTPS oficial do INPE")
    if source.get("role") != "metadata_catalog_search":
        fail("papel da fonte deve ser metadata_catalog_search")

    conflicts = data.get("conflicts")
    if not isinstance(conflicts, list) or len(conflicts) != 5:
        fail("exatamente cinco conflitos observados são obrigatórios")
    roles = {item.get("distribution_role") for item in conflicts}
    if roles != EXPECTED_ROLES:
        fail(f"papéis conflitantes inesperados: {sorted(roles)}")

    all_uuids: set[str] = set()
    for item in conflicts:
        registered = item.get("registered_uuid")
        observed = item.get("currently_observed_uuid")
        for label, value in (("registered_uuid", registered), ("currently_observed_uuid", observed)):
            if not isinstance(value, str) or not UUID_RE.fullmatch(value):
                fail(f"{item.get('distribution_role')}: {label} inválido")
            if value in all_uuids:
                fail(f"UUID repetido entre conflitos: {value}")
            all_uuids.add(value)
        if registered == observed:
            fail(f"{item.get('distribution_role')}: conflito exige UUIDs distintos")
        if item.get("identity_state") != "multiple_metadata_records_observed":
            fail(f"{item.get('distribution_role')}: identity_state inválido")
        if item.get("resolution_state") != "unresolved":
            fail(f"{item.get('distribution_role')}: conflito não pode ser resolvido prematuramente")

    required = data.get("required_resolution_evidence")
    if not isinstance(required, list) or len(required) < 6:
        fail("evidência mínima de resolução deve permanecer explícita")
    required_text = " ".join(str(item) for item in required).casefold()
    for term in ("datas", "links", "substituição", "checksum", "decisão curatorial"):
        if term not in required_text:
            fail(f"evidência de resolução ausente: {term}")

    prohibited = data.get("prohibited_inferences")
    if not isinstance(prohibited, list) or len(prohibited) < 5:
        fail("inferências proibidas devem permanecer explícitas")
    prohibited_text = " ".join(str(item) for item in prohibited).casefold()
    for term in ("substituir automaticamente", "release", "fundir", "canônica", "excluir"):
        if term not in prohibited_text:
            fail(f"proteção semântica ausente: {term}")

    serialized = PATH.read_text(encoding="utf-8")
    for token in ('"promotion_authorized": true', '"resolution_state": "resolved"'):
        if token in serialized:
            fail(f"resolução ou promoção prematura detectada: {token}")

    print("OK: volatilidade de identidade dos metadados PRODES protegida sem promoção prematura")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
