# Science Data Sources Catalog — Simbiotrama

**Catálogo relacional de fontes e ofertas de dados científicos, com prioridade para o Brasil.**

O Simbiotrama ajuda pessoas a descobrir o que uma fonte oferece, quais temas e variáveis estão disponíveis, onde e quando os dados se aplicam e como continuar o acesso na plataforma original.

O projeto não copia datasets externos, não reconstrói catálogos de terceiros e não exige a enumeração completa de arquivos, layers, bandas ou versões.

## Estado atual

- **Marco 1:** incorporado pelos PRs #54 e #55;
- **sanity pós-marco:** incorporado pelo PR #56;
- **pacote ativo:** simplificação governada da Instância 1;
- **arquitetura de destino:** PostgreSQL/PostGIS;
- **autoridade pública transitória:** CSV/JSON atuais;
- **Instância 2 — visualização federada:** backlog;
- **Instância 3 — literatura científica:** backlog;
- **explorador visual N0:** legado operacional preservado.

Documentos principais:

- [Estado canônico](docs/PROJECT_STATE.md)
- [Política de escopo e granularidade](docs/policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md)
- [Contrato da Instância 1](docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md)
- [Decisão de simplificação](docs/decisions/DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md)
- [Roadmap](docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md)
- [Workflow de curadoria](docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md)
- [Governança](docs/GOVERNANCE.md)

## Catálogo público atual

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Consultar o piloto de produtos](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Analisar a composição atual](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Consultar método e escopo](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Baixar o CSV público](data/data_resources.csv)

A página publicada permanece disponível durante a transição. Nenhuma mudança desta etapa implica deploy.

## Arquitetura da Instância 1

```text
Organização
  └── Entrada de catálogo
        ├── temas e variáveis principais
        ├── metadados essenciais
        ├── evidências proporcionais
        └── conector opcional futuro
```

Uma entrada pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

O nível escolhido deve ser útil ao usuário. Não se cria uma nova entrada apenas porque existe outro arquivo, layer, banda, formato, endpoint ou atualização técnica.

## Ficha pública

Uma entrada deve buscar, conforme disponibilidade:

- organização e nome oficial;
- tipo amplo;
- resumo e escopo científico;
- modalidades de dados;
- temas e variáveis principais;
- cobertura espacial e temporal;
- resolução ou suporte quando material;
- atualização;
- gratuidade e autenticação;
- página oficial;
- metadados;
- acesso principal;
- metodologia, licença e citação;
- estado e data de verificação.

A terminologia da fonte deve ser preservada. Termos simplificados podem ser adicionados para busca e filtros.

## O que não é requisito universal

A Instância 1 não exige, para cada entrada:

- família de produtos;
- release;
- distribuição;
- ativo;
- inventário de arquivos;
- checksum;
- inspeção de bytes;
- schema físico completo;
- enumeração de endpoints;
- pacote forense de qualidade.

Esses elementos só devem ser aprofundados quando resolvem uma ambiguidade central, sustentam um filtro importante ou viabilizam um conector selecionado.

## Banco relacional e transição

O núcleo-alvo é:

- `organizations`;
- `catalog_entries`;
- `entry_variables`;
- `entry_evidence`;
- `connector_profiles` opcional.

As estruturas profundas incorporadas no Marco 1 serão preservadas durante a migração e poderão permanecer como legado técnico ou extensões futuras. A simplificação deve ser idempotente, reversível e sem perda do staging.

O PostgreSQL/PostGIS somente se tornará autoridade após validação, exportações reproduzíveis e autorização humana.

## Curadoria

A unidade de trabalho é uma **entrada de catálogo suficientemente descrita**.

A pesquisa começa por páginas e metadados oficiais e termina quando:

1. o usuário consegue compreender o que encontrará;
2. os campos essenciais estão sustentados;
3. existe caminho oficial para acesso;
4. as lacunas relevantes estão explícitas;
5. aprofundamento adicional não mudaria materialmente a ficha pública.

## Validação inicial

O modelo simplificado será testado com:

- GEDI;
- DETER Cerrado;
- IBGE;
- ANA/SNIRH.

O modelo deve representar os quatro casos sem proliferação de tabelas, inventário integral ou perda do significado necessário ao usuário.

## Instâncias futuras

### Instância 2

Visualização federada por APIs e conectores externos selecionados, sem armazenamento central dos datasets.

### Instância 3

Contextualização por literatura científica curada, sem impor profundidade adicional à Instância 1.

## Citação

> CLEMENTE, Ian. *Science Data Sources Catalog — Simbiotrama: catálogo relacional de fontes e ofertas de dados científicos*. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318)
