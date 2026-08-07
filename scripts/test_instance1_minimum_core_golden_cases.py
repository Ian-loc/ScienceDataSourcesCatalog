#!/usr/bin/env python3
"""Exercise the minimum core with GEDI, DETER Cerrado, IBGE and ANA/SNIRH.

Fixtures are transactional and rolled back. They test representability and
scope discipline; they are not public catalog records.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from promote_instance1_minimum_core import access_level, normalized_flag

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "instance1_scope_contract.json"
DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)

FIXTURES = (
    {
        "stable_id": "TEST-GOLDEN-GEDI",
        "organization": "NASA",
        "entry_type": "platform",
        "name": "Global Ecosystem Dynamics Investigation (GEDI)",
        "summary": "Missão e oferta de dados LiDAR orbital para estrutura da vegetação.",
        "scope": "Estrutura vertical da vegetação e biomassa em nível de descoberta.",
        "modalities": ["LiDAR orbital", "footprints", "produtos derivados"],
        "spatial": "faixa orbital da ISS; Brasil incluído",
        "temporal": "aquisições desde 2019; varia por produto",
        "resolution": "aprox. 25 m apenas quando material para produtos footprint",
        "update": "varia por produto",
        "official": "https://science.nasa.gov/mission/gedi/",
        "metadata": "https://daac.ornl.gov/cgi-bin/dataset_lister.pl?p=40/",
        "access": "https://daac.ornl.gov/cgi-bin/dataset_lister.pl?p=40/",
        "themes": ["estrutura vertical", "altura do dossel", "biomassa"],
    },
    {
        "stable_id": "TEST-GOLDEN-DETER-CERRADO",
        "organization": "Instituto Nacional de Pesquisas Espaciais (INPE)",
        "entry_type": "data_service",
        "name": "DETER Cerrado",
        "summary": "Sistema de avisos de alteração da cobertura de vegetação nativa no Cerrado.",
        "scope": "Monitoramento operacional para fiscalização; não é taxa anual consolidada.",
        "modalities": ["alertas geoespaciais", "dashboard"],
        "spatial": "bioma Cerrado",
        "temporal": "série operacional disponibilizada desde 2018",
        "resolution": None,
        "update": "operacional/frequente",
        "official": "https://terrabrasilis.dpi.inpe.br/",
        "metadata": "https://terrabrasilis.dpi.inpe.br/downloads/",
        "access": "https://terrabrasilis.dpi.inpe.br/",
        "themes": ["alteração da cobertura", "classes de alerta", "área"],
    },
    {
        "stable_id": "TEST-GOLDEN-IBGE",
        "organization": "Instituto Brasileiro de Geografia e Estatística (IBGE)",
        "entry_type": "source",
        "name": "IBGE — estatísticas e geociências",
        "summary": "Fonte oficial ampla de informações estatísticas e geocientíficas do Brasil.",
        "scope": "Estatísticas, censos, cartografia, território e geociências.",
        "modalities": ["tabelas", "microdados", "bases geoespaciais", "mapas"],
        "spatial": "Brasil; múltiplos recortes territoriais",
        "temporal": "varia por operação estatística e produto",
        "resolution": None,
        "update": "varia por operação/produto",
        "official": "https://www.ibge.gov.br/",
        "metadata": "https://metadados.ibge.gov.br/",
        "access": "https://www.ibge.gov.br/",
        "themes": ["demografia", "economia", "território", "geociências"],
    },
    {
        "stable_id": "TEST-GOLDEN-SNIRH",
        "organization": "Agência Nacional de Águas e Saneamento Básico (ANA)",
        "entry_type": "platform",
        "name": "Sistema Nacional de Informações sobre Recursos Hídricos (SNIRH)",
        "summary": "Sistema nacional de informações sobre recursos hídricos e sua gestão.",
        "scope": "Quantidade e qualidade das águas, usos, disponibilidade e gestão.",
        "modalities": ["séries hidrológicas", "dados tabulares", "geoespaciais", "mapas"],
        "spatial": "território brasileiro; varia por sistema/oferta",
        "temporal": "varia por sistema; atualização permanente no nível da plataforma",
        "resolution": None,
        "update": "permanente no nível do sistema",
        "official": "https://www.snirh.gov.br/portal/snirh",
        "metadata": "https://www.snirh.gov.br/portal/snirh",
        "access": "https://www.snirh.gov.br/portal/snirh",
        "themes": ["precipitação", "vazões", "reservatórios", "qualidade da água"],
    },
)


def load_contract_entry_types() -> tuple[str, ...]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    entry_types = contract.get("entry_types")
    if not isinstance(entry_types, list) or not entry_types or not all(isinstance(value, str) for value in entry_types):
        raise ValueError("entry_types inválidos no contrato mínimo")
    return tuple(entry_types)


def validate_normalization_semantics() -> None:
    cases = {
        "aberto": "open",
        "restrito": "restricted",
        "mediante solicitação": "restricted",
        "aberto | alguns dados mediante solicitação": "partial",
        "aberto | cadastro para alguns serviços": "partial",
        "parcial": "partial",
    }
    for raw, expected in cases.items():
        actual = access_level(raw)
        if actual != expected:
            raise ValueError(
                f"normalização de acesso incorreta para {raw!r}: {actual!r} != {expected!r}"
            )

    if normalized_flag("não se aplica") != "not_applicable":
        raise ValueError("não se aplica deve permanecer not_applicable")
    if normalized_flag("cadastro", authentication=True) != "yes":
        raise ValueError("cadastro deve registrar autenticação requerida")


def validate_database_entry_type_domain(connection, entry_types: tuple[str, ...]) -> None:
    """Prove that every contract entry type is accepted by the executable schema."""
    for index, entry_type in enumerate(entry_types, start=1):
        connection.execute(
            """
            INSERT INTO catalog.catalog_entries (
                stable_id, entry_type, official_name, summary, curation_status
            ) VALUES (%s, %s, %s, %s, 'needs_review')
            """,
            (
                f"TEST-CONTRACT-TYPE-{index}",
                entry_type,
                f"Contract type fixture: {entry_type}",
                "Transactional fixture for contract/schema alignment.",
            ),
        )

    inserted = connection.execute(
        "SELECT count(*) FROM catalog.catalog_entries WHERE stable_id LIKE 'TEST-CONTRACT-TYPE-%'"
    ).fetchone()[0]
    if inserted != len(entry_types):
        raise ValueError(
            f"domínio entry_type não materializou todos os valores do contrato: {inserted}/{len(entry_types)}"
        )


def main() -> int:
    validate_normalization_semantics()
    entry_types = load_contract_entry_types()
    fixture_types = {fixture["entry_type"] for fixture in FIXTURES}
    unknown_fixture_types = fixture_types - set(entry_types)
    if unknown_fixture_types:
        raise ValueError(
            f"fixtures usam entry_type fora do contrato: {sorted(unknown_fixture_types)}"
        )

    try:
        import psycopg  # type: ignore
    except ImportError:
        print("ERRO: psycopg não instalado", file=sys.stderr)
        return 1

    with psycopg.connect(DEFAULT_DATABASE_URL) as connection:
        try:
            validate_database_entry_type_domain(connection, entry_types)

            for index, fixture in enumerate(FIXTURES, start=1):
                organization_id = connection.execute(
                    """
                    INSERT INTO catalog.organizations (stable_id, official_name, organization_type)
                    VALUES (%s, %s, 'golden_case_fixture')
                    RETURNING organization_id
                    """,
                    (f"TEST-GOLDEN-ORG-{index}", fixture["organization"]),
                ).fetchone()[0]
                entry_id = connection.execute(
                    """
                    INSERT INTO catalog.catalog_entries (
                        stable_id, organization_id, entry_type, official_name, summary,
                        scientific_scope, data_modalities, geographic_coverage_text,
                        temporal_coverage_text, spatial_resolution_text, update_frequency_text,
                        access_level, free_access, authentication_required, official_page_url,
                        metadata_url, primary_access_url, curation_status, last_verified_at
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        'open', 'yes', 'unknown', %s,
                        %s, %s, 'partially_verified', DATE '2026-08-07'
                    ) RETURNING entry_id
                    """,
                    (
                        fixture["stable_id"], organization_id, fixture["entry_type"], fixture["name"],
                        fixture["summary"], fixture["scope"], fixture["modalities"], fixture["spatial"],
                        fixture["temporal"], fixture["resolution"], fixture["update"], fixture["official"],
                        fixture["metadata"], fixture["access"],
                    ),
                ).fetchone()[0]
                for theme in fixture["themes"]:
                    connection.execute(
                        """
                        INSERT INTO catalog.entry_variables (
                            entry_id, term_role, source_label, search_label, verification_status
                        ) VALUES (%s, 'theme', %s, %s, 'partially_verified')
                        """,
                        (entry_id, theme, theme.casefold()),
                    )
                connection.execute(
                    """
                    INSERT INTO catalog.entry_evidence (
                        entry_id, field_name, evidence_url, evidence_role,
                        support_note, verification_status, retrieved_at
                    ) VALUES (
                        %s, 'essential_profile', %s, 'official_page',
                        'Golden-case fixture sustentada pelo perfil auditado do PR #58.',
                        'partially_verified', DATE '2026-08-07'
                    )
                    """,
                    (entry_id, fixture["official"]),
                )

            count = connection.execute(
                "SELECT count(*) FROM catalog.catalog_entries WHERE stable_id LIKE 'TEST-GOLDEN-%'"
            ).fetchone()[0]
            if count != 4:
                raise ValueError(f"esperadas 4 entradas golden-case; obtidas {count}")
            if connection.execute(
                "SELECT to_regclass('catalog.connector_profiles') IS NOT NULL"
            ).fetchone()[0]:
                raise ValueError("golden cases não justificam connector_profiles")
            if connection.execute(
                "SELECT count(*) FROM catalog.entry_variables ev JOIN catalog.catalog_entries e USING (entry_id) WHERE e.stable_id LIKE 'TEST-GOLDEN-%'"
            ).fetchone()[0] < 12:
                raise ValueError("temas principais não foram representados")

            print(
                "OK: contrato/schema de entry_type alinhados; GEDI, DETER Cerrado, IBGE e ANA/SNIRH "
                "representados no núcleo mínimo sem proliferação; normalização adversarial aprovada"
            )
            connection.rollback()
            return 0
        except Exception:
            connection.rollback()
            raise


if __name__ == "__main__":
    raise SystemExit(main())
