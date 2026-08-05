# Auditoria das facetas de busca do GeoPackage PRODES Amazônia

**Data:** 2026-08-05 18:23–18:45, America/Sao_Paulo  
**Escopo:** Instância 1 — resolução operacional do pacote GeoPackage PRODES Amazônia  
**Família:** `PF000001`  
**Alvo científico:** `PD-PRODES-AMZ-ANNUAL-MAP`  
**Ativo operacional:** `PRODES-ASSET-AMAZON-GEOPACKAGE`

## Objetivo

Verificar se as facetas públicas do catálogo GeoNetwork permitem atribuir, ao registro individual **GeoPackage - PRODES Amazônia**, uma ação de download, um estado operacional ou uma release.

## Evidência oficial verificada

A busca oficial filtrada pelo formato GeoPackage informa:

- oito registros;
- oito recursos do tipo Dataset;
- oito representações vetoriais;
- uma ação agregada `Downloadable`;
- oito ocorrências agregadas do status `Planned`;
- presença do registro `GeoPackage - PRODES Amazônia` no conjunto retornado.

Fonte oficial consultada:

- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?format=GeoPackage`

O resumo do registro Amazônia descreve um pacote vetorial único, aproximadamente 820 MB, e lista dez componentes com seus respectivos UUIDs de metadados. Essa descrição sustenta a composição declarada do pacote, mas não expõe, no conteúdo recuperado, URL direta individual, checksum ou resposta HTTP do arquivo.

## Achado principal

As facetas são contagens do conjunto filtrado, e não atributos individualizados de cada resultado.

Portanto:

```text
Downloadable (1) em um conjunto de 8 registros
≠
GeoPackage - PRODES Amazônia é o registro baixável
```

Da mesma forma:

```text
Planned (8)
≠
estado operacional individual resolvido para o ativo Amazônia
```

A busca comprova descoberta e classificação agregada. Ela não permite identificar qual dos oito registros recebe a ação `Downloadable`, nem resolve a semântica operacional do status `Planned` para o registro-alvo.

## Consequência curatorial

Permanecem não resolvidos:

- identificador próprio do registro agregador, quando distinto dos UUIDs componentes;
- atribuição individual da ação de download;
- URL direta;
- cadeia de redirecionamentos;
- status HTTP do arquivo;
- nome e tamanho exatos;
- checksum;
- inventário real das camadas;
- CRS, geometrias e atributos;
- licença aplicável ao pacote;
- vínculo com uma release específica.

O tamanho aproximado de 820 MB não deve ser inserido como `byte_size`. Os campos `endpoint_state`, `asset_state` e `release_id` devem permanecer não resolvidos.

## Portão implementado

Foram adicionados:

- `database/mappings/prodes_amazon_geopackage_search_facet_guard_2026.json`;
- `scripts/validate_prodes_amazon_geopackage_search_facet_guard.py`.

O validador exige a preservação das contagens auditadas e bloqueia:

- atribuição da única ação `Downloadable` ao registro Amazônia;
- resolução individual do status com base nas facetas;
- preenchimento prematuro de download, endpoint, ativo ou release;
- promoção canônica.

## Ocorrência

| Campo | Valor |
|---|---|
| ID | `I1-20260805-030` |
| Categoria | atribuição de faceta agregada |
| Severidade | `medium` |
| Estado | `accepted_limitation` |
| Evidência | busca oficial GeoNetwork filtrada por GeoPackage |
| Correção | portão declarativo e validador executável |
| Risco residual | endpoint individual e bytes continuam não resolvidos |

## Decisão

**Não promover o GeoPackage PRODES Amazônia como ativo operacional resolvido.**

A próxima resolução válida exige evidência individual do registro-alvo ou endpoint oficial capaz de fornecer sua distribuição. Na ausência disso, o fluxo deve avançar para outro ativo PRODES independente, preservando esta limitação sem bloquear a família inteira.
