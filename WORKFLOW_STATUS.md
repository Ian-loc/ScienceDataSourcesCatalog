# Estado do workflow

## Regra operacional

Uma tarefa só é concluída após branch, pull request, integração à `main`, GitHub Actions verde e registro no changelog. Alterações públicas também exigem confirmação do deploy. CI verde comprova estrutura interna, não verdade factual externa.

## Limitações

- revisão externa bloqueada até cada afirmação receber evidência oficial atual, data e revisor;
- prioridade e onda operacional não elevam confiança nem autorizam correções no CSV;
- URLs iguais entre homepage e acesso permanecem pendentes;
- novas fontes permanecem fora do CSV;
- planilha nativa e `.xlsx` são espelhos derivados e não substituem o CSV canônico;
- o `.xlsx` ainda não está sincronizado com os 34 campos canônicos;
- v1.0.0 e DOI permanecem bloqueados.

## Backlog

| Frente | Estado | Produto/critério |
|---|---|---|
| QC0 | concluído | 14 regras alinhadas |
| SELECT1 | concluído | política de seleção ativa |
| DATA1-BX | projeção concluída | 51 × 5 dimensões; confiança desconhecida |
| DATA1-BR | auditoria interna concluída | BR1–BR5 cobrem 35 casos |
| DATA1-BR-CLOSE | concluído | fila corrigida, evidência longa, documentação e validação integradas |
| STATE-SYNC | concluído | estados documentais corrigidos, contrato criado e estado real dos espelhos verificado |
| MIRROR-XLSX | bloqueado por upload | substituir 51 × 22 por export 51 × 34 e verificar igualdade |
| DATA1-EXT | ativo | portão G0 e revisão por ondas W1A–W1C, W2–W5 |
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
- fila integrada: **35 fontes**;
- prioridade científica: **P0=23, P1=9, P2=3, P3=0**;
- ondas: **G0=1, W1=7, W2=9, W3=7, W4=8, W5=3**;
- W1 subdividida operacionalmente em **W1A=2, W1B=3, W1C=2**;
- evidências externas registradas: **0**;
- candidatos: **18 fora do CSV**;
- esquema 0.8.0 não aplicado; expansão e DOI bloqueados;
- planilha nativa: **51 × 34**, cabeçalhos canônicos verificados;
- `.xlsx`: **51 × 22**, download bruto verificado; substituição falhou duas vezes por proxy `407`.

## STATE-SYNC

O ciclo foi integrado pelo PR #32 no commit `f35b2c766043308d9e19751539a2c99972df949b`. O run `29836549232` passou integralmente, incluindo workflow, CSV, esquema, matrizes, DOI e interface. O changelog do Drive registra a integração e uma correção factual posterior.

Produtos concluídos:

- DATA1-BR-CLOSE alinhado como concluído e DATA1-EXT como ativo;
- `DRIVE_MIRROR_CONTRACT.md` integrado;
- W1 subdividida em W1A–W1C sem alteração de composição;
- estado real dos dois arquivos do Drive verificado;
- declaração incorreta de sincronização total corrigida no changelog;
- pendência do `.xlsx` isolada em MIRROR-XLSX, sem bloquear DATA1-EXT.

## Fechamento DATA1-BR-CLOSE

Enquanto esta sessão ainda preparava o pull request, outra sessão abriu e integrou o PR #28, gerando o merge commit `df66ab15a064e2b1b70a6e9387a1abcc20b7358a`. O estado foi novamente validado pelo PR #29, run `29778282362`, e o fechamento documental foi integrado pelo PR #30 no commit `ced7bc7274b740fdc0eed4963d36f0fc33b05d9f`.

`scientific_priority_tier` usa somente impacto e risco comparáveis. `execution_wave` organiza escopo, papéis dos links e documentação ausente. Número bruto de flags ou dimensões não entra na prioridade.

`migration/external_review_evidence.csv` registra uma linha por afirmação e dimensão; nenhuma evidência altera o CSV automaticamente.

## Espelhamento do Drive

A autoridade e a direção do fluxo são definidas em `DRIVE_MIRROR_CONTRACT.md`.

- GitHub `main` e `data/data_resources.csv` permanecem canônicos;
- a planilha nativa corresponde atualmente ao catálogo 0.7.0 de 51 × 34;
- o `.xlsx` permanece histórico, com 51 × 22;
- um espelho sincronizado deve declarar versão, esquema, commit-fonte, data e resultado da comparação;
- MIRROR-XLSX deve ser retomado quando o upload de substituição estiver operacional;
- a regeneração obrigatória 51 × 38 ocorre após DATA1-C e DATA1-D.

## Próximos produtos

1. executar **G0** e produzir parecer de elegibilidade do Project COSMOS e regra geral para recursos bibliométricos;
2. executar **W1A** para TerraBrasilis e Google Earth Engine Data Catalog;
3. executar **W1B** para SiBBr, BDiA e HidroWeb;
4. executar **W1C** para SIRENE e Global Carbon Atlas;
5. realizar checkpoint científico conjunto pós-W1A–W1C;
6. retomar **MIRROR-XLSX** quando o upload de substituição estiver disponível;
7. produzir prévia 0.8.0 somente depois das decisões críticas, em arquivo não canônico;
8. preservar CSV 51 × 34, versão 0.7.0, candidatos e DOI bloqueado.

A autoridade documental segue `WORKFLOW_STATUS.md`, `IMPLEMENTATION_WORKFLOW.md`, `QUALITY_CORRECTION_WORKFLOW.md`, `FINAL_OBJECTIVES_AND_DOI_GATES.md`, `METHODOLOGY.md`, `CODEBOOK.md`, `DRIVE_MIRROR_CONTRACT.md` e contratos executáveis. A inspeção está em `DOCUMENTATION_CONSISTENCY_AUDIT.md`.

RES1 e EDU1 permanecem não bloqueantes para v1.0.0 e DOI.
