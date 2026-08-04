# Dicionário de dados

## 1. Estado da transição

O projeto possui dois níveis simultâneos:

1. **esquema público atual 0.7.0**, baseado em CSVs;
2. **modelo relacional de destino da Instância 1**, implementado em PostgreSQL/PostGIS.

Os CSVs permanecem canônicos para a versão pública atual até o portão de promoção do banco relacional.

## 2. CSV de fontes — esquema 0.7.0

Arquivo: `data/data_resources.csv`

| Campo | Definição |
|---|---|
| `resource_id` | Identificador estável da fonte, DR0001… |
| `resource_name` | Nome oficial da fonte. |
| `acronym` | Sigla ou nome curto. |
| `official_identity` | Natureza declarada pela própria fonte. |
| `description` | Síntese objetiva do propósito. |
| `homepage_url` | Página institucional ou página oficial da fonte. |
| `data_access_url` | Página para pesquisar, visualizar, solicitar ou baixar dados. |
| `research_areas` | Áreas condensadas usadas no filtro. |
| `keywords` | Temas pesquisáveis. |
| `data_product_types` | Resumo dos tipos de produtos. Não substitui a tabela de produtos. |
| `data_formats` | Resumo de formatos. Pode variar por produto. |
| `visualization_types` | Interfaces gerais disponíveis. |
| `geographic_coverage` | Abrangência espacial geral da fonte. |
| `covers_brazil` | Presença de dados aplicáveis ao Brasil. |
| `spatial_resolution` | Resumo da escala, resolução ou suporte; frequentemente varia por produto. |
| `temporal_coverage` | Período geral coberto. |
| `temporal_resolution` | Frequência ou granularidade geral. |
| `data_sources` | Origem empírica ou institucional dos dados. |
| `free_download` | Disponibilidade geral de download gratuito. |
| `access_conditions` | Cadastro, solicitação, embargo, quota ou restrição. |
| `programmatic_access` | Acesso automatizado documentado. |
| `access_protocols` | Protocolos e APIs no esquema atual. |
| `authentication_required` | Necessidade de credencial. |
| `access_documentation_url` | Documentação técnica do acesso. |
| `license` | Licença geral ou condição declarada. |
| `institutional_status` | Natureza institucional. |
| `owner_or_manager` | Responsável. |
| `academic_uses` | Usos relevantes para ensino e pesquisa. |
| `limitations` | Limitações gerais da fonte. |
| `academic_evidence_type` | Natureza da evidência externa. |
| `academic_evidence_url` | Artigo ou documento representativo. |
| `academic_evidence_note` | O que a evidência sustenta. |
| `verification_url` | Evidência oficial principal. |
| `last_verified` | Data da revisão do registro. Não certifica todos os produtos. |

## 3. CSV de produtos — piloto atual

Arquivo: `data/data_products.csv`

O arquivo continua operacional durante a migração, mas seus campos serão normalizados em entidades relacionais.

Campos principais atuais:

- `product_id`;
- `resource_id`;
- `product_name`;
- `product_acronym`;
- `product_family`;
- `product_kind`;
- `product_description`;
- `research_areas`;
- `keywords`;
- `geographic_coverage`;
- `covers_brazil`;
- `spatial_support`;
- `spatial_resolution`;
- `temporal_coverage`;
- `temporal_resolution`;
- `update_frequency`;
- `product_status`;
- `version_or_collection`;
- `enumeration_scope`;
- `product_page_url`;
- `methodology_url`;
- `primary_or_derived`;
- `limitations`;
- `last_verified`.

Limitação estrutural: o piloto mistura produtos científicos, catálogos e serviços. Essa mistura deverá ser corrigida na migração.

## 4. CSV de distribuições — piloto atual

Arquivo: `data/product_distributions.csv`

Campos principais atuais:

- `distribution_id`;
- `product_id`;
- `distribution_name`;
- `access_url`;
- `format`;
- `access_protocol`;
- `access_tool`;
- `free_download`;
- `authentication_required`;
- `access_conditions`;
- `license`;
- `provider_attribution_required`;
- `subset_support`;
- `notes`;
- `last_verified`.

No modelo relacional, uma distribuição será vinculada a um release específico.

## 5. Banco relacional da Instância 1

Arquivo: `database/schema/001_instance1_core.sql`

Schema PostgreSQL: `catalog`

### `organizations`

Instituições, consórcios e iniciativas responsáveis.

Campos essenciais:

- `organization_id`;
- `stable_id`;
- `official_name`;
- `acronym`;
- `organization_type`;
- `country_code`;
- `homepage_url`;
- `description`.

### `sources`

Portais, repositórios, catálogos, plataformas, redes, observatórios, programas ou infraestruturas.

Campos essenciais:

- `stable_id` — DR…;
- `source_name`;
- `source_type`;
- `official_identity`;
- `description`;
- URLs institucionais e de acesso;
- `geographic_scope`;
- `covers_brazil`;
- `active_status`;
- `enumeration_strategy`.

### `product_families`

Agrupamentos de produtos relacionados.

Campos essenciais:

- `family_name`;
- `source_id`;
- `scientific_scope`;
- `enumeration_scope`.

### `products`

Produtos científicos georreferenciados.

Campos essenciais:

