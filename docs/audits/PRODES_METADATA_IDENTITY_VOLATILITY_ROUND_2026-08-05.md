# Auditoria — volatilidade da identidade de metadados PRODES

**Data/hora:** 05/08/2026 10:24 BRT  
**Escopo:** família `PF000001` — PRODES Amazônia  
**Estado:** pré-promoção; nenhuma alteração da autoridade canônica

## Unidade auditada

Foi comparado o registro local de UUIDs GeoNetwork com o conjunto atualmente exposto pela busca oficial do catálogo TerraBrasilis para o GeoPackage PRODES Amazônia Legal.

## Achado material

Cinco papéis científico-operacionais apresentam UUIDs distintos entre o inventário previamente registrado e o conjunto atualmente observado no catálogo:

- máscara acumulada de supressão;
- incremento anual;
- hidrografia;
- resíduo anual;
- máscara de não floresta.

A divergência não prova erro, substituição nem atualização do produto. Ela prova somente que existem múltiplos registros de metadados observados para papéis equivalentes ou semelhantes. UUID do GeoNetwork é identidade de registro de catálogo; não é, por si só, identidade permanente de produto, release, distribuição ou ativo.

## Correção implementada

Foram criados:

- `database/mappings/prodes_metadata_identity_volatility_guard_2026.json`;
- `scripts/validate_prodes_metadata_identity_volatility_guard.py`.

O portão:

1. preserva os UUIDs anteriormente registrados;
2. registra separadamente os UUIDs atualmente observados;
3. mantém todos os conflitos como `unresolved`;
4. proíbe substituição automática, fusão por título, promoção canônica e exclusão prematura;
5. exige inspeção completa dos registros, datas, links, escopo, responsáveis, relações de supersessão e ativos associados antes de qualquer decisão curatorial.

O validador foi integrado à cadeia `scripts/validate_prodes_operational_evidence.py`.

## Auditoria da própria correção

Verificado:

- vínculo exclusivo com `PF000001`;
- cinco papéis controlados;
- dez UUIDs válidos e não repetidos;
- pares de UUIDs distintos;
- estados de conflito e resolução controlados;
- fonte HTTPS oficial do INPE;
- ausência de autorização de promoção;
- exigência explícita de evidência para resolver cada conflito;
- proteção contra substituição, fusão, exclusão e promoção prematuras.

## Limitação residual

Ainda é necessário recuperar o conteúdo completo dos dez registros envolvidos e determinar, por papel, se representam duplicação, revisão, substituição, recorte distinto, pacote diferente ou coexistência legítima. Nenhum UUID foi promovido como canônico.

## Decisão

A identidade de metadados PRODES passa a ser tratada como entidade versionável e potencialmente volátil. Produto, release, registro de metadado, distribuição e ativo permanecem entidades distintas.
