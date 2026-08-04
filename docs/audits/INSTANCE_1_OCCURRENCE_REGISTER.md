# Registro cumulativo de ocorrências — Instância 1

Este registro acompanha ocorrências encontradas durante os rounds de implementação, curadoria e auditoria da Instância 1. Horários humanos usam `America/Sao_Paulo`.

## Vocabulários controlados

**Severidade:** `critical`, `high`, `medium`, `low`, `observation`  
**Estado:** `open`, `corrected`, `accepted_limitation`, `deferred_private_migration`, `not_reproducible`, `closed`

## Ocorrências

| ID | Data e hora | Round | Entidade/arquivo | Categoria | Descrição e evidência | Severidade | Estado | Correção/verificação | Risco residual |
|---|---|---:|---|---|---|---|---|---|---|
| I1-20260804-001 | 04/08/2026 19:32 BRT | 3 | `scripts/enrich_instance1_dynamic_world.py` | integridade semântica do esquema | A primeira implementação usou `product_release` em `metadata_assertions.entity_type`, mas o contrato SQL aceita `release`. A inspeção direta de `001_instance1_core.sql` detectou a divergência antes da integração ao CI. | high | corrected | A implementação inicial foi removida e substituída; o script vigente usa `release`. O workflow compila e executa o enriquecimento duas vezes para testar idempotência. | Nenhum risco conhecido após CI verde. |
| I1-20260804-002 | 04/08/2026 19:37 BRT | 3 | Dynamic World V1 / `PR000011` | profundidade científica | O piloto possuía significado científico mínimo, mas não tinha bandas, método, perfis espacial/temporal, qualidade ou citação normalizados. | high | corrected | Adicionado enriquecimento idempotente com nove probabilidades, banda `label`, método, perfis, qualidade, seis evidências oficiais e artigo descritor. O validador exige 10 variáveis vinculadas e perfis completos. | Métricas detalhadas por classe ainda precisam de auditoria direta do artigo antes de aprovação final. |
| I1-20260804-003 | 04/08/2026 19:39 BRT | 3 | Dynamic World V1 / qualidade | completude de validação | A documentação oficial registra probabilidades, cautelas e referência ao artigo, mas o round não transcreveu métricas de acurácia por classe. | medium | open | Mantido `review_status=in_progress`; `corrections_required` registra a auditoria pendente do artigo e o teste dos endpoints/ativos. | Impede aprovação científica final do produto, mas não bloqueia o aprofundamento de TerraClass ou outras unidades independentes. |
| I1-20260804-004 | 04/08/2026 19:41 BRT | 3 | repositório público atual | patrimônio intelectual | Todo conteúdo no PR público é publicamente acessível e não pode ser tornado confidencial retroativamente. | observation | deferred_private_migration | O round limitou-se ao núcleo da Instância 1 e não implementou componentes proprietários das Instâncias 2/3. A migração privada permanece condicionada ao portão final e à autorização humana. | Exposição histórica do material já publicado permanece inerente ao repositório público. |

## Regra de continuidade

Ocorrências localizadas bloqueiam apenas a unidade ou promoção diretamente dependente. O trabalho independente continua. Ações destrutivas, merge, publicação, promoção canônica e migração irreversível permanecem bloqueadas diante de ocorrência `critical` ou falta de autorização humana.
