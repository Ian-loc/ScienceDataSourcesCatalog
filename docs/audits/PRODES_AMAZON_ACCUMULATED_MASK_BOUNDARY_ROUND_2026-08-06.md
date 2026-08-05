# Auditoria da máscara acumulada PRODES Amazônia até 2007

**Data:** 6 de agosto de 2026  
**Timezone:** `America/Sao_Paulo`  
**Escopo:** Instância 1 — Fluxo A  
**Família:** `PF000001` — PRODES  
**Registro de metadado:** `c6748fdf-a18e-41b9-a523-ea14bae92602`

## Objetivo

Determinar a fronteira científica e temporal do componente público **“Máscara de área acumulada de supressão da vegetação nativa — Shapefile (2007)”**, evitando sua assimilação indevida ao mapa anual, à taxa anual ou aos incrementos posteriores.

## Evidência oficial examinada

1. Catálogo BIG/GeoNetwork do INPE, que descreve a área total desmatada acumulada até 2007 no bioma Amazônia, o limiar de 6,25 ha, a definição de desmatamento, a possibilidade de revisão e o esquema parcial de atributos.
2. Página oficial de downloads do TerraBrasilis, que lista a distribuição Shapefile com corte temporal explícito em 2007.
3. Registro oficial do GeoPackage PRODES Amazônia, que inclui a máscara acumulada como componente próprio e associa a ela UUID individual.

## Achados científicos

### 1. A unidade é uma linha de base acumulada, não uma observação anual

A documentação define o conjunto como área total desmatada medida **até 2007**. O valor temporal representa o corte científico do acumulado. Não representa:

- data de publicação;
- data de atualização do arquivo;
- ano de uma única observação anual;
- release atualmente disponível;
- taxa anual de desmatamento.

### 2. A fronteira com os incrementos anuais deve ser preservada

O catálogo separa a máscara acumulada até 2007 da série de incrementos anuais iniciada em 2008. Para reconstruir uma série cartográfica completa, os dois objetos podem ser relacionados, mas não colapsados:

```text
máscara acumulada até 2007
+
incrementos anuais desde 2008
≠
um único registro sem fronteira temporal
```

A arquitetura deve preservar produto, release, distribuição e proveniência de cada componente.

### 3. O limiar de 6,25 ha não é resolução espacial

A documentação declara que o mapeamento registra áreas maiores que 6,25 ha. Esse limiar não deve ser normalizado como tamanho de pixel, resolução nominal ou suporte universal. Ele é uma regra de mapeamento e comparabilidade do produto.

### 4. O esquema publicado é informativo, mas ainda parcial

O metadado documenta, entre outros, `uuid`, `uid`, `state`, `path_row`, `main_class`, `class_name`, `year`, `area_km`, `source`, `geom` e `pub_date`.

As qualificações críticas são:

- `main_class` é documentado como `DESMATAMENTO`;
- `class_name` é documentado como `d2007`;
- `year` é documentado como 2007;
- `uid` pode mudar em revisões ou atualizações;
- `pub_date` é atualizado automaticamente a cada exportação e não constitui período científico;
- `uuid` da feição não é o UUID do registro GeoNetwork.

A integralidade do esquema, os domínios reais, os nulos e a estabilidade dos identificadores dependem de inspeção dos bytes.

### 5. A máscara pode sofrer revisões sem alterar sua semântica de corte

O catálogo informa que o conjunto pode receber ajustes oriundos de revisão. Uma revisão publicada posteriormente não transforma o conjunto em mapa do ano da revisão: sua semântica continua sendo acumulado até 2007, salvo documentação oficial que redefina o produto.

## Decisão curatorial

A unidade foi classificada como candidato a produto científico de linha de base:

`PD-PRODES-AMZ-ACCUMULATED-MASK-2007`

Estado definido:

```text
metadata identity verified
scientific boundary verified
scientific cutoff = 2007
annual increment boundary = 2008
partial schema documented
current release unresolved
endpoint unresolved
asset not inspected
promotion not authorized
```

Não foram promovidos:

- release vigente;
- URL direta;
- cadeia de redirecionamentos;
- bytes, tamanho ou checksum;
- CRS e geometria verificados;
- esquema integral;
- licença específica do ativo;
- citação da release;
- estado operacional do endpoint.

## Ocorrência

**ID:** `I1-20260806-033`  
**Categoria:** colapso temporal entre linha de base acumulada e incrementos anuais  
**Severidade:** `high` para a promoção da unidade  
**Estado:** `corrected`

**Correção:** criação de contrato e validador que bloqueiam:

- tratamento da máscara como série anual;
- conversão de 2007 em data de publicação ou release;
- assimilação automática aos incrementos desde 2008;
- interpretação de 6,25 ha como resolução espacial;
- uso de `uid` como identificador persistente;
- uso de `pub_date` como período científico;
- promoção sem release, endpoint e bytes verificados.

**Risco residual:** método-base versionado, regras de revisão, release atual, endpoint direto, esquema integral, qualidade, licença e citação ainda não foram resolvidos.

## Arquivos do pacote

- `database/mappings/prodes_amazon_accumulated_mask_guard_2026.json`;
- `scripts/validate_prodes_amazon_accumulated_mask_guard.py`;
- integração no gate do GeoPackage PRODES Amazônia.

## Próxima ação

1. resolver o método-base e as regras específicas de revisão da máscara;
2. identificar release ou snapshot oficialmente acessível;
3. resolver endpoint direto sem inferência por padrão de URL;
4. inspecionar bytes, CRS, geometria e esquema integral;
5. resolver licença e citação da release;
6. somente então avaliar promoção seletiva de produto, release, distribuição e ativo.
