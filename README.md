# Science Data Sources Catalog

**Catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão.**

O projeto reúne e descreve plataformas, repositórios, redes, sistemas, produtos e formas de acesso a dados científicos, com prioridade para fontes brasileiras e para fontes internacionais com cobertura efetiva do Brasil.

## Acessar o catálogo

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Buscar e comparar produtos](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Analisar a composição do catálogo](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Consultar método, escopo e citação](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Código, dados e documentação](https://github.com/Ian-loc/ScienceDataSourcesCatalog)
- [Baixar o CSV canônico](data/data_resources.csv)

O catálogo é uma camada de descoberta e triagem. Ele não hospeda os datasets externos e não substitui a documentação, a licença, a versão ou a citação dos produtos originais.

## Escopo

A curadoria segue uma orientação **Brasil primeiro**:

1. fontes brasileiras com dados sobre o país;
2. fontes internacionais com cobertura sistemática do Brasil;
3. fontes com cobertura brasileira parcial ou dependente do produto;
4. referências comparativas mantidas apenas quando possuem justificativa científica explícita.

A classificação territorial organiza descoberta e prioridade de curadoria; ela não constitui uma nota de qualidade científica.

## Modelo de dados

O catálogo distingue três níveis:

```text
Fonte ou infraestrutura
  └── Produto, série ou coleção
        └── Distribuição ou forma de acesso
```

Essa separação evita atribuir à infraestrutura inteira propriedades que pertencem a um produto ou acesso específico, como resolução, versão, formato, autenticação e licença.

## Autoridade dos dados

`data/data_resources.csv` na branch `main` é a fonte canônica do catálogo de fontes.

- JSONs e metadados do site são gerados automaticamente.
- `data/data_products.csv` e `data/product_distributions.csv` mantêm a camada de produtos e acessos.
- Planilhas no Google Drive são espelhos derivados e devem ser regeneradas somente após integração e validação no GitHub.
- Evidências e auditorias não alteram silenciosamente o CSV canônico.

## Curadoria e qualidade

Cada registro combina documentação oficial, documentos técnicos, literatura científica representativa e avaliação curatorial. A data de revisão indica quando o registro foi inspecionado; não certifica automaticamente todos os produtos, endpoints ou condições de uso mantidos pela fonte.

Antes de usar um dataset, confirme no produto original:

- versão e período;
- resolução e cobertura;
- metodologia e incerteza;
- licença e requisitos de atribuição;
- condições de acesso e autenticação.

## Estrutura do repositório

- `data/`: dados canônicos e derivados públicos;
- `assets/` e arquivos HTML: interface do catálogo;
- `scripts/`: geração e validação;
- `schema/`: contratos de esquema;
- `docs/`: método, governança, manutenção e auditorias;
- `.github/workflows/`: integração contínua e publicação.

## Documentação principal

- [Metodologia](METHODOLOGY.md)
- [Dicionário de variáveis](CODEBOOK.md)
- [Política de seleção e cobertura](SELECTION_AND_COVERAGE_POLICY.md)
- [Modelo fonte–produto–distribuição](PRODUCT_CATALOG_MODEL.md)
- [Governança](docs/GOVERNANCE.md)
- [Política de releases](docs/RELEASE_POLICY.md)
- [Como contribuir](CONTRIBUTING.md)
- [Histórico de mudanças](CHANGELOG.md)

## Citação

> CLEMENTE, Ian. *Science Data Sources Catalog: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Versão 0.7.0. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318)

A citação do catálogo não substitui a citação do dataset, produto e versão originais.

## Licenças

- código: [MIT](LICENSE);
- CSV, metadados e curadoria original: [CC BY 4.0](LICENSE-DATA.md);
- fontes externas: licenças e termos próprios.
