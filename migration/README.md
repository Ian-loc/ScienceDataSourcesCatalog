# Matrizes de migração DATA1

## Finalidade

A migração do esquema 0.7.0 para 0.8.0 é preparada sem substituir o CSV canônico:

- `data1b_migration_matrix.csv`: tipo funcional, escala, formatos, protocolos, ferramentas e situação institucional;
- `data1bx_migration_matrix.csv`: produtos, visualizações, fontes dos dados, resolução temporal e condições de acesso;
- `br_batch_registry.json`: ordem e estado dos lotes de revisão manual;
- `br1_review_matrix.csv`, `br2_review_matrix.csv`, `br3_review_matrix.csv` e `br4_review_matrix.csv`: auditorias internas aprofundadas.

Todas as matrizes permanecem ligadas por `resource_id`. O arquivo `data/data_resources.csv` continua canônico e a versão 0.7.0 permanece protegida até DATA1-C.

## DATA1-B

A matriz inicial contém as 51 fontes:

- 16 registros prontos para migração;
- 35 registros em revisão manual;
- 24 decisões de alta confiança e 27 de confiança média;
- todo valor `other_documented` exige exceção explícita;
- orientação de citação só é preenchida quando existe página oficial confirmada.

## DATA1-BX

Cinco dimensões são controladas separadamente:

- `data_product_types`;
- `visualization_types`;
- `data_sources`;
- `temporal_resolution`;
- `access_conditions`.

Cada dimensão possui valor, confiança, estado, base de evidência, URL, data e revisor. O estado `carregado_do_csv` apenas preserva o conteúdo atual; não equivale a verificação externa. Enquanto não houver confronto com documentação oficial, a confiança permanece `desconhecida`.

## Registro de lotes DATA1-BR

`br_batch_registry.json` define cinco lotes planejados, BR1–BR5. Os lotes ativos devem:

- seguir a ordem planejada sem saltos;
- conter exatamente sete fontes;
- usar os mesmos arquivos canônicos e matrizes de origem;
- não repetir `resource_id` entre lotes;
- preservar confiança DATA1-BX desconhecida enquanto a revisão externa estiver bloqueada;
- proibir alterações automáticas do CSV.

### BR1 — plataformas e monitoramento de alto impacto

CEMADEN, dados.gov.br, MapBiomas, TerraBrasilis, BDQueimadas, Google Earth Engine e Global Forest Watch.

Riscos dominantes: heterogeneidade por produto, agregação de terceiros, acesso e licença variáveis, temporalidade, protocolos e semântica de alertas, focos, incêndios, áreas queimadas e desmatamento.

### BR2 — biodiversidade, ciência cidadã e redes de dados

speciesLink, SiBBr, eBird, Movebank, DataONE, iNaturalist e TRY.

Riscos dominantes: duplicação entre redes, distinção entre agregador e fonte primária, licença por registro ou dataset, coordenadas sensíveis, viés amostral, produtos brutos versus modelados, qualidade taxonômica, acesso por solicitação e termos dos contribuidores.

### BR3 — clima, repositórios e redes de fluxos

Copernicus Climate Data Store, WorldClim, NEON, PANGAEA, Climate Data Guide, AmeriFlux e FLUXNET.

Riscos dominantes: versão e coleção, mistura de observações, reanálises, modelos e produtos derivados, período climatológico e cenário, dados provisórios ou reprocessados, licença por dataset ou sítio, área de influência das torres e sobreposição entre AmeriFlux e FLUXNET.

### BR4 — sistemas territoriais e climáticos brasileiros

Clima Gerais, IDE-SISEMA, AdaptaBrasil, SIRENE, PANORAMA/CENSIPAM, UrbVerde e BDiA.

Riscos dominantes: indicadores compostos confundidos com observações, atualização não demonstrada por produto, camada ou módulo, resolução visual confundida com escala cartográfica, formatos e serviços generalizados, dashboard tratado como download e ausência de separação comprovada entre página institucional e acesso efetivo aos dados.

## Papéis dos links

Os cards usam dois destinos distintos:

- `homepage_url`: página institucional principal, página “Sobre” ou página oficial do órgão responsável;
- `data_access_url`: catálogo, busca, visualizador, formulário de solicitação ou página de download.

`homepage_and_data_access_role` é dimensão obrigatória do BR4. Três casos do lote usam atualmente o mesmo destino e permanecem pendentes: SIRENE, UrbVerde e BDiA. O PANORAMA usa `/` e `/home`, mas a auditoria interna não considera essa diferença de caminho prova suficiente de que exista separação institucional e operacional.

`scripts/audit_link_roles.py` gera `data/link_role_audit.json` e contabiliza:

- destinos separados;
- URLs iguais pendentes de revisão;
- casos em que acesso aos dados não se aplica.

A igualdade ou a diferença superficial entre links não autoriza correção automática. O destino correto depende de inspeção oficial atual.

## Interpretação da auditoria interna

Cada matriz BR registra justificativa, prioridade, riscos, achados de consistência, URLs existentes, dimensões que exigem documentação oficial e decisão conservadora sobre o CSV.

A auditoria interna não equivale a validação factual. Enquanto `external_review_status` for `bloqueada_sem_web`, a linha não pode receber nova URL de evidência, revisor, data, confiança elevada ou decisão de correção.

## Validação

Execute:

```bash
python3 scripts/validate_migration_matrix.py
python3 scripts/validate_data1bx_matrix.py
python3 scripts/load_data1bx_from_canonical.py
python3 scripts/validate_br_batches.py
python3 scripts/audit_link_roles.py
```

O validador dos lotes confere registro, contratos, matrizes, ordem, exclusividade dos IDs, URLs existentes, estado manual em DATA1-B, confiança desconhecida em DATA1-BX e bloqueios de evidência.

## Estado protegido

- CSV canônico: 51 fontes × 34 campos;
- versão formal: 0.7.0;
- esquema 0.8.0: proposta não aplicada;
- DATA1-BX: projeção concluída, confiança externa desconhecida;
- BR1–BR4: auditorias internas concluídas; revisões factuais externas bloqueadas;
- 28 dos 35 casos manuais distribuídos em lotes;
- 7 casos manuais restantes para BR5;
- candidatos: fora do CSV;
- DOI: bloqueado.
