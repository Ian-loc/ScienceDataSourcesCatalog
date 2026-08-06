# Auditoria da fronteira científica e contabilização — resíduo anual PRODES Amazônia

**Data/hora:** 2026-08-05 21:42, `America/Sao_Paulo`  
**Família:** `PF000001`  
**Ativo candidato:** `PRODES-ASSET-ANNUAL-NATIVE-VEGETATION-SUPPRESSION-RESIDUAL-SHP`  
**Produto científico candidato:** `PD-PRODES-AMZ-ANNUAL-RESIDUAL`  
**UUID de metadado:** `00a728cb-8577-458a-9c38-082c1f3bca9e`

## Objetivo

Preservar a identidade e a semântica temporal da distribuição pública **Resíduo anual na supressão da vegetação nativa — Shapefile**, evitando que ela seja tratada como incremento do ano de detecção, taxa anual, máscara acumulada, erro estatístico ou sinônimo da camada residual não florestal.

## Evidência oficial inspecionada

1. O catálogo TerraBrasilis lista a distribuição Shapefile com rótulo e UUID próprios.
2. O registro oficial do GeoPackage PRODES Amazônia inclui o componente residual separadamente e o distingue do resíduo não florestal.
3. A página metodológica do Prodes mantém classes residuais com ano de detecção associado e separa as camadas vetoriais `yearly deforestation` e `residual`.
4. A nota técnica oficial **Polígonos de resíduos do Prodes**, identificada por `id.inpe.br/mtc-m21d/2024/12.02.13.49-NTC`, define os resíduos como áreas suprimidas em anos anteriores, mas não detectadas no ano de ocorrência por motivos como cobertura de nuvens e confusão entre classes.

Fontes oficiais:

- `https://terrabrasilis.dpi.inpe.br/downloads/`;
- `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?any=2026&fast=index`;
- `https://data.inpe.br/biomasbr/prodes-monitoramento-anual-da-supressao-de-vegetacao-nativa/`;
- `https://data.inpe.br/biomasbr/wp-content/uploads/sites/3/2026/04/POLIGONOS-DE-RESIDUOS-DO-PRODES.pdf`;
- documento persistente: `http://urlib.net/8JMKD2USNNW34T/4CG97L8`.

## Achados científicos

### Ano de detecção não é ano exato da supressão

O polígono recebe a classe residual referente ao ano em que foi detectado e mapeado. A supressão ocorreu anteriormente, mas sua data exata não é resolvida por essa classe.

```text
resíduo_2021
=
detectado e mapeado como resíduo em 2021
≠
supressão necessariamente ocorrida em 2021
```

### Resíduos não integram o incremento anual

Os polígonos residuais não são computados no incremento do ano de detecção. Fazer isso atribuiria incorretamente a supressão ao ano Prodes em que a omissão foi corrigida.

### Resíduos contribuem para o acumulado

A área residual é computada no desmatamento acumulado até aquele ano. Consequentemente, o acumulado de um ano pode não equivaler exatamente ao acumulado anterior somado ao incremento corrente.

### Resíduos entram na máscara subsequente

No ciclo seguinte, os polígonos residuais e de incremento são incorporados à máscara Prodes, restringindo o novo mapeamento às áreas de vegetação nativa ainda não classificadas como desmatadas.

### Uso analítico exige sinalização temporal

Quando a análise depende da data exata da ocorrência da supressão, os polígonos residuais não devem ser usados como se o ano da classe fosse o ano do evento.

## Decisão de modelagem

O componente permanece candidato a produto científico de correção retrospectiva:

`PD-PRODES-AMZ-ANNUAL-RESIDUAL`

Ele não deve ser colapsado em:

- mapa anual;
- taxa anual;
- máscara acumulada de 2007;
- conjunto suplementar de pequenos polígonos;
- resíduo específico de áreas não florestais.

Dois portões complementares preservam a unidade:

- `prodes_amazon_annual_residual_guard_2026.json`: identidade, revisão retrospectiva e esquema parcial;
- `prodes_amazon_annual_residual_accounting_guard_2026.json`: ano de detecção, exclusão do incremento, inclusão no acumulado e incorporação à máscara seguinte.

## Estados mantidos como não resolvidos

- release ou snapshot vigente;
- escopo integral entre vegetação florestal e não florestal nos bytes;
- URL direta e cadeia de redirecionamentos;
- bytes, tamanho exato e checksum;
- inventário do pacote Shapefile;
- CRS, geometria e esquema integral;
- validação e incerteza quantitativa;
- licença, atribuição e citação da release.

## Ocorrência

**ID:** `I1-20260805-035`  
**Categoria:** atribuição temporal e contábil indevida de polígonos residuais  
**Severidade:** `high` para promoção e uso temporal da unidade  
**Estado:** `corrected`  
**Correção:** contratos e validadores preservam revisão retrospectiva, ano de detecção versus ocorrência, exclusão do incremento anual, inclusão no acumulado, incorporação à máscara seguinte e promoção negativa.  
**Risco residual:** release, escopo integral, endpoint, bytes, perfil espacial, qualidade quantitativa, licença e citação permanecem pendentes.

## Resultado

A unidade avançou de componente enumerado para candidato científico-operacional com identidade, esquema parcial, semântica temporal e regra de contabilização protegidas. Nenhuma promoção foi autorizada e nenhum atributo não comprovado foi herdado de outro produto ou do pacote agregado.
