# DETER Cerrado — perfil metodológico específico de 2024

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** `I1-M2A-DETER-CERRADO`  
**Estado:** método documentado; release e métricas quantitativas de qualidade não resolvidas

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

A edição metodológica documenta:

| Satélite | Sensor | Resolução nominal |
|---|---|---:|
| Amazônia-1 | WFI | 64 m |
| CBERS-4A | WFI | 55 m |
| CBERS-4 | AWFI | 64 m |

Também registra:

- faixa nominal de resolução de 55–64 m;
- revisita aproximada de cinco dias;
- área mínima detectável de aviso igual ou superior a 3 ha;
- cobertura diária de uma ou mais faixas do Cerrado, sustentando monitoramento contínuo.

O limiar de 3 ha não foi convertido em garantia de detecção completa. A resolução do sensor não foi confundida com escala de digitalização ou tamanho do polígono.

## 4. Método de mapeamento

- fotointerpretação manual;
- digitalização manual de polígonos;
- escala de digitalização 1:100.000;
- elementos de interpretação: tonalidade, cor, forma, textura e contexto;
- uso de séries multitemporais Landsat e CBERS como apoio;
- legenda operacional padronizada.

A legenda completa ainda não foi extraída para o contrato. A escala 1:100.000 permanece escala de digitalização, não resolução do sensor.

## 5. Semântica temporal

- a data atribuída ao aviso é a data de aquisição da imagem usada na detecção;
- essa data não é necessariamente a data real do evento;
- a data real pode ser desconhecida;
- a publicação pública é diária, à noite, com dados validados do dia anterior;
- instituições de fiscalização recebem acesso controlado em tempo real conforme os avisos são produzidos;
- consolidações mensais são publicadas após o término do mês;
- consolidação mensal não equivale a taxa mensal.

## 6. Comparabilidade temporal

A metodologia desaconselha:

- comparar meses consecutivos sem controle de disponibilidade de imagens;
- comparar automaticamente o mesmo mês entre anos.

Quando necessária, a comparação deve:

- usar o mesmo intervalo em anos diferentes;
- considerar no mínimo três meses;
- preservar cautela;
- considerar variabilidade de imagens, nuvens e oportunidade de observação.

## 7. Validação

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

## 8. Linha do tempo sem colapso

Diferentes fontes registram eventos distintos:

- 2018 — criação/início operacional ou início da série/distribuição, segundo página atual do programa e metadados;
- 2019 — lançamento do sistema, segundo a metodologia de 2024.

Esses anos não foram tratados como respostas concorrentes para a mesma pergunta. Permanecem como eventos distintos até que documentação institucional mais específica permita reconstruir a cronologia completa.

## 9. Divergência de contexto documental

O registro específico de metadados declara “Landsat ou similares”, enquanto a metodologia de 2024 descreve WFI/AWFI em Amazônia-1 e CBERS.

Disposição:

- preservar ambas as afirmações com fonte e data;
- não substituir silenciosamente o texto do metadado;
- usar a metodologia de 2024 como perfil metodológico resolvido para essa edição;
- não usar a metodologia como prova da release ou do ativo vigente;
- investigar se o metadado mantém descrição histórica/genérica ou se existe atualização ainda não reconciliada.

## 10. Artefatos

Criados:

- `database/mappings/deter_cerrado_method_profile_guard_2026.json`;
- `scripts/validate_deter_cerrado_method_profile_guard.py`.

Atualizado:

- `scripts/validate_deter_cerrado_scientific_boundary_guard.py`.

## 11. Estados preservados

Resolvido no nível da metodologia de 2024:

- propósito;
- sensores e resolução nominal;
- limiar;
- fotointerpretação e digitalização;
- semântica temporal;
- orientação de comparação;
- processo de validação;
- latência pública e acesso antecipado controlado.

Não resolvido:

- release vigente;
- vinculação da release atual à edição metodológica;
- legenda operacional completa;
- métricas quantitativas de acurácia;
- classes de validação completas;
- confirmação da história atual de sensores nos bytes;
- endpoints, ativos e pacotes.

## 12. Próxima ação

1. extrair a legenda operacional do DETER Cerrado e as classes de validação sem extrapolar para a release atual;
2. localizar métricas ou resultados de acurácia aplicáveis;
3. resolver workspace/layer WFS e URL direta;
4. inspecionar bytes e pacote;
5. reconciliar cronologia 2018/2019 e metadado Landsat versus método WFI/AWFI;
6. manter a promoção bloqueada até a identidade da release e do ativo estar resolvida.
