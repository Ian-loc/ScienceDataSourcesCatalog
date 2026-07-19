# Workflow de implementação — interface, conteúdo, governança e release

## Objetivo

Melhorar a descoberta e comparação de fontes, corrigir ambiguidades documentais e preparar uma primeira versão científica estável e arquivável, sem misturar redesign, revisão científica do CSV e publicação com DOI no mesmo ciclo.

## Princípios

1. busca e decisão do usuário vêm antes da documentação institucional;
2. a página pública é atualizável; cada versão científica citável deverá ser arquivada como objeto imutável;
3. `data/data_resources.csv` é a fonte canônica;
4. JSON e metadados do site são derivados do CSV;
5. o Drive é registro histórico e changelog executivo, não fonte de publicação;
6. mudanças de interface não alteram silenciosamente o conteúdo científico;
7. nenhuma etapa é marcada como publicada sem evidência do site resultante;
8. `1.0.0` e DOI somente serão criados após fechamento técnico, científico e documental;
9. o depósito final deverá representar a contribuição principal como **Dataset**;
10. manter apenas `CITATION.cff`, salvo necessidade concreta de `.zenodo.json`;
11. licenças de código e dados devem permanecer materialmente separadas.

## Título oficial

**Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão**

O título deve ser idêntico no site, README, `CITATION.cff`, Zenodo, ORCID, currículo, Lattes e documentação técnica.

## Ciclos

| Ciclo | Escopo | Estado | Critério de conclusão |
|---|---|---|---|
| UX1 | Arquitetura, linguagem e navegação | validado e documentado | PR #5 e run 29700737238 concluídos; publicação ainda sem evidência direta |
| UX2 | Filtros e resultados | em desenvolvimento | branch implementada; falta PR, CI, integração e registro no Drive |
| UX3 | Redesenho dos cards | planejado | cards curtos, estados de acesso claros e detalhes agrupados |
| UX4 | Acessibilidade, responsividade e desempenho | planejado | teclado, contraste, mobile, carregamento e testes verificados |
| DATA1 | Correções estruturais do esquema | planejado | `resource_type`, escala geográfica controlada, formatos e citações normalizados |
| DATA2 | Revisão das 51 fontes | planejado | lotes auditáveis com evidência, diff, validação e changelog |
| RELEASE1 | Fechamento documental | validado e documentado | título, ORCID, licenças e CFF integrados no PR #5 |
| RELEASE2 | Versão estável | bloqueado | trabalho não lançado encerrado; site, CSV e metadados verificados |
| DOI | Arquivamento no Zenodo | bloqueado | release `v1.0.0` depositada como Dataset e metadados conferidos |
| POST-DOI | Propagação dos identificadores | bloqueado | DOI de versão e conceito no repositório, site, ORCID e currículos |

## UX1 — resultado

- [x] definir título oficial;
- [x] criar navegação superior consistente;
- [x] reposicionar a busca no hero;
- [x] apresentar o benefício principal antes do nome institucional;
- [x] reduzir botões concorrentes no hero;
- [x] revisar rótulos de busca e filtros;
- [x] criar atalhos de busca por temas e recursos frequentes;
- [x] criar exploração pelas áreas de pesquisa;
- [x] reduzir a altura do hero e ajustar a hierarquia tipográfica;
- [x] preservar estatísticas, filtros, cards e conteúdo científico;
- [x] validar CSV, HTML, referências locais e JavaScript no PR;
- [x] registrar o resultado no changelog do GitHub e no Drive;
- [ ] confirmar visualmente o site publicado e o commit exibido no build.

## UX2 — tarefas

- [x] separar filtros essenciais e avançados;
- [x] adicionar contagens por opção;
- [x] adicionar filtros por cobertura, formato e tipo de evidência;
- [x] mostrar filtros ativos como controles removíveis;
- [x] adicionar ordenação por relevância, nome e verificação;
- [x] representar busca, filtros e ordenação na URL;
- [x] restaurar o estado a partir da URL ao abrir a página;
- [x] indicar visualmente a área temática selecionada;
- [x] preservar o CSV canônico e os campos de busca existentes;
- [ ] validar o build e a sintaxe no pull request;
- [ ] integrar após CI aprovado;
- [ ] registrar o resultado no Drive;
- [ ] confirmar visualmente a publicação.

## RELEASE1 — resultado

- [x] preservar `type: dataset`;
- [x] incluir ORCID `0000-0003-1164-9318` no `CITATION.cff`;
- [x] manter `version: "0.7.0"` até a release estável;
- [x] manter a data efetiva da versão e usar aspas no YAML;
- [x] criar `LICENSE-DATA.md` para CSV, metadados e curadoria;
- [x] esclarecer no README o escopo de MIT e CC BY 4.0;
- [x] não criar `.zenodo.json` sem necessidade comprovada;
- [x] documentar que o DOI pode ser inserido no repositório ativo após o primeiro arquivamento.

## Condições obrigatórias para `v1.0.0`

1. encerrar os blocos não lançados no changelog;
2. validar CSV e artefatos derivados;
3. verificar o site e o commit exibido no build;
4. concluir UX1–UX4 ou registrar explicitamente o que ficará para versões posteriores;
5. concluir DATA1 e a revisão mínima das 51 fontes;
6. validar título, autor, ORCID, licenças, versão e data;
7. alterar `CITATION.cff` para `version: "1.0.0"` somente no dia da release;
8. criar tag e GitHub Release `v1.0.0`;
9. testar se GitHub–Zenodo preserva o tipo Dataset;
10. se necessário, realizar depósito manual classificado como Dataset;
11. conferir arquivos, autor, título, licença, tipo e versão antes da publicação;
12. inserir DOI de versão e DOI de conceito no repositório ativo após a atribuição.

## Citação planejada

Versão específica:

> LARA, Ian. *Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Versão 1.0.0. Zenodo, 2026. DOI: [DOI da versão].

Projeto geral:

> LARA, Ian. *Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Zenodo, 2026. Concept DOI: [DOI de conceito].

## Ordem operacional atual

1. validar e integrar UX2;
2. registrar UX2 no Drive e confirmar a publicação quando houver evidência;
3. executar UX3 e UX4;
4. executar DATA1 e DATA2;
5. fechar documentação e publicação;
6. somente então criar `v1.0.0` e o depósito no Zenodo.
