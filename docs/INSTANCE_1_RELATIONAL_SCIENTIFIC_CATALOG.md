# Instância 1 — Catálogo relacional científico-operacional

**Status:** direção canônica de implementação e curadoria  
**Prioridade:** foco ativo do projeto  
**Escopo:** produtos de dados com informação geográfica explícita ou associação territorial inequívoca  
**Banco-alvo:** PostgreSQL com PostGIS  
**Princípio:** identificar precisamente o objeto científico e operacional que cada plataforma entrega

## 1. Decisão

O desenvolvimento ativo do projeto concentra-se na **Instância 1**: um catálogo relacional aprofundado de fontes e produtos de dados georreferenciados sobre o Brasil.

O objetivo imediato não é ampliar funcionalidades analíticas, calcular relações entre variáveis nem generalizar a sobreposição de camadas. O objetivo é construir uma base científica, técnica e operacional suficientemente precisa para que o catálogo seja útil por si só e possa sustentar expansões futuras sem reconstrução conceitual.

A Instância 1 deverá permitir ao usuário:

1. descobrir fontes e produtos;
2. compreender o que cada produto representa no mundo real;
3. identificar quais variáveis, classes, indicadores ou atributos o produto contém;
4. compreender como os dados foram produzidos;
5. reconhecer suporte, resolução, cobertura e estrutura temporal;
6. avaliar qualidade, incerteza, viés e limitações declaradas;
7. localizar versões, documentação, citação e licença;
8. saber como acessar os dados e quais operações técnicas são oferecidas;
9. distinguir produto científico, plataforma, catálogo, serviço, visualizador, distribuição e arquivo;
10. comparar perfis de produtos sem declarar compatibilidade científica universal.

## 2. Separação das três instâncias

### Instância 1 — Catálogo relacional científico-operacional

**Estado:** foco ativo e autorizado.

Objeto central:

```text
Fonte ou infraestrutura
  └── Família de produtos
        └── Produto científico
              └── Versão ou edição
                    ├── Variáveis e classes
                    ├── perfil espacial e temporal
                    ├── método e qualidade
                    └── distribuições, ativos e capacidades de acesso
```

A Instância 1 não armazena necessariamente os datasets externos. Ela armazena metadados normalizados, significado científico, proveniência, formas de acesso e evidências de curadoria.

### Instância 2 — Composição de produtos georreferenciados

**Estado:** ambição documentada; implementação não prioritária e não autorizada nesta fase.

Objeto futuro:

- selecionar camadas resolvidas a partir de produtos catalogados;
- verificar executabilidade técnica;
- visualizar conjuntamente produtos georreferenciados;
- preservar fonte, versão, método, escala, incerteza e citação;
- oferecer sobreposição, mapas sincronizados ou perfis territoriais sem tratar composição visual como associação científica.

A Instância 2 dependerá da qualidade e da estrutura produzidas na Instância 1.

### Instância 3 — Contextualização científica da composição

**Estado:** ambição documentada; somente leitura conceitual nesta fase.

Objeto futuro:

- recuperar literatura relacionada aos fenômenos representados pelos produtos selecionados;
- apresentar síntese científica curta e auditável;
- explicar o significado ecológico, social, sanitário ou territorial da composição;
- comunicar mecanismos discutidos na literatura, controvérsias, limitações e variáveis de confusão;
- evitar transformar coincidência espacial em correlação ou causalidade.

A Instância 3 não deverá gerar perguntas de pesquisa para o usuário nem funcionar como interface booleana de busca bibliográfica. Ela deverá usar os metadados estruturados da Instância 1 para contextualizar, em linguagem acessível, uma composição escolhida pelo usuário.

## 3. Regra de escopo geográfico

O catálogo registra produtos que:

- contenham coordenadas, geometrias, grades, pixels, footprints, trajetórias ou unidades territoriais; ou
- possuam ligação inequívoca a município, estado, bioma, bacia, unidade de conservação, setor censitário, estabelecimento, parcela, localidade ou outra unidade geográfica identificável.

Uma tabela município–ano é georreferenciável mesmo quando distribuída em CSV ou XLSX. Um PDF sem georreferenciamento pode ser documentação, metodologia ou produto cartográfico de consulta, mas não é automaticamente uma camada operacional.

O banco descreve a geografia do produto; não precisa hospedar a totalidade dos dados espaciais.

## 4. Definições canônicas

### Fonte

