# Estado canônico e disposição dos artefatos

**Projeto:** Simbiotrama  
**Data de referência:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Estado global:** Marco 1 incorporado; Instância 1 ativa; curadoria científica em expansão.

Este documento é o índice normativo para distinguir trabalho ativo, backlog, legado operacional, material retirado e evidência histórica. Em caso de dúvida sobre prioridade ou validade operacional, ele deve ser lido junto da direção científica, da decisão da Instância 1 e da governança.

## 1. Hierarquia de autoridade

1. `main` do repositório;
2. direção científica e decisões aprovadas;
3. esquema relacional, migrações e validadores executáveis;
4. dados públicos canônicos durante a transição;
5. evidências, auditorias e revisões curatoriais;
6. espelhos, protótipos e documentos históricos.

Durante a transição:

- `data/data_resources.csv`, `data/data_products.csv` e `data/product_distributions.csv` sustentam a versão pública atual;
- PostgreSQL/PostGIS é a arquitetura canônica de destino, ainda não a autoridade de produção;
- planilhas do Drive são snapshots ou espelhos derivados;
- conversas, relatórios de sessão e branches não incorporadas não são autoridade.

## 2. Classificação de ciclo de vida

### `ACTIVE`

Trabalho autorizado e pertencente ao caminho crítico atual:

- Instância 1 — catálogo relacional científico-operacional;
- esquema PostgreSQL/PostGIS, staging e promoções seletivas;
- curadoria integral por produto e release;
- variáveis, métodos, perfis espaciais, temporais e de qualidade no modelo relacional;
- distribuições, ativos, endpoints e capacidades de acesso;
- licenças, citações, evidências por afirmação e revisões curatoriais;
- gates científicos e operacionais;
- revisão seletiva das 51 fontes legadas;
- página pública e CSV/JSON atuais somente como autoridade pública transitória.

### `BACKLOG`

Direções preservadas, mas sem implementação ativa:

- Instância 2 — composição e visualização federada;
- Instância 3 — literatura científica curada;
- receitas analíticas e produtos derivados;
- sinalizadores contextuais avançados;
- contratos de passaporte de variável, avaliação de relações e evidência científica;
- níveis N0–N5 como linguagem conceitual futura;
- casos adversariais ou dourados para operações entre produtos;
- API pública e nova interface relacional após maturidade do banco.

Os contratos em `schema/scientific-variable-passport-v0.1.json`, `schema/comparability-assessment-v0.1.json` e `schema/scientific-relation-evidence-v0.1.json` permanecem preservados como backlog de desenho. Não constituem modelos ativos nem autorizam registros paralelos aos dados relacionais.

### `LEGACY_OPERATIONAL`

Artefatos ainda funcionais, preservados apenas para continuidade pública e regressão:

- `explorer.html`;
- `data/federated_layers.json`;
- composição visual N0 atualmente publicada;
- interface estática baseada nos CSV/JSON simplificados.

Esses artefatos podem receber apenas correções de segurança, disponibilidade ou regressão. Não devem receber novas capacidades analíticas, ontologias de compatibilidade ou expansão funcional antes da ativação formal da Instância 2.

### `RETIRED` ou `SUPERSEDED`

Não devem orientar desenvolvimento novo:

- “Fase 1 do Simbioscópio” como workstream ativo;
- classes A–E como julgamento universal de compatibilidade científica;
- registros paralelos de variáveis e passaportes propostos no PR #53;
- uso de família de produtos não resolvida como entrada analítica;
- branch `agent/consolidate-instance-1-relational-catalog` após o merge do PR #54;
- branch `agent/simbioscope-phase1-variable-registry` e PR #53;
- o nome `Symbiotrama` como variante ativa;
- `Simbioscópio` como nome do projeto ou de uma fase em execução.

Conceitos úteis desses artefatos podem ser reimplementados seletivamente, com nova evidência e aderência ao modelo relacional. Não se deve fazer cherry-pick integral de estruturas aposentadas.

### `HISTORICAL_EVIDENCE`

Deve ser preservado, mas não tratado como instrução ativa:

- `docs/audits/`;
- registros de ocorrências;
- PRs e commits encerrados;
- propostas de correção ainda não promovidas;
- snapshots e matrizes de migração;
- documentação de transição e resultados de CI.

Evidência histórica não deve ser apagada para “limpar” o repositório. A limpeza deve reduzir duplicação normativa e ambiguidade, não remover rastreabilidade.

## 3. Documentos canônicos ativos

- `README.md` — entrada pública do repositório;
- `docs/PROJECT_STATE.md` — estado e ciclo de vida;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md` — missão e princípios;
- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md` — contrato científico da Instância 1;
- `docs/decisions/DEC-INSTANCE1-RELATIONAL-CORE.md` — decisão arquitetural;
- `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md` — sequência global;
- `docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md` — workflow por produto;
- `docs/GOVERNANCE.md` — autoridade, gates e papéis;
- `docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md` — guardrail futuro, sem workstream ativo;
- `docs/milestones/` — somente registros consolidados e política de pacotes.

## 4. Pacote ativo e sequência

A limpeza `sanity()` pós-Marco 1 precede novo aprofundamento científico.

Após sua incorporação, o próximo pacote é:

> **Marco 2A — fechamento científico-operacional do DETER Cerrado.**

O Marco 2A deve partir da `main` atualizada e permanecer limitado ao DETER Cerrado. DETER Amazônia, DETER Pantanal, PRODES, Clima Gerais, MapBiomas e mudanças transversais independentes não pertencem ao mesmo PR.

## 5. Critério de sanidade contínua

Antes de iniciar ou ampliar um pacote, verificar:

1. existe uma única autoridade para a decisão em questão;
2. o artefato está classificado no ciclo de vida correto;
3. o pacote pertence ao foco ativo;
4. não existe branch ou PR anterior que já foi substituído;
5. não há duplicação entre documento normativo, checkpoint e log transitório;
6. o trabalho preserva evidência e proveniência;
7. a expansão não antecipa Instâncias 2 ou 3;
8. o PR pode ser revisado como unidade coerente;
9. o critério de completude está explícito;
10. o CI e a revisão científica são proporcionais ao risco.
