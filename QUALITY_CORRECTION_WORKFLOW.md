# Workflow de correções de qualidade

## Objetivo

Corrigir fragilidades antes de migrar para 0.8.0, expandir fontes ou preparar v1.0.0 e DOI. Controle de processo não substitui verificação científica: CI verde comprova estrutura, não atualidade ou correção de links, APIs, licenças, formatos e resoluções.

## Regras de prioridade

1. corrigir contradições entre documentos, contratos e validadores;
2. revisar as 51 fontes atuais antes de expandir;
3. separar risco científico, esforço operacional e decisão de escopo;
4. registrar evidência por afirmação e dimensão;
5. não alterar CSV, versão ou DOI enquanto os portões estiverem bloqueados;
6. reavaliar a ordem após cada ciclo relevante;
7. manter RES1 e EDU1 como enriquecimentos não bloqueantes.

## Ordem operacional atual

| Ordem | Ciclo | Estado | Produto/critério |
|---:|---|---|---|
| 1 | QC0 | concluído | 14 regras semânticas alinhadas |
| 2 | SELECT1 | concluído | política de seleção e cobertura |
| 3 | DATA1-BX | projeção concluída | 51 × 5 dimensões; confiança desconhecida |
| 4 | DATA1-BR | auditoria interna concluída | BR1–BR5 cobrem 35 casos |
| 5 | DATA1-BR-CLOSE | implementado_pendente_integracao | fila comparável e evidência longa |
| 6 | DATA1-EXT | próximo ciclo | G0 e ondas W1–W5 com evidência oficial |
| 7 | DATA1-C | bloqueado | migração atômica para 38 campos |
| 8 | DATA1-D | planejado | 14 regras no CSV final |
| 9 | DATA2 | planejado | revisão das 51 fontes no esquema final |
| 10 | UX5 | parcial | 38 campos e testes funcionais |
| 11 | RELEASE2 | bloqueado | v1.0.0 e deploy confirmado |
| 12 | DOI | bloqueado | G1–G12 concluídos |
| 13 | RES1 | P3 | resolução por produto |
| 14 | EDU1 | P3 | página didática referenciada |

## DATA1-BR-CLOSE

A primeira proposta de fila somava quantidade de flags e dimensões. Isso era inadequado porque BR1–BR5 foram descritos com granularidades diferentes.

O modelo corrigido usa:

- `scientific_priority_tier`: somente impacto e risco científico;
- `execution_wave`: escopo, papéis dos links, documentação ausente e sequência;
- `external_review_evidence.csv`: várias evidências por fonte, dimensão e afirmação.

O Project COSMOS é tratado em `G0`, portão de escopo separado. Ele não recebe pontos artificiais e não é removido automaticamente.

## DATA1-EXT

Cada evidência deve registrar:

- fonte e dimensão revisada;
- afirmação e valor atual;
- valor observado oficialmente;
- URL e tipo de evidência;
- data, revisor e organização;
- suporte ao valor atual;
- ação e valor propostos;
- limitações.

Documentação oficial sustenta API, formato, licença e autenticação. Literatura revisada por pares confronta identidade, uso efetivo, limitações e interpretação; não substitui documentação técnica atual.

## Migração e revisão final

DATA1-C somente começa quando decisões críticas estiverem resolvidas. A migração deve preservar 51 IDs, todo o conteúdo científico e produzir 38 campos. DATA1-D ativa as 14 regras no CSV final. DATA2 revisa as 51 fontes no esquema estabilizado.

## RES1 — resolução por produto

Não é cientificamente seguro inferir resolução pelo zoom de um visualizador. Distinguir célula raster, escala cartográfica, precisão de coordenadas, suporte espacial, resolução temporal e limite de exibição.

A tabela futura `data/product_resolution_examples.csv` deve registrar produto, tipo de resolução, valores mais fino e mais grosseiro, unidade ou escala, versão, evidência, data, confiança e notas. Faixas só podem ser comparadas quando usam a mesma dimensão e unidade.

RES1 é não bloqueante para v1.0.0 e DOI, salvo quando revelar erro factual no valor atual.

## EDU1 — página didática

A página didática deve explicar fenômeno, medição, tipos de dados, limitações, fontes relacionadas e referências. Linguagem acessível não autoriza simplificação enganosa ou inferência causal por visualização.

EDU1 é não bloqueante para v1.0.0 e DOI e deve começar após DATA2 ou com capacidade editorial separada.

## Checkpoints de reordenação

Reavaliar após DATA1-BR-CLOSE, G0, W1, migração 0.8.0, primeiros lotes DATA2 e testes funcionais. Uma tarefa sobe quando bloqueia dependências, evita perda, corrige informação pública ou reduz retrabalho; desce quando é apenas enriquecimento ou pode ser entregue com segurança depois.

## Estado protegido

- versão formal 0.7.0;
- CSV 51 × 34 até DATA1-C;
- `doi_allowed = false`;
- nenhuma nova fonte entra diretamente no catálogo;
- candidatos permanecem fora do CSV;
- RES1 e EDU1 não desbloqueiam nem bloqueiam o DOI.
