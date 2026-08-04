#!/usr/bin/env python3
"""Enrich the Dynamic World V1 pilot with audited scientific-operational metadata."""
from __future__ import annotations

import argparse
import os
import sys

DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)

CATALOG_URL = "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1"
PAPER_URL = "https://doi.org/10.1038/s41597-022-01307-4"

BANDS = (
    ("water", "Água", "water", "Probabilidade estimada de cobertura completa por água."),
    ("trees", "Árvores", "trees", "Probabilidade estimada de cobertura completa por árvores."),
    ("grass", "Gramíneas", "grass", "Probabilidade estimada de cobertura completa por gramíneas."),
    ("flooded_vegetation", "Vegetação inundada", "flooded vegetation", "Probabilidade estimada de cobertura completa por vegetação inundada."),
    ("crops", "Cultivos", "crops", "Probabilidade estimada de cobertura completa por cultivos."),
    ("shrub_and_scrub", "Arbustos e vegetação arbustiva", "shrub and scrub", "Probabilidade estimada de cobertura completa por arbustos e vegetação arbustiva."),
    ("built", "Área construída", "built", "Probabilidade estimada de cobertura completa por superfícies construídas."),
    ("bare", "Superfície exposta", "bare", "Probabilidade estimada de cobertura completa por superfície exposta."),
    ("snow_and_ice", "Neve e gelo", "snow and ice", "Probabilidade estimada de cobertura completa por neve e gelo."),
)


def import_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "psycopg não instalado. Execute: python -m pip install -r database/requirements.txt"
        ) from exc
    return psycopg


def upsert_method(connection) -> int:
    connection.execute(
        """
        INSERT INTO catalog.methods (
            stable_id, method_name, method_type, description, input_data,
            processing_summary, validation_summary, method_version,
            methodology_url, limitations
        ) VALUES (
            'MT-DW-V1', 'Dynamic World V1 inference', 'remote_sensing_classification',
            %s, %s, %s, %s, 'V1', %s, %s
        )
        ON CONFLICT (stable_id) DO UPDATE SET
            method_name = EXCLUDED.method_name,
            method_type = EXCLUDED.method_type,
            description = EXCLUDED.description,
            input_data = EXCLUDED.input_data,
            processing_summary = EXCLUDED.processing_summary,
            validation_summary = EXCLUDED.validation_summary,
            method_version = EXCLUDED.method_version,
            methodology_url = EXCLUDED.methodology_url,
            limitations = EXCLUDED.limitations,
            updated_at = now()
        """,
        (
            "Classificação de uso e cobertura da terra quase em tempo real para imagens Sentinel-2 individuais.",
            "Sentinel-2 L1C elegível, com CLOUDY_PIXEL_PERCENTAGE <= 35%.",
            "Inferência por imagem; probabilidades para nove classes somam 1 e a banda label registra a classe de maior probabilidade. Nuvens e sombras são mascaradas por combinação de S2 Cloud Probability, Cloud Displacement Index e Directional Distance Transform.",
            "Validação e desenho metodológico documentados no artigo descritor de Dynamic World.",
            PAPER_URL,
            "Predições derivadas de uma única imagem e de contexto espacial local podem apresentar baixa confiança em classes definidas parcialmente por persistência temporal, como cultivos; superfícies brilhantes, areia, ambientes áridos e sunglint também exigem cautela.",
        ),
    )
    return connection.execute(
        "SELECT method_id FROM catalog.methods WHERE stable_id = 'MT-DW-V1'"
    ).fetchone()[0]


