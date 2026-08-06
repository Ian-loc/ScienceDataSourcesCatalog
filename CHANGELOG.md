# Histórico de mudanças

Este projeto segue versionamento semântico. Alterações ainda não publicadas são agrupadas em uma única seção; detalhes operacionais permanecem rastreáveis no histórico de commits, pull requests e auditorias arquivadas.

## Não lançado

### Sanity pós-Marco 1

- nome canônico padronizado como **Simbiotrama**;
- criado `docs/PROJECT_STATE.md` para classificar `ACTIVE`, `BACKLOG`, `LEGACY_OPERATIONAL`, `RETIRED` e `HISTORICAL_EVIDENCE`;
- criado roadmap canônico `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md`;
- caminho antigo do roadmap do Simbioscópio convertido em alias aposentado para preservar links históricos;
- governança, direção científica, decisão arquitetural e README alinhados ao estado pós-Marco 1;
- PR #53 fechado como `superseded`, sem incorporação de registros paralelos ou classes universais de compatibilidade;
- documentação de marcos reduzida ao registro consolidado, política de pacotes, índice e estado legível por máquina;
- explorador visual N0 e `data/federated_layers.json` classificados como legado operacional sem desenvolvimento analítico ativo;
- validador científico ampliado para testar autoridade, ciclo de vida, roadmap, nomenclatura e preservação do legado N0.

### Adicionado — Instância 1

- decisão estratégica que estabelece a **Instância 1 — Catálogo relacional científico-operacional** como foco ativo;
- documentação canônica da Instância 1;
- modelo PostgreSQL/PostGIS para organizações, fontes, famílias, produtos, releases, variáveis, métodos, perfis espaciais e temporais, qualidade, distribuições, ativos, capacidades, taxonomias, citações, evidências e revisões;
- schema de staging para migração sem perda dos CSVs atuais;
- registro de problemas e bloqueios de migração;
- workflow contínuo de curadoria produto por produto;
- portões de migração, aprofundamento, interface e promoção do banco;
- definição de `information_message` para explicar qual informação sobre o mundo real o produto comunica;
- definição de `non_representations` para registrar interpretações que o produto não sustenta;
- evidência de metadados por entidade e campo.

### Alterado — direção do projeto

- projeto recentrado no aprofundamento do catálogo, antes de novas capacidades analíticas;
- PostgreSQL/PostGIS definido como arquitetura canônica de destino;
- CSVs mantidos como autoridade pública durante a transição e futura exportação do banco;
- separação normativa reforçada entre organização, fonte, família, produto, release, distribuição, ativo e variável;
- catálogos genéricos, serviços de processamento e visualizadores deixam de ser tratados como produtos científicos;
- README, direção científica, roadmap, modelo de produtos e dicionário de dados harmonizados com a Instância 1;
- Instâncias 2 e 3 registradas somente como backlog;
- política de comparabilidade e inferência mantida como guardrail futuro, sem workstream analítico ativo.

### Preservado do desenvolvimento anterior

- camada pública atual de fontes, produtos e distribuições;
- Explorador Federado como protótipo N0 e legado operacional, sem promoção a núcleo consolidado;
- classificação territorial Brasil-primeiro;
- Dynamic World V1 como produto piloto selecionado;
- contratos experimentais de variáveis, comparabilidade e relações, mantidos em backlog sem promoção automática ao modelo canônico;
- validações, governança, contribuição e política de releases;
- separação de autoria, citação, licença e proveniência.

### Corrigido

- mistura entre produtos científicos, catálogos, serviços interoperáveis e infraestrutura computacional;
- roadmap excessivamente orientado a comparabilidade, causalidade e visualização antes da consolidação dos dados;
- ausência de releases explícitos entre produto e distribuição;
- ausência de estrutura relacional para evidência por campo e revisão curatorial;
- falta de distinção entre descrição do produto, mensagem científica e usos potenciais;
- falta de estratégia executável de migração dos CSVs;
- duplicação normativa entre checkpoints, notas, autorizações e ponteiros transitórios de execução.

## 0.7.0 — 2026-07-18

- consolidado `data/data_resources.csv` como fonte canônica;
- ampliado o esquema para 34 campos;
- revisadas 51 fontes de dados;
- incorporadas evidências acadêmicas, técnicas e oficiais representativas;
- condensados temas em nove áreas de pesquisa;
- separados download, acesso programático, protocolos e autenticação;
- adicionadas páginas de catálogo, análise, método e citação;
- adicionados metodologia, codebook, licenças separadas e `CITATION.cff`.

## 0.6.0 — 2026-07-18

- definida a autoridade do CSV no GitHub;
- ampliado o esquema de 22 para 26 campos;
- revisadas identidade, utilidade, limitações, links e condições de acesso;
- adicionadas validação automática e geração do JSON público.
