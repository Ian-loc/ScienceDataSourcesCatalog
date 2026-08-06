# Auditoria — camadas cartográficas auxiliares PRODES Amazônia

**Data/hora:** 2026-08-05 22:00–22:15, `America/Sao_Paulo`  
**Família:** `PF000001`  
**Pacote relacionado:** `PRODES-ASSET-AMAZON-GEOPACKAGE`

## Unidades auditadas

| Unidade | Resolução curatorial | UUID de metadado |
|---|---|---|
| Hidrografia | produto cartográfico auxiliar candidato `PD-PRODES-AMZ-HYDROGRAPHY` | `1df78632-68e7-4e91-bca0-25305d3f831e` |
| Hidrografia em não floresta | produto cartográfico auxiliar candidato `PD-PRODES-AMZ-NON-FOREST-HYDROGRAPHY` | `87fb6a32-01c1-4421-b7d0-a93568e1b079` |
| Máscara de não floresta | entidade auxiliar de domínio `AX-PRODES-AMZ-NON-FOREST-DOMAIN-MASK`; produto autônomo não sustentado | `bed1276c-aa3d-4f5b-b560-1879617ef13d` |

## Objetivo

Preservar a identidade de três componentes cartográficos auxiliares do PRODES Amazônia, evitando que sejam normalizados como supressão de vegetação, incrementos, taxas, resíduos, incerteza ou produtos autônomos sem evidência suficiente.

## Evidência oficial examinada

1. O catálogo TerraBrasilis descreve a hidrografia como mapeamento anual de corpos hídricos — rios, lagos, barramentos e represamentos — e registra ajuste aos limites de biomas publicados pelo IBGE em 2019.
2. O metadado da hidrografia geral documenta `main_class=HIDROGRAFIA` e `class_name=HIDROGRAFIA`, além de uma lista padronizada de atributos preenchidos apenas quando aplicáveis.
3. A hidrografia em não floresta é descrita separadamente como corpos hídricos situados no domínio não florestal do bioma Amazônia.
4. O contexto oficial do programa não florestal registra operação sistemática a partir de 2023 e objetivo de série histórica desde 2000. Essas datas pertencem ao programa de monitoramento de supressão e não podem ser promovidas automaticamente como release ou série temporal do ativo hidrográfico.
5. A documentação da hidrografia em não floresta referencia explicitamente a máscara de não floresta por UUID próprio.
6. A máscara de não floresta é definida como tipologias de vegetação que não se enquadram na classe de Floresta adotada no mapeamento. As classes documentadas são `NAO_FLORESTA` e `NAO_FLORESTA2`.
7. A página geral do PRODES apresenta Hidrografia e Não Floresta como classes ou camadas específicas no produto completo, separadas de desmatamento anual e resíduos.
8. O catálogo de downloads lista as três distribuições Shapefile separadamente. A data exibida na interface não constitui release científica nem comprova identidade dos bytes.

## Decisões científicas e curatoriais

### Hidrografia geral

É candidata a produto cartográfico auxiliar de corpos hídricos. A cadência anual declarada não transforma a camada em incremento anual nem comprova uma release vigente específica.

```text
hidrografia
≠ supressão
≠ incremento
≠ taxa
≠ resíduo
≠ máscara acumulada
```

### Hidrografia em não floresta

É candidata a produto auxiliar próprio dentro do domínio não florestal. Não deve ser colapsada na hidrografia geral porque possui recorte ecológico e relação explícita com a máscara de não floresta. Também não deve herdar automaticamente toda a história de sensores, cadência e método do produto de supressão não florestal.

```text
hidrografia geral
≠ hidrografia em não floresta
```

### Máscara de não floresta

A evidência disponível sustenta **entidade auxiliar de domínio e classificação**, não produto científico autônomo. Essa decisão é coerente com o guard específico `prodes_amazon_non_forest_mask_entity_guard_2026.json`.

A máscara não representa supressão ocorrida, ausência de vegetação, ausência de dados nem área acumulada de desmatamento.

```text
não floresta
= classe auxiliar relativa à definição de Floresta adotada no mapeamento
≠ produto autônomo já resolvido
≠ área sem vegetação
≠ dado ausente
≠ supressão
```

Uma futura promoção como produto exigiria evidência adicional de identidade científica autônoma, release, método, finalidade e citação próprios. Até lá, a unidade permanece `AX-PRODES-AMZ-NON-FOREST-DOMAIN-MASK`.

### Campos padronizados

A lista de atributos é padronizada com o dado principal do PRODES, mas a documentação afirma que, para outras classes, os campos são preenchidos somente quando aplicáveis. Assim:

- a presença de um campo no metadado não comprova valores não nulos nos bytes;
- `year`, `publish_year` e `pub_date` não constituem release;
- `uid` não deve ser chave persistente;
- `uuid` de feição não é UUID de metadado;
- sensores e datas de imagem não podem ser promovidos sem inspeção do ativo específico.

## Estados preservados como não resolvidos

Para as três unidades permanecem pendentes:

- papel final no nível de entidade ou produto;
- release vigente e política de revisão;
- método específico da camada;
- endpoint direto e cadeia de redirecionamentos;
- bytes, nome, tamanho e checksum;
- inventário do pacote Shapefile;
- CRS, geometria, cobertura e esquema integral;
- valores efetivamente presentes, nulos e domínios;
- qualidade, validação, incerteza, vieses e limitações;
- licença, atribuição e citação aplicáveis.

## Ocorrência

**ID:** `I1-20260805-039`  
**Categoria:** colapso de camadas auxiliares em produtos de supressão e herança indevida entre domínios  
**Severidade:** `high` para promoção das unidades  
**Estado:** `corrected`

**Evidência:** metadados oficiais distinguem hidrografia geral, hidrografia em não floresta e máscara de não floresta, com objetos, classes e recortes próprios; a ocorrência `I1-20260805-038` já protege especificamente a máscara como entidade auxiliar, não produto autônomo.  
**Correção:** contrato e validador transversal preservam três identidades, reutilizam a resolução auxiliar da máscara, proíbem interpretações de supressão e bloqueiam herança automática de temporalidade, sensores, classes e release.  
**Teste:** `scripts/validate_prodes_amazon_ancillary_layers_guard.py`, complementado por `validate_prodes_amazon_non_forest_mask_entity_guard.py` e integrado ao gate agregado do GeoPackage PRODES Amazônia.  
**Risco residual:** releases, métodos específicos, endpoints, bytes, perfis completos, licenças e citações ainda não foram resolvidos.

## Artefatos

- `database/mappings/prodes_amazon_ancillary_layers_guard_2026.json`;
- `scripts/validate_prodes_amazon_ancillary_layers_guard.py`;
- `database/mappings/prodes_amazon_non_forest_mask_entity_guard_2026.json`;
- `scripts/validate_prodes_amazon_non_forest_mask_entity_guard.py`;
- integração em `scripts/validate_prodes_amazon_geopackage_composition_guard.py`.

## Resultado

Os dez componentes declarados do GeoPackage PRODES Amazônia agora possuem fronteiras protegidas por gates especializados ou por contratos operacionais prévios. Este resultado não equivale à conclusão de produtos ou ativos: os endpoints e bytes continuam não resolvidos e nenhuma promoção foi autorizada.
