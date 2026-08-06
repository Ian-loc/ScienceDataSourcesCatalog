# DETER Cerrado — perfil metodológico específico de 2024

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** `I1-M2A-DETER-CERRADO`  
**Estado:** método e legenda operacional documentados; release e métricas quantitativas de qualidade não resolvidas

## 1. Documento metodológico

Foi individualizada a edição:

- **Título:** *Metodologia dos sistemas PRODES e DETER para o bioma Cerrado*;
- **Produtor:** Instituto Nacional de Pesquisas Espaciais — INPE;
- **Ano:** 2024;
- **Atualização declarada:** 28 de março de 2024;
- **DOI:** `10.13140/RG.2.2.24196.49281`;
- **Natureza:** documento técnico de metodologia.

O documento resolve um perfil metodológico datado. Ele não constitui identificador da release vigente, do arquivo, da camada WFS ou dos bytes atualmente distribuídos.

Uma síntese científica posterior, publicada por autores do INPE em 2025, cita explicitamente essa metodologia e confirma o papel do DETER como sistema de interpretação visual, atualização diária e apoio à fiscalização.

## 2. Fronteira científica

O DETER Cerrado:

- mapeia expedita e diariamente evidências de supressão total e alteração da estrutura da vegetação nativa;
- produz avisos para fiscalização ambiental;
- não é proxy do PRODES;
- não produz taxa mensal de desmatamento;
- não constitui inventário anual completo;
- não deve ser usado para quantificar com precisão a área anual suprimida;
- remete ao PRODES Cerrado como fonte oficial da quantificação anual precisa.

## 3. Sensores, resolução e limiar

| Satélite | Sensor | Resolução nominal |
|---|---|---:|
| Amazônia-1 | WFI | 64 m |
| CBERS-4A | WFI | 55 m |
| CBERS-4 | AWFI | 64 m |

Também estão documentados:

- faixa nominal de resolução de 55–64 m;
- revisita aproximada de cinco dias;
- área mínima detectável de aviso igual ou superior a 3 ha;
- cobertura diária de uma ou mais faixas do Cerrado.

O limiar de 3 ha não foi convertido em garantia de detecção completa. A resolução do sensor não foi confundida com escala de digitalização ou tamanho do polígono.

## 4. Método de mapeamento

- fotointerpretação manual;
- digitalização manual de polígonos;
- escala de digitalização 1:100.000;
- elementos de interpretação: tonalidade, cor, forma, textura e contexto;
- uso de séries multitemporais Landsat e CBERS como apoio;
- legenda operacional padronizada.

A escala 1:100.000 permanece escala de digitalização, não resolução do sensor.

## 5. Legenda operacional

A Tabela 2 da metodologia registra classes por satélite:

- `Alerta_cb4` — aviso mapeado em imagem CBERS-4;
- `Alerta_amz1` — aviso mapeado em imagem Amazônia-1;
- `Alerta_cba` — aviso mapeado em imagem CBERS-4A;
- classe final: `Aviso`.

A mesma tabela registra tipos relacionados a:

- corte raso;
- alteração recorrente da estrutura vegetal;
- contextos antropizados ou outros exemplos documentados;
- queimada de origem antrópica.

Disposição:

- as classes por satélite são classes operacionais, não releases;
- `Aviso` não foi mapeado automaticamente para `DESMATAMENTO_CR`;
- a legenda operacional não substitui classes de validação;
- o papel exato do terceiro tipo permanece não resolvido;
- o crosswalk com o esquema da release vigente permanece pendente.

O detalhamento está no contrato `deter_cerrado_operational_legend_latency_guard_2026.json`.

## 6. Padrões de interpretação

A metodologia ilustra padrões como:

- remoção completa e abrupta com solo exposto e limites claros;
- remoção em superfícies acidentadas;
- incorporação de fragmentos remanescentes a áreas já abertas;
- remoção em topos de planalto;
- remoção gradativa com textura e tonalidade heterogêneas.

Também diferencia queimada antrópica e fogo natural por cor, tonalidade, textura, forma e contexto.

Esses padrões são auxiliares de fotointerpretação especializada; não foram convertidos em regras determinísticas de classificação.

## 7. Semântica temporal e latência

