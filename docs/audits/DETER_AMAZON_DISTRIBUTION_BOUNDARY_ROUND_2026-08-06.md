# Auditoria — fronteira entre distribuições DETER Amazônia

**Data/hora:** 2026-08-06 00:24–00:34, `America/Sao_Paulo`  
**Família:** `PF000002`  
**Produto-pai candidato:** `PD-DETER-AMZ-ALERTS`

## Objetivo

Individualizar as distribuições públicas de alertas DETER em áreas de Floresta e de Não Floresta na Amazônia, sem transferir classes, esquema, maturidade, período, release ou estado operacional entre elas.

## Evidência oficial

O catálogo TerraBrasilis lista separadamente:

- **Avisos em áreas de Floresta — Shapefile (desde 2016)**;
- **Avisos em áreas de Não Floresta — Shapefile (desde 2023)**.

Na observação de 6 de agosto de 2026, a interface exibia `28/07/2026` como data de atualização para ambas. Essa data é um snapshot de interface e não foi promovida como release científica.

O registro florestal oficial documenta série desde agosto de 2016, sete classes, esquema parcial e o UUID `f2153c4a-915b-48a6-8658-963bdce7366c`. Também registra que `areatotkm` não deve ser somado, que `areamunkm` é o campo orientado para somas municipais, que `publish_month` não está no Shapefile de download e que nomes podem ser truncados a dez caracteres.

O registro não florestal documenta início em agosto de 2023, estado experimental, quatro classes e esquema próprio com `fid`, `class_name`, `area_km`, `view_date`, `create_date`, `audit_date`, `sensor`, `satellite`, `path_row` e `uuid`. O UUID individual do metadado não foi localizado com evidência suficiente nesta rodada e permanece nulo.

## Decisão científica

```text
DETER Amazônia — Floresta
≠
DETER Amazônia — Não Floresta experimental
```

As duas unidades diferem em domínio ecológico, início temporal, maturidade, classes e esquema. Portanto, devem permanecer candidatas a produtos e distribuições distintos sob a família DETER Amazônia.

A data `view_date` representa a imagem usada na identificação do alerta e não comprova a data exata de ocorrência do processo. O caráter experimental do produto não florestal não deve ser transferido ao produto florestal.

## Estados não resolvidos

- UUID individual do metadado não florestal;
- releases ou snapshots científicos;
- URLs diretas e respostas HTTP;
- bytes, tamanho e checksum;
- CRS, geometria, domínios e nulos;
- cobertura efetiva dos pacotes;
- licença, atribuição e citação por release.

## Ocorrência

**ID:** `I1-20260806-043`  
**Categoria:** colapso entre distribuições florestal e não florestal e herança de esquema/maturidade  
**Severidade:** `high` para promoção das unidades  
**Estado:** `corrected`  
**Correção:** contrato e validador preservam produtos, períodos, classes, esquemas e estados de maturidade separados.  
**Teste:** `scripts/validate_deter_amazon_distribution_boundary_guard.py`.  
**Risco residual:** endpoint, bytes, release, UUID não florestal, qualidade, licença e citação permanecem pendentes.

## Resultado

A família DETER Amazônia avançou de uma fronteira geral de alertas para duas distribuições científicas-operacionais explicitamente separadas. Nenhuma promoção canônica foi autorizada.
