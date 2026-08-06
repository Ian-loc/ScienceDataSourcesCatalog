# DETER Cerrado — classes de validação e fronteiras de crosswalk

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** I1-M2A  
**Produto candidato:** `PD-DETER-CER-ALERTS`

## Objetivo

Resolver o domínio de classes usado na auditoria especializada dos polígonos DETER Cerrado e impedir que classes de etapas distintas do fluxo sejam tratadas como equivalentes.

## Fonte

A metodologia INPE de 2024 apresenta:

- Tabela 2 — legenda operacional;
- Figuras 15 e 16 — interface e visualização da validação;
- Figura 17 — classes de validação do Sistema DETER.

DOI: `10.13140/RG.2.2.24196.49281`.

## Três domínios distintos

### 1. Classes operacionais por sensor

```text
Alerta_cb4
Alerta_amz1
Alerta_cba
```

Elas registram o satélite/imagem em que o alerta foi mapeado.

### 2. Classe operacional final

```text
Aviso
```

É a classe final apresentada na legenda operacional da edição metodológica.

### 3. Classes de validação

A auditoria por especialistas atribui uma entre cinco classes:

| Classe | Significado metodológico |
|---|---|
| `Alerta` | supressão total por corte raso e/ou alteração antrópica da estrutura da vegetação nativa |
| `Falso Positivo` | erro de inclusão em vegetação nativa sem distúrbio antrópico |
| `Resíduo` | supressão total detectável em imagens PRODES de anos anteriores |
| `Não Observado` | erro de inclusão associado a nuvem ou sombra de nuvem |
| `Sem condições de avaliação` | área com alta sazonalidade sem imagens adequadas suficientes para avaliação; a definição integral da fonte não foi recuperada |

O domínio está resolvido para a **edição metodológica de 2024**, não para o esquema físico da release ou do ativo atualmente distribuído.

## Fontes usadas na validação

A metodologia descreve comparação especializada com:

1. imagem-base do mapeamento, para avaliar falso positivo;
2. série histórica Landsat do PRODES Cerrado, para avaliar `Resíduo`;
3. mosaico Planet de alta resolução, para contexto da área;
4. série temporal NDVI MODIS apresentada como suporte contextual na interface.

Nenhuma dessas etapas foi convertida automaticamente em matriz de confusão ou estatística agregada de acurácia.

## Colisão terminológica: `Resíduo`

A classe de validação `Resíduo` significa que a supressão já era detectável em imagens PRODES de anos anteriores.

Ela não é automaticamente:

- produto anual de resíduo PRODES;
- distribuição;
- release;
- ativo;
- valor da classe `classname` do Shapefile DETER.

A coincidência lexical não estabelece identidade de entidade.

## Fronteiras de crosswalk

Não foram autorizados os seguintes mapeamentos:

```text
Aviso operacional → Alerta de validação
Alerta de validação → DESMATAMENTO_CR
Resíduo de validação → produto resíduo anual PRODES
classes da metodologia → domínio físico da release atual
classes de validação → valores públicos de classname
```

`Alerta` na validação é semanticamente mais amplo que a descrição específica de `DESMATAMENTO_CR`, pois inclui corte raso e/ou alteração antrópica da estrutura da vegetação. O crosswalk depende de evidência da release e do esquema efetivamente distribuído.

## Terceiro tipo da Tabela 2

A Tabela 2 lista como terceiro tipo:

- floresta plantada;
- agropecuária;
- áreas urbanas;
- mineração;
- represa.

A posição desses exemplos na coluna de tipos foi confirmada. Entretanto, seu papel como semântica positiva da classe final `Aviso` permanece ambíguo na extração textual. Esses contextos não foram tratados como classes de supressão de vegetação nativa e não podem ser mapeados para `DESMATAMENTO_CR`.

## Correções implementadas

Foram atualizados:

- `database/mappings/deter_cerrado_operational_legend_latency_guard_2026.json`;
- `scripts/validate_deter_cerrado_operational_legend_latency_guard.py`.

O gate agora verifica:

- domínio exato das cinco classes de validação;
- definições e fontes comparativas;
- separação entre classe operacional, final, validação e metadado;
- colisão terminológica de `Resíduo`;
- estado incompleto da definição de `Sem condições de avaliação`;
- ausência de crosswalk com release e bytes;
- manutenção de todos os gates negativos de promoção.

## Estado

Resolvido:

```text
validation_class_domain_resolved_for_method_edition = true
third_type_table_placement_resolved = true
```

Não resolvido:

```text
third_type_positive_alert_semantics_resolved = false
validation_class_domain_resolved_for_current_release = false
crosswalk_to_metadata_classname_resolved = false
crosswalk_to_release_schema_resolved = false
current_release_resolved = false
current_asset_verified = false
```

## Próxima ação

O crosswalk somente poderá avançar após inspeção de um esquema contemporâneo (`DescribeFeatureType` ou bytes do pacote), identificação da release e verificação de quais campos e valores de validação são efetivamente publicados.
