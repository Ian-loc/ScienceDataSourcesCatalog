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

- GitHub Issues está desativado neste repositório; este arquivo é o backlog versionado autoritativo.
- O conector disponível confirma runs associados a pull requests, mas não expõe o run disparado por push na `main`.
- A inspeção externa do GitHub Pages ainda não fornece evidência direta do conteúdo publicado.

## Backlog

| Prioridade | Frente | Estado | Evidência ou critério de conclusão |
|---|---|---|---|
| P0 | Identificação verificável do build | integrado | `build-meta.json` contém versão, commit, data, fontes e campos |
| P0 | Impedir versionamento de artefatos derivados | concluído | `.gitignore` cobre JSON, metadados de build e cache Python |
| P0 | Confirmar deploy posterior ao merge | bloqueado | requer inspeção direta do site ou evidência do run de push da `main` |
| UX1 | Arquitetura, linguagem e navegação | validado e documentado | PR #5 integrado; run 29700737238 concluído; Drive atualizado |
| UX1 | Confirmar publicação da interface | bloqueado | site deve exibir commit compatível com a `main` |
| UX2 | Filtros e resultados | em desenvolvimento | branch implementada; falta PR, validação, integração e registro no Drive |
| UX3 | Redesenho dos cards | planejado | cards curtos, estados claros e detalhes agrupados |
| UX4 | Acessibilidade, responsividade e desempenho | planejado | teclado, contraste, mobile, carregamento e testes verificados |
| DATA1 | Restaurar `resource_type` e escala controlada | planejado | esquema, CSV, codebook, validação e interface atualizados |
| DATA1 | Normalizar formatos, protocolos e citações | planejado | campos não misturam formatos, visualizações e notas livres |
| DATA1 | Ampliar validações cruzadas | planejado | inconsistências semânticas bloqueiam o build |
| DATA2 | Revisar as 51 fontes em lotes auditáveis | planejado | cada lote tem evidência, diff, validação e changelog |
| RELEASE1 | Título, ORCID, licenças e CFF | validado e documentado | PR #5 integrado, CI aprovado e Drive atualizado |
| RELEASE2 | Criar versão `1.0.0` | bloqueado | trabalho não lançado encerrado e site/CSV/metadados verificados |
| DOI | Arquivar no Zenodo como Dataset | bloqueado | release estável publicada e metadados conferidos |
| POST-DOI | Propagar DOI de versão e conceito | bloqueado | repositório, site, ORCID e currículos atualizados |

## Ciclo UX1 + RELEASE1 documental — resultado

- **PR:** #5;
- **Commit integrado:** `678d7e716bf31c856bc70c3b028b23457c6f537f`;
- **Validação:** run `29700737238`, sucesso;
- **Conteúdo científico:** CSV canônico não alterado;
- **Drive:** fase registrada;
- **Publicação:** ainda não confirmada por evidência direta;
- **DOI:** não criado.

## Ciclo atual — UX2

- **Branch:** `agent/ux2-filters-results`;
- **Escopo:** filtros essenciais e avançados, ordenação, filtros ativos e URL compartilhável;
- **Implementado:** contagens por opção, filtros por cobertura/formato/evidência, ordenação por relevância/nome/verificação, remoção individual de filtros e persistência na URL;
- **Conteúdo científico:** `data/data_resources.csv` não alterado;
- **Pendente:** PR, CI, revisão, integração, verificação do site e registro no Drive.

Consulte `IMPLEMENTATION_WORKFLOW.md` para a sequência completa até a release estável e o Zenodo.
