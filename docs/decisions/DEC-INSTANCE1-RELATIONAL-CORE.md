# DEC — Instância 1 como núcleo ativo do Simbiotrama

**Data original:** 2026-08-04  
**Estado atual:** `SUPERSEDED_IN_PART`  
**Substituída por:** `DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md`

## Disposição

Esta decisão estabeleceu corretamente:

- Instância 1 como foco ativo;
- separação entre catálogo, visualização e literatura;
- PostgreSQL como destino possível;
- preservação da autoridade pública durante a migração;
- necessidade de evidência e revisão;
- manutenção das Instâncias 2 e 3 em backlog.

Esses elementos permanecem válidos.

## Elementos substituídos

A revisão de escopo de 6 de agosto de 2026 concluiu que a seguinte arquitetura era excessivamente profunda para a Instância 1:

```text
organização
→ fonte
→ família
→ produto
→ release
→ distribuição
→ ativo
→ capacidade
```

Deixam de ser requisitos canônicos:

- inventário de famílias;
- releases obrigatórias;
- distribuições como entidade obrigatória;
- `data_assets`;
- capacidades de acesso enumeradas;
- perfis separados obrigatórios;
- curadoria integral por produto/release;
- reconstrução de genealogia externa.

## Direção vigente

A arquitetura ativa proposta é:

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles  [opcional]
```

Consulte:

- `DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md`;
- `../PROJECT_STATE.md`;
- `../policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md`;
- `../INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`.

## Valor histórico

O esquema profundo e seus artefatos permanecem como `LEGACY_TRANSITIONAL`. Podem fornecer staging, idempotência, evidências e componentes reutilizáveis, mas não devem orientar nova expansão.
