#!/usr/bin/env python3
"""Idempotently enrich Dynamic World V1 in the normalized Instance 1 pilot."""
from __future__ import annotations

import argparse
import os
import sys

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
CATALOG_URL = "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1"
PAPER_URL = "https://doi.org/10.1038/s41597-022-01307-4"

BANDS = (
    ("water", "Água", "water"),
    ("trees", "Árvores", "trees"),
    ("grass", "Gramíneas", "grass"),
    ("flooded_vegetation", "Vegetação inundada", "flooded vegetation"),
    ("crops", "Cultivos", "crops"),
    ("shrub_and_scrub", "Arbustos e vegetação arbustiva", "shrub and scrub"),
    ("built", "Área construída", "built"),
    ("bare", "Superfície exposta", "bare"),
    ("snow_and_ice", "Neve e gelo", "snow and ice"),
)


def psycopg_module():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit("Instale database/requirements.txt") from exc
    return psycopg


def one_id(connection, table: str, stable_id: str, id_column: str) -> int:
    row = connection.execute(
        f"SELECT {id_column} FROM catalog.{table} WHERE stable_id = %s", (stable_id,)
    ).fetchone()
    if not row:
        raise ValueError(f"registro ausente: {table}/{stable_id}")
    return int(row[0])


def upsert_profiles(connection) -> tuple[int, int, int, int]:
    connection.execute(
        """
        INSERT INTO catalog.methods (
          stable_id, method_name, method_type, description, input_data,
          processing_summary, validation_summary, method_version,
          methodology_url, limitations
        ) VALUES (
          'MT-DW-V1', 'Dynamic World V1 inference',
          'remote_sensing_classification',
          'Classificação quase em tempo real de uso e cobertura da terra por imagem Sentinel-2 individual.',
          'Sentinel-2 L1C com CLOUDY_PIXEL_PERCENTAGE <= 35%.',
          'Produz nove probabilidades que somam 1 e um rótulo top-1; nuvens e sombras são mascaradas com S2 Cloud Probability, Cloud Displacement Index e Directional Distance Transform.',
          'Desenho de validação e métricas descritos no artigo científico do produto.',
          'V1', %s,
          'Classes dependentes de persistência temporal e superfícies espectralmente ambíguas podem apresentar baixa probabilidade top-1; composições temporais exigem processamento explícito.'
        ) ON CONFLICT (stable_id) DO UPDATE SET
          description=EXCLUDED.description, input_data=EXCLUDED.input_data,
          processing_summary=EXCLUDED.processing_summary,
          validation_summary=EXCLUDED.validation_summary,
          methodology_url=EXCLUDED.methodology_url,
          limitations=EXCLUDED.limitations, updated_at=now()
        """,
        (PAPER_URL,),
    )
    connection.execute(
        """
        INSERT INTO catalog.spatial_profiles (
          stable_id, support_type, support_description, geometry_type,
          nominal_resolution_value, nominal_resolution_unit, crs,
          grid_definition, geographic_coverage_text, spatial_limitations
        ) VALUES (
          'SP-DW-V1', 'pixel',
          'Pixel de predição correspondente a uma aquisição Sentinel-2 L1C elegível.',
          'raster', 10, 'm', 'grade do Sentinel-2 de origem',
          'A imagem Dynamic World corresponde ao ativo Sentinel-2 L1C de origem.',
          'Global, incluindo o Brasil.',
          'Resolução nominal de 10 m não equivale a observação de campo nem elimina mistura espectral.'
        ) ON CONFLICT (stable_id) DO UPDATE SET
          support_description=EXCLUDED.support_description,
          nominal_resolution_value=EXCLUDED.nominal_resolution_value,
          nominal_resolution_unit=EXCLUDED.nominal_resolution_unit,
          crs=EXCLUDED.crs, grid_definition=EXCLUDED.grid_definition,
          geographic_coverage_text=EXCLUDED.geographic_coverage_text,
          spatial_limitations=EXCLUDED.spatial_limitations, updated_at=now()
        """
    )
    connection.execute(
        """
        INSERT INTO catalog.temporal_profiles (
          stable_id, representation_type, support_description, coverage_start,
          temporal_resolution, observation_window, update_frequency,
          temporal_aggregation, temporal_limitations
        ) VALUES (
          'TP-DW-V1', 'event',
          'Cada imagem corresponde a uma aquisição Sentinel-2 L1C elegível.',
          DATE '2015-06-27', 'por aquisição elegível',
          'data e janela da aquisição Sentinel-2 de origem',
          'quase em tempo real; revisita típica de 2 a 5 dias conforme latitude',
          'nenhuma composição temporal embutida',
          'Uma imagem individual não representa classe anual, persistência ou transição validada.'
        ) ON CONFLICT (stable_id) DO UPDATE SET
          support_description=EXCLUDED.support_description,
          coverage_start=EXCLUDED.coverage_start,
          temporal_resolution=EXCLUDED.temporal_resolution,
          observation_window=EXCLUDED.observation_window,
          update_frequency=EXCLUDED.update_frequency,
          temporal_aggregation=EXCLUDED.temporal_aggregation,
          temporal_limitations=EXCLUDED.temporal_limitations, updated_at=now()
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
          'Validação descrita no artigo científico; documentação oficial expõe probabilidades e versões dos algoritmos.',
          'Consultar o artigo descritor para métricas por classe.',
          true, 'class_probability',
          'Nove bandas de probabilidade entre 0 e 1; label é o índice da maior probabilidade.',
          'dynamicworld_algorithm_version; qa_algorithm_version',
          'Nuvens e sombras são mascaradas; somente cenas com CLOUDY_PIXEL_PERCENTAGE <= 35% são processadas.',
          'Baixa confiança em classes temporalmente dependentes e superfícies espectralmente ambíguas; o produtor recomenda limiar top-1.',
          'O rótulo top-1 não é verdade de campo e deve ser interpretado com probabilidade, data e contexto.',
          %s
        ) ON CONFLICT (stable_id) DO UPDATE SET
          validation_design=EXCLUDED.validation_design,
          accuracy_metrics=EXCLUDED.accuracy_metrics,
          uncertainty_available=EXCLUDED.uncertainty_available,
          uncertainty_type=EXCLUDED.uncertainty_type,
          uncertainty_description=EXCLUDED.uncertainty_description,
          quality_flags=EXCLUDED.quality_flags,
          missing_data_definition=EXCLUDED.missing_data_definition,
          known_artifacts=EXCLUDED.known_artifacts,
          representativeness_limits=EXCLUDED.representativeness_limits,
          quality_documentation_url=EXCLUDED.quality_documentation_url,
          updated_at=now()
        """,
        (CATALOG_URL,),
    )
    return (
        one_id(connection, "methods", "MT-DW-V1", "method_id"),
        one_id(connection, "spatial_profiles", "SP-DW-V1", "spatial_profile_id"),
        one_id(connection, "temporal_profiles", "TP-DW-V1", "temporal_profile_id"),
        one_id(connection, "quality_profiles", "QP-DW-V1", "quality_profile_id"),
    )