def upsert_profiles(connection) -> tuple[int, int, int]:
    connection.execute(
        """
        INSERT INTO catalog.spatial_profiles (
            stable_id, support_type, support_description, geometry_type,
            nominal_resolution_value, nominal_resolution_unit, crs,
            grid_definition, geographic_coverage_text, spatial_limitations
        ) VALUES (
            'SP-DW-V1', 'pixel',
            'Pixel de saída associado a uma predição para uma imagem Sentinel-2 L1C individual.',
            'raster', 10, 'm', 'Sentinel-2 source grid',
            'Grade correspondente ao ativo Sentinel-2 L1C de origem.',
            'Global, incluindo o Brasil.',
            'Resolução nominal de 10 m não equivale a verdade de campo nem elimina mistura espectral ou dependência do contexto local.'
        )
        ON CONFLICT (stable_id) DO UPDATE SET
            support_type = EXCLUDED.support_type,
            support_description = EXCLUDED.support_description,
            geometry_type = EXCLUDED.geometry_type,
            nominal_resolution_value = EXCLUDED.nominal_resolution_value,
            nominal_resolution_unit = EXCLUDED.nominal_resolution_unit,
            crs = EXCLUDED.crs,
            grid_definition = EXCLUDED.grid_definition,
            geographic_coverage_text = EXCLUDED.geographic_coverage_text,
            spatial_limitations = EXCLUDED.spatial_limitations,
            updated_at = now()
        """
    )
    connection.execute(
        """
        INSERT INTO catalog.temporal_profiles (
            stable_id, representation_type, support_description,
            coverage_start, temporal_resolution, observation_window,
            update_frequency, temporal_aggregation, temporal_limitations
        ) VALUES (
            'TP-DW-V1', 'event',
            'Cada imagem Dynamic World corresponde a uma imagem Sentinel-2 L1C elegível.',
            DATE '2015-06-27', 'por aquisição Sentinel-2 elegível',
            'Instante/período da aquisição Sentinel-2 de origem.',
            'Quase em tempo real; revisita Sentinel-2 tipicamente de 2 a 5 dias conforme latitude.',
            'Nenhuma composição temporal é embutida na imagem individual.',
            'Uma imagem individual não representa persistência, transição validada ou classe anual; composições temporais exigem processamento explícito.'
        )
        ON CONFLICT (stable_id) DO UPDATE SET
            representation_type = EXCLUDED.representation_type,
            support_description = EXCLUDED.support_description,
            coverage_start = EXCLUDED.coverage_start,
            temporal_resolution = EXCLUDED.temporal_resolution,
            observation_window = EXCLUDED.observation_window,
            update_frequency = EXCLUDED.update_frequency,
            temporal_aggregation = EXCLUDED.temporal_aggregation,
            temporal_limitations = EXCLUDED.temporal_limitations,
            updated_at = now()
        """
    )
    connection.execute(
        """
        INSERT INTO catalog.quality_profiles (
            stable_id, quality_status, validation_design, accuracy_metrics,
            uncertainty_available, uncertainty_type, uncertainty_description,
            quality_flags, missing_data_definition, known_artifacts,
            representativeness_limits, quality_documentation_url
        ) VALUES (
            'QP-DW-V1', 'documented',
            'Validação descrita no artigo científico do produto; o catálogo oficial fornece probabilidades por classe e versões do algoritmo de inferência e do mascaramento de nuvens.',
            'Consultar o artigo descritor para métricas por classe e desenho de validação.',
            true, 'class_probability',
            'Nove bandas contínuas entre 0 e 1 expressam probabilidades estimadas; a banda label é o índice da maior probabilidade.',
            'dynamicworld_algorithm_version; qa_algorithm_version',
            'Pixels afetados por nuvens e sombras são mascarados; somente imagens com CLOUDY_PIXEL_PERCENTAGE <= 35% são processadas.',
            'Baixa probabilidade top-1 pode ocorrer em classes temporalmente dependentes e em superfícies espectralmente ambíguas; o produtor recomenda limiar de probabilidade para seleção confiante.',
            'Uma classe top-1 não é observação de campo e não deve ser interpretada sem considerar probabilidade, data, contexto espacial e finalidade analítica.',
            %s
        )
        ON CONFLICT (stable_id) DO UPDATE SET
            quality_status = EXCLUDED.quality_status,
            validation_design = EXCLUDED.validation_design,
            accuracy_metrics = EXCLUDED.accuracy_metrics,
            uncertainty_available = EXCLUDED.uncertainty_available,
            uncertainty_type = EXCLUDED.uncertainty_type,
            uncertainty_description = EXCLUDED.uncertainty_description,
            quality_flags = EXCLUDED.quality_flags,
            missing_data_definition = EXCLUDED.missing_data_definition,
            known_artifacts = EXCLUDED.known_artifacts,
            representativeness_limits = EXCLUDED.representativeness_limits,
            quality_documentation_url = EXCLUDED.quality_documentation_url,
            updated_at = now()
        """,
        (CATALOG_URL,),
    )
    spatial = connection.execute(
        "SELECT spatial_profile_id FROM catalog.spatial_profiles WHERE stable_id = 'SP-DW-V1'"
    ).fetchone()[0]
    temporal = connection.execute(
        "SELECT temporal_profile_id FROM catalog.temporal_profiles WHERE stable_id = 'TP-DW-V1'"
    ).fetchone()[0]
    quality = connection.execute(
        "SELECT quality_profile_id FROM catalog.quality_profiles WHERE stable_id = 'QP-DW-V1'"
    ).fetchone()[0]
    return spatial, temporal, quality


