# Dynamic World e ecossistema WRI: incorporação e implicações para a expansão do catálogo

**Data da revisão:** 2026-08-03  
**Escopo:** produto Dynamic World V1, registro no WRI Data Explorer, repositório `google/dynamicworld` e recursos públicos selecionados da organização GitHub do World Resources Institute.  
**Decisão:** incorporar Dynamic World como produto selecionado do Earth Engine Data Catalog e registrar separadamente suas formas de acesso, documentação, visualização e software associado.

## 1. Decisão de modelagem

Dynamic World não deve ser cadastrado como uma nova infraestrutura genérica nem confundido com o Google Earth Engine, o WRI Data Explorer ou o repositório de software que publica os modelos.

A representação adotada é:

```text
Fonte ou infraestrutura
DR0019 — Google Earth Engine Data Catalog
  └── Produto
      DP000011 — Dynamic World V1 — Google/WRI
          ├── DD000016 — ImageCollection no Earth Engine
          ├── DD000017 — registro de metadados no WRI Data Explorer
          ├── DD000018 — explorador visual oficial
          └── DD000019 — modelo e notebook de inferência no GitHub
```

Essa decisão preserva quatro objetos distintos:

1. **produto científico:** mapas probabilísticos e rótulos de uso e cobertura da terra;
2. **infraestrutura computacional:** Earth Engine, onde a coleção é consultada e processada;
3. **catálogo e documentação:** WRI Data Explorer e página oficial do Earth Engine Data Catalog;
4. **artefato de software:** modelos TensorFlow e notebook de inferência do repositório `google/dynamicworld`.

A licença do produto também não deve ser confundida com a licença do software: os dados Dynamic World usam CC BY 4.0, enquanto o repositório do model runner usa Apache License 2.0.

## 2. Dossiê técnico do Dynamic World V1

| Elemento | Registro verificado |
|---|---|
| Nome | Dynamic World V1 |
| Produtores declarados | Google e World Resources Institute; a atribuição oficial também menciona a National Geographic Society |
| Asset | `GOOGLE/DYNAMICWORLD/V1` |
| Tipo | `ee.ImageCollection` |
| Conteúdo | rótulo top-1 e probabilidades por pixel para nove classes LULC |
| Cobertura geográfica | global, incluindo o Brasil |
| Resolução espacial | 10 m para todas as bandas |
| Cobertura temporal | 2015-06-27 ao presente |
| Unidade temporal nativa | uma previsão por imagem Sentinel-2 L1C elegível |
| Revisita nominal do sensor | aproximadamente 2–5 dias, dependente da latitude |
| Regra inicial de elegibilidade | imagem Sentinel-2 L1C com `CLOUDY_PIXEL_PERCENTAGE <= 35%` |
| Controle de nuvens e sombras | S2 Cloud Probability, Cloud Displacement Index e Directional Distance Transform |
| Proveniência de cena | o identificador de cada imagem Dynamic World corresponde ao identificador da imagem Sentinel-2 L1C de origem |
| Licença dos dados | CC BY 4.0, com atribuição específica e aviso dos dados Sentinel modificados |
| Publicação principal | Brown et al. (2022), *Scientific Data*, DOI `10.1038/s41597-022-01307-4` |

### 2.1 Bandas e classes

As nove bandas probabilísticas variam de 0 a 1 e, em conjunto, somam 1 por pixel. A banda `label` contém o índice da classe com a maior probabilidade estimada.

| Valor de `label` | Banda probabilística | Classe | Cor oficial de referência |
|---:|---|---|---|
| 0 | `water` | água | `#419bdf` |
| 1 | `trees` | árvores | `#397d49` |
| 2 | `grass` | gramíneas | `#88b053` |
| 3 | `flooded_vegetation` | vegetação inundada | `#7a87c6` |
| 4 | `crops` | culturas agrícolas | `#e49635` |
| 5 | `shrub_and_scrub` | arbustos e vegetação arbustiva | `#dfc35a` |
| 6 | `built` | área construída | `#c4281b` |
| 7 | `bare` | solo ou superfície exposta | `#a59b8f` |
| 8 | `snow_and_ice` | neve e gelo | `#b39fe1` |