def upsert_variable(connection, stable_id: str, canonical: str, pt: str, en: str,
                    definition: str, data_type: str, unit: str | None) -> int:
    connection.execute(
        """
        INSERT INTO catalog.variables (
          stable_id, canonical_name, display_name_pt, display_name_en,
          definition, phenomenon, object_observed, default_data_type,
          canonical_unit, vocabulary_reference_url
        ) VALUES (%s,%s,%s,%s,%s,'uso e cobertura da terra',
                  'cobertura superficial inferida por pixel',%s,%s,%s)
        ON CONFLICT (stable_id) DO UPDATE SET
          canonical_name=EXCLUDED.canonical_name,
          display_name_pt=EXCLUDED.display_name_pt,
          display_name_en=EXCLUDED.display_name_en,
          definition=EXCLUDED.definition,
          default_data_type=EXCLUDED.default_data_type,
          canonical_unit=EXCLUDED.canonical_unit,
          vocabulary_reference_url=EXCLUDED.vocabulary_reference_url,
          updated_at=now()
        """,
        (stable_id, canonical, pt, en, definition, data_type, unit, CATALOG_URL),
    )
    return one_id(connection, "variables", stable_id, "variable_id")


def link_variable(connection, release_id: int, variable_id: int, source_name: str,
                  role: str, definition: str, data_type: str,
                  method_id: int, spatial_id: int, temporal_id: int,
                  quality_id: int, interpretation: str, non_interpretations: str) -> None:
    connection.execute(
        """
        INSERT INTO catalog.product_variables (
          stable_id, release_id, variable_id, source_variable_name,
          variable_role, source_definition, unit, data_type, method_id,
          spatial_profile_id, temporal_profile_id, quality_profile_id,
          interpretation, scientific_potential, non_interpretations,
          aggregation_semantics, class_legend_url, review_status
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                  'Exploração e monitoramento com processamento temporal explicitamente documentado.',
                  %s,
                  'Probabilidades requerem regra explícita de agregação; label é argmax por aquisição.',
                  %s,'reviewed')
        ON CONFLICT (release_id, source_variable_name) DO UPDATE SET
          variable_id=EXCLUDED.variable_id, variable_role=EXCLUDED.variable_role,
          source_definition=EXCLUDED.source_definition, unit=EXCLUDED.unit,
          data_type=EXCLUDED.data_type, method_id=EXCLUDED.method_id,
          spatial_profile_id=EXCLUDED.spatial_profile_id,
          temporal_profile_id=EXCLUDED.temporal_profile_id,
          quality_profile_id=EXCLUDED.quality_profile_id,
          interpretation=EXCLUDED.interpretation,
          non_interpretations=EXCLUDED.non_interpretations,
          aggregation_semantics=EXCLUDED.aggregation_semantics,
          class_legend_url=EXCLUDED.class_legend_url,
          review_status=EXCLUDED.review_status, updated_at=now()
        """,
        (
            f"PV-DW-{source_name.upper().replace('_','-')}", release_id, variable_id,
            source_name, role, definition, "1" if role == "probability" else None,
            data_type, method_id, spatial_id, temporal_id, quality_id,
            interpretation, non_interpretations, CATALOG_URL,
        ),
    )


