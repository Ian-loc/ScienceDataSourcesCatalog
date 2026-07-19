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
| UX3 | Redesenho dos cards | validado e documentado | PR #9 e run 29701341054 concluídos |
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

- [x] filtros essenciais e avançados com contagens;
- [x] filtros ativos, ordenação e URL compartilhável;
- [x] PR #7 e run `29701061221` concluídos;
- [x] CSV preservado e Drive atualizado;
- [ ] confirmar visualmente a publicação.

## UX3 — resultado

- [x] identidade oficial em linha secundária;
- [x] descrição, sigla e verificação mais escaneáveis;
- [x] estados semânticos para download, API e Brasil;
- [x] utilidade acadêmica e limitação em destaque;
- [x] ação `Acessar dados` priorizada;
- [x] seis grupos técnicos implementados;
- [x] todos os campos e links preservados;
- [x] CI exige referência aos 34 campos;
- [x] PR #9 e run `29701341054` concluídos;
- [x] commit `eec289ee5036848fa836c43e7dcd088b47da3710` integrado;
- [x] Drive atualizado;
- [ ] confirmar visualmente a publicação.

## UX4 — tarefas planejadas

- [ ] testar navegação integral por teclado;
- [ ] revisar ordem de foco, nomes acessíveis e estados expandidos;
- [ ] validar contraste e uso de cor não exclusivo;
- [ ] revisar layouts em larguras móveis e intermediárias;
- [ ] evitar animação quando `prefers-reduced-motion` estiver ativo;
- [ ] adicionar fallback informativo quando JavaScript estiver indisponível;
- [ ] verificar peso dos arquivos e ausência de dependências desnecessárias;
- [ ] ampliar testes automáticos de acessibilidade estrutural;
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

1. executar UX4;
2. executar DATA1 e DATA2;
3. confirmar publicação e fechar documentação;
4. somente então criar `v1.0.0` e o depósito no Zenodo.