def upsert_variable(connection, stable_id: str, canonical: str, pt: str, en: str, definition: str, data_type: str, unit: str | None) -> int:
    connection.execute(
        """
        INSERT INTO catalog.variables (
            stable_id, canonical_name, display_name_pt, display_name_en,
            definition, phenomenon, object_observed, default_data_type,
            canonical_unit, vocabulary_reference_url
        ) VALUES (%s, %s, %s, %s, %s, 'uso e cobertura da terra',
                  'cobertura superficial inferida por pixel', %s, %s, %s)
        ON CONFLICT (stable_id) DO UPDATE SET
            canonical_name = EXCLUDED.canonical_name,
            display_name_pt = EXCLUDED.display_name_pt,
            display_name_en = EXCLUDED.display_name_en,
            definition = EXCLUDED.definition,
            phenomenon = EXCLUDED.phenomenon,
            object_observed = EXCLUDED.object_observed,
            default_data_type = EXCLUDED.default_data_type,
            canonical_unit = EXCLUDED.canonical_unit,
            vocabulary_reference_url = EXCLUDED.vocabulary_reference_url,
            updated_at = now()
        """,
        (stable_id, canonical, pt, en, definition, data_type, unit, CATALOG_URL),
    )
    return connection.execute(
        "SELECT variable_id FROM catalog.variables WHERE stable_id = %s", (stable_id,)
    ).fetchone()[0]


def link_product_variable(connection, release_id: int, variable_id: int, source_name: str, role: str, source_definition: str, data_type: str, method_id: int, spatial_id: int, temporal_id: int, quality_id: int, interpretation: str, non_interpretations: str) -> None:
    stable_id = f"PV-DW-{source_name.upper().replace('_', '-') }"
    connection.execute(
        """
        INSERT INTO catalog.product_variables (
            stable_id, release_id, variable_id, source_variable_name,
            variable_role, source_definition, unit, data_type, method_id,
            spatial_profile_id, temporal_profile_id, quality_profile_id,
            interpretation, scientific_potential, non_interpretations,
            aggregation_semantics, class_legend_url, review_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, 'reviewed')
        ON CONFLICT (release_id, source_variable_name) DO UPDATE SET
            variable_id = EXCLUDED.variable_id,
            variable_role = EXCLUDED.variable_role,
            source_definition = EXCLUDED.source_definition,
            unit = EXCLUDED.unit,
            data_type = EXCLUDED.data_type,
            method_id = EXCLUDED.method_id,
            spatial_profile_id = EXCLUDED.spatial_profile_id,
            temporal_profile_id = EXCLUDED.temporal_profile_id,
            quality_profile_id = EXCLUDED.quality_profile_id,
            interpretation = EXCLUDED.interpretation,
            scientific_potential = EXCLUDED.scientific_potential,
            non_interpretations = EXCLUDED.non_interpretations,
            aggregation_semantics = EXCLUDED.aggregation_semantics,
            class_legend_url = EXCLUDED.class_legend_url,
            review_status = EXCLUDED.review_status,
            updated_at = now()
        """,
        (
            stable_id, release_id, variable_id, source_name, role, source_definition,
            "probability" if role == "probability" else None, data_type, method_id,
            spatial_id, temporal_id, quality_id, interpretation,
            "Mapeamento exploratório, monitoramento, composição temporal explícita e análise de padrões de uso e cobertura da terra.",
            non_interpretations,
            "Probabilidades devem ser agregadas com método explícito; label é argmax por imagem e não deve ser tratado como frequência ou proporção sem transformação documentada.",
            CATALOG_URL,
        ),
    )


def upsert_citation(connection, product_id: int, release_id: int) -> None:
    row = connection.execute(
        "SELECT citation_id FROM catalog.citations WHERE doi = '10.1038/s41597-022-01307-4'"
    ).fetchone()
    if row:
        citation_id = row[0]
    else:
        citation_id = connection.execute(
            """
            INSERT INTO catalog.citations (
                citation_type, title, authors, publication_year,
                publisher_or_journal, doi, url, peer_reviewed, notes
            ) VALUES (
                'data_descriptor',
                'Dynamic World, Near real-time global 10 m land use land cover mapping',
                'Brown, C. F.; Brumby, S. P.; Guzder-Williams, B.; et al.',
                2022, 'Scientific Data', '10.1038/s41597-022-01307-4',
                %s, true, 'Artigo descritor e de validação do produto Dynamic World.'
            ) RETURNING citation_id
            """,
            (PAPER_URL,),
        ).fetchone()[0]
    connection.execute(
        """
        INSERT INTO catalog.product_citations (product_id, citation_id, relationship_type, is_primary)
        VALUES (%s, %s, 'describes_product', true)
        ON CONFLICT DO NOTHING
        """,
        (product_id, citation_id),
    )
    connection.execute(
        """
        INSERT INTO catalog.release_citations (release_id, citation_id, relationship_type, is_primary)
        VALUES (%s, %s, 'method_and_validation', true)
        ON CONFLICT DO NOTHING
        """,
        (release_id, citation_id),
    )


