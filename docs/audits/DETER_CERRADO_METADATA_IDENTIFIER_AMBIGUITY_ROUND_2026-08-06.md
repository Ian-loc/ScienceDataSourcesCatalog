# DETER Cerrado — reconciliação do identificador de metadado

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** I1-M2A  
**Entidade:** `PD-DETER-CER-ALERTS`

## Achado inicial

O UUID `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830` aparecia em dois contextos oficiais incompatíveis:

1. na orientação de citação publicada pelo BiomasBR para o Shapefile DETER Cerrado desde 2018;
2. no catálogo TerraBrasilis como metadado do componente **Incrementos no desmatamento** do PRODES Amazônia Legal.

O identificador não poderia, portanto, sustentar sozinho a identidade corrente do registro DETER Cerrado.

## Evidência nova e reconciliação

A página oficial de busca do GeoNetwork para recursos vetoriais expõe o registro:

> **Avisos de supressão da vegetação nativa no Cerrado à partir de 2018**

O link desse resultado aponta para:

`e6e15388-4ca9-49b9-aec9-03891339a35e`

A referência é corroborada pela declaração de disponibilidade de dados do artigo metodológico de Pinheiro et al. (2023), DOI `10.1080/25726838.2023.2265242`, que identifica os dados DETER Cerrado no TerraBrasilis pelo mesmo número.

Ao mesmo tempo, o catálogo oficial de GeoPackages e a orientação de citação do PRODES associam `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830` ao incremento PRODES da Amazônia Legal.

## Decisão curatorial

A divergência foi classificada como:

`published_citation_reference_drift`

A partir desta rodada:

- `e6e15388-4ca9-49b9-aec9-03891339a35e` é o identificador do **registro GeoNetwork corrente** do DETER Cerrado;
- `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830` é preservado como referência histórica da orientação de citação publicada e como referência observada do componente PRODES Amazônia Legal;
- nenhum dos UUIDs é promovido como identificador de produto, release, distribuição, ativo, pacote ou feição;
- a causa editorial ou técnica da deriva permanece desconhecida;
- novas citações devem apontar para o registro corrente e usar a data real de acesso, sem declarar uma release ainda não resolvida.

## Limitação instrumental

A tentativa de recuperar diretamente o endpoint:

`https://terrabrasilis.dpi.inpe.br/geonetwork/srv/api/records/e6e15388-4ca9-49b9-aec9-03891339a35e`

retornou erro interno durante a consulta. O resultado oficial de busca e o artigo metodológico são convergentes, mas a resposta integral da API não foi registrada. Essa falha não foi interpretada como indisponibilidade permanente nem como invalidade do registro.

## Correções implementadas

Foram atualizados:

- `database/mappings/deter_cerrado_metadata_profile_guard_2026.json`;
- `database/mappings/deter_cerrado_access_license_citation_guard_2026.json`;
- `database/mappings/deter_cerrado_metadata_identifier_ambiguity_guard_2026.json`;
- os três validadores correspondentes.

Os gates agora impedem:

- reaparecimento do UUID antigo como identidade corrente do DETER Cerrado;
- conversão do UUID corrente em identidade de produto, release ou ativo;
- uso da orientação de citação de 2024 sem correção do link e da data de acesso;
- promoção de release ou ativo com base apenas no registro de metadados.

## Estado após a reconciliação

Resolvido:

```text
current_metadata_identifier_reconciled = true
current_metadata_record = e6e15388-4ca9-49b9-aec9-03891339a35e
published_guidance_identifier_current = false
identifier_ambiguity_blocks_product_promotion = false
```

Continuam não resolvidos:

```text
current_release_resolved = false
direct_download_url_verified = false
specific_wfs_layer_name_resolved = false
describe_feature_type_verified = false
asset_bytes_inspected = false
checksum_computed = false
current_release_license_resolved = false
current_release_citation_resolved = false
```

## Evidências

1. INPE / TerraBrasilis GeoNetwork — busca de recursos vetoriais e link do registro DETER Cerrado.
2. Pinheiro et al. (2023) — artigo metodológico e declaração de disponibilidade dos dados.
3. INPE / TerraBrasilis GeoNetwork — catálogo GeoPackage e associação do UUID antigo ao PRODES Amazônia Legal.
4. INPE / BiomasBR — orientação de citação publicada com a referência antiga.

## Risco residual

A identidade do registro de metadados deixou de ser bloqueio. O Marco 2A continua bloqueado por ausência de release explícita, endpoint/ativo verificável, inspeção dos bytes, licença e citação da release e revisão curatorial final.
