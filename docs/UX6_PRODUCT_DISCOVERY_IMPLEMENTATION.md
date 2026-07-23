# UX6 — descoberta e comparação de produtos

## Objetivo

Transformar a camada fonte → produto → distribuição em uma experiência pública de descoberta científica, sem alterar o CSV canônico de 51 fontes × 34 campos.

## Produto implementado

- página `products.html` separada do catálogo de fontes;
- geração de `data/data_products.json` no build;
- associação explícita entre produto, fonte e distribuições;
- busca por nomes, descrições, fenômenos, palavras-chave, fonte, formatos e protocolos;
- expansão controlada de sinônimos em português e inglês;
- filtros representados na URL;
- comparação de dois ou três produtos;
- exposição de suporte e resolução espacial, cobertura e resolução temporal, versão, origem, limitações e última verificação;
- detalhamento de cada distribuição com URL, formato, protocolo, ferramenta, autenticação, licença e condições de acesso;
- navegação integrada entre Fontes, Produtos, Análise e Método.

## Regras preservadas

- fonte, produto e distribuição não são tratados como unidades equivalentes;
- o CSV de fontes permanece canônico e inalterado;
- o JSON de produtos é artefato derivado gerado no workflow;
- formatos diferentes do mesmo produto não geram produtos duplicados;
- resolução não é inferida a partir do visualizador;
- alerta operacional não é apresentado como resultado anual consolidado;
- licença e provedor são apresentados no nível mais específico disponível;
- catálogos muito grandes permanecem como índices externos ou famílias selecionadas.

## Validação

O workflow passa a exigir:

1. validação da camada de produtos;
2. geração dos JSONs de fontes e produtos;
3. existência das páginas e dos artefatos publicáveis;
4. sintaxe válida de todos os arquivos JavaScript;
5. estrutura HTML e acessibilidade;
6. produtos com fonte existente e pelo menos uma distribuição;
7. orçamento de peso da interface;
8. publicação pelo workflow oficial do GitHub Pages.

## Limite do pacote

O piloto continua restrito a TerraBrasilis e Google Earth Engine. A expansão para outras fontes deve ocorrer em ciclos curatoriais, com documentação oficial, produto identificável, resolução e cobertura específicas e distribuição verificável.

## Dependência administrativa externa ao código

O repositório precisa ter `Settings → Pages → Build and deployment → Source` configurado como `GitHub Actions`. Essa configuração não é representada por arquivo versionado e deve ser confirmada por um administrador do repositório.
