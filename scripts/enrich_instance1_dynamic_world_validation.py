#!/usr/bin/env python3
"""Idempotently consolidate primary validation evidence for Dynamic World V1."""
from __future__ import annotations

import argparse
import os
import sys

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)
PAPER_URL = "https://doi.org/10.1038/s41597-022-01307-4"


def psycopg_module():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit("Instale database/requirements.txt") from exc
    return psycopg


def require_one(connection, query: str, params: tuple[object, ...], label: str):
    row = connection.execute(query, params).fetchone()
    if not row:
        raise ValueError(f"registro ausente: {label}")
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DATABASE_URL)
    args = parser.parse_args()
    psycopg = psycopg_module()

    accuracy = (
        "Concordância global de 73,8% entre rótulos top-1 de imagens individuais e "
        "o esquema Expert Consensus, avaliada em 409 tiles globais; concordância "
        "humano não especialista–especialista de 77,8%. Ao fundir grass e shrub & "
        "scrub para comparação com LCMAP, a concordância Dynamic World foi 74,2%. "
        "O artigo relata maior concordância para water, trees, built area e snow & "
        "ice; grass apresentou 30,1% e crops 88,9% no Expert Consensus."
    )
    validation_design = (
        "Validação primária com 409 tiles globais de 5,1 km × 5,1 km e anotações de "
        "especialistas. O esquema Expert Consensus inclui pixels com concordância de "
        "ao menos dois especialistas e totaliza 68.137.571 pixels avaliados. As "
        "comparações usam a predição Dynamic World da mesma data da imagem Sentinel-2."
    )
    limitations = (
        "As métricas são concordâncias com anotações e não probabilidades de correção "
        "por pixel. O desempenho varia espacial e temporalmente com mascaramento de "
        "nuvens e condição da cobertura. Há confusão relevante em classes transitórias "
        "ou espectralmente ambíguas, especialmente grass, flooded vegetation, shrub & "
        "scrub e bare; regiões áridas apresentam confusão crops–shrub. Comparações com "
        "produtos anuais exigem crosswalk de classes e podem envolver datas distintas."
    )

    try:
        with psycopg.connect(args.database_url) as connection:
            require_one(
                connection,
                "SELECT quality_profile_id FROM catalog.quality_profiles WHERE stable_id=%s",
                ("QP-DW-V1",),
                "quality_profiles/QP-DW-V1",
            )
            connection.execute(
                """
                UPDATE catalog.quality_profiles SET
                  validation_design=%s,
                  accuracy_metrics=%s,
                  known_artifacts=%s,
                  representativeness_limits=%s,
                  quality_documentation_url=%s,
                  updated_at=now()
                WHERE stable_id='QP-DW-V1'
                """,
                (validation_design, accuracy, limitations, limitations, PAPER_URL),
            )

            assertions = (
                ("validation_design", validation_design),
                ("overall_agreement_expert_consensus", "73.8%"),
                ("nonexpert_to_expert_agreement", "77.8%"),
                ("validation_tiles", "409 global tiles"),
                ("expert_consensus_pixels", "68137571"),
                ("grass_agreement_expert_consensus", "30.1%"),
                ("crops_agreement_expert_consensus", "88.9%"),
                ("merged_grass_shrub_agreement", "74.2%"),
                ("validation_limitations", limitations),
            )
            for field_name, asserted_value in assertions:
                connection.execute(
                    """
                    INSERT INTO catalog.metadata_assertions (
                      entity_type, entity_stable_id, field_name, asserted_value,
                      evidence_url, evidence_type, support_note, confidence, retrieved_at
                    ) SELECT
                      'quality_profile','QP-DW-V1',%s,%s,%s,'peer_reviewed_article',
                      'Verificado diretamente no artigo descritor e de validação do Dynamic World V1.',
                      'high',now()
                    WHERE NOT EXISTS (
                      SELECT 1 FROM catalog.metadata_assertions
                      WHERE entity_type='quality_profile'
                        AND entity_stable_id='QP-DW-V1'
                        AND field_name=%s
                        AND evidence_url=%s
                    )
                    """,
                    (field_name, asserted_value, PAPER_URL, field_name, PAPER_URL),
                )

            connection.execute(
                """
                UPDATE catalog.curation_reviews SET
                  review_status='in_progress',
                  findings='Dez bandas, método, perfis espacial e temporal, qualidade, citação e métricas primárias de validação do artigo registrados.',
                  corrections_required='Testar endpoints, ativos, licença operacional e comportamento de acesso antes da aprovação final.'
                WHERE entity_type='product' AND entity_stable_id='DP000011'
                """
            )

            row = require_one(
                connection,
                "SELECT validation_design, accuracy_metrics FROM catalog.quality_profiles WHERE stable_id=%s",
                ("QP-DW-V1",),
                "quality_profiles/QP-DW-V1 após atualização",
            )
            if "73,8%" not in row[1] or "409 tiles" not in row[0]:
                raise ValueError("métricas primárias Dynamic World não persistidas")
            count = connection.execute(
                """
                SELECT count(*) FROM catalog.metadata_assertions
                WHERE entity_type='quality_profile'
                  AND entity_stable_id='QP-DW-V1'
                  AND evidence_url=%s
                  AND evidence_type='peer_reviewed_article'
                """,
                (PAPER_URL,),
            ).fetchone()[0]
            if count != len(assertions):
                raise ValueError(f"esperadas {len(assertions)} afirmações primárias; obtidas {count}")
            connection.commit()

        print("OK: validação primária do Dynamic World V1 consolidada e verificada")
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
