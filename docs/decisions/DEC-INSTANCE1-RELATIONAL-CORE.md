# DEC — Instância 1 como núcleo ativo do Symbiotrama

**Data:** 2026-08-04  
**Status:** aprovada para implementação  
**Escopo:** direção científica, arquitetura de dados e prioridades do projeto

## Contexto

A evolução recente do projeto misturou três capacidades distintas:

1. catálogo de fontes e produtos;
2. composição e visualização de produtos georreferenciados;
3. contextualização científica e síntese de literatura sobre composições.

A tentativa de modelar simultaneamente essas capacidades ampliou prematuramente o escopo e desviou atenção da principal lacuna atual: a base ainda possui poucas famílias de produtos descritas em profundidade e mistura produtos científicos com catálogos, serviços e infraestruturas.

## Decisão

O foco ativo do projeto passa a ser a **Instância 1 — Catálogo relacional científico-operacional**.

Ela será implementada sobre PostgreSQL/PostGIS e deverá descrever, com precisão:

- fontes;
- famílias de produtos;
- produtos científicos;
- versões;
- variáveis e classes;
- significado científico;
- métodos;
- suporte espacial e temporal;
- qualidade, incerteza e vieses;
- distribuições, ativos e capacidades de acesso;
- citações, evidências e revisão curatorial.

Os CSVs atuais serão preservados durante a migração. O banco relacional será promovido a fonte canônica somente após validação e geração reproduzível das exportações públicas.

## Consequências

### Positivas

- reduz ambiguidade entre fonte, produto e serviço;
- melhora integridade e rastreabilidade;
- permite expansão produto por produto;
- torna o catálogo útil independentemente das visualizações futuras;
- cria base para filtros científicos e operacionais;
- preserva caminho técnico para API, composição e síntese científica.

### Custos

- exige migração e normalização dos dados atuais;
- aumenta o esforço de curadoria por produto;
- requer evidência por campo para afirmações importantes;
- demanda controle de versões, IDs e revisões.

## Instâncias adiadas

### Instância 2 — composição geográfica

Permanece documentada, mas não deve liderar a modelagem nem receber novas capacidades analíticas antes da consolidação da Instância 1.

### Instância 3 — contexto científico

Permanece documentada como ambição futura de síntese breve e auditável de literatura associada a composições escolhidas pelo usuário. Não será implementada nesta fase.

## Regra operacional

Toda intervenção atual deve responder primeiro:

> Esta mudança melhora a capacidade de descobrir, compreender, verificar e acessar produtos de dados georreferenciados?

Se a resposta for negativa e a mudança servir apenas às Instâncias 2 ou 3, ela deve permanecer no backlog de longo prazo.

## Referências internas

- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`;
- `database/schema/001_instance1_core.sql`;
- `database/README.md`;
- `PRODUCT_CATALOG_MODEL.md`;
- `docs/roadmap/SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md`.
