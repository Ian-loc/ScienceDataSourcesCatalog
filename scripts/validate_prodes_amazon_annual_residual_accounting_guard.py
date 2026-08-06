#!/usr/bin/env python3
"""Validate PRODES Amazon annual residual temporal and accounting semantics."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

PATH = Path("database/mappings/prodes_amazon_annual_residual_accounting_guard_2026.json")
COMPANION_PATH = Path("database/mappings/prodes_amazon_annual_residual_guard_2026.json")
EXPECTED_UUID = "00a728cb-8577-458a-9c38-082c1f3bca9e"
EXPECTED_TARGET = "PRODES-ASSET-ANNUAL-NATIVE-VEGETATION-SUPPRESSION-RESIDUAL-SHP"
EXPECTED_PRODUCT = "PD-PRODES-AMZ-ANNUAL-RESIDUAL"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def official_inpe_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").endswith("inpe.br")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    if not COMPANION_PATH.is_file():
        fail(f"portão companheiro ausente: {COMPANION_PATH}")

    data = json.loads(PATH.read_text(encoding="utf-8"))
    companion = json.loads(COMPANION_PATH.read_text(encoding="utf-8"))

    if data.get("family_stable_id") != "PF000001":
        fail("portão deve permanecer vinculado à família PF000001")
    if data.get("target_id") != EXPECTED_TARGET:
        fail("alvo operacional inesperado")
    if data.get("candidate_scientific_product_id") != EXPECTED_PRODUCT:
        fail("candidato a produto inesperado")
    if data.get("metadata_identifier") != EXPECTED_UUID:
        fail("UUID de metadado foi alterado")
    if data.get("companion_metadata_guard") != str(COMPANION_PATH):
        fail("vínculo ao portão companheiro foi alterado")
    if data.get("status") != "official_residual_detection_year_and_accounting_semantics_verified":
        fail("estado curatorial inesperado")
    if data.get("timezone") != "America/Sao_Paulo":
        fail("timezone deve ser America/Sao_Paulo")
    if data.get("promotion_authorized") is not False:
        fail("portão não pode autorizar promoção")

    for key, expected in (
        ("target_id", EXPECTED_TARGET),
        ("candidate_scientific_product_id", EXPECTED_PRODUCT),
        ("metadata_identifier", EXPECTED_UUID),
    ):
        if companion.get(key) != expected:
            fail(f"inconsistência com portão companheiro: {key}")
    if companion.get("promotion_authorized") is not False:
        fail("portão companheiro não pode autorizar promoção")

    note = data.get("official_note")
    if not isinstance(note, dict):
        fail("official_note deve ser objeto")
    if note.get("institutional_ibi") != "id.inpe.br/mtc-m21d/2024/12.02.13.49-NTC":
        fail("IBI da nota técnica divergente")
    if note.get("publication_year") != 2024 or note.get("document_date") != "2023-09-30":
        fail("datas da nota técnica divergentes")
    if not official_inpe_https(note.get("public_pdf_url")):
        fail("PDF público deve usar URL HTTPS oficial do INPE")
    if "urlib.net" not in str(note.get("original_url", "")):
        fail("URL persistente original não registrada")

    definition = data.get("scientific_definition")
    if not isinstance(definition, dict):
        fail("scientific_definition deve ser objeto")
    for key in ("is_statistical_residual", "is_uncertainty_estimate", "is_current_year_increment"):
        if definition.get(key) is not False:
            fail(f"interpretação proibida detectada: {key}")
    causes = definition.get("documented_omission_causes")
    if not isinstance(causes, list) or len(causes) < 3:
        fail("causas documentadas de omissão insuficientes")
    causes_text = " ".join(causes).casefold()
    for token in ("nuvens", "classes", "detecção"):
        if token not in causes_text:
            fail(f"causa documentada ausente: {token}")

    semantics = data.get("temporal_and_accounting_semantics")
    if not isinstance(semantics, dict):
        fail("temporal_and_accounting_semantics deve ser objeto")
    expected_semantics = {
        "class_year_represents_detection_and_mapping_year": True,
        "class_year_represents_exact_suppression_year": False,
        "exact_suppression_year_resolved": False,
        "counted_in_annual_increment_for_detection_year": False,
        "counted_in_accumulated_suppression_through_detection_year": True,
        "incorporated_into_next_year_deforestation_mask": True,
        "appropriate_when_exact_occurrence_date_is_required": False,
    }
    for key, expected in expected_semantics.items():
        if semantics.get(key) != expected:
            fail(f"semântica temporal ou contábil alterada: {key}")
    semantics_text = " ".join(str(value) for value in semantics.values()).casefold()
    for token in ("interpretação errônea", "intensidade anual", "data real", "incerta"):
        if token not in semantics_text:
            fail(f"justificativa temporal incompleta: {token}")

    evidence = data.get("official_evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        fail("evidências oficiais insuficientes")
    for item in evidence:
        if not isinstance(item, dict) or not official_inpe_https(item.get("url")):
            fail("toda evidência deve usar URL HTTPS oficial do INPE")
    evidence_text = " ".join(json.dumps(item, ensure_ascii=False) for item in evidence).casefold()
    for token in ("omissão", "ano de detecção", "incremento anual", "acumulado", "máscara do ano seguinte", "data exata"):
        if token not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    state = data.get("verified_state")
    if not isinstance(state, dict):
        fail("verified_state deve ser objeto")
    for key in (
        "official_note_resolved",
        "detection_vs_occurrence_year_boundary_documented",
        "annual_increment_exclusion_documented",
        "accumulated_area_inclusion_documented",
        "next_year_mask_incorporation_documented",
        "exact_occurrence_date_limitation_documented",
        "qualitative_temporal_uncertainty_documented",
    ):
        if state.get(key) is not True:
            fail(f"fato verificado ausente: {key}")
    for key in (
        "current_release_resolved",
        "direct_download_url_verified",
        "asset_bytes_inspected",
        "checksum_computed",
        "promotion_authorized",
    ):
        if state.get(key) is not False:
            fail(f"estado prematuro detectado: {key}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 10:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in ("ano de detecção", "ano exato", "incremento anual", "acumulado", "máscara", "erro estatístico", "não florestal", "release"):
        if token not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    required = data.get("required_before_product_promotion")
    if not isinstance(required, list) or len(required) < 8:
        fail("requisitos de promoção incompletos")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"class_year_represents_exact_suppression_year": true',
        '"exact_suppression_year_resolved": true',
        '"counted_in_annual_increment_for_detection_year": true',
        '"current_release_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
    ):
        if forbidden in serialized:
            fail(f"promoção ou interpretação prematura detectada: {forbidden}")

    print("OK: resíduo PRODES preserva ano de detecção, exclusão do incremento, inclusão no acumulado e limitação temporal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
