# Estado do workflow

## Regra operacional

Uma tarefa só é concluída após branch, pull request, integração à `main`, GitHub Actions verde e registro no changelog. Alterações públicas também exigem confirmação do deploy.

CI verde comprova estrutura e coerência interna. Não comprova atualidade, acesso ou correção factual das fontes externas.

## Limitações

- revisão externa bloqueada nas matrizes BR1–BR5 até que cada linha receba documentação oficial atual, URL de evidência, data e revisor;
- auditoria interna e pontuação de prioridade não elevam confiança nem autorizam correções no CSV;
- URLs iguais em `homepage_url` e `data_access_url` permanecem pendentes;
- novas fontes permanecem fora do CSV até a estabilização das 51 atuais;
- versão 1.0.0 e DOI continuam bloqueados.

## Backlog

| Frente | Estado | Critério principal |
|---|---|---|
| DATA1-A | concluído | esquema 0.8.0 documentado |
| DATA1-B | concluído | 51 linhas classificadas |
| QC0 | concluído | 14 regras semânticas alinhadas |
| SELECT1 | concluído | inclusão, exclusão, duplicidade e lacunas documentadas |
| DATA1-BX | projeção concluída | 51 × 5 dimensões; confiança desconhecida |
| DATA1-BR | auditoria interna concluída | BR1–BR5 cobrem os 35 casos manuais |
| DATA1-BR-CLOSE | concluído | fila única priorizada e reproduzível para 35 fontes |
| DATA1-EXT/P0 | próximo checkpoint | revisão factual das sete prioridades máximas |
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
- fila externa: **35 fontes**, sendo **P0=7, P1=10, P2=11 e P3=7**;
- candidatos: **18 fora do CSV**;
- esquema 0.8.0: não aplicado;
- expansão, v1.0.0 e DOI: bloqueados.

## Fila DATA1-BR-CLOSE

`migration/external_review_queue.csv` consolida os cinco lotes. A prioridade é calculada com dados versionados:

- impacto da fonte;
- risco científico;
- quantidade de alertas de risco;
- quantidade de dimensões documentais a revisar;
- ausência de documentação de acesso;
- pendência na separação dos papéis dos links;
- necessidade de decisão explícita de escopo.

A pontuação serve para ordenar o trabalho. Ela não mede qualidade científica absoluta, importância institucional ou confiabilidade final da fonte.

### P0 — revisão imediata

1. Banco de Dados e Informações Ambientais — BDiA;
2. Global Carbon Atlas;
3. Sistema de Registro Nacional de Emissões — SIRENE;
4. IDE-SISEMA;
5. SiBBr;
6. AdaptaBrasil MCTI;
7. Project COSMOS.

BDiA e Global Carbon Atlas alcançam 95 pontos. SIRENE alcança 94. IDE-SISEMA, SiBBr, AdaptaBrasil e COSMOS completam o P0. O COSMOS recebe prioridade adicional porque sua permanência depende de decisão de escopo: é bibliométrico e não fornece medições ambientais diretas.

### Interpretação dos níveis

- **P0:** bloqueios mais críticos ou combinação máxima de impacto, risco e lacunas documentais;
- **P1:** alta prioridade para fontes amplamente usadas, redes complexas ou produtos com versões, autenticação e licenças variáveis;
- **P2:** revisão necessária, mas com menor combinação de bloqueios imediatos;
- **P3:** revisão obrigatória antes da migração, porém posterior aos grupos anteriores.

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

As 35 fontes permanecem com decisão `manter_csv_atual` até revisão oficial com evidência, data e revisor.

## Controles técnicos

- `migration/br_batch_registry.json`: ordem, contratos e matrizes BR1–BR5;
- `scripts/validate_br_batches.py`: valida cada lote;
- `scripts/validate_br_completion.py`: confirma cobertura exata dos 35 casos manuais;
- `migration/external_review_queue_contract.json`: pesos, faixas, desempate e regras da fila;
- `scripts/validate_external_review_queue.py`: recalcula pontuação, ordem, níveis e correspondência com os lotes;
- `scripts/audit_link_roles.py`: controla papéis de homepage, acesso e documentação técnica.

## Resolução e conteúdo didático

RES1 e EDU1 permanecem P3 e não bloqueantes. RES1 deve distinguir célula raster, escala cartográfica, precisão, suporte espacial, resolução temporal e zoom. EDU1 deve explicar fenômenos, medição, tipos de dados e limitações.

## Próxima execução

1. iniciar DATA1-EXT/P0 pelas sete fontes de prioridade máxima;
2. inspecionar documentação oficial atual e registrar evidência, data e revisor por fonte;
3. separar homepage, acesso aos dados e documentação técnica sem inferir URLs;
4. decidir explicitamente o escopo do Project COSMOS;
5. não iniciar DATA1-C enquanto decisões críticas estiverem bloqueadas;
6. preservar CSV 51 × 34, versão 0.7.0, candidatos externos e DOI bloqueado.

Consulte os contratos e matrizes BR1–BR5, `migration/external_review_queue.csv`, `migration/external_review_queue_contract.json`, `migration/data1bx_migration_matrix.csv`, `METHODOLOGY.md`, `CODEBOOK.md`, `QUALITY_CORRECTION_WORKFLOW.md` e `FINAL_OBJECTIVES_AND_DOI_GATES.md`.
