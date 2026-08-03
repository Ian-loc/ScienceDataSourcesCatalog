# Governança do projeto

## Finalidade

O Science Data Sources Catalog é um projeto científico contínuo de descoberta, descrição e comparação de fontes de dados com prioridade para o Brasil. A governança preserva rastreabilidade, revisão factual e separação entre dados canônicos, artefatos derivados e documentação operacional.

## Autoridade

A autoridade canônica é composta por:

1. branch `main` do repositório;
2. `data/data_resources.csv` para o catálogo de fontes;
3. `data/data_products.csv` e `data/product_distributions.csv` para produtos e acessos;
4. contratos de esquema e validadores executáveis;
5. releases identificadas e histórico de pull requests.

Em caso de divergência, os arquivos canônicos validados em `main` prevalecem sobre planilhas, cópias locais, documentos históricos e conversas de trabalho.

## Artefatos derivados

São derivados:

- JSONs da interface;
- metadados de build;
- website publicado;
- planilha nativa e arquivo XLSX no Google Drive;
- relatórios ou visualizações produzidos a partir do catálogo.

Derivados devem registrar, quando aplicável, versão, commit-fonte e data de geração. Eles não constituem uma segunda fonte de edição.

## Papéis

### Responsável científico e mantenedor

- define escopo e critérios de inclusão;
- decide interpretações científicas;
- aprova mudanças canônicas e releases;
- responde pela identidade, autoria e citação do projeto.

### Contribuidores

- apresentam evidências e propostas rastreáveis;
- limitam alterações ao escopo declarado;
- executam ou documentam validações;
- não tratam CI verde como prova de verdade factual externa.

### Automação

- valida estrutura, contratos e consistência;
- gera artefatos derivados;
- publica somente o artefato público permitido;
- não decide elegibilidade científica nem altera silenciosamente valores canônicos.

## Ciclo de mudança

Uma mudança canônica deve percorrer:

1. identificação da necessidade;
2. evidência e proposta explícita;
3. branch dedicada;
4. alteração dos arquivos-fonte;
5. validação automática e inspeção científica;
6. pull request;
7. integração em `main`;
8. regeneração dos derivados;
9. registro em changelog e, quando aplicável, release.

## Decisões científicas e técnicas

Decisões duradouras devem ser registradas em documentação estável, contrato de esquema, issue, pull request ou registro de decisão. Logs de sessão, tentativas temporárias e falhas operacionais podem ser arquivados, mas não devem dominar a documentação pública.

## Auditorias

Auditorias são evidência de controle de qualidade, não componentes da interface pública. Devem informar:

- escopo;
- data;
- método;
- evidências consultadas;
- achados;
- correções aceitas;
- limitações e pendências.

Achados não alteram automaticamente os dados canônicos.

## Segurança editorial

O GitHub Pages publica apenas arquivos copiados para `_site`. Scripts, workflows, matrizes de migração, auditorias e documentação interna permanecem acessíveis no repositório, mas não são incluídos no artefato do website.
