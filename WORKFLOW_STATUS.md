# Estado do workflow

## Regra operacional

Uma tarefa só é considerada concluída quando estiver implementada em branch, revisada em pull request, integrada à `main`, validada pelo GitHub Actions e registrada no changelog. Quando afetar o site, a publicação também precisa ser confirmada.

CI verde comprova estrutura e coerência interna. Não comprova, sozinho, que uma fonte externa esteja atual, acessível ou cientificamente correta.

## Limitações atuais

- a publicação só será marcada como confirmada mediante inspeção direta do site ou evidência equivalente;
- a revisão factual exige documentação oficial atual;
- o acesso web de pesquisa não está disponível neste ambiente;
- novas fontes permanecem fora do CSV até a estabilização das 51 atuais;
- candidatos permanecem em triagem, sem decisão final;
- auditoria interna e seleção de lotes não autorizam elevar confiança nem corrigir o CSV sem evidência externa atual;
- URLs iguais em `homepage_url` e `data_access_url` são pendências, não confirmação de que o mesmo destino é adequado aos dois botões.

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
| DATA1-BR/BR1 | Plataformas e monitoramento de alto impacto | auditoria interna concluída; revisão externa bloqueada | sete fontes; contrato e matriz validados |
| DATA1-BR/BR2 | Biodiversidade, ciência cidadã e redes | auditoria interna concluída; revisão externa bloqueada | sete fontes; contrato e matriz validados |
| DATA1-BR/BR3 | Clima, repositórios e redes de fluxos | auditoria interna concluída; revisão externa bloqueada | sete fontes; contrato e matriz integrados ao registro comum |
| DATA1-BR/BR4 | Sistemas territoriais e climáticos brasileiros | auditoria interna concluída; revisão externa bloqueada | sete fontes; papéis dos links incluídos como dimensão obrigatória |
| DATA1-BR/BR5 | Revisar 7 casos restantes | planejado | lote final com os mesmos controles de evidência e URLs |
| DATA1-C | Migração atômica para 38 campos | bloqueado | decisões DATA1-B e DATA1-BX revisadas |
| DATA1-D | Validação semântica do esquema final | planejado | 14 regras ativas no CSV 0.8.0 |
| DATA2 | Revisar as 51 fontes no esquema final | planejado | links, acesso, formatos, licença, evidência e data revisados |
| UX5 | Interface dos 38 campos e testes de navegador | em desenvolvimento parcial | resumo público de qualidade e indicador dos papéis dos links; adaptação aos 38 campos ainda pendente |
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
- **DATA1-B:** 16 registros prontos e 35 em revisão manual;
- **DATA1-BX:** cinco dimensões carregadas para 51 fontes, com confiança `desconhecida`;
- **Lotes ativos:** BR1–BR4, totalizando 28 fontes sem sobreposição;
- **Casos manuais ainda não distribuídos:** 7;
- **Revisões externas BR1–BR4:** bloqueadas enquanto não houver documentação oficial atual acessível;
- **Papéis dos links:** regra documentada, auditoria automática integrada ao build e dimensão obrigatória no BR4;
- **Relatório de qualidade:** gerado automaticamente durante o build;
- **Página inicial:** mostra documentação oficial, evidência revisada por pares, incertezas de acesso/licença e URLs iguais pendentes;
- **Esquema 0.8.0:** ainda não aplicado;
- **Expansão:** bloqueada;
- **v1.0.0 e DOI:** bloqueados.

## BR1 — achados principais

Fontes: CEMADEN, dados.gov.br, MapBiomas, TerraBrasilis, BDQueimadas, Google Earth Engine e Global Forest Watch.

Riscos dominantes: agregadores tratados como produtores; atributos generalizados entre produtos; mistura de protocolos, ferramentas e formatos; resolução e temporalidade uniformizadas; confusão entre alertas, focos, incêndios, áreas queimadas e desmatamento.

## BR2 — achados principais

Fontes: speciesLink, SiBBr, eBird, Movebank, DataONE, iNaturalist e TRY.

Riscos dominantes: duplicação entre redes; agregador confundido com fonte primária; licença por coleção, observação, mídia, estudo ou dataset; coordenadas sensíveis; viés amostral; dados brutos versus produtos modelados; acesso por solicitação ou termos específicos.

## BR3 — achados principais

Fontes: Copernicus Climate Data Store, WorldClim, NEON, PANGAEA, Climate Data Guide, AmeriFlux e FLUXNET.

Riscos dominantes:

- versão, coleção, produto e cenário tratados de forma genérica;
- observações, reanálises, modelos e produtos derivados misturados;
- resolução nominal confundida com suporte ou precisão;
- dados provisórios, revisados ou reprocessados sem distinção;
- licença, período e processamento definidos no nível do dataset ou sítio;
- área de influência das torres tratada como geometria fixa;
- duplicação de sítios entre AmeriFlux e coleções FLUXNET;
- catálogo ou guia confundido com provedor original.