Cada imagem também registra:

- `dynamicworld_algorithm_version`: versão do modelo e do processo de inferência;
- `qa_algorithm_version`: versão do processamento usado para mascarar nuvens e sombras.

Essas propriedades devem integrar qualquer manifesto de proveniência produzido pelo catálogo.

## 3. Interpretação científica e cautelas

### 3.1 O rótulo top-1 não é uma classe definitiva

A banda `label` é apenas a classe de maior probabilidade relativa entre nove possibilidades. A utilização científica deve considerar as bandas probabilísticas e, quando apropriado, um limiar explícito para a probabilidade top-1.

O limiar não deve ser tratado como constante universal. Ele precisa ser escolhido e documentado segundo:

- finalidade da análise;
- classe de interesse;
- bioma e sazonalidade;
- tolerância a falso positivo e falso negativo;
- qualidade da máscara de nuvens;
- disponibilidade de referência independente.

### 3.2 Classificações de cena única são sensíveis ao contexto

As previsões são derivadas de imagens individuais e de uma janela espacial pequena. Classes que dependem de comportamento ao longo do tempo, especialmente culturas agrícolas, podem apresentar probabilidades top-1 relativamente baixas em cenas sem características fenológicas distintivas.

O WRI Data Explorer destaca ainda que:

- o desempenho varia espacial e temporalmente;
- o desempenho tende a ser mais forte em biomas temperados e dominados por árvores;
- áreas áridas, arbustivas e de pastagem apresentam confusão particularmente relevante entre culturas e arbustos;
- nuvens omitidas podem aparecer como neve e gelo;
- sombras omitidas podem aparecer como água.

No Brasil, esses alertas são particularmente importantes para Cerrado, Caatinga, Pantanal sazonal, mosaicos agropecuários e superfícies com forte variação fenológica ou hídrica.

### 3.3 Contagem de pixels não é estimativa não enviesada de área

Estatísticas zonais obtidas diretamente por contagem de pixels descrevem a classificação do produto. Elas não constituem automaticamente uma estimativa não enviesada da área real de uma classe.

Para inferência de área com validade estatística, recomenda-se:

1. definir população, domínio e período;
2. utilizar amostra de referência probabilística ou desenho amostral adequado;
3. construir matriz de erro;
4. corrigir o viés de área da classificação;
5. reportar incerteza e intervalo de confiança;
6. preservar versão do algoritmo, limiar e regras de composição.

### 3.4 Mudança aparente não é necessariamente mudança de cobertura

Mudanças entre duas cenas podem resultar de:

- fenologia;
- umidade ou inundação temporária;
- colheita e preparo do solo;
- nuvens, sombras ou fumaça residuais;
- diferenças atmosféricas ou geométricas;
- baixa margem entre as duas classes mais prováveis;
- mudança efetiva de uso ou cobertura.

Detecção de mudança deve usar séries temporais, persistência, probabilidades e inspeção das imagens Sentinel-2 correspondentes.

## 4. Papel do Dynamic World no contexto brasileiro

Dynamic World é valioso para o catálogo porque oferece granularidade temporal e probabilística que complementa produtos brasileiros consolidados. Ele não deve substituir produtos temáticos nacionais.

| Produto | Objeto principal | Temporalidade | Relação recomendada |
|---|---|---|---|
| Dynamic World | estado LULC probabilístico por cena Sentinel-2 | quase em tempo real | triagem rápida, séries probabilísticas, contexto e geração de hipóteses |
| MapBiomas | coleções anuais e produtos temáticos adaptados ao Brasil | anual e produtos específicos | referência nacional para séries consolidadas de uso e cobertura, segundo coleção e método |
| PRODES | supressão anual de vegetação nativa conforme regras de cada domínio | anual | monitoramento oficial de desmatamento consolidado; não equivale a mudança genérica de classe LULC |
| DETER | avisos operacionais de alteração | evento/operacional | fiscalização e priorização; não equivale a taxa anual consolidada |
| TerraClass | uso e cobertura em domínios e áreas definidos pelo produto | por edição | interpretação temática especializada do território pós-desmatamento ou do domínio analisado |