Infraestrutura institucional ou funcional que publica, organiza, hospeda ou oferece acesso a produtos.

Exemplos: portal, repositório, observatório, programa, rede, catálogo, plataforma ou infraestrutura computacional.

### Família de produtos

Agrupamento oficial ou curatorial de produtos relacionados por missão, programa, método ou finalidade, sem presumir que compartilhem a mesma resolução, legenda, período ou qualidade.

### Produto científico

Conjunto cientificamente coerente e versionado de informações espaciais, produzido por metodologia definida, com significado temático, cobertura, suporte espacial e temporal, variáveis e formas de distribuição identificáveis.

Não são produtos científicos, por si sós:

- organizações;
- portais;
- megacatálogos;
- APIs genéricas;
- serviços de processamento;
- visualizadores;
- formatos de arquivo;
- páginas de download.

Esses elementos devem aparecer como fontes, distribuições, ativos ou capacidades de acesso.

### Versão ou edição

Manifestação temporal e metodológica identificável de um produto. Coleção, release, ano-base, cenário ou edição devem ser preservados porque mudanças podem alterar toda a série histórica, a legenda, o método ou os resultados.

### Distribuição

Forma pela qual uma versão do produto é acessada: download, API, serviço geoespacial, catálogo, visualizador, repositório de código, formulário ou documentação.

### Ativo

Objeto concreto exposto por uma distribuição: arquivo, endpoint, camada, coleção, tabela, legenda, metadado, banda, recurso de qualidade ou esquema.

### Variável ou componente informacional

Propriedade, indicador, banda, classe, métrica, atributo ou flag com significado próprio dentro do produto.

A variável não substitui o produto como unidade pública principal. Ela aprofunda o perfil e permite buscas precisas, interpretação científica e expansões posteriores.

## 5. O perfil científico-operacional do produto

Cada produto deve possuir um perfil organizado em seis blocos.

### 5.1 Identidade e proveniência

- nome oficial;
- acrônimo;
- fonte e organização produtora;
- família;
- versão, edição ou coleção;
- estado: ativo, experimental, legado, descontinuado;
- página oficial;
- documentação metodológica;
- citação recomendada;
- licença;
- data de revisão curatorial.

### 5.2 Significado científico

- objeto científico representado;
- fenômeno ou processo;
- população ou universo de referência;
- mensagem informacional do produto;
- variáveis, classes e indicadores contidos;
- unidade e tipo de dado;
- usos científicos potenciais;
- o que o produto não representa diretamente.

A descrição deve responder em linguagem clara:

> Que informação sobre o mundo real está registrada aqui?

Exemplos:

- um alerta DETER representa evidência detectada de alteração da cobertura, não uma taxa anual consolidada de desmatamento;
- uma classe de vegetação secundária representa uma área classificada como regeneração, não uma medição direta de biomassa, carbono ou diversidade;
- um índice espectral representa uma transformação de reflectâncias, não a propriedade ecológica final que pode estar associada a ele;
- uma taxa municipal de internações representa registros administrativos agregados, não risco individual nem necessariamente incidência da doença.

### 5.3 Natureza de produção

- medido;
- observado por sensor;
- registro administrativo;
- censo;
- levantamento amostral;
- classificado;
- modelado;
- interpolado;
- agregado;
- derivado;
- índice composto;
- método misto.

O método deve registrar entradas, processamento, validação, versão e limitações.

### 5.4 Estrutura espacial e temporal

- tipo de geometria;
- suporte espacial;
- resolução nominal;
- escala cartográfica, quando aplicável;
- unidade mínima mapeável;
- CRS;
- grade;
- unidade geográfica;
- extensão;
- cobertura temporal;
- janela de observação;
- resolução temporal;
- frequência de atualização;
- latência;
- forma de agregação.

Resolução, suporte e escala não são sinônimos. O catálogo deve registrar o que cada valor significa.

### 5.5 Qualidade, incerteza e limitações

- desenho de validação;
- métricas de acurácia;
- incerteza disponível;
- tipo de incerteza;
- flags de qualidade;
- tratamento de ausência de dados;
- cobertura de nuvens;
- erro de classificação;
- viés de coleta;
- detectabilidade;
- representatividade;
- artefatos conhecidos;
- limitações de interpretação.

A ausência de documentação deve permanecer explícita. Não se deve inferir que incerteza inexiste apenas porque não está registrada.

### 5.6 Acesso operacional

