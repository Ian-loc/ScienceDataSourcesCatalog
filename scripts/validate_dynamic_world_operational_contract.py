#!/usr/bin/env python3
"""Validate the Dynamic World V1 operational-access contract."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/dynamic_world_operational_contract_2026.json")
EXPECTED_BANDS = {
    "water",
    "trees",
    "grass",
    "flooded_vegetation",
    "crops",
    "shrub_and_scrub",
    "built",
    "bare",
    "snow_and_ice",
    "label",
}
EXPECTED_DISTRIBUTIONS = {
    "DD000016": "canonical_machine_access",
    "DD000017": "secondary_metadata_record",
    "DD000018": "visual_explorer",
    "DD000019": "software_and_model",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def https(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.hostname)


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("product_stable_id") != "DP000011":
        fail("contrato deve permanecer vinculado a DP000011")
    if data.get("release_stable_id") != "PR000011":
        fail("contrato deve permanecer vinculado a PR000011")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("contrato operacional não pode autorizar promoção")

    asset = data.get("canonical_asset")
    if not isinstance(asset, dict):
        fail("canonical_asset deve ser objeto")
    if asset.get("asset_id") != "GOOGLE/DYNAMICWORLD/V1":
        fail("identificador canônico do asset incorreto")
    if asset.get("asset_type") != "Earth Engine ImageCollection":
        fail("tipo do asset deve permanecer Earth Engine ImageCollection")
    for key in ("catalog_url", "status_url"):
        if not https(str(asset.get(key, ""))):
            fail(f"{key} deve ser URL HTTPS")
    if asset.get("status_at_check") != "OK":
        fail("estado operacional verificado deve ser OK")
    if asset.get("availability_start") != "2015-06-27":
        fail("data inicial do produto incorreta")
    if "continuously updated" not in str(asset.get("availability_end_semantics", "")):
        fail("semântica de disponibilidade contínua ausente")
    if asset.get("nominal_pixel_size_m") != 10:
        fail("pixel nominal deve ser 10 m")
    if set(asset.get("bands", [])) != EXPECTED_BANDS:
        fail("conjunto de bandas incompleto ou inesperado")
    if set(asset.get("image_properties", [])) != {
        "dynamicworld_algorithm_version",
        "qa_algorithm_version",
    }:
        fail("propriedades de versão do asset incompletas")
    if asset.get("authentication_required") is not True:
        fail("acesso Earth Engine não deve ser descrito como anônimo")
    if asset.get("direct_file_download") is not False:
        fail("ImageCollection não deve ser descrita como download direto")
    if set(asset.get("subset_support", [])) != {
        "spatial",
        "temporal",
        "band",
        "class_probability",
    }:
        fail("capacidades de subset incompletas")

    constraints = data.get("scientific_access_constraints")
    if not isinstance(constraints, list) or len(constraints) < 5:
        fail("restrições científicas insuficientes")
    constraints_text = " ".join(str(item) for item in constraints).casefold()
    for term in ("sentinel-2", "sum to one", "field truth", "temporal composites", "clouds"):
        if term not in constraints_text:
            fail(f"restrição científica ausente: {term}")

    license_data = data.get("license")
    if not isinstance(license_data, dict):
        fail("license deve ser objeto")
    if license_data.get("dataset_license") != "CC BY 4.0":
        fail("licença do dataset incorreta")
    attribution = str(license_data.get("required_attribution", ""))
    for name in ("Google", "National Geographic Society", "World Resources Institute"):
        if name not in attribution:
            fail(f"atribuição incompleta: {name}")
    if "Copernicus Sentinel" not in str(license_data.get("upstream_notice", "")):
        fail("aviso upstream Sentinel ausente")
    if license_data.get("software_license_separate") is not True:
        fail("licença de software deve permanecer separada")

    citation = data.get("citation")
    if not isinstance(citation, dict) or citation.get("doi") != "10.1038/s41597-022-01307-4":
        fail("DOI científico ausente ou incorreto")

    distributions = data.get("distributions")
    if not isinstance(distributions, list) or len(distributions) != 4:
        fail("quatro distribuições legadas são obrigatórias")
    observed: dict[str, str] = {}
    for item in distributions:
        distribution_id = str(item.get("legacy_distribution_id", ""))
        role = str(item.get("role", ""))
        if distribution_id in observed:
            fail(f"distribuição duplicada: {distribution_id}")
        observed[distribution_id] = role
        if not https(str(item.get("url", ""))):
            fail(f"URL inválida em {distribution_id}")
        if item.get("promotion_target") != "release_distribution":
            fail(f"alvo de promoção incorreto em {distribution_id}")
        if not str(item.get("restriction", "")) and distribution_id != "DD000016":
            fail(f"restrição operacional ausente em {distribution_id}")
    if observed != EXPECTED_DISTRIBUTIONS:
        fail(f"papéis de distribuição inesperados: {observed}")

    requirements = data.get("required_before_curatorial_approval")
    if not isinstance(requirements, list) or len(requirements) < 6:
        fail("portão pré-aprovação insuficiente")
    requirements_text = " ".join(str(item) for item in requirements).casefold()
    for term in ("four distinct roles", "asset identifier", "license", "anonymous", "continuously updated", "database validator"):
        if term not in requirements_text:
            fail(f"requisito pré-aprovação ausente: {term}")

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or len(evidence) != 4:
        fail("quatro fontes de evidência são obrigatórias")
    types = {str(item.get("type", "")) for item in evidence}
    if types != {
        "official_dataset_catalog",
        "official_ingestion_status",
        "official_project_documentation",
        "peer_reviewed_data_descriptor",
    }:
        fail(f"tipos de evidência inesperados: {sorted(types)}")
    for item in evidence:
        if not https(str(item.get("url", ""))):
            fail("evidência deve usar URL HTTPS")
        if not item.get("supports"):
            fail("cada evidência deve declarar os campos sustentados")

    print("OK: contrato operacional do Dynamic World V1 validado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
