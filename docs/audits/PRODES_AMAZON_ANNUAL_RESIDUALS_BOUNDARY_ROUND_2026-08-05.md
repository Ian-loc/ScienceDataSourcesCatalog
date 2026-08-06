# Auditoria — resíduos anuais PRODES Amazônia

**Data/hora:** 2026-08-05 21:43–21:55, America/Sao_Paulo  
**Família:** `PF000001`

## Unidades auditadas

### Resíduo anual de supressão da vegetação nativa

- **Ativo candidato:** `PRODES-ASSET-ANNUAL-NATIVE-VEGETATION-SUPPRESSION-RESIDUAL-SHP`
- **Produto científico candidato:** `PD-PRODES-AMZ-ANNUAL-RESIDUAL`
- **UUID de metadado:** `00a728cb-8577-458a-9c38-082c1f3bca9e`

### Resíduo anual de supressão da vegetação nativa não florestal

- **Ativo candidato:** `PRODES-ASSET-ANNUAL-NON-FOREST-SUPPRESSION-RESIDUAL-SHP`
- **Produto científico candidato:** `PD-PRODES-AMZ-NON-FOREST-ANNUAL-RESIDUAL`
- **UUID de metadado:** `63751b72-3e6a-4d15-8fc0-740e57bbc346`

## Objetivo

Preservar a identidade científica e a semântica temporal dos resíduos anuais PRODES sem tratá-los como incrementos do ano corrente, taxas, máscaras acumuladas, erros estatísticos, estimativas de incerteza ou classes residuais genéricas.

## Evidência oficial inspecionada

1. O catálogo TerraBrasilis lista separadamente as duas distribuições Shapefile e associa UUIDs de metadados próprios a cada componente do GeoPackage PRODES Amazônia.
2. O registro do resíduo anual geral define o objeto como resultado da revisão de levantamentos de anos anteriores ao ano corrente de mapeamento. A documentação informa uso de imagens Landsat ou similares, área mapeada maior ou igual a 6,25 ha, padrão `class_name = rYYYY` e exemplo `r2020`.
3. A documentação registra `pub_date` como data de publicação ou exportação atualizada automaticamente nos arquivos vetoriais. Esse campo não constitui período científico nem identificador de release.
4. O registro do resíduo não florestal descreve domínio ecológico próprio nas fitofisionomias não florestais do bioma Amazônia.
5. Para o programa não florestal, a operação sistemática é declarada a partir de 2023, enquanto o objetivo da série histórica começa em 2000. O mapa-base é de 2000; os incrementos foram bienais entre 2002 e 2018, com 2012 substituído por 2013, e anuais a partir de 2018.
6. A metodologia não florestal usa como base Almeida et al. (2022), com adaptações específicas ainda não versionadas integralmente no catálogo. A documentação registra Landsat 5 TM, Landsat 7 ETM+, Landsat 8 OLI, Sentinel-2A/2B MSI, interpretação visual, auditoria por auditores seniores e eliminação de polígonos menores que 1 ha.
7. A lista de atributos é declarada como padronizada e preenchida conforme aplicabilidade. Ela não comprova que todos os valores possíveis de `main_class` ou `class_name` estejam presentes em cada distribuição específica.

## Decisões de modelagem

### Semântica de resíduo

```text
resíduo PRODES
= feições identificadas por revisão retrospectiva de levantamentos anteriores
```

Não significa:

- resíduo estatístico de um modelo;
- erro ou incerteza quantitativa;
- diferença aritmética calculada pelo catálogo;
- vegetação remanescente;
- incremento do período corrente;
- máscara acumulada;
- taxa anual.

### Fronteira entre os dois produtos

```text
resíduo anual geral/florestal
≠ resíduo anual de fitofisionomias não florestais
```

O segundo possui domínio ecológico, trajetória operacional, sensores, temporalidade e limiar mínimo próprios. Nenhum desses atributos pode ser herdado automaticamente pelo primeiro.

### Fronteira temporal não florestal

```text
início operacional declarado: 2023
≠ início pretendido da série: 2000
```

A data de implantação operacional não deve apagar a reconstrução histórica declarada pelo produtor.

### Identificadores e campos temporais

- `uid` pode mudar em revisões e atualizações e não é identificador persistente.
- `uuid` de feição não é o UUID do registro de metadados.
- `class_name`, `year`, `publish_year` e `pub_date` não são identificadores de release sem contrato explícito.
- datas exibidas na interface de downloads não constituem período científico.

## Estados preservados como não resolvidos

Para ambos os produtos permanecem pendentes:

- release vigente e último ano científico;
- URL direta e cadeia de redirecionamentos;
- bytes, nome, tamanho exato e checksum;
- inventário do pacote Shapefile;
- CRS, geometria e esquema integral observado nos bytes;
- classes efetivamente presentes;
- perfil completo de validação, qualidade, incerteza, vieses e dados ausentes;
- licença, atribuição e citação da release.

Para o resíduo não florestal permanece adicionalmente pendente a versão documental das adaptações específicas ao método-base.

## Ocorrências

### `I1-20260805-035`

- **Categoria:** colapso semântico de resíduo retrospectivo em incremento, taxa, incerteza ou máscara acumulada
- **Severidade:** `high` para promoção das unidades
- **Estado:** `corrected`
- **Correção:** contratos e validadores tornam obrigatória a semântica de revisão retrospectiva e proíbem interpretações estatísticas ou temporais indevidas.
- **Risco residual:** metodologia versionada, release, endpoint, bytes, qualidade, licença e citação continuam pendentes.

### `I1-20260805-036`

- **Categoria:** herança indevida entre resíduo geral e resíduo não florestal
- **Severidade:** `high` para promoção da unidade não florestal
- **Estado:** `corrected`
- **Correção:** o contrato não florestal preserva domínio, início operacional em 2023, série desde 2000, cadências, sensores, auditoria sênior e limiar de 1 ha como atributos próprios.
- **Risco residual:** as adaptações específicas ainda não possuem versão documental integralmente resolvida e o ativo não foi inspecionado.

## Validação

Os validadores:

- `scripts/validate_prodes_amazon_annual_residual_guard.py`;
- `scripts/validate_prodes_amazon_non_forest_annual_residual_guard.py`;

verificam IDs, UUIDs, URLs oficiais, fronteiras científicas, temporalidade, método, esquema parcial, evidências, estados negativos de promoção e requisitos remanescentes.

Ambos são executados pela cadeia agregada do GeoPackage PRODES Amazônia.

## Resultado

Os dois componentes avançaram de itens enumerados no pacote para candidatos científico-operacionais com semântica retrospectiva e fronteiras próprias protegidas. Nenhuma promoção foi autorizada, nenhum endpoint foi inferido e nenhum atributo foi transferido automaticamente entre os produtos.
