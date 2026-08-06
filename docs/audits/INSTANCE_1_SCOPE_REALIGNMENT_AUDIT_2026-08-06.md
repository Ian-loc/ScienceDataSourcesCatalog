# Auditoria de realinhamento da Instância 1

**Projeto:** Simbiotrama — Catálogo de Dados Científicos do Brasil  
**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** I1-S1 — simplificação governada

## 1. Pergunta de auditoria

A arquitetura, a curadoria e o plano de trabalho atuais são proporcionais ao objetivo de entregar um catálogo funcional de fontes e ofertas de dados científicos?

## 2. Diagnóstico

Não. O Marco 1 incorporou uma arquitetura tecnicamente sólida, mas sua aplicação como obrigação universal levou a:

- decomposição excessiva em fonte, família, produto, release, distribuição e ativo;
- pesquisa forense de endpoints, bytes, schemas e checksums;
- reconstrução parcial dos catálogos externos;
- proliferação de JSONs e validadores específicos;
- critérios de completude difíceis de encerrar;
- PRs grandes e revisão tardia;
- métricas centradas em profundidade, não em utilidade pública.

O PR #57 materializou esse desvio. Seu conteúdo científico pode ser útil, mas seu desenho não deve ser repetido.

## 3. Decisão

A Instância 1 passa a ser um catálogo de granularidade mínima suficiente, centrado em `catalog_entry`.

Núcleo-alvo:

- `organizations`;
- `catalog_entries`;
- `entry_variables`;
- `entry_evidence`;
- `connector_profiles` opcional.

A estrutura profunda do Marco 1 será preservada durante a migração e poderá servir como extensão futura, mas deixa de definir completude.

## 4. Documentos revisados

- `README.md`;
- `CHANGELOG.md`;
- `METHODOLOGY.md`;
- `PRODUCT_CATALOG_MODEL.md`;
- `CODEBOOK.md`;
- `SELECTION_AND_COVERAGE_POLICY.md`;
- `database/README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`;
- `docs/GOVERNANCE.md`;
- roadmap e workflow de curadoria;
- decisões e política de escopo;
- template de PR;
- validador de direção.

## 5. Regras consolidadas

### Unidade de trabalho

Uma entrada de catálogo suficientemente descrita.

### Critério de parada

Encerrar quando a ficha é compreensível, os campos essenciais disponíveis estão sustentados, existe caminho oficial de acesso e os detalhes restantes não alterariam materialmente a apresentação pública.

### Regra de granularidade

Não criar nova entrada apenas por arquivo, layer, banda, formato, endpoint ou atualização técnica.

### Pesquisa

Priorizar página oficial e metadados diretos. Método, licença, citação e acesso são aprofundados proporcionalmente.

### Evidência

Registrar suporte suficiente para campos materiais, sem pacote forense por entrada.

### Expansão do esquema

Exigir caso de uso concreto para descoberta, interpretação mínima, filtro do website ou conector selecionado.

## 6. Casos de validação

- GEDI;
- DETER Cerrado;
- IBGE;
- ANA/SNIRH.

O modelo falha se exigir inventário integral ou perder informação necessária ao usuário.

## 7. Disposição do PR #57

- aberto;
- convertido novamente em draft;
- título alterado para indicar congelamento e candidatura a `superseded`;
- seis threads P2 permanecem abertas;
- nenhuma correção adicional deve ser feita no desenho antigo;
- autorização de merge anterior invalidada;
- fechamento depende de decisão humana explícita.

## 8. Ocorrência operacional

### Descrição

Durante a preparação do pacote, uma chamada de escrita foi direcionada à `main` antes da criação da branch e criou um arquivo com conteúdo provisório.

### Contenção

- o arquivo foi identificado imediatamente;
- foi removido no commit seguinte;
- nenhum conteúdo provisório permanece na árvore da `main`;
- os commits permanecem no histórico para transparência.

### Causa

Sequenciamento incorreto entre criação de branch e chamada à API de conteúdo.

### Controle preventivo

Para qualquer escrita futura:

1. consultar `main` e registrar o SHA;
2. criar a branch;
3. confirmar a branch por busca ou leitura;
4. somente então escrever;
5. nunca usar `main` como fallback de branch;
6. interromper após a primeira resposta `branch not found`;
7. auditar a árvore antes de continuar.

### Gravidade

Moderada para governança; impacto material final nulo após reversão imediata.

## 9. Validação

O novo gate `scripts/validate_scientific_direction.py` verifica:

- documentos e decisões vigentes;
- núcleo mínimo;
- marcos I1-S1 a I1-S7;
- critério de parada;
- plano de migração;
- quatro casos de validação;
- proibição de frases normativas aposentadas;
- preservação do schema profundo e staging;
- permanência do explorador legado em N0;
- validade dos contratos de backlog.

Uma tentativa de validação local por clone foi bloqueada por falha DNS do ambiente. O CI remoto permanece o gate executável autoritativo deste PR.

## 10. Estado do pacote

- documentação normativa: revisada;
- tarefa recorrente: atualizada;
- PR #57: congelado;
- PR #58: draft ativo;
- plano de migração: documentado;
- casos dourados: documentados;
- schema SQL mínimo: ainda não implementado;
- CI final: pendente;
- revisão do PR: pendente;
- merge: não autorizado.

## 11. Próxima unidade

Após CI verde e revisão do PR de direção:

1. corrigir qualquer achado;
2. congelar o head documental;
3. solicitar autorização de merge;
4. somente após incorporação, abrir pacote separado para migration aditiva do núcleo mínimo;
5. materializar os quatro casos sem pesquisa forense adicional.