## BR4 — achados principais

Fontes: Clima Gerais, IDE-SISEMA, AdaptaBrasil, SIRENE, PANORAMA/CENSIPAM, UrbVerde e BDiA.

Riscos dominantes:

- indicadores compostos confundidos com observações ou medições diretas;
- datas de atualização atribuídas à plataforma em vez do produto, camada ou módulo;
- visualizador tratado como prova de download, formato ou protocolo;
- resolução visual confundida com escala cartográfica, precisão ou suporte espacial;
- serviços OGC e acesso programático declarados sem documentação técnica associada;
- licenças e fontes generalizadas entre camadas e levantamentos;
- homepage, página operacional e acesso aos dados sem papéis demonstrados separadamente.

SIRENE, UrbVerde e BDiA usam atualmente o mesmo destino nos dois botões. O PANORAMA usa `/` e `/home`, mas essa diferença superficial não comprova separação entre página institucional e aplicação de dados.

As 28 fontes são internamente coerentes com ressalvas, mas não estão prontas para migração. A decisão permanece manter o CSV 0.7.0 até confronto com documentação oficial atual, URL de evidência, data e revisor.

## Controle dos lotes

`migration/br_batch_registry.json` controla ordem, contratos e matrizes. `scripts/validate_br_batches.py` verifica:

- sete fontes por lote;
- IDs exclusivos entre lotes;
- correspondência com CSV, DATA1-B e DATA1-BX;
- estado `revisão_manual` na DATA1-B;
- confiança `desconhecida` na DATA1-BX;
- URLs existentes idênticas ao CSV;
- bloqueio de evidência, revisor, data e correções enquanto não houver revisão externa.

A projeção DATA1-BX reduz risco de perda, mas não aumenta confiança.

## Papéis dos links

A regra operacional é:

- **Site oficial** (`homepage_url`): página institucional principal, página “Sobre” ou página oficial do órgão responsável;
- **Acessar dados** (`data_access_url`): catálogo, busca, visualizador, formulário de solicitação ou página de download;
- **Documentação de acesso** (`access_documentation_url`): instruções técnicas de API, protocolos ou credenciais.

`scripts/audit_link_roles.py` gera `data/link_role_audit.json`, identifica URLs iguais e incorpora o total aos indicadores públicos de qualidade. URLs iguais permanecem pendentes até inspeção oficial; nenhuma substituição será inferida.

A diferença entre dois caminhos também não comprova papéis distintos. A revisão precisa demonstrar a função de cada destino no nível da fonte e do produto.

## Qualidade e apresentação

O build produz indicadores de documentação oficial, evidência revisada por pares, incerteza de acesso, licença variável, papéis dos links e placeholders por campo. Esses indicadores descrevem a qualidade do catálogo; não certificam todos os produtos de cada plataforma.

## Resolução e página didática

### RES1

Registrar resolução no nível de produto, distinguindo célula raster, escala cartográfica, precisão de coordenadas, resolução temporal e limite de zoom. Não inferir resolução a partir do visualizador.

### EDU1

Criar página separada para explicar fenômenos, formas de medição, tipos de dados, limitações e fontes relacionadas.

RES1 e EDU1 permanecem não bloqueantes para v1.0.0 e DOI, salvo quando revelarem erro factual no catálogo.

## Checkpoints de reordenação

Reavaliar a ordem após:

1. BR1–BR4 — auditorias internas concluídas; revisões externas bloqueadas;
2. BR5;
3. migração 0.8.0;
4. primeiros lotes DATA2;
5. testes funcionais da interface.

## Próxima execução

1. executar revisão externa de BR1–BR4 quando houver acesso atual à documentação oficial;
2. enquanto esse acesso não estiver disponível, registrar BR5 com os sete casos manuais restantes;
3. incluir a separação entre `homepage_url` e `data_access_url` na revisão de cada fonte;
4. não alterar confiança, evidência, data ou CSV com base em inferência;
5. manter os 18 candidatos fora do CSV;
6. preservar CSV 51 × 34, versão 0.7.0, esquema 0.8.0 não aplicado e DOI bloqueado.

Consulte `migration/br_batch_registry.json`, os contratos e matrizes BR1–BR4, `migration/data1bx_contract.json`, `migration/data1bx_migration_matrix.csv`, `METHODOLOGY.md`, `CODEBOOK.md`, `QUALITY_CORRECTION_WORKFLOW.md`, `SELECTION_AND_COVERAGE_POLICY.md` e `FINAL_OBJECTIVES_AND_DOI_GATES.md`.
