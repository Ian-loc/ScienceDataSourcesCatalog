# Auditoria — máscara acumulada de supressão não florestal PRODES Amazônia

**Data/hora:** 2026-08-05 21:26–21:34, America/Sao_Paulo  
**Família:** `PF000001`  
**Ativo candidato:** `PRODES-ASSET-NON-FOREST-ACCUMULATED-MASK-2000-SHP`  
**Produto científico candidato:** `PD-PRODES-AMZ-NON-FOREST-ACCUMULATED-MASK-2000`  
**UUID de metadado:** `215be904-3828-41a9-a1bd-c7daa0133944`

## Objetivo

Preservar a fronteira científica e temporal da distribuição pública **Máscara de área acumulada de supressão da vegetação nativa não florestal — Shapefile (2000)** sem inferir release, endpoint, conteúdo do arquivo ou autorização de promoção.

## Evidência oficial inspecionada

1. O catálogo TerraBrasilis lista explicitamente a distribuição Shapefile, identifica o objeto como máscara acumulada de supressão não florestal e apresenta o corte temporal de 2000.
2. O registro do GeoPackage PRODES Amazônia declara esse componente separadamente e associa o UUID `215be904-3828-41a9-a1bd-c7daa0133944`.
3. A documentação oficial do monitoramento não florestal descreve mapa-base de 2000 e incrementos posteriores iniciados em 2002, inicialmente em cadência bienal, com metodologia PRODES adaptada às fitofisionomias não florestais.
4. A metodologia-base está identificada em Almeida et al. (2022), mas a documentação versionada das adaptações específicas continua não resolvida.

## Decisão de modelagem

A máscara acumulada não florestal de 2000 deve permanecer candidata a produto científico próprio. Ela não pode ser colapsada em:

- máscara acumulada geral ou florestal de 2007;
- incrementos de supressão não florestal;
- mapa anual PRODES Amazônia;
- taxa anual PRODES.

A fronteira temporal é:

```text
linha de base acumulada não florestal até 2000
→ incrementos não florestais posteriores desde 2002
```

O ano de 2000 representa o corte científico da linha de base. Ele não deve ser reinterpretado como data de publicação, data de atualização do arquivo ou identificador de release.

## Estados preservados como não resolvidos

- release vigente;
- documentação das adaptações metodológicas específicas;
- URL direta e cadeia de redirecionamentos;
- bytes, tamanho exato e checksum;
- inventário do pacote Shapefile;
- CRS, geometria e esquema integral;
- classes e domínios semânticos;
- qualidade, validação, incerteza e dados ausentes;
- licença, atribuição e citação da release.

## Ocorrência

**ID:** `I1-20260805-034`  
**Categoria:** colapso entre linha de base não florestal e produtos PRODES temporalmente distintos  
**Severidade:** `high` para promoção da unidade  
**Estado:** `corrected`  
**Correção:** criação de contrato verificável e validador que preservam identidade, corte de 2000, fronteira com incrementos desde 2002 e estados negativos de promoção.  
**Risco residual:** documentação específica, release, endpoint, bytes, perfil espacial, qualidade, licença e citação permanecem pendentes.

## Validação

O validador `scripts/validate_prodes_amazon_non_forest_accumulated_mask_guard.py` verifica:

- IDs e UUID esperados;
- fonte oficial HTTPS do INPE;
- identidade científica própria;
- corte temporal em 2000;
- fronteira posterior em 2002 e cadência inicial bienal;
- relação entre metodologia-base e adaptações ainda pendentes;
- evidência oficial mínima;
- estados negativos para release, endpoint, bytes, checksum, licença e citação;
- ausência de autorização de promoção.

O gate é executado pela cadeia agregada do GeoPackage PRODES Amazônia.

## Resultado

A unidade avançou de um componente apenas enumerado no pacote para um candidato científico-operacional com identidade e temporalidade protegidas. Nenhuma promoção foi autorizada e nenhum atributo não comprovado foi herdado de outra distribuição ou produto.