- a data atribuída ao aviso é a data de aquisição da imagem usada na detecção;
- essa data não é necessariamente a data real do evento;
- a data real pode ser desconhecida;
- a publicação pública é diária, à noite, com dados validados;
- o fluxo entre passagem do satélite e inserção do aviso auditado no banco leva tipicamente 48–72 horas;
- a faixa de 48–72 horas pode variar com calendário e trabalho da equipe e não constitui SLA universal;
- instituições de fiscalização recebem acesso controlado conforme os avisos são produzidos;
- consolidações mensais são publicadas após o término do mês;
- consolidação mensal não equivale a taxa mensal.

As afirmações sobre atualização noturna, latência do processamento e acesso antecipado controlado foram preservadas como dimensões distintas.

## 8. Máscara do ciclo DETER

Os avisos diários formam uma máscara de áreas que deixam de ser reinspecionadas no ciclo de observação corrente. Os polígonos permanecem nessa máscara até o fim do ciclo.

Avisos DETER não confirmados pelo PRODES podem voltar a ser analisados no mapeamento seguinte.

A máscara:

- não é classe permanente de cobertura da terra;
- não é máscara acumulada PRODES;
- não prova falso positivo apenas pela ausência de confirmação PRODES.

## 9. Comparabilidade temporal

A metodologia desaconselha:

- comparar meses consecutivos sem controle de disponibilidade de imagens;
- comparar automaticamente o mesmo mês entre anos.

Quando necessária, a comparação deve:

- usar o mesmo intervalo em anos diferentes;
- considerar no mínimo três meses;
- preservar cautela;
- considerar variabilidade de imagens, nuvens e oportunidade de observação.

## 10. Validação

O documento informa que:

- todos os polígonos são validados;
- avisos validados são enviados diariamente ao IBAMA;
- a validação busca calcular estatísticas de acurácia, eliminar erros/falsos alertas e identificar melhorias;
- existe plataforma específica de validação.

Ainda não foram promovidos:

- valores de acurácia;
- matriz de confusão;
- domínio completo das classes de validação;
- métricas atuais por release.

## 11. Linha do tempo sem colapso

Diferentes fontes registram eventos distintos:

- 2018 — criação/início operacional ou início da série/distribuição;
- 2019 — lançamento do sistema, segundo a metodologia de 2024.

Esses anos foram preservados como eventos distintos até que documentação institucional mais específica permita reconstruir a cronologia completa.

## 12. Divergência de contexto documental

O registro específico declara “Landsat ou similares”, enquanto a metodologia de 2024 descreve WFI/AWFI em Amazônia-1 e CBERS.

Disposição:

- preservar ambas as afirmações com fonte e data;
- não substituir silenciosamente o texto do metadado;
- usar a metodologia de 2024 como perfil metodológico resolvido para essa edição;
- não usar a metodologia como prova da release ou do ativo vigente;
- investigar se o metadado mantém descrição histórica/genérica ou se existe atualização ainda não reconciliada.

## 13. Artefatos

Criados:

- `database/mappings/deter_cerrado_method_profile_guard_2026.json`;
- `scripts/validate_deter_cerrado_method_profile_guard.py`;
- `database/mappings/deter_cerrado_operational_legend_latency_guard_2026.json`;
- `scripts/validate_deter_cerrado_operational_legend_latency_guard.py`.

Atualizado:

- `scripts/validate_deter_cerrado_scientific_boundary_guard.py`.

## 14. Estados preservados

Resolvido no nível da metodologia de 2024:

- propósito;
- sensores e resolução nominal;
- limiar;
- fotointerpretação e digitalização;
- legenda operacional;
- padrões de interpretação;
- latência típica;
- máscara de ciclo;
- semântica temporal;
- orientação de comparação;
- processo de validação;
- publicação pública e acesso antecipado controlado.

Não resolvido:

- release vigente;
- vinculação da release atual à edição metodológica;
- crosswalk da legenda operacional com `classname` e classes de validação;
- papel exato do terceiro tipo da Tabela 2;
- métricas quantitativas de acurácia;
- classes de validação completas;
- confirmação da história atual de sensores nos bytes;
- endpoints, ativos e pacotes.

## 15. Próxima ação

1. extrair as classes de validação sem extrapolar para a release atual;
2. localizar métricas ou resultados de acurácia aplicáveis;
3. resolver workspace/layer WFS e URL direta;
4. inspecionar bytes e pacote;
5. reconciliar cronologia 2018/2019 e metadado Landsat versus método WFI/AWFI;
6. manter a promoção bloqueada até a identidade da release e do ativo estar resolvida.
