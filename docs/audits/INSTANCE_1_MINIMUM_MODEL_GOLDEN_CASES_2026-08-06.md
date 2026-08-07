# Casos de validação do modelo mínimo da Instância 1

**Data:** 6 de agosto de 2026  
**Revalidação:** 7 de agosto de 2026, America/Sao_Paulo  
**Objetivo:** testar se o modelo representa ofertas heterogêneas sem reconstrução integral das fontes.

## 1. Critérios comuns

Cada caso deve permitir:

- uma entrada pública compreensível;
- organização e identidade oficial;
- modalidades, temas e variáveis principais;
- cobertura espacial e temporal;
- acesso e links oficiais;
- metadados adicionais sem proliferação de tabelas;
- candidato a conector opcional;
- conclusão sem inventário de arquivos, layers ou releases.

O caso falha se exigir decomposição integral da plataforma ou se perder informação indispensável ao usuário.

## 2. Caso A — GEDI

### Representação proposta

- uma entrada de catálogo para a missão/família de dados GEDI;
- organização responsável;
- modalidade `LiDAR orbital`;
- conteúdos principais, como estrutura vertical da vegetação, altura do dossel, waveform e biomassa;
- cobertura e período gerais;
- condições de acesso;
- links oficiais de página, metadados, método e acesso.

### Não requerido

- entrada para cada nível de processamento;
- cadastro de cada arquivo ou grânulo;
- inventário de bandas, tabelas e versões;
- reconstrução do catálogo da NASA.

### Conector futuro

Um identificador de coleção específico pode ser registrado somente quando um conector selecionado exigir esse identificador.

### Resultado esperado

`PASS` se uma ficha única ou poucas subentradas materialmente distintas forem suficientes.

## 3. Caso B — DETER Cerrado

### Representação proposta

- uma entrada para o sistema de alertas DETER Cerrado;
- INPE como organização e TerraBrasilis como plataforma principal de acesso;
- modalidade de monitoramento por sensoriamento remoto;
- alerta de alteração da cobertura como escopo;
- variáveis e classes principais em nível resumido;
- cobertura Cerrado, temporalidade operacional e links oficiais;
- método, acesso, licença e citação quando documentados.

### Não requerido

- resolver release vigente;
- separar `_curr` e `_hist` como entidades;
- inventariar cada layer ou endpoint;
- inspecionar bytes, checksum e schema físico;
- reproduzir todos os guards do PR #57.

### Limite científico necessário

A ficha deve deixar claro que alerta operacional não é inventário ou taxa anual consolidada.

### Resultado esperado

`PASS` se o conteúdo útil puder ser condensado em uma ficha curta com evidências proporcionais.

## 4. Caso C — IBGE

### Representação proposta

- entrada ampla para o IBGE como fonte institucional, com plataformas oficiais materialmente distintas separáveis apenas quando isso melhorar descoberta ou acesso;
- modalidades territoriais, estatísticas, censitárias e cartográficas;
- temas e variáveis representativos;
- cobertura nacional;
- links para portal, metadados e acesso.

### Subentradas permitidas

Somente quando uma plataforma ou coleção possui identidade e função próprias, como um sistema estatístico ou uma oferta cartográfica claramente separada.

### Não requerido

- entrada para cada tabela;
- entrada para cada código de variável;
- enumeração de todas as pesquisas, anos e arquivos;
- espelho do SIDRA ou de outros catálogos.

### Resultado esperado

`PASS` se o usuário puder descobrir a oferta e ser encaminhado ao sistema oficial sem duplicação massiva.

## 5. Caso D — ANA/SNIRH

### Representação proposta

- entrada para o SNIRH e subentradas apenas para sistemas ou coleções materialmente distintas;
- ANA como organização responsável;
- modalidades como séries hidrológicas, dados tabulares, vetores, mapas e serviços;
- cobertura, atualização e acesso em nível geral;
- links oficiais para dados e documentação.

### Não requerido

- entrada para cada shapefile, planilha ou PDF;
- inventário de todas as bacias e layers;
- modelagem de cada formato como distribuição ou ativo;
- download e inspeção de cada pacote.

### Conector futuro

Serviço ou API selecionado pode ganhar `connector_profile` quando houver caso de uso concreto.

### Resultado esperado

`PASS` se formatos diferentes puderem ser descritos como parte da oferta sem virar entidades públicas obrigatórias.

