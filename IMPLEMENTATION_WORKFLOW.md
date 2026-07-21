# Workflow de implementação — interface, dados, governança e release

## Objetivo

Melhorar descoberta e comparação, corrigir ambiguidades científicas e preparar uma versão estável sem misturar revisão externa, migração, redesign e DOI no mesmo ciclo.

## Princípios

1. `data/data_resources.csv` é a fonte canônica;
2. JSON e metadados do site são derivados;
3. Drive mantém changelog executivo, histórico e espelhos derivados, nunca uma fonte concorrente;
4. CI verde não comprova verdade factual externa;
5. nenhuma fonte é declarada revisada sem evidência atual, data e revisor;
6. nenhuma publicação é confirmada sem evidência do site;
7. expansão não precede estabilização das 51 fontes;
8. v1.0.0 e DOI exigem fechamento técnico, científico e documental;
9. o depósito final será classificado como Dataset;
10. licenças de código e dados permanecem separadas;
11. planilha nativa e `.xlsx` devem declarar o commit-fonte e ser regeneradas do CSV, conforme `DRIVE_MIRROR_CONTRACT.md`.

## Ciclos concluídos

| Ciclo | Resultado |
|---|---|
| UX1–UX4 | arquitetura, filtros, cards, acessibilidade e desempenho |
| DATA1-A | auditoria e proposta do esquema 0.8.0 |
| DATA1-B | matriz inicial de migração |
| QC0 | 14 regras alinhadas |
| SELECT1 | política de seleção e cobertura |
| DATA1-BX | projeção de cinco dimensões para 51 fontes |
| DATA1-BR | auditorias internas BR1–BR5 e cobertura dos 35 casos |
| DATA1-BR-CLOSE | fila comparável, ondas operacionais e evidência longa integradas |
| OBJ | objetivos finais e portões para DOI |

## Ordem operacional atual

| Ordem | Ciclo | Estado | Produto |
|---:|---|---|---|
| 1 | QC0 | concluído | contrato semântico comum |
| 2 | SELECT1 | concluído | política de elegibilidade e duplicidade |
| 3 | DATA1-BX | concluído como projeção | 51 × 5 dimensões; confiança desconhecida |
| 4 | DATA1-BR | auditoria interna concluída | cinco lotes reais de sete fontes |
| 5 | DATA1-BR-CLOSE | concluído | fila, ondas e evidência longa |
| 6 | STATE-SYNC | implementado_pendente_integracao | estados documentais e contrato de espelhamento coerentes |
| 7 | DATA1-EXT | ativo | decisão G0 e revisão W1–W5 |
| 8 | DATA1-C | bloqueado | CSV 0.8.0 com 38 campos |
| 9 | DATA1-D | planejado | 14 regras ativas no CSV final |
| 10 | DATA2 | planejado | 51 fontes revisadas no esquema final |
| 11 | UX5 | parcial | interface e filtros dos 38 campos |
| 12 | RELEASE2 | bloqueado | v1.0.0 e deploy confirmado |
| 13 | DOI | bloqueado | G1–G12 e depósito inspecionado |
| 14 | RES1 | não bloqueante | resolução por produto |
| 15 | EDU1 | não bloqueante | conteúdo didático referenciado |

## STATE-SYNC

O ciclo corrige a divergência entre documentos de estado e formaliza o espelhamento do catálogo no Drive.

Produtos:

1. `DATA1-BR-CLOSE` aparece como concluído e `DATA1-EXT` como ativo em todos os workflows operacionais;
2. `DRIVE_MIRROR_CONTRACT.md` define autoridade, direção do fluxo, metadados, verificação e tratamento de concorrência;
3. o estado observado dos espelhos é registrado: GitHub 0.7.0 com 51 × 34; Drive histórico com 51 × 22;
4. nenhuma tabela do Drive é promovida a fonte canônica;
5. o ciclo só será encerrado após PR, CI, merge e registro no changelog.

## DATA1-BR-CLOSE

`br_batch_registry.json` é o único registro dos lotes. A matriz histórica `data1br_review_batches.csv` foi removida.

A fila externa não usa quantidade bruta de flags ou dimensões. A prioridade científica deriva de impacto e risco. As ondas operacionais tratam decisão de escopo, links e documentação ausente.

`external_review_evidence.csv` guarda uma linha por fonte, dimensão e afirmação. A fila contém ordem, estado e contagem de evidências; não contém uma única URL genérica para toda a fonte.

## DATA1-EXT

1. executar `G0` e decidir a elegibilidade do Project COSMOS;
2. revisar `W1A`: TerraBrasilis e Google Earth Engine Data Catalog;
3. revisar `W1B`: SiBBr, BDiA e HidroWeb;
4. revisar `W1C`: SIRENE e Global Carbon Atlas;
5. registrar páginas institucionais, acesso, documentação técnica, licença, método, versão, resolução e limitações em linhas distintas;
6. atualizar fila e propostas sem escrever automaticamente no CSV;
7. reavaliar a ordem após G0 e o fechamento conjunto de W1A–W1C.

A subdivisão de W1 reduz o tamanho de cada PR sem alterar as sete fontes prioritárias nem a lógica da fila.

## DATA1-C e DATA1-D

Somente após decisões críticas e evidências suficientes:

1. atualizar o cabeçalho para 38 campos;
2. migrar as 51 linhas em uma branch atômica;
3. preservar IDs e conteúdo narrativo;
4. atualizar codebook, metodologia, scripts e interface;
5. atualizar `CITATION.cff` para 0.8.0 apenas junto da migração;
6. ativar as 14 regras no CSV final;
7. não criar DOI.

## Espelhamento do Drive

A planilha nativa e o `.xlsx` seguem `DRIVE_MIRROR_CONTRACT.md`.

- o estado atual de 22 campos é histórico e não substitui o CSV 51 × 34;
- um snapshot 0.7.0 de 34 campos pode ser produzido para consulta operacional;
- após DATA1-C e DATA1-D, os dois espelhos devem ser obrigatoriamente regenerados com 51 × 38;
- qualquer espelho declarado sincronizado deve informar versão, esquema, commit-fonte, data de geração e resultado da comparação.

## DATA2, UX5 e release

DATA2 revisa todas as 51 fontes no esquema final. UX5 expõe os 38 campos e executa testes funcionais. RELEASE2 exige documentação coerente, v1.0.0, tag/release e deploy confirmado. DOI exige inspeção do depósito Dataset e todos os portões de `FINAL_OBJECTIVES_AND_DOI_GATES.md`.

## Enriquecimentos

RES1 documentará resolução por produto sem inferir valores do zoom. EDU1 será uma página separada sobre fenômenos, medição, tipos de dados e incertezas. Ambos são não bloqueantes.

## Checkpoints

Reavaliar após STATE-SYNC, G0, W1A–W1C, migração 0.8.0, regeneração dos espelhos, primeiros lotes DATA2 e testes de interface.
