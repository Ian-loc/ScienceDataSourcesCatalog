# DATA1 — auditoria estrutural do esquema e proposta 0.8.0

## Objetivo

Avaliar integralmente os 34 campos e as 51 fontes da versão 0.7.0 antes de alterar o CSV canônico. Este documento define o que deve ser preservado, normalizado ou acrescentado e estabelece regras para uma migração verificável.

**Estado deste ciclo:** auditoria e projeto de esquema. `data/data_resources.csv` não é alterado neste PR.

## Diagnóstico executivo

O esquema atual é cientificamente útil e não deve ser substituído. Os principais problemas são de separação semântica:

1. `official_identity` preserva corretamente a autodescrição, mas não permite comparar a função principal dos recursos;
2. `geographic_coverage` combina escala controlável e descrição territorial;
3. `data_formats` contém formatos, protocolos, ambientes de processamento e notas de variabilidade;
4. `access_protocols` combina protocolos, APIs, pacotes, clientes, exportações manuais e ambientes computacionais;
5. `institutional_status` usa combinações livres para conceitos que podem ser multivalorados;
6. não há campo específico para localizar instruções oficiais de citação;
7. as validações atuais garantem forma e completude, mas ainda não bloqueiam várias contradições entre campos.

A mudança deve ser evolutiva: preservar os 34 campos e acrescentar apenas quatro dimensões necessárias. A proposta passa de **34 para 38 campos**.

## Unidade de registro

A unidade continua sendo uma **fonte**, não um dataset individual. Por isso:

- `dataset` não integra o vocabulário principal de `resource_type`;
- DOI de artigo usado como evidência não pode ser tratado como DOI da fonte;
- DOI e versão de datasets específicos continuam sendo conferidos na fonte original;
- o catálogo pode registrar repositórios e bases que contêm milhares de datasets sem criar uma linha para cada produto.

## Novos campos mínimos

| Campo | Tipo | Função | Obrigatório |
|---|---|---|---|
| `resource_type` | categoria controlada singular | Função principal do recurso no catálogo. Não substitui `official_identity`. | sim |
| `geographic_scope` | categoria controlada singular | Maior extensão geográfica geral, separada da descrição territorial. | sim |
| `access_tools` | lista controlada | Clientes, pacotes e ambientes usados para acessar ou processar dados. | não |
| `citation_guidance_url` | URL HTTPS | Página oficial com instruções de citação, quando existir. | não |

Não se recomenda um campo genérico `doi`: na maior parte das fontes, o DOI pertence ao dataset, produto, versão ou publicação metodológica, e não à infraestrutura catalogada.

## Ordem proposta dos 38 campos

1. `resource_id`
2. `resource_name`
3. `acronym`
4. `official_identity`
5. `resource_type`
6. `description`
7. `homepage_url`
8. `data_access_url`
9. `research_areas`
10. `keywords`
11. `data_product_types`
12. `data_formats`
13. `visualization_types`
14. `geographic_scope`
15. `geographic_coverage`
16. `covers_brazil`
17. `spatial_resolution`
18. `temporal_coverage`
19. `temporal_resolution`
20. `data_sources`
21. `free_download`
22. `access_conditions`
23. `programmatic_access`
24. `access_protocols`
25. `access_tools`
26. `authentication_required`
27. `access_documentation_url`
28. `license`
29. `citation_guidance_url`
30. `institutional_status`
31. `owner_or_manager`
32. `academic_uses`
33. `limitations`
34. `academic_evidence_type`
35. `academic_evidence_url`
36. `academic_evidence_note`
37. `verification_url`
38. `last_verified`

## Decisão por campo atual

