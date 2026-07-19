# Workflow de implementação — interface, conteúdo, governança e release

## Objetivo

Melhorar a descoberta e comparação de fontes, corrigir ambiguidades documentais e preparar uma primeira versão científica estável e arquivável, sem misturar redesign, revisão científica do CSV e publicação com DOI no mesmo ciclo.

## Princípios

1. busca e decisão do usuário vêm antes da documentação institucional;
2. a página pública é atualizável; cada versão científica citável deverá ser arquivada como objeto imutável;
3. `data/data_resources.csv` é a fonte canônica;
4. JSON e metadados do site são derivados do CSV;
5. o Drive é registro histórico e changelog executivo, não fonte de publicação;
6. mudanças de interface não alteram silenciosamente o conteúdo científico;
7. nenhuma etapa é marcada como publicada sem evidência do site resultante;
8. `1.0.0` e DOI somente serão criados após fechamento técnico, científico e documental;
9. o depósito final deverá representar a contribuição principal como **Dataset**;
10. manter apenas `CITATION.cff`, salvo necessidade concreta de `.zenodo.json`;
11. licenças de código e dados devem permanecer materialmente separadas.

## Título oficial

**Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão**

## Ciclos

| Ciclo | Escopo | Estado | Critério de conclusão |
|---|---|---|---|
| UX1 | Arquitetura, linguagem e navegação | validado e documentado | PR #5 e run 29700737238 concluídos |
| UX2 | Filtros e resultados | validado e documentado | PR #7 e run 29701061221 concluídos |
| UX3 | Redesenho dos cards | validado e documentado | PR #9 e run 29701341054 concluídos |
| UX4 | Acessibilidade, responsividade e desempenho | validado e documentado | PR #11 e run 29702280394 concluídos |
| DATA1-A | Auditoria e projeto do esquema | em desenvolvimento | proposta 0.8.0 documentada e validada sem alterar o CSV |
| DATA1-B | Matriz de migração | planejado | decisão por registro com confiança e justificativa |
| DATA1-C | Migração para 38 campos | bloqueado | depende de DATA1-A e DATA1-B validados |
| DATA1-D | Validação semântica e interface | planejado | regras cruzadas e exibição dos 38 campos aprovadas |
| DATA2 | Revisão das 51 fontes | planejado | lotes auditáveis com evidência, diff, validação e changelog |
| RELEASE1 | Fechamento documental | validado e documentado | título, ORCID, licenças e CFF integrados no PR #5 |
| RELEASE2 | Versão estável | bloqueado | trabalho não lançado encerrado; site, CSV e metadados verificados |
| DOI | Arquivamento no Zenodo | bloqueado | release `v1.0.0` depositada como Dataset e metadados conferidos |
| POST-DOI | Propagação dos identificadores | bloqueado | DOI de versão e conceito no repositório, site, ORCID e currículos |

## UX1–UX4 — resultado

- [x] busca, navegação e exploração temática;
- [x] filtros, contagens, ordenação e URLs compartilháveis;
- [x] cards orientados à decisão com todos os campos preservados;
- [x] acessibilidade estrutural, movimento reduzido, alto contraste e fallback sem JavaScript;
- [x] orçamento máximo de 120 KB e ausência de dependências externas;
- [x] GitHub Actions e Drive atualizados em cada ciclo;
- [ ] confirmar visualmente o site e o commit exibido no build.

## DATA1-A — auditoria do esquema

### Entregas implementadas

- [x] leitura integral dos 34 campos e das 51 fontes;
- [x] diagnóstico de mistura entre formatos, protocolos, ferramentas e notas;
- [x] distinção entre `official_identity` e tipo funcional controlado;
- [x] proposta mínima de 38 campos;
- [x] novos campos: `resource_type`, `geographic_scope`, `access_tools`, `citation_guidance_url`;
- [x] vocabulário de dez tipos funcionais;
- [x] vocabulário de oito escalas geográficas;
- [x] classificação preliminar das 51 fontes;
- [x] vocabulários iniciais para formatos, protocolos, ferramentas, origem e situação institucional;
- [x] 14 regras de validação cruzada;
- [x] contrato em `schema/v0.8.0-draft.json`;
- [x] teste em `scripts/validate_schema_draft.py`;
- [x] bloqueio explícito de migração automática, DOI e alteração prematura do CSV;
- [ ] validar em pull request;
- [ ] integrar após CI aprovado;
- [ ] registrar no Drive.

