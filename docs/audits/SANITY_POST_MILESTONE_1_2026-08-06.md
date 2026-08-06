# Auditoria de sanidade pós-Marco 1

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Escopo:** autoridade, documentação, ciclo de vida, branches/PRs, backlog, legado e continuidade operacional  
**Base auditada:** `main` após os PRs #54 e #55

## 1. Objetivo

Reduzir ambiguidade e custo de manutenção antes do Marco 2A, sem apagar evidências históricas, enfraquecer gates científicos ou antecipar Instâncias 2 e 3.

## 2. Diagnóstico

### Achado A — governança materialmente desatualizada

A governança ainda descrevia o projeto como caminho ativo para o “Simbioscópio”, mantinha comparabilidade e relações entre entidades como extensão paralela e não refletia o PostgreSQL/PostGIS já incorporado como arquitetura de destino.

**Severidade:** alta para coerência normativa.  
**Disposição:** corrigida.

### Achado B — nomenclatura inconsistente

Documentos ativos alternavam `Symbiotrama`, `Simbiotrama` e `Simbioscópio`. O roadmap possuía nome de arquivo associado ao protótipo anterior.

**Severidade:** média.  
**Disposição:** `Simbiotrama` definido como nome canônico; o caminho antigo do roadmap foi mantido apenas como alias aposentado.

### Achado C — PR #53 incompatível com o núcleo relacional

O PR #53:

- partia de `main` anterior ao Marco 1;
- criava variáveis e passaportes em arquivos paralelos;
- tratava comparabilidade A–E como modelo operacional;
- usava família PRODES não resolvida como entrada;
- alterava CI para um workstream fora do foco ativo.

**Severidade:** alta para risco de regressão conceitual.  
**Disposição:** fechado como `superseded`, sem merge. Distinções úteis poderão ser reimplementadas seletivamente no modelo relacional.

### Achado D — documentação de marco excessivamente fragmentada

O PR #55 criou 16 arquivos para registrar um único marco, incluindo notas, checkpoints, ponteiros e autorizações já consolidados no registro principal.

**Severidade:** média para custo de manutenção e risco de divergência.  
**Disposição:** 12 arquivos transitórios removidos. Permanecem apenas:

- `README.md`;
- `INSTANCE_1_MILESTONE_1_2026-08-06.md`;
- `EXECUTION_POLICY.md`;
- `MILESTONE_STATUS.json`.

### Achado E — ausência de índice de ciclo de vida

O repositório não possuía uma única referência para distinguir trabalho ativo, backlog, legado operacional, material retirado e evidência histórica.

**Severidade:** alta para priorização e continuidade.  
**Disposição:** criado `docs/PROJECT_STATE.md`.

### Achado F — protótipo visual ainda funcional, mas semanticamente legado

`explorer.html` e `data/federated_layers.json` permanecem funcionais e protegidos por teto N0, porém contêm nomenclatura e classes da fase anterior.

**Severidade:** baixa enquanto congelados.  
**Disposição:** classificados como `LEGACY_OPERATIONAL`; preservados sem alterações públicas nesta limpeza. Novas capacidades analíticas permanecem proibidas.

### Achado G — contratos analíticos futuros ainda existem no schema

Os contratos de passaporte, comparabilidade e evidência científica são válidos como material de desenho, mas não pertencem ao modelo ativo.

**Severidade:** média se confundidos com autoridade.  
**Disposição:** classificados explicitamente como `BACKLOG`; preservados para evitar perda de desenho e permitir retomada futura governada.

## 3. Disposição consolidada

| Classe | Conteúdo |
|---|---|
| `ACTIVE` | Instância 1, núcleo relacional, staging, curadoria, gates, evidência e autoridade pública transitória |
| `BACKLOG` | Instâncias 2 e 3, receitas, relações, literatura, contratos analíticos futuros |
| `LEGACY_OPERATIONAL` | explorador visual N0, registro federado e interface estática simplificada |
| `RETIRED` / `SUPERSEDED` | PR #53, Fase 1 do Simbioscópio, classes universais de compatibilidade, branches substituídas |
| `HISTORICAL_EVIDENCE` | auditorias, ocorrências, PRs, commits, propostas e snapshots |

## 4. Mudanças executadas

- PR #53 fechado como substituído;
- tarefa recorrente bloqueada no sanity antes do Marco 2A;
- criado estado canônico do projeto;
- criado roadmap canônico do Simbiotrama;
- roadmap antigo convertido em alias aposentado;
- README, direção, decisão e governança harmonizados;
- changelog atualizado;
- documentação de marcos reduzida;
- validador científico ampliado para testar ciclo de vida e nomenclatura.

## 5. Itens deliberadamente não modificados

- dados científicos e CSVs públicos;
- esquema SQL e migrações;
- gates de PRODES, DETER, Dynamic World e TerraClass;
- auditorias e registros de ocorrências;
- GitHub Pages e arquivos públicos do explorador;
- planilhas do Drive;
- visibilidade ou estrutura administrativa do repositório.

## 6. Critério de saída

A limpeza estará pronta quando:

1. o diff estiver restrito a governança, documentação e validador;
2. o PR #53 estiver fechado;
3. não houver referências ativas que tratem Simbioscópio como workstream;
4. o roadmap canônico usar Simbiotrama;
5. a documentação de marcos não possuir arquivos transitórios redundantes;
6. o CI estiver verde no head exato;
7. nenhuma revisão contrária ou thread permanecer aberta.

## 7. Próxima ação após incorporação

Atualizar `agent/marco-2a-deter-cerrado` para a nova `main` e retomar exclusivamente o fechamento científico-operacional do DETER Cerrado.
