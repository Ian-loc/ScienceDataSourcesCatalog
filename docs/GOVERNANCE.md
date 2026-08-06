# Governança do Simbiotrama

## 1. Finalidade

O Simbiotrama é um catálogo relacional de fontes e ofertas de dados científicos. A fase ativa é a **Instância 1**, dedicada a descoberta, compreensão e acesso por meio de metadados essenciais e links oficiais.

A Instância 1 não copia datasets externos, não reconstrói catálogos de terceiros e não exige decomposição completa em produtos, releases, distribuições e ativos.

As Instâncias 2 e 3 permanecem em backlog.

## 2. Autoridade

A hierarquia vigente é:

1. `main`;
2. `docs/PROJECT_STATE.md`;
3. políticas e decisões incorporadas;
4. contrato funcional e roadmap;
5. esquema, migrações e validadores executáveis;
6. dados públicos canônicos durante a transição;
7. evidências e revisões curatoriais;
8. auditorias, protótipos e documentos históricos.

Literatura, reflexões de outros chats, branches não incorporadas e relatórios de sessão são insumos, não autoridade arquitetural.

## 3. Ciclo de vida

Todo artefato deve ser classificado como:

- `ACTIVE`;
- `BACKLOG`;
- `LEGACY_OPERATIONAL`;
- `RETIRED` / `SUPERSEDED`;
- `HISTORICAL_EVIDENCE`.

A disposição detalhada está em `docs/PROJECT_STATE.md`.

## 4. Regime de mudança

Mudanças devem percorrer:

1. delimitação do pacote;
2. justificativa de utilidade pública;
3. branch derivada da `main` corrente;
4. alterações limitadas ao escopo;
5. validação e inspeção do delta;
6. pull request;
7. revisão concluída;
8. congelamento do head;
9. autorização humana quando exigida;
10. incorporação preferencialmente por squash merge.

Cada PR deve ser pequeno e coerente. Alterações arquiteturais, curadoria de entradas e mudanças de interface não devem ser misturadas sem necessidade demonstrável.

## 5. Gate de escopo

Antes de criar entidade, tabela, coluna, vocabulário, documento normativo ou validador, responder:

1. melhora descoberta no catálogo?
2. melhora interpretação mínima?
3. sustenta filtro ou apresentação no website?
4. é necessário para conector selecionado?

Se todas as respostas forem negativas, a mudança permanece em backlog.

Também verificar:

- o dado já pertence à fonte externa?
- estamos reconstruindo a genealogia da plataforma?
- a nova entrada existe apenas por arquivo, layer, banda ou endpoint?
- o aprofundamento altera materialmente a ficha pública?
- existe critério de parada?

## 6. Gates humanos

Exigem autorização humana explícita:

- merge de mudança científica, estrutural, executável ou pública;
- promoção do PostgreSQL como autoridade;
- publicação ou deploy;
- mudança de visibilidade;
- criação, encerramento ou migração de repositório;
- modificação ou substituição de arquivos do Drive;
- ação destrutiva ou irreversível;
- decisão científica ambígua de alto impacto.

A autorização é válida apenas para o SHA exato revisado.

## 7. Curadoria

A unidade de trabalho é uma **entrada de catálogo suficientemente descrita**.

A conclusão requer, conforme disponibilidade:

- organização e nome;
- tipo amplo;
- resumo e escopo;
- modalidades, temas e variáveis principais;
- cobertura espacial e temporal;
- resolução ou suporte material;
- atualização;
- gratuidade e autenticação;
- links oficiais de página, metadados e acesso;
- metodologia, licença e citação quando disponíveis;
- evidência proporcional;
- revisão e data de verificação.

Não são requisitos universais:

- release;
- distribuição;
- ativo;
- checksum;
- bytes;
- schema físico;
- inventário de layers;
- perfil forense de qualidade.

## 8. Pesquisa

A pesquisa deve priorizar páginas e metadados oficiais. O critério de parada é atingido quando a ficha é útil, sustentada e encaminha o usuário à fonte.

A existência de documentação adicional não torna a entrada automaticamente incompleta.

Ausência de documentação deve permanecer como lacuna, sem inferência.

## 9. Automação

A automação pode:

- validar estrutura, IDs, links e estados curatoriais;
- detectar duplicidade e regressão de escopo;
- gerar exportações autorizadas;
- registrar ocorrências.

A automação não pode:

- inventar metadados;
- criar taxonomia universal;
- transformar literatura em expansão automática;
- medir sucesso por quantidade de assets, releases, claims ou validadores;
- executar gate humano.

Validadores devem testar contratos estruturais e casos adversariais relevantes, evitando verificações frágeis por simples presença de palavras.

## 10. Revisão e merge

A ordem obrigatória é:

```text
implementação
→ testes
→ revisão
→ correções
→ novo teste
→ confirmação de zero threads acionáveis
→ congelamento do head
→ autorização humana do SHA exato
→ merge
```

CI verde antes do término da revisão não libera merge.

## 11. Instâncias futuras

### Instância 2

Visualização federada por conectores externos selecionados. Não requer inventário integral nem armazenamento dos dados.

### Instância 3

Contextualização por literatura curada. Não lidera o esquema da Instância 1.

## 12. Evidência histórica

Auditorias, ocorrências, PRs, commits e propostas devem ser preservados. Material histórico não orienta trabalho novo quando conflita com decisões vigentes.

## 13. Publicação e espelhos

Os CSV/JSON e a página pública permanecem transitórios. Mudanças no núcleo relacional não implicam deploy ou promoção automática.

Espelhos do Drive devem declarar versão, commit-fonte e data de geração. Eles não são fonte independente.
