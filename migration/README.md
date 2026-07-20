# Matrizes de migração DATA1

## Fonte canônica

A migração 0.7.0 → 0.8.0 é preparada sem substituir `data/data_resources.csv`. Todas as tabelas usam `resource_id`.

- `data1b_migration_matrix.csv`: tipo, escala, formatos, protocolos, ferramentas e situação institucional;
- `data1bx_migration_matrix.csv`: produtos, visualizações, fontes, resolução temporal e acesso;
- `br_batch_registry.json`: registro único e atual de BR1–BR5;
- `br1_review_matrix.csv` a `br5_review_matrix.csv`: auditorias internas;
- `external_review_queue.csv`: ordem de revisão externa;
- `external_review_evidence.csv`: evidências em formato longo.

O antigo `data1br_review_batches.csv` foi removido porque representava uma distribuição anterior e conflitava com os contratos reais dos lotes.

## Estado

- DATA1-B: 51 fontes, sendo 16 `pronto_para_migração` e 35 `revisão_manual`;
- DATA1-BX: cinco dimensões carregadas do CSV, confiança `desconhecida`;
- BR1–BR5: 35 casos distribuídos sem sobreposição;
- revisão factual externa: ainda não iniciada;
- CSV: 51 × 34; versão: 0.7.0; DOI: bloqueado.

## Lotes internos

- **BR1:** CEMADEN, dados.gov.br, MapBiomas, TerraBrasilis, BDQueimadas, Google Earth Engine e Global Forest Watch.
- **BR2:** speciesLink, SiBBr, eBird, Movebank, DataONE, iNaturalist e TRY.
- **BR3:** Copernicus Climate Data Store, WorldClim, NEON, PANGAEA, Climate Data Guide, AmeriFlux e FLUXNET.
- **BR4:** Clima Gerais, IDE-SISEMA, AdaptaBrasil, SIRENE, PANORAMA/CENSIPAM, UrbVerde e BDiA.
- **BR5:** HidroWeb, BIEN, Global Carbon Atlas, Copernicus Data Space Ecosystem, ILTER, ORNL DAAC e Project COSMOS.

As matrizes internas registram riscos e foco de revisão; não comprovam os atributos externos.

## DATA1-BR-CLOSE

A fila externa separa:

- **prioridade científica:** somente impacto e risco, comparáveis em todos os lotes;
- **onda operacional:** escopo, homepage/acesso, documentação ausente e ordem de execução.

Contagens brutas de flags e dimensões não são usadas. O Project COSMOS entra em `G0`, um portão de escopo separado. A primeira onda `W1` reúne sete fontes P0 com homepage e acesso no mesmo destino.

## Evidências externas

`external_review_evidence.csv` usa uma linha por fonte, dimensão e afirmação. Campos principais:

- afirmação revisada e valor atual;
- valor observado na fonte oficial;
- URL e tipo de evidência;
- organização responsável;
- data e revisor;
- suporte ao valor atual;
- ação e valor propostos;
- notas e limitações.

Uma fonte pode ter várias evidências. A fila guarda apenas estado, ordem e `evidence_record_count`. Nenhuma evidência modifica automaticamente o CSV.

## Papéis dos links

- `homepage_url`: página institucional ou página Sobre;
- `data_access_url`: busca, catálogo, visualizador, solicitação ou download;
- `access_documentation_url`: API, protocolo, autenticação ou credenciais.

URLs iguais ou caminhos superficialmente distintos permanecem pendentes até inspeção oficial.

## Validação

```bash
python3 scripts/validate_migration_matrix.py
python3 scripts/validate_data1bx_matrix.py
python3 scripts/load_data1bx_from_canonical.py
python3 scripts/validate_br_batches.py
python3 scripts/validate_br_completion.py
python3 scripts/validate_external_review_evidence.py
python3 scripts/validate_external_review_queue.py
python3 scripts/audit_link_roles.py
```

O esquema 0.8.0 só poderá ser aplicado em DATA1-C após as decisões críticas e evidências necessárias.
