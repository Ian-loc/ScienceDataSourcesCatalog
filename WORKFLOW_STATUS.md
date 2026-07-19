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
| QC0 | Alinhar 14 regras semânticas | em desenvolvimento | auditoria, JSON e CI devem exigir o mesmo conjunto exato |
| SELECT1 | Inclusão, exclusão, duplicidade e lacunas | em desenvolvimento | política integrada e validada |
| DATA1-BX | Completar campos da matriz | planejado e prioritário | incluir produtos, visualizações, origens, temporalidade e condições de acesso |
| DATA1-BR | Revisão dos 35 casos pendentes | bloqueado por DATA1-BX | cinco lotes de sete; evidência oficial obrigatória |
| DATA1-C | Migração atômica para 38 campos | bloqueado | 51 registros prontos e matriz completa |
| DATA1-D | Validação semântica do esquema final | planejado | 14 regras ativas contra o CSV 0.8.0 |
| DATA2 | Revisar as 51 fontes no esquema final | planejado | evidência, links, acesso, formatos, licença e data revisados |
| UX5 | Interface dos 38 campos e testes de navegador | planejado | campos exibidos e fluxos funcionais verificados |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 |
| RELEASE2 | Criar versão 1.0.0 | bloqueado | G1–G10 concluídos e deploy confirmado |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | G1–G12 concluídos e depósito inspecionado |
| RES1 | Faixas de resolução por produto | P3, não bloqueante | tabela auxiliar com evidência e unidades comparáveis |
| EDU1 | Página didática de fenômenos | P3, não bloqueante | conteúdo referenciado e ligado às fontes do catálogo |
| POST-DOI | Propagar identificadores | bloqueado | DOI de versão e conceito em repositório, site, ORCID e currículos |

## Estado consolidado

- **Versão formal:** 0.7.0;
- **Fontes:** 51;
- **Campos canônicos atuais:** 34;
- **UX1–UX4:** integrados e validados;
- **DATA1-A e DATA1-B:** integrados e validados;
- **G1:** concluído;
- **G2–G12:** parciais ou bloqueados;
- **Matriz atual:** 16 registros prontos e 35 em revisão manual;
- **Matriz completa:** ainda não existe; DATA1-BX pendente;
- **Esquema 0.8.0:** ainda não aplicado;
- **Expansão:** bloqueada; candidatos podem ser registrados separadamente;
- **Publicação atual:** ainda não confirmada por inspeção direta;
- **v1.0.0:** bloqueada;
- **DOI:** bloqueado e não criado.

## Correção de rota atual

A auditoria transversal identificou:

1. 14 regras documentadas, mas somente 11 no contrato JSON;
2. matriz sem todos os campos cuja normalização foi prometida;
3. ausência de política formal de seleção e lacunas;
4. risco de confundir validação estrutural com verificação científica.

A resposta operacional é:

- concluir QC0 e SELECT1;
- executar DATA1-BX antes de BR1;
- manter DATA1-BR bloqueado até a matriz cobrir todos os campos-alvo;
- não expandir o CSV antes de DATA2;
- manter RES1 e EDU1 como enriquecimentos posteriores e não bloqueantes.

## Resolução e página didática

### RES1

Registrar resolução no nível de produto, distinguindo tamanho de célula raster, escala cartográfica, precisão de coordenadas, resolução temporal e limite de zoom. Não inferir resolução a partir do visualizador. A estrutura proposta é `data/product_resolution_examples.csv`.

### EDU1

Criar página separada para explicar fenômenos, formas de medição, tipos de dados, limitações e fontes relacionadas. Temas iniciais: clima, biodiversidade, fragmentação, carbono, solos, uso da terra, agroflorestas, sistemas alimentares e sensoriamento remoto.

RES1 e EDU1 não condicionam v1.0.0 ou DOI, salvo quando revelarem erro factual no catálogo atual.

## Checkpoints de reordenação

Reavaliar a ordem após:

1. QC0 + SELECT1;
2. DATA1-BX;
3. cada lote BR1–BR5;
4. migração 0.8.0;
5. primeiros lotes DATA2;
6. testes funcionais da interface.

## Próxima execução

1. validar e integrar QC0 + SELECT1;
2. ampliar a matriz em DATA1-BX;
3. revisar a nova matriz e seu validador;
4. somente então iniciar BR1;
5. preservar CSV 51 × 34, versão 0.7.0 e DOI bloqueado até os portões correspondentes.

Consulte `QUALITY_CORRECTION_WORKFLOW.md`, `SELECTION_AND_COVERAGE_POLICY.md`, `FINAL_OBJECTIVES_AND_DOI_GATES.md`, `IMPLEMENTATION_WORKFLOW.md` e `DATA1_SCHEMA_AUDIT.md`.
