# Auditoria da fronteira científica — incrementos PRODES em áreas não florestais da Amazônia

**Data:** 2026-08-05 18:27–19:03, America/Sao_Paulo  
**Escopo:** Instância 1 — individualização de produto, release, distribuição e ativo  
**Família:** `PF000001`  
**Componente operacional:** `PRODES-ASSET-NON-FOREST-INCREMENT-SHP`  
**UUID de metadado:** `a8208a12-679b-432a-8a47-fc42d2279f9a`

## Objetivo

Determinar se o componente **Incrementos de supressão da vegetação nativa não florestal** pode herdar a identidade científica, a temporalidade e o método do produto `PD-PRODES-AMZ-ANNUAL-MAP` ou se exige fronteira própria antes de promoção ao catálogo normalizado.

## Evidência oficial verificada

O catálogo oficial TerraBrasilis lista, no conjunto PRODES do bioma Amazônia:

- `Incrementos de supressão da vegetação nativa não florestal - Shapefile`;
- o UUID individual `a8208a12-679b-432a-8a47-fc42d2279f9a`;
- a presença do mesmo componente dentro do pacote agregado `GeoPackage - PRODES Amazônia`.

A descrição oficial do monitoramento de fitofisionomias não florestais informa que:

- o objeto é a supressão da vegetação nativa em áreas de não floresta da porção brasileira do bioma Amazônia;
- o programa pretende produzir série histórica a partir de 2000;
- a metodologia PRODES, citada como Almeida et al. (2022), foi tomada como base e adaptada ao novo objeto;
- o mapa-base representa a supressão detectada em imagens de 2000;
- os incrementos de 2002 a 2018 foram mapeados em frequência bienal;
- 2012 foi substituído por 2013 devido à ausência de imagens Landsat com requisitos mínimos de qualidade;
- a partir de 2018, o mapeamento passou a ser anual;
- entre 2000 e 2014 foram usados TM/Landsat 5, ETM+/Landsat 7 e OLI/Landsat 8;
- a partir de 2016 foram empregados MSI/Sentinel-2A e Sentinel-2B.

Fontes oficiais consultadas:

- `https://www.terrabrasilis.dpi.inpe.br/downloads/`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?any=2026&fast=index`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?cl_maintenanceAndUpdateFrequency=asNeeded`;
- `https://data.inpe.br/biomasbr/prodes-monitoramento-anual-da-supressao-de-vegetacao-nativa/`.

## Metodologia-base resolvida

A referência abreviada `Almeida et al. 2022`, citada nos metadados, foi resolvida em fonte oficial do INPE:

> ALMEIDA, C. A.; MAURANO, L. E. P.; VALERIANO, D. M.; CÂMARA, G.; VINHAS, L.; MOTTA, M.; GOMES, A. R.; MONTEIRO, A. M. V.; SOUZA, A. A. A.; MESSIAS, C. G.; RENNÓ, C. D.; ADAMI, M.; ESCADA, M. I. S.; SOLER, L. S.; AMARAL, S. *Metodologia utilizada nos sistemas Prodes e Deter – 2ª edição (atualizada).* 2. ed. São José dos Campos: INPE, 2022. 47 p.

Identificadores persistentes registrados:

- IBI: `sid.inpe.br/mtc-m21d/2022/08.25.11.46-NTC`;
- URL: `http://urlib.net/ibi/8JMKD3MGP3W34T/47GAF6S`.

Essa resolução confirma a metodologia-base. Ela **não resolve automaticamente** as adaptações e adequações específicas para o monitoramento de fitofisionomias não florestais. Essas adaptações permanecem como lacuna metodológica própria do candidato a produto.

## Achado científico principal

Este componente não é apenas outra distribuição do mapa anual de desmatamento florestal.

Há diferenças explícitas em:

- objeto monitorado;
- domínio espacial e ecológico;
- adaptação metodológica;
- cronologia da série;
- frequência histórica;
- sensores empregados;
- interpretação das classes.

Portanto, a relação segura é:

```text
família PRODES
  ├── produto de desmatamento florestal anual
  └── candidato a produto de supressão em fitofisionomias não florestais
```

A individualização final ainda depende de confirmação do nome oficial do produto, release vigente, adaptações metodológicas específicas, variáveis, classes, licença e citação.

## Risco corrigido

Sem um portão explícito, a normalização poderia:

1. herdar frequência anual para toda a série;
2. apagar a fase bienal 2002–2018;
3. omitir a exceção 2012/2013;
4. atribuir a metodologia-base sem registrar adaptações;
5. converter uma data de atualização do catálogo em release;
6. tratar o UUID como endpoint direto;
7. promover o componente como ativo inspecionado sem bytes.

## Artefatos implementados

- `database/mappings/prodes_amazon_non_forest_increment_metadata_guard_2026.json`;
- `scripts/validate_prodes_amazon_non_forest_increment_metadata_guard.py`.

O contrato preserva:

- identidade científica própria;
- perfil temporal em duas fases;
- perfil histórico de sensores;
- citação e identificadores persistentes da metodologia-base;
- separação entre metodologia-base resolvida e adaptações específicas não resolvidas;
- estados negativos explícitos para release, endpoint, bytes, checksum, licença e citação do produto;
- requisitos independentes para promoção do produto e do ativo.

## Ocorrência

| Campo | Valor |
|---|---|
| ID | `I1-20260805-031` |
| Categoria | herança científica indevida entre produtos PRODES |
| Severidade | `high` para a promoção da unidade; não bloqueia trabalho independente |
| Estado | `corrected` |
| Evidência | catálogo, metadados e página metodológica oficial do INPE |
| Correção | fronteira de produto candidata, metodologia-base versionada, contrato declarativo e validador executável |
| Teste | validação de identidade, temporalidade, sensores, citação, estados e proibições |
| Risco residual | adaptações específicas, produto, release, endpoint, licença, citação do produto e bytes ainda não resolvidos |

## Decisão

**Não promover o componente como parte indiferenciada de `PD-PRODES-AMZ-ANNUAL-MAP`.**

Mantê-lo como candidato a produto científico distinto dentro da família PRODES. A metodologia-base está resolvida, mas a promoção continua bloqueada até que as adaptações específicas, a release, as classes, os perfis e as condições de uso estejam integralmente documentados.

A próxima unidade segura é localizar documentação oficial das adaptações metodológicas específicas ou, se ela não estiver publicamente recuperável, resolver outro componente PRODES independente sem enfraquecer este portão.
