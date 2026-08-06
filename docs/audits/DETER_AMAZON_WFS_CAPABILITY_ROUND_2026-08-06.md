# Auditoria — capacidade WFS do DETER Amazônia

**Data/hora:** 6 de agosto de 2026, 01h21–01h31, `America/Sao_Paulo`  
**Família:** `PF000002 — DETER Amazônia`  
**Produto candidato:** `PD-DETER-AMZ-ALERTS`

## Objetivo

Resolver a natureza e os limites do canal WFS oficial usado para acesso aos alertas DETER Amazônia, sem converter serviço, workspace, camada ou exemplo de consulta em produto científico, release ou ativo inspecionado.

## Evidência oficial

A documentação TerraBrasilis descreve duas formas de obtenção dos dados PRODES e DETER: download direto de arquivos e serviço WFS. Para o DETER Amazônia, registra:

- endpoint-base `https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/wfs`;
- workspace `deter-amz`;
- operações `GetCapabilities`, `DescribeFeatureType` e `GetFeature`;
- feature type usado no exemplo: `deter_public`;
- WFS 2.0.0;
- `srsName=EPSG:4674`;
- exportação `SHAPE-ZIP`;
- filtro CQL pelo atributo `date`;
- alerta sobre diferenças de orientação dos eixos entre versões WFS.

O exemplo oficial usa o intervalo de 1º de janeiro a 1º de fevereiro de 2019. Esse intervalo demonstra a sintaxe de consulta e não define cobertura completa, release vigente ou período do produto.

A busca diária atual de metadados documenta parcialmente os campos `fid`, `class_name`, `area_km`, `view_date`, `create_date`, `audit_date`, `sensor`, `satellite`, `path_row` e `uuid`. Também informa que `fid` distingue tabelas corrente e histórica por `_curr` e `_hist`, e que a exportação Shapefile reduz nomes de colunas a dez caracteres, como `create_date` para `create_dat`.

## Tentativa operacional

Foram tentadas consultas de `GetCapabilities`, `DescribeFeatureType` e `GetFeature` com `resultType=hits` usando os clientes HTTP disponíveis nesta execução.

A tentativa não produziu resposta autoritativa utilizável:

- o cliente de execução local falhou instrumentalmente antes de retornar resposta HTTP do servidor;
- o cliente web recusou ou normalizou algumas URLs e uma tentativa de `DescribeFeatureType` resultou em `400 Bad Request` sem conteúdo suficiente para distinguir erro de parametrização, normalização do cliente ou estado do serviço.

Portanto:

```text
falha do cliente
≠ WFS indisponível
≠ WFS operacionalmente confirmado
```

O estado vivo permanece não resolvido.

## Decisão arquitetural

O WFS é registrado como **capacidade de acesso da fonte TerraBrasilis**. Ele não é:

- produto científico;
- release;
- distribuição individual resolvida;
- ativo baixado;
- substituto da identidade do Shapefile publicado.

A camada `deter_public` somente poderá ser vinculada a produto, release e distribuição após confirmação contemporânea de namespace, esquema, período e relação com as distribuições florestal e não florestal.

## Regras científicas e operacionais

1. O campo `date` do exemplo não deve ser tratado como data exata do evento sem definição contemporânea.
2. O esquema parcial do metadado não substitui `DescribeFeatureType` nem inspeção dos bytes.
3. Nomes truncados do Shapefile pertencem à distribuição e não substituem nomes canônicos de atributos.
4. A camada florestal não fornece automaticamente o esquema da distribuição não florestal.
5. O CRS documentado na consulta não comprova o CRS de todos os ativos sem resposta viva ou inspeção.
6. O serviço deve ser testado com consultas mínimas antes de qualquer estado `working` ou `unavailable`.

## Ocorrência

**ID:** `I1-20260806-044`  
**Categoria:** colapso entre capacidade WFS, camada, distribuição, ativo e release  
**Severidade:** `high` para promoção operacional  
**Estado:** `corrected`  
**Evidência:** documentação oficial de acesso WFS e metadados diários; tentativa viva inconclusiva por limitação instrumental.  
**Correção:** contrato e validador preservam o WFS como capacidade da fonte, registram esquema parcial e mantêm todos os estados vivos e de promoção negativos.  
**Teste:** `scripts/validate_deter_amazon_wfs_capability_guard.py`, encadeado ao gate DETER Amazônia.  
**Risco residual:** estado vivo, namespaces atuais, camada não florestal, esquema canônico, respostas HTTP, CRS, geometria, licença e vínculo com release permanecem pendentes.

## Resultado

A unidade avançou de “WFS mencionado genericamente” para capacidade formalmente modelada e auditável, sem afirmar disponibilidade não comprovada. O próximo avanço válido requer resposta viva datada de `GetCapabilities`, `DescribeFeatureType` e uma consulta mínima de `GetFeature`.
