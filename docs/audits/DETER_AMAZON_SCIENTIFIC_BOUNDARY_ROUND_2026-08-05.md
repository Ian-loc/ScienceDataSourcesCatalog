# Auditoria — fronteira científica inicial do DETER Amazônia

**Data/hora:** 5 de agosto de 2026, 23h22–23h31, `America/Sao_Paulo`  
**Família:** `PF000002` — DETER Amazônia  
**Produto científico candidato:** `PD-DETER-AMZ-ALERTS`

## Objetivo

Estabelecer a fronteira científica mínima do produto de alertas DETER Amazônia antes de resolver release, distribuição ou ativo. O foco é impedir que avisos operacionais sejam tratados como taxa mensal, inventário anual completo, release PRODES ou produto indiferenciado de outros recortes DETER.

## Evidência oficial examinada

### Perfil atual BiomasBR

A página oficial atual apresenta o DETER como sistema de monitoramento diário por sensoriamento remoto que indica locais com evidências de supressão ou degradação da cobertura nativa. Para a Amazônia Legal, os dados são alertas ou avisos voltados ao apoio à fiscalização e ao controle ambiental.

O perfil atualmente publicado informa uso de imagens dos satélites Amazônia-1, CBERS-4 e CBERS-4A, sensor WFI, e mapeamento de alertas com área mínima de 3 hectares.

### Perfil histórico DETER-B

A página institucional atualizada em 30 de dezembro de 2021 descreve o DETER-B como sistema em tempo quase real, utilizando CBERS-4/WFI e IRS/AWiFS, com resoluções nominais de 64 m e 56 m.

Esse perfil documenta:

- envio ao IBAMA sem restrição de área mínima mapeada;
- disponibilização pública histórica de polígonos a partir de 6,25 ha;
- diferença histórica de cinco dias entre detecção e publicação;
- interpretação visual baseada em cor, tonalidade, textura, forma e contexto;
- uso do Modelo Linear de Mistura Espectral;
- classes de desmatamento, degradação e exploração madeireira.

## Achado principal — perfis operacionais não podem ser colapsados

Os dois perfis oficiais registram configurações distintas:

```text
perfil histórico DETER-B
sensores WFI/AWiFS
64 m / 56 m
limiar público 6,25 ha
latência pública de cinco dias

≠

perfil atual BiomasBR
Amazônia-1 e CBERS-4/4A WFI
área mínima declarada de 3 ha
release e latência atuais ainda não resolvidas
```

A divergência não deve ser interpretada como erro. Ela evidencia transição operacional e exige registro datado por perfil, produto e release.

## Fronteira alerta × taxa

O produtor afirma explicitamente que o DETER é um sistema expedito de alerta para priorização da fiscalização. A informação de área não deve ser entendida como taxa mensal de desmatamento.

O número oficial anual é fornecido pelo PRODES.

Portanto:

```text
alerta DETER
≠ taxa mensal
≠ taxa anual PRODES
≠ inventário anual completo
```

## Fronteira temporal

Nuvens, resolução e disponibilidade de imagens afetam a oportunidade de detecção. Um alerta detectado em determinado mês pode corresponder a processo iniciado anteriormente.

Logo:

```text
data de detecção
≠ data exata da ocorrência
```

A comparação direta entre meses não deve ser promovida como se a detectabilidade fosse constante.

## Classes documentadas

A documentação histórica organiza as classes em dois níveis.

Nível 1:

- `DESMATAMENTO (ALERTAS)`;
- `DEGRADAÇÃO`;
- `EXPLORAÇÃO MADEIREIRA`.

Nível 2:

- Desmatamento com solo exposto;
- Desmatamento com vegetação;
- Mineração;
- Degradação;
- Cicatriz de incêndio florestal;
- Corte Seletivo Tipo 1 (Desordenado);
- Corte Seletivo Tipo 2 (Geométrico).

O domínio integral da release atual ainda depende de documentação contemporânea específica e inspeção dos bytes.

## Decisão curatorial

A unidade foi classificada como candidato a produto operacional de alertas:

`PD-DETER-AMZ-ALERTS`

Permanecem não resolvidos:

- release ou snapshot atual;
- distribuição individual vigente;
- endpoint direto;
- bytes e checksum;
- CRS, geometria e esquema integral;
- domínio completo de classes atual;
- resolução, suporte e área mínima por release;
- latência pública vigente;
- validação, qualidade, incerteza e vieses;
- licença, atribuição e citação da release.

## Ocorrência

**ID:** `I1-20260805-042`  
**Categoria:** colapso entre alerta operacional, taxa e perfis históricos/atuais do DETER  
**Severidade:** `high` para promoção da unidade  
**Estado:** `corrected`  
**Correção:** contrato e validador preservam alerta versus taxa, data de detecção versus ocorrência e dois perfis operacionais datados, impedindo herança automática de sensores, resolução, limiar e latência.  
**Risco residual:** produto, release, distribuição, endpoint, bytes e perfis completos ainda não foram resolvidos.

## Artefatos

- `database/mappings/deter_amazon_scientific_boundary_guard_2026.json`;
- `scripts/validate_deter_amazon_scientific_boundary_guard.py`;
- integração ao workflow de validação da Instância 1.

## Resultado

A família DETER Amazônia deixa de ser apenas uma linha legada genérica e passa a possuir fronteira científica verificável. Nenhuma promoção foi autorizada. A próxima unidade deve resolver a distribuição oficial atual de alertas Amazônia e seu metadado individual, preservando a separação entre configuração histórica e release vigente.
