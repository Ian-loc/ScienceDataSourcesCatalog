# Dicionário de variáveis

## Esquema canônico 0.7.0

| Campo | Definição |
|---|---|
| `resource_id` | Identificador estável DR0001… |
| `resource_name` | Nome oficial da fonte. |
| `acronym` | Sigla ou nome curto. |
| `official_identity` | Natureza declarada pela própria fonte. |
| `description` | Síntese objetiva do propósito. |
| `homepage_url` | Página institucional, página Sobre ou página oficial dedicada à fonte. |
| `data_access_url` | Destino para pesquisar, visualizar, solicitar ou baixar dados. |
| `research_areas` | Áreas condensadas usadas no filtro. |
| `keywords` | Temas específicos pesquisáveis. |
| `data_product_types` | Produtos disponibilizados. |
| `data_formats` | Formatos de arquivo ou representação. |
| `visualization_types` | Mapas, gráficos, dashboards e outras interfaces. |
| `geographic_coverage` | Abrangência espacial declarada. |
| `covers_brazil` | Presença de dados aplicáveis ao Brasil. |
| `spatial_resolution` | Escala, resolução ou suporte espacial, com ressalvas. |
| `temporal_coverage` | Período coberto. |
| `temporal_resolution` | Frequência ou granularidade temporal. |
| `data_sources` | Origem empírica ou institucional dos dados. |
| `free_download` | Disponibilidade de download gratuito. |
| `access_conditions` | Cadastro, solicitação, embargo, quota ou restrição. |
| `programmatic_access` | Disponibilidade de acesso automatizado documentado. |
| `access_protocols` | No 0.7.0, reúne protocolos, APIs e alguns clientes ou pacotes ainda não separados. |
| `authentication_required` | Necessidade de conta, token, projeto ou credencial. |
| `access_documentation_url` | Documentação técnica do acesso. |
| `license` | Licença ou condição declarada; pode variar por dataset ou produto. |
| `institutional_status` | Natureza institucional. |
| `owner_or_manager` | Responsável pela fonte. |
| `academic_uses` | Usos relevantes para ensino e pesquisa. |
| `limitations` | Restrições e riscos de interpretação. |
| `academic_evidence_type` | Natureza da evidência externa ou técnica. |
| `academic_evidence_url` | Artigo ou documento representativo. |
| `academic_evidence_note` | O que a evidência sustenta. |
| `verification_url` | Principal evidência oficial disponível. |
| `last_verified` | Data da revisão do registro, AAAA-MM-DD; não certifica integralmente todos os produtos ou campos da fonte. |

## Novos campos propostos para 0.8.0

- `resource_type`: função principal controlada;
- `geographic_scope`: maior extensão geográfica geral;
- `access_tools`: pacotes, clientes, exportadores e ambientes de processamento;
- `citation_guidance_url`: instruções oficiais de citação.

No 0.8.0, `access_protocols` conterá somente interfaces técnicas; pacotes e clientes migrarão para `access_tools`. `data_formats` não poderá conter protocolos ou visualizações.

## Extensões científicas paralelas

A direção do Simbioscópio não acrescenta imediatamente dezenas de campos ao CSV de fontes. Ela introduz entidades separadas para evitar misturar nível institucional, produto e significado científico da variável.

### Passaporte de variável

Contrato: `schema/scientific-variable-passport-v0.1.json`.

Campos conceituais principais:

- `passport_id` — identificador estável do passaporte;
- `variable_id` — identificador da variável;
- `display_name` e `canonical_name` — nomes público e normalizado;
- `definition` — significado científico;
- `domain_tags` — múltiplos domínios aplicáveis;
- `unit` e `unit_reference` — unidade e referência;
- `data_type` — natureza estatística;
- `object_observed` — fenômeno, entidade ou objeto observado;
- `population_or_universe` — população ou universo de referência;
- `unit_of_observation` — unidade de observação;
- `spatial_support` — suporte, resolução, CRS e cobertura;
- `temporal_support` — período, frequência e forma de representação;
- `method_type` — medido, administrativo, declarado, modelado, derivado etc.;
- `uncertainty` — informação de erro ou incerteza;
- `provenance` — fonte, produto, versão e linhagem;
- `sensitivity_class` — classificação de sensibilidade;
- `limitations` — limitações de interpretação;
- `review` — estado e revisão humana.

### Avaliação de comparabilidade

Contrato: `schema/comparability-assessment-v0.1.json`.

Campos principais:

- `operation_type` — operação efetivamente solicitada;
- `input_variable_ids` — variáveis avaliadas;
- `dimensions` — semântica, população/suporte, espaço, tempo, método, estatística, proveniência e jurídico-ética;
- `compatibility_class` — A, B, C, D ou E;
- `harmonization_steps` — transformações necessárias;
- `diagnostics_required` — controles estatísticos exigidos;
- `inference_ceiling` — N0 a N5;
- `analytical_use_allowed` — autorização explícita;
- `warnings` e `review` — limitações e revisão.

### Relação e evidência

Contrato: `schema/scientific-relation-evidence-v0.1.json`.

Campos principais:

- variáveis de origem e destino;
- tipo e direção da relação;
- mecanismo;
- mediadores e confundidores;
- aplicabilidade espacial, temporal e populacional;
- registros de evidência favorável, contraditória ou inconclusiva;
- síntese separada de concordância, certeza, aplicabilidade e suporte mecanístico;
- teto de inferência;
- revisão humana obrigatória.

Esses contratos são rascunhos versionados. Eles não constituem ainda tabelas canônicas nem autorizam análise automatizada.

## Regra dos links

**Site oficial**, **Acessar dados** e **Documentação de acesso** têm papéis distintos. URLs iguais permanecem pendentes até confirmação oficial de que uma única página cumpre efetivamente os papéis. `data_access_url = não se aplica` é reservado a recursos sem dados próprios para consulta ou download.

## Evidência externa

A tabela `migration/external_review_evidence.csv` registra uma linha por fonte, dimensão e afirmação. Ela não acrescenta campos ao CSV canônico e não altera valores automaticamente.

Essa evidência sobre fontes não deve ser confundida com a futura evidência sobre relações entre variáveis, que possuirá contrato e revisão próprios.

## Valores controlados

- `free_download`, `programmatic_access`, `authentication_required` e `covers_brazil`: sim, parcial, não, desconhecido, não se aplica;
- campos multivalorados usam ` | `;
- valores desconhecidos devem permanecer explícitos, nunca inferidos como negativos.

Consulte [METHODOLOGY.md](METHODOLOGY.md), [PRODUCT_CATALOG_MODEL.md](PRODUCT_CATALOG_MODEL.md), [Direção científica](docs/PROJECT_SCIENTIFIC_DIRECTION.md) e [Política de comparabilidade](docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md).
