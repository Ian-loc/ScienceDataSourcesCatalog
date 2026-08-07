# DEC — Instância 1 como núcleo relacional profundo

**Data original:** 4 de agosto de 2026  
**Estado atual:** `SUPERSEDED`  
**Substituída por:** `DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md`

## Disposição

Esta decisão registrou a arquitetura incorporada no Marco 1, baseada na separação entre organização, fonte, família, produto, release, distribuição, ativo e capacidade.

O Marco 1 permanece uma evidência técnica válida de:

- PostgreSQL/PostGIS;
- staging sem perda;
- integridade referencial;
- migrações e cargas idempotentes;
- separação entre plataformas, produtos e serviços;
- revisão e evidência curatorial.

Entretanto, a aplicação prática do modelo demonstrou granularidade e custo excessivos para a finalidade atual da Instância 1. A decisão deixou de orientar completude, curadoria e expansão do esquema.

## Elementos aposentados como obrigação universal

Não devem ser tratados como requisitos para toda entrada:

- família de produtos;
- release ou edição;
- distribuição;
- ativo;
- capacidade detalhada;
- método versionado como entidade;
- perfis completos de espaço, tempo e qualidade;
- evidência atômica por afirmação;
- inspeção integral de endpoints e arquivos.

Esses elementos podem ser reutilizados seletivamente quando houver caso de uso concreto, especialmente em conectores futuros.

## Autoridade vigente

A decisão vigente é:

- `docs/decisions/DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md`;
- `docs/policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md`.

A arquitetura incorporada não deve ser removida de forma destrutiva antes de migração auditada. Ela permanece como legado técnico e evidência histórica.
