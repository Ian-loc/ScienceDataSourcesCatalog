# Continuação 4 do registro cumulativo de ocorrências — Instância 1

Horários humanos usam `America/Sao_Paulo`.

| ID | Data e hora | Round | Entidade/arquivo | Categoria | Evidência | Severidade | Estado | Correção/verificação | Risco residual |
|---|---|---|---|---|---|---|---|---|---|
| `I1-20260805-041` | 05/08/2026 22:23–22:31 | PRODES — catálogo de downloads | `prodes_catalog_reprocessing_state_guard_2026.json` | inferência operacional indevida a partir de aviso genérico de reprocessamento | página oficial mantém entradas descobríveis, aviso de atualização de 03/03/2026 e mensagem genérica de arquivo em reprocessamento, sem identificar inequivocamente o componente afetado | `medium` | `corrected` | gate impede converter aviso em `working`, `unavailable`, release ou vínculo individual; exige teste datado por componente | arquivos e endpoints podem mudar durante o reprocessamento; estado individual permanece não resolvido |
| `I1-20260805-042` | 05/08/2026 23:22–23:31 | DETER Amazônia — fronteira científica inicial | `deter_amazon_scientific_boundary_guard_2026.json` | colapso entre alerta operacional, taxa e perfis históricos/atuais | fontes oficiais distinguem alerta expedito de taxa PRODES e registram perfis diferentes: DETER-B histórico com WFI/AWiFS, 6,25 ha públicos e cinco dias; perfil atual com Amazônia-1/CBERS WFI e 3 ha | `high` | `corrected` | gate preserva alerta versus taxa, detecção versus ocorrência e perfis operacionais datados; impede herança automática de sensores, resolução, limiar e latência | release, distribuição, endpoint, bytes, esquema, qualidade, licença e citação atuais permanecem não resolvidos |

## Estado de continuidade

A ocorrência `041` bloqueia apenas promoção operacional PRODES baseada na interface agregada. A ocorrência `042` bloqueia apenas a promoção do DETER Amazônia sem produto, release e perfis contemporâneos resolvidos. Nenhuma autoriza merge, publicação, promoção canônica ou herança de atributos entre famílias e releases.
