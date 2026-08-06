# Modelo relacional do catálogo de produtos

## 1. Decisão

A camada de produtos é o núcleo científico da Instância 1 e não é redundante com o catálogo de fontes.

A fonte responde:

- quem mantém;
- qual é a infraestrutura;
- qual papel institucional ou funcional possui;
- quais tipos gerais de conteúdo e acesso oferece.

O produto responde:

- qual informação científica existe;
- o que ela representa;
- como foi produzida;
- em qual versão;
- quais variáveis contém;
- qual é seu suporte espacial e temporal;
- quais limitações possui;
- como pode ser acessada.

## 2. Hierarquia canônica

```text
Organização
  1 ─── N Fonte ou infraestrutura
              1 ─── N Família de produtos
                          1 ─── N Produto científico
                                      1 ─── N Release, versão ou edição
                                                  1 ─── N Distribuição
                                                              1 ─── N Ativo
```

Relações científicas:

```text
Release
  N ─── N Variável, classe, indicador ou banda
              ├── método
              ├── perfil espacial
              ├── perfil temporal
              ├── perfil de qualidade
              └── interpretação científica
```

## 3. Entidades

### Organização

Instituição, consórcio, rede ou iniciativa responsável.

### Fonte ou infraestrutura

Portal, repositório, catálogo, plataforma, programa, observatório, rede ou serviço que publica ou oferece acesso.

Uma fonte pode agregar produtos de produtores diferentes. O provedor primário deve permanecer explícito.

### Família de produtos

Agrupamento de produtos relacionados por missão, programa, método ou finalidade.

A família não transfere automaticamente resolução, legenda, período, método, licença ou qualidade aos produtos membros.

### Produto científico

Conjunto coerente e versionado de informações espaciais, produzido por metodologia definida, com significado temático, cobertura, suporte espacial e temporal, variáveis e formas de distribuição identificáveis.

Exemplos:

- série anual de supressão de vegetação;
- coleção de cobertura e uso da terra;
- série de indicadores municipais;
- produto de biomassa modelada;
- conjunto de alertas;
- mapa de referência territorial;
- coleção de ocorrências georreferenciadas.

Não são produtos científicos por si sós:

- catálogo genérico;
- API genérica;
- serviço de processamento;
- visualizador;
- protocolo;
- formato;
- página de download.

### Release, versão ou edição

Manifestação identificável de um produto.

Pertencem a esta entidade:

- versão;
- coleção;
- ano-base;
- cenário;
- edição;
- data de release;
- estado atual, substituído ou experimental;
- notas de mudança.

Distribuições pertencem ao release, não ao produto abstrato, porque formatos, URLs e conteúdos podem mudar entre versões.

### Distribuição

Forma de acesso ao release:

- download direto;
- API;
- serviço geoespacial;
- registro de catálogo;
- visualizador;
- repositório de código;
- formulário;
- documentação.

### Ativo

Objeto concreto exposto pela distribuição:

- arquivo;
- tabela;
- endpoint;
- camada;
- coleção;
- legenda;
- arquivo de qualidade;
- metadado;
- esquema;
- recurso de incerteza.

### Variável ou componente informacional

Propriedade, indicador, banda, classe, métrica, atributo ou flag com significado próprio.

A variável possui definição canônica, enquanto a associação produto–variável preserva:

- nome original;
- papel;
- unidade;
- tipo;
- definição do produtor;
- método;
- suporte;
- interpretação;
- limitações.

### Método

Descreve como a informação foi produzida:

- medição;
- sensoriamento remoto;
- registro administrativo;
- censo;
- levantamento amostral;
- classificação;
- modelagem;
- interpolação;
- agregação;
- índice composto.

### Perfil espacial

Descreve:

- suporte;
- geometria;
- resolução;
- escala;
- unidade mínima;
- CRS;
- grade;
- extensão;
- unidade geográfica;
- agregação;
- limitações espaciais.

### Perfil temporal

Descreve:

- período;
- janela de observação;
- resolução;
- frequência;
- latência;
- calendário;
- agregação;
- limitações temporais.

### Perfil de qualidade

Descreve:

