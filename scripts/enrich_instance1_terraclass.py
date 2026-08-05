#!/usr/bin/env python3
"""Enrich TerraClass Amazônia 2020 in the normalized Instance 1 pilot."""
from __future__ import annotations

import argparse
import os
import sys

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
PROJECT_URL = "https://www.terraclass.gov.br/"
ACCURACY_URL = "https://www.terraclass.gov.br/acuracia-amz"
INPE_URL = (
    "https://www.gov.br/inpe/pt-br/area-conhecimento/unidade-amazonia/"
    "projetos-e-pesquisas/terraclass/terraclass"
)
OLOFSSON_DOI = "10.1016/j.rse.2014.02.015"
OLOFSSON_URL = f"https://doi.org/{OLOFSSON_DOI}"

CLASSES = (
    ("vegetacao_natural_florestal_secundaria", "Vegetação Natural Florestal Secundária"),
    ("silvicultura", "Silvicultura"),
    ("pastagem_arbustiva_arborea", "Pastagem Arbustiva/Arbórea"),
    ("pastagem_herbacea", "Pastagem Herbácea"),
    ("cultura_agricola_semiperene", "Cultura Agrícola Semiperene"),
    ("cultura_agricola_temporaria_1_ciclo", "Cultura Agrícola Temporária de 1 Ciclo"),
    ("cultura_agricola_temporaria_mais_1_ciclo", "Cultura Agrícola Temporária de Mais de 1 Ciclo"),
    ("mineracao", "Mineração"),
    ("urbanizada", "Urbanizada"),
)

