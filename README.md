# Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão

Catálogo público e pesquisável de plataformas, repositórios, redes e sistemas para ecologia, biodiversidade, clima, carbono, solos, vegetação e temas relacionados.

## Produto

- [Buscar fontes](https://ian-loc.github.io/ecology-data-catalog/#catalogo)
- [Analisar o catálogo](https://ian-loc.github.io/ecology-data-catalog/analytics.html)
- [Sobre, método e citação](https://ian-loc.github.io/ecology-data-catalog/about.html)
- [CSV canônico](data/data_resources.csv)

O catálogo é uma camada de descoberta, comparação e triagem. Ele não armazena os datasets externos e não substitui a documentação metodológica, a licença ou a citação exigida por cada produto.

## Fonte única de dados

A fonte canônica é **[data/data_resources.csv](data/data_resources.csv)**. O arquivo `data/data_resources.json` é validado e gerado a partir do CSV no workflow do GitHub Pages. A planilha do Google Drive é referência histórica e changelog executivo; ela não participa da publicação.

## Conteúdo

A versão 0.7.0 reúne 51 fontes e 34 variáveis, incluindo:

- identidade declarada pela própria fonte;
- áreas de pesquisa condensadas e palavras-chave;
- formatos, produtos e tipos de visualização;
- cobertura do Brasil;
- download, autenticação e acesso programático;
- protocolos como REST, OGC, STAC, S3, Earth Engine e pacotes R/Python;
- utilidade acadêmica e limitações;
- evidência oficial, técnica ou revisada por pares.

## Atualização

1. Edite somente `data/data_resources.csv` para alterar o conteúdo científico.
2. Use documentação oficial e, quando disponível, literatura revisada por pares.
3. Registre incertezas; não converta ausência de documentação em “não”.
4. Execute `python3 scripts/build_catalog.py`.
5. Abra um pull request e confira a validação automática.
6. Registre mudanças integradas no changelog do GitHub e no registro executivo do Drive.

Consulte [METHODOLOGY.md](METHODOLOGY.md), [CODEBOOK.md](CODEBOOK.md), [AUDIT_WORKFLOW.md](AUDIT_WORKFLOW.md), [IMPLEMENTATION_WORKFLOW.md](IMPLEMENTATION_WORKFLOW.md) e [WORKFLOW_STATUS.md](WORKFLOW_STATUS.md).

## Como citar

> LARA, Ian. *Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Versão 0.7.0. GitHub, 2026. https://ian-loc.github.io/ecology-data-catalog/

ORCID do autor: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318).

A citação do catálogo não substitui a citação do dataset, produto e versão originais.

## Licenças

- **Código e rotinas:** MIT, conforme [LICENSE](LICENSE).
- **CSV, metadados e curadoria original:** CC BY 4.0, conforme [LICENSE-DATA.md](LICENSE-DATA.md).
- **Fontes externas:** licenças, termos de uso e condições de citação próprias.

## Versão estável e DOI

A versão `1.0.0` e o DOI ainda não foram criados. Eles estão condicionados ao fechamento técnico, científico e documental descrito em [IMPLEMENTATION_WORKFLOW.md](IMPLEMENTATION_WORKFLOW.md).

A futura release deverá ser arquivada no Zenodo como **Dataset**. O projeto mantém apenas `CITATION.cff` enquanto não houver necessidade comprovada de `.zenodo.json`.