- validação;
- acurácia;
- incerteza;
- flags;
- ausências;
- viés de coleta;
- artefatos;
- representatividade.

### Capacidade de acesso

Registra se uma distribuição permite:

- descobrir;
- pré-visualizar;
- visualizar;
- consultar atributos;
- recortar;
- baixar;
- processar;
- exportar;
- abrir em QGIS, R, Python ou Earth Engine.

A capacidade pode ser disponível, condicional, indisponível ou desconhecida.

### Evidência de metadados

Afirmações importantes devem indicar a fonte que as sustenta.

O modelo registra:

- entidade;
- campo;
- valor;
- URL;
- tipo de evidência;
- nota de suporte;
- data de recuperação;
- confiança curatorial.

## 4. Esquema executável

O esquema de referência está em:

`database/schema/001_instance1_core.sql`

O banco-alvo é PostgreSQL/PostGIS.

Os CSVs atuais permanecem canônicos durante a transição. O banco será promovido após migração, auditoria e geração reproduzível das exportações.

## 5. Mensagem informacional

Todo produto deve possuir uma descrição técnica e uma **mensagem informacional**.

A descrição informa o que o produto é.

A mensagem informacional responde:

> Que informação sobre o mundo real este produto comunica?

Também deve existir `non_representations`, indicando interpretações que o produto não sustenta diretamente.

Exemplo:

```text
Produto: alertas DETER
Mensagem: localização e classe de evidências detectadas de alteração da cobertura.
Não representa: taxa anual consolidada, data exata da ocorrência ou legalidade da alteração.
```

## 6. Escala de enumeração

- `complete`: portfólio relevante enumerado integralmente;
- `family_level`: famílias registradas, com aprofundamento progressivo;
- `external_index`: índice integral permanece externo;
- `representative_sample`: amostra piloto explicitamente incompleta;
- `selective`: seleção orientada por Brasil, relevância e utilidade.

Megacatálogos não devem ser copiados integralmente. Seus produtos prioritários podem ser curados seletivamente.

## 7. Regras de normalização

- organização não é fonte;
- fonte não é produto;
- família não é release;
- produto não é arquivo;
- distribuição não é variável;
- formato não é protocolo;
- serviço não é informação científica;
- visualizador não é produto, exceto quando contém produto próprio claramente definido;
- resolução pertence ao suporte que descreve;
- versão pertence ao release;
- URL de acesso pertence à distribuição ou ao ativo;
- significado pertence ao produto e à variável;
- método e qualidade devem ser vinculados no nível mais específico disponível;
- licença deve ser registrada no nível mais específico sustentado pela evidência.

## 8. Busca e filtros

A Instância 1 deverá permitir filtros por:

- tema;
- fenômeno;
- objeto observado;
- produto;
- variável ou classe;
- natureza de produção;
- método;
- unidade;
- suporte espacial;
- resolução;
- unidade territorial;
- período;
- resolução temporal;
- incerteza disponível;
- cobertura do Brasil;
- gratuidade;
- autenticação;
- protocolo;
- formato;
- capacidade de visualização, recorte, consulta ou download;
- versão e estado.

A interface não deve exigir operadores booleanos. A busca textual complementa os filtros estruturados.

## 9. Migração dos dados atuais

### Estado atual

As três tabelas públicas são:

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`.

### Problema identificado

O piloto de produtos mistura:

- produtos científicos;
- catálogos;
- serviços interoperáveis;
- infraestruturas de processamento.

### Regra de correção

- catálogos e infraestruturas migram para `sources`;
- serviços genéricos migram para `distributions` e `access_capabilities`;
- produtos científicos permanecem em `products`;
- versões migram para `product_releases`;
- variáveis migram para `variables` e `product_variables`;
- URLs e formatos migram para `distributions` e `data_assets`.

## 10. Instâncias futuras

### Instância 2

Consumirá releases, variáveis, distribuições e capacidades da Instância 1 para resolver camadas visualizáveis.

### Instância 3

Consumirá significado científico, taxonomias, escala, território e método para recuperar e sintetizar literatura relevante.

Essas extensões não alteram a prioridade atual: o catálogo deve primeiro ser profundo, preciso, relacional e útil por si só.
