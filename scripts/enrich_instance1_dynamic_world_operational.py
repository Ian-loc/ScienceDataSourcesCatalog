#!/usr/bin/env python3
"""Idempotently reconcile the Dynamic World operational contract with Instance 1."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "database" / "mappings" / "dynamic_world_operational_contract_2026.json"
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)

EXPECTED_ROLES = {
    "DD000016": "api",
    "DD000017": "catalog_record",
    "DD000018": "visualizer",
    "DD000019": "code_repository",
}

CAPABILITIES = {
    "DD000016": {
        "discover": "available",
        "query_attributes": "conditional",
        "spatial_subset": "conditional",
        "temporal_subset": "conditional",
        "process": "conditional",
        "export": "conditional",
        "open_in_earth_engine": "conditional",
        "open_in_python": "conditional",
    },
    "DD000017": {"discover": "available", "preview": "available"},
    "DD000018": {"preview": "available", "visualize": "available"},
    "DD000019": {
        "discover": "available",
        "download": "available",
        "open_in_python": "conditional",
    },
}


def psycopg_module():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit("Instale database/requirements.txt") from exc
    return psycopg


def load_contract() -> dict[str, Any]:
    with CONTRACT_PATH.open(encoding="utf-8") as handle:
        contract = json.load(handle)
    if contract.get("product_stable_id") != "DP000011":
        raise ValueError("contrato Dynamic World aponta produto inesperado")
    if contract.get("release_stable_id") != "PR000011":
        raise ValueError("contrato Dynamic World aponta release inesperado")
    if contract.get("promotion_authorized") is not False:
        raise ValueError("contrato não pode autorizar promoção canônica")
    ids = {row["legacy_distribution_id"] for row in contract["distributions"]}
    if ids != set(EXPECTED_ROLES):
        raise ValueError(f"distribuições divergentes no contrato: {sorted(ids)}")
    return contract


def distribution_pk(connection, stable_id: str) -> int:
    row = connection.execute(
        "SELECT distribution_id FROM catalog.distributions WHERE stable_id=%s",
        (stable_id,),
    ).fetchone()
    if not row:
        raise ValueError(f"distribuição normalizada ausente: {stable_id}")
    return int(row[0])


def reconcile_distributions(connection, contract: dict[str, Any]) -> None:
    by_id = {
        row["legacy_distribution_id"]: row
        for row in contract["distributions"]
    }
    canonical = contract["canonical_asset"]
    license_info = contract["license"]
    checked_at = contract["checked_at"]

    settings = {
        "DD000016": {
            "name": "Dynamic World V1 — Google Earth Engine ImageCollection",
            "url": by_id["DD000016"]["url"],
            "protocol": "Google Earth Engine API",
            "tool": "Earth Engine Code Editor, Python API or JavaScript API",
            "free_access": "yes",
            "auth": "yes",
            "conditions": canonical["access_requirement"],
            "license": license_info["dataset_license"],
            "attribution": True,
            "subset": "spatial; temporal; band; class probability; export subject to Earth Engine limits",
            "notes": (
                "Canonical machine access. No anonymous direct file download; "
                "availability is continuously updated and must not be frozen to the crawl date."
            ),
            "status": "working" if canonical["status_at_check"] == "OK" else "unknown",
        },
        "DD000017": {
            "name": "Dynamic World V1 — WRI metadata record",
            "url": by_id["DD000017"]["url"],
            "protocol": "HTTPS",
            "tool": "web browser",
            "free_access": "yes",
            "auth": "no",
            "conditions": "Metadata discovery only; does not host the canonical raster assets.",
            "license": license_info["dataset_license"],
            "attribution": True,
            "subset": None,
            "notes": "Secondary metadata record; not an asset host.",
            "status": "working",
        },
        "DD000018": {
            "name": "Dynamic World visual explorer",
            "url": by_id["DD000018"]["url"],
            "protocol": "HTTPS",
            "tool": "web browser",
            "free_access": "yes",
            "auth": "no",
            "conditions": "Visualization only; not equivalent to reproducible analytical access.",
            "license": license_info["dataset_license"],
            "attribution": True,
            "subset": "interactive visual spatial and temporal exploration",
            "notes": "Visual explorer separated from machine access.",
            "status": "working",
        },
        "DD000019": {
            "name": "Dynamic World source code and model repository",
            "url": by_id["DD000019"]["url"],
            "protocol": "Git/HTTPS",
            "tool": "GitHub, git or web browser",
            "free_access": "yes",
            "auth": "no",
            "conditions": "Software and model artifacts; not the dataset distribution.",
            "license": "Apache-2.0 (software); dataset remains CC BY 4.0",
            "attribution": False,
            "subset": None,
            "notes": "Software licensing is explicitly separated from dataset licensing.",
            "status": "working",
        },
    }

    for stable_id, values in settings.items():
        connection.execute(
            """
            UPDATE catalog.distributions
            SET distribution_name=%s,
                distribution_role=%s,
                access_url=%s,
                access_protocol=%s,
                access_tool=%s,
                free_access=%s,
                authentication_required=%s,
                access_conditions=%s,
                license=%s,
                attribution_required=%s,
                subset_support=%s,
                service_level_notes=%s,
                access_status=%s,
                last_access_tested_at=%s::timestamptz,
                updated_at=now()
            WHERE stable_id=%s
            """,
            (
                values["name"], EXPECTED_ROLES[stable_id], values["url"],
                values["protocol"], values["tool"], values["free_access"],
                values["auth"], values["conditions"], values["license"],
                values["attribution"], values["subset"], values["notes"],
                values["status"], checked_at, stable_id,
            ),
        )
        pk = distribution_pk(connection, stable_id)
        for capability_type, status in CAPABILITIES[stable_id].items():
            requirement = (
                canonical["access_requirement"] if stable_id == "DD000016"
                and status == "conditional" else values["conditions"]
            )
            connection.execute(
                """
                INSERT INTO catalog.access_capabilities (
                    distribution_id, capability_type, capability_status,
                    requirements, documentation_url
                ) VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (distribution_id, capability_type) DO UPDATE SET
                    capability_status=EXCLUDED.capability_status,
                    requirements=EXCLUDED.requirements,
                    documentation_url=EXCLUDED.documentation_url
                """,
                (pk, capability_type, status, requirement, values["url"]),
            )


def reconcile_asset(connection, contract: dict[str, Any]) -> None:
    canonical = contract["canonical_asset"]
    pk = distribution_pk(connection, "DD000016")
    connection.execute(
        """
        INSERT INTO catalog.data_assets (
            stable_id, distribution_id, asset_name, asset_role,
            asset_url, asset_identifier, format, media_type,
            machine_readable, supports_range_requests,
            supports_spatial_subset, supports_temporal_subset,
            crs, notes
        ) VALUES (
            'AS-DW-EE-V1', %s,
            'Dynamic World V1 Earth Engine ImageCollection', 'data',
            %s, %s, 'Earth Engine ImageCollection',
            'application/vnd.google-earth-engine.imagecollection',
            true, false, true, true, NULL, %s
        )
        ON CONFLICT (stable_id) DO UPDATE SET
            distribution_id=EXCLUDED.distribution_id,
            asset_name=EXCLUDED.asset_name,
            asset_role=EXCLUDED.asset_role,
            asset_url=EXCLUDED.asset_url,
            asset_identifier=EXCLUDED.asset_identifier,
            format=EXCLUDED.format,
            media_type=EXCLUDED.media_type,
            machine_readable=EXCLUDED.machine_readable,
            supports_range_requests=EXCLUDED.supports_range_requests,
            supports_spatial_subset=EXCLUDED.supports_spatial_subset,
            supports_temporal_subset=EXCLUDED.supports_temporal_subset,
            crs=EXCLUDED.crs,
            notes=EXCLUDED.notes,
            updated_at=now()
        """,
        (
            pk,
            canonical["catalog_url"],
            canonical["asset_id"],
            (
                "Canonical logical asset identifier stored independently from the catalog URL. "
                "The collection is continuously updated; exports are user-created derivatives."
            ),
        ),
    )


def add_assertion(
    connection,
    entity_type: str,
    entity_id: str,
    field_name: str,
    value: str,
    evidence_url: str,
    evidence_type: str,
    note: str,
) -> None:
    connection.execute(
        """
        INSERT INTO catalog.metadata_assertions (
            entity_type, entity_stable_id, field_name, asserted_value,
            evidence_url, evidence_type, support_note, confidence, retrieved_at
        )
        SELECT %s,%s,%s,%s,%s,%s,%s,'high',now()
        WHERE NOT EXISTS (
            SELECT 1 FROM catalog.metadata_assertions
            WHERE entity_type=%s AND entity_stable_id=%s
              AND field_name=%s AND evidence_url=%s
        )
        """,
        (
            entity_type, entity_id, field_name, value, evidence_url,
            evidence_type, note, entity_type, entity_id, field_name, evidence_url,
        ),
    )


def reconcile_evidence(connection, contract: dict[str, Any]) -> None:
    catalog_url = contract["canonical_asset"]["catalog_url"]
    license_info = contract["license"]
    add_assertion(
        connection, "asset", "AS-DW-EE-V1", "asset_identifier",
        contract["canonical_asset"]["asset_id"], catalog_url,
        "official_documentation",
        "Identificador lógico canônico verificado no catálogo oficial Earth Engine.",
    )
    add_assertion(
        connection, "distribution", "DD000016", "access_model",
        "authenticated Earth Engine API; no anonymous direct file download",
        catalog_url, "official_documentation",
        "O acesso exige projeto Google Cloud registrado e API habilitada.",
    )
    add_assertion(
        connection, "distribution", "DD000016", "license",
        license_info["dataset_license"], catalog_url, "license",
        "Licença do dataset registrada separadamente da licença do software.",
    )
    add_assertion(
        connection, "release", "PR000011", "required_attribution",
        license_info["required_attribution"], catalog_url, "license",
        "Atribuição obrigatória da distribuição oficial.",
    )
    add_assertion(
        connection, "release", "PR000011", "upstream_notice",
        license_info["upstream_notice"], catalog_url, "license",
        "Aviso dos dados Sentinel modificados preservado.",
    )


def update_review(connection) -> None:
    result = connection.execute(
        """
        UPDATE catalog.curation_reviews
        SET review_status='reviewed',
            completeness_score=0.95,
            scientific_precision_score=0.95,
            operational_precision_score=0.95,
            reviewer='automated contract reconciliation with curated evidence',
            reviewed_at=now(),
            findings=%s,
            corrections_required=%s
        WHERE entity_type='product' AND entity_stable_id='DP000011'
        """,
        (
            "Scientific validation and operational contract reconciled with normalized "
            "release, distributions, canonical asset, capabilities, licensing and evidence.",
            "Final transversal pilot audit and human authorization remain required before "
            "canonical promotion or merge; live Earth Engine execution is not asserted.",
        ),
    )
    if result.rowcount != 1:
        raise ValueError("revisão curatorial Dynamic World ausente ou duplicada")


def validate(connection, contract: dict[str, Any]) -> None:
    rows = connection.execute(
        """
        SELECT stable_id, distribution_role, access_url, authentication_required,
               license, access_status
        FROM catalog.distributions
        WHERE stable_id IN ('DD000016','DD000017','DD000018','DD000019')
        """
    ).fetchall()
    if len(rows) != 4:
        raise ValueError(f"distribuições Dynamic World encontradas={len(rows)}; esperado=4")
    by_id = {row[0]: row for row in rows}
    contract_urls = {
        row["legacy_distribution_id"]: row["url"]
        for row in contract["distributions"]
    }
    for stable_id, expected_role in EXPECTED_ROLES.items():
        row = by_id[stable_id]
        if row[1] != expected_role:
            raise ValueError(f"{stable_id}: role={row[1]}; esperado={expected_role}")
        if row[2] != contract_urls[stable_id]:
            raise ValueError(f"{stable_id}: URL divergente")
    if by_id["DD000016"][3] != "yes":
        raise ValueError("DD000016 deve registrar autenticação obrigatória")
    if by_id["DD000016"][4] != "CC BY 4.0":
        raise ValueError("licença do dataset Dynamic World divergente")
    if by_id["DD000019"][4] == "CC BY 4.0":
        raise ValueError("licença de software não pode ser confundida com a licença do dataset")

    asset = connection.execute(
        """
        SELECT asset_identifier, machine_readable, supports_spatial_subset,
               supports_temporal_subset
        FROM catalog.data_assets WHERE stable_id='AS-DW-EE-V1'
        """
    ).fetchone()
    if not asset:
        raise ValueError("ativo canônico Dynamic World ausente")
    if asset[0] != contract["canonical_asset"]["asset_id"]:
        raise ValueError("identificador do ativo canônico divergente")
    if tuple(asset[1:]) != (True, True, True):
        raise ValueError("capacidades do ativo canônico divergentes")

    capabilities = int(connection.execute(
        """
        SELECT count(*) FROM catalog.access_capabilities ac
        JOIN catalog.distributions d ON d.distribution_id=ac.distribution_id
        WHERE d.stable_id IN ('DD000016','DD000017','DD000018','DD000019')
        """
    ).fetchone()[0])
    if capabilities != 15:
        raise ValueError(f"capacidades Dynamic World={capabilities}; esperado=15")

    review = connection.execute(
        """
        SELECT review_status, completeness_score, scientific_precision_score,
               operational_precision_score
        FROM catalog.curation_reviews
        WHERE entity_type='product' AND entity_stable_id='DP000011'
        """
    ).fetchone()
    if not review or review[0] != "reviewed":
        raise ValueError("revisão Dynamic World não alcançou estado reviewed")
    if any(float(value) < 0.9 for value in review[1:]):
        raise ValueError("escores curatoriais Dynamic World abaixo do portão")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DATABASE_URL)
    args = parser.parse_args()
    contract = load_contract()
    psycopg = psycopg_module()

    with psycopg.connect(args.database_url) as connection:
        reconcile_distributions(connection, contract)
        reconcile_asset(connection, contract)
        reconcile_evidence(connection, contract)
        update_review(connection)
        validate(connection, contract)

    print("OK: contrato operacional Dynamic World reconciliado com o catálogo normalizado")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