def add_assertions(connection) -> None:
    rows = (
        ("release", "PR000011", "nominal_resolution", "10 m"),
        ("release", "PR000011", "coverage_start", "2015-06-27"),
        ("release", "PR000011", "source_imagery", "Sentinel-2 L1C; CLOUDY_PIXEL_PERCENTAGE <= 35%"),
        ("release", "PR000011", "class_structure", "nine probability bands plus top-1 label"),
        ("quality_profile", "QP-DW-V1", "uncertainty", "per-class estimated probabilities; threshold top-1 for confident selection"),
        ("method", "MT-DW-V1", "cloud_masking", "S2 Cloud Probability, Cloud Displacement Index and Directional Distance Transform"),
    )
    for entity_type, entity_id, field_name, value in rows:
        connection.execute(
            """
            INSERT INTO catalog.metadata_assertions (
              entity_type, entity_stable_id, field_name, asserted_value,
              evidence_url, evidence_type, support_note, confidence, retrieved_at
            ) SELECT %s,%s,%s,%s,%s,'official_documentation',
                     'Verificado na documentação oficial Dynamic World V1.',
                     'high',now()
              WHERE NOT EXISTS (
                SELECT 1 FROM catalog.metadata_assertions
                WHERE entity_type=%s AND entity_stable_id=%s
                  AND field_name=%s AND evidence_url=%s
              )
            """,
            (entity_type, entity_id, field_name, value, CATALOG_URL,
             entity_type, entity_id, field_name, CATALOG_URL),
        )


