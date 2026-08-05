#!/usr/bin/env python3
"""Validate the complementary operational evidence contract for PRODES."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_operational_evidence_2026.json")
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
        fail("evidência operacional deve permanecer vinculada a PF000001")
    if data.get("status") != "pre_promotion_evidence":
        fail("evidência operacional deve permanecer em pre_promotion_evidence")
    if data.get("promotion_authorized") is not False:
        fail("evidência complementar não pode autorizar promoção")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")

    sources = data.get("official_evidence")
    if not isinstance(sources, list) or len(sources) < 2:
        fail("ao menos duas fontes oficiais operacionais são obrigatórias")

    evidence_ids: set[str] = set()
    for source in sources:
        evidence_id = source.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id:
            fail("toda fonte deve possuir evidence_id")
        if evidence_id in evidence_ids:
            fail(f"evidence_id duplicado: {evidence_id}")
        evidence_ids.add(evidence_id)

        url = source.get("url")
        parsed = urlparse(url) if isinstance(url, str) else None
        host = (parsed.hostname or "").lower() if parsed else ""
        if not parsed or parsed.scheme != "https" or not host.endswith("inpe.br"):
            fail(f"{evidence_id}: URL HTTPS oficial do INPE obrigatória")
        if source.get("observed_state") != "active":
            fail(f"{evidence_id}: estado observado deve ser active")
        if not isinstance(source.get("supports"), list) or not source["supports"]:
            fail(f"{evidence_id}: supports deve ser lista não vazia")
        if not isinstance(source.get("limitations"), list) or not source["limitations"]:
            fail(f"{evidence_id}: limitations deve ser lista não vazia")

    findings = data.get("resolved_operational_findings")
    if not isinstance(findings, dict):
        fail("resolved_operational_findings deve ser objeto")

    distributions = findings.get("map_distribution_families")
    if not isinstance(distributions, list) or len(distributions) != 4:
        fail("quatro famílias operacionais de distribuição devem ser registradas")
    roles = {item.get("role") for item in distributions}
    if roles != EXPECTED_ROLES:
        fail(f"papéis de distribuição inesperados: {sorted(roles)}")
    formats = {item.get("format") for item in distributions}
    if formats != {"Shapefile", "GeoTIFF", "GeoPackage"}:
        fail(f"formatos operacionais inesperados: {sorted(formats)}")
    for item in distributions:
        cited = item.get("evidence_ids")
        if not isinstance(cited, list) or not cited or set(cited) - evidence_ids:
            fail(f"{item.get('role')}: evidência ausente ou inválida")

    lifecycle = findings.get("rate_result_lifecycle")
    if not isinstance(lifecycle, dict):
        fail("ciclo de vida da taxa deve ser objeto")
    if lifecycle.get("ordered_states") != ["preliminary_estimate", "consolidated_rate"]:
        fail("ordem deve preservar estimativa preliminar antes da taxa consolidada")
    if set(lifecycle.get("evidence_ids", [])) - evidence_ids:
        fail("ciclo de vida referencia evidência inexistente")

    cloud = findings.get("cloud_handling_scope")
    if not isinstance(cloud, dict):
        fail("escopo de nuvens deve ser objeto")
    unresolved_cloud = str(cloud.get("not_resolved", "")).casefold()
    if "áreas não observadas" not in unresolved_cloud:
        fail("ajuste vigente para áreas não observadas deve permanecer não resolvido")

    unresolved = data.get("unresolved_before_promotion")
    if not isinstance(unresolved, list) or len(unresolved) < 6:
        fail("pendências pré-promoção devem permanecer explícitas")
    unresolved_text = " ".join(str(item) for item in unresolved).casefold()
    required_terms = ("algoritmo", "áreas não observadas", "release", "licença", "citação")
    for term in required_terms:
        if term not in unresolved_text:
            fail(f"pendência obrigatória ausente: {term}")

    prohibited = data.get("prohibited_inferences")
    if not isinstance(prohibited, list) or len(prohibited) < 4:
        fail("inferências proibidas devem ser explicitadas")

    serialized = PATH.read_text(encoding="utf-8")
    forbidden_tokens = ('"promotion_authorized": true', '"release_id"', '"algorithm_version"')
    for token in forbidden_tokens:
        if token in serialized:
            fail(f"promoção ou precisão prematura detectada: {token}")

    subprocess.run(
        [sys.executable, "scripts/validate_prodes_catalog_integrity_guard.py"],
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/validate_prodes_geonetwork_metadata_registry.py"],
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/validate_prodes_asset_endpoint_contract.py"],
        check=True,
    )
    print("OK: evidência operacional PRODES validada sem promoção ou extrapolação metodológica")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