### 4.1 Usos de maior valor

- priorizar áreas para inspeção visual ou amostragem;
- obter contexto LULC próximo da data de uma observação ecológica;
- construir indicadores de persistência e frequência de classes;
- explorar sazonalidade agrícola, inundação e exposição de solo;
- detectar candidatos a transição para posterior validação;
- produzir covariáveis probabilísticas para modelos, preservando risco de circularidade;
- apoiar ensino de classificação probabilística e séries de observação da Terra.

### 4.2 Usos que exigem restrição explícita

- estatísticas oficiais de desmatamento;
- estimativas de área sem correção de viés;
- comparação direta de classes com legendas de MapBiomas ou TerraClass;
- identificação de culturas específicas;
- inferência causal de mudança de uso da terra;
- classificação de uma cena única como verdade de campo.

## 5. Auditoria do WRI Data Explorer

O WRI Data Explorer é uma referência relevante não porque deva ser copiado integralmente, mas porque integra descoberta, metadados, acesso operacional e documentação em uma mesma ficha.

### 5.1 Capacidades observadas

- busca textual sobre todos os metadados;
- filtros por localização, projeto, equipe, tópico, tags, cobertura temporal, frequência, formato, licença, idioma e visibilidade;
- distinção entre equipes responsáveis, aplicações que usam os dados e tópicos científicos;
- ficha com descrição curta, datas de criação e atualização, cobertura temporal, formatos e opções de pré-visualização;
- abas de descrição, arquivos, API, metodologia, contato, datasets relacionados e notas de versão;
- exemplos de consulta à API CKAN em Query, JavaScript, Python e R;
- recursos que podem ser arquivos locais, links externos, URLs de tile cache ou identificadores de assets do Earth Engine;
- visualizações tabulares, gráficos e mapas;
- possibilidade de adicionar ao mapa camadas provenientes de outros datasets.

### 5.2 O caso Dynamic World demonstra um princípio importante

O registro do Dynamic World no WRI Data Explorer informa zero arquivos locais e recomenda o uso pelo Earth Engine. Isso é correto: o catálogo não precisa fingir que todo produto possui um arquivo direto para download.

O tipo de ação deve ser explícito:

```text
baixar arquivo
abrir dado externo
copiar endpoint
copiar asset ID
abrir visualizador
consultar API de metadados
abrir metodologia
abrir código e modelo
```

Esse princípio deve orientar o Science Data Sources Catalog.

## 6. Auditoria dos recursos GitHub do WRI

Foram examinados padrões representativos, não uma enumeração integral dos repositórios da organização.

### 6.1 `wri/gfw-data-api`

O repositório mostra uma API dedicada, assíncrona e validada, baseada em FastAPI, Pydantic, PostgreSQL, migrações e contêineres. O benefício para o catálogo não é copiar essa infraestrutura imediatamente, mas adotar seus princípios:

- contrato de dados explícito;
- validação de entradas e saídas;
- documentação automática da API;
- migrações versionadas;
- testes;
- separação entre interface pública e serviço de dados;
- ambientes isolados por branch para mudanças estruturais.

### 6.2 `wri/gfw`

A documentação do Global Forest Watch separa claramente **dataset** de **layer**. O dataset mantém identidade e metadados; as layers definem comportamento de visualização, legenda, interação, fonte, estilo, animação e parâmetros.

O catálogo brasileiro deve conservar a mesma separação:

```text
produto científico
  └── distribuição ou asset
        └── configuração de camada no visualizador
```

Uma camada pode ser servida como tiles vetoriais, tiles raster, CARTO, Mapbox, raster codificado ou Earth Engine. A configuração visual não deve sobrescrever a descrição científica do produto.

### 6.3 `wri/Aqueduct40`

O repositório reúne, no mesmo release lógico:

- licença;
- citação sugerida;
- finalidade;
- log de mudanças;
- scripts de produção;
- dicionários de dados;
- FAQ.

Esse é um excelente padrão para produtos derivados próprios do catálogo: cada produto deve nascer com dados, método, dicionário, versão, citação e histórico vinculados.

