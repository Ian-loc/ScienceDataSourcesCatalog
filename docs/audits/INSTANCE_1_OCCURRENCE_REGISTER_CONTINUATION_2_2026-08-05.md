# Continuação 2 do registro cumulativo de ocorrências — Instância 1

Horários humanos usam `America/Sao_Paulo`.

| ID | Data e hora | Round | Entidade/arquivo | Categoria | Descrição e evidência | Severidade | Estado | Correção/verificação | Risco residual |
|---|---|---:|---|---|---|---|---|---|---|
| I1-20260805-025 | 05/08/2026 13:30 BRT | Dynamic World — reconciliação operacional normalizada | `DD000017`, `DD000019`; scripts de enriquecimento e validação | força da evidência operacional e proveniência | A primeira implementação transformava a classificação do registro WRI e do repositório de software em `access_status=working` com timestamp de teste, embora o contrato não registrasse teste operacional equivalente ao catálogo Earth Engine e ao visualizador. | high | corrected | Criados pós-processamento idempotente e validador estrito. `DD000017` e `DD000019` permanecem `unknown`, sem `last_access_tested_at`; `DD000016` e `DD000018` preservam estado testado. CI executa enriquecimento, correção duas vezes e ambos os validadores. | Teste vivo autenticado do Earth Engine não é executado no CI e continua explicitamente não afirmado. |

## Continuidade

A ocorrência não bloqueia o aprofundamento de TerraClass, PRODES ou DETER. Ela bloqueia apenas qualquer afirmação de disponibilidade operacional testada para endpoints sem evidência direta.
