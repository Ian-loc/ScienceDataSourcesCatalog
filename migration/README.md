# Matrizes de migração DATA1

## Finalidade

A migração do esquema 0.7.0 para 0.8.0 é preparada sem substituir o CSV canônico:

- `data1b_migration_matrix.csv`: tipo funcional, escala, formatos, protocolos, ferramentas e situação institucional;
- `data1bx_migration_matrix.csv`: produtos, visualizações, fontes dos dados, resolução temporal e condições de acesso;
- `br_batch_registry.json`: ordem e estado dos lotes de revisão manual;
- `br1_review_matrix.csv` e `br2_review_matrix.csv`: auditorias internas aprofundadas.

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

1. CEMADEN (`DR0005`);
2. dados.gov.br (`DR0008`);
3. MapBiomas (`DR0010`);
4. TerraBrasilis (`DR0011`);
5. BDQueimadas (`DR0012`);
6. Google Earth Engine (`DR0019`);
7. Global Forest Watch (`DR0044`).

Riscos dominantes: heterogeneidade por produto, agregação de terceiros, acesso e licença variáveis, temporalidade, protocolos e semântica de alertas, focos, incêndios, áreas queimadas e desmatamento.

### BR2 — biodiversidade, ciência cidadã e redes de dados

1. speciesLink (`DR0013`);
2. SiBBr (`DR0014`);
3. eBird (`DR0027`);
4. Movebank (`DR0028`);
5. DataONE (`DR0030`);
6. iNaturalist (`DR0034`);
7. TRY (`DR0040`).

Riscos dominantes: duplicação entre redes, distinção entre agregador e fonte primária, licença por registro ou dataset, coordenadas sensíveis, viés amostral, produtos brutos versus modelados, qualidade taxonômica, acesso por solicitação e termos dos contribuidores.

## Interpretação da auditoria interna

Cada matriz BR registra:

- justificativa e prioridade;
- flags de risco;
- achados de consistência interna;
- URLs já existentes no CSV;
- dimensões que exigem documentação oficial;
- estado factual externo;
- decisão conservadora sobre o CSV.

A auditoria interna não equivale a validação factual. Enquanto `external_review_status` for `bloqueada_sem_web`, a linha não pode receber nova URL de evidência, revisor, data, confiança elevada ou decisão de correção.

## Validação

Execute:

```bash
python3 scripts/validate_migration_matrix.py
python3 scripts/validate_data1bx_matrix.py
python3 scripts/load_data1bx_from_canonical.py
python3 scripts/validate_br_batches.py
```

Para compatibilidade, `python3 scripts/validate_br1_matrix.py` valida somente BR1 por meio do validador comum.

O validador dos lotes confere registro, contratos, matrizes, ordem, exclusividade dos IDs, URLs existentes, estado manual em DATA1-B, confiança desconhecida em DATA1-BX e bloqueios de evidência.

## Estado protegido

- CSV canônico: 51 fontes × 34 campos;
- versão formal: 0.7.0;
- esquema 0.8.0: proposta não aplicada;
- DATA1-BX: projeção concluída, confiança externa desconhecida;
- BR1 e BR2: auditorias internas concluídas; revisões factuais externas bloqueadas;
- 14 dos 35 casos manuais distribuídos em lotes;
- candidatos: fora do CSV;
- DOI: bloqueado.
