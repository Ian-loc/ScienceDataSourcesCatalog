# Histórico de mudanças

Este projeto segue versionamento semântico. Alterações ainda não publicadas são agrupadas em uma única seção; detalhes operacionais permanecem rastreáveis no histórico de commits, pull requests e auditorias arquivadas.

## Não lançado

### Simplificação governada da Instância 1

- `catalog_entry` definido como unidade central de granularidade mínima suficiente;
- núcleo-alvo simplificado para `organizations`, `catalog_entries`, `entry_variables`, `entry_evidence` e `connector_profiles` opcional;
- removida a obrigação universal de decompor fontes em família, produto, release, distribuição e ativo;
- releases, arquivos, layers, bandas, endpoints, bytes, checksums e schemas deixam de ser requisitos normais de completude;
- criada política explícita contra cópia de dados, reconstrução de catálogos externos e proliferação de entidades;
- workflow de curadoria redefinido por ficha essencial e critério de parada;
- evidência passa a ser proporcional aos campos materiais, sem pacote forense por entrada;
- métricas passam a priorizar entradas prontas para o website, campos essenciais, links e variáveis principais;
- criado plano de migração aditiva, idempotente, reversível e sem perda do modelo profundo incorporado;
- GEDI, DETER Cerrado, IBGE e ANA/SNIRH definidos como casos de validação heterogêneos;
- decisão profunda anterior classificada como `SUPERSEDED`, preservada como legado técnico;
- PR #57 congelado, devolvido a draft e classificado como candidato a `superseded`;
- criado template de PR com gate de escopo, critério de parada e revisão completa antes da autorização de merge;
- validador de direção atualizado para impedir regressões ao regime de curadoria integral por produto/release;
- tarefa recorrente atualizada para executar exclusivamente a Instância 1 mínima.

### Ocorrência operacional

- um arquivo provisório foi criado acidentalmente na `main` durante a inicialização da branch de simplificação;
- o arquivo foi removido imediatamente no commit seguinte e nenhum conteúdo provisório permanece na árvore;
- a ocorrência permanece registrada no histórico e no PR para transparência;
- o processo foi corrigido para exigir criação e confirmação da branch antes de qualquer escrita.

### Sanity pós-Marco 1

- nome canônico padronizado como **Simbiotrama**;
- criado `docs/PROJECT_STATE.md` para classificar `ACTIVE`, `BACKLOG`, `LEGACY_OPERATIONAL`, `RETIRED` e `HISTORICAL_EVIDENCE`;
- criado roadmap canônico `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md`;
- caminho antigo do roadmap do Simbioscópio convertido em alias aposentado para preservar links históricos;
- governança, direção científica, decisão arquitetural e README alinhados ao estado pós-Marco 1;
- PR #53 fechado como `superseded`;
- documentação de marcos reduzida ao registro consolidado, política de pacotes, índice e estado legível por máquina;
- explorador visual N0 e `data/federated_layers.json` classificados como legado operacional;
- validador científico ampliado para testar autoridade, ciclo de vida e preservação do legado N0.

### Marco 1 — arquitetura profunda incorporada

- decisão estratégica original da Instância 1;
- documentação do núcleo relacional profundo;
- modelo PostgreSQL/PostGIS para organizações, fontes, famílias, produtos, releases, variáveis, métodos, perfis, distribuições, ativos, capacidades, citações, evidências e revisões;
- schema de staging para migração sem perda dos CSVs atuais;
- carga e promoção idempotentes;
- resolução inicial de entidades;
- evidência por campo e revisão curatorial;
- separação entre produtos científicos, catálogos, serviços e infraestrutura.

Esse marco permanece tecnicamente válido e preservado, mas sua granularidade deixou de ser obrigatória após a decisão de simplificação.

### Preservado

- camada pública atual de fontes, produtos e distribuições;
- Explorador Federado como protótipo N0 e legado operacional;
- classificação territorial Brasil-primeiro;
- staging, hashes, integridade e idempotência;
- contratos experimentais de variáveis, comparabilidade e relações como backlog;
- governança, contribuição, releases, autoria, citação, licença e proveniência.

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
