# Science Data Sources Catalog — Simbiotrama

**Catálogo relacional científico-operacional de produtos de dados georreferenciados sobre o Brasil.**

O Simbiotrama organiza fontes, famílias, produtos científicos, releases, variáveis, métodos, escalas, qualidade, formas de acesso, licenças, citações e evidências curatoriais.

Seu foco ativo é a **Instância 1 — Catálogo relacional científico-operacional**: construir uma base profunda e precisa que permita descobrir não apenas onde existe um dado, mas qual informação o produto representa, como foi produzida, em que escala pode ser interpretada e como pode ser acessada.

> **A vida acontece em relação. Antes de investigar relações, é preciso compreender precisamente cada informação.**

## Estado atual

- **Marco 1:** incorporado à `main` pelos PRs #54 e #55;
- **arquitetura de destino:** PostgreSQL/PostGIS;
- **autoridade pública transitória:** CSV/JSON atuais;
- **foco ativo:** curadoria científica e operacional da Instância 1;
- **Instância 2 — composição geográfica:** backlog;
- **Instância 3 — contexto científico:** backlog;
- **explorador visual N0:** legado operacional preservado, sem expansão analítica.

Consulte:

- [Estado canônico e ciclo de vida](docs/PROJECT_STATE.md)
- [Direção científica](docs/PROJECT_SCIENTIFIC_DIRECTION.md)
- [Instância 1](docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md)
- [Roadmap](docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md)
- [Workflow contínuo de curadoria](docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md)
- [Banco relacional](database/README.md)
- [Esquema SQL](database/schema/001_instance1_core.sql)
- [Código, dados e documentação](https://github.com/Ian-loc/ScienceDataSourcesCatalog)

## Catálogo público atual

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Buscar e comparar perfis de produtos](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Analisar a composição atual do catálogo](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Consultar método, escopo e citação](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Baixar o CSV público atual](data/data_resources.csv)

A página publicada continua disponível durante a migração. Ela representa uma projeção simplificada e transitória, não a profundidade integral do modelo relacional.

## Arquitetura da Instância 1

```text
Organização
  └── Fonte ou infraestrutura
        └── Família de produtos
              └── Produto científico
                    └── Release, versão ou edição
                          ├── variáveis e classes
                          ├── método
                          ├── perfil espacial e temporal
                          ├── qualidade e incerteza
                          └── distribuição
                                ├── ativo
                                └── capacidade de acesso
```

Um produto é um conjunto coerente e versionado de informações georreferenciadas, produzido por metodologia definida, com significado científico, cobertura, suporte espacial e temporal, variáveis e formas de distribuição identificáveis.

Não são produtos científicos, por si sós:

- organizações;
- portais ou catálogos genéricos;
- APIs ou serviços de processamento;
- visualizadores;
- formatos de arquivo;
- páginas de download.

Esses objetos são registrados em entidades próprias.

## Perfil científico-operacional

Cada produto ou release deve responder:

- quem produz e qual versão está em uso;
- qual fenômeno, objeto ou população representa;
- quais variáveis, bandas, classes ou indicadores contém;
- se é medido, administrativo, amostral, classificado, modelado, interpolado, agregado ou derivado;
- qual é o suporte, resolução, escala, grade, CRS e extensão;
- qual é a cobertura, janela, frequência e latência temporal;
- quais validações, incertezas, vieses, ausências e limitações existem;
- como acessar por download, API, serviço geoespacial ou infraestrutura computacional;
- qual licença, citação e evidência sustentam o registro.

Resolução, suporte e escala não são sinônimos. Incerteza não documentada não equivale a ausência de incerteza.

## Banco relacional e transição

O modelo de destino usa PostgreSQL com PostGIS e inclui:

- organizações e fontes;
- famílias, produtos e releases;
- variáveis e associações produto–variável;
- métodos;
- perfis espaciais, temporais e de qualidade;
- distribuições, ativos e capacidades;
- taxonomias, citações e evidências;
- revisões curatoriais.

PostGIS descreve extensão e suporte geográfico. O Simbiotrama não precisa copiar integralmente os grandes datasets externos.

Durante a transição:

- `data/data_resources.csv` — fontes da versão pública;
- `data/data_products.csv` — piloto público de produtos;
- `data/product_distributions.csv` — formas de acesso do piloto;
- `database/schema/001_instance1_core.sql` — arquitetura relacional canônica de destino;
- planilhas no Drive — snapshots ou espelhos derivados.

O PostgreSQL/PostGIS somente se tornará autoridade após o gate formal de prontidão, exportações reproduzíveis e autorização humana.

## Curadoria

A unidade de trabalho é **um produto ou release integralmente inspecionado**.

O pipeline inclui:

1. identidade e produtor;
2. família, produto e release;
3. significado, variáveis e classes;
4. método;
5. perfil espacial;
6. perfil temporal;
7. qualidade, incerteza e limitações;
8. distribuições, ativos e capacidades;
9. licença e citação;
10. evidências por afirmação;
11. revisão curatorial e decisão de promoção.

A prioridade é Brasil primeiro: fontes brasileiras e produtos internacionais com cobertura efetiva do país.

## Ciclo de vida

- `ACTIVE`: núcleo e curadoria da Instância 1;
- `BACKLOG`: Instâncias 2 e 3, receitas e contratos analíticos futuros;
- `LEGACY_OPERATIONAL`: explorador N0 e interface estática transitória;
- `RETIRED` / `SUPERSEDED`: workstreams e branches substituídos;
- `HISTORICAL_EVIDENCE`: auditorias, ocorrências, PRs e snapshots.

A classificação detalhada está em [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md).

## Documentação principal

- [Estado do projeto](docs/PROJECT_STATE.md)
- [Instância 1](docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md)
- [Modelo fonte–produto–distribuição](PRODUCT_CATALOG_MODEL.md)
- [Dicionário de dados](CODEBOOK.md)
- [Metodologia](METHODOLOGY.md)
- [Política de seleção e cobertura](SELECTION_AND_COVERAGE_POLICY.md)
- [Governança](docs/GOVERNANCE.md)
- [Política de releases](docs/RELEASE_POLICY.md)
- [Guardrail futuro de comparabilidade e inferência](docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md)
- [Histórico de mudanças](CHANGELOG.md)

## Citação

> CLEMENTE, Ian. *Science Data Sources Catalog — Simbiotrama: catálogo científico-operacional de produtos de dados georreferenciados sobre o Brasil*. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318)

A citação do catálogo não substitui a citação da fonte, do produto e da release originais.

## Licenças

- código: [MIT](LICENSE);
- metadados e curadoria original: [CC BY 4.0](LICENSE-DATA.md);
- produtos externos: licenças e termos próprios.