## 6. Matriz de avaliação estrutural

| Critério | GEDI | DETER Cerrado | IBGE | ANA/SNIRH |
|---|---:|---:|---:|---:|
| entrada compreensível | sim | sim | sim | sim |
| variáveis/temas principais | sim | sim | sim | sim |
| cobertura e período | sim | sim | sim | sim |
| links oficiais | sim | sim | sim | sim |
| inventário integral necessário | não | não | não | não |
| release obrigatória | não | não | não | não |
| ativo obrigatório | não | não | não | não |
| conector obrigatório | não | não | não | não |
| campos adicionais fora do núcleo | não | não | não | não |

## 7. Perfis estruturados materializados

Os perfis abaixo são **test fixtures de granularidade**, não novos registros públicos e não constituem inventário das plataformas. A verificação usa páginas oficiais e metadados diretos e para quando a ficha essencial está sustentada e existe caminho oficial de acesso.

### GEDI — missão/família de dados

| Campo essencial | Valor representativo |
|---|---|
| organização | NASA; distribuição de produtos científicos via NASA Earthdata/ORNL DAAC |
| nome | Global Ecosystem Dynamics Investigation (GEDI) |
| tipo amplo | source / platform |
| resumo | missão/instrumento LiDAR orbital para estrutura tridimensional da vegetação e aplicações em carbono e biodiversidade |
| escopo | observações LiDAR e produtos derivados de estrutura da vegetação e biomassa |
| modalidades | LiDAR orbital; footprints; produtos derivados em grade quando materialmente distintos |
| temas/variáveis principais | estrutura vertical, altura do dossel, métricas de waveform, densidade de biomassa acima do solo |
| cobertura espacial | faixa orbital quase global coberta pela ISS; Brasil incluído |
| cobertura temporal | aquisições desde 2019; produtos possuem períodos próprios |
| resolução quando material | footprints de aproximadamente 25 m em produtos footprint; não elevar isso a propriedade universal de todos os produtos GEDI |
| atualização | depende do produto; releases não são entidades obrigatórias |
| acesso | catálogo GEDI no ORNL DAAC / Earthdata |
| gratuidade/autenticação | dados NASA abertos; autenticação pode ser exigida para download |
| página oficial | https://science.nasa.gov/mission/gedi/ |
| metadados | https://daac.ornl.gov/cgi-bin/dataset_lister.pl?p=40/ |
| metodologia | documentação específica por produto; L4A possui user guide/ATBD |
| licença | orientação NASA Earthdata de uso de dados; não inferir licença de produto para toda a família |
| citação | por produto; `not_applicable` como citação única da entrada ampla |
| estado | partially_verified |
| data de verificação | 2026-08-07 |

**Teste de granularidade:** o catálogo GEDI contém produtos com significado científico distinto (por exemplo, métricas de estrutura e biomassa). Esses produtos podem justificar subentradas quando forem necessários para descoberta; versões/revisões de um mesmo produto não justificam entrada por si só. O produto L4A V3, por exemplo, descreve AGBD e erro de predição em footprints e fornece DOI/citação próprios, demonstrando diferença material de significado sem exigir inventário de grânulos.

### DETER Cerrado — alertas de supressão de vegetação nativa

| Campo essencial | Valor representativo |
|---|---|
| organização | Instituto Nacional de Pesquisas Espaciais (INPE) |
| nome | DETER Cerrado |
| tipo amplo | data_product / data_service |
| resumo | sistema de avisos para evidências de alteração/supressão da cobertura de vegetação nativa no Cerrado |
| escopo | monitoramento operacional para apoiar fiscalização e resposta rápida; não representa taxa anual consolidada de desmatamento |
| modalidades | alertas geoespaciais e consultas/dashboards |
| temas/variáveis principais | evidências de alteração da cobertura, classes de alerta, área, localização e tempo do aviso em nível resumido |
| cobertura espacial | bioma Cerrado |
| cobertura temporal | oferta corrente com série de avisos disponibilizada desde 2018 no download oficial |
| resolução quando material | registrar somente quando sustentada pela metodologia específica; não inferida nesta fixture |
| atualização | operacional/frequente; página de downloads registra atualização dos avisos |
| acesso | TerraBrasilis: dashboards, downloads, metadados e serviços web |
| gratuidade/autenticação | consulta pública; condições específicas podem diferir para acesso antecipado/restrito |
| página oficial | https://terrabrasilis.dpi.inpe.br/ |
| metadados | https://terrabrasilis.dpi.inpe.br/downloads/ |
| metodologia | página oficial do DETER/INPE e documentação vinculada pelo programa |
| licença | uso condicionado à licença e citação da fonte conforme orientação TerraBrasilis; não preencher texto de licença sem evidência direta |
| citação | referência oficial da plataforma/programa quando publicada; registrar lacuna se não capturada |
| estado | partially_verified |
| data de verificação | 2026-08-07 |