### 6.4 `wri/global-power-plant-database`

Esse repositório demonstra dois princípios de governança:

1. declarar de maneira destacada quando um produto não é mais mantido e qual foi sua última versão;
2. preservar linhagem, regras de integração, identificadores e scripts mesmo quando os dados vêm de múltiplas fontes heterogêneas.

O status do repositório não deve ser inferido apenas por estrelas, commits recentes ou disponibilidade do código. O catálogo precisa registrar `ativo`, `arquivado`, `descontinuado` ou `desconhecido` a partir de evidência explícita.

## 7. Como recursos GitHub devem beneficiar o catálogo

### 7.1 GitHub não é uma categoria única de fonte

Um repositório pode representar:

- fonte de código;
- pipeline de produção;
- documentação pública;
- dicionário de dados;
- release de dataset;
- API;
- modelo treinado;
- notebook de exemplo;
- esquema ou vocabulário;
- arquivo histórico ou projeto descontinuado.

Portanto, não se recomenda criar uma lista paralela indiscriminada de repositórios. Cada repositório deve ser vinculado a uma fonte, produto, distribuição, variável, receita ou software específico.

### 7.2 Extensão recomendada do modelo

A evolução do catálogo deve acrescentar uma entidade operacional `data_assets`, com papéis controlados como:

```text
download
api
stac_collection
gee_asset
wms
wfs
tile_service
visualizer
metadata
methodology
data_dictionary
release_notes
source_code
production_pipeline
trained_model
notebook
quality_documentation
citation
license
```

Campos mínimos recomendados:

```text
asset_id
product_id
distribution_id
asset_role
access_url
repository_owner
repository_name
repository_ref
release_or_tag
commit_sha
file_path
media_type
format
protocol
license
archived
maintenance_status
last_release_date
last_access_test
provider
attribution
notes
```

A introdução dessa tabela deve ocorrer por migração versionada; os quatro acessos do Dynamic World permanecem, por enquanto, na tabela de distribuições existente.

### 7.3 Registro de maturidade técnica sem confundir qualidade científica

Um perfil de repositório pode registrar:

- licença identificada;
- release ou tag;
- DOI ou citação;
- documentação de instalação;
- dicionário de dados;
- testes automatizados;
- integração contínua;
- ambiente reproduzível;
- changelog;
- status arquivado;
- último release e última revisão humana.

Esses itens descrevem maturidade e manutenção do artefato. Eles **não certificam precisão, validade ou adequação científica do dataset**.

## 8. Plano de expansão proposto

### Fase A — enriquecimento de metadados

1. registrar contatos, notas de versão, dicionário e repositórios associados aos produtos prioritários;
2. distinguir `access_url`, `metadata_url`, `methodology_url`, `code_repository_url` e `data_dictionary_url`;
3. adicionar papéis de assets controlados;
4. preservar licença e citação no nível mais específico.

### Fase B — descoberta automatizada, sem inclusão automática

Criar um processo de triagem que consulte GitHub e outras APIs para sugerir candidatos, registrando:

- repositório e organização;
- relação com uma fonte ou produto existente;
- arquivo README, licença e citação;
- releases e tags;
- status arquivado;
- caminhos de dicionários, esquemas e pipelines;
- evidência de cobertura do Brasil;
- risco de duplicação.

A sugestão deve entrar numa fila curatorial. Nenhum repositório deve alterar silenciosamente o catálogo canônico.

### Fase C — adaptadores operacionais

Prioridades:

1. adaptador Earth Engine para registrar asset ID, bandas, propriedades e exemplos de exportação;
2. adaptador CKAN para metadados e recursos do WRI Data Explorer e de portais compatíveis;
3. adaptador GitHub para releases, arquivos documentais e status de manutenção;
4. adaptador STAC para coleções espaço-temporais;
5. adaptador OGC para WMS, WFS, WCS e OGC APIs.

### Fase D — receitas Dynamic World

As primeiras receitas reproduzíveis podem ser:

