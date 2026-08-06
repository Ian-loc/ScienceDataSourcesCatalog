# Governança do Simbiotrama

## 1. Finalidade

O Simbiotrama é um catálogo relacional científico-operacional de produtos de dados georreferenciados sobre o Brasil. Sua fase ativa é a **Instância 1**, dedicada a identificar, definir, versionar, documentar, verificar e tornar acessíveis produtos de dados com rigor científico e operacional.

Composição geográfica e contextualização por literatura permanecem como Instâncias 2 e 3 em backlog. Elas não constituem workstreams ativos.

## 2. Autoridade

A hierarquia vigente é:

1. branch `main`;
2. `docs/PROJECT_STATE.md`;
3. `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
4. decisões aprovadas em `docs/decisions/`;
5. esquema relacional, migrações e validadores executáveis;
6. dados públicos canônicos durante a transição;
7. evidências, auditorias e revisões curatoriais;
8. protótipos, espelhos e documentos históricos.

Durante a transição:

- `data/data_resources.csv`, `data/data_products.csv` e `data/product_distributions.csv` sustentam a versão pública;
- PostgreSQL/PostGIS é a arquitetura canônica de destino, mas ainda não a autoridade de produção;
- planilhas do Google Drive são snapshots ou espelhos derivados;
- branches não incorporadas, conversas e relatórios de sessão não constituem autoridade.

Em caso de divergência, a `main` e os documentos normativos vigentes prevalecem.

## 3. Ciclo de vida dos artefatos

Todo artefato deve ser classificado como:

- `ACTIVE` — pertence ao caminho crítico da Instância 1;
- `BACKLOG` — direção futura preservada, sem implementação ativa;
- `LEGACY_OPERATIONAL` — artefato funcional mantido apenas para continuidade ou regressão;
- `RETIRED` / `SUPERSEDED` — não orienta trabalho novo;
- `HISTORICAL_EVIDENCE` — preservado para rastreabilidade, sem autoridade normativa.

A disposição detalhada está em `docs/PROJECT_STATE.md`.

## 4. Regime de mudança

Mudanças devem percorrer:

1. delimitação do pacote e do critério de completude;
2. evidência e proposta explícita;
3. branch derivada da `main` corrente;
4. alterações limitadas ao escopo;
5. validação automática e inspeção científica;
6. auditoria do delta;
7. pull request;
8. congelamento do head;
9. autorização humana quando exigida;
10. incorporação em `main`, preferencialmente por squash merge;
11. atualização de marco, estado ou changelog quando material.

Cada PR deve representar uma família de produtos, um pequeno conjunto estreitamente relacionado ou uma alteração transversal indispensável. Não se devem misturar famílias independentes, limpeza de legado e mudanças arquiteturais amplas.

## 5. Gates humanos

Exigem autorização humana explícita:

- merge de mudança científica, estrutural, executável ou pública;
- promoção do PostgreSQL como autoridade;
- publicação ou deploy deliberado;
- mudança de visibilidade;
- criação, encerramento ou migração de repositório;
- modificação ou substituição de arquivos do Drive;
- ação destrutiva ou irreversível;
- decisão científica ambígua de alto impacto.

Microdecisões reversíveis, cobertas por contrato, evidência e teste, podem ser executadas dentro de um pacote autorizado.

## 6. Papéis

### Responsável científico e mantenedor

- define missão, escopo e prioridades;
- aprova interpretações científicas e mudanças canônicas;
- autoriza merges e releases;
- decide promoção de autoridade e publicação;
- responde por identidade, autoria, licença e citação do projeto.

### Curadoria e contribuição

- apresenta evidências rastreáveis;
- preserva valores desconhecidos como desconhecidos;
- separa fonte, família, produto, release, distribuição, ativo e capacidade;
- registra limitações e evidência contraditória;
- não trata CI verde como prova factual externa;
- não generaliza metadados entre produtos, releases ou biomas.

### Automação

- valida estrutura, contratos, integridade e regressões;
- gera artefatos derivados autorizados;
- registra ocorrências e estados negativos;
- não inventa metadados;
- não promove unidades incompletas;
- não atribui compatibilidade científica universal;
- não executa gates humanos.

## 7. Curadoria e promoção

A unidade de trabalho é **um produto ou release integralmente inspecionado**.

Uma promoção requer, conforme aplicável:

- identidade e produtor;
- significado científico;
- variáveis e classes;
- método versionado;
- perfis espacial e temporal;
- qualidade, incerteza e limitações;
- distribuições, ativos, endpoints e capacidades;
- licença e citação;
- evidências por afirmação;
- revisão curatorial;
- integridade relacional e idempotência.

Presença em catálogo, URL conhecida ou CI verde não é suficiente para promoção.

## 8. Instâncias futuras

A política `docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md` é um guardrail de backlog. Ela preserva limites para futuras composições e análises, mas não autoriza motores de compatibilidade, correlação, regressão ou causalidade durante a Instância 1.

O explorador visual atual e `data/federated_layers.json` são `LEGACY_OPERATIONAL`, limitados a composição N0. Só podem receber correções de disponibilidade, segurança ou regressão enquanto a Instância 2 não for ativada.

## 9. Evidência histórica

Auditorias, ocorrências, PRs, commits e propostas de transição devem ser preservados. A limpeza do repositório deve remover duplicação normativa e ambiguidade, não rastreabilidade.

Achados históricos não alteram automaticamente dados canônicos. Uma correção só se torna vigente quando incorporada no local autoritativo apropriado.

## 10. Releases, espelhos e publicação

Releases devem ser identificáveis, reproduzíveis e coerentes com `docs/RELEASE_POLICY.md`.

Espelhos do Drive devem declarar versão, commit-fonte, data de geração e verificação de correspondência. Eles não devem ser editados como fonte independente.

A página pública atual permanece transitória. Mudanças no núcleo relacional não implicam automaticamente promoção, deploy ou substituição da interface.
