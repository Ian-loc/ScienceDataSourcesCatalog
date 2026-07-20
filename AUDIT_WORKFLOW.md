# Workflow de verificação do catálogo

## Governança

`data/data_resources.csv` é a única fonte canônica. O JSON do site é gerado no build. O Drive mantém somente changelog executivo e histórico.

## Preparação

1. localizar a fonte na fila `migration/external_review_queue.csv`;
2. confirmar se existe portão de escopo ou relação de duplicidade;
3. revisar o foco herdado do lote BR;
4. não editar o CSV antes de registrar evidências e decisão.

## Revisão por fonte

1. confirmar nome, identidade, objetivo, função e responsável;
2. testar homepage, acesso aos dados e documentação técnica separadamente;
3. conferir produtos, formatos, visualizações, cobertura, versão e atualização;
4. distinguir download, API/protocolo, ferramenta cliente, autenticação e restrições;
5. verificar resolução, escala ou suporte no nível do produto;
6. conferir licença, orientação de citação e atribuição da fonte original;
7. localizar literatura representativa de uso ou avaliação;
8. registrar limitações, sobreposição e incerteza;
9. atualizar `last_verified` somente após decisão canônica aprovada.

## Evidência em formato longo

Cada linha de `migration/external_review_evidence.csv` sustenta uma afirmação específica. Registrar:

- `resource_id`, dimensão e afirmação;
- valor atual e valor observado;
- URL, tipo de evidência e fonte oficial;
- data e revisor;
- se a evidência sustenta o valor atual;
- ação e valor propostos;
- limitações.

Uma fonte pode exigir várias linhas. Uma homepage não comprova automaticamente API, licença, formato, resolução ou atualização.

## Decisão

- `manter`: evidência sustenta o valor;
- `corrigir`: evidência oficial contradiz o valor e há proposta explícita;
- `marcar_desconhecido`: informação insuficiente;
- `documentar_variabilidade`: atributo varia por dataset, produto, sítio ou coleção;
- `avaliar_exclusão_ou_fusão`: problema de elegibilidade, sucessão ou duplicidade.

Nenhuma decisão é aplicada automaticamente ao CSV.

## Controle automático

```bash
python3 scripts/validate_quality_correction_plan.py
python3 scripts/validate_candidate_queue.py
python3 scripts/build_catalog.py
python3 scripts/audit_link_roles.py
python3 scripts/validate_schema_draft.py
python3 scripts/validate_migration_matrix.py
python3 scripts/validate_data1bx_matrix.py
python3 scripts/load_data1bx_from_canonical.py
python3 scripts/validate_br_batches.py
python3 scripts/validate_br_completion.py
python3 scripts/validate_external_review_evidence.py
python3 scripts/validate_external_review_queue.py
python3 scripts/validate_doi_readiness.py
python3 scripts/validate_frontend.py
```

## Frequência

- trimestral: links, acesso, autenticação e disponibilidade;
- anual: conteúdo, evidência acadêmica, versões e áreas;
- imediata: mudança de licença, API, formato, cobertura ou responsável;
- por pull request: validação estrutural e inspeção científica do diff.

Respostas 401, 403 e 429 não provam indisponibilidade para usuários; podem refletir autenticação, cotas ou bloqueio a robôs.