| Campo | Decisão | Regra 0.8.0 |
|---|---|---|
| `resource_id` | manter | Identificador estável e contínuo. |
| `resource_name` | manter | Nome oficial; não traduzir nomes próprios. |
| `acronym` | manter | Opcional; vazio quando não existir. |
| `official_identity` | manter | Texto fiel à autodescrição da fonte. |
| `description` | manter | Síntese curatorial objetiva. |
| `homepage_url` | manter | URL institucional HTTPS. |
| `data_access_url` | manter | URL efetiva; `não se aplica` apenas quando justificável. |
| `research_areas` | manter controlado | Nove áreas já validadas. |
| `keywords` | manter semi-controlado | Termos específicos, sem duplicar áreas. |
| `data_product_types` | normalizar | Lista de classes de produtos, sem formatos ou interfaces. |
| `data_formats` | normalizar estritamente | Somente formatos de arquivo, serialização ou pacote. |
| `visualization_types` | normalizar | Somente formas de visualização ou apresentação. |
| `geographic_coverage` | manter livre | Território e ressalvas em linguagem legível. |
| `covers_brazil` | manter controlado | Regra existente permanece. |
| `spatial_resolution` | manter livre | Unidade, suporte espacial ou texto de variabilidade. |
| `temporal_coverage` | manter livre | Intervalo ou explicação por produto. |
| `temporal_resolution` | manter semi-controlado | Frequências canônicas mais ressalvas necessárias. |
| `data_sources` | normalizar | Origem empírica em categorias multivaloradas. |
| `free_download` | manter controlado | `sim`, `parcial`, `não`, `desconhecido`, `não se aplica`. |
| `access_conditions` | manter semi-controlado | Condições curtas; detalhes excepcionais podem permanecer. |
| `programmatic_access` | manter controlado | Abrange acesso automatizado documentado, não somente REST. |
| `access_protocols` | normalizar estritamente | Protocolos e interfaces técnicas; pacotes migram para `access_tools`. |
| `authentication_required` | manter controlado | Conta, token, projeto ou credencial. |
| `access_documentation_url` | manter | Documentação técnica do acesso. |
| `license` | manter livre | Licença da fonte ou indicação de variabilidade por dataset. |
| `institutional_status` | normalizar multivalorado | Categorias institucionais controladas. |
| `owner_or_manager` | manter | Organização responsável. |
| `academic_uses` | manter | Finalidades acadêmicas e educacionais. |
| `limitations` | manter | Limitações científicas, operacionais e de interpretação. |
| `academic_evidence_type` | manter controlado | Vocabulário atual. |
| `academic_evidence_url` | manter | Evidência representativa; não equivale ao DOI da fonte. |
| `academic_evidence_note` | manter | Relação entre evidência e avaliação. |
| `verification_url` | manter | Evidência oficial principal. |
| `last_verified` | manter | Data ISO efetiva da revisão. |

## Vocabulário proposto para `resource_type`

| Valor | Definição operacional |
|---|---|
| `database` | Coleção estruturada e persistente de registros ou produtos relacionados. |
| `repository` | Serviço que recebe, preserva, documenta e distribui datasets. |
| `catalog` | Índice de metadados cuja função principal é localizar dados ou recursos. |
| `portal` | Interface de consulta e acesso que não tem processamento integrado como função principal. |
| `platform` | Ambiente que integra dados, visualização, análise ou processamento. |
| `information_system` | Sistema institucional amplo de produção e gestão contínua de informação. |
| `monitoring_system` | Observação recorrente, indicadores operacionais ou alertas como função central. |
| `data_service` | Extração, consulta, transformação ou entrega de dados sob demanda. |
| `data_network` | Rede distribuída de produtores, sítios, repositórios ou participantes. |
| `publishing_software` | Software usado para publicar e administrar dados, sem ser uma base agregadora. |

### Classificação preliminar das 51 fontes

| `resource_type` | Registros propostos |
|---|---|
| `platform` | DR0001, DR0006, DR0007, DR0019, DR0044, DR0045, DR0047 |
| `information_system` | DR0002, DR0003, DR0004, DR0014, DR0017 |
| `monitoring_system` | DR0005, DR0010, DR0012, DR0029 |
| `catalog` | DR0008, DR0035 |
| `portal` | DR0011 |
| `data_network` | DR0009, DR0013, DR0026, DR0027, DR0030, DR0034, DR0042, DR0043, DR0048, DR0049 |
| `database` | DR0015, DR0016, DR0018, DR0022, DR0023, DR0024, DR0025, DR0036, DR0037, DR0038, DR0040, DR0041, DR0046, DR0051 |
| `data_service` | DR0020, DR0021 |
| `repository` | DR0028, DR0031, DR0032, DR0033, DR0050 |
| `publishing_software` | DR0039 |

A classificação é funcional e curatorial. Fontes híbridas continuam descritas integralmente em `official_identity`, `description`, produtos e limitações.

## Vocabulário proposto para `geographic_scope`

- `local`
- `subnational`
- `national`
- `regional`
- `continental`
- `global`
- `variable`
- `not_applicable`

### Classificação preliminar

| Escopo | Registros propostos |
|---|---|
| `subnational` | DR0001, DR0002 |
| `national` | DR0003, DR0004, DR0005, DR0007, DR0008, DR0010, DR0011, DR0014, DR0015, DR0016, DR0017, DR0018, DR0029 |
| `regional` | DR0006, DR0012, DR0013 |
| `continental` | DR0042 |
| `global` | DR0009, DR0019–DR0028, DR0030–DR0038, DR0040–DR0041, DR0043–DR0051 |
| `not_applicable` | DR0039 |

`geographic_scope` representa a maior extensão geral. `geographic_coverage` continua registrando qualificadores como “global terrestre”, “global marinho”, “Amazônia”, “Estados Unidos” ou cobertura desigual.

## Vocabulários técnicos iniciais

### `data_formats`

Valores permitidos devem representar formatos reais ou pacotes identificáveis:

`CSV`, `TSV`, `TXT`, `XLSX`, `JSON`, `XML`, `GeoJSON`, `GeoTIFF`, `Shapefile`, `GeoPackage`, `File Geodatabase`, `KML`, `NetCDF`, `GRIB`, `HDF`, `HDF5`, `LAZ`, `VRT`, `ZIP`, `PDF`, `EML`, `Darwin Core Archive`, `SAFE`, `JPEG2000`, `TFRecord`, `GeoParquet`, `other_documented`, `varies_by_dataset`, `not_applicable`, `unknown`.

