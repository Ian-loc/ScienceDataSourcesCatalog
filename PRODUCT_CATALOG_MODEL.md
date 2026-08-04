# Modelo de catálogo de produtos

## Decisão

A camada de produtos **não é redundante** com `data/data_resources.csv`.

O CSV atual tem uma linha por fonte e responde perguntas institucionais e gerais: quem mantém, qual é o papel da infraestrutura, quais temas cobre e quais formas de acesso podem existir. Campos como `data_product_types`, `data_formats`, `spatial_resolution` e `temporal_resolution` precisam resumir fontes heterogêneas e, por isso, frequentemente contêm valores como “varia conforme o produto”.

O modelo de produtos responde perguntas científicas e operacionais que não podem ser respondidas com precisão no nível da fonte:

- qual produto ou série contém o fenômeno de interesse;
- o que o produto representa e como foi derivado;
- qual é sua cobertura, suporte espacial, resolução e periodicidade;
- qual versão, coleção, cenário ou edição deve ser citada;
- por quais arquivos, APIs ou serviços o mesmo produto pode ser obtido.

## Relação entre as tabelas atuais

```text
Fonte / infraestrutura
  1 ─── N Produto ou série
              1 ─── N Distribuição ou forma de acesso
```

### Fonte

Permanece em `data/data_resources.csv`. É a unidade institucional e funcional: portal, base, repositório, plataforma, rede ou serviço.

### Produto

Fica em `data/data_products.csv`. É uma unidade científica ou informacional reconhecível: uma série anual, coleção de imagens, família de indicadores, produto modelado, conjunto de alertas, catálogo federado ou serviço de processamento.

### Distribuição

Fica em `data/product_distributions.csv`. Representa a forma concreta de acesso a um produto: arquivo, endpoint, protocolo, API, cliente ou exportação. Formato e protocolo pertencem aqui porque um mesmo produto pode ser oferecido simultaneamente como Shapefile, GeoTIFF, CSV, WMS, WFS ou API.

## Extensão para o Simbioscópio

A nova direção científica exige acrescentar uma camada entre produtos e análises. Fonte, produto e distribuição permanecem necessários, mas não são suficientes para avaliar relações entre dados.

```text
Fonte
  └── Produto
        └── Distribuição ou ativo
              └── Variável
                    └── Passaporte científico

Variáveis selecionadas
  └── Avaliação de comparabilidade por operação
        └── Relação e evidência
              └── Receita e execução reproduzível
```

### Ativo de dados

`data_assets` deverá representar o objeto efetivamente acessível: arquivo, camada, coleção, endpoint, tabela, banda, API, serviço ou recurso de metadados.

A distribuição descreve uma forma de acesso. O ativo descreve aquilo que essa forma de acesso entrega ou expõe.

### Variável

`variables` deverá representar variável, indicador, banda, classe, métrica ou atributo com significado científico próprio.

A mesma variável conceitual poderá ocorrer em produtos distintos, mas cada associação produto–variável deverá preservar nome original, unidade, método, resolução, período e versão.

### Passaporte científico

O **Passaporte científico** descreve o significado necessário para combinar uma variável com outras:

- definição;
- domínio ou domínios;
- unidade;
- tipo de dado;
- população ou objeto observado;
- unidade de observação;
- suporte espacial e temporal;
- método;
- incerteza;
- proveniência;
- sensibilidade e limitações.

O contrato inicial está em `schema/scientific-variable-passport-v0.1.json`.

### Avaliação de comparabilidade

A **Avaliação de comparabilidade** é específica da operação solicitada. Ela verifica dimensões semânticas, populacionais, espaciais, temporais, metodológicas, estatísticas, de proveniência e jurídico-éticas.

Ela produz:

- classe A–E;
- transformações exigidas;
- diagnósticos necessários;
- avisos;
- autorização ou bloqueio de uso analítico;
- teto de inferência N0–N5.

O contrato inicial está em `schema/comparability-assessment-v0.1.json`.

### Relação e evidência

A entidade **Relação e evidência** representa uma relação científica proposta entre variáveis sem confundir hipótese, associação, mecanismo e causalidade.

Ela deverá registrar:

- direção esperada;
- mecanismo;
- mediadores e confundidores;
- escalas de aplicabilidade;
- estudos favoráveis, contraditórios e inconclusivos;
- concordância;
- certeza;
- aplicabilidade;
- suporte mecanístico;
- teto de inferência e revisão humana.

O contrato inicial está em `schema/scientific-relation-evidence-v0.1.json`.

## O que não deve ser duplicado

- proprietário, governança e identidade institucional permanecem na fonte;
- descrição científica, versão, resolução e cobertura específicas permanecem no produto;
- formato, URL, protocolo, autenticação e condições de download permanecem na distribuição;
- arquivo, endpoint, camada ou banda efetivamente acessível permanece no ativo;
- significado, unidade, população e suporte permanecem na variável e no passaporte;
- compatibilidade permanece na avaliação vinculada à operação;
- mecanismo e literatura permanecem na relação e evidência;
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

O piloto usa fontes já presentes no catálogo:

- `DR0011` TerraBrasilis: PRODES, DETER por domínio, TerraClass, vegetação secundária e serviços OGC;
- `DR0019` Google Earth Engine Data Catalog: catálogo público, catálogos de publicadores, serviço de processamento/exportação e Dynamic World.

O contraste testa os dois extremos do modelo: uma plataforma com famílias explicitamente listadas e um megacatálogo cuja enumeração integral deve permanecer externa.

## Busca e filtros atuais

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

## Busca e filtros futuros

O Simbioscópio deverá permitir busca por:

- variável e definição;
- unidade;
- população ou objeto observado;
- suporte espacial;
- período;
- método de obtenção;
- incerteza;
- sensibilidade;
- domínio científico;
- compatibilidade com uma operação;
- relações e mecanismos documentados.

## Regras científicas

- alerta operacional não é sinônimo de desmatamento anual consolidado;
- resolução espacial não deve ser inferida pelo zoom do visualizador;
- periodicidade do dado não é frequência de atualização do portal;
- agregadores devem preservar o provedor primário;
- produtos derivados devem registrar método, coleção e versão;
- arquivos de formatos diferentes podem representar o mesmo produto e não devem gerar produtos duplicados;
- megacatálogos devem ser referenciados por índice externo, com ingestão seletiva de produtos relevantes;
- duas variáveis com unidades iguais não são necessariamente comparáveis;
- duas versões ou produtos derivados da mesma fonte não constituem evidência independente;
- combinação visual não autoriza estatística conjunta;
- compatibilidade deve ser avaliada para a operação solicitada;
- relações científicas devem preservar evidência contraditória e limites de aplicação.

## Estratégia de migração

1. preservar as três tabelas atuais;
2. validar contratos v0.1 em paralelo;
3. selecionar variáveis piloto de múltiplos domínios;
4. criar casos dourados de comparação A–E;
5. implementar tabelas novas somente após estabilizar os contratos;
6. manter IDs estáveis e relações explícitas;
7. não promover rascunhos de evidência a conteúdo público sem revisão.

## Próxima integração

A próxima integração estrutural não deve ser um botão de correlação. Deve ser:

1. registro de variáveis;
2. passaportes científicos;
3. painel de comparabilidade;
4. linhagem de produtos;
5. ficha de relações e evidências.

Somente depois desses componentes o projeto poderá oferecer análises quantitativas sem comprometer sua integridade científica.