ACCURACY_SUMMARY = (
    "Exatidão global 85,89% (IC ±1,84%). EP/EU por classe: "
    "vegetação secundária 83±4/96±2; silvicultura 46±21/97±3; "
    "pastagem arbustiva/arbórea 75±6/63±5; pastagem herbácea 91±2/88±3; "
    "cultura semiperene 94±9/98±3; temporária 1 ciclo 65±18/85±6; "
    "temporária >1 ciclo 95±5/97±2; mineração 100/97±4; urbanizada 81±25/98±3."
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


def update_product(connection) -> tuple[int, int]:
    connection.execute(
        """
        UPDATE catalog.products SET
          product_description=%s, scientific_object=%s, information_message=%s,
          intended_uses=%s, non_representations=%s, primary_or_derived='classified',
          geographic_coverage_text=%s, official_product_page_url=%s,
          methodology_url=%s, limitations_summary=%s, updated_at=now()
        WHERE stable_id='DP000005'
        """,
        (
            "Mapeamento temático de cobertura e uso da terra associado à qualificação das áreas "
            "desflorestadas identificadas pelo PRODES no bioma Amazônia, ano-base 2020.",
            "Classe temática de cobertura e uso da terra atribuída a unidades espaciais mapeadas "
            "no contexto do TerraClass Amazônia 2020.",
            "Informa a classe de cobertura ou uso da terra mapeada para 2020, preservando a relação "
            "metodológica com a qualificação de áreas desflorestadas pelo PRODES.",
            "Análise da ocupação de áreas desflorestadas, dinâmica de usos agropecuários, vegetação "
            "secundária e apoio a políticas territoriais.",
            "Não mede diretamente carbono, biodiversidade, produtividade, causalidade do "
            "desflorestamento, data exata da conversão ou condição de campo sem erro de classificação.",
            "Bioma Amazônia brasileiro, no universo e nas categorias espaciais definidos pelo projeto.",
            PROJECT_URL,
            INPE_URL,
            "A interpretação depende da legenda do release, do universo efetivamente mapeado, da "
            "matriz de erro e da distinção entre área mapeada e área ajustada por acurácia.",
        ),
    )
    connection.execute(
        """
        UPDATE catalog.product_releases SET
          valid_from=DATE '2020-01-01', valid_to=DATE '2020-12-31',
          temporal_coverage_text='Ano-base 2020', change_summary=%s,
          release_notes_url=%s, updated_at=now()
        WHERE stable_id='PR000005'
        """,
        ("Release anual do mapeamento TerraClass Amazônia 2020.", PROJECT_URL),
    )
    return (
        one_id(connection, "products", "DP000005", "product_id"),
        one_id(connection, "product_releases", "PR000005", "release_id"),
    )


def upsert_profiles(connection) -> tuple[int, int, int, int]:
    connection.execute(
        """
        INSERT INTO catalog.methods (
          stable_id, method_name, method_type, description, input_data,
          processing_summary, validation_summary, method_version,
          methodology_url, limitations
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (stable_id) DO UPDATE SET
          method_name=EXCLUDED.method_name, method_type=EXCLUDED.method_type,
          description=EXCLUDED.description, input_data=EXCLUDED.input_data,
          processing_summary=EXCLUDED.processing_summary,
          validation_summary=EXCLUDED.validation_summary,
          method_version=EXCLUDED.method_version,
          methodology_url=EXCLUDED.methodology_url,
          limitations=EXCLUDED.limitations, updated_at=now()
        """,
        (
            "MT-TC-AMZ-2020", "TerraClass Amazônia 2020",
            "remote_sensing_classification",
            "Classificação temática de cobertura e uso da terra para qualificar áreas "
            "desflorestadas delimitadas pelo PRODES.",
            "Áreas de desflorestamento PRODES e imagens orbitais usadas pelo projeto.",
            "Sensoriamento remoto e geoprocessamento para atribuição de classes temáticas; o "
            "catálogo não presume tamanho nominal de pixel sem metadado direto do ativo.",
            "Acurácia avaliada por amostragem e matriz de erro segundo Olofsson et al. (2014).",
            "Amazônia 2020", INPE_URL,
            "Classes e universo espacial dependem do release; diferenças de legenda entre gerações "
            "não devem ser harmonizadas silenciosamente.",
        ),
    )
    connection.execute(
        """
        INSERT INTO catalog.spatial_profiles (
          stable_id, support_type, support_description, geometry_type,
          nominal_resolution_value, nominal_resolution_unit, crs, grid_definition,
          geographic_coverage_text, spatial_biases, spatial_limitations
        ) VALUES (%s,%s,%s,%s,NULL,NULL,%s,%s,%s,%s,%s)
        ON CONFLICT (stable_id) DO UPDATE SET
          support_type=EXCLUDED.support_type,
          support_description=EXCLUDED.support_description,
          geometry_type=EXCLUDED.geometry_type,
          nominal_resolution_value=NULL, nominal_resolution_unit=NULL,
          crs=EXCLUDED.crs, grid_definition=EXCLUDED.grid_definition,
          geographic_coverage_text=EXCLUDED.geographic_coverage_text,
          spatial_biases=EXCLUDED.spatial_biases,
          spatial_limitations=EXCLUDED.spatial_limitations, updated_at=now()
        """,
        (
            "SP-TC-AMZ-2020", "pixel",
            "Unidade raster categórica; tamanho nominal do pixel permanece não documentado no "
            "catálogo até inspeção direta do metadado do ativo.",
            "raster", "não verificado", "grade do ativo oficial a verificar",
            "Bioma Amazônia brasileiro, conforme universo espacial do TerraClass 2020.",
            "Erros de borda, mistura espectral e desigualdade de desempenho entre classes.",
            "A cobertura não deve ser inferida como mapeamento independente e homogêneo de todo o "
            "bioma sem consulta à documentação do release.",
        ),
    )
    connection.execute(
        """
        INSERT INTO catalog.temporal_profiles (
          stable_id, representation_type, support_description, coverage_start,
          coverage_end, temporal_resolution, observation_window, update_frequency,
          calendar_definition, temporal_aggregation, temporal_limitations
        ) VALUES (%s,%s,%s,DATE '2020-01-01',DATE '2020-12-31',%s,%s,%s,%s,%s,%s)
        ON CONFLICT (stable_id) DO UPDATE SET
          representation_type=EXCLUDED.representation_type,
          support_description=EXCLUDED.support_description,
          coverage_start=EXCLUDED.coverage_start, coverage_end=EXCLUDED.coverage_end,
          temporal_resolution=EXCLUDED.temporal_resolution,
          observation_window=EXCLUDED.observation_window,
          update_frequency=EXCLUDED.update_frequency,
          calendar_definition=EXCLUDED.calendar_definition,
          temporal_aggregation=EXCLUDED.temporal_aggregation,
          temporal_limitations=EXCLUDED.temporal_limitations, updated_at=now()
        """,
        (
            "TP-TC-AMZ-2020", "annual",
            "Classe temática representativa do ano-base 2020.", "ano-base",
            "janela de observação e composição definida pelo método do release",
            "edições periódicas, não necessariamente anuais", "ano civil de referência",
            "classe categórica do mapeamento anual",
            "O ano-base não fornece data exata de mudança nem prova persistência intra-anual.",
        ),
    )
    connection.execute(
        """
        INSERT INTO catalog.quality_profiles (
          stable_id, quality_status, validation_design, accuracy_metrics,
          uncertainty_available, uncertainty_type, uncertainty_description,
          quality_flags, missing_data_definition, collection_bias, known_artifacts,
          representativeness_limits, quality_documentation_url
        ) VALUES (%s,%s,%s,%s,true,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (stable_id) DO UPDATE SET
          quality_status=EXCLUDED.quality_status,
          validation_design=EXCLUDED.validation_design,
          accuracy_metrics=EXCLUDED.accuracy_metrics,
          uncertainty_available=EXCLUDED.uncertainty_available,
          uncertainty_type=EXCLUDED.uncertainty_type,
          uncertainty_description=EXCLUDED.uncertainty_description,
          quality_flags=EXCLUDED.quality_flags,
          missing_data_definition=EXCLUDED.missing_data_definition,
          collection_bias=EXCLUDED.collection_bias,
          known_artifacts=EXCLUDED.known_artifacts,
          representativeness_limits=EXCLUDED.representativeness_limits,
          quality_documentation_url=EXCLUDED.quality_documentation_url,
          updated_at=now()
        """,
        (
            "QP-TC-AMZ-2020", "documented",
            "Amostragem e estimativa de exatidão/área seguindo Olofsson et al. (2014).",
            ACCURACY_SUMMARY, "classification_error_and_area_estimation",
            "Exatidão global, intervalos de confiança, exatidão do produtor e do usuário por classe.",
            "Consultar EP, EU e intervalos por classe; mineração não apresenta IC de EP na tabela oficial.",
            "Área não observada e categorias auxiliares devem ser tratadas segundo a legenda do ativo.",
            "Desempenho heterogêneo entre classes, especialmente silvicultura, pastagem "
            "arbustiva/arbórea e agricultura temporária de um ciclo.",
            "Confusão temática, limites de interpretação visual e efeitos da amostragem.",
            "As métricas se aplicam ao desenho de validação de 2020 e não transformam cada pixel "
            "em observação sem incerteza.", ACCURACY_URL,
        ),
    )
    return (
        one_id(connection, "methods", "MT-TC-AMZ-2020", "method_id"),
        one_id(connection, "spatial_profiles", "SP-TC-AMZ-2020", "spatial_profile_id"),
        one_id(connection, "temporal_profiles", "TP-TC-AMZ-2020", "temporal_profile_id"),
        one_id(connection, "quality_profiles", "QP-TC-AMZ-2020", "quality_profile_id"),
    )


def upsert_variable(connection, release_id: int, method_id: int, spatial_id: int,
                    temporal_id: int, quality_id: int) -> None:
    connection.execute(
        """
        INSERT INTO catalog.variables (
          stable_id, canonical_name, display_name_pt, display_name_en, definition,
          phenomenon, object_observed, population_or_universe, default_data_type,
          canonical_unit, vocabulary_reference_url
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,%s)
        ON CONFLICT (stable_id) DO UPDATE SET
          canonical_name=EXCLUDED.canonical_name,
          display_name_pt=EXCLUDED.display_name_pt,
          display_name_en=EXCLUDED.display_name_en,
          definition=EXCLUDED.definition, phenomenon=EXCLUDED.phenomenon,
          object_observed=EXCLUDED.object_observed,
          population_or_universe=EXCLUDED.population_or_universe,
          default_data_type=EXCLUDED.default_data_type,
          canonical_unit=NULL,
          vocabulary_reference_url=EXCLUDED.vocabulary_reference_url,
          updated_at=now()
        """,
        (
            "VR000011", "terraclass_amazonia_2020_land_cover_use_class",
            "Classe de cobertura e uso da terra — TerraClass Amazônia 2020",
            "Land cover and land use class — TerraClass Amazon 2020",
            "Categoria temática atribuída à unidade espacial no release TerraClass Amazônia 2020.",
            "cobertura e uso da terra", "classe temática mapeada",
            "unidades espaciais do universo TerraClass Amazônia 2020", "nominal", PROJECT_URL,
        ),
    )
    variable_id = one_id(connection, "variables", "VR000011", "variable_id")
    connection.execute(
        """
        INSERT INTO catalog.product_variables (
          stable_id, release_id, variable_id, source_variable_name, variable_role,
          source_definition, unit, data_type, method_id, spatial_profile_id,
          temporal_profile_id, quality_profile_id, interpretation,
          scientific_potential, non_interpretations, aggregation_semantics,
          class_legend_url, review_status
        ) VALUES (%s,%s,%s,%s,%s,%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (release_id, source_variable_name) DO UPDATE SET
          variable_id=EXCLUDED.variable_id, variable_role=EXCLUDED.variable_role,
          source_definition=EXCLUDED.source_definition, unit=NULL,
          data_type=EXCLUDED.data_type, method_id=EXCLUDED.method_id,
          spatial_profile_id=EXCLUDED.spatial_profile_id,
          temporal_profile_id=EXCLUDED.temporal_profile_id,
          quality_profile_id=EXCLUDED.quality_profile_id,
          interpretation=EXCLUDED.interpretation,
          scientific_potential=EXCLUDED.scientific_potential,
          non_interpretations=EXCLUDED.non_interpretations,
          aggregation_semantics=EXCLUDED.aggregation_semantics,
          class_legend_url=EXCLUDED.class_legend_url,
          review_status=EXCLUDED.review_status, updated_at=now()
        """,
        (
            "PV-TC-AMZ-2020-CLASS", release_id, variable_id, "class", "class_label",
            "Classe temática do mapeamento TerraClass Amazônia 2020.", "categorical",
            method_id, spatial_id, temporal_id, quality_id,
            "Uso ou cobertura da terra mapeado para a unidade espacial no ano-base 2020.",
            "Análise espacial e estatística das classes, respeitando validação e legenda.",
            "Não é medição direta de manejo, carbono, biodiversidade ou causalidade.",
            "Áreas por classe devem declarar se são mapeadas ou ajustadas por matriz de erro.",
            PROJECT_URL, "reviewed",
        ),
    )
    for code, label in CLASSES:
        term_id = int(connection.execute(
            """
            INSERT INTO catalog.taxonomy_terms (
              scheme, term_code, preferred_label_pt, preferred_label_en,
              definition, vocabulary_url
            ) VALUES (%s,%s,%s,NULL,%s,%s)
            ON CONFLICT (scheme, term_code) DO UPDATE SET
              preferred_label_pt=EXCLUDED.preferred_label_pt,
              definition=EXCLUDED.definition,
              vocabulary_url=EXCLUDED.vocabulary_url
            RETURNING term_id
            """,
            (
                "terraclass_amazonia_2020_accuracy_classes", code, label,
                f"Classe avaliada na tabela oficial de acurácia de 2020: {label}.", ACCURACY_URL,
            ),
        ).fetchone()[0])
        connection.execute(
            "INSERT INTO catalog.variable_terms (variable_id, term_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
            (variable_id, term_id),
        )


def add_assertions(connection) -> None:
    rows = (
        ("product", "DP000005", "scientific_scope",
         "qualificação de cobertura e uso vinculada a áreas desflorestadas do PRODES",
         INPE_URL, "official_page"),
        ("release", "PR000005", "year_base", "2020", ACCURACY_URL, "official_page"),
        ("release", "PR000005", "overall_accuracy", "85,89%", ACCURACY_URL, "official_page"),
        ("release", "PR000005", "overall_accuracy_confidence_interval", "±1,84%",
         ACCURACY_URL, "official_page"),
        ("quality_profile", "QP-TC-AMZ-2020", "validation_protocol",
         "Olofsson et al. 2014", ACCURACY_URL, "official_page"),
        ("quality_profile", "QP-TC-AMZ-2020", "class_accuracy_metrics",
         ACCURACY_SUMMARY, ACCURACY_URL, "official_page"),
        ("spatial_profile", "SP-TC-AMZ-2020", "nominal_pixel_size",
         "não promovido; requer inspeção direta do metadado do ativo",
         PROJECT_URL, "curatorial_inference"),
    )
    for entity_type, entity_id, field_name, value, url, evidence_type in rows:
        connection.execute(
            """
            INSERT INTO catalog.metadata_assertions (
              entity_type, entity_stable_id, field_name, asserted_value,
              evidence_url, evidence_type, support_note, confidence, retrieved_at
            ) SELECT %s,%s,%s,%s,%s,%s,%s,%s,now()
            WHERE NOT EXISTS (
              SELECT 1 FROM catalog.metadata_assertions
              WHERE entity_type=%s AND entity_stable_id=%s
                AND field_name=%s AND evidence_url=%s
            )
            """,
            (
                entity_type, entity_id, field_name, value, url, evidence_type,
                "Verificado em fonte oficial; inferências permanecem rotuladas.",
                "medium" if evidence_type == "curatorial_inference" else "high",
                entity_type, entity_id, field_name, url,
            ),
        )


def add_citation(connection, product_id: int, release_id: int) -> None:
    row = connection.execute(
        "SELECT citation_id FROM catalog.citations WHERE doi=%s", (OLOFSSON_DOI,)
    ).fetchone()
    if row:
        citation_id = int(row[0])
    else:
        citation_id = int(connection.execute(
            """
            INSERT INTO catalog.citations (
              citation_type,title,authors,publication_year,publisher_or_journal,
              doi,url,peer_reviewed,notes
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,true,%s)
            RETURNING citation_id
            """,
            (
                "validation",
                "Good practices for estimating area and assessing accuracy of land change",
                "Olofsson, P.; Foody, G. M.; Herold, M.; et al.", 2014,
                "Remote Sensing of Environment", OLOFSSON_DOI, OLOFSSON_URL,
                "Protocolo citado pela página oficial de acurácia TerraClass.",
            ),
        ).fetchone()[0])
    connection.execute(
        "INSERT INTO catalog.product_citations VALUES (%s,%s,%s,false) ON CONFLICT DO NOTHING",
        (product_id, citation_id, "validation_protocol"),
    )
    connection.execute(
        "INSERT INTO catalog.release_citations VALUES (%s,%s,%s,true) ON CONFLICT DO NOTHING",
        (release_id, citation_id, "validation_protocol"),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DATABASE_URL)
    args = parser.parse_args()
    psycopg = psycopg_module()
    try:
        with psycopg.connect(args.database_url) as connection:
            product_id, release_id = update_product(connection)
            method_id, spatial_id, temporal_id, quality_id = upsert_profiles(connection)
            upsert_variable(connection, release_id, method_id, spatial_id, temporal_id, quality_id)
            add_assertions(connection)
            add_citation(connection, product_id, release_id)
            connection.execute(
                """
                UPDATE catalog.curation_reviews SET
                  review_status='in_progress', findings=%s,
                  corrections_required=%s, reviewed_at=now()
                WHERE entity_type='product' AND entity_stable_id='DP000005'
                """,
                (
                    "Variável categórica, nove classes avaliadas, método, perfis, métricas de "
                    "acurácia, protocolo e evidências oficiais registrados.",
                    "Inspecionar metadado direto do GeoTIFF para pixel, CRS, grade, códigos "
                    "integrais da legenda e teste de acesso antes da aprovação final.",
                ),
            )
            connection.commit()
        print("OK: TerraClass Amazônia 2020 enriquecido com perfil científico e qualidade")
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
