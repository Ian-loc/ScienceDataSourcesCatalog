# Auditoria — reconciliação operacional normalizada do Dynamic World V1

**Data:** 2026-08-05 13:30 America/Sao_Paulo  
**PR:** #54  
**Branch:** `agent/consolidate-instance-1-relational-catalog`

## Objetivo

Materializar no catálogo relacional o contrato operacional já auditado do Dynamic World V1, sem confundir página de catálogo, ativo lógico, visualizador, registro secundário de metadados e repositório de software.

## Resultado material

Foi criado `scripts/enrich_instance1_dynamic_world_operational.py`, que reconcilia idempotentemente:

- quatro distribuições com papéis distintos;
- o ativo canônico `AS-DW-EE-V1` com identificador `GOOGLE/DYNAMICWORLD/V1` separado da URL do catálogo;
- quinze capacidades de acesso;
- licença CC BY 4.0 e atribuição do dataset;
- aviso dos dados Sentinel modificados;
- separação da licença Apache-2.0 do software;
- cinco afirmações operacionais com evidência;
- revisão curatorial `DP000011` em estado `reviewed`, sem autorização de promoção canônica.

Foi criado `scripts/validate_dynamic_world_normalized_operational.py` para validar distribuições, ativo, capacidades, afirmações, escores curatoriais e preservação do gate humano.

## Auditoria de delta

A primeira modelagem marcava como `working` e atribuía `last_access_tested_at` às quatro distribuições. A evidência disponível, entretanto, comprova teste operacional datado apenas para:

- `DD000016`: catálogo/asset Earth Engine com status oficial de ingestão;
- `DD000018`: visualizador explicitamente verificado.

Os registros `DD000017` e `DD000019` têm identidade e papel classificados, mas o contrato não documenta teste operacional equivalente. Para impedir que classificação fosse apresentada como disponibilidade testada, foram criados:

- `scripts/correct_dynamic_world_endpoint_test_states.py`;
- `scripts/validate_dynamic_world_endpoint_test_states.py`.

O pós-processamento mantém `DD000017` e `DD000019` em `access_status=unknown`, limpa `last_access_tested_at` e registra explicitamente que nenhum teste operacional direto é afirmado. A correção é idempotente e executada duas vezes no CI.

## Ocorrência

### I1-20260805-025

- **Categoria:** força da evidência operacional e proveniência;
- **Severidade:** `high`;
- **Estado:** `corrected`;
- **Descrição:** a implementação inicial extrapolava a classificação dos papéis de WRI e do repositório de software para uma afirmação de disponibilidade operacional testada;
- **Risco:** inflar a confiabilidade de endpoints e datas de teste sem evidência específica;
- **Correção:** separar `role classified` de `endpoint tested`, preservar `unknown` onde não houve teste direto e validar automaticamente a correspondência entre estado e timestamp;
- **Teste:** compilação Python, execução idempotente do enriquecimento e da correção, validador operacional normalizado e validador estrito de força da evidência;
- **Risco residual:** testes vivos autenticados do Earth Engine continuam fora do CI e não são afirmados.

## Gates preservados

- nenhuma promoção canônica;
- nenhum merge;
- nenhum deploy;
- nenhuma alteração da página pública;
- nenhuma afirmação de download direto anônimo;
- revisão `reviewed` não equivale a `approved` nem a autorização humana.

## Próxima unidade

1. confirmar CI integral no SHA final;
2. atualizar o validador transversal do piloto para incluir o ativo canônico e o estado `reviewed` do Dynamic World;
3. avançar para inspeção do ativo específico TerraClass Amazônia 2020;
4. se o ativo permanecer indisponível, retomar a resolução de endpoints PRODES e iniciar DETER em paralelo seguro.
