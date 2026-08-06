# Auditoria de completude dos componentes GeoNetwork — PRODES Amazônia

**Data e hora:** 05/08/2026 08:26 BRT  
**Escopo:** Instância 1, família `PF000001 — PRODES`  
**Estado:** pré-promoção; nenhum ativo, release ou distribuição normalizada foi promovido

## Unidade auditada

Foi revisado o registro `database/mappings/prodes_geonetwork_metadata_registry_2026.json`, que anteriormente continha seis UUIDs específicos do GeoNetwork para o pacote GeoPackage do PRODES Amazônia.

A inspeção do registro oficial agregado mostrou que o pacote documenta também quatro componentes específicos do domínio cartográfico de não floresta que estavam ausentes do contrato local:

- máscara acumulada de supressão em não floresta;
- incrementos de supressão em não floresta;
- resíduo anual em não floresta;
- hidrografia em não floresta.

A ausência não invalidava os seis identificadores já registrados, mas deixava o inventário operacional incompleto e criava risco de fundir objetos do domínio florestal com objetos do domínio de não floresta.

## Correções aplicadas

O contrato foi ampliado de seis para dez registros, preservando `promotion_authorized=false` e todos os campos de ativo, checksum, release e URL direta como nulos.

Foi acrescentado `domain_context` com vocabulário controlado:

- `forest_domain`;
- `nonforest_domain`.

Os papéis de distribuição foram tornados específicos para evitar o uso do papel genérico `complete_map_vector_component` em objetos semanticamente distintos.

O validador `scripts/validate_prodes_geonetwork_metadata_registry.py` agora exige:

- exatamente dez UUIDs verificados;
- dez papéis de distribuição únicos;
- presença dos dois domínios cartográficos;
- cinco papéis específicos no domínio de não floresta;
- ausência de URL direta, checksum e release antes de inspeção material;
- manutenção das inferências proibidas e pendências críticas.

## Verificação científica e semântica

A máscara `Não Floresta` permanece distinta de eventos anuais de supressão dentro desse domínio. Hidrografia permanece componente de referência e não evento de desmatamento. Componentes homólogos dos domínios florestal e não floresta não foram fundidos.

Não foram inferidos CRS, geometria, esquema de campos, licença, citação, estabilidade de endpoint, data de release ou integridade dos bytes.

## Resultado

A identidade de metadados do pacote PRODES Amazônia está mais completa, mas continua em pré-promoção. A próxima etapa é resolver links associados a cada UUID e inspecionar pelo menos um ativo manejável antes de normalizar distribuição, ativo ou release.
