# Auditoria — proteção de escopo do TerraClass Amazônia 2020

**Data e horário:** 2026-08-05 12:31 America/Sao_Paulo  
**PR:** #54  
**Branch:** `agent/consolidate-instance-1-relational-catalog`

## Objetivo

Preservar a identidade científica e operacional do release `PR000005` — TerraClass Amazônia 2020 — diante da publicação, em junho de 2026, de uma edição TerraClass 2024 com novo contexto de dados, processamento e cobertura.

## Risco identificado

A documentação oficial de 2024 informa uso de Sentinel-2/MSI, produto de 16 dias, resolução espacial de 10 m e processamento com Brazil Data Cube/SITS. Esses elementos são válidos para o mapeamento 2024, mas não comprovam automaticamente o CRS, a grade, a resolução nominal de saída, o método ou a estrutura do ativo de 2020.

Sem um portão explícito, uma atualização curatorial poderia:

- copiar propriedades do release 2024 para o release 2020;
- substituir `PR000005` pela edição mais recente;
- confundir resolução dos insumos com resolução do produto de saída;
- generalizar entre Amazônia Legal, bioma Amazônia, áreas desflorestadas pelo PRODES e mapas de cobertura do bioma;
- preencher legenda, licença, citação ou checksum sem evidência específica.

## Resultado material

Foi criado `database/mappings/terraclass_release_scope_guard_2026.json`, que:

- mantém `DP000005` e `PR000005` vinculados ao ano de referência 2020;
- mantém o ativo em `not_inspected` e a revisão em `in_progress`;
- exige que CRS, grade, pixel de saída, legenda integral, checksum, licença e citação permaneçam nulos;
- registra o contexto 2024 em bloco separado e explicitamente não transferível;
- determina que um release TerraClass 2024 receba ID, evidências, distribuições, ativo e revisão próprios;
- lista requisitos objetivos antes da aprovação curatorial de 2020.

## Evidências

Foram diferenciadas quatro categorias de evidência oficial:

1. página histórica do projeto TerraClass — finalidade e relação com PRODES;
2. nota oficial de 2020 sobre resultado parcial de vegetação secundária;
3. comunicação oficial de 2026 sobre o release 2024;
4. catálogo oficial de dados abertos — categorias gerais TIFF e web.

Cada evidência contém uma restrição explícita para impedir extrapolação ao contrato técnico do release 2020.

## Auditoria de delta

Foi criado `scripts/validate_terraclass_release_scope_guard.py`, integrado ao workflow principal. O validador exige:

- IDs e rótulo corretos;
- promoção desautorizada;
- campos técnicos não comprovados nulos;
- distinção rígida entre 2020 e 2024;
- controles contra cópia, substituição e inferência;
- quatro tipos de evidência com escopo e restrição;
- regra de criação de release independente;
- requisitos de metadado, inspeção do ativo, CRS, legenda, SHA-256, licença e reconciliação com acurácia.

## Ocorrência

### I1-20260805-024

- **Severidade:** `high`
- **Estado:** `corrected`
- **Categoria:** volatilidade de release e transferência indevida de metadados
- **Entidade afetada:** TerraClass Amazônia 2020 / `PR000005`
- **Descrição:** a publicação de uma edição 2024 tecnicamente distinta cria risco de retroprojetar propriedades atuais para o release 2020 ou de substituir o release histórico no catálogo normalizado.
- **Correção aplicada:** portão legível por máquina, validador dedicado e integração ao CI.
- **Teste de verificação:** `python3 scripts/validate_terraclass_release_scope_guard.py`.
- **Risco residual:** o ativo 2020 ainda não foi localizado e inspecionado; a aprovação curatorial continua bloqueada somente para essa unidade.

## Estado

O risco de mutação silenciosa foi corrigido estruturalmente. O produto permanece parcial até a inspeção direta do ativo e dos metadados específicos de 2020.

## Próxima unidade

1. localizar recurso 2020 específico no GeoPortal, catálogo de dados abertos ou registro de metadados;
2. recuperar um ativo manejável;
3. inspecionar CRS, grade, tipo raster/vetor, bandas ou campos e legenda;
4. calcular SHA-256;
5. reconciliar o ativo com o perfil de acurácia já registrado;
6. criar separadamente o produto/release 2024 apenas quando houver pacote curatorial completo.
