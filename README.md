# Science Data Sources Catalog — Symbiotrama

**Catálogo relacional científico-operacional de produtos de dados georreferenciados sobre o Brasil.**

O projeto organiza fontes, famílias de produtos, produtos científicos, versões, variáveis, métodos, escalas, qualidade, formas de acesso, licenças, citações e evidências curatoriais.

Seu foco ativo é a **Instância 1 do Symbiotrama**: construir uma base profunda e precisa que permita descobrir não apenas onde existe um dado, mas **qual informação científica o produto representa, como foi produzida, em que escala pode ser interpretada e como pode ser acessada**.

> **A vida acontece em relação. Antes de investigar relações, é preciso compreender precisamente cada informação.**

## Acessar o catálogo público atual

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Buscar e comparar produtos](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Analisar a composição atual do catálogo](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Consultar método, escopo e citação](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Baixar o CSV canônico atual](data/data_resources.csv)

A página pública atual permanece disponível durante a migração. Ela ainda representa uma versão simplificada do conhecimento que o novo modelo relacional deverá sustentar.

## Foco ativo: Instância 1

A Instância 1 é um catálogo de metadados científicos e operacionais. Ela não copia necessariamente os grandes datasets externos.

```text
Organização
  └── Fonte ou infraestrutura
        └── Família de produtos
              └── Produto científico
                    └── Versão ou edição
                          ├── variáveis e classes
                          ├── método
                          ├── perfil espacial e temporal
                          ├── qualidade e incerteza
                          └── distribuições, ativos e capacidades de acesso
```

A documentação canônica da direção está em:

- [Instância 1 — Catálogo relacional científico-operacional](docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md)
- [Decisão estratégica da Instância 1](docs/decisions/DEC-INSTANCE1-RELATIONAL-CORE.md)
- [Workflow contínuo de curadoria](docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md)
- [Banco relacional](database/README.md)
- [Esquema SQL](database/schema/001_instance1_core.sql)

## O que é um produto científico

Um produto é um conjunto coerente e versionado de informações espaciais, produzido por metodologia definida, com significado temático, cobertura, suporte espacial e temporal, variáveis e formas de distribuição identificáveis.

Não são produtos científicos, por si sós:

- uma organização;
- um portal;
- um catálogo genérico;
- uma API ou serviço de processamento;
- um visualizador;
- um formato de arquivo;
- uma página de download.

Esses elementos são registrados, mas em entidades próprias.

## Perfil do produto

Cada produto deverá responder:

### Identidade

- quem produz;
- qual versão ou coleção;
- qual citação e licença;
- qual é o estado do produto.

### Significado científico

- qual fenômeno representa;
- qual objeto ou população observa;
- quais variáveis e classes contém;
- o que a informação significa;
- o que o produto não representa diretamente.

### Natureza de produção

- medido, observado por sensor, administrativo, amostral, classificado, modelado, interpolado, agregado ou derivado;
- entradas, processamento, validação e versão do método.

### Espaço e tempo

- geometria, suporte, resolução, escala, grade e CRS;
- extensão territorial;
- cobertura, janela e resolução temporal;
- frequência de atualização e latência.

### Qualidade

- validação;
- acurácia;
- incerteza;
- flags;
- dados ausentes;
- vieses e artefatos;
- limites de representatividade e interpretação.

### Acesso

- download;
- API;
- serviços geoespaciais;
- Earth Engine;
- formatos;
- autenticação;
- gratuidade;
- recorte, consulta, visualização e exportação.

## Banco relacional

O modelo de destino usa **PostgreSQL + PostGIS**.

PostGIS é usado para descrever extensão e suporte geográfico dos produtos. O banco não precisa hospedar todos os rasters, vetores e séries externas.

O esquema inclui:

- organizações e fontes;
- famílias, produtos e releases;
- variáveis e associações produto–variável;
- métodos;
- perfis espaciais, temporais e de qualidade;
- distribuições, ativos e capacidades de acesso;
- taxonomias e citações;
- evidências por campo;
- revisões curatoriais.

Durante a migração, os CSVs permanecem canônicos para a versão pública atual. Depois do portão de validação, o banco deverá se tornar a fonte canônica, e CSVs e planilhas serão exportações reproduzíveis.

## Dados georreferenciados

O catálogo inclui produtos com:

- coordenadas;
- pontos e footprints;
- linhas e trajetórias;
- polígonos;
- pixels e grades;
- bacias, biomas e unidades de conservação;
- municípios, estados e outras unidades administrativas;
- tabelas com códigos territoriais e séries território–tempo.

Uma tabela município–ano pode ser georreferenciável mesmo quando distribuída em CSV ou XLSX.

## Curadoria

A unidade de trabalho é **um produto integralmente inspecionado**, não apenas uma linha ou nome cadastrado.

A curadoria verifica:

1. identidade e produtor primário;
2. significado científico;
3. variáveis e classes;
4. método;
5. suporte espacial e temporal;
6. qualidade, incerteza e vieses;
7. versões;
8. formas de acesso;
9. licença e citação;
10. evidência de cada afirmação material;
11. completude e precisão.

A prioridade é Brasil primeiro: fontes brasileiras e produtos internacionais com cobertura efetiva do país.

## Instâncias futuras — somente leitura conceitual

### Instância 2 — composição geográfica

Possível visualização conjunta de camadas resolvidas, mapas sincronizados e perfis territoriais, com transparência de escala, método e proveniência.

### Instância 3 — contexto científico

Possível síntese breve e auditável de literatura sobre os fenômenos representados em uma composição escolhida pelo usuário.

Essas instâncias não são o foco de implementação atual. Não devem atrasar nem enfraquecer a consolidação do catálogo relacional.

## Autoridade dos dados durante a transição

- `data/data_resources.csv` — fontes da versão pública atual;
- `data/data_products.csv` — piloto de produtos;
- `data/product_distributions.csv` — piloto de formas de acesso;
- `database/schema/001_instance1_core.sql` — arquitetura relacional canônica de destino;
- planilhas no Google Drive — espelhos derivados após consolidação no GitHub.

## Estrutura do repositório

- `data/` — CSVs e registros públicos atuais;
- `database/` — banco relacional e migrações;
- `schema/` — contratos e validações complementares;
- `docs/` — direção, decisões, método, governança, auditorias e roadmap;
- `scripts/` — geração e validação;
- `assets/` e HTML — interface pública atual;
- `.github/workflows/` — integração contínua e publicação.

## Documentação principal

- [Instância 1](docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md)
- [Modelo fonte–produto–distribuição](PRODUCT_CATALOG_MODEL.md)
- [Dicionário de dados](CODEBOOK.md)
- [Metodologia](METHODOLOGY.md)
- [Política de seleção e cobertura](SELECTION_AND_COVERAGE_POLICY.md)
- [Governança](docs/GOVERNANCE.md)
- [Política de releases](docs/RELEASE_POLICY.md)
- [Como contribuir](CONTRIBUTING.md)
- [Histórico de mudanças](CHANGELOG.md)

## Citação

> CLEMENTE, Ian. *Science Data Sources Catalog: catálogo científico-operacional de produtos de dados georreferenciados sobre o Brasil*. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318)

A citação do catálogo não substitui a citação da fonte, do produto e da versão originais.

## Licenças

- código: [MIT](LICENSE);
- metadados e curadoria original: [CC BY 4.0](LICENSE-DATA.md);
- produtos externos: licenças e termos próprios.
