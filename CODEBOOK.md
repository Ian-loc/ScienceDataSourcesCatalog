# Dicionário de dados

## 1. Estado da transição

O projeto possui três camadas distintas:

1. **CSV/JSON público atual**, que permanece como autoridade da interface publicada;
2. **staging relacional**, que preserva sem perda os registros atuais;
3. **núcleo mínimo proposto**, centrado em entradas de catálogo.

A arquitetura profunda incorporada no Marco 1 permanece disponível como legado técnico durante a migração, mas não define mais a completude da Instância 1.

## 2. CSV público de fontes

Arquivo: `data/data_resources.csv`

| Campo | Definição |
|---|---|
| `resource_id` | Identificador estável atual, como `DR0001`. |
| `resource_name` | Nome oficial da fonte ou infraestrutura. |
| `acronym` | Sigla ou nome curto. |
| `official_identity` | Natureza declarada pela fonte. |
| `description` | Síntese objetiva do que a fonte oferece. |
| `homepage_url` | Página institucional ou oficial. |
| `data_access_url` | Caminho principal para pesquisar, visualizar, solicitar ou baixar dados. |
| `research_areas` | Áreas usadas em busca e filtros. |
| `keywords` | Temas pesquisáveis. |
| `data_product_types` | Resumo não exaustivo das modalidades ou ofertas. |
| `data_formats` | Formatos gerais conhecidos; não constitui inventário. |
| `visualization_types` | Interfaces gerais disponíveis. |
| `geographic_coverage` | Abrangência espacial geral. |
| `covers_brazil` | Presença de dados aplicáveis ao Brasil. |
| `spatial_resolution` | Resolução ou suporte geral quando documentado e material. |
| `temporal_coverage` | Período geral coberto. |
| `temporal_resolution` | Granularidade ou frequência temporal geral. |
| `data_sources` | Origem empírica ou institucional dos dados. |
| `free_download` | Disponibilidade geral de acesso gratuito. |
| `access_conditions` | Cadastro, solicitação, embargo, quota ou restrição. |
| `programmatic_access` | Presença geral de acesso automatizado documentado. |
| `access_protocols` | Protocolos gerais conhecidos. |
| `authentication_required` | Necessidade de credencial. |
| `access_documentation_url` | Instruções técnicas de acesso. |
| `license` | Licença ou condição geral declarada; não deve ser herdada por todos os arquivos. |
| `institutional_status` | Natureza institucional. |
| `owner_or_manager` | Responsável institucional. |
| `academic_uses` | Usos gerais relevantes. |
| `limitations` | Limitações gerais da entrada. |
| `academic_evidence_type` | Tipo da evidência externa representativa. |
| `academic_evidence_url` | Documento ou artigo representativo. |
| `academic_evidence_note` | O que essa evidência sustenta. |
| `verification_url` | Evidência oficial principal. |
| `last_verified` | Data da revisão do registro; não certifica todo o conteúdo da fonte. |

## 3. CSVs piloto

### `data/data_products.csv`

Permanece como piloto histórico e operacional. Não determina que toda fonte deva ser decomposta em produtos.

### `data/product_distributions.csv`

Permanece como piloto histórico de formas de acesso. Não determina inventário de arquivos, layers ou endpoints.

Ambos serão mapeados seletivamente para o núcleo mínimo. Nenhuma linha se torna entrada apenas por existir nesses arquivos.

## 4. Núcleo mínimo proposto

Schema PostgreSQL: `catalog`.

### `organizations`

Instituições responsáveis.

Campos principais:

- `organization_id`;
- `stable_id`;
- `official_name`;
- `acronym`;
- `organization_type`;
- `country_code`;
- `homepage_url`;
- `description`.

### `catalog_entries`

Unidade pública central.

Campos propostos:

- `entry_id`;
- `stable_id`;
- `organization_id`;
- `parent_entry_id` opcional;
- `entry_type`;
- `official_name`;
- `acronym`;
- `summary`;
- `scientific_scope`;
- `data_modalities`;
- `geographic_coverage_text`;
- `temporal_coverage_text`;
- `spatial_resolution_text`;
- `temporal_resolution_text`;
- `update_frequency_text`;
- `access_level`;
- `authentication_required`;
- `official_page_url`;
- `metadata_url`;
- `primary_access_url`;
- `methodology_url`;
- `license_text`;
- `license_url`;
- `citation_text`;
- `citation_url`;
- `curation_status`;
- `last_verified_at`;
- `additional_metadata` JSONB;
- `source_record_ids` JSONB;
- timestamps.

### `entry_type`

Valores iniciais:

- `source`;
- `platform`;
- `collection`;
- `data_product`;
- `data_service`.

O tipo organiza a interface e não reproduz obrigatoriamente a ontologia da fonte.

### `entry_variables`

Temas, fenômenos e variáveis principais úteis para busca.

Campos propostos:

- `entry_variable_id`;
- `entry_id`;
- `source_label`;
- `source_definition`;
- `search_label` opcional;
- `variable_group`;
- `unit_text` opcional;
- `evidence_id` opcional;
- `curation_status`.

Não deve receber automaticamente cada coluna, banda, classe ou flag.

### `entry_evidence`

Evidência proporcional para um campo ou conjunto de campos.

Campos propostos:

- `evidence_id`;
- `entry_id`;
- `supported_fields`;
- `evidence_url`;
- `evidence_type`;
- `support_note`;
- `retrieved_at`;
- `curation_status`.

### `connector_profiles`

Extensão opcional para candidatos selecionados da Instância 2.

Campos propostos:

- `connector_profile_id`;
- `entry_id`;
- `connector_type`;
- `endpoint_url`;
- `external_identifier`;
- `authentication`;
- `supported_operations`;
- `configuration` JSONB;
- `last_tested_at`;
- `status`.

Um conector não implica cópia, hospedagem ou harmonização dos dados.

## 5. Estados curatoriais

Valores recomendados:

- `needs_review`;
- `partially_verified`;
- `verified`;
- `not_found`;
- `not_applicable`.

`not_found` significa que a informação não foi localizada no escopo de busca registrado. Não significa ausência factual universal.

## 6. Granularidade

Uma nova entrada exige diferença material de significado, modalidade, cobertura, método, finalidade, público ou acesso.

Não criar entrada apenas por:

- arquivo;
- formato;
- layer;
- banda;
- endpoint;
- tabela interna;
- diretório;
- atualização técnica.

## 7. Links

Papéis principais:

- `official_page_url` — identidade e apresentação oficial;
- `metadata_url` — metadados da entrada;
- `primary_access_url` — caminho principal aos dados;
- `methodology_url` — método;
- `license_url` — termos ou licença;
- `citation_url` — orientação de citação.

URLs podem coincidir quando a mesma página cumpre efetivamente mais de um papel.

## 8. Estruturas profundas legadas

As tabelas incorporadas no Marco 1 — incluindo fontes, famílias, produtos, releases, distribuições, ativos, capacidades, métodos e perfis — permanecem preservadas até migração auditada.

Elas são:

- fonte de componentes reutilizáveis;
- evidência histórica;
- extensões potenciais para casos concretos.

Elas não são requisitos universais nem devem gerar entradas automaticamente.

## 9. Autoridade

Durante a transição:

- CSV/JSON atuais = autoridade da interface pública;
- staging = preservação sem perda;
- núcleo mínimo = arquitetura de destino proposta;
- estrutura profunda = legado técnico preservado;
- planilhas do Drive = espelhos derivados.

A promoção do núcleo mínimo depende de migração idempotente, exportação reproduzível, CI, revisão e autorização humana.