### Decisões centrais

1. a unidade de registro permanece `source`, não dataset;
2. `dataset` não integra o vocabulário de `resource_type`;
3. a autodescrição oficial nunca é substituída pela classificação curatorial;
4. `geographic_scope` guarda a classe; `geographic_coverage` preserva o detalhe;
5. `data_formats` aceita somente formatos e placeholders documentados;
6. protocolos técnicos permanecem em `access_protocols`;
7. pacotes, clientes e ambientes migram para `access_tools`;
8. não haverá campo DOI genérico para fontes; a orientação oficial será registrada por URL;
9. a migração alvo é 0.8.0, ainda sem DOI.

## DATA1-B — matriz de migração

A matriz deve conter, para cada `resource_id`:

- `resource_type_current_basis`;
- `resource_type_proposed`;
- `geographic_scope_proposed`;
- normalização proposta de `data_formats`;
- normalização proposta de `access_protocols`;
- conteúdo proposto de `access_tools`;
- normalização de `institutional_status`;
- `citation_guidance_url` quando confirmada;
- nível de confiança: `alta`, `média` ou `baixa`;
- justificativa e evidência.

Casos de confiança média ou baixa exigem revisão manual antes da migração.

## DATA1-C — migração atômica 0.8.0

Somente após DATA1-A e DATA1-B:

1. atualizar o cabeçalho para 38 campos;
2. migrar as 51 linhas em uma única branch;
3. atualizar `CODEBOOK.md`, metodologia, scripts e interface;
4. preservar os 51 IDs;
5. impedir perda de qualquer informação científica;
6. atualizar `CITATION.cff` para `0.8.0` apenas junto à migração;
7. validar e registrar no Drive;
8. não criar DOI.

## DATA1-D — validação semântica

Implementar regras que bloqueiem:

- acesso programático positivo sem protocolo ou ferramenta;
- download gratuito sem URL de acesso;
- autenticação positiva sem condição correspondente;
- formatos contendo APIs, OGC, mapas ou visualizações;
- protocolos contendo pacotes ou clientes;
- placeholders combinados com valores positivos;
- escala `global` contraditória com cobertura do Brasil, sem justificativa;
- escala `not_applicable` com cobertura geográfica positiva;
- URLs de citação que não sejam HTTPS.

## RELEASE1 — resultado

- [x] `type: dataset`, ORCID, versão e data adequados;
- [x] `LICENSE-DATA.md` e separação de licenças;
- [x] ausência deliberada de `.zenodo.json`;
- [x] política de inserção posterior do DOI documentada.

## Condições obrigatórias para `v1.0.0`

1. encerrar os blocos não lançados no changelog;
2. validar CSV e artefatos derivados;
3. verificar o site e o commit exibido no build;
4. concluir UX1–UX4;
5. concluir DATA1 e a revisão mínima das 51 fontes;
6. validar título, autor, ORCID, licenças, versão e data;
7. alterar `CITATION.cff` para `version: "1.0.0"` somente no dia da release;
8. criar tag e GitHub Release `v1.0.0`;
9. testar se GitHub–Zenodo preserva o tipo Dataset;
10. se necessário, realizar depósito manual classificado como Dataset;
11. conferir arquivos e metadados antes da publicação;
12. inserir DOI de versão e DOI de conceito no repositório ativo.

## Citação planejada

> LARA, Ian. *Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Versão 1.0.0. Zenodo, 2026. DOI: [DOI da versão].

## Ordem operacional atual

1. validar e integrar DATA1-A;
2. produzir e revisar DATA1-B;
3. migrar atomicamente para 0.8.0 em DATA1-C;
4. concluir validações e interface em DATA1-D;
5. executar DATA2 em lotes;
6. confirmar publicação e fechar documentação;
7. somente então criar `v1.0.0` e o depósito no Zenodo.
