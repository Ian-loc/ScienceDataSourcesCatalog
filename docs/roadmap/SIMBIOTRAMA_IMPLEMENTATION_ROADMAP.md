# Roadmap de implementação do Simbiotrama

**Status:** vigente  
**Foco ativo:** Instância 1 — catálogo relacional científico-operacional  
**Marco incorporado:** I1-M1  
**Instâncias 2 e 3:** backlog de longo prazo

## 1. Objetivo atual

Transformar o catálogo público simplificado em uma base relacional profunda de produtos de dados georreferenciados sobre o Brasil, com significado científico, integridade, evidência e acesso operacional verificáveis.

A unidade de progresso é um produto ou release integralmente inspecionado. O número bruto de fontes, links ou camadas não é critério suficiente de qualidade.

## 2. Regras de execução

1. Aprofundar produtos antes de expandir funcionalidades.
2. Separar organização, fonte, família, produto, release, distribuição, ativo e capacidade.
3. Não promover valores desconhecidos por inferência.
4. Sustentar afirmações materiais com evidência rastreável.
5. Operar por branches e PRs pequenos, coerentes e auditáveis.
6. Não misturar famílias independentes, higiene do legado e alterações transversais.
7. Preservar CSV/JSON e a página pública durante a transição.
8. Manter Instâncias 2 e 3 fora do caminho crítico.
9. Executar auditoria proporcional ao risco e à extensão do delta.
10. Promover o banco somente após gate formal de prontidão canônica.

## 3. Marcos da Instância 1

### I1-M1 — núcleo relacional e staging

**Estado:** `COMPLETED`  
**Incorporação:** PR #54; registro no PR #55.

Entregas consolidadas:

- direção científica da Instância 1;
- esquema PostgreSQL/PostGIS;
- staging sem perda;
- carga e promoção idempotentes;
- resolução inicial de entidades;
- evidência por afirmação;
- revisão curatorial;
- gates científicos e operacionais;
- preservação da autoridade pública transitória.

### I1-M1-SANITY — alinhamento pós-marco

**Estado:** `ACTIVE_UNTIL_MERGED`

Objetivos:

- harmonizar nome, autoridade e documentação;
- classificar ativos, backlog, legado, retirados e evidência histórica;
- fechar PRs substituídos;
- reduzir documentação redundante;
- preservar protótipos apenas como legado operacional;
- preparar uma linha de base limpa para o Marco 2A.

### I1-M2 — fechamento científico-operacional do piloto

**Estado:** `NEXT`

Pacotes independentes:

- **M2A — DETER Cerrado**;
- M2B — DETER Amazônia;
- M2C — DETER Pantanal;
- M2D — PRODES, dividido por famílias e produtos coerentes;
- M2E — vegetação secundária;
- M2F — Dynamic World V1;
- M2G — TerraClass Amazônia 2020.

Critério de completude por produto/release:

- identidade e produtor;
- significado, variáveis e classes;
- método versionado;
- perfis espacial e temporal;
- qualidade, validação, incerteza e limitações;
- distribuição, ativo, endpoint e capacidades;
- licença e citação;
- evidências por afirmação;
- revisão curatorial;
- gates executáveis e auditoria do delta.

### I1-M3 — resolução das 51 fontes legadas

**Estado:** `PLANNED`

Objetivo:

- resolver cada registro como organização, fonte, família, produto, distribuição, capacidade ou item não resolvido;
- identificar produtos reais escondidos em plataformas;
- registrar propostas sem substituir silenciosamente a autoridade pública;
- promover seletivamente somente unidades suficientes.

Primeiro cursor preservado: `DR0001 — Clima Gerais`.

### I1-M4 — expansão brasileira prioritária

**Estado:** `PLANNED`

Ordem inicial:

1. MapBiomas;
2. TerraBrasilis / INPE;
3. IBGE;
4. ANA / SNIRH;
5. DATASUS;
6. INMET;
7. Embrapa;
8. ICMBio e MMA;
9. produtos internacionais com cobertura sistemática do Brasil.

Cada família relevante deve possuir estratégia de enumeração: `complete`, `family_level`, `external_index`, `representative_sample` ou `selective`.

### I1-M5 — interface sustentada pelo banco

**Estado:** `BLOCKED_BY_MATURITY`

Entregas futuras:

- busca por produto, variável, objeto observado, método, qualidade e acesso;
- filtros espaciais e temporais estruturados;
- perfis públicos de produto e release;
- evidências e data de revisão;
- exportações reproduzíveis.

A interface não deve depender de campos agregados ambíguos.

### I1-M6 — prontidão e promoção canônica

**Estado:** `BLOCKED_BY_GATES`

Entregas:

- auditoria transversal do esquema e dos dados;
- importação e exportação reproduzíveis;
- backups e migrações;
- API ou camada de leitura;
- sincronização do site e dos espelhos;
- resolução das ocorrências críticas e altas;
- decisão humana de promoção.

Somente após esse gate PostgreSQL/PostGIS poderá substituir os CSVs como autoridade canônica.

### I1-M7 — migração privada controlada

**Estado:** `BLOCKED_BY_I1_COMPLETION`

Preparar:

- manifesto e inventário;
- hashes e backup integral;
- baseline limpa;
- histórico selecionado;
- CI e proteção de branch;
- revalidação completa;
- separação entre núcleo privado e presença pública autorizada.

Criação, visibilidade e encerramento de repositório exigem autorização humana explícita.

## 4. Workstreams permanentes

### Curadoria científica

Significado, variáveis, métodos, escalas, qualidade, incerteza, limitações e evidências.

### Curadoria operacional

URLs, formatos, APIs, serviços, autenticação, licenças, testes de acesso e ativos.

### Arquitetura de dados

Normalização, IDs, chaves, migrações, taxonomias, importação e exportação.

### Qualidade e governança

Auditoria, ocorrências, duplicidade, versões, rastreabilidade, CI e gates humanos.

## 5. Backlog preservado

### Instância 2 — composição geográfica

Poderá incluir composição visual, mapas sincronizados, perfis territoriais, recortes e receitas documentadas. Não deve atribuir compatibilidade científica universal.

### Instância 3 — contexto científico

Poderá recuperar literatura curada por fenômeno, território, escala, período e método, distinguindo evidência direta, análoga e metodológica.

Nenhuma das duas instâncias deve receber implementação ativa antes da maturidade e promoção da Instância 1.

## 6. Critério de sucesso

O catálogo deve responder com precisão:

- o que o produto representa;
- qual release está em uso;
- quais variáveis contém;
- como foi produzido;
- qual é o suporte espacial e temporal;
- quais limitações e incertezas existem;
- como acessar;
- qual licença e citação se aplicam;
- quais evidências sustentam cada afirmação material.
