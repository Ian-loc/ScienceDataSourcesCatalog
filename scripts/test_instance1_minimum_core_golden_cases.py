#!/usr/bin/env python3
"""Exercise the minimum core with GEDI, DETER Cerrado, IBGE and ANA/SNIRH.

Fixtures are transactional and rolled back. They test representability and
scope discipline; they are not public catalog records.
"""
from __future__ import annotations

import os
import sys

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
        "entry_type": "service",
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


def main() -> int:
    try:
        import psycopg  # type: ignore
    except ImportError:
        print("ERRO: psycopg não instalado", file=sys.stderr)
        return 1

    with psycopg.connect(DEFAULT_DATABASE_URL) as connection:
        try:
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
            print("OK: GEDI, DETER Cerrado, IBGE e ANA/SNIRH representados no núcleo mínimo sem proliferação")
            connection.rollback()
            return 0
        except Exception:
            connection.rollback()
            raise


if __name__ == "__main__":
    raise SystemExit(main())
