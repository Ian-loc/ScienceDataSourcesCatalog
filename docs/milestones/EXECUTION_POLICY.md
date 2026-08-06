# Política de marcos e pacotes de execução

O desenvolvimento do Simbiotrama opera por pacotes coerentes, pequenos e revisáveis.

## 1. Preparação obrigatória

1. consultar a `main` e registrar o SHA;
2. criar branch própria;
3. confirmar que a branch existe;
4. somente então executar a primeira escrita;
5. interromper diante de `branch not found` ou ref ambígua;
6. nunca usar `main` como fallback de escrita.

## 2. Regras do pacote

1. cada pacote recebe branch e PR próprios;
2. cada PR possui uma entrega pública ou operacional identificável;
3. alteração arquitetural, curadoria de entradas e interface devem ser separadas quando independentes;
4. o critério de completude e de parada é declarado antes da implementação;
5. nova entidade ou coluna deve passar pelo gate de escopo;
6. o delta é auditado e corrigido antes do congelamento;
7. CI deve estar verde no SHA final;
8. revisão deve estar concluída;
9. não pode haver thread acionável aberta;
10. merge exige autorização humana explícita do SHA exato;
11. squash merge é preferido.

## 3. Escala recomendada

Um PR deve representar preferencialmente:

- uma alteração transversal indispensável;
- uma migration coerente;
- um lote pequeno de entradas relacionadas;
- um exportador ou componente de interface isolado;
- um conector selecionado da Instância 2, quando essa instância estiver ativa.

“Uma fonte inteira” ou “um produto inteiro” não define automaticamente o tamanho do PR. O pacote deve ser dividido quando diferentes riscos puderem ser revisados separadamente.

## 4. Pacotes da Instância 1

### Arquitetura

- políticas e contratos;
- migrations aditivas;
- staging e crosswalk;
- exportações.

### Curadoria

- lotes de 5 a 10 entradas após validação do modelo;
- evidência proporcional;
- revisão de granularidade e duplicidade.

### Interface

- busca;
- filtros;
- ficha de entrada;
- links oficiais;
- exportação de metadados.

Não misturar desenvolvimento da Instância 2 ou 3 com a Instância 1 sem dependência formal.

## 5. Gate de escopo

Toda mudança deve demonstrar necessidade para:

- descoberta;
- interpretação mínima;
- filtro/exibição no website;
- conector selecionado.

Sem caso de uso concreto, a proposta permanece no backlog.

## 6. Relatório

Cada pacote registra:

- base e head;
- arquivos alterados;
- entrega e limites;
- testes;
- revisão e threads;
- ocorrências;
- estados negativos;
- próximo gate;
- necessidade de autorização.

O relatório não substitui o avanço material nem autoriza merge.
