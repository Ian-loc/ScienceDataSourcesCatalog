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

## Ciclos

| Ciclo | Escopo | Estado | Critério de conclusão |
|---|---|---|---|
| UX1 | Arquitetura, linguagem e navegação | validado e documentado | PR #5 e run 29700737238 concluídos |
| UX2 | Filtros e resultados | validado e documentado | PR #7 e run 29701061221 concluídos |
| UX3 | Redesenho dos cards | planejado | cards curtos, estados de acesso claros e detalhes agrupados |
| UX4 | Acessibilidade, responsividade e desempenho | planejado | teclado, contraste, mobile, carregamento e testes verificados |
| DATA1 | Correções estruturais do esquema | planejado | `resource_type`, escala geográfica controlada, formatos e citações normalizados |
| DATA2 | Revisão das 51 fontes | planejado | lotes auditáveis com evidência, diff, validação e changelog |
| RELEASE1 | Fechamento documental | validado e documentado | título, ORCID, licenças e CFF integrados no PR #5 |
| RELEASE2 | Versão estável | bloqueado | trabalho não lançado encerrado; site, CSV e metadados verificados |
| DOI | Arquivamento no Zenodo | bloqueado | release `v1.0.0` depositada como Dataset e metadados conferidos |
| POST-DOI | Propagação dos identificadores | bloqueado | DOI de versão e conceito no repositório, site, ORCID e currículos |

## UX1 — resultado

- [x] busca no hero e navegação consistente;
- [x] benefício principal, atalhos e exploração por áreas;
- [x] linguagem, hierarquia e documentação revisadas;
- [x] CSV, HTML, referências locais e JavaScript validados;
- [x] GitHub e Drive atualizados;
- [ ] confirmar visualmente o site e o commit exibido no build.

## UX2 — resultado

- [x] separar filtros essenciais e avançados;
- [x] adicionar contagens por opção;
- [x] filtrar por cobertura, formato e tipo de evidência;
- [x] mostrar filtros ativos removíveis;
- [x] ordenar por relevância, nome e verificação;
- [x] representar e restaurar estado pela URL;
- [x] destacar a área selecionada;
- [x] preservar o CSV e os campos de busca;
- [x] validar o PR no run `29701061221`;
- [x] integrar no commit `a212192174c354508eaf48dea30a81faa5311ae5`;
- [x] registrar no Drive;
- [ ] confirmar visualmente a publicação.

## UX3 — tarefas planejadas

- [ ] mover a identidade oficial para uma linha secundária;
- [ ] tornar a descrição mais escaneável;
- [ ] apresentar estados de download, API e Brasil com texto semântico;
- [ ] destacar utilidade acadêmica e principal limitação;
- [ ] priorizar a ação `Acessar dados`;
- [ ] agrupar detalhes em Acesso, Cobertura, Produtos, Uso acadêmico, Evidências e Avaliação;
- [ ] manter todos os campos e links disponíveis;
- [ ] validar estrutura, sintaxe e integridade do CSV;
- [ ] registrar GitHub e Drive.

## RELEASE1 — resultado

- [x] `type: dataset`, ORCID, versão e data adequados;
- [x] `LICENSE-DATA.md` e separação de licenças;
- [x] ausência deliberada de `.zenodo.json`;
- [x] política de inserção posterior do DOI documentada.

## Condições obrigatórias para `v1.0.0`

1. encerrar os blocos não lançados no changelog;
2. validar CSV e artefatos derivados;
3. verificar o site e o commit exibido no build;
4. concluir UX1–UX4 ou registrar o que ficará para versões posteriores;
5. concluir DATA1 e a revisão mínima das 51 fontes;
6. validar título, autor, ORCID, licenças, versão e data;
7. alterar `CITATION.cff` para `version: "1.0.0"` somente no dia da release;
8. criar tag e GitHub Release `v1.0.0`;
9. testar se GitHub–Zenodo preserva o tipo Dataset;
10. se necessário, realizar depósito manual classificado como Dataset;
11. conferir arquivos e metadados antes da publicação;
12. inserir DOI de versão e DOI de conceito no repositório ativo.

## Citação planejada

> LARA, Ian. *Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Versão 1.0.0. Zenodo, 2026. DOI: [DOI da versão].

## Ordem operacional atual

1. executar UX3;
2. executar UX4;
3. executar DATA1 e DATA2;
4. confirmar publicação e fechar documentação;
5. somente então criar `v1.0.0` e o depósito no Zenodo.
