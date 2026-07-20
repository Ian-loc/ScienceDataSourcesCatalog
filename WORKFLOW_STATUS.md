# Estado do workflow

## Regra operacional

Uma tarefa só é considerada concluída quando estiver implementada em branch, revisada em pull request, integrada à `main`, validada pelo GitHub Actions e registrada no changelog. Quando afetar o site, a publicação também precisa ser confirmada.

CI verde comprova estrutura e coerência interna. Não comprova, sozinho, que uma fonte externa esteja atual, acessível ou cientificamente correta.

## Limitações atuais

- a publicação só será marcada como confirmada mediante inspeção direta do site ou evidência equivalente;
- a revisão factual exige documentação oficial atual;
- o acesso web de pesquisa não está disponível neste ambiente;
- novas indicações podem ser registradas, mas novas fontes permanecem fora do CSV até a estabilização das 51 atuais;
- candidatos identificados por conhecimento prévio ou URL submetida permanecem em triagem, sem decisão final.

## Backlog

| Prioridade | Frente | Estado | Evidência ou critério de conclusão |
|---|---|---|---|
| P0 | Identificação verificável do build | integrado | versão, commit, fontes e campos em `build-meta.json` |
| P0 | Confirmar deploy posterior ao merge | bloqueado | inspeção direta do site ou evidência equivalente |
| UX1–UX4 | Interface, filtros, cards, acessibilidade e desempenho | validado e documentado | PRs #5, #7, #9 e #11 |
| OBJ | Objetivos finais e portões para DOI | concluído | PR #17 |
| DATA1-A | Auditoria e projeto do esquema 0.8.0 | validado e documentado | PR #13 |
| DATA1-B | Matriz inicial de migração | validado e documentado | PR #15 |
| QC0 | Alinhar 14 regras semânticas | validado e documentado | PR #19 |
| SELECT1 | Inclusão, exclusão, duplicidade e lacunas | validado e documentado | PR #19 |
| CAND1 | Fila versionada de candidatos | em desenvolvimento | 18 candidatos; nenhum incluído no CSV |
| DATA1-BX | Completar campos da matriz | projeção canônica concluída | 51 fontes × 5 dimensões carregadas; confiança desconhecida; revisão externa pendente |
| DATA1-BR | Revisão dos 35 casos pendentes | bloqueado por DATA1-BX | iniciar somente após definição do lote e evidência oficial disponível |
| DATA1-C | Migração atômica para 38 campos | bloqueado | decisões DATA1-B e DATA1-BX revisadas |
| DATA1-D | Validação semântica do esquema final | planejado | 14 regras ativas no CSV 0.8.0 |
| DATA2 | Revisar as 51 fontes no esquema final | planejado | links, acesso, formatos, licença, evidência e data revisados |
| UX5 | Interface dos 38 campos e testes de navegador | em desenvolvimento parcial | resumo público de qualidade criado; adaptação aos 38 campos ainda pendente |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 |
| RELEASE2 | Criar versão 1.0.0 | bloqueado | G1–G10 concluídos e deploy confirmado |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | G1–G12 concluídos e depósito inspecionado |
| RES1 | Faixas de resolução por produto | P3, não bloqueante | tabela auxiliar com evidência e unidades comparáveis |
| EDU1 | Página didática de fenômenos | P3, não bloqueante | conteúdo referenciado e ligado às fontes |
| POST-DOI | Propagar identificadores | bloqueado | DOI de versão e conceito em repositório, site, ORCID e currículos |

## Estado consolidado

- **Versão formal:** 0.7.0;
- **Fontes canônicas:** 51;
- **Campos canônicos:** 34;
- **Fila de candidatos:** 18 registros separados do CSV;
- **Candidatos prioritários de saúde e demografia:** WHO GHO, GHDx, OpenDataSUS, DATASUS TabNet, SIDRA, WPP, EM-DAT, DesInventar, SINITOX e PAHO ENLACE;
- **Repositórios científicos candidatos:** SciELO Data, Zenodo, Harvard Dataverse e re3data;
- **DATA1-B:** 16 registros prontos e 35 em revisão manual;
- **DATA1-BX:** cinco valores atuais carregados para todas as 51 fontes, com confiança `desconhecida` e todas as dimensões ainda pendentes de verificação externa;
- **Relatório de qualidade:** gerado automaticamente em `data/data_quality_report.json`;
- **Página inicial:** passa a mostrar documentação oficial, evidência revisada por pares e incertezas de acesso/licença;
- **Esquema 0.8.0:** ainda não aplicado;
- **Expansão:** bloqueada;
- **v1.0.0 e DOI:** bloqueados.

## Interpretação correta do avanço DATA1-BX

A projeção canônica reduz risco de perda e permite comparar sistematicamente as cinco dimensões. Ela não aumenta a confiança dos valores. Cada campo continua pendente até ser confrontado com documentação oficial e receber evidência, data e revisor.

Os cinco campos são:

- `data_product_types`;
- `visualization_types`;
- `data_sources`;
- `temporal_resolution`;
- `access_conditions`.

A ferramenta `scripts/load_data1bx_from_canonical.py` garante que a matriz continue correspondente ao CSV 0.7.0 enquanto a revisão externa não começa.

## Qualidade e apresentação

O build agora produz indicadores de:

- registros sustentados por documentação oficial;
- registros com evidência revisada por pares;
- fontes com incerteza em condições de acesso;
- fontes com licença variável ou ainda incerta;
- placeholders e incertezas por campo.

Esses indicadores descrevem a qualidade do catálogo; não certificam todos os produtos de cada plataforma.

## Resolução e página didática

### RES1

Registrar resolução no nível de produto, distinguindo célula raster, escala cartográfica, precisão de coordenadas, resolução temporal e limite de zoom. Não inferir resolução a partir do visualizador.

### EDU1

Criar página separada para explicar fenômenos, formas de medição, tipos de dados, limitações e fontes relacionadas.

RES1 e EDU1 permanecem não bloqueantes para v1.0.0 e DOI, salvo quando revelarem erro factual no catálogo.

## Checkpoints de reordenação

Reavaliar a ordem após:

1. DATA1-BX — projeção concluída; revisão externa ainda pendente;
2. cada lote BR1–BR5;
3. migração 0.8.0;
4. primeiros lotes DATA2;
5. testes funcionais da interface.

## Próxima execução

1. selecionar BR1 com sete fontes de maior risco científico ou maior impacto público;
2. revisar, por campo, documentação oficial e divergências entre a matriz e o CSV;
3. atualizar confiança, evidência, data, revisor e campos ainda não resolvidos;
4. manter os 18 candidatos fora do CSV até um ciclo de expansão autorizado;
5. preservar CSV 51 × 34, versão 0.7.0 e DOI bloqueado.

Consulte `QUALITY_CORRECTION_WORKFLOW.md`, `SELECTION_AND_COVERAGE_POLICY.md`, `FINAL_OBJECTIVES_AND_DOI_GATES.md`, `migration/data1bx_contract.json`, `migration/data1bx_migration_matrix.csv` e `candidates/source_candidates.csv`.
