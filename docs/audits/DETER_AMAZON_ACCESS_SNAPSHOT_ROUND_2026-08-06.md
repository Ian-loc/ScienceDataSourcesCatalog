# Auditoria — acesso e snapshot operacional DETER Amazônia

**Data/hora:** 2026-08-06 00:29–00:43, `America/Sao_Paulo`  
**Família:** `PF000002`  
**Produto-pai candidato:** `PD-DETER-AMZ-ALERTS`

## Objetivo

Registrar evidências oficiais de acesso e um snapshot operacional contemporâneo do DETER Amazônia sem transformar página de download, relatório agregado, data de corte ou totais reportados em release científica, ativo ou prova de funcionamento de endpoint.

## Evidência oficial consolidada

1. O TerraBrasilis informa que os dados DETER Amazônia Não Floresta são disponibilizados em formato Shapefile na área de downloads desde 8 de novembro de 2023.
2. O registro não florestal permanece recuperável na busca diária do catálogo oficial, com caráter experimental, início em agosto de 2023, classes e esquema parcial.
3. O relatório oficial DETER Amazônia Não Floresta apresenta série iniciada em 1º de agosto de 2023 e snapshot com corte em 20 de julho de 2026.
4. No snapshot foram exibidos 1.356,46 km² de alertas acumulados de supressão e 56.823,45 km² de alertas acumulados de degradação.
5. A representação pública inspecionada não expõe UUID individual verificável para o metadado não florestal nem URL direta do pacote Shapefile.

## Decisão curatorial

O relatório é uma projeção operacional agregada e datada. Ele não substitui:

- produto e release;
- distribuição Shapefile;
- pacote de arquivos;
- inventário de feições;
- checksum;
- esquema integral;
- citação da release.

Os totais do relatório são observações de um snapshot e podem mudar com atualização, consolidação ou revisão dos dados experimentais. A data de 20 de julho de 2026 é o corte do relatório recuperado, não um identificador de release.

A presença de uma distribuição na página de downloads comprova descoberta e forma declarada de acesso, mas não comprova URL direta, estado HTTP, redirecionamentos, autenticação, identidade dos bytes ou disponibilidade operacional corrente.

## Estados preservados como não resolvidos

- UUID individual do metadado não florestal;
- release das distribuições florestal e não florestal;
- URLs diretas;
- respostas HTTP e redirecionamentos;
- autenticação;
- bytes, tamanho e checksums;
- CRS, geometria, esquema integral, domínios e nulos;
- cobertura territorial e temporal observada nos pacotes;
- licença, atribuição e citação por release.

## Ocorrência

**ID:** `I1-20260806-043`  
**Categoria:** conversão indevida de relatório operacional ou página de download em release/ativo  
**Severidade:** `high` para promoção das distribuições  
**Estado:** `corrected`  
**Correção:** contrato e validador separam canal de acesso, metadado, relatório agregado, distribuição e ativo; preservam estados negativos de endpoint e promoção.  
**Teste:** o gate é encadeado ao validador científico DETER Amazônia já executado pelo CI.  
**Risco residual:** o UUID não florestal e os endpoints diretos continuam indisponíveis na representação pública recuperada.

## Artefatos

- `database/mappings/deter_amazon_access_snapshot_guard_2026.json`;
- `scripts/validate_deter_amazon_access_snapshot_guard.py`;
- encadeamento em `scripts/validate_deter_amazon_scientific_boundary_guard.py`.

## Resultado

A unidade avançou de distribuição catalogada com acesso genérico para um perfil operacional datado, verificável e explicitamente não promovido. O próximo avanço válido exige resolver individualmente o registro de metadados não florestal e as URLs diretas das duas distribuições.
