# Auditoria — validação científica primária do Dynamic World V1

**Data e horário:** 2026-08-05 11:21–11:39 America/Sao_Paulo  
**PR:** #54  
**Branch:** `agent/consolidate-instance-1-relational-catalog`  
**Entidade:** `DP000011` / `PR000011` / `QP-DW-V1`

## Objetivo

Fechar a pendência de métricas primárias de validação do Dynamic World V1 sem confundir concordância com especialistas, probabilidades de classe e acurácia universal por pixel.

## Fonte primária

Brown, C. F. et al. *Dynamic World, Near real-time global 10 m land use land cover mapping*. Scientific Data 9, 251 (2022). DOI: `10.1038/s41597-022-01307-4`.

## Evidências consolidadas

- validação global em 409 tiles de 5,1 km × 5,1 km;
- esquema principal `Expert Consensus`, com 68.137.571 pixels avaliados;
- concordância global Dynamic World top-1 × Expert Consensus: 73,8%;
- concordância anotadores não especialistas × especialistas: 77,8%;
- concordância de 74,2% quando `grass` e `shrub & scrub` são fundidas para a comparação com LCMAP;
- classes com maior concordância relativa: water, trees, built area e snow & ice;
- concordância relatada de 30,1% para grass e 88,9% para crops no Expert Consensus;
- desempenho espacial e temporalmente variável em função do mascaramento de nuvens e da condição da cobertura;
- confusão relevante crops–shrub em ambientes áridos;
- comparações com produtos anuais dependem de crosswalk de classes e podem envolver datas diferentes.

## Correção implementada

Foi criado `scripts/enrich_instance1_dynamic_world_validation.py`, que:

1. atualiza idempotentemente `QP-DW-V1` com desenho, métricas e limitações de validação;
2. registra nove afirmações apoiadas diretamente pelo artigo revisado por pares;
3. remove da revisão curatorial a pendência de auditar métricas por classe;
4. mantém `review_status=in_progress`, pois endpoints, ativos, licença operacional e acesso ainda exigem teste;
5. verifica após a gravação a persistência das métricas e a cardinalidade das afirmações;
6. é executado duas vezes no CI para comprovar idempotência.

## Auditoria de delta

Verificado:

- nenhuma métrica foi convertida em probabilidade individual de correção;
- nenhuma métrica externa de outro artigo foi misturada ao perfil primário;
- a data e o suporte da predição permanecem por aquisição Sentinel-2;
- a concordância de 74,2% permanece explicitamente condicionada à fusão de classes;
- limitações espaciais, temporais e taxonômicas foram mantidas;
- a revisão não foi promovida a `approved` antes do teste operacional.

## Ocorrência

### I1-20260805-003

- **Severidade:** `medium`
- **Estado anterior:** `open`
- **Estado atual:** `closed`, condicionado ao CI verde do SHA final
- **Categoria:** completude de validação
- **Correção:** métricas primárias, desenho de validação, limitações e evidências por campo adicionadas ao banco efêmero.
- **Risco residual:** o produto ainda não possui aprovação final porque distribuições, endpoints, ativos e condições operacionais de acesso não foram integralmente testados.

## Próxima unidade

1. verificar as distribuições oficiais do Dynamic World V1;
2. testar o asset `GOOGLE/DYNAMICWORLD/V1` e os papéis das formas de acesso;
3. confirmar licença e citação operacional no nível da distribuição;
4. decidir a aprovação curatorial somente após o portão operacional.
