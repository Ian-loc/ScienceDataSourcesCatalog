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
| DATA1 | Restaurar `resource_type` e escala controlada | autorizado | iniciar auditoria do esquema, vocabulários e regras de migração |
| DATA1 | Normalizar formatos, protocolos e citações | planejado | campos não misturam formatos, visualizações e notas livres |
| DATA1 | Ampliar validações cruzadas | planejado | inconsistências semânticas bloqueiam o build |
| DATA2 | Revisar as 51 fontes em lotes auditáveis | planejado | cada lote tem evidência, diff, validação e changelog |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 integrado, CI aprovado e Drive atualizado |
| RELEASE2 | Criar versão `1.0.0` | bloqueado | trabalho não lançado encerrado e site/CSV/metadados verificados |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | release estável publicada e metadados conferidos |
| POST-DOI | Propagar DOI de versão e conceito | bloqueado | repositório, site, ORCID e currículos atualizados |

## UX1 + RELEASE1 documental — resultado

- **PR:** #5;
- **Commit:** `678d7e716bf31c856bc70c3b028b23457c6f537f`;
- **Validação:** run `29700737238`, sucesso;
- **CSV:** não alterado;
- **Drive:** registrado;
- **Publicação:** não confirmada;
- **DOI:** não criado.

## UX2 — resultado

- **PR:** #7;
- **Commit:** `a212192174c354508eaf48dea30a81faa5311ae5`;
- **Validação:** run `29701061221`, sucesso;
- **CSV:** não alterado;
- **Drive:** registrado;
- **Publicação:** não confirmada.

## UX3 — resultado

- **PR:** #9;
- **Commit:** `eec289ee5036848fa836c43e7dcd088b47da3710`;
- **Validação:** run `29701341054`, sucesso;
- **CI:** exige referência aos 34 campos;
- **CSV:** não alterado;
- **Drive:** registrado;
- **Publicação:** não confirmada.

## UX4 — resultado

- **PR:** #11 — `Concluir acessibilidade, responsividade e desempenho`;
- **Commit integrado:** `70d2cb868054c551c9aaf2d41ea9fbdb8eef58f1`;
- **Validação:** GitHub Actions run `29702280394`, sucesso;
- **Implementado:** landmarks, fieldsets, foco previsível, estados de carregamento, fallbacks sem JavaScript, movimento reduzido, alto contraste e breakpoints adicionais;
- **Desempenho:** orçamento total máximo de 120 KB e proibição de dependências externas de scripts e estilos;
- **CSV:** `data/data_resources.csv` não foi alterado;
- **Drive:** fase registrada na aba `project_changelog`;
- **Publicação:** ainda não confirmada por evidência direta do site.

## Próximo ciclo autorizado

O próximo ciclo é **DATA1 — fortalecimento estrutural do esquema**. A primeira etapa deve ser uma auditoria completa dos 34 campos, dos valores existentes e dos vocabulários propostos antes de qualquer migração do CSV.

Consulte `IMPLEMENTATION_WORKFLOW.md` para a sequência completa até a release estável e o Zenodo.
