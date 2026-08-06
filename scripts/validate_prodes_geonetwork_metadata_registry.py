#!/usr/bin/env python3
"""Validate verified GeoNetwork metadata identifiers for PRODES before asset promotion."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_geonetwork_metadata_registry_2026.json")
SCOPE_VALIDATOR = Path("scripts/validate_prodes_scope_alignment_guard.py")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
EXPECTED_IDS = {
    "b75b83db-8026-43f9-9537-ee1dfa308158",
    "5f5cfb4c-e207-4932-9c93-2d51cea8adbc",
    "c6748fdf-a18e-41b9-a523-ea14bae92602",
    "215be904-3828-41a9-a1bd-c7daa0133944",
    "a8208a12-679b-432a-8a47-fc42d2279f9a",
    "00a728cb-8577-458a-9c38-082c1f3bca9e",
    "63751b72-3e6a-4d15-8fc0-740e57bbc346",
    "1df78632-68e7-4e91-bca0-25305d3f831e",
    "87fb6a32-01c1-4421-b7d0-a93568e1b079",
    "bed1276c-aa3d-4f5b-b560-1879617ef13d",
}
EXPECTED_ROLES = {
    "annual_increment_vector",
    "small_polygon_increment_vector",
    "accumulated_suppression_mask_vector",
    "accumulated_suppression_nonforest_mask_vector",
    "annual_increment_nonforest_vector",
    "annual_residue_vector",
    "annual_residue_nonforest_vector",
    "hydrography_reference_vector",
    "hydrography_nonforest_reference_vector",
    "nonforest_domain_mask_vector",
}
ALLOWED_DOMAINS = {"forest_domain", "nonforest_domain"}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("family_stable_id") != "PF000001":
        fail("registro deve permanecer vinculado a PF000001")
    if data.get("status") != "verified_metadata_identifiers_pre_promotion":
        fail("estado deve permanecer pré-promoção")
    if data.get("promotion_authorized") is not False:
        fail("registro de metadados não pode autorizar promoção")
    catalog = data.get("catalog") or {}
    if catalog.get("role") != "metadata_catalog":
        fail("GeoNetwork deve ser classificado como catálogo de metadados")
    host = (urlparse(str(catalog.get("base_url", ""))).hostname or "").lower()
    if not host.endswith("inpe.br"):
        fail("catálogo deve permanecer em domínio oficial do INPE")

    records = data.get("records")
    if not isinstance(records, list) or len(records) != 10:
        fail("dez registros específicos são obrigatórios para o pacote PRODES Amazônia documentado")
    uuids: set[str] = set()
    record_ids: set[str] = set()
    roles: set[str] = set()
    domains: set[str] = set()
    nonforest_roles: set[str] = set()
    for record in records:
        record_id = record.get("record_id")
        uuid = record.get("uuid")
        if not isinstance(record_id, str) or not record_id or record_id in record_ids:
            fail("record_id ausente ou duplicado")
        record_ids.add(record_id)
        if not isinstance(uuid, str) or not UUID_RE.match(uuid) or uuid in uuids:
            fail(f"{record_id}: UUID inválido ou duplicado")
        uuids.add(uuid)
        metadata_url = str(record.get("metadata_url", ""))
        parsed = urlparse(metadata_url)
        if parsed.scheme != "https" or not (parsed.hostname or "").endswith("inpe.br"):
            fail(f"{record_id}: URL oficial HTTPS obrigatória")
        if uuid not in metadata_url:
            fail(f"{record_id}: URL deve conter o UUID declarado")
        if record.get("verification_state") != "metadata_identifier_verified":
            fail(f"{record_id}: estado de verificação inesperado")
        if record.get("asset_state") != "not_downloaded":
            fail(f"{record_id}: ativo não pode ser considerado inspecionado")
        for field in ("direct_download_url", "checksum_sha256", "release_id"):
            if record.get(field) is not None:
                fail(f"{record_id}: {field} deve permanecer nulo antes da inspeção")
        formats = record.get("format_context")
        if not isinstance(formats, list) or not formats:
            fail(f"{record_id}: contexto de formato ausente")
        role = record.get("expected_distribution_role")
        if role not in EXPECTED_ROLES or role in roles:
            fail(f"{record_id}: papel de distribuição ausente, inesperado ou duplicado")
        roles.add(role)
        domain = record.get("domain_context")
        if domain not in ALLOWED_DOMAINS:
            fail(f"{record_id}: domínio cartográfico inválido")
        domains.add(domain)
        if domain == "nonforest_domain":
            nonforest_roles.add(role)

    if uuids != EXPECTED_IDS:
        fail("conjunto de UUIDs diverge do registro verificado")
    if roles != EXPECTED_ROLES:
        fail("papéis de distribuição divergem do contrato esperado")
    if domains != ALLOWED_DOMAINS:
        fail("domínios florestal e não floresta devem estar representados")
    required_nonforest_roles = {
        "accumulated_suppression_nonforest_mask_vector",
        "annual_increment_nonforest_vector",
        "annual_residue_nonforest_vector",
        "hydrography_nonforest_reference_vector",
        "nonforest_domain_mask_vector",
    }
    if nonforest_roles != required_nonforest_roles:
        fail("componentes do domínio não floresta estão incompletos ou fundidos incorretamente")

    unresolved = " ".join(str(x) for x in data.get("unresolved_before_asset_promotion", [])).casefold()
    for term in ("checksum", "crs", "geometr", "licença", "citação", "release"):
        if term not in unresolved:
            fail(f"pendência obrigatória ausente: {term}")
    prohibited = " ".join(str(x) for x in data.get("prohibited_inferences", [])).casefold()
    for term in ("uuid", "release", "metadado", "ativo", "geopackage", "não floresta"):
        if term not in prohibited:
            fail(f"inferência proibida ausente: {term}")

    if not SCOPE_VALIDATOR.is_file():
        fail(f"validador territorial ausente: {SCOPE_VALIDATOR}")
    subprocess.run([sys.executable, str(SCOPE_VALIDATOR)], check=True)

    print("OK: dez UUIDs GeoNetwork PRODES registrados com separação dos domínios florestal e não floresta")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
