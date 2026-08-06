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
2. O metadado oficial **Máscara de Não Floresta na Amazônia Legal** define o objeto como tipologias de vegetação não enquadradas na classe de Floresta adotada no mapeamento e informa que, no contexto descrito, elas não eram objetos da análise e mapeamento florestal do projeto.
3. O metadado documenta `main_class = NAO_FLORESTA` e `class_name = NAO_FLORESTA` ou `NAO_FLORESTA2`.
4. A documentação do produto matricial qualifica `NAO_FLORESTA2` como revisão de Não Floresta.
5. O catálogo TerraBrasilis lista a distribuição Shapefile separadamente.
6. O registro do GeoPackage PRODES Amazônia associa o componente ao UUID `bed1276c-aa3d-4f5b-b560-1879617ef13d`.

Fontes oficiais:

- `https://data.inpe.br/biomasbr/prodes-monitoramento-anual-da-supressao-de-vegetacao-nativa/`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?format=vetorial`;
- `https://terrabrasilis.dpi.inpe.br/downloads/`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?any=2026&fast=index`.

## Achado principal

A evidência sustenta uma **máscara auxiliar de domínio**, não um produto científico autônomo de supressão ou cobertura atual.

```text
Máscara Não Floresta
=
classe espacial definida pelo produtor para tipologias não enquadradas na classe Floresta do PRODES Amazônia
```

Ela não equivale automaticamente a:

- inventário de vegetação natural remanescente;
- mapa atual de extensão florestal;
- incremento anual de supressão;
- incremento de supressão em fitofisionomias não florestais;
- máscara acumulada de supressão não florestal;
- resíduo anual não florestal;
- taxa de desmatamento.

## Decisão de modelagem

A unidade foi resolvida como:

```text
candidate_entity_type = auxiliary_domain_mask
candidate_scientific_product_id = null
scientific_product_promotion_blocked = true
```

Isso não diminui sua importância operacional. A camada pode ser necessária para:

- delimitar o domínio espacial usado pelo produtor;
- interpretar as demais camadas PRODES Amazônia;
- compreender a fronteira entre o monitoramento florestal histórico e os produtos posteriores de supressão em fitofisionomias não florestais;
- reproduzir operações quando a release, os bytes e a metodologia estiverem resolvidos.

Entretanto, utilidade operacional não autoriza transformá-la em produto científico independente sem evidência de identidade, método, versão e release próprios.

## Fronteiras semânticas preservadas

### Classe do produtor, não categoria reinterpretada

A terminologia original `NAO_FLORESTA` e `NAO_FLORESTA2` deve ser preservada. O catálogo não deve substituir esses valores por “vegetação remanescente”, “vegetação natural”, “savana”, “campo” ou outra categoria inferida.

### `NAO_FLORESTA2` não é um segundo produto

A fonte oficial a qualifica como revisão de Não Floresta. Sem evidência adicional, ela deve permanecer valor de classe/revisão, e não produto, release ou série independente.

### Não herdar atributos do monitoramento não florestal

A máscara não pode herdar automaticamente:

- limiar mínimo de 1 ha;
- sensores e cronologia;
- cadência bienal ou anual;
- adaptações metodológicas;
- validação por auditores seniores;
- status de release;

dos produtos de supressão de fitofisionomias não florestais. Esses atributos pertencem a outras unidades e exigem evidência individual.

### Não herdar estado experimental do DETER

O DETER Amazônia Não Floresta é outro sistema e outro produto. O estado experimental anunciado para ele não caracteriza automaticamente a máscara PRODES Não Floresta.

## Esquema parcial documentado

Foram preservados como metadados documentados, sem alegar integralidade:

- `uuid`;
- `uid`;
- `state`;
- `path_row`;
- `main_class`;
- `class_name`;
- `def_cloud`.

A integralidade do esquema, os domínios reais, nulos, CRS, geometria e estabilidade dos identificadores dependem da inspeção dos bytes.

## Estados mantidos como não resolvidos

- método versionado de criação e revisão da máscara;
- temporalidade de `NAO_FLORESTA2`;
- release ou snapshot vigente;
- URL direta e cadeia de redirecionamentos;
- bytes, tamanho exato e checksum;
- CRS, geometria e esquema integral;
- qualidade, validação, vieses e incerteza de classificação;
- licença, atribuição e citação.

## Ocorrência

**ID:** `I1-20260805-037`  
**Categoria:** promoção indevida de classe/máscara auxiliar como produto científico  
**Severidade:** `high` para resolução de entidade e promoção  
**Estado:** `corrected`  
**Correção:** contrato e validador fixam o papel `auxiliary_domain_mask`, mantêm `candidate_scientific_product_id = null`, preservam as classes originais e proíbem heranças sem evidência.  
**Risco residual:** método, temporalidade, release, endpoint, bytes, perfil espacial, qualidade, licença e citação permanecem pendentes.

## Resultado

A unidade avançou de componente apenas enumerado para camada auxiliar científico-operacional com papel, fronteiras semânticas e esquema parcial protegidos. Nenhuma promoção foi autorizada e nenhum atributo de outros produtos foi herdado.