Devem sair deste campo: API, WMS, WFS, WCS, visualização web, mapa, serviço web, pacote R/Python, Earth Engine e notas livres.

### `access_protocols`

`REST API`, `OGC WMS`, `OGC WFS`, `OGC WCS`, `OGC WMTS`, `STAC`, `S3`, `openEO`, `OData`, `WebDAV`, `OAI-PMH`, `HTTP download`, `DataONE API`, `Earthdata CMR API`, `Earth Engine API`, `other_documented`, `not_applicable`, `unknown`.

### `access_tools`

`R package`, `Python package`, `JavaScript client`, `command-line client`, `Google Earth Engine`, `cloud processing environment`, `web export`, `other_documented`.

O nome do pacote ou cliente permanece junto ao valor quando necessário, por exemplo `R package: neonUtilities` ou `R package: amerifluxr`.

### `institutional_status`

Campo multivalorado com:

`public`, `academic`, `private`, `nonprofit`, `consortium`, `intergovernmental`.

Exemplos de migração:

- `consórcio acadêmico` → `consortium | academic`;
- `público-acadêmico` → `public | academic`;
- `organização sem fins lucrativos` → `nonprofit`;
- `empresa de comunicação científica` → `private`;
- `público internacional` deve ser classificado pela natureza da organização, não pela palavra “internacional”.

### `data_sources`

Categorias de nível superior:

`satellite`, `field`, `laboratory`, `sensors`, `models`, `literature`, `citizen_science`, `scientific_collections`, `administrative_records`, `official_statistics`, `expert_assessment`, `research_repositories`, `mixed`.

Detalhes instrumentais ou institucionais não devem criar categorias novas quando puderem ser registrados em documentação, descrição ou limitações.

## Validações cruzadas propostas

1. `resource_type = publishing_software` exige `geographic_scope = not_applicable` e estados de acesso coerentes com software, não com dataset agregado.
2. `geographic_scope = global` normalmente exige `covers_brazil = sim`; exceções precisam ser explicitamente justificadas.
3. `geographic_scope = not_applicable` exige `covers_brazil = não se aplica`.
4. `programmatic_access = sim` exige pelo menos um `access_protocols` ou `access_tools` documentado.
5. `programmatic_access = não` ou `não se aplica` não pode coexistir com protocolo positivo sem justificativa.
6. `authentication_required = sim` exige condição compatível, como cadastro, token, projeto ou solicitação.
7. `free_download = sim` exige `data_access_url` válido e não pode ter apenas condição paga ou restrita.
8. `data_formats` não pode conter protocolos, APIs, visualizações ou ambientes de processamento.
9. `visualization_types` não pode conter formatos de arquivo ou protocolos de acesso.
10. `access_protocols` não pode conter pacotes ou clientes, que pertencem a `access_tools`.
11. `citation_guidance_url`, quando preenchido, deve ser HTTPS.
12. DOI em `academic_evidence_url` continua sendo evidência, não identificador da fonte.
13. valores multivalorados não podem conter itens duplicados ou espaços inconsistentes.
14. placeholders `unknown`, `not_applicable` e `varies_by_dataset` não podem coexistir com valores positivos no mesmo campo.

## Riscos de migração identificados

### Alta segurança de derivação

- `geographic_scope` para a maioria dos registros;
- separação de pacotes R/Python e clientes em `access_tools`;
- remoção de WMS/WFS/WCS e APIs de `data_formats`;
- normalização de combinações de `institutional_status`.

### Exige revisão curatorial

- escolha da função principal de fontes híbridas;
- formatos de portais que agregam produtos heterogêneos;
- diferença entre `programmatic_access = parcial` e `sim`;
- cobertura regional com produtos globais secundários;
- existência e escopo de páginas oficiais de citação;
- casos em que a licença varia por dataset ou camada.

## Sequência de migração

1. integrar esta auditoria sem alterar o CSV;
2. criar vocabulários versionados e testes para o esquema 0.8.0;
3. gerar uma matriz de migração com valor antigo, valor proposto e justificativa por registro;
4. revisar manualmente todos os casos de confiança média;
5. alterar cabeçalho, codebook, script de validação e renderer na mesma branch de migração;
6. migrar as 51 linhas de forma atômica;
7. validar que nenhuma informação desapareceu dos cards;
8. publicar como **0.8.0**, ainda sem DOI;
9. iniciar DATA2 em lotes somente depois da validação do novo esquema.

## Critérios de aceite da migração 0.8.0

- 51 IDs preservados;
- 38 campos na ordem documentada;
- nenhum valor científico removido sem destino explícito;
- vocabulários validados automaticamente;
- contradições entre acesso, autenticação, protocolos e formatos bloqueadas;
- todos os campos exibidos ou pesquisáveis na interface;
- PR, GitHub Actions e changelog do Drive concluídos;
- site publicado verificado antes de marcar a etapa como publicada;
- `CITATION.cff` atualizado para `0.8.0` somente junto à migração efetiva.
