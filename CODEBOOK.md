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
| `last_verified` | Data efetiva da revisão, AAAA-MM-DD. |

## Novos campos propostos para 0.8.0

- `resource_type`: função principal controlada;
- `geographic_scope`: maior extensão geográfica geral;
- `access_tools`: pacotes, clientes, exportadores e ambientes de processamento;
- `citation_guidance_url`: instruções oficiais de citação.

No 0.8.0, `access_protocols` conterá somente interfaces técnicas; pacotes e clientes migrarão para `access_tools`. `data_formats` não poderá conter protocolos ou visualizações.

## Regra dos links

**Site oficial**, **Acessar dados** e **Documentação de acesso** têm papéis distintos. URLs iguais permanecem pendentes até confirmação oficial de que uma única página cumpre efetivamente os papéis. `data_access_url = não se aplica` é reservado a recursos sem dados próprios para consulta ou download.

## Evidência externa

A tabela `migration/external_review_evidence.csv` registra uma linha por fonte, dimensão e afirmação. Ela não acrescenta campos ao CSV canônico e não altera valores automaticamente.

## Valores controlados

- `free_download`, `programmatic_access`, `authentication_required` e `covers_brazil`: sim, parcial, não, desconhecido, não se aplica;
- campos multivalorados usam ` | `;
- valores desconhecidos devem permanecer explícitos, nunca inferidos como negativos.

Consulte [METHODOLOGY.md](METHODOLOGY.md) e [DATA1_SCHEMA_AUDIT.md](DATA1_SCHEMA_AUDIT.md).
