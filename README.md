# Catálogo de Fontes de Dados Ambientais

Catálogo público e pesquisável de fontes para ecologia, biodiversidade, clima, carbono, solo, vegetação e temas relacionados.

## Produto

- [Catálogo de fontes](https://ian-loc.github.io/ecology-data-catalog/#catalogo)
- [Visão analítica](https://ian-loc.github.io/ecology-data-catalog/analytics.html)
- [Sobre, método e citação](https://ian-loc.github.io/ecology-data-catalog/about.html)
- [CSV canônico](data/data_resources.csv)

O catálogo é uma camada de descoberta e triagem. Ele não armazena os datasets externos e não substitui a documentação metodológica ou a licença de cada produto.

## Fonte única de dados

A fonte canônica é **[data/data_resources.csv](data/data_resources.csv)**. O arquivo `data/data_resources.json` é validado e gerado a partir do CSV no workflow do GitHub Pages. A planilha do Google Drive é apenas referência histórica e não participa da publicação.

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

1. Edite somente `data/data_resources.csv`.
2. Use documentação oficial e, quando disponível, literatura revisada por pares.
3. Registre incertezas; não converta ausência de documentação em “não”.
4. Execute `python3 scripts/build_catalog.py`.
5. Abra um pull request e confira a validação automática.

Consulte [METHODOLOGY.md](METHODOLOGY.md), [CODEBOOK.md](CODEBOOK.md) e [AUDIT_WORKFLOW.md](AUDIT_WORKFLOW.md).

## Como citar

> Ian Lara. 2026. *Catálogo de Fontes de Dados Ambientais*, versão 0.7.0 [catálogo de dados]. GitHub. https://ian-loc.github.io/ecology-data-catalog/

A citação do catálogo não substitui a citação do dataset, produto e versão originais.

## Licenças

- Código: MIT
- Curadoria original do catálogo: CC BY 4.0
- Fontes externas: licenças e condições próprias.
