# Estado do workflow

## Regra operacional

Uma tarefa só é considerada concluída quando estiver:

1. implementada em branch;
2. revisada em pull request;
3. integrada à `main`;
4. validada pelo GitHub Actions;
5. publicada, quando afetar o site;
6. registrada no changelog do GitHub e no registro executivo do Google Drive.

CI verde comprova estrutura e coerência interna. A verificação factual de fontes externas exige evidência atual e inspeção humana.

## Limitações atuais

- GitHub Issues está desativado; este arquivo é o backlog versionado autoritativo.
- A publicação só será marcada como confirmada mediante inspeção direta do site ou evidência equivalente.
- A revisão externa exige acesso atual à documentação oficial.
- O acesso web de pesquisa não está disponível neste ambiente; nenhuma fonte será declarada revisada apenas por inferência.
- Novas fontes permanecem fora do CSV até a estabilização das 51 atuais.

## Backlog

| Prioridade | Frente | Estado | Evidência ou critério de conclusão |
|---|---|---|---|
| P0 | Identificação verificável do build | integrado | `build-meta.json` contém versão, commit, data, fontes e campos |
| P0 | Confirmar deploy posterior ao merge | bloqueado | requer inspeção direta do site ou evidência equivalente |
| UX1–UX4 | Interface, filtros, cards, acessibilidade e desempenho | validado e documentado | PRs #5, #7, #9 e #11; CI e Drive atualizados |
| OBJ | Objetivos finais e portões para DOI | concluído | PR #17; run 29704132742; Drive atualizado |
| DATA1-A | Auditoria e projeto do esquema 0.8.0 | validado e documentado | PR #13; run 29702732587 |
| DATA1-B | Matriz inicial de migração | validado e documentado | PR #15; run 29703654373 |
| QC0 | Alinhar 14 regras semânticas | validado e documentado | PR #19; run 29706338430 |
| SELECT1 | Inclusão, exclusão, duplicidade e lacunas | validado e documentado | PR #19; política integrada e validada |
| CAND1 | Fila versionada de candidatos | em desenvolvimento | OWID registrado como CAND0001; validação e PR pendentes |
| DATA1-BX | Completar campos da matriz | em desenvolvimento | contrato, matriz de 51 IDs e validação por campo; preenchimento ainda pendente |
| DATA1-BR | Revisão dos 35 casos pendentes | bloqueado por DATA1-BX | cinco lotes de sete; evidência oficial obrigatória |
| DATA1-C | Migração atômica para 38 campos | bloqueado | 51 registros prontos e matriz completa |
| DATA1-D | Validação semântica do esquema final | planejado | 14 regras ativas contra o CSV 0.8.0 |
| DATA2 | Revisar as 51 fontes no esquema final | planejado | links, acesso, formatos, licença e data revisados |
| UX5 | Interface dos 38 campos e testes de navegador | planejado | campos exibidos e fluxos funcionais verificados |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 |
| RELEASE2 | Criar versão 1.0.0 | bloqueado | G1–G10 concluídos e deploy confirmado |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | G1–G12 concluídos e depósito inspecionado |
| RES1 | Faixas de resolução por produto | P3, não bloqueante | tabela auxiliar com evidência e unidades comparáveis |
| EDU1 | Página didática de fenômenos | P3, não bloqueante | conteúdo referenciado e ligado às fontes do catálogo |
| POST-DOI | Propagar identificadores | bloqueado | DOI de versão e conceito em repositório, site, ORCID e currículos |

## Estado consolidado

- **Versão formal:** 0.7.0;
- **Fontes canônicas:** 51;
- **Campos canônicos atuais:** 34;
- **Fila de candidatos:** 1 registro, separado do CSV canônico;
- **CAND0001:** Our World in Data, aguardando evidência oficial;
- **UX1–UX4:** integrados e validados;
- **DATA1-A e DATA1-B:** integrados e validados;
- **QC0 e SELECT1:** integrados e validados no PR #19;
- **G1:** concluído;
- **G2–G12:** parciais ou bloqueados;
- **Matriz DATA1-B:** 16 registros prontos e 35 em revisão manual;
- **DATA1-BX:** contrato e estrutura de 51 linhas criados; cinco dimensões ainda não preenchidas;
- **Esquema 0.8.0:** ainda não aplicado;
- **Expansão:** bloqueada; candidatos podem ser registrados separadamente;
- **Publicação atual:** ainda não confirmada por inspeção direta;
- **v1.0.0:** bloqueada;
- **DOI:** bloqueado e não criado.

## Correção de rota atual

A auditoria transversal encontrou quatro fragilidades. Duas foram corrigidas no PR #19:

1. as 14 regras semânticas foram alinhadas entre documentação, contrato e CI;
2. a política de inclusão, exclusão, duplicidade, candidatos e lacunas foi formalizada.

Persistem duas pendências materiais:

1. a matriz DATA1-B não cobre `data_product_types`, `visualization_types`, `data_sources`, `temporal_resolution` e `access_conditions`;
2. uma confiança global por linha não representa adequadamente a incerteza diferente entre campos.

A resposta operacional é:

- usar o contrato DATA1-BX com confiança por dimensão e estados explícitos de revisão;
- carregar valores do CSV apenas como ponto de partida, sem tratá-los como verificação externa;
- manter DATA1-BR bloqueado até as 51 linhas cobrirem as cinco dimensões;
- não expandir o CSV antes de DATA2;
- registrar novas indicações apenas em `candidates/source_candidates.csv`;
- manter RES1 e EDU1 como enriquecimentos posteriores e não bloqueantes.

## Resolução e página didática

### RES1

Registrar resolução no nível de produto, distinguindo tamanho de célula raster, escala cartográfica, precisão de coordenadas, resolução temporal e limite de zoom. Não inferir resolução a partir do visualizador. A estrutura proposta é `data/product_resolution_examples.csv`.

### EDU1

Criar página separada para explicar fenômenos, formas de medição, tipos de dados, limitações e fontes relacionadas. Temas iniciais: clima, biodiversidade, fragmentação, carbono, solos, uso da terra, agroflorestas, sistemas alimentares e sensoriamento remoto.

RES1 e EDU1 não condicionam v1.0.0 ou DOI, salvo quando revelarem erro factual no catálogo atual.

## Checkpoints de reordenação

Reavaliar a ordem após:

1. QC0 + SELECT1 — concluído;
2. DATA1-BX;
3. cada lote BR1–BR5;
4. migração 0.8.0;
5. primeiros lotes DATA2;
6. testes funcionais da interface.

## Próxima execução

1. carregar na matriz DATA1-BX os cinco valores atuais de cada uma das 51 fontes, marcando-os como não verificados externamente;
2. atribuir confiança por campo e registrar todas as dimensões ainda pendentes;
3. validar a matriz completa e revisar qualquer discrepância com o CSV canônico;
4. somente então iniciar BR1;
5. manter OWID e outros candidatos fora do CSV até um ciclo autorizado de expansão;
6. preservar CSV 51 × 34, versão 0.7.0 e DOI bloqueado até os portões correspondentes.

Consulte `QUALITY_CORRECTION_WORKFLOW.md`, `SELECTION_AND_COVERAGE_POLICY.md`, `FINAL_OBJECTIVES_AND_DOI_GATES.md`, `IMPLEMENTATION_WORKFLOW.md`, `DATA1_SCHEMA_AUDIT.md`, `migration/data1bx_contract.json` e `candidates/README.md`.
