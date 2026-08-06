# Política de marcos e pacotes de execução

A partir do Marco 1 da Instância 1, o desenvolvimento do Simbiotrama deve operar por pacotes cientificamente coerentes e revisáveis.

## Regras

1. Todo pacote parte da `main` corrente.
2. Cada pacote recebe branch e pull request próprios.
3. Famílias independentes não são misturadas no mesmo PR.
4. Alterações estruturais transversais são isoladas.
5. Cada PR declara critério de completude antes do merge.
6. O delta é auditado e corrigido antes do congelamento do head.
7. O CI deve estar verde no SHA exato a ser incorporado.
8. Não pode haver revisão contrária ou thread aberta.
9. Merge exige autorização humana explícita.
10. Squash merge é preferido para preservar a legibilidade da `main`.

## Escala recomendada

Um PR deve representar, preferencialmente:

- uma família de produtos;
- um pequeno conjunto de produtos estreitamente relacionados;
- ou uma única alteração transversal indispensável.

A revisão das fontes legadas, o aprofundamento de famílias científicas e mudanças de arquitetura não devem ser combinados sem dependência explícita e demonstrada.
