# Matrizes de migração DATA1

## Finalidade

A migração 0.7.0 → 0.8.0 é preparada sem substituir o CSV canônico:

- `data1b_migration_matrix.csv`: tipo, escala, formatos, protocolos, ferramentas e situação institucional;
- `data1bx_migration_matrix.csv`: produtos, visualizações, fontes, resolução temporal e acesso;
- `br_batch_registry.json`: ordem e estado dos lotes;
- `br1_review_matrix.csv` a `br5_review_matrix.csv`: auditorias internas aprofundadas.

Todas as matrizes usam `resource_id`. `data/data_resources.csv` permanece canônico até DATA1-C.

## DATA1-B e DATA1-BX

DATA1-B preserva:

- 51 fontes;
- 16 registros `pronto_para_migração`;
- 35 registros `revisão_manual`.

DATA1-BX controla cinco dimensões e mantém confiança `desconhecida` enquanto não houver revisão oficial. `carregado_do_csv` significa preservação, não validação externa.

## Lotes DATA1-BR

Cada lote contém sete fontes, segue a ordem planejada, não repete IDs, usa os mesmos arquivos canônicos e proíbe alteração automática do CSV.

### BR1

CEMADEN, dados.gov.br, MapBiomas, TerraBrasilis, BDQueimadas, Google Earth Engine e Global Forest Watch.

Riscos: heterogeneidade por produto, agregação de terceiros, acesso, licença, temporalidade, protocolos e semântica de alertas.

### BR2

speciesLink, SiBBr, eBird, Movebank, DataONE, iNaturalist e TRY.

Riscos: duplicação, agregadores versus fontes, licença por registro ou dataset, coordenadas sensíveis, viés amostral e produtos modelados.

### BR3

Copernicus Climate Data Store, WorldClim, NEON, PANGAEA, Climate Data Guide, AmeriFlux e FLUXNET.

Riscos: versão, coleção, observações versus modelos, cenário, reprocessamento, licença por sítio ou dataset e sobreposição entre redes.

### BR4

Clima Gerais, IDE-SISEMA, AdaptaBrasil, SIRENE, PANORAMA/CENSIPAM, UrbVerde e BDiA.

Riscos: indicadores compostos, atualização por produto, visualizador versus download, escala cartográfica, protocolos e papéis dos links.

### BR5

HidroWeb, BIEN, Global Carbon Atlas, Copernicus Data Space Ecosystem, ILTER, ORNL DAAC e Project COSMOS.

Riscos: qualidade de séries de estações, datasets e sítios heterogêneos, API de metadados versus arquivos, ferramenta versus protocolo, processamento, autenticação, DOI, licença, interface pública versus base integral e escopo bibliométrico.

O Project COSMOS permanece no CSV para decisão futura. É um recurso bibliométrico sobre pesquisa climática, não uma fonte direta de medições ambientais.

## Papéis dos links

- `homepage_url`: página institucional, homepage ou página Sobre;
- `data_access_url`: busca, catálogo, visualizador, solicitação ou download;
- `access_documentation_url`: API, protocolo, autenticação ou credenciais.

URLs iguais ou caminhos superficialmente diferentes são pendências até inspeção oficial. Nenhuma URL é corrigida por inferência.

## Validação

Execute:

```bash
python3 scripts/validate_migration_matrix.py
python3 scripts/validate_data1bx_matrix.py
python3 scripts/load_data1bx_from_canonical.py
python3 scripts/validate_br_batches.py
python3 scripts/validate_br_completion.py
python3 scripts/audit_link_roles.py
```

`validate_br_batches.py` verifica cada lote. `validate_br_completion.py` confirma que BR1–BR5 cobrem exatamente os 35 casos `revisão_manual` e que os 16 registros prontos permanecem fora dos lotes.

## Estado protegido

- CSV: 51 fontes × 34 campos;
- versão: 0.7.0;
- esquema 0.8.0: não aplicado;
- DATA1-BX: confiança externa desconhecida;
- BR1–BR5: auditorias internas concluídas; revisões externas bloqueadas;
- casos manuais distribuídos: 35 de 35;
- candidatos: fora do CSV;
- DOI: bloqueado.