- download gratuito, parcial ou pago;
- autenticação;
- condições de acesso;
- protocolo;
- formato;
- API;
- WMS, WFS, WCS, WMTS ou OGC API;
- STAC;
- COG;
- Earth Engine;
- ferramentas de acesso;
- suporte a recorte espacial ou temporal;
- visualização direta;
- consulta de atributos;
- capacidade de exportação;
- estado atual do endpoint.

A existência de API não garante visualização imediata. O catálogo deve registrar requisitos de projeto, credenciais, quotas, processamento ou transformação.

## 6. Modelo relacional

O esquema executável inicial está em:

`database/schema/001_instance1_core.sql`

O banco-alvo é PostgreSQL com PostGIS porque:

1. o volume de metadados e relações excederá a manutenção segura em uma única planilha;
2. integridade referencial é necessária para distinguir fontes, produtos, versões, distribuições e variáveis;
3. PostGIS permite registrar extensão, cobertura e suporte geográfico sem hospedar os datasets externos;
4. busca textual, filtros e API podem ser construídos sobre o mesmo núcleo;
5. versões e evidências de curadoria precisam de rastreabilidade;
6. as Instâncias 2 e 3 poderão consumir o mesmo banco no futuro.

O modelo normaliza:

- organizações;
- fontes;
- famílias de produtos;
- produtos;
- versões;
- perfis espaciais;
- perfis temporais;
- métodos;
- perfis de qualidade;
- variáveis;
- associações produto–variável;
- distribuições;
- ativos;
- capacidades de acesso;
- taxonomias;
- citações;
- evidências de metadados;
- revisões curatoriais.

## 7. Autoridade e transição dos dados

Durante a migração:

1. `data/data_resources.csv`, `data/data_products.csv` e `data/product_distributions.csv` permanecem fontes canônicas operacionais da versão pública atual;
2. o esquema relacional é o modelo canônico de destino;
3. os CSVs serão importados para tabelas de staging;
4. registros serão normalizados e promovidos somente após validação;
5. exportações CSV e planilhas futuras serão derivadas do banco relacional;
6. a planilha do Drive permanecerá espelho e não deverá liderar alterações canônicas;
7. nenhuma informação será inventada para completar campos obrigatórios; registros incompletos permanecerão em estado de curadoria.

Após o portão de migração, o PostgreSQL deverá tornar-se a fonte canônica, e os CSVs passarão a ser exportações versionadas.

## 8. Regra de enumeração

Nem toda fonte deverá ser copiada integralmente.

- `complete`: portfólio controlado e totalmente enumerado;
- `family_level`: famílias estáveis são registradas e produtos específicos são aprofundados progressivamente;
- `external_index`: megacatálogo permanece externo; produtos brasileiros prioritários são selecionados;
- `representative_sample`: amostra explicitamente incompleta para teste;
- `selective`: inclusão orientada por relevância, cobertura do Brasil e utilidade científica.

Earth Engine, Zenodo, DataONE e PANGAEA não devem ser replicados integralmente. MapBiomas, TerraBrasilis, IBGE, ANA, DATASUS e outras fontes com produtos brasileiros prioritários devem receber enumeração mais profunda e estruturada.

## 9. Separação entre produto, serviço e infraestrutura

A revisão do piloto identificou que registros científicos e infraestruturas estavam misturados em `data_products.csv`.

Devem migrar para fonte, distribuição ou capacidade de acesso:

- serviços interoperáveis genéricos;
- catálogos públicos;
- catálogos de publicadores;
- serviços de processamento e exportação;
- visualizadores sem conteúdo científico próprio.

Devem permanecer como produtos:

- séries de mapeamento;
- coleções de observações;
- indicadores territoriais;
- mapas classificados;
- modelos e estimativas;
- estatísticas administrativas georreferenciáveis;
- produtos de referência espacial.

## 10. Busca e filtros da Instância 1

A interface pública deverá oferecer filtros acessíveis, sem exigir sintaxe booleana.

### Temas

- ecologia;
- socioecologia;
- biodiversidade;
- clima;
- água;
- saúde;
- sociedade;
- desigualdade;
- agricultura;
- agricultura familiar;
- uso e cobertura da terra;
- carbono;
- demografia;
- economia;
- infraestrutura;
- governança.

### Conteúdo científico

- fenômeno;
- objeto observado;
- variável ou classe;
- natureza de produção;
- unidade;
- método;
- incerteza disponível;
- produto primário ou derivado.

### Estrutura geográfica