def add_citation(connection, product_id: int, release_id: int) -> None:
    row = connection.execute(
        "SELECT citation_id FROM catalog.citations WHERE doi='10.1038/s41597-022-01307-4'"
    ).fetchone()
    if row:
        citation_id = int(row[0])
    else:
        citation_id = int(connection.execute(
            """
            INSERT INTO catalog.citations (
              citation_type,title,authors,publication_year,publisher_or_journal,
              doi,url,peer_reviewed,notes
            ) VALUES (
              'data_descriptor',
              'Dynamic World, Near real-time global 10 m land use land cover mapping',
              'Brown, C. F.; Brumby, S. P.; Guzder-Williams, B.; et al.',
              2022,'Scientific Data','10.1038/s41597-022-01307-4',%s,true,
              'Artigo descritor e de validação do produto.'
            ) RETURNING citation_id
            """,
            (PAPER_URL,),
        ).fetchone()[0])
    connection.execute(
        "INSERT INTO catalog.product_citations VALUES (%s,%s,'describes_product',true) ON CONFLICT DO NOTHING",
        (product_id, citation_id),
    )
    connection.execute(
        "INSERT INTO catalog.release_citations VALUES (%s,%s,'method_and_validation',true) ON CONFLICT DO NOTHING",
        (release_id, citation_id),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DATABASE_URL)
    args = parser.parse_args()
    psycopg = psycopg_module()
    try:
        with psycopg.connect(args.database_url) as connection:
            product_id = one_id(connection, "products", "DP000011", "product_id")
            release_id = one_id(connection, "product_releases", "PR000011", "release_id")
            method_id, spatial_id, temporal_id, quality_id = upsert_profiles(connection)
            for idx, (source_name, pt, en) in enumerate(BANDS, start=1):
                definition = f"Probabilidade estimada de cobertura completa pela classe {pt.lower()}."
                variable_id = upsert_variable(
                    connection, f"VR{idx:06d}",
                    f"dynamic_world_probability_{source_name}",
                    f"Probabilidade Dynamic World — {pt}",
                    f"Dynamic World probability — {en}",
                    definition, "proportion", "1",
                )
                link_variable(
                    connection, release_id, variable_id, source_name, "probability",
                    definition, "float", method_id, spatial_id, temporal_id, quality_id,
                    f"Probabilidade estimada para {pt.lower()} no pixel e na aquisição correspondente.",
                    "Não é proporção temporal, área da classe, observação de campo ou confiança universalmente calibrada.",
                )
            label_id = upsert_variable(
                connection, "VR000010", "dynamic_world_top1_label",
                "Rótulo Dynamic World de maior probabilidade", "Dynamic World top-1 label",
                "Índice inteiro de 0 a 8 da classe com maior probabilidade estimada.",
                "nominal", None,
            )
            link_variable(
                connection, release_id, label_id, "label", "class_label",
                "Índice da banda com maior probabilidade estimada.", "uint8",
                method_id, spatial_id, temporal_id, quality_id,
                "Classe top-1 no pixel e na aquisição correspondente.",
                "Não representa verdade de campo, classe anual ou mudança validada sem análise temporal e local.",
            )
            add_assertions(connection)
            add_citation(connection, product_id, release_id)
            connection.execute(
                """
                UPDATE catalog.curation_reviews SET
                  review_status='in_progress',
                  findings='Dez bandas, método, perfis espacial/temporal, qualidade, citação e evidências oficiais registrados.',
                  corrections_required='Auditar métricas por classe no artigo e testar endpoints/ativos antes da aprovação final.'
                WHERE entity_type='product' AND entity_stable_id='DP000011'
                """
            )
            connection.commit()
        print("OK: Dynamic World V1 enriquecido com 10 variáveis e perfis auditáveis")
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
