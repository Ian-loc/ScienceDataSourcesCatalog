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
- A inspeção externa do GitHub Pages ainda não fornece evidência direta do conteúdo publicado.

## Backlog

| Prioridade | Frente | Estado | Evidência ou critério de conclusão |
|---|---|---|---|
| P0 | Identificação verificável do build | integrado | `build-meta.json` contém versão, commit, data, fontes e campos |
| P0 | Impedir versionamento de artefatos derivados | concluído | `.gitignore` cobre JSON, metadados de build e cache Python |
| P0 | Confirmar deploy posterior ao merge | bloqueado | requer inspeção direta do site ou evidência do run de push da `main` |
| UX1 | Arquitetura, linguagem e navegação | validado e documentado | PR #5; run 29700737238; Drive atualizado |
| UX2 | Filtros e resultados | validado e documentado | PR #7; run 29701061221; Drive atualizado |
| UX3 | Redesenho dos cards | em desenvolvimento | branch implementada; falta PR, validação, integração e Drive |
| UX4 | Acessibilidade, responsividade e desempenho | planejado | teclado, contraste, mobile, carregamento e testes verificados |
| DATA1 | Restaurar `resource_type` e escala controlada | planejado | esquema, CSV, codebook, validação e interface atualizados |
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

## Ciclo atual — UX3

- **Branch:** `agent/ux3-card-redesign`;
- **Escopo:** reorganização visual e semântica dos cards, sem alterar `data/data_resources.csv`;
- **Implementado:** identidade secundária, estados de acesso, utilidade e limitação em destaque, ações priorizadas e seis grupos técnicos;
- **Preservação:** todos os 34 campos e todos os links continuam disponíveis na interface;
- **Pendente:** PR, CI, integração, registro no Drive e verificação do site.

Consulte `IMPLEMENTATION_WORKFLOW.md` para a sequência completa até a release estável e o Zenodo.
