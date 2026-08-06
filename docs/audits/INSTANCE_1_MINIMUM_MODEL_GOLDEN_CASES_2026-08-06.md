# Casos de validação do modelo mínimo da Instância 1

**Data:** 6 de agosto de 2026  
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

- uma entrada de catálogo para a missão ou coleção GEDI;
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

Um identificador de coleção específico pode ser registrado somente quando a Instância 2 selecionar uma visualização.

### Resultado esperado

`PASS` se uma ficha única ou poucas subentradas materialmente distintas forem suficientes.

## 3. Caso B — DETER Cerrado

### Representação proposta

- uma entrada para o sistema de alertas DETER Cerrado;
- INPE/TerraBrasilis como organização/fonte relacionadas;
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

`PASS` se o conteúdo útil do PR #57 puder ser condensado em uma ficha curta com evidências proporcionais.

## 4. Caso C — IBGE

### Representação proposta

- entrada ampla para o IBGE ou para plataformas oficiais materialmente distintas;
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

- entrada para a infraestrutura principal e subentradas apenas para sistemas ou coleções materialmente distintas;
- modalidades como séries hidrológicas, dados tabulares, vetores e serviços;
- cobertura, atualização e acesso em nível geral;
- links oficiais para dados e documentação.

### Não requerido

- entrada para cada shapefile, planilha ou PDF;
- inventário de todas as bacias e layers;
- modelagem de cada formato como distribuição ou ativo;
- download e inspeção de cada pacote.

### Conector futuro

Serviço ou API selecionado pode ganhar `connector_profile` quando houver caso de visualização.

### Resultado esperado

`PASS` se formatos diferentes puderem ser descritos como parte da oferta sem virar entidades públicas obrigatórias.

## 6. Matriz de avaliação

| Critério | GEDI | DETER Cerrado | IBGE | ANA/SNIRH |
|---|---:|---:|---:|---:|
| entrada compreensível | requerido | requerido | requerido | requerido |
| variáveis/temas principais | requerido | requerido | requerido | requerido |
| cobertura e período | requerido | requerido | requerido | requerido |
| links oficiais | requerido | requerido | requerido | requerido |
| inventário integral | proibido | proibido | proibido | proibido |
| release obrigatória | não | não | não | não |
| ativo obrigatório | não | não | não | não |
| conector | opcional | opcional | opcional | opcional |
| metadados adicionais JSONB | permitido | permitido | permitido | permitido |

## 7. Testes adversariais

O modelo deve impedir ou sinalizar:

1. criação automática de uma entrada para cada arquivo;
2. transformação de página de metadados em dataset;
3. herança de propriedades específicas para toda a fonte;
4. preenchimento de licença ou resolução por inferência;
5. conversão de endpoint genérico em conector verificado;
6. expansão do esquema baseada apenas em um caso excepcional;
7. uso de quantidade de subentradas como métrica de qualidade.

## 8. Conclusão preliminar

Os quatro casos são representáveis pelo núcleo mínimo proposto. A próxima validação deve materializar exemplos estruturados e executar o crosswalk contra os registros atuais, sem pesquisa forense adicional.
