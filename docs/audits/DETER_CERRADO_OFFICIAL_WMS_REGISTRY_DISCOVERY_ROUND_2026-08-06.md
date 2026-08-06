# DETER Cerrado — descoberta no registro WMS oficial TerraBrasilis

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** I1-M2A  
**Entidade:** `PD-DETER-CER-ALERTS`

## Objetivo

Verificar se uma superfície operacional mantida pelo próprio projeto TerraBrasilis permite resolver o workspace e o nome da camada contemporânea do DETER Cerrado sem inferência por analogia.

## Fonte inspecionada

Foi inspecionado o repositório público:

`terrabrasilis/terrabrasilis_datasource`

O README descreve um plugin QGIS que oferece acesso às camadas WMS da Infraestrutura de Dados Espaciais TerraBrasilis. O plugin usa um registro de projetos, workspaces e camadas:

`data/geoserver_terrabrasilis_info.json`

A revisão observada corresponde ao commit:

`2f39a2e164d6a180aaf4559d93a162e2c6c56cf1`

Data do commit: **24 de abril de 2026**.

## Resultado

O registro atual contém workspaces e camadas de diferentes produtos, incluindo:

```text
workspace: prodes-cerrado-nb
produto: PRODES Cerrado
```

Entretanto, não foram localizados no arquivo:

- entrada textual DETER;
- workspace DETER Cerrado;
- camada DETER Cerrado;
- UUID corrente `e6e15388-4ca9-49b9-aec9-03891339a35e`.

O UUID antigo `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830` aparece no registro associado a metadado PRODES da Amazônia Legal, reforçando a reconciliação da deriva de referência publicada.

## Interpretação

A ausência do DETER Cerrado nesse arquivo significa somente:

> o plugin QGIS não expõe, neste registro WMS inspecionado, uma entrada DETER Cerrado que permita resolver o workspace ou a camada.

Ela **não demonstra**:

- inexistência de uma publicação no GeoServer;
- inexistência de camada WFS;
- inexistência de outro workspace não usado pelo plugin;
- indisponibilidade do Shapefile listado na página de downloads;
- ausência de distribuição ou ativo em outro canal.

O arquivo é um registro operacional do plugin WMS, não um `GetCapabilities` WFS completo nem um inventário integral do GeoServer.

## Fronteiras preservadas

```text
prodes-cerrado-nb ≠ workspace DETER Cerrado
registro WMS do plugin ≠ GetCapabilities WFS completo
ausência no registro ≠ inexistência do serviço
metadado GeoNetwork ≠ layer name
listing de download ≠ URL direta do ativo
```

O exemplo oficial `deter-amz:deter_public` permanece restrito ao DETER Amazônia e não foi reutilizado para o Cerrado.

## Correções implementadas

Foram atualizados:

- `database/mappings/deter_cerrado_endpoint_discovery_guard_2026.json`;
- `scripts/validate_deter_cerrado_endpoint_discovery_guard.py`.

O gate agora exige:

- SHA e data do registro oficial inspecionado;
- distinção entre registro WMS e catálogo completo do GeoServer;
- estado negativo para entrada DETER no registro;
- proibição de herdar `prodes-cerrado-nb`;
- proibição de interpretar ausência como inexistência;
- manutenção dos estados negativos de workspace, feature type, `DescribeFeatureType`, `GetFeature`, URL direta, release e ativo.

## Estado após a auditoria

Resolvido:

```text
official_qgis_wms_registry_inspected = true
deter_absent_from_official_qgis_wms_registry = true
registry_absence_interpreted_as_service_nonexistence = false
```

Não resolvido:

```text
specific_vector_workspace_resolved = false
specific_vector_feature_type_resolved = false
specific_describe_feature_type_verified = false
specific_get_feature_verified = false
direct_download_url_resolved = false
live_http_status_verified = false
current_release_resolved = false
asset_identity_resolved = false
```

## Próxima ação técnica

A descoberta específica somente poderá avançar mediante uma das seguintes evidências oficiais:

1. `GetCapabilities` vivo contendo workspace e feature type do Cerrado;
2. link de distribuição ou recurso de transferência do registro GeoNetwork atual;
3. URL direta do download com cadeia de redirecionamento e cabeçalhos verificáveis;
4. documentação oficial específica do serviço vetorial DETER Cerrado.

Até lá, a ausência operacional deve permanecer um estado negativo documentado, não uma lacuna preenchida por suposição.
