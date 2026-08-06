# DEC — Instância 1 como núcleo ativo do Simbiotrama

**Data:** 2026-08-04  
**Status:** aprovada e incorporada no Marco 1  
**Escopo:** direção científica, arquitetura de dados e prioridades do projeto

## Contexto

A evolução inicial misturou três capacidades distintas:

1. catálogo de fontes e produtos;
2. composição e visualização de produtos georreferenciados;
3. contextualização científica e literatura sobre composições.

Essa simultaneidade ampliou prematuramente o escopo e desviou atenção da principal lacuna: poucas famílias estavam descritas em profundidade e produtos científicos apareciam misturados a catálogos, serviços e infraestruturas.

## Decisão

O foco ativo é a **Instância 1 — Catálogo relacional científico-operacional**.

Ela é implementada sobre PostgreSQL/PostGIS e descreve:

- organizações e fontes;
- famílias de produtos;
- produtos científicos;
- releases, versões e edições;
- variáveis e classes;
- significado científico;
- métodos;
- suporte espacial e temporal;
- qualidade, incerteza, vieses e limitações;
- distribuições, ativos e capacidades de acesso;
- licenças, citações, evidências e revisão curatorial.

Os CSVs atuais permanecem como autoridade da versão pública durante a migração. O banco relacional somente será promovido a fonte canônica após validação transversal, exportações reproduzíveis e autorização humana.

## Consequências

### Positivas

- reduz ambiguidade entre fonte, produto e serviço;
- melhora integridade e rastreabilidade;
- permite expansão produto por produto;
- torna o catálogo útil independentemente das visualizações futuras;
- cria base para filtros científicos e operacionais;
- preserva caminho técnico para API, composição e literatura curada.

### Custos

- exige migração e normalização dos dados atuais;
- aumenta o esforço de curadoria por produto;
- requer evidência por afirmação;
- demanda controle de versões, IDs, revisões e ocorrências;
- posterga funcionalidades visuais e analíticas não essenciais.

## Disposição das Instâncias 2 e 3

### Instância 2 — composição geográfica

**Estado:** `BACKLOG`.

Permanece documentada, mas não deve liderar a modelagem nem receber capacidades analíticas antes da consolidação e promoção da Instância 1.

### Instância 3 — contexto científico

**Estado:** `BACKLOG`.

Permanece como ambição futura de literatura curada e contextualização auditável. Não é implementada na fase atual.

## Disposições pós-Marco 1

- a antiga “Fase 1 do Simbioscópio” foi substituída;
- o PR #53 foi fechado como `superseded` e não deve ser mesclado ou reutilizado integralmente;
- classes universais de compatibilidade não são modelo ativo;
- registros de variáveis devem usar o núcleo relacional, não tabelas paralelas de protótipo;
- o explorador visual atual é `LEGACY_OPERATIONAL` e limitado a N0;
- auditorias e protótipos anteriores são `HISTORICAL_EVIDENCE`;
- a nomenclatura ativa do projeto é **Simbiotrama**.

## Regra operacional

Toda intervenção deve responder:

> Esta mudança melhora a capacidade de descobrir, compreender, verificar e acessar produtos de dados georreferenciados?

Se a resposta for negativa e a mudança servir apenas às Instâncias 2 ou 3, ela permanece no backlog.

## Referências internas

- `docs/PROJECT_STATE.md`;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`;
- `database/schema/001_instance1_core.sql`;
- `database/README.md`;
- `PRODUCT_CATALOG_MODEL.md`;
- `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md`.
