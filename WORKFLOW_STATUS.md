# Estado do workflow

## Regra operacional

Uma tarefa só é concluída após branch, pull request, integração à `main`, GitHub Actions verde e registro no changelog. Alterações públicas também exigem confirmação do deploy. CI verde comprova estrutura interna, não verdade factual externa.

## Limitações

- revisão externa bloqueada nas matrizes BR1–BR5 até cada linha receber evidência oficial atual, data e revisor;
- prioridade e onda operacional não elevam confiança nem autorizam correções no CSV;
- URLs iguais entre homepage e acesso permanecem pendentes;
- novas fontes permanecem fora do CSV;
- v1.0.0 e DOI permanecem bloqueados.

## Backlog

| Frente | Estado | Produto/critério |
|---|---|---|
| QC0 | concluído | 14 regras alinhadas |
| SELECT1 | concluído | política de seleção ativa |
| DATA1-BX | projeção concluída | 51 × 5 dimensões; confiança desconhecida |
| DATA1-BR | auditoria interna concluída | BR1–BR5 cobrem 35 casos |
| DATA1-BR-CLOSE | implementado_pendente_integracao | fila corrigida, evidência longa e documentação coerente |
| DATA1-EXT | próximo ciclo | portão G0 e revisão por ondas |
| DATA1-C | bloqueado | decisões e evidências resolvidas |
| DATA1-D | planejado | 14 regras no CSV 0.8.0 |
| DATA2 | planejado | 51 fontes no esquema final |
| UX5 | parcial | 38 campos e testes de navegador |
| RELEASE2 | bloqueado | G1–G10 e deploy confirmado |
| DOI | bloqueado | G1–G12 e depósito inspecionado |
| RES1 | P3, não bloqueante | resolução por produto |
| EDU1 | P3, não bloqueante | página didática referenciada |

## Estado consolidado

- versão **0.7.0**; CSV **51 × 34**;
- DATA1-B: **16 prontos + 35 revisão_manual**;
- DATA1-BX: confiança `desconhecida`;
- BR1–BR5: **35 de 35** casos distribuídos;
- fila no branch: **35 fontes**;
- prioridade científica: **P0=23, P1=9, P2=3, P3=0**;
- ondas: **G0=1, W1=7, W2=9, W3=7, W4=8, W5=3**;
- evidências externas registradas: **0**;
- candidatos: **18 fora do CSV**;
- esquema 0.8.0 não aplicado; expansão e DOI bloqueados.

## Modelo revisado

`scientific_priority_tier` usa somente impacto e risco científico, comparáveis entre lotes. `execution_wave` organiza escopo, papéis dos links e documentação ausente. Número bruto de flags ou dimensões não entra mais na prioridade.

**G0:** decidir a elegibilidade do Project COSMOS; decisão de escopo não adiciona pontos nem remove a fonte automaticamente.

**W1:** SiBBr, SIRENE, BDiA, Global Carbon Atlas, TerraBrasilis, Google Earth Engine Data Catalog e HidroWeb — sete P0 com homepage e acesso no mesmo destino.

`migration/external_review_evidence.csv` é uma tabela longa: cada linha sustenta uma afirmação e dimensão. Uma fonte pode ter várias evidências para identidade, acesso, API, licença, formato, resolução, atualização, método e citação.

## Autoridade documental

1. `WORKFLOW_STATUS.md`: estado comprovado;
2. `IMPLEMENTATION_WORKFLOW.md`: sequência;
3. `QUALITY_CORRECTION_WORKFLOW.md`: justificativa e checkpoints;
4. `FINAL_OBJECTIVES_AND_DOI_GATES.md`: produto e portões;
5. `METHODOLOGY.md` e `CODEBOOK.md`: interpretação;
6. contratos, matrizes e validadores: execução.

A inspeção está registrada em `DOCUMENTATION_CONSISTENCY_AUDIT.md`. `br_batch_registry.json` substitui integralmente o plano antigo de lotes.

## Próxima execução

1. concluir PR, CI, merge e changelog de DATA1-BR-CLOSE;
2. registrar o fechamento integrado;
3. executar G0 do COSMOS;
4. revisar W1 com documentação oficial e evidências longas;
5. reavaliar a ordem antes de DATA1-C;
6. preservar CSV 51 × 34, versão 0.7.0, candidatos e DOI bloqueado.

RES1 e EDU1 permanecem não bloqueantes para v1.0.0 e DOI.