- cobertura;
- suporte;
- resolução;
- unidade territorial;
- tipo de geometria;
- período;
- frequência temporal.

### Acesso

- gratuito;
- autenticação;
- API;
- download;
- serviço geoespacial;
- Earth Engine;
- compatibilidade com QGIS, R ou Python;
- recorte espacial e temporal;
- visualização disponível.

## 11. Curadoria contínua

A unidade de trabalho é **um produto integralmente inspecionado**, não uma linha preenchida superficialmente.

Para cada produto:

1. identificar a fonte e o produtor primário;
2. confirmar que o objeto é produto científico, e não serviço ou plataforma;
3. localizar página oficial, documentação, metodologia, citação, licença e acesso;
4. identificar versões e releases;
5. descrever o objeto científico e a mensagem informacional;
6. enumerar variáveis, classes e flags relevantes;
7. registrar natureza de produção;
8. registrar suporte espacial e temporal;
9. registrar qualidade, incerteza, viés e limitações;
10. registrar distribuições e capacidades de acesso;
11. criar evidências por campo para afirmações importantes;
12. executar revisão de completude, precisão científica e precisão operacional;
13. promover o registro somente depois da auditoria.

A curadoria deve priorizar produtos brasileiros e produtos internacionais com cobertura efetiva do Brasil.

## 12. Evidência e rastreabilidade

O campo `metadata_assertions` registra qual evidência sustenta afirmações importantes.

Exemplos:

- resolução declarada;
- período;
- natureza derivada;
- definição de classe;
- precisão;
- licença;
- capacidade de API;
- estado experimental;
- versão atual.

A evidência pode ser:

- página oficial;
- documentação oficial;
- relatório técnico;
- artigo revisado por pares;
- registro de metadados;
- licença;
- resposta de API;
- inferência curatorial explicitamente rotulada.

A data de revisão não certifica automaticamente toda a fonte ou todos os produtos associados.

## 13. Portões de consolidação

### Portão A — contrato relacional

- esquema SQL versionado;
- definições canônicas aprovadas;
- separação entre produto e infraestrutura;
- IDs e chaves estrangeiras estáveis;
- campos científicos essenciais definidos.

### Portão B — migração do piloto

- 11 registros atuais classificados corretamente;
- serviços e catálogos retirados do conjunto de produtos científicos;
- releases explícitos;
- distribuições vinculadas a releases;
- variáveis piloto identificadas;
- evidências de metadados registradas.

### Portão C — expansão de fontes prioritárias

- MapBiomas profundamente enumerado;
- TerraBrasilis revisado por produto e bioma;
- IBGE, ANA e DATASUS com produtos prioritários;
- cobertura ecológica, socioeconômica e de saúde;
- filtros funcionando sobre dados normalizados.

### Portão D — promoção do banco

- PostgreSQL torna-se fonte canônica;
- CSVs e planilhas são exportações reproduzíveis;
- validação automática de integridade;
- interface lê do banco ou de uma API derivada;
- documentação e dados permanecem sincronizados.

## 14. Critério de sucesso da Instância 1

O sucesso não será medido apenas pelo número de fontes ou produtos.

Será medido pela capacidade de responder com precisão:

- o que este produto representa;
- qual é a unidade científica ou informacional;
- como o valor, classe ou geometria foi produzido;
- qual é o suporte espacial e temporal;
- quais variáveis estão disponíveis;
- quais limitações existem;
- qual versão deve ser usada;
- como acessar os dados;
- o que é possível fazer tecnicamente;
- qual evidência sustenta cada afirmação importante.

## 15. Instâncias 2 e 3 — registro somente para leitura

As seguintes ambições ficam preservadas, mas fora do escopo ativo:

### Instância 2

- composição visual de camadas resolvidas;
- mapas sincronizados;
- perfis territoriais;
- transparência comparativa;
- verificação de executabilidade;
- processamento seletivo por adaptadores e receitas.

### Instância 3

- contexto científico breve associado à composição;
- recuperação de literatura por fenômenos, território, escala e período;
- síntese auditável semelhante, em espírito, a uma revisão curta assistida;
- distinção entre evidência direta, análoga e metodológica;
- comunicação pública palatável;
- nenhuma inferência automática de causalidade.

Nenhuma dessas instâncias deve orientar a modelagem de forma a enfraquecer ou atrasar a Instância 1. A obrigação atual é construir um catálogo profundo, preciso, documentado e útil por si mesmo.