**Teste de granularidade:** `_curr`, `_hist`, shapefiles, serviços WFS ou outros endpoints são caminhos técnicos da mesma oferta e não viram entradas. A diferença entre DETER e PRODES é material — finalidade operacional e periodicidade distintas — e pode justificar entradas separadas.

### IBGE — fonte institucional de estatísticas e geociências

| Campo essencial | Valor representativo |
|---|---|
| organização | Instituto Brasileiro de Geografia e Estatística (IBGE) |
| nome | IBGE — estatísticas e geociências |
| tipo amplo | source |
| resumo | fonte oficial ampla de informações estatísticas e geocientíficas do Brasil |
| escopo | estatísticas econômicas, sociais e demográficas; geociências, cartografia, território e recursos naturais, entre outros domínios institucionais |
| modalidades | tabelas agregadas, microdados, bases geoespaciais, mapas, publicações e aplicações |
| temas/variáveis principais | demografia, economia, sociedade, território, cartografia, geociências e ambiente em nível de descoberta |
| cobertura espacial | Brasil, com múltiplos recortes territoriais conforme pesquisa/produto |
| cobertura temporal | varia por operação estatística e produto; não há período único correto para a fonte ampla |
| resolução quando material | `not_applicable` na entrada institucional ampla; registrar em subentrada quando material |
| atualização | varia por operação/produto; calendário e periodicidade específicos pertencem às ofertas materialmente distintas |
| acesso | portal IBGE, Downloads, SIDRA, BME, Portal de Mapas e outras plataformas oficiais |
| gratuidade/autenticação | acesso público predominante; condições específicas permanecem no sistema de origem |
| página oficial | https://www.ibge.gov.br/ |
| metadados | https://metadados.ibge.gov.br/ |
| metodologia | metadados estatísticos e documentação de cada operação/produto |
| licença | registrar apenas condição diretamente sustentada para a oferta selecionada; não generalizar de um produto para toda a instituição |
| citação | por publicação/operação/produto quando aplicável; `not_applicable` como citação única institucional |
| estado | partially_verified |
| data de verificação | 2026-08-07 |

**Teste de granularidade:** SIDRA, BME, BDiA e Portal de Mapas podem ser subentradas se sua função e forma principal de acesso forem relevantes para descoberta. Tabelas SIDRA, arquivos de download, anos e formatos permanecem fora da granularidade pública normal.

### ANA/SNIRH — sistema nacional de informações sobre recursos hídricos

| Campo essencial | Valor representativo |
|---|---|
| organização | Agência Nacional de Águas e Saneamento Básico (ANA) |
| nome | Sistema Nacional de Informações sobre Recursos Hídricos (SNIRH) |
| tipo amplo | platform |
| resumo | sistema nacional que reúne, trata, armazena, recupera e divulga informações sobre recursos hídricos e sua gestão |
| escopo | quantidade e qualidade das águas, usos, disponibilidade hídrica, eventos críticos, planejamento, regulação e gestão |
| modalidades | séries hidrológicas, dados tabulares e geoespaciais, mapas, indicadores, dados abertos e geoserviços |
| temas/variáveis principais | precipitação, níveis e vazões, reservatórios, qualidade da água, usos da água, disponibilidade e divisões hidrográficas, em nível de descoberta |
| cobertura espacial | território brasileiro, com recortes por bacia, estação e demais unidades conforme sistema/oferta |
| cobertura temporal | varia por sistema e conjunto de dados; o SNIRH declara atualização permanente das informações |
| resolução quando material | `not_applicable` para a plataforma ampla; registrar por oferta quando material |
| atualização | permanente no nível do sistema; frequências específicas pertencem aos conjuntos/sistemas correspondentes |
| acesso | Portal SNIRH, HidroWeb, mapas, portal de metadados, dados abertos e geoserviços |
| gratuidade/autenticação | ampla consulta pública; APIs ou serviços específicos podem possuir requisitos próprios |
| página oficial | https://www.snirh.gov.br/portal/snirh |
| metadados | Portal de Metadados da ANA, acessível pelo SNIRH |
| metodologia | documentação e manuais específicos dos sistemas e redes |
| licença | dados abertos quando assim identificados no portal; não herdar essa condição automaticamente para toda oferta |
| citação | por conjunto/publicação quando aplicável; registrar `not_applicable` ou `not_found` no nível amplo conforme evidência |
| estado | partially_verified |
| data de verificação | 2026-08-07 |

