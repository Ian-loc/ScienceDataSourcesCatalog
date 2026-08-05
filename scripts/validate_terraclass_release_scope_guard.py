#!/usr/bin/env python3
"""Validate the TerraClass Amazônia 2020 release-scope guard."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/terraclass_release_scope_guard_2026.json")
NULL_FIELDS = {
    "crs",
    "grid",
    "nominal_output_pixel_size",
    "complete_legend_and_codes",
    "checksum",
    "license_release_specific",
    "citation_release_specific",
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

    if data.get("product_stable_id") != "DP000005":
        fail("portão deve permanecer vinculado a DP000005")
    if data.get("release_stable_id") != "PR000005":
        fail("portão deve permanecer vinculado a PR000005")
    if data.get("release_label") != "TerraClass Amazônia 2020":
        fail("rótulo do release inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")

    release_2020 = data.get("release_2020")
    if not isinstance(release_2020, dict):
        fail("release_2020 deve ser objeto")
    if release_2020.get("reference_year") != 2020:
        fail("ano de referência 2020 incorreto")
    if release_2020.get("asset_state") != "not_inspected":
        fail("ativo 2020 deve permanecer not_inspected")
    if release_2020.get("curation_state") != "in_progress":
        fail("revisão 2020 deve permanecer in_progress")
    for field in NULL_FIELDS:
        if release_2020.get(field) is not None:
            fail(f"campo 2020 não comprovado deve permanecer nulo: {field}")
    scope_text = str(release_2020.get("known_scope_statement", "")).casefold()
    for term in ("prodes", "exact release coverage", "verified"):
        if term not in scope_text:
            fail(f"qualificação de escopo ausente: {term}")

    context_2024 = data.get("newer_2024_context")
    if not isinstance(context_2024, dict):
        fail("newer_2024_context deve ser objeto")
    if context_2024.get("reference_year") != 2024:
        fail("contexto novo deve permanecer 2024")
    if context_2024.get("publication_date") != "2026-06-23":
        fail("data da comunicação oficial 2024 incorreta")
    processing = str(context_2024.get("input_and_processing_statement", ""))
    for term in ("Sentinel-2", "16-day", "10 m", "Brazil Data Cube", "SITS"):
        if term not in processing:
            fail(f"descrição do contexto 2024 incompleta: {term}")
    for key in ("may_describe_release_2020", "may_supply_2020_asset_metadata", "may_replace_2020_method"):
        if context_2024.get(key) is not False:
            fail(f"{key} deve permanecer falso")

    controls = data.get("mandatory_controls")
    if not isinstance(controls, list) or len(controls) < 6:
        fail("controles obrigatórios insuficientes")
    controls_text = " ".join(str(item) for item in controls).casefold()
    for term in ("do not copy", "do not replace", "do not infer", "source imagery", "amazônia legal", "direct inspection"):
        if term not in controls_text:
            fail(f"controle obrigatório ausente: {term}")

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or len(evidence) != 4:
        fail("quatro evidências oficiais são obrigatórias")
    expected_types = {
        "official_project_background",
        "official_2020_partial_result_notice",
        "official_2024_release_context",
        "official_open_data_catalog",
    }
    observed_types = set()
    for item in evidence:
        if not https(str(item.get("url", ""))):
            fail("evidência deve usar URL HTTPS")
        evidence_type = str(item.get("type", ""))
        observed_types.add(evidence_type)
        if not item.get("supports"):
            fail(f"evidência sem supports: {evidence_type}")
        if not str(item.get("restriction", "")):
            fail(f"evidência sem restrição: {evidence_type}")
    if observed_types != expected_types:
        fail(f"tipos de evidência inesperados: {sorted(observed_types)}")

    creation_rule = str(data.get("release_creation_rule", "")).casefold()
    for term in ("own stable id", "must not mutate pr000005"):
        if term not in creation_rule:
            fail(f"regra de novo release incompleta: {term}")

    requirements = data.get("required_before_2020_approval")
    if not isinstance(requirements, list) or len(requirements) < 7:
        fail("requisitos pré-aprovação 2020 insuficientes")
    requirements_text = " ".join(str(item) for item in requirements).casefold()
    for term in ("metadata", "actual 2020", "crs", "legend", "sha-256", "license", "accuracy"):
        if term not in requirements_text:
            fail(f"requisito pré-aprovação ausente: {term}")

    print("OK: portão de escopo do TerraClass Amazônia 2020 validado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
