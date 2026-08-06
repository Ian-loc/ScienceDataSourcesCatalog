# Science Data Sources Catalog — Simbiotrama

**Catálogo relacional de fontes e ofertas de dados científicos com cobertura ou relevância para o Brasil.**

O Simbiotrama organiza metadados essenciais para que pessoas encontrem, compreendam e acessem dados científicos mantidos por instituições e plataformas externas.

O projeto não pretende copiar datasets, reconstruir catálogos de terceiros, enumerar todos os arquivos disponíveis ou reproduzir a genealogia completa de cada produto.

> **A Instância 1 deve ser simples, funcional, verificável e sustentável como catálogo.**

## Estado atual

- **Instância 1:** foco ativo;
- **arquitetura-alvo:** catálogo relacional simplificado;
- **autoridade pública transitória:** CSV/JSON atuais;
- **PostgreSQL:** destino de implementação após validação do modelo simplificado;
- **Instância 2:** visualização federada por APIs e outros conectores, em backlog;
- **Instância 3:** contexto científico por literatura curada, em backlog;
- **explorador atual:** legado operacional preservado, sem expansão analítica.

## Arquitetura da Instância 1

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles  [opcional]
```

A entidade central é uma **entrada de catálogo**. Ela pode representar uma fonte, plataforma, coleção, produto de dados ou serviço quando esse nível for útil para descoberta e compreensão.

Uma nova entrada só deve existir quando houver diferença material de significado científico, cobertura, método, finalidade ou forma principal de acesso. Outro arquivo, formato, layer, banda ou endpoint não cria automaticamente uma nova entrada.

## O que cada entrada deve informar

Quando aplicável e disponível:

- organização responsável;
- nome oficial e tipo amplo;
- resumo e escopo científico;
- modalidades de dados;
- variáveis ou grupos de variáveis;
- cobertura espacial e temporal;
- resolução ou suporte relevante;
- frequência de atualização;
- condições de acesso;
- gratuidade e autenticação;
- página oficial;
- metadados;
- metodologia;
- licença;
- citação;
- estado e data de verificação.

O catálogo preserva nomes e definições do produtor. Normaliza apenas o necessário para busca e filtros.

## Dados permanecem externos

O Simbiotrama:

- não hospeda datasets de terceiros;
- não mantém arquivos externos como acervo;
- não promete preservação dos bytes;
- não inventaria todos os ativos de uma plataforma;
- não assume autoria, hospedagem ou custódia;
- direciona o usuário às fontes originais.

## Instância 2

A futura Instância 2 deverá visualizar e consultar dados externos por APIs, serviços geoespaciais, STAC, Earth Engine e outros conectores selecionados.

Um `connector_profile` registra somente a configuração necessária para uma operação aprovada. Ele não exige que a Instância 1 tenha enumerado todos os arquivos ou layers da fonte.

## Catálogo público atual

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Buscar e comparar perfis atuais](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Analisar a composição atual](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Consultar método, escopo e citação](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Baixar o CSV público atual](data/data_resources.csv)

A página atual permanece operacional durante a reestruturação. Ela é uma projeção transitória e não deve orientar expansão do modelo antigo.

## Documentação canônica

- [Estado do projeto](docs/PROJECT_STATE.md)
- [Decisão do núcleo simplificado](docs/decisions/DEC-INSTANCE1-MINIMUM-SUFFICIENT-CATALOG.md)
- [Política de escopo e granularidade](docs/policies/INSTANCE_1_SCOPE_AND_GRANULARITY_POLICY.md)
- [Instância 1](docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md)
- [Roadmap](docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md)
- [Workflow de curadoria](docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md)
- [Governança](docs/GOVERNANCE.md)
- [Banco e transição](database/README.md)

## Ciclo de vida

- `ACTIVE`: núcleo simplificado, curadoria de entradas e website dinâmico da Instância 1;
- `BACKLOG`: conectores federados, Instâncias 2 e 3, receitas e análises;
- `LEGACY_TRANSITIONAL`: esquema profundo do Marco 1, mantido para migração e reaproveitamento seletivo;
- `LEGACY_OPERATIONAL`: interface pública atual;
- `HISTORICAL_EVIDENCE`: auditorias, ocorrências, PRs e snapshots.

## Citação

> CLEMENTE, Ian. *Science Data Sources Catalog — Simbiotrama: catálogo relacional de fontes e ofertas de dados científicos*. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318)

A citação do catálogo não substitui a citação das fontes originais.

## Licenças

- código: [MIT](LICENSE);
- metadados e curadoria original: [CC BY 4.0](LICENSE-DATA.md);
- dados externos: licenças e termos próprios das respectivas fontes.
