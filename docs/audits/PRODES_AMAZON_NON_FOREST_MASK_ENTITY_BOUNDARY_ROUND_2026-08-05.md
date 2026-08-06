# Auditoria de resolução de entidade — máscara Não Floresta PRODES Amazônia

**Data/hora:** 2026-08-05 22:02, `America/Sao_Paulo`  
**Família:** `PF000001`  
**Ativo candidato:** `PRODES-ASSET-NON-FOREST-MASK-SHP`  
**Entidade auxiliar candidata:** `AX-PRODES-AMZ-NON-FOREST-DOMAIN-MASK`  
**UUID de metadado:** `bed1276c-aa3d-4f5b-b560-1879617ef13d`

## Objetivo

Determinar se a distribuição pública **Não floresta — Shapefile** deve ser promovida como produto científico autônomo ou resolvida como camada auxiliar de domínio e classificação do PRODES Amazônia.

## Evidência oficial inspecionada

1. A documentação geral do PRODES apresenta **Não Floresta** como classe específica do PRODES Amazônia Legal e, no GeoPackage vetorial, como camada `no_forest_biome`, separada de `yearly deforestation`, `residual` e das camadas de supressão em áreas não florestais.
2. O metadado oficial **Máscara de Não Floresta na Amazônia Legal** define o objeto como tipologias de vegetação não enquadradas na classe de Floresta adotada no mapeamento e informa que elas não eram objetos da análise e mapeamento florestal descritos.
3. O metadado documenta `main_class = NAO_FLORESTA` e `class_name = NAO_FLORESTA` ou `NAO_FLORESTA2`.
4. A documentação do produto matricial qualifica `NAO_FLORESTA2` como revisão de Não Floresta.
5. O catálogo TerraBrasilis lista a distribuição Shapefile separadamente.
6. O GeoPackage PRODES Amazônia associa o componente ao UUID individual acima.

Fontes oficiais:

- `https://data.inpe.br/biomasbr/prodes-monitoramento-anual-da-supressao-de-vegetacao-nativa/`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?format=vetorial`;
- `https://terrabrasilis.dpi.inpe.br/downloads/`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?any=2026&fast=index`.

## Achado principal

A evidência sustenta uma **máscara auxiliar de domínio**, não um produto científico autônomo de supressão ou cobertura atual:

```text
Máscara Não Floresta
=
classe espacial definida pelo produtor para tipologias não enquadradas na classe Floresta do PRODES Amazônia
```

Ela não equivale automaticamente a inventário de vegetação natural remanescente, mapa atual de extensão florestal, incremento anual, supressão em fitofisionomias não florestais, acumulado de supressão, resíduo anual ou taxa de desmatamento.

## Decisão de modelagem

```text
candidate_entity_type = auxiliary_domain_mask
candidate_scientific_product_id = null
scientific_product_promotion_blocked = true
```

A camada continua operacionalmente relevante para delimitar o domínio do produtor, interpretar outras camadas PRODES e reproduzir operações futuras. Utilidade operacional, porém, não autoriza promoção como produto científico sem identidade, método, versão e release suficientes.

## Fronteiras preservadas

- Preservar `NAO_FLORESTA` e `NAO_FLORESTA2` como terminologia original; não substituir por vegetação remanescente, savana, campo ou categoria inferida.
- Tratar `NAO_FLORESTA2` como revisão documentada da classe, não como segundo produto ou release.
- Não herdar limiar de 1 ha, sensores, cronologia, cadência, adaptações metodológicas ou auditoria dos produtos de supressão não florestal.
- Não herdar o estado experimental do DETER Amazônia Não Floresta, que pertence a outro sistema e produto.
- Não colapsar a máscara nos produtos de supressão acumulada, incremental ou residual.

## Esquema parcial documentado

Foram preservados, sem alegar integralidade: `uuid`, `uid`, `state`, `path_row`, `main_class`, `class_name` e `def_cloud`. A integralidade, os domínios, nulos, CRS, geometria e estabilidade dos identificadores dependem da inspeção dos bytes.

## Estados não resolvidos

- método versionado de criação e revisão;
- temporalidade de `NAO_FLORESTA2`;
- release ou snapshot vigente;
- URL direta e redirecionamentos;
- bytes, tamanho e checksum;
- CRS, geometria e esquema integral;
- qualidade, validação, vieses e incerteza;
- licença, atribuição e citação.

## Ocorrência

**ID:** `I1-20260805-038`  
**Categoria:** promoção indevida de classe/máscara auxiliar como produto científico  
**Severidade:** `high` para resolução de entidade e promoção  
**Estado:** `corrected`  
**Correção:** contrato e validador fixam o papel `auxiliary_domain_mask`, mantêm `candidate_scientific_product_id = null`, preservam as classes originais e proíbem heranças sem evidência.  
**Risco residual:** método, temporalidade, release, endpoint, bytes, perfil espacial, qualidade, licença e citação permanecem pendentes.

## Resultado

A unidade avançou de componente enumerado para camada auxiliar científico-operacional com papel, fronteiras semânticas e esquema parcial protegidos. Nenhuma promoção foi autorizada e nenhum atributo de outros produtos foi herdado.
