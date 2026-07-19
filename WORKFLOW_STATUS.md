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
- A revisão externa das fontes exige acesso atual à documentação oficial; nenhum caso será declarado resolvido apenas por inferência a partir do CSV existente.

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
| OBJ | Objetivos finais e portões para DOI | concluído | PR #17; run 29704132742; commit 894be4f17a7e78f521acddf5fab12ef21086db01; Drive atualizado |
| DATA1-A | Auditoria e projeto do esquema 0.8.0 | validado e documentado | PR #13; run 29702732587; Drive atualizado |
| DATA1-B | Matriz de migração das 51 fontes | validado e documentado | PR #15; run 29703654373; Drive atualizado |
| DATA1-BR | Revisão dos 35 casos pendentes | autorizado | cinco lotes de sete registros; evidência oficial obrigatória |
| DATA1-C | Migração atômica para 38 campos | bloqueado | depende da resolução dos 35 casos em revisão manual |
| DATA1-D | Validações cruzadas do esquema 0.8.0 | planejado | inconsistências semânticas bloqueiam o build |
| DATA2 | Revisar as 51 fontes no esquema final | planejado | cada lote tem evidência, diff, validação e changelog |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 integrado, CI aprovado e Drive atualizado |
| RELEASE2 | Criar versão `1.0.0` | bloqueado | G1-G10 concluídos e release preparada |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | G1-G12 concluídos e depósito inspecionado |
| POST-DOI | Propagar DOI de versão e conceito | bloqueado | repositório, site, ORCID e currículos atualizados |

## Estado consolidado

- **Versão formal:** 0.7.0;
- **Fontes:** 51;
- **Campos canônicos atuais:** 34;
- **UX1–UX4:** integrados e validados;
- **DATA1-A:** integrado e validado;
- **DATA1-B:** integrado e validado;
- **G1 — escopo científico:** concluído;
- **G2–G12:** parciais ou bloqueados;
- **Matriz:** 16 registros prontos e 35 em revisão manual;
- **Esquema 0.8.0:** ainda não aplicado;
- **Publicação atual:** ainda não confirmada por inspeção direta;
- **v1.0.0:** bloqueada;
- **DOI:** bloqueado e não criado.

## Objetivos finais — resultado

- **PR:** #17 — `Definir objetivos finais e portões antes do DOI`;
- **Commit integrado:** `894be4f17a7e78f521acddf5fab12ef21086db01`;
- **Validação:** GitHub Actions run `29704132742`, sucesso;
- **Contrato científico:** `FINAL_OBJECTIVES_AND_DOI_GATES.md`;
- **Contrato legível por máquina:** `release/doi_readiness.json`;
- **Portões:** G1-G12;
- **G1:** concluído;
- **Drive:** fase registrada na aba `project_changelog`;
- **Proteção:** versão formal permanece 0.7.0 e `doi_allowed` permanece `false`.

## DATA1-BR — lotes autorizados

Os 35 registros em revisão manual estão em `migration/data1br_review_batches.csv`:

- **BR1:** sete fontes brasileiras e subnacionais com lacunas de formato, protocolo ou atualização;
- **BR2:** sete portais e sistemas nacionais/regionais com classificação ou acesso a confirmar;
- **BR3:** sete infraestruturas com ferramentas, protocolos ou formatos não especificados;
- **BR4:** sete redes, catálogos e bases globais com exceções técnicas;
- **BR5:** sete plataformas e recursos globais com classificação, acesso ou escopo a resolver.

Nenhum lote está marcado como revisado. Cada registro exige documentação oficial atual antes de alterar a matriz.

## Próxima execução

1. executar BR1 com documentação oficial;
2. atualizar matriz, confiança, exceções e status somente com evidência;
3. repetir BR2-BR5;
4. exigir 51 registros `pronto_para_migração`;
5. autorizar DATA1-C somente após esse critério.

Consulte `FINAL_OBJECTIVES_AND_DOI_GATES.md`, `IMPLEMENTATION_WORKFLOW.md`, `DATA1_SCHEMA_AUDIT.md` e `migration/README.md`.
