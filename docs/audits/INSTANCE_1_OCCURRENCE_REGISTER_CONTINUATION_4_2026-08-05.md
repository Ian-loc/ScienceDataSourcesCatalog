# Continuação 4 do registro cumulativo de ocorrências — Instância 1

Horários humanos usam `America/Sao_Paulo`.

| ID | Data e hora | Round | Entidade/arquivo | Categoria | Evidência | Severidade | Estado | Correção/verificação | Risco residual |
|---|---|---|---|---|---|---|---|---|---|
| `I1-20260805-041` | 05/08/2026 22:23–22:31 | PRODES — catálogo de downloads | `prodes_catalog_reprocessing_state_guard_2026.json` | inferência operacional indevida a partir de aviso genérico de reprocessamento | página oficial mantém entradas descobríveis, aviso de atualização de 03/03/2026 e mensagem genérica de arquivo em reprocessamento, sem identificar inequivocamente o componente afetado | `medium` | `corrected` | gate impede converter aviso em `working`, `unavailable`, release ou vínculo individual; exige teste datado por componente | arquivos e endpoints podem mudar durante o reprocessamento; estado individual permanece não resolvido |

## Estado de continuidade

A ocorrência `041` não bloqueia a família PRODES nem o trabalho independente. Ela bloqueia apenas a promoção operacional baseada exclusivamente na interface agregada. A próxima promoção exige URL oficial individual, resposta HTTP, redirecionamentos, cabeçalhos, bytes, checksum e vínculo com release ou snapshot científico.
