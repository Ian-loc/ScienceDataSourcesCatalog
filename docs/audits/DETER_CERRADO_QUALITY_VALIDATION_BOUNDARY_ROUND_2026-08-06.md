# DETER Cerrado — fronteira de qualidade e validação quantitativa

**Data:** 6 de agosto de 2026  
**Horário de referência:** 08:18–08:27, `America/Sao_Paulo`  
**Pacote:** I1-M2A  
**Produto candidato:** `PD-DETER-CER-ALERTS`

## Objetivo

Verificar se as fontes oficiais recuperadas permitem registrar métricas quantitativas de qualidade, acurácia ou incerteza específicas do DETER Cerrado e da release atualmente distribuída.

## Evidências consultadas

1. Página oficial DETER do Programa BiomasBR: finalidade operacional, sensores atuais, área mínima geral de 3 ha, classes e orientação de citação.
2. Página institucional do BiomasBR: metodologias adaptadas às características de cada bioma.
3. Página histórica DETER da OBT/INPE: referência a estatísticas de validação publicadas para o DETER Amazônia.
4. Documentação técnica TerraBrasilis WFS: exemplos operacionais exclusivamente associados ao workspace `deter-amz`.

## Resultado

Não foi localizada, no conjunto oficial recuperado nesta rodada, avaliação quantitativa inequivocamente específica do DETER Cerrado contendo matriz de confusão, precisão, revocação, erros de omissão/comissão, acurácia ajustada por área ou protocolo de validação vinculado à release vigente.

Esse resultado não demonstra inexistência de avaliação. Demonstra somente que métricas aplicáveis ao produto/release não foram resolvidas com evidência suficiente.

## Fronteiras preservadas

- métricas históricas do DETER Amazônia não são herdadas pelo DETER Cerrado;
- métricas de acurácia do PRODES não são herdadas pelo DETER;
- limiar de 3 ha não é probabilidade de detecção nem garantia de completude;
- fotointerpretação manual não equivale a verdade de campo;
- latência de 48–72 horas não é acurácia;
- janela comparativa mínima de três meses não é desenho de validação;
- ausência de incerteza documentada não é ausência de incerteza.

## Limitações registradas

- avisos abaixo do limiar operacional podem não ser mapeados;
- nuvens e condições de observação podem retardar a detecção;
- a data da imagem não representa necessariamente a data exata da supressão;
- o sistema prioriza resposta operacional e não substitui o inventário anual PRODES;
- comparações curtas podem refletir disponibilidade de imagens e latência;
- qualidade quantitativa e incerteza da release permanecem não resolvidas.

## Artefatos

- `database/mappings/deter_cerrado_quality_validation_guard_2026.json`;
- `scripts/validate_deter_cerrado_quality_validation_guard.py`;
- integração no gate agregado `validate_deter_cerrado_scientific_boundary_guard.py`.

## Decisão curatorial

`quality_framework_documented = true`

`cerrado_specific_quantitative_accuracy_resolved = false`

`current_release_validation_resolved = false`

`current_release_uncertainty_resolved = false`

`quality_profile_complete = false`

A promoção permanece bloqueada até que uma avaliação específica seja vinculada à edição correta ou que a ausência documental seja formalmente aceita como limitação após busca final auditada.
