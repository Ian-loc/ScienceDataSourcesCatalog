# Estado do workflow

## Regra operacional

Uma tarefa só é concluída após branch, pull request, integração à `main`, GitHub Actions verde e registro no changelog. Alterações públicas também exigem confirmação do deploy.

CI verde comprova estrutura e coerência interna. Não comprova atualidade, acesso ou correção factual das fontes externas.

## Limitações

- revisão factual depende de documentação oficial atual;
- acesso web de pesquisa não está disponível neste ambiente;
- auditoria interna não eleva confiança nem autoriza correções no CSV;
- URLs iguais em `homepage_url` e `data_access_url` permanecem pendentes;
- as 18 fontes candidatas permanecem fora do catálogo;
- versão 1.0.0 e DOI continuam bloqueados.

## Backlog

| Frente | Estado | Critério principal |
|---|---|---|
| DATA1-A | concluído | esquema 0.8.0 documentado |
| DATA1-B | concluído | 51 linhas classificadas |
| DATA1-BX | projeção concluída | 51 × 5 dimensões; confiança desconhecida |
| DATA1-BR/BR1–BR5 | auditoria interna concluída | 35 casos manuais cobertos sem sobreposição |
| DATA1-BR-CLOSE | próximo checkpoint | fila única de revisão externa |
| DATA1-C | bloqueado | decisões e evidências revisadas |
| DATA1-D | planejado | 14 regras no CSV 0.8.0 |
| DATA2 | planejado | revisão factual das 51 fontes |
| UX5 | parcial | interface dos 38 campos |
| RELEASE2 | bloqueado | portões G1–G10 e deploy confirmado |
| DOI | bloqueado | portões G1–G12 e depósito inspecionado |
| RES1 | P3 | resolução por produto |
| EDU1 | P3 | página didática referenciada |

## Estado consolidado

- versão formal: **0.7.0**;
- CSV canônico: **51 fontes × 34 campos**;
- DATA1-B: **16 prontos + 35 revisão_manual**;
- DATA1-BX: confiança `desconhecida`;
- lotes ativos: **BR1–BR5**;
- casos manuais distribuídos: **35 de 35**;
- casos manuais restantes: **0**;
- candidatos: **18 fora do CSV**;
- esquema 0.8.0: não aplicado;
- expansão, v1.0.0 e DOI: bloqueados.

## Síntese dos lotes

### BR1

CEMADEN, dados.gov.br, MapBiomas, TerraBrasilis, BDQueimadas, Google Earth Engine e Global Forest Watch.

Riscos: agregadores versus produtores, heterogeneidade por produto, protocolos, resolução, temporalidade e semântica de alertas.

### BR2

speciesLink, SiBBr, eBird, Movebank, DataONE, iNaturalist e TRY.

Riscos: duplicação entre redes, licença por registro ou dataset, coordenadas sensíveis, viés amostral, taxonomia e dados brutos versus modelados.

### BR3

Copernicus Climate Data Store, WorldClim, NEON, PANGAEA, Climate Data Guide, AmeriFlux e FLUXNET.

Riscos: versão e coleção, observação versus modelo, dados reprocessados, licença por dataset ou sítio, suporte espacial e duplicação entre redes.

### BR4

Clima Gerais, IDE-SISEMA, AdaptaBrasil, SIRENE, PANORAMA/CENSIPAM, UrbVerde e BDiA.

Riscos: indicadores compostos, atualização por produto, visualizador versus download, escala cartográfica, protocolos sem documentação e papéis dos links.

### BR5

HidroWeb, BIEN, Global Carbon Atlas, Copernicus Data Space Ecosystem, ILTER, ORNL DAAC e Project COSMOS.

Riscos: qualidade de séries de estações, generalização entre datasets e sítios, API de metadados versus arquivos, ferramentas versus protocolos, processamento, autenticação, DOI, licença e base integral versus interface pública.

O Project COSMOS é bibliométrico e não fornece medições ambientais diretas. Sua permanência exige decisão futura de escopo; a auditoria interna não autoriza exclusão automática.

As 35 fontes permanecem internamente coerentes com ressalvas e com decisão `manter_csv_atual` até revisão oficial com evidência, data e revisor.

## Controles técnicos

`migration/br_batch_registry.json` controla ordem, contratos e matrizes.

`scripts/validate_br_batches.py` valida sete fontes por lote, IDs exclusivos, correspondência com CSV, DATA1-B e DATA1-BX, URLs existentes e bloqueios de evidência.

`scripts/validate_br_completion.py` confirma que BR1–BR5 cobrem exatamente os 35 IDs `revisão_manual` e que os 16 registros prontos permanecem fora dos lotes.

`scripts/audit_link_roles.py` controla a distinção entre página institucional, acesso aos dados e documentação técnica. Igualdade ou diferença superficial entre URLs não autoriza correção automática.

## Resolução e conteúdo didático

RES1 deve distinguir célula raster, escala cartográfica, precisão, suporte espacial, resolução temporal e zoom. EDU1 deve explicar fenômenos, medição, tipos de dados e limitações. Ambos permanecem P3 e não bloqueantes, salvo quando revelarem erro factual.

## Próxima execução

1. consolidar BR1–BR5 em uma fila única de revisão externa;
2. ordenar as fontes por risco, impacto e documentação necessária;
3. executar a revisão factual quando houver acesso oficial atual;
4. não iniciar DATA1-C enquanto decisões críticas estiverem bloqueadas;
5. preservar CSV 51 × 34, versão 0.7.0, candidatos externos e DOI bloqueado.

Consulte os contratos e matrizes BR1–BR5, `migration/data1bx_migration_matrix.csv`, `METHODOLOGY.md`, `CODEBOOK.md`, `QUALITY_CORRECTION_WORKFLOW.md` e `FINAL_OBJECTIVES_AND_DOI_GATES.md`.
