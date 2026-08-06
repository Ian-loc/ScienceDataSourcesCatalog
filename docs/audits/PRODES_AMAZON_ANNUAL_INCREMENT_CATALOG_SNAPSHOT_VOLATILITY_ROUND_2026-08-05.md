# PRODES Amazônia — volatilidade dos snapshots do catálogo do incremento anual

**Data:** 2026-08-05 16:21–16:50, `America/Sao_Paulo`  
**Escopo:** Instância 1; pré-promoção; família `PF000001`; alvo `PRODES-ASSET-ANNUAL-INCREMENT-SHP`.  
**Resultado:** `PASS_WITH_PROMOTION_BLOCKED`.

## Objetivo

Verificar se a informação pública atualmente recuperável sobre a distribuição **Incremento anual no desmatamento — Shapefile (desde 2008)** permite resolver endpoint direto, ativo ou release.

## Evidência oficial observada

O catálogo oficial TerraBrasilis mantém a distribuição no grupo **Bioma Amazônia — PRODES (Desmatamento)** e associa o registro de metadados ao UUID:

`b75b83db-8026-43f9-9537-ee1dfa308158`

Foram observados snapshots públicos do catálogo oficial nos hosts com e sem `www`. Esses snapshots exibem datas distintas para a mesma distribuição:

- `https://terrabrasilis.dpi.inpe.br/downloads/` — snapshot indexado com data exibida `2026-06-16`;
- `https://www.terrabrasilis.dpi.inpe.br/downloads/` — snapshot indexado com data exibida `2026-07-20`.

A divergência não é tratada como erro do produto nem como duas releases. Ela demonstra que a data apresentada na interface do catálogo é volátil e insuficiente, isoladamente, para definir identidade dos bytes, release científico ou período representado.

## Decisão curatorial

Permanece verificado apenas que:

1. a distribuição está presente no catálogo oficial;
2. o formato declarado é Shapefile;
3. a série é apresentada como disponível desde 2008;
4. o UUID de metadado está associado ao incremento anual.

Permanecem **não resolvidos**:

- URL direta vigente;
- cadeia de redirecionamentos;
- status HTTP do download;
- nome e tamanho exatos do arquivo;
- checksum;
- conteúdo do pacote;
- CRS, geometria e atributos;
- cobertura temporal efetiva dos bytes;
- licença, atribuição e citação aplicáveis;
- relação inequívoca com uma release.

## Implementação

Adicionados:

- `database/mappings/prodes_amazon_annual_increment_catalog_snapshot_guard_2026.json`;
- `scripts/validate_prodes_amazon_annual_increment_catalog_snapshot_guard.py`.

O validador foi encadeado ao gate do GeoPackage e, por consequência, ao gate geral `scripts/validate_prodes_product_targets.py`.

## Regras preservadas

- data de interface não é `release_id`;
- UUID de metadado não identifica bytes;
- host com e sem `www` não cria duas distribuições;
- presença no catálogo não confirma estabilidade do endpoint;
- nenhuma das datas conflitantes pode ser promovida como canônica;
- `endpoint_state` permanece `unresolved`;
- `asset_state` permanece `not_inspected`;
- `promotion_authorized` permanece `false`.

## Ocorrência

| ID | Categoria | Severidade | Estado | Evidência | Correção | Risco residual |
|---|---|---|---|---|---|---|
| I1-20260805-028 | catalog_snapshot_volatility | medium | accepted_limitation | snapshots oficiais apresentam datas diferentes para a mesma distribuição | criado portão automatizado que impede promoção de data, endpoint, bytes ou release | endpoint direto ainda precisa ser resolvido e inspecionado |

## Próxima ação

Resolver a URL direta por evidência oficial contemporânea ou pela interação controlada com o catálogo; registrar redirecionamentos e status; recuperar os bytes somente em ambiente temporário apropriado; calcular checksum; inspecionar o pacote e então decidir sobre promoção do ativo.