**Teste de granularidade:** HidroWeb, Telemetria, SAR ou um portal de geosserviços podem justificar subentradas por função/acesso materialmente distintos. Estações, layers, arquivos e endpoints individuais não são entradas do catálogo por padrão.

## 8. Crosswalk contra o núcleo mínimo

Os quatro fixtures usam somente:

- `organizations` para responsabilidade institucional;
- `catalog_entries` para a oferta pública compreensível e sua ficha essencial;
- `entry_variables` para temas/variáveis principais em nível de descoberta;
- `entry_evidence` para sustentar campos materiais e registrar `not_found`/`not_applicable` sem inferência;
- `connector_profiles` somente se um caso de uso concreto selecionar acesso automatizado.

Nenhum caso exige tabela pública para release, distribuição, ativo, arquivo, layer, banda, endpoint, observação primária, estimand ou linhagem. Nenhum campo essencial fica estruturalmente impossível de representar: campos que não possuem valor único no nível amplo são explicitamente `not_applicable`, variáveis por produto são mantidas em resumo de descoberta e lacunas documentais usam `not_found` ou `needs_review`.

## 9. Testes adversariais

O modelo deve impedir ou sinalizar:

1. criação automática de uma entrada para cada arquivo;
2. transformação de página de metadados em dataset;
3. herança de propriedades específicas para toda a fonte;
4. preenchimento de licença ou resolução por inferência;
5. conversão de endpoint genérico em conector verificado;
6. expansão do esquema baseada apenas em um caso excepcional;
7. uso de quantidade de subentradas como métrica de qualidade.

Os quatro fixtures exercitam explicitamente os itens 1, 3, 4 e 5: granularidade técnica foi mantida fora do núcleo, propriedades específicas não foram elevadas ao nível institucional, lacunas foram preservadas e nenhum endpoint foi promovido a conector.

## 10. Resultado do gate

**PASS para o desenho mínimo.** GEDI, DETER Cerrado, IBGE e ANA/SNIRH podem ser representados pela unidade `catalog_entry` e pelo núcleo-alvo sem proliferação de tabelas, inventário integral ou perda do significado necessário à descoberta e ao encaminhamento do usuário.

Este `PASS` valida **a suficiência estrutural do modelo**, não declara as quatro fichas como registros públicos prontos para produção. Antes de publicação de cada entrada, seus campos devem seguir o workflow normal de curadoria e evidência proporcional. A validação também não autoriza promoção de schema, publicação de Pages ou criação de conectores.

## 11. Evidência oficial consultada na revalidação

- NASA Science — GEDI: https://science.nasa.gov/mission/gedi/
- ORNL DAAC — catálogo GEDI: https://daac.ornl.gov/cgi-bin/dataset_lister.pl?p=40/
- ORNL DAAC — GEDI L4A Footprint Level Aboveground Biomass Density, Version 3: https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=2508
- INPE — DETER: https://www.gov.br/inpe/pt-br/area-conhecimento/unidade-amazonia/projetos-e-pesquisas/deter
- TerraBrasilis — plataforma e acesso: https://terrabrasilis.dpi.inpe.br/
- TerraBrasilis — downloads: https://terrabrasilis.dpi.inpe.br/downloads/
- IBGE — portal e plataformas: https://www.ibge.gov.br/
- IBGE — metadados: https://metadados.ibge.gov.br/
- ANA — Sistema Nacional de Informações sobre Recursos Hídricos: https://www.gov.br/ana/pt-br/assuntos/gestao-das-aguas/politica-nacional-de-recursos-hidricos/sistema-de-informacoes-sobre-recursos-hidricos
- SNIRH — portal: https://www.snirh.gov.br/portal/snirh
- ANA — acesso aos sistemas: https://www.gov.br/ana/pt-br/servicos/acesso-a-sistemas/acesso-aos-sistemas
