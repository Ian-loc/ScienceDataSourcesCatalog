# Estado canônico e disposição dos artefatos

**Projeto:** Simbiotrama — Catálogo de Dados Científicos do Brasil  
**Data de referência:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Estado global:** Marco 1 incorporado; simplificação governada da Instância 1 em execução.

Este documento é o índice normativo para prioridade, autoridade e ciclo de vida. Deve ser lido junto da política de escopo, do contrato da Instância 1, do roadmap e da governança.

## 1. Hierarquia de autoridade

1. `main` do repositório;
2. decisões e políticas incorporadas;
3. esquema, migrações e validadores executáveis;
4. dados públicos canônicos durante a transição;
5. evidências e revisões curatoriais;
6. auditorias, branches, protótipos e relatórios históricos.

Conversas, relatórios de sessão, literatura, reflexões de outros ambientes e branches não incorporadas são insumos. Não são autoridade arquitetural.

## 2. Direção ativa

A Instância 1 é um **catálogo relacional de fontes e ofertas de dados científicos**. Sua unidade central é uma entrada de catálogo de granularidade mínima suficiente.

O projeto deve permitir que o usuário:

- descubra uma fonte ou oferta de dados;
- compreenda, em nível suficiente, o que ela oferece;
- identifique temas, variáveis, cobertura e modalidade de dados;
- encontre os links oficiais para metadados, método, acesso, licença e citação;
- reconheça se existe candidato a conector para visualização futura.

O projeto não deve reconstruir catálogos externos, enumerar integralmente arquivos ou layers, armazenar datasets de terceiros nem exigir genealogia completa de produtos.

## 3. Classificação de ciclo de vida

### `ACTIVE`

- simplificação e alinhamento documental da Instância 1;
- núcleo mínimo: organizações, entradas, variáveis, evidências e conectores opcionais;
- staging sem perda e migração idempotente;
- curadoria proporcional por entrada;
- website dinâmico sustentado por campos essenciais;
- validação do modelo com GEDI, DETER Cerrado, IBGE e ANA/SNIRH;
- preservação da página e dos CSV/JSON públicos durante a transição.

### `BACKLOG`

- Instância 2 — visualização federada por APIs e conectores externos;
- Instância 3 — literatura científica curada;
- receitas e produtos derivados;
- harmonização, ontologias, estimands e linhagens de transformação;
- inventários detalhados de arquivos e serviços;
- perfis analíticos avançados de escala, qualidade e compatibilidade;
- API pública após estabilização do catálogo.

### `LEGACY_OPERATIONAL`

- `explorer.html`;
- `data/federated_layers.json`;
- composição visual N0 atualmente publicada;
- interface estática baseada nos CSV/JSON atuais.

Esses artefatos recebem apenas correções de segurança, disponibilidade e regressão até ativação formal da Instância 2.

### `RETIRED` ou `SUPERSEDED`

Não devem orientar desenvolvimento novo:

- classes universais de compatibilidade;
- Fase 1 do Simbioscópio;
- registros paralelos do PR #53;
- obrigação universal de separar família, produto, release, distribuição e ativo;
- curadoria forense integral por produto;
- inventário de bytes, checksums, schemas e endpoints como rotina da Instância 1;
- `data_assets` como entidade necessária do catálogo;
- número de claims, assets, releases ou validadores como métrica principal.

### `HISTORICAL_EVIDENCE`

- `docs/audits/`;
- registros de ocorrências;
- PRs e commits encerrados;
- snapshots, matrizes e protótipos;
- reflexões anteriores que defendiam a arquitetura profunda;
- resultados de CI e documentação de transição.

Esses materiais devem ser preservados, mas não tratados como instrução ativa.

## 4. Documentos canônicos

- `README.md` — entrada pública;
- `docs/PROJECT_STATE.md` — autoridade e ciclo de vida;
- `docs/policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md` — limites e gate de expansão;
- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md` — contrato funcional da Instância 1;
- `docs/decisions/DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md` — decisão de simplificação;
- `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md` — sequência global;
- `docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md` — workflow por entrada;
- `docs/GOVERNANCE.md` — gates e autoridade.

## 5. Pacote ativo

> **I1-S1 — simplificação governada da Instância 1.**

Entregas:

1. formalizar granularidade mínima suficiente;
2. substituir completude por produto/release por completude de ficha essencial;
3. revisar arquitetura e plano de migração sem perda;
4. congelar o PR #57 e classificá-lo como candidato a `superseded`;
5. validar o modelo com quatro casos heterogêneos;
6. preparar o próximo delta executável do esquema e das exportações.

O PR #57 permanece aberto apenas como evidência e pacote congelado até decisão humana explícita sobre seu encerramento. Sua autorização de merge anterior não é reutilizável.

## 6. Gate de sanidade contínua

Antes de criar tabela, coluna, entidade, validador ou requisito, verificar:

1. atende descoberta, interpretação mínima, filtro do website ou conector selecionado;
2. não reconstrói informação que já pertence à fonte externa;
3. não cria uma entrada apenas por arquivo, layer, banda ou endpoint;
4. não transforma ausência de informação em inferência;
5. possui critério de parada proporcional;
6. pode ser testado com entradas heterogêneas;
7. não antecipa Instâncias 2 ou 3;
8. mantém o PR pequeno e revisável;
9. preserva rastreabilidade sem produzir pacote forense desnecessário;
10. melhora utilidade pública de forma demonstrável.