- composição temporal com mediana ou probabilidade média, sem ocultar o período;
- máscara por limiar de probabilidade configurável;
- frequência de classe por pixel;
- persistência e margem entre primeira e segunda classe;
- estatísticas por território acompanhadas de aviso de que são estatísticas do mapa;
- detecção de candidatos a mudança com persistência mínima;
- comparação visual com Sentinel-2 e produtos nacionais;
- exportação de GeoTIFF, tabela, parâmetros, citação e manifesto de proveniência.

Cada execução deve registrar:

```text
asset e período
limite espacial
bandas
algoritmo e versão de QA
limiar de probabilidade
regra de composição
projeção e escala
tratamento de NoData
parâmetros de exportação
código ou commit
citações e licenças
```

## 9. Critérios para selecionar repositórios GitHub

Um repositório merece registro quando satisfaz pelo menos uma função concreta do catálogo e possui vínculo verificável com uma fonte ou produto.

| Dimensão | Pergunta curatorial |
|---|---|
| Identidade | quem mantém e a qual produto o repositório pertence? |
| Função | contém dados, código, API, modelo, documentação ou pipeline? |
| Autoridade | é oficial, institucional, comunitário ou fork? |
| Estado | ativo, arquivado, descontinuado ou desconhecido? |
| Versionamento | há releases, tags, DOI ou commit citável? |
| Licença | dados e software possuem licenças distintas e claras? |
| Reprodutibilidade | há ambiente, dependências, testes e instruções? |
| Proveniência | entradas, transformações e saídas são rastreáveis? |
| Brasil | possui dados, método ou aplicação relevante para o país? |
| Duplicação | já está representado por outra fonte, produto ou distribuição? |

## 10. Decisões para o Explorador Federado

Dynamic World **não foi adicionado diretamente** a `data/federated_layers.json` nesta etapa.

Motivo:

- o asset Earth Engine exige autenticação e geração de mapas ou tiles por sessão ou por serviço intermediário;
- não foi identificado um endpoint público estável de tiles que possa ser consumido diretamente pelo MVP estático;
- inserir token efêmero ou credencial no repositório seria incorreto;
- uma composição temporal exige parâmetros científicos explícitos.

Condição para publicação futura:

1. implementar adaptador seguro no backend ou serviço de tiles controlado;
2. definir uma composição ou data explícita;
3. mostrar probabilidade e não apenas rótulo;
4. registrar versão, período, limiar e regra de composição;
5. manter compatibilidade inicial `C — composição visual`;
6. disponibilizar links para produto, metodologia, licença e citação.

## 11. Resultado desta intervenção

- Dynamic World passou a ser um produto pesquisável do catálogo;
- quatro formas de acesso foram diferenciadas;
- o WRI Data Explorer foi registrado como catálogo de metadados e não como arquivo de dados;
- o explorador visual foi distinguido do produto analítico;
- o repositório de modelo foi distinguido da licença e do suporte do dataset;
- foi formalizado um caminho para incorporar repositórios GitHub sem transformar o catálogo numa lista desestruturada de código;
- foi preservado o princípio de federação: a fonte autoritativa permanece externa, enquanto o catálogo normaliza descoberta, acesso, cautelas e proveniência.

## Referências e recursos oficiais

- Google Earth Engine Data Catalog. **Dynamic World V1**. `GOOGLE/DYNAMICWORLD/V1`. https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1
- Brown, C. F. et al. **Dynamic World, Near real-time global 10 m land use land cover mapping**. *Scientific Data* 9, 251 (2022). https://doi.org/10.1038/s41597-022-01307-4
- WRI Data Explorer. **Dynamic World**. https://datasets.wri.org/datasets/dynamic-world
- WRI Data Explorer. **Data Explorer User Guide**. https://datasets.wri.org/user-guide
- Dynamic World. **Explore**. https://dynamicworld.app/explore/
- Google. **Dynamic World Model Runner**. https://github.com/google/dynamicworld
- WRI. **GFW Data API**. https://github.com/wri/gfw-data-api
- WRI. **Global Forest Watch frontend and layer documentation**. https://github.com/wri/gfw
- WRI. **Aqueduct 4.0 Public Documentation**. https://github.com/wri/Aqueduct40
- WRI. **Global Power Plant Database**. https://github.com/wri/global-power-plant-database