def upsert_assertions(connection) -> None:
    assertions = (
        ("product_release", "PR000011", "nominal_resolution", "10 m", "official_documentation"),
        ("product_release", "PR000011", "coverage_start", "2015-06-27", "official_documentation"),
        ("product_release", "PR000011", "source_imagery", "Sentinel-2 L1C with CLOUDY_PIXEL_PERCENTAGE <= 35%", "official_documentation"),
        ("product_release", "PR000011", "class_structure", "nine probability bands plus top-1 label", "official_documentation"),
        ("quality_profile", "QP-DW-V1", "uncertainty", "per-class estimated probabilities; top-1 confidence should be thresholded for confident selection", "official_documentation"),
        ("method", "MT-DW-V1", "cloud_masking", "S2 Cloud Probability, Cloud Displacement Index and Directional Distance Transform", "official_documentation"),
    )
    for entity_type, entity_id, field_name, value, evidence_type in assertions:
        connection.execute(
            """
            INSERT INTO catalog.metadata_assertions (
                entity_type, entity_stable_id, field_name, asserted_value,
                evidence_url, evidence_type, support_note, confidence, retrieved_at
            ) SELECT %s, %s, %s, %s, %s, %s,
                     'Afirmação verificada na documentação oficial do catálogo Dynamic World V1.',
                     'high', now()
            WHERE NOT EXISTS (
                SELECT 1 FROM catalog.metadata_assertions
                WHERE entity_type = %s AND entity_stable_id = %s
                  AND field_name = %s AND evidence_url = %s
            )
            """,
            (entity_type, entity_id, field_name, value, CATALOG_URL, evidence_type,
             entity_type, entity_id, field_name, CATALOG_URL),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    args = parser.parse_args()
    psycopg = import_psycopg()
    try:
        with psycopg.connect(args.database_url) as connection:
            product = connection.execute(
                "SELECT product_id FROM catalog.products WHERE stable_id = 'DP000011'"
            ).fetchone()
            release = connection.execute(
                "SELECT release_id FROM catalog.product_releases WHERE stable_id = 'PR000011'"
            ).fetchone()
            if not product or not release:
                raise ValueError("Dynamic World V1 deve ser promovido antes do enriquecimento")
            method_id = upsert_method(connection)
            spatial_id, temporal_id, quality_id = upsert_profiles(connection)
            for index, (source_name, pt, en, definition) in enumerate(BANDS, start=1):
                variable_id = upsert_variable(
                    connection, f"VR{index:06d}", f"dynamic_world_probability_{source_name}",
                    f"Probabilidade Dynamic World — {pt}", f"Dynamic World probability — {en}",
                    definition, "proportion", "1",
                )
                link_product_variable(
                    connection, release[0], variable_id, source_name, "probability",
                    definition, "float", method_id, spatial_id, temporal_id, quality_id,
                    f"Probabilidade estimada de cobertura completa pela classe {pt.lower()} no pixel e na aquisição correspondente.",
                    "Não é probabilidade frequentista calibrada para qualquer finalidade, proporção temporal, área da classe ou observação de campo.",
                )
            label_id = upsert_variable(
                connection, "VR000010", "dynamic_world_top1_label",
                "Rótulo Dynamic World de maior probabilidade", "Dynamic World top-1 label",
                "Índice inteiro de 0 a 8 da banda com a maior probabilidade estimada.",
                "nominal", None,
            )
            link_product_variable(
                connection, release[0], label_id, "label", "class_label",
                "Índice da banda com a maior probabilidade estimada.", "uint8",
                method_id, spatial_id, temporal_id, quality_id,
                "Classe top-1 para o pixel na aquisição correspondente.",
                "Não representa verdade de campo, classe anual, mudança validada nem confiança alta sem consulta às probabilidades.",
            )
            upsert_citation(connection, product[0], release[0])
            upsert_assertions(connection)
            connection.execute(
                """
                UPDATE catalog.curation_reviews
                SET review_status = 'in_progress',
                    findings = 'Identidade, dez bandas/variáveis, método, perfis espacial e temporal, qualidade, citação e evidências oficiais registrados.',
                    corrections_required = 'Auditar métricas de validação por classe no artigo e testar endpoints/ativos antes de aprovação final.',
                    updated_at = now()
                WHERE entity_type = 'product' AND entity_stable_id = 'DP000011'
                """
            )
            connection.commit()
            print("OK: Dynamic World V1 enriquecido com 10 variáveis e perfis científico-operacionais")
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
