# DETER Cerrado — fronteira de qualidade, proximidade operacional e validação quantitativa

**Data:** 6 de agosto de 2026  
**Horários de referência:** 08:18–08:27 e 11:05–11:18, `America/Sao_Paulo`  
**Pacote:** I1-M2A  
**Produto candidato:** `PD-DETER-CER-ALERTS`

## Objetivo

Distinguir três dimensões que não devem ser colapsadas:

1. controles metodológicos e operacionais do sistema;
2. evidência quantitativa de utilidade ou proximidade operacional;
3. avaliação de acurácia, erro e incerteza vinculada a uma release.

## Evidências consultadas

### Fontes institucionais

1. Página oficial DETER do Programa BiomasBR: finalidade operacional, sensores, área mínima geral de 3 ha e distinção entre alerta e inventário anual.
2. Página institucional do BiomasBR: metodologias adaptadas às características de cada bioma.
3. Página histórica DETER da OBT/INPE: referência a validação publicada para o DETER Amazônia, sem transferência ao Cerrado.

### Evidência revisada por pares

Pinheiro et al. (2023), DOI `10.1080/25726838.2023.2265242`, apresenta a metodologia e resultados do DETER Cerrado.

O estudo relata:

- capacidade de detectar uma variedade de tamanhos de supressão, incluindo áreas maiores que 1 ha e menores que 10 ha;
- **80% do desmatamento posteriormente detectado pelo PRODES concentrado em uma zona de 10 km dos alertas DETER**;
- utilidade do sistema para apoiar a fiscalização no Cerrado.

## Interpretação correta do resultado de 80% em 10 km

O resultado é uma evidência quantitativa de **proximidade espacial e utilidade operacional**.

Ele não é, por si só:

- precisão;
- revocação ou sensibilidade;
- especificidade;
- erro de omissão;
- erro de comissão;
- matriz de confusão;
- acurácia ajustada por área;
- incerteza da geometria;
- validação da release atualmente distribuída.

O denominador reportado é o desmatamento posteriormente identificado pelo PRODES, e a relação é definida por um buffer de 10 km. Portanto, proximidade espacial não equivale a coincidência geométrica entre alertas e polígonos anuais.

O PRODES é o inventário anual oficial usado como referência posterior no estudo; não foi reinterpretado como verdade de campo universal para todas as feições ou semânticas do DETER.

## O que continua não localizado

Não foi localizada avaliação específica contendo:

- matriz de confusão DETER Cerrado;
- precisão ou revocação;
- erros de omissão e comissão;
- desenho amostral integral;
- acurácia ajustada por área;
- incerteza quantitativa dos alertas;
- vínculo inequívoco entre essas métricas e a release vigente.

Esse estado não demonstra inexistência de avaliação. Significa apenas que a acurácia aplicável ao produto/release não foi resolvida com evidência suficiente.

## Fronteiras preservadas

- evidência de proximidade operacional não é acurácia;
- métricas históricas do DETER Amazônia não são herdadas pelo DETER Cerrado;
- métricas de acurácia do PRODES não são herdadas pelo DETER;
- limiar de 3 ha não é probabilidade de detecção nem garantia de completude;
- fotointerpretação manual não equivale a verdade de campo;
- latência de 48–72 horas não é acurácia;
- janela comparativa mínima de três meses não é desenho de validação;
- ausência de incerteza documentada não é ausência de incerteza.

## Artefatos atualizados

- `database/mappings/deter_cerrado_quality_validation_guard_2026.json`;
- `scripts/validate_deter_cerrado_quality_validation_guard.py`;
- integração mantida no gate agregado `validate_deter_cerrado_scientific_boundary_guard.py`.

## Decisão curatorial

Resolvido:

```text
quality_framework_documented = true
cerrado_specific_operational_proximity_evidence_resolved = true
reported_proximity_percentage = 80
reported_buffer_radius_km = 10
```

Não resolvido:

```text
cerrado_specific_quantitative_accuracy_resolved = false
current_release_validation_resolved = false
current_release_uncertainty_resolved = false
quality_profile_complete = false
```

A promoção permanece bloqueada até que a avaliação de acurácia seja vinculada à edição correta ou que essa limitação seja formalmente aceita após busca final auditada e revisão curatorial.
