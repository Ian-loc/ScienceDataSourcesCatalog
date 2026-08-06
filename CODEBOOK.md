# Dicionário de dados — Instância 1 simplificada

## 1. Estado da transição

O projeto possui:

1. CSV/JSON públicos atuais, ainda operacionais;
2. esquema profundo do Marco 1, classificado como `LEGACY_TRANSITIONAL`;
3. arquitetura simplificada proposta para a Instância 1.

Os CSVs permanecem autoridade pública até a promoção formal do novo núcleo.

## 2. Núcleo proposto

### `organizations`

| Campo | Definição |
|---|---|
| `organization_id` | Identificador interno. |
| `stable_id` | Identificador estável. |
| `official_name` | Nome oficial. |
| `acronym` | Sigla. |
| `country_code` | País principal. |
| `homepage_url` | Página institucional. |
| `description` | Descrição curta. |

### `catalog_entries`

| Campo | Definição |
|---|---|
| `catalog_entry_id` | Identificador interno. |
| `stable_id` | Identificador estável da entrada. |
| `organization_id` | Organização principal. |
| `parent_entry_id` | Relação opcional entre entrada ampla e entrada mais específica. |
| `entry_type` | `source`, `platform`, `collection`, `data_product` ou `data_service`. |
| `official_name` | Nome usado pela fonte. |
| `acronym` | Sigla ou nome curto. |
| `summary` | Síntese objetiva. |
| `scientific_scope` | Informação científica oferecida. |
| `data_modalities` | Tipos amplos de dados. |
| `geographic_coverage` | Cobertura espacial. |
| `temporal_coverage` | Cobertura temporal. |
| `spatial_resolution_text` | Resolução ou suporte relevante, em texto. |
| `temporal_resolution_text` | Granularidade temporal relevante. |
| `update_frequency_text` | Atualização declarada. |
| `access_level` | Gratuito, parcial, pago, restrito ou desconhecido. |
| `authentication_required` | Necessidade de autenticação. |
| `official_page_url` | Página oficial da entrada. |
| `metadata_url` | Metadados diretos. |
| `primary_access_url` | Canal principal de acesso. |
| `methodology_url` | Metodologia principal. |
| `license_text` | Licença ou condição declarada. |
| `license_url` | Link oficial da licença. |
| `citation_text` | Citação recomendada. |
| `citation_url` | Orientação oficial de citação. |
| `status` | Estado operacional conhecido. |
| `last_verified_at` | Última verificação. |
| `curation_status` | Estado da curadoria. |
| `additional_metadata_json` | Metadados adicionais sem normalização obrigatória. |

### `entry_variables`

| Campo | Definição |
|---|---|
| `entry_variable_id` | Identificador interno. |
| `catalog_entry_id` | Entrada associada. |
| `source_label` | Nome usado pela fonte. |
| `source_definition` | Definição original ou síntese fiel. |
| `unit_text` | Unidade quando material. |
| `variable_group` | Grupo amplo de busca. |
| `search_label` | Rótulo normalizado opcional. |
| `evidence_url` | Evidência principal. |

Não é obrigatório enumerar todas as bandas, colunas, classes ou arquivos.

### `entry_evidence`

| Campo | Definição |
|---|---|
| `entry_evidence_id` | Identificador interno. |
| `catalog_entry_id` | Entrada sustentada. |
| `field_name` | Campo ou afirmação. |
| `evidence_url` | URL oficial ou documento direto. |
| `evidence_type` | Página oficial, metadado, metodologia, licença, citação ou outro. |
| `support_note` | O que a evidência sustenta. |
| `retrieved_at` | Data de recuperação. |
| `confidence` | Confiança curatorial. |

### `connector_profiles`

| Campo | Definição |
|---|---|
| `connector_profile_id` | Identificador interno. |
| `catalog_entry_id` | Entrada associada. |
| `connector_type` | WMS, WFS, STAC, REST, OGC API, Earth Engine ou outro. |
| `endpoint_url` | Endpoint externo. |
| `external_identifier` | Identificador necessário à operação. |
| `authentication` | Requisito de autenticação. |
| `supported_operation` | Operação selecionada. |
| `configuration_json` | Configuração mínima. |
| `last_tested_at` | Data do teste. |
| `status` | Estado do conector. |

Conectores são opcionais e não constituem inventário de ativos.

## 3. Valores controlados

### `entry_type`

- `source`;
- `platform`;
- `collection`;
- `data_product`;
- `data_service`.

### `curation_status`

- `draft`;
- `reviewed`;
- `approved`;
- `needs_evidence`;
- `deprecated`.

### Estado desconhecido

Desconhecido não equivale a `não`. Quando necessário, usar:

- `unknown`;
- `not_found_after_bounded_search`;
- `not_applicable`;
- `inaccessible_in_current_environment`;
- `contradictory`.

## 4. Regra dos links

Priorizar:

- página oficial;
- metadados;
- acesso principal;
- metodologia;
- licença;
- citação.

URLs iguais são aceitáveis quando a mesma página cumpre mais de um papel. Não se deve inventariar toda a árvore de links.

## 5. Regra de granularidade

Uma nova entrada exige diferença material de significado, modalidade, cobertura, período, método, finalidade, acesso principal ou identidade oficial.

Outro arquivo, formato, layer, banda, endpoint, diretório, tabela ou data técnica não cria automaticamente nova entrada.

## 6. Regra de dados externos

Não existe entidade canônica de `data_asset` na Instância 1 simplificada.

Arquivos, datasets, layers, endpoints e coleções permanecem externos. O catálogo registra links e metadados, não custódia ou armazenamento.

## 7. CSVs atuais

### `data/data_resources.csv`

Permanece como catálogo público de fontes durante a transição.

### `data/data_products.csv`

Permanece como piloto legado. Seus registros serão avaliados como candidatos a `catalog_entries`, sem obrigação de preservar a distinção antiga entre família, produto e release.

### `data/product_distributions.csv`

Permanece legado operacional. Links úteis serão condensados em campos principais ou conectores selecionados. Não será migrado como inventário integral.

## 8. Esquema profundo do Marco 1

As tabelas `product_families`, `product_releases`, `distributions`, `data_assets`, `access_capabilities` e perfis separados permanecem como evidência de desenvolvimento e possível fonte de componentes.

Elas não são mais requisitos canônicos da Instância 1 e não devem receber expansão até decisão arquitetural contrária formal.

## 9. Autoridade

Durante a transição:

- CSV/JSON atuais = autoridade pública;
- documentação desta branch = proposta de reorientação;
- novo SQL simplificado = próximo pacote executável;
- planilhas do Drive = espelhos;
- PR #57 = pacote congelado e candidato a `superseded`.
