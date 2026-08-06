# Direção científica do projeto

**Status:** decisão estratégica vigente  
**Sistema de trabalho:** **Symbiotrama**  
**Foco ativo:** **Instância 1 — Catálogo relacional científico-operacional**  
**Princípio:** **Antes de investigar relações, é preciso compreender precisamente cada informação.**

## 1. Decisão central

O projeto consolida primeiro um banco relacional profundo de fontes e produtos de dados georreferenciados sobre o Brasil.

A prioridade não é implementar imediatamente análises, correlações, sínteses automáticas de literatura ou combinações universais. A prioridade é identificar com precisão o objeto científico e operacional entregue por cada plataforma.

O catálogo deve permitir descobrir:

- quem produz;
- qual é o produto;
- qual versão está disponível;
- qual fenômeno representa;
- quais variáveis, classes ou indicadores contém;
- como foi produzido;
- qual é o suporte espacial e temporal;
- quais limitações, incertezas e vieses existem;
- como acessar, visualizar, consultar ou baixar;
- quais evidências sustentam os metadados registrados.

## 2. Missão da Instância 1

> Organizar e descrever produtos de dados georreferenciados sobre o Brasil com profundidade científica, integridade relacional, proveniência e precisão operacional, tornando explícito o significado de cada informação e as condições de seu uso.

A Instância 1 deve ser útil como sistema autônomo, independentemente da implementação das expansões futuras.

## 3. Objeto científico

O objeto principal é o **produto científico georreferenciado**.

Um produto é um conjunto coerente e versionado de informações espaciais, produzido por metodologia definida, com significado temático, cobertura, suporte espacial e temporal, variáveis e formas de distribuição identificáveis.

O catálogo também registra, em entidades separadas:

- organizações;
- fontes e infraestruturas;
- famílias de produtos;
- versões e edições;
- distribuições;
- ativos;
- variáveis e classes;
- métodos;
- perfis espaciais e temporais;
- qualidade e incerteza;
- taxonomias;
- citações;
- evidências e revisão curatorial.

## 4. Escopo geográfico

O catálogo trabalha somente com produtos que contenham informação geográfica ou associação territorial inequívoca.

São incluídos:

- rasters;
- vetores;
- pontos e footprints;
- trajetórias;
- grades;
- bacias;
- biomas;
- unidades de conservação;
- municípios, estados e outras unidades administrativas;
- tabelas com códigos territoriais;
- séries território–tempo.

O banco descreve os produtos e sua geografia; não precisa hospedar integralmente os datasets externos.

## 5. Significado científico obrigatório

Cada produto deve responder:

1. que fenômeno representa;
2. qual objeto, população ou território observa;
3. qual informação o valor, classe ou geometria comunica;
4. quais variáveis ou classes contém;
5. se é medido, administrativo, amostral, classificado, modelado, interpolado, agregado ou derivado;
6. o que o produto não representa diretamente;
7. quais usos potenciais possui;
8. quais limitações condicionam sua interpretação.

Exemplos de distinções obrigatórias:

- alerta operacional não é inventário anual consolidado;
- índice espectral não é a propriedade ecológica final;
- classe de vegetação secundária não é biomassa ou diversidade medida;
- taxa municipal não é risco individual;
- produto classificado não é observação direta da classe;
- infraestrutura computacional não é produto científico.

## 6. Arquitetura científica

```text
Organização
  └── Fonte ou infraestrutura
        └── Família de produtos
              └── Produto científico
                    └── Release, versão ou edição
                          ├── variável, indicador, banda ou classe
                          ├── método
                          ├── perfil espacial
                          ├── perfil temporal
                          ├── perfil de qualidade
                          └── distribuição
                                ├── ativo
                                └── capacidade de acesso
```

O modelo executável está em `database/schema/001_instance1_core.sql`.

## 7. Princípios permanentes

1. Fonte, produto, versão, distribuição e ativo são entidades distintas.
2. Portais, catálogos genéricos, serviços de processamento e visualizadores não são produtos científicos por si sós.
3. Metadados da fonte não substituem metadados específicos do produto.
4. Metadados de uma versão não devem ser generalizados para toda a série.
5. Resolução, suporte e escala não são sinônimos.
6. Periodicidade do dado não é frequência de atualização do portal.
7. A ausência de documentação deve permanecer explícita.
8. Incerteza desconhecida não equivale a incerteza inexistente.
9. Uso científico potencial não equivale a variável medida.
10. Afirmações materiais devem ser sustentadas por evidência rastreável.
11. A planilha e os CSVs são formatos de intercâmbio; a arquitetura final exige integridade relacional.
12. O catálogo aponta para a fonte autoritativa e preserva citação, versão e licença.

## 8. Banco de dados

O banco-alvo é PostgreSQL com PostGIS.

Essa decisão sustenta:

- integridade referencial;
- crescimento do inventário;
- busca textual e filtros;
- relações muitos-para-muitos;
- versionamento;
- evidência por campo;
- cobertura geográfica consultável;
- API futura;
- geração reproduzível de CSVs e planilhas.

PostGIS é usado para metadados espaciais. O projeto não assume armazenamento integral de grandes rasters, vetores ou cubos externos.

## 9. Curadoria

A unidade de trabalho é um produto integralmente inspecionado.

A curadoria deve incluir:

- identidade;
- versão;
- significado científico;
- variáveis;
- método;
- suporte espacial e temporal;
- qualidade e incerteza;
- limitações;
- acesso;
- licença;
- citação;
- evidências;
- auditoria.

A expansão seguirá prioridade Brasil primeiro e será realizada fonte por fonte, produto por produto.

## 10. Instância 2 — composição geográfica

**Estado:** ambição futura registrada; não é foco ativo.

Poderá permitir:

- seleção de camadas resolvidas;
- sobreposição ou mapas sincronizados;
- perfis territoriais;
- transparência comparativa;
- verificação de executabilidade técnica;
- preservação de escala, método, versão e proveniência.

A Instância 2 dependerá de produtos e distribuições suficientemente descritos na Instância 1.

## 11. Instância 3 — contexto científico

**Estado:** ambição futura registrada; não é foco ativo.

Poderá apresentar síntese breve e auditável da literatura sobre os fenômenos representados em uma composição escolhida pelo usuário.

A Instância 3 deverá:

- usar metadados da Instância 1;
- priorizar literatura aplicável ao Brasil e à escala observada;
- distinguir evidência direta, análoga e metodológica;
- comunicar mecanismos, controvérsias e limitações;
- não gerar perguntas para o usuário;
- não transformar coincidência espacial em associação ou causalidade.

## 12. Regra de prioridade

Toda nova intervenção deverá responder:

> Esta mudança melhora a capacidade de descobrir, compreender, verificar e acessar produtos de dados georreferenciados?

Mudanças voltadas exclusivamente às Instâncias 2 ou 3 permanecem no backlog até a consolidação da Instância 1.

## 13. Critério de sucesso

O sucesso da fase atual será medido pela capacidade de responder com precisão:

- o que este produto representa;
- qual informação científica está contida nele;
- quais variáveis disponibiliza;
- como os dados foram produzidos;
- em que escala e período podem ser interpretados;
- quais incertezas e limitações existem;
- qual versão deve ser usada;
- como acessar os dados;
- quais evidências sustentam o registro.

A documentação detalhada está em `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`.
