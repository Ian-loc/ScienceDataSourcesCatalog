# Auditoria da fronteira científica dos polígonos PRODES entre 1 e 6,25 ha

**Data:** 5 de agosto de 2026  
**Timezone:** `America/Sao_Paulo`  
**Escopo:** Instância 1 — Fluxo A  
**Família:** `PF000001` — PRODES  
**Registro de metadado:** `5f5cfb4c-e207-4932-9c93-2d51cea8adbc`

## Objetivo

Determinar se o componente público denominado **“Incremento anual no desmatamento (polígonos com área entre 1 e 6,25 ha) — Shapefile”** pode ser tratado apenas como outra distribuição do mapa anual PRODES ou se exige uma fronteira científica e curatorial própria.

## Evidência oficial examinada

1. Catálogo BIG/GeoNetwork do INPE para o bioma Amazônia, que descreve o conjunto, sua origem histórica, o limiar de área, o armazenamento desde 2016, a regra de exclusão da taxa, a substituição integral a cada publicação e parte do esquema de atributos.
2. Nota técnica oficial do INPE de 2025, **“Disponibilização dos polígonos de desmatamento com área entre 1 e 6,25 ha detectados pelo PRODES no bioma Amazônia”**.
3. Página de downloads do TerraBrasilis, que lista a distribuição Shapefile separadamente.
4. Registro do GeoPackage PRODES Amazônia, que inclui o componente com UUID próprio.

## Achados científicos

### 1. O limiar de 6,25 ha não é resolução espacial

Na fase analógica do PRODES, os incrementos eram delimitados manualmente em papel vegetal sobre imagens impressas na escala 1:250.000. Esse processo sustentava a delimitação de polígonos maiores que 6,25 ha. Na transição ao mapeamento digital, a digitalização passou a ocorrer em tela e em escala 1:75.000, permitindo detectar polígonos menores.

Logo, `6,25 ha` não deve ser normalizado como:

- tamanho de pixel;
- resolução espacial nominal;
- suporte observacional universal;
- limite técnico atual de detecção.

Ele é uma regra histórica e operacional mantida para preservar a comparabilidade da série oficial.

### 2. Os pequenos polígonos possuem regra própria de entrada na taxa

Desde 2016, polígonos detectados com área entre 1 e 6,25 ha passaram a ser armazenados em uma máscara interna. A documentação afirma que eles **não entram no cálculo da taxa anual até ultrapassarem 6,25 ha**.

Portanto, o conjunto não pode ser colapsado no produto da taxa anual nem interpretado como parcela já contabilizada nela.

### 3. A publicação tem semântica de substituição integral

A documentação informa que o conjunto é integralmente substituído a cada publicação. Isso exige que uma futura promoção registre explicitamente:

- a data e o contexto de acesso;
- a release ou snapshot científico correspondente;
- o checksum dos bytes recuperados;
- o último ano científico contido;
- a relação entre feições persistentes, revisadas ou removidas.

A data de atualização da página ou do arquivo, isoladamente, não é identificador suficiente de release.

### 4. `uid` não é identificador persistente

O esquema publicado informa que `uid` é um identificador numérico usado na exportação e pode mudar em revisões ou atualizações. Assim, ele não pode ser empregado como chave científica persistente entre publicações.

O campo `uuid` é descrito como identificador único da feição, mas sua estabilidade temporal ainda deve ser confirmada nos bytes e entre snapshots. Ele também não deve ser confundido com o UUID do registro de metadados GeoNetwork.

### 5. O conjunto possui fronteira científica suplementar própria

A unidade foi classificada como candidato a produto científico suplementar:

`PD-PRODES-AMZ-SMALL-POLYGON-INCREMENTS`

A classificação não afirma independência metodológica completa do PRODES. Ela preserva uma fronteira necessária porque o conjunto possui:

- intervalo de área explícito;
- regra própria de armazenamento;
- regra própria de inclusão na taxa;
- semântica própria de substituição;
- distribuição e UUID de metadado próprios.

## Decisão curatorial

Estado definido:

```text
metadata identity verified
scientific boundary verified
historical threshold documented
rate exclusion rule documented
replacement semantics documented
endpoint unresolved
asset not inspected
promotion not authorized
```

Não foram promovidos:

- release vigente;
- último ano científico;
- URL direta;
- cadeia de redirecionamentos;
- nome e tamanho exatos do arquivo;
- checksum;
- CRS;
- geometria;
- esquema integral;
- licença do ativo;
- citação da release de dados;
- estado operacional do endpoint.

## Ocorrência

**ID:** `I1-20260805-032`  
**Categoria:** risco de colapso entre produto suplementar, mapa anual e taxa anual  
**Severidade:** `high` para a promoção da unidade  
**Estado:** `corrected`

**Correção:** criação de contrato e validador que bloqueiam:

- inclusão automática dos pequenos polígonos na taxa;
- interpretação de 6,25 ha como resolução;
- uso de `uid` como identificador persistente;
- promoção sem release e bytes inspecionados;
- conversão da data de atualização em período científico.

**Risco residual:** o método específico, a release vigente, o endpoint direto, a estabilidade de `uuid`, o esquema integral, a qualidade, a licença e a citação da release ainda precisam ser resolvidos.

## Arquivos do pacote

- `database/mappings/prodes_amazon_small_polygon_increment_guard_2026.json`;
- `scripts/validate_prodes_amazon_small_polygon_increment_guard.py`;
- integração no gate do GeoPackage PRODES Amazônia.

## Próxima ação

1. resolver a nota técnica completa e extrair as regras metodológicas sem extrapolação;
2. resolver endpoint direto e snapshot publicado;
3. inspecionar bytes, pacote, CRS, geometria e esquema integral;
4. verificar estabilidade de `uuid` entre publicações, se snapshots históricos oficiais estiverem disponíveis;
5. somente depois avaliar produto, release, distribuição e ativo para promoção seletiva.
