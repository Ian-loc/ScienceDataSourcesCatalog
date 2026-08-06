#!/usr/bin/env python3
"""Validate the boundary between forest and non-forest DETER Amazon distributions."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/deter_amazon_distribution_boundary_guard_2026.json")
FOREST_UUID = "f2153c4a-915b-48a6-8658-963bdce7366c"


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
    if data.get("family_stable_id") != "PF000002":
        fail("família DETER Amazônia inesperada")
    if data.get("parent_product_candidate_id") != "PD-DETER-AMZ-ALERTS":
        fail("produto-pai inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("contrato não pode autorizar promoção")

    distributions = data.get("distributions")
    if not isinstance(distributions, list) or len(distributions) != 2:
        fail("duas distribuições DETER Amazônia são obrigatórias")
    by_id = {item.get("candidate_distribution_id"): item for item in distributions if isinstance(item, dict)}
    forest = by_id.get("DD-DETER-AMZ-FOREST-ALERTS-SHP")
    nonforest = by_id.get("DD-DETER-AMZ-NON-FOREST-ALERTS-SHP")
    if not forest or not nonforest:
        fail("identidades das distribuições incompletas")
    if forest.get("metadata_identifier") != FOREST_UUID:
        fail("UUID florestal divergente")
    if nonforest.get("metadata_identifier") is not None:
        fail("UUID não florestal foi resolvido prematuramente")
    if forest.get("experimental") is not False or nonforest.get("experimental") is not True:
        fail("estado experimental foi transferido incorretamente")
    if forest.get("scientific_start") != "2016-08" or nonforest.get("scientific_start") != "2023-08":
        fail("fronteiras temporais divergentes")
    if forest.get("candidate_product_id") == nonforest.get("candidate_product_id"):
        fail("produtos candidatos não podem ser colapsados")

    forest_classes = set(forest.get("documented_classes", []))
    required_forest = {"DESMATAMENTO_CR", "DESMATAMENTO_VEG", "MINERACAO", "DEGRADACAO", "CICATRIZ_DE_QUEIMADA", "CS_DESORDENADO", "CS_GEOMETRICO"}
    if forest_classes != required_forest:
        fail("domínio de classes florestais divergente")
    nonforest_classes = set(nonforest.get("documented_classes", []))
    if nonforest_classes != {"SUPRESSAO_COM_SOLO_EXPOSTO", "SUPRESSAO_COM_VEGETACAO", "MINERACAO", "CICATRIZ_DE_QUEIMADA"}:
        fail("domínio de classes não florestais divergente")

    fq = forest.get("schema_qualifications", {})
    if fq.get("areatotkm_is_additive") is not False or fq.get("areamunkm_is_additive_for_municipal_summation") is not True:
        fail("regras de soma da distribuição florestal ausentes")
    if fq.get("publish_month_available_in_download_shapefile") is not False:
        fail("publish_month não pode ser promovido no Shapefile")
    nq = nonforest.get("schema_qualifications", {})
    if nq.get("view_date_is_exact_event_date") is not False:
        fail("view_date não pode ser data exata do evento")
    if nq.get("experimental_data_may_change_partially_or_entirely") is not True:
        fail("limitação experimental não florestal ausente")

    shared = data.get("shared_boundaries", {})
    for key in ("same_scientific_product", "same_class_domain", "same_schema", "same_start_period", "same_maturity_state", "catalog_update_date_is_release_identifier", "current_release_resolved", "direct_download_urls_verified", "asset_bytes_inspected", "checksums_computed"):
        if shared.get(key) is not False:
            fail(f"fronteira ou estado prematuro: {key}")
    if shared.get("current_catalog_snapshot_date") != "2026-07-28":
        fail("snapshot do catálogo divergente")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 4:
        fail("evidência oficial insuficiente")
    for item in evidence:
        if not isinstance(item, dict) or not official_https(item.get("url")):
            fail("toda evidência deve usar URL oficial HTTPS do INPE")

    rules_text = " ".join(str(x) for x in data.get("normalization_rules", [])).casefold()
    for token in ("não colapsar", "experimental", "areatotkm", "publish_month", "view_date", "2026-07-28", "uuid", "endpoint"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")
    if len(data.get("required_before_promotion", [])) < 8:
        fail("requisitos de promoção incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in ('"promotion_authorized": true', '"current_release_resolved": true', '"direct_download_urls_verified": true', '"asset_bytes_inspected": true'):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    print("OK: distribuições DETER Amazônia preservam domínios, esquemas e maturidade distintos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
