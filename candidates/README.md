# Fila de fontes candidatas

## Finalidade

`source_candidates.csv` registra recursos propostos para futura avaliação sem alterar o catálogo publicado. A fila implementa a política definida em `SELECTION_AND_COVERAGE_POLICY.md` e permanece separada de `data/data_resources.csv`.

Um registro na fila não significa que a fonte foi aprovada, verificada ou incluída no catálogo.

## Campos

- `candidate_id`: identificador interno no padrão `CAND0001`;
- `official_name`: nome apresentado pelo proponente, ainda sujeito a confirmação;
- `acronym`: sigla presumida;
- `homepage_url`: URL submetida para triagem;
- `candidacy_reason`: motivo de relevância potencial;
- `presumed_research_areas`: temas presumidos, separados por ` | `;
- `presumed_geographic_coverage`: cobertura presumida;
- `presumed_resource_type`: função presumida do recurso;
- `possible_duplication`: sobreposição potencial com fontes já catalogadas;
- `initial_evidence`: origem da indicação inicial;
- `evidence_status`: nível da evidência disponível;
- `priority`: prioridade de revisão;
- `decision`: decisão corrente;
- `review_status`: etapa da triagem;
- `added_date`: data de entrada na fila;
- `notes`: verificações ainda necessárias.

## Valores controlados

### `evidence_status`

- `user_submitted_url_only`: somente URL indicada pelo usuário;
- `official_page_located`: página oficial localizada, mas documentação ainda incompleta;
- `official_documentation_reviewed`: documentação oficial revisada;
- `insufficient_evidence`: evidência insuficiente ou contraditória.

### `priority`

- `alta`;
- `média`;
- `baixa`.

### `decision`

- `aguardar_evidência`;
- `incluir`;
- `excluir`;
- `fundir`.

### `review_status`

- `triagem_inicial`;
- `revisão_de_elegibilidade`;
- `revisão_de_completude`;
- `decisão_registrada`.

## Fluxo

1. registrar a indicação sem inferir dados ausentes;
2. verificar identidade, governança e função;
3. distinguir infraestrutura de dados de conteúdo apenas editorial;
4. comparar o candidato com fontes já catalogadas;
5. confirmar acesso, formatos, API, licença, citação, cobertura e limitações;
6. registrar decisão fundamentada;
7. migrar para o CSV canônico somente em um ciclo futuro de expansão autorizado.

## Primeiro candidato

O Our World in Data foi registrado como `CAND0001` com decisão `aguardar_evidência`. A triagem reconhece relevância potencial como agregador e plataforma de visualização, mas exige verificar a infraestrutura reutilizável de dados, a atribuição por dataset e a possível duplicidade com provedores primários.

## Validação

Execute:

```bash
python3 scripts/validate_candidate_queue.py
```

O teste verifica cabeçalho, IDs, URLs, valores controlados, separação do CSV canônico e coerência entre evidência, estado e decisão.
