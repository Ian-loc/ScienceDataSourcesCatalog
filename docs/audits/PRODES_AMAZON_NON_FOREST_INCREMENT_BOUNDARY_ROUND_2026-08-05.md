# Auditoria da fronteira científica — incrementos PRODES em áreas não florestais da Amazônia

**Data:** 2026-08-05 18:27–18:58, America/Sao_Paulo  
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
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?cl_maintenanceAndUpdateFrequency=asNeeded`.

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

A individualização final ainda depende de confirmação do nome oficial do produto, release vigente, metodologia completa, variáveis, classes, licença e citação.

## Risco corrigido

Sem um portão explícito, a normalização poderia:

1. herdar frequência anual para toda a série;
2. apagar a fase bienal 2002–2018;
3. omitir a exceção 2012/2013;
4. atribuir o método florestal sem registrar adaptações;
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
- referência metodológica ainda não integralmente resolvida;
- estados negativos explícitos para release, endpoint, bytes, checksum, licença e citação;
- requisitos independentes para promoção do produto e do ativo.

## Ocorrência

| Campo | Valor |
|---|---|
| ID | `I1-20260805-031` |
| Categoria | herança científica indevida entre produtos PRODES |
| Severidade | `high` para a promoção da unidade; não bloqueia trabalho independente |
| Estado | `corrected` |
| Evidência | catálogo e metadados oficiais TerraBrasilis |
| Correção | fronteira de produto candidata, contrato declarativo e validador executável |
| Teste | validação de identidade, temporalidade, sensores, estados e proibições |
| Risco residual | produto, release, endpoint, licença, citação e bytes ainda não resolvidos |

## Decisão

**Não promover o componente como parte indiferenciada de `PD-PRODES-AMZ-ANNUAL-MAP`.**

Mantê-lo como candidato a produto científico distinto dentro da família PRODES até que a metodologia, a release, as classes, os perfis e as condições de uso estejam integralmente documentados.

A próxima unidade segura é localizar e versionar a metodologia completa citada como Almeida et al. (2022) ou, se a fonte não for recuperável, resolver outro componente PRODES independente sem enfraquecer este portão.
