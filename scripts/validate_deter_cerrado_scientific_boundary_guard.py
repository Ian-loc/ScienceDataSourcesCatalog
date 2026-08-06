#!/usr/bin/env python3
"""Validate the final scientific-operational audit boundary for DETER Cerrado."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from validate_deter_cerrado_access_license_citation_guard import main as validate_access_license_citation
from validate_deter_cerrado_endpoint_discovery_guard import main as validate_endpoint_discovery
from validate_deter_cerrado_metadata_identifier_ambiguity_guard import main as validate_identifier_reconciliation
from validate_deter_cerrado_metadata_profile_guard import main as validate_metadata_profile
from validate_deter_cerrado_method_profile_guard import main as validate_method_profile
from validate_deter_cerrado_operational_legend_latency_guard import main as validate_operational_legend_latency
from validate_deter_cerrado_quality_validation_guard import main as validate_quality_validation

PATH = Path("database/mappings/deter_cerrado_scientific_boundary_guard_2026.json")
CURRENT_UUID = "e6e15388-4ca9-49b9-aec9-03891339a35e"
STALE_UUID = "a5220c18-f7fa-4e3e-b39b-feeb3ccc4830"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def trusted_https(url: object) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    host = (parsed.hostname or "").casefold()
    return parsed.scheme == "https" and (
        host.endswith("inpe.br")
        or host.endswith("gov.br")
        or host == "doi.org"
        or (host == "github.com" and parsed.path.casefold().startswith("/terrabrasilis/terrabrasilis_datasource"))
    )


def require_true(mapping: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) is not True:
            fail(f"{label} incompleto: {key}")


def require_false(mapping: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if mapping.get(key) is not False:
            fail(f"{label} promovido prematuramente: {key}")


def main() -> int:
    if not PATH.is_file():
        fail(f"arquivo ausente: {PATH}")
    data = json.loads(PATH.read_text(encoding="utf-8"))

    expected_top = {
        "contract_version": "2.0.0",
        "package_id": "I1-M2A-DETER-CERRADO",
        "family_stable_id": "PF000003",
        "candidate_scientific_product_id": "PD-DETER-CER-ALERTS",
        "status": "scientific_operational_audit_complete_with_bounded_external_incompleteness_promotion_blocked",
        "timezone": "America/Sao_Paulo",
        "promotion_authorized": False,
    }
    for key, value in expected_top.items():
        if data.get(key) != value:
            fail(f"campo superior divergente: {key}")

    identity = data.get("scientific_identity")
    if not isinstance(identity, dict):
        fail("scientific_identity deve ser objeto")
    if identity.get("product_boundary_state") != "candidate_operational_alert_product":
        fail("fronteira de produto operacional ausente")
    if identity.get("operational_start_year_documented") != 2018:
        fail("início operacional divergente")
    require_false(
        identity,
        (
            "is_annual_deforestation_rate",
            "is_monthly_deforestation_rate",
            "is_complete_annual_inventory",
            "is_prodes_release",
            "is_deter_amazon_distribution",
        ),
        "identidade científica",
    )
    identity_text = json.dumps(identity, ensure_ascii=False).casefold()
    for token in ("avisos", "supressão", "vegetação nativa", "cerrado", "fiscalização"):
        if token not in identity_text:
            fail(f"identidade incompleta: {token}")

    distribution = data.get("distribution_identity")
    if not isinstance(distribution, dict):
        fail("distribution_identity deve ser objeto")
    if distribution.get("current_metadata_identifier") != CURRENT_UUID:
        fail("UUID corrente divergente")
    if distribution.get("superseded_published_citation_identifier") != STALE_UUID:
        fail("UUID histórico divergente")
    if CURRENT_UUID not in str(distribution.get("current_metadata_url", "")):
        fail("URL do metadado corrente divergente")
    if not trusted_https(distribution.get("current_metadata_url")) or not trusted_https(distribution.get("catalog_url")):
        fail("URLs oficiais da distribuição inválidas")
    if distribution.get("declared_format") != "ESRI Shapefile":
        fail("formato declarado divergente")
    if distribution.get("catalog_last_updated_displayed") != "2026-07-28":
        fail("data exibida divergente")
    if distribution.get("metadata_identifier_reconciled") is not True:
        fail("identificador de metadado não reconciliado")
    require_false(
        distribution,
        (
            "catalog_display_date_is_release_identifier",
            "metadata_identifier_is_product_identifier",
            "metadata_identifier_is_release_identifier",
            "metadata_identifier_is_asset_identifier",
            "direct_download_url_verified",
            "http_status_verified",
            "redirect_chain_verified",
            "asset_bytes_inspected",
            "checksum_computed",
        ),
        "distribuição/ativo",
    )

    resolved = data.get("resolved_scientific_operational_profiles")
    if not isinstance(resolved, dict):
        fail("resolved_scientific_operational_profiles deve ser objeto")
    require_true(
        resolved,
        (
            "specific_metadata_record_resolved",
            "metadata_schema_inventory_documented",
            "validation_class_domain_resolved_for_method_edition",
            "cycle_mask_semantics_resolved",
            "published_citation_guidance_documented",
            "generic_wfs_capability_documented",
            "registered_download_channel_documented",
            "official_qgis_wms_registry_inspected",
            "peer_reviewed_operational_proximity_evidence_resolved",
        ),
        "perfil científico-operacional",
    )
    if resolved.get("metadata_class_documented") != "DESMATAMENTO_CR":
        fail("classe de metadado divergente")
    if resolved.get("method_edition_resolved") != "INPE 2024-03-28":
        fail("edição metodológica divergente")
    if resolved.get("method_doi") != "10.13140/RG.2.2.24196.49281":
        fail("DOI metodológico divergente")
    if resolved.get("specific_nominal_resolution_m") != [55, 64]:
        fail("resolução específica divergente")
    if resolved.get("specific_interpretation_scale") != "1:100.000":
        fail("escala de interpretação divergente")
    if resolved.get("specific_minimum_alert_area_ha") != 3:
        fail("limiar específico divergente")
    if resolved.get("typical_processing_latency_hours") != [48, 72]:
        fail("latência divergente")
    if set(resolved.get("operational_classes_resolved", [])) != {"Alerta_cb4", "Alerta_amz1", "Alerta_cba", "Aviso"}:
        fail("classes operacionais divergentes")
    if set(resolved.get("validation_class_domain_resolved_for_method_edition", [])) != {
        "Alerta", "Falso Positivo", "Resíduo", "Não Observado", "Sem condições de avaliação"
    }:
        fail("domínio de validação divergente")
    if resolved.get("program_level_license_resolved") != "CC-BY-SA-4.0":
        fail("licença do programa divergente")
    if resolved.get("reported_proximity_percentage") != 80 or resolved.get("reported_buffer_radius_km") != 10:
        fail("evidência quantitativa de proximidade divergente")
    if resolved.get("proximity_result_is_accuracy_metric") is not False:
        fail("proximidade não pode virar acurácia")

    boundaries = data.get("cross_domain_boundaries")
    if not isinstance(boundaries, dict):
        fail("cross_domain_boundaries deve ser objeto")
    require_false(boundaries, tuple(boundaries.keys()), "fronteira entre domínios")

    unresolved = data.get("bounded_unresolved_state")
    if not isinstance(unresolved, dict) or len(unresolved) < 20:
        fail("bounded_unresolved_state insuficiente")
    require_false(unresolved, tuple(unresolved.keys()), "estado externo não resolvido")

    completion = data.get("curatorial_completion")
    if not isinstance(completion, dict):
        fail("curatorial_completion deve ser objeto")
    require_true(
        completion,
        (
            "identity_review_complete",
            "meaning_and_boundary_review_complete",
            "method_review_complete",
            "spatial_temporal_review_complete",
            "class_and_variable_review_complete",
            "quality_and_uncertainty_review_complete_with_explicit_negative_states",
            "access_endpoint_and_asset_review_complete_with_explicit_negative_states",
            "license_and_citation_review_complete_with_explicit_scope_limits",
            "evidence_by_material_assertion_documented",
            "bounded_external_incompleteness_is_fail_closed",
            "scientific_audit_package_complete",
            "merge_ready_after_exact_head_ci_and_human_authorization",
            "human_merge_authorization_required",
        ),
        "completude curatorial",
    )
    if completion.get("occurrence_register_updated_through") != "I1-20260806-058":
        fail("cursor de ocorrências divergente")
    require_false(
        completion,
        (
            "product_profile_complete_for_promotion",
            "release_profile_complete_for_promotion",
            "asset_profile_complete_for_promotion",
        ),
        "promoção curatorial",
    )

    evidence = data.get("evidence_surfaces")
    if not isinstance(evidence, list) or len(evidence) != 6:
        fail("seis superfícies de evidência são obrigatórias")
    expected_roles = {
        "current_metadata_record",
        "current_download_listing",
        "current_program_definition",
        "method_edition",
        "peer_reviewed_operational_evidence",
        "official_qgis_wms_registry",
    }
    if {item.get("role") for item in evidence if isinstance(item, dict)} != expected_roles:
        fail("papéis de evidência divergentes")
    for item in evidence:
        if not isinstance(item, dict) or not trusted_https(item.get("url")):
            fail(f"superfície de evidência inválida: {item.get('url') if isinstance(item, dict) else item}")
    evidence_text = json.dumps(evidence, ensure_ascii=False).casefold()
    for token in (CURRENT_UUID, "2026-07-28", "10.13140", "80 percent", "official wms registry"):
        if token.casefold() not in evidence_text:
            fail(f"cobertura de evidência ausente: {token}")

    rules = data.get("normalization_rules")
    if not isinstance(rules, list) or len(rules) < 15:
        fail("regras de normalização insuficientes")
    rules_text = " ".join(str(item) for item in rules).casefold()
    for token in (
        CURRENT_UUID,
        STALE_UUID,
        "taxa mensal",
        "deter amazônia",
        "2018",
        "28/07/2026",
        "classes operacionais",
        "resíduo de validação",
        "80 por cento",
        "registro wms",
        "dns",
        "incerteza",
        "pacote de auditoria completo",
        "ci verde",
        "autorização humana",
    ):
        if token.casefold() not in rules_text:
            fail(f"regra obrigatória ausente: {token}")

    requirements = data.get("required_before_future_product_release_or_asset_promotion")
    if not isinstance(requirements, list) or len(requirements) < 9:
        fail("requisitos futuros de promoção insuficientes")

    serialized = PATH.read_text(encoding="utf-8")
    for forbidden in (
        '"promotion_authorized": true',
        '"current_release_resolved": true',
        '"specific_wfs_workspace_resolved": true',
        '"direct_download_url_verified": true',
        '"asset_bytes_inspected": true',
        '"checksum_computed": true',
        '"product_profile_complete_for_promotion": true',
        '"release_profile_complete_for_promotion": true',
        '"asset_profile_complete_for_promotion": true',
    ):
        if forbidden in serialized:
            fail(f"promoção prematura detectada: {forbidden}")

    validate_metadata_profile()
    validate_identifier_reconciliation()
    validate_access_license_citation()
    validate_method_profile()
    validate_operational_legend_latency()
    validate_endpoint_discovery()
    validate_quality_validation()

    print(
        "OK: auditoria I1-M2A do DETER Cerrado completa com incompletude externa delimitada; "
        "produto, release e ativo permanecem fail-closed e dependem de autorização humana para merge"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