- `stable_id` — DP…;
- `product_name`;
- `product_kind`;
- `product_description`;
- `scientific_object`;
- `information_message`;
- `intended_uses`;
- `non_representations`;
- `primary_or_derived`;
- cobertura;
- estado;
- páginas oficiais;
- limitações.

`information_message` responde qual informação sobre o mundo real o produto comunica.

`non_representations` registra interpretações que o produto não sustenta diretamente.

### `product_releases`

Versões, coleções, edições, cenários ou anos-base.

Campos essenciais:

- `version_label`;
- `release_date`;
- validade;
- cobertura temporal;
- `release_status`;
- notas de mudança;
- identificador ou checksum;
- `is_current`.

### `spatial_profiles`

Campos essenciais:

- `support_type`;
- `support_description`;
- geometria;
- resolução nominal e unidade;
- escala;
- unidade mínima mapeável;
- CRS;
- grade;
- agregação;
- unidade geográfica;
- cobertura textual;
- geometria de cobertura PostGIS;
- vieses e limitações espaciais.

### `temporal_profiles`

Campos essenciais:

- tipo de representação;
- descrição do suporte;
- datas inicial e final;
- resolução;
- janela de observação;
- frequência;
- latência;
- calendário;
- agregação;
- vieses e limitações temporais.

### `methods`

Descreve medição, sensoriamento remoto, registro administrativo, levantamento, classificação, modelagem, interpolação, agregação ou método misto.

Campos essenciais:

- nome e tipo;
- descrição;
- dados de entrada;
- processamento;
- validação;
- versão;
- documentação;
- limitações.

### `quality_profiles`

Campos essenciais:

- estado da documentação;
- desenho de validação;
- métricas de acurácia;
- disponibilidade e tipo de incerteza;
- flags;
- dados ausentes;
- viés de coleta;
- artefatos;
- limites de representatividade;
- documentação.

### `variables`

Vocabulário de variáveis, indicadores, classes, bandas e métricas.

Campos essenciais:

- `stable_id` — VR…;
- nome canônico;
- nomes em português e inglês;
- definição;
- fenômeno;
- objeto observado;
- população ou universo;
- tipo de dado;
- unidade canônica;
- vocabulário de referência;
- sensibilidade.

### `product_variables`

Associação entre release e variável.

Campos essenciais:

- nome original no produto;
- papel da variável;
- definição original;
- unidade;
- tipo;
- método;
- perfis espacial, temporal e de qualidade;
- interpretação;
- potencial científico;
- não-interpretações;
- semântica de agregação;
- legenda;
- estado de revisão.

Papéis controlados incluem:

- observação principal;
- estimativa principal;
- variável derivada;
- classe;
- probabilidade;
- qualidade;
- incerteza;
- coordenada;
- dimensão;
- identificador;
- máscara;
- auxiliar.

### `distributions`

Formas de acesso a releases.

Campos essenciais:

- `stable_id` — DD…;
- nome;
- papel;
- URL;
- formato;
- media type;
- protocolo;
- ferramenta;
- gratuidade;
- autenticação;
- condições;
- licença;
- atribuição;
- suporte a recorte;
- estado do acesso;
- data do teste.

### `data_assets`

Arquivos, endpoints, camadas, tabelas, legendas, metadados e recursos concretos.

### `access_capabilities`

Capacidades controladas:

- descobrir;
- pré-visualizar;
- visualizar;
- consultar atributos;
- recortar no espaço ou tempo;
- baixar;
- transmitir;
- processar;
- exportar;
- abrir em QGIS, R, Python ou Earth Engine.

### `taxonomy_terms`

Vocabulários temáticos, científicos, territoriais e operacionais.

### `citations`, `product_citations`, `release_citations`

Citações de dataset, metodologia, validação, documentação, licença e ciência relacionada.

### `metadata_assertions`

Evidência por campo.

Campos essenciais:

- entidade;
- identificador;
- campo;
- valor;
- URL;
- tipo de evidência;
- nota de suporte;
- confiança;
- data de recuperação.

### `curation_reviews`

Estado, escores de completude e precisão, achados, correções e próxima revisão.

## 6. Valores controlados importantes

### Estado desconhecido

O desconhecido deve permanecer explícito. Não deve ser convertido em `não`.

### Natureza de produção

- observação primária;
- registro administrativo;
- estimativa amostral;
- classificado;
- modelado;
- interpolado;
- derivado;
- misto;
- desconhecido.

### Estratégia de enumeração

- `complete`;
- `family_level`;
- `external_index`;
- `representative_sample`;
- `selective`.

### Estado de revisão

- `draft`;
- `reviewed`;
- `approved`;
- `deprecated`.

## 7. Regra dos links

- página institucional;
- página do produto;
- acesso aos dados;
- metodologia;
- documentação de acesso;
- licença;
- citação;
- visualizador.

Esses papéis são distintos. URLs iguais só são aceitas quando a página cumpre efetivamente mais de uma função.

## 8. Regra de autoridade

Durante a transição:

- CSVs atuais = autoridade da versão pública;
- SQL relacional = arquitetura canônica de destino;
- planilha do Drive = espelho derivado;
- evidências não alteram silenciosamente os dados;
- promoção exige auditoria.

Consulte:

- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`;
- `PRODUCT_CATALOG_MODEL.md`;
- `database/README.md`;
- `docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md`.
