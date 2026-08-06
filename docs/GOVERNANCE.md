# Governança do Simbiotrama

## 1. Finalidade

O Simbiotrama é um catálogo relacional de fontes e ofertas de dados científicos. A fase ativa é a Instância 1 simplificada.

Visualização federada e contexto por literatura permanecem como Instâncias 2 e 3 em backlog.

## 2. Autoridade

1. `main`;
2. `docs/PROJECT_STATE.md`;
3. `docs/decisions/DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md`;
4. `docs/policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md`;
5. contrato da Instância 1, roadmap e workflow;
6. esquema simplificado quando incorporado;
7. CSV/JSON públicos durante a transição;
8. evidências e auditorias históricas.

Prompts, conversas, branches e PRs não incorporados não são autoridade.

## 3. Regime de mudança

Toda mudança deve seguir:

1. delimitar a entrada ou regra alterada;
2. justificar necessidade e granularidade;
3. declarar o que ficará fora do escopo;
4. partir da `main` corrente;
5. implementar delta pequeno;
6. validar estrutura, conteúdo e simplicidade;
7. auditar o diff;
8. abrir PR;
9. concluir revisão;
10. congelar o head;
11. obter autorização humana quando exigida;
12. incorporar preferencialmente por squash merge.

## 4. Gate de simplicidade

Antes de criar tabela, entidade, classificação ou relação, demonstrar:

- problema recorrente que ela resolve;
- por que campo simples ou JSON adicional não basta;
- por que não replica estrutura externa;
- aplicabilidade a mais de um caso;
- impacto sobre website, busca ou acesso;
- custo de curadoria e manutenção.

Sem essa justificativa, a estrutura não deve ser criada.

## 5. Gate de granularidade

Uma nova entrada requer diferença material de significado, modalidade, cobertura, período, método, finalidade ou acesso principal.

Não são justificativas suficientes:

- outro arquivo;
- formato;
- layer;
- banda;
- endpoint;
- diretório;
- tabela;
- data técnica;
- nome interno de download.

## 6. Gate de pesquisa

A pesquisa deve parar quando os campos essenciais estiverem sustentados.

Não é permitido prolongar curadoria para reconstruir genealogia, inventário de ativos ou documentação completa da plataforma.

Toda lacuna deve ser classificada como:

- desconhecida;
- não encontrada após busca delimitada;
- não aplicável;
- inacessível no ambiente atual;
- contraditória.

## 7. Gate de dados externos

A Instância 1 não pode:

- copiar ou armazenar datasets de terceiros;
- registrar caminho local permanente para dados externos;
- criar inventário integral de ativos;
- prometer preservação;
- atribuir ao Simbiotrama produção, hospedagem ou custódia externas.

Downloads temporários de validação devem ser descartados e não promovidos como acervo.

## 8. Gate de conectores

Conectores são opcionais e pertencem à preparação da Instância 2.

Cada conector deve estar associado a uma operação concreta e registrar somente a configuração necessária. Não deve gerar decomposição automática da entrada em arquivos, layers ou releases.

## 9. Gates humanos

Exigem autorização humana explícita:

- merge de mudança normativa, estrutural ou pública;
- promoção do banco como autoridade;
- deploy;
- alteração de Pages;
- criação, encerramento ou mudança de visibilidade de repositório;
- modificação do Drive;
- armazenamento persistente de conteúdo externo;
- ação destrutiva;
- decisão científica ambígua de alto impacto.

## 10. Revisão e autorização

A sequência obrigatória é:

```text
implementação
→ testes
→ revisão automática ou humana
→ correções
→ nova revisão
→ zero threads acionáveis
→ head congelado
→ autorização humana para o SHA exato
→ merge
```

Autorização não pode ser transferida entre SHAs.

CI verde não substitui revisão semântica nem evidência externa.

## 11. PR #57

O PR #57 permanece congelado e não deve ser mesclado ou ampliado. É candidato a `superseded`. Sua autorização anterior está inválida.

A reutilização futura deve ocorrer por seleção de evidências úteis, não por cherry-pick integral da arquitetura profunda.

## 12. Instâncias futuras

A Instância 2 visualizará dados mantidos externamente. A Instância 3 usará literatura curada. Nenhuma delas deve ampliar o núcleo da Instância 1 antes dos respectivos gates.

## 13. Evidência histórica

Auditorias, ocorrências e PRs devem ser preservados. Evidência histórica não se torna norma automaticamente.
