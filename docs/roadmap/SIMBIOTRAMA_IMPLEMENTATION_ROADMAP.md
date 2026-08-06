# Roadmap de implementação do Simbiotrama

**Foco ativo:** Instância 1 — catálogo relacional simplificado  
**Instâncias 2 e 3:** backlog

## 1. Objetivo

Entregar um catálogo funcional, pesquisável e sustentável de fontes e ofertas de dados científicos, com metadados suficientes para descoberta, compreensão e acesso.

O catálogo não deve reproduzir a estrutura interna completa das plataformas externas.

## 2. Princípios de execução

1. Usar granularidade mínima suficiente.
2. Preservar a terminologia e os metadados diretos do produtor.
3. Normalizar somente o necessário para busca e filtros.
4. Manter dados e arquivos nas fontes originais.
5. Não enumerar integralmente produtos, releases, arquivos, layers ou endpoints.
6. Não criar novas entidades sem necessidade demonstrada.
7. Separar catálogo da Instância 1 de conectores da Instância 2.
8. Manter CSV/JSON e página pública durante a transição.
9. Validar com casos heterogêneos antes de expandir.
10. Promover somente após auditoria e autorização humana.

## 3. Marcos

### I1-R0 — correção de direção

**Estado:** `ACTIVE`

Entregas:

- decisão do núcleo simplificado;
- política de escopo e granularidade;
- alinhamento de README, estado, roadmap, workflow, governança e dicionário;
- congelamento do PR #57;
- classificação do esquema profundo como `LEGACY_TRANSITIONAL`;
- tarefa recorrente atualizada.

### I1-R1 — núcleo relacional simplificado

**Estado:** `NEXT`

Implementar:

- `organizations`;
- `catalog_entries`;
- `entry_variables`;
- `entry_evidence`;
- `connector_profiles` opcionais;
- IDs estáveis;
- índices e constraints mínimos;
- migração reversível a partir dos CSVs atuais;
- validação de idempotência.

O pacote não deve implementar inventário de ativos, genealogia de releases ou taxonomia universal.

### I1-R2 — piloto heterogêneo

**Estado:** `PLANNED`

Testar o mesmo modelo com:

1. GEDI;
2. DETER Cerrado;
3. IBGE;
4. ANA/SNIRH.

Critérios de aprovação:

- nenhuma plataforma precisa ser reproduzida integralmente;
- poucos campos obrigatórios permanecem vazios;
- o usuário entende conteúdo, cobertura e acesso;
- a entrada suporta busca e filtros;
- conectores são opcionais;
- o modelo não exige arquivo, layer ou release por entrada.

### I1-R3 — migração do catálogo atual

**Estado:** `BLOCKED_BY_R2`

- mapear os 51 registros atuais para entradas;
- preservar campos e proveniência;
- resolver duplicidades evidentes;
- registrar lacunas;
- evitar decomposição automática em múltiplos produtos;
- gerar exportações compatíveis com a página atual.

### I1-R4 — website dinâmico da Instância 1

**Estado:** `BLOCKED_BY_R3`

- busca textual;
- filtros por organização, tema, modalidade, variável, cobertura, período e acesso;
- ficha de entrada;
- links oficiais;
- sinalização de acesso e autenticação;
- JSON ou API de leitura simples;
- preservação de atribuição.

Não inclui visualização federada de dados.

### I1-R5 — prontidão canônica

**Estado:** `BLOCKED_BY_GATES`

- auditoria transversal;
- migração e exportação reproduzíveis;
- backups;
- CI;
- documentação;
- resolução de ocorrências críticas;
- decisão humana de promoção.

Somente então o banco simplificado poderá substituir os CSVs como autoridade.

### I2 — visualização federada

**Estado:** `BACKLOG`

- seleção de conectores;
- APIs e serviços externos;
- visualização de camadas;
- atribuição por fonte;
- configuração compartilhável;
- sem cópia integral dos dados.

### I3 — contexto científico

**Estado:** `BACKLOG`

- literatura curada;
- mapeamento entre entradas e evidências científicas;
- sínteses auditáveis;
- sem busca web irrestrita por padrão.

## 4. Indicadores de progresso

- entradas suficientemente curadas;
- campos essenciais sustentados;
- cobertura de variáveis ou grupos;
- links oficiais válidos;
- registros migrados sem perda;
- entradas representáveis pelo mesmo modelo;
- tempo médio por entrada;
- retrabalho por revisão;
- conectores selecionados, não inventariados;
- ausência de expansão indevida de escopo.

Número de arquivos, commits, layers ou endpoints não é indicador de progresso.

## 5. Critério de sucesso

A Instância 1 deve responder:

- quem oferece os dados;
- que tipo de informação está disponível;
- quais variáveis ou temas são cobertos;
- onde e quando se aplica;
- como acessar;
- quais condições de uso existem;
- onde consultar os metadados oficiais;
- se há conector futuro disponível.

Se o usuário precisa navegar pela genealogia interna de uma plataforma para compreender a ficha, o catálogo falhou em simplificar.
