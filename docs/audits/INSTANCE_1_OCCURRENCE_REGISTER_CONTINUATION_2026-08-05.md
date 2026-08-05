# Continuação do registro cumulativo de ocorrências — Instância 1

Continuação operacional de `docs/audits/INSTANCE_1_OCCURRENCE_REGISTER.md`, iniciada em 05/08/2026. Horários humanos usam `America/Sao_Paulo`.

**Severidade:** `critical`, `high`, `medium`, `low`, `observation`  
**Estado:** `open`, `corrected`, `accepted_limitation`, `deferred_private_migration`, `not_reproducible`, `closed`

| ID | Data e hora | Round | Entidade/arquivo | Categoria | Descrição e evidência | Severidade | Estado | Correção/verificação | Risco residual |
|---|---|---:|---|---|---|---|---|---|---|
| I1-20260805-017 | 05/08/2026 06:25 BRT | 13 | catálogo público de downloads TerraBrasilis; `database/mappings/prodes_catalog_integrity_guard_2026.json` | integridade e confiança de endpoint | A inspeção direta do HTML público encontrou conteúdo externo não relacionado aos dados científicos e link para o domínio não oficial `dentoxol.com`, entre o título de downloads e o menu de produtos. Isso impede usar a página agregadora como fonte automática confiável de URLs diretas, licença, citação, release ou metadados críticos. | high | accepted_limitation | Criado portão com `integrity_state=suspended_for_automatic_extraction`; extração automática bloqueada; resolução redirecionada ao GeoNetwork e aos geosserviços oficiais, com verificação específica por registro/camada. `scripts/validate_prodes_catalog_integrity_guard.py` foi integrado à cadeia PRODES executada pelo CI. | A página pode continuar misturando rótulos válidos com conteúdo comprometido. Pode confirmar visualmente categorias, mas não sustentar automaticamente endpoints ou metadados de promoção. |

## Continuidade

A ocorrência bloqueia apenas a extração automática a partir da página agregadora. A inspeção independente de registros do GeoNetwork, camadas do GeoServer, documentação técnica e ativos recuperados de endpoints verificados continua autorizada.
