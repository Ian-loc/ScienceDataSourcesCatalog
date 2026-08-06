# Estado canônico do Simbiotrama

**Data de referência:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`

## 1. Objetivo ativo

A Instância 1 é um **catálogo relacional de fontes e ofertas de dados científicos**. Seu objetivo é permitir descoberta, compreensão e acesso a dados mantidos por instituições e plataformas externas.

Não é objetivo da Instância 1:

- copiar datasets de terceiros;
- reconstruir catálogos externos;
- enumerar integralmente releases, arquivos, layers, bandas ou endpoints;
- reproduzir genealogias completas;
- hospedar ativos externos;
- antecipar a visualização federada da Instância 2.

## 2. Hierarquia de autoridade

1. `main`;
2. este documento;
3. `docs/decisions/DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md`;
4. `docs/policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md`;
5. roadmap, workflow e governança;
6. esquema relacional simplificado quando incorporado;
7. dados públicos transitórios;
8. auditorias e evidências históricas.

Branches, conversas, tarefas recorrentes e PRs não incorporados não constituem autoridade.

## 3. Ciclo de vida

### `ACTIVE`

- Instância 1 simplificada;
- `organizations`;
- `catalog_entries`;
- `entry_variables`;
- `entry_evidence`;
- `connector_profiles` opcionais;
- curadoria de granularidade mínima suficiente;
- preparação de website dinâmico sustentado pelo catálogo;
- migração controlada dos registros públicos atuais.

### `BACKLOG`

- Instância 2 — visualização federada por conectores;
- Instância 3 — contexto científico por literatura curada;
- receitas analíticas;
- produtos derivados;
- harmonização e composição;
- taxonomias avançadas;
- inventários técnicos de endpoints quando necessários a conectores específicos.

### `LEGACY_TRANSITIONAL`

Preservado para migração e reaproveitamento seletivo, sem expansão como arquitetura-alvo:

- esquema profundo do Marco 1;
- `product_families`;
- `product_releases`;
- `distributions`;
- `data_assets`;
- `access_capabilities`;
- perfis metodológicos, espaciais, temporais e de qualidade como entidades obrigatórias;
- guards específicos por produto.

Esses componentes podem fornecer evidências, campos ou padrões úteis. Não devem voltar a determinar a completude da Instância 1.

### `LEGACY_OPERATIONAL`

- CSV/JSON atuais;
- interface pública estática;
- explorador visual N0;
- `data/federated_layers.json`.

Esses artefatos permanecem funcionais durante a transição, mas não orientam expansão do novo núcleo.

### `RETIRED` / `SUPERSEDED`

- classes universais de compatibilidade;
- Fase 1 do Simbioscópio;
- registros paralelos de variáveis;
- branches encerradas após os PRs #54–#56;
- qualquer fluxo que trate inventário integral de ativos externos como requisito geral.

### `HISTORICAL_EVIDENCE`

- auditorias;
- ocorrências;
- commits e PRs encerrados;
- snapshots;
- relatórios de CI;
- pacotes de curadoria não promovidos.

## 4. PR #57

O PR #57 está congelado e não deve ser mesclado ou ampliado. Sua autorização antiga não é válida. O pacote é candidato a `superseded` porque implementa profundidade incompatível com a nova granularidade.

Seus achados podem ser reutilizados seletivamente como evidência para uma entrada compacta do DETER Cerrado. Os JSONs, guards, inventário de ativos e exigências de promoção não devem ser transportados automaticamente.

## 5. Unidade de trabalho

A unidade de trabalho é uma **entrada de catálogo suficientemente útil**.

Uma entrada pode representar fonte, plataforma, coleção, produto de dados ou serviço. A granularidade deve seguir a identidade oferecida pela fonte e a necessidade do usuário, não a estrutura interna completa da plataforma.

## 6. Critério de completude

Uma entrada está concluída quando informa, com evidência proporcional:

- quem oferece;
- o que é;
- quais dados e variáveis inclui;
- onde e quando se aplica;
- como acessar;
- quais condições de uso existem;
- quais links oficiais sustentam a ficha;
- se há conector futuro selecionado.

Não se exige inventário de arquivos, release, checksum, bytes, esquema físico ou licença por ativo, salvo necessidade específica documentada.

## 7. Próximo caminho crítico

1. incorporar a decisão e a política de escopo;
2. implementar o núcleo relacional simplificado;
3. migrar registros atuais sem perda;
4. testar GEDI, DETER Cerrado, IBGE e ANA/SNIRH;
5. gerar uma projeção JSON para website dinâmico;
6. auditar simplicidade, utilidade e sustentabilidade;
7. promover o novo núcleo somente após autorização humana.
