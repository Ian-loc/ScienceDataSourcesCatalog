# Modelo de catálogo de produtos

## Decisão

A camada de produtos **não é redundante** com `data/data_resources.csv`.

O CSV atual tem uma linha por fonte e responde perguntas institucionais e gerais: quem mantém, qual é o papel da infraestrutura, quais temas cobre e quais formas de acesso podem existir. Campos como `data_product_types`, `data_formats`, `spatial_resolution` e `temporal_resolution` precisam resumir fontes heterogêneas e, por isso, frequentemente contêm valores como “varia conforme o produto”.

O modelo novo responde perguntas científicas e operacionais que não podem ser respondidas com precisão no nível da fonte:

- qual produto ou série contém o fenômeno de interesse;
- o que o produto representa e como foi derivado;
- qual é sua cobertura, suporte espacial, resolução e periodicidade;
- qual versão, coleção, cenário ou edição deve ser citada;
- por quais arquivos, APIs ou serviços o mesmo produto pode ser obtido.

## Relação entre as tabelas

```text
Fonte / infraestrutura
  1 ─── N Produto ou série
              1 ─── N Distribuição ou forma de acesso
              1 ─── N Variável ou métrica (extensão futura)
```

### Fonte

Permanece em `data/data_resources.csv`. É a unidade institucional e funcional: portal, base, repositório, plataforma, rede ou serviço.

### Produto

Fica em `data/data_products.csv`. É uma unidade científica ou informacional reconhecível: uma série anual, coleção de imagens, família de indicadores, produto modelado, conjunto de alertas, catálogo federado ou serviço de processamento.

### Distribuição

Fica em `data/product_distributions.csv`. Representa a forma concreta de acesso a um produto: arquivo, endpoint, protocolo, API, cliente ou exportação. Formato e protocolo pertencem aqui porque um mesmo produto pode ser oferecido simultaneamente como Shapefile, GeoTIFF, CSV, WMS, WFS ou API.

## O que não deve ser duplicado

- proprietário, governança e identidade institucional permanecem na fonte;
- descrição científica, versão, resolução e cobertura específicas permanecem no produto;
- formato, URL, protocolo, autenticação e condições de download permanecem na distribuição;
- a licença é registrada no nível mais específico que a evidência permitir;
- valores gerais no nível da fonte podem ser derivados dos produtos verificados, mas não devem sobrescrever detalhes mais precisos.

## Escala de enumeração

Nem todas as fontes devem ser tratadas da mesma maneira.

- `complete`: todos os produtos relevantes e estáveis foram enumerados;
- `family_level`: a fonte é representada por famílias de produtos, evitando uma linha para cada arquivo anual ou recorte;
- `external_index`: a fonte é um catálogo muito grande ou mutável; o catálogo local registra sua estrutura e produtos selecionados, enquanto o índice integral permanece na fonte;
- `representative_sample`: amostra explicitamente incompleta, usada apenas em piloto ou demonstração.

Isso evita tentar copiar milhares de registros do Google Earth Engine, Zenodo, DataONE ou PANGAEA e, ao mesmo tempo, permite uma descrição detalhada de fontes com portfólio controlado, como TerraBrasilis ou MapBiomas.

## Piloto incorporado

O piloto usa duas fontes já presentes no catálogo:

- `DR0011` TerraBrasilis: PRODES, DETER por domínio, TerraClass, vegetação secundária e serviços OGC;
- `DR0019` Google Earth Engine Data Catalog: catálogo público, catálogos de publicadores e serviço de processamento/exportação.

O contraste testa os dois extremos do modelo: uma plataforma com famílias explicitamente listadas e um megacatálogo cuja enumeração integral deve permanecer externa.

## Busca e filtros

A interface deve indexar conjuntamente:

`nome da fonte + nome do produto + família + descrição do produto + áreas de pesquisa + palavras-chave + cobertura + formato + protocolo`.

Filtros prioritários:

1. conteúdo/fenômeno do produto;
2. área de pesquisa;
3. cobertura do Brasil;
4. suporte e resolução espacial;
5. resolução temporal e frequência de atualização;
6. formato e protocolo;
7. download gratuito e autenticação;
8. versão e estado do produto.

O filtro por descrição deve usar busca textual e palavras-chave normalizadas. O campo descritivo não substitui filtros estruturados: ele amplia descoberta sem transformar frases livres em categorias inconsistentes.

## Regras científicas

- alerta operacional não é sinônimo de desmatamento anual consolidado;
- resolução espacial não deve ser inferida pelo zoom do visualizador;
- periodicidade do dado não é frequência de atualização do portal;
- agregadores devem preservar o provedor primário;
- produtos derivados devem registrar método, coleção e versão;
- arquivos de formatos diferentes podem representar o mesmo produto e não devem gerar produtos duplicados;
- megacatálogos devem ser referenciados por índice externo, com ingestão seletiva de produtos relevantes.

## Próxima integração

A interface pública ainda precisa carregar as duas novas tabelas e oferecer busca/filtros de produto. Essa integração deve preservar os cards de fontes e adicionar uma visualização “Produtos”, evitando misturar instituições, datasets e arquivos no mesmo nível.
