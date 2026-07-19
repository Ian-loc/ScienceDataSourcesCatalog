# Estado do workflow

## Regra operacional

Uma tarefa só é considerada concluída quando estiver:

1. implementada em branch;
2. revisada em pull request;
3. integrada à `main`;
4. validada pelo GitHub Actions;
5. publicada, quando afetar o site;
6. registrada no changelog do GitHub e no registro executivo do Google Drive.

Os estados usados são: `planejado`, `em desenvolvimento`, `em revisão`, `integrado`, `validado`, `publicado`, `documentado`, `bloqueado` e `concluído`.

## Limitações atuais

- GitHub Issues está desativado; este arquivo é o backlog versionado autoritativo.
- O conector confirma runs associados a pull requests, mas não expõe o run disparado por push na `main`.
- A publicação só será marcada como confirmada mediante inspeção direta do site ou evidência equivalente.
- A tentativa de inspeção direta após o UX4 falhou por indisponibilidade de resolução de rede; isso não constitui evidência de falha do site.

## Backlog

| Prioridade | Frente | Estado | Evidência ou critério de conclusão |
|---|---|---|---|
| P0 | Identificação verificável do build | integrado | `build-meta.json` contém versão, commit, data, fontes e campos |
| P0 | Impedir versionamento de artefatos derivados | concluído | `.gitignore` cobre JSON, metadados de build e cache Python |
| P0 | Confirmar deploy posterior ao merge | bloqueado | requer inspeção direta do site ou evidência do run de push da `main` |
| UX1 | Arquitetura, linguagem e navegação | validado e documentado | PR #5; run 29700737238; Drive atualizado |
| UX2 | Filtros e resultados | validado e documentado | PR #7; run 29701061221; Drive atualizado |
| UX3 | Redesenho dos cards | validado e documentado | PR #9; run 29701341054; Drive atualizado |
| UX4 | Acessibilidade, responsividade e desempenho | validado e documentado | PR #11; run 29702280394; Drive atualizado |
| UX4 | Confirmar publicação da interface | bloqueado | site deve exibir commit compatível com `70d2cb868054c551c9aaf2d41ea9fbdb8eef58f1` ou posterior |
| DATA1-A | Auditoria e projeto do esquema 0.8.0 | em desenvolvimento | documentos e contrato criados; falta PR, CI, integração e Drive |
| DATA1-B | Matriz de migração das 51 fontes | planejado | valor atual, valor proposto, confiança e justificativa por registro |
| DATA1-C | Migração atômica para 38 campos | bloqueado | depende da integração e revisão da auditoria e da matriz |
| DATA1-D | Validações cruzadas do esquema 0.8.0 | planejado | inconsistências semânticas bloqueiam o build |
| DATA2 | Revisar as 51 fontes em lotes auditáveis | planejado | cada lote tem evidência, diff, validação e changelog |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 integrado, CI aprovado e Drive atualizado |
| RELEASE2 | Criar versão `1.0.0` | bloqueado | trabalho não lançado encerrado e site/CSV/metadados verificados |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | release estável publicada e metadados conferidos |
| POST-DOI | Propagar DOI de versão e conceito | bloqueado | repositório, site, ORCID e currículos atualizados |

## UX1–UX4 — resultado consolidado

- **UX1:** PR #5, run `29700737238`;
- **UX2:** PR #7, run `29701061221`;
- **UX3:** PR #9, run `29701341054`;
- **UX4:** PR #11, run `29702280394`;
- **CSV:** permaneceu com 51 fontes e 34 campos durante todos os ciclos de interface;
- **Drive:** todos os ciclos foram registrados;
- **Publicação:** ainda não confirmada por inspeção direta;
- **DOI:** não criado.

## Ciclo atual — DATA1-A

- **Branch:** `agent/data1-schema-audit`;
- **Escopo:** auditoria integral dos 34 campos e das 51 linhas, sem alterar o CSV;
- **Documentação:** `DATA1_SCHEMA_AUDIT.md`;
- **Contrato preliminar:** `schema/v0.8.0-draft.json`;
- **Proposta mínima:** evolução de 34 para 38 campos;
- **Novos campos:** `resource_type`, `geographic_scope`, `access_tools`, `citation_guidance_url`;
- **Classificação:** dez tipos funcionais e oito escalas geográficas;
- **Validação:** `scripts/validate_schema_draft.py` impede migração prematura e exige a preservação de 51 fontes e 34 campos nesta fase;
- **Versão:** permanece 0.7.0;
- **Pendente:** PR, CI, integração e registro no Drive.

## Próxima etapa após DATA1-A

Criar a **matriz de migração por registro**. Nenhum valor das 51 linhas deve ser convertido antes de registrar valor atual, valor proposto, confiança e justificativa.

Consulte `IMPLEMENTATION_WORKFLOW.md` e `DATA1_SCHEMA_AUDIT.md` para a sequência completa.
