# Metodologia de curadoria

## 1. Escopo vigente

O foco ativo é a **Instância 1 — Catálogo relacional científico-operacional**.

A unidade de trabalho deixa de ser apenas a fonte e passa a incluir o **produto científico georreferenciado**, suas versões, variáveis, métodos, perfis espaciais e temporais, qualidade, distribuições e evidências.

Os CSVs atuais permanecem públicos durante a migração, mas o modelo de destino é PostgreSQL/PostGIS.

## 2. Unidades de registro

### Fonte

Portal, repositório, catálogo, plataforma, rede, programa, observatório ou infraestrutura.

### Produto

Conjunto coerente e versionado de informações espaciais, com significado científico, método, cobertura, suporte, variáveis e formas de acesso identificáveis.

### Release

Versão, coleção, edição, cenário ou ano-base.

### Distribuição

Forma de acesso ao release.

### Ativo

Arquivo, endpoint, camada, coleção, tabela, legenda, metadado ou recurso concreto.

### Variável

Propriedade, indicador, banda, classe, métrica, atributo ou flag com significado próprio.

## 3. Regra de escopo geográfico

São incluídos produtos que possuam:

- coordenadas;
- geometrias;
- pixels ou grades;
- pontos, footprints ou trajetórias;
- bacias, biomas ou unidades de conservação;
- códigos territoriais;
- séries por município, estado ou outra unidade geográfica.

Uma tabela territorial pode ser georreferenciável mesmo quando distribuída em CSV ou XLSX.

## 4. Evidências

A curadoria prioriza:

1. página oficial do produto;
2. documentação oficial;
3. metadados do release;
4. metodologia técnica;
5. licença e termos;
6. documentação de API ou serviço;
7. artigos revisados por pares que descrevem ou validam o produto;
8. relatórios técnicos institucionais.

Cada evidência sustenta apenas as afirmações que efetivamente contém.

Exemplos:

- homepage comprova identidade, não necessariamente resolução;
- página de download comprova disponibilidade, não necessariamente licença;
- artigo de aplicação não substitui documentação oficial do produto;
- resolução de visualização não comprova resolução científica;
- data de atualização do portal não define a periodicidade do dado.

Afirmações importantes são registradas em `metadata_assertions`.

## 5. Identificação do objeto

Antes de preencher qualquer perfil, deve-se resolver:

1. quem é o produtor primário;
2. qual é a fonte de acesso;
3. se o objeto é família, produto, versão, distribuição ou serviço;
4. se possui informação geográfica;
5. se a enumeração será completa, por família, seletiva ou por índice externo.

Catálogos, APIs genéricas, visualizadores e serviços de processamento não devem ser classificados como produtos científicos.

## 6. Significado científico

Todo produto deve conter:

- `scientific_object` — objeto ou fenômeno central;
- `information_message` — informação sobre o mundo real que o produto comunica;
- `non_representations` — interpretações que não são sustentadas diretamente;
- variáveis e classes;
- usos potenciais;
- limitações.

A mensagem informacional deve ser objetiva e proporcional à documentação.

Exemplo:

```text
Produto: alerta de alteração da cobertura
Mensagem: localização, data de detecção e classe atribuída a uma evidência observada.
Não representa: taxa anual consolidada, data exata do evento ou causalidade da mudança.
```

## 7. Natureza de produção

O produto ou variável deve ser classificado como:

- observação primária;
- registro administrativo;
- censo;
- levantamento amostral;
- estimativa amostral;
- classificação;
- modelagem;
- interpolação;
- agregação;
- índice composto;
- produto derivado;
- método misto;
- desconhecido.

A classificação deve ser acompanhada de descrição do método, dados de entrada, processamento, validação e versão.

## 8. Perfil espacial

Registrar:

- tipo de suporte;
- geometria;
- resolução nominal e unidade;
- escala, quando aplicável;
- unidade mínima mapeável;
- CRS;
- grade;
- agregação;
- unidade geográfica;
- extensão;
- vieses e limitações espaciais.

Resolução, escala, suporte e unidade territorial não devem ser concatenados em um único campo no banco relacional.

## 9. Perfil temporal

Registrar:

- cobertura inicial e final;
- instante, evento, intervalo ou agregado;
- resolução temporal;
- janela de observação;
- frequência de atualização;
- latência;
- calendário;
- forma de agregação;
- vieses e limitações temporais.

## 10. Qualidade, incerteza e viés

Registrar, quando disponível:

- desenho de validação;
- acurácia;
- incerteza;
- erro;
- probabilidades;
- flags;
- dados ausentes;
- NoData;
- cobertura de nuvens;
- viés amostral;
- detectabilidade;
- erro de classificação;
- artefatos;
- representatividade.

`desconhecido` não deve ser convertido em `ausente`.

## 11. Acesso operacional

Separar:

- página institucional;
- página do produto;
- acesso aos dados;
- metodologia;
- documentação da API;
- licença;
- citação;
- visualizador;
- código.

Registrar:

- formato;
- media type;
- protocolo;
- ferramenta;
- gratuidade;
- autenticação;
- quotas;
- recorte;
- consulta;
- visualização;
- download;
- processamento;
- exportação;
- estado atual do endpoint.

A existência de API não implica acesso sem autenticação, processamento gratuito ou visualização direta.

## 12. Taxonomias e filtros

Os temas podem incluir múltiplos domínios:

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
- carbono;
- uso da terra;
- demografia;
- economia;
- governança;
- infraestrutura.

A busca pública deve usar filtros e linguagem comum. Sintaxe booleana não é requisito de interface.

## 13. Estratégia de enumeração

- `complete` — portfólio relevante enumerado;
- `family_level` — famílias enumeradas, aprofundamento progressivo;
- `external_index` — catálogo integral permanece externo;
- `representative_sample` — piloto explicitamente incompleto;
- `selective` — produtos escolhidos por relevância e cobertura do Brasil.

A estratégia deve ser declarada para evitar falsa impressão de completude.

## 14. Migração

1. importar CSVs para `staging` sem transformação destrutiva;
2. registrar hash e data;
3. resolver entidade;
4. registrar problemas;
5. normalizar IDs e valores;
6. criar releases;
7. migrar distribuições;
8. aprofundar perfis;
9. auditar;
10. promover registros aprovados.

Nenhum problema bloqueante pode permanecer aberto na promoção.

## 15. Auditoria

A auditoria avalia:

- completude;
- precisão científica;
- precisão operacional;
- coerência;
- evidência;
- separação das entidades;
- atualização;
- clareza pública.

“Verificado” significa confrontado com as evidências registradas na data indicada. Não garante disponibilidade futura nem certifica integralmente a fonte.

## 16. Instâncias futuras

### Instância 2

Composição geográfica, transparência comparativa e executabilidade técnica.

### Instância 3

Síntese científica breve e auditável sobre fenômenos escolhidos pelo usuário.

Essas instâncias permanecem fora do escopo ativo. A metodologia atual deve apenas manter os metadados necessários para que sejam possíveis no futuro.

Consulte:

- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`;
- `database/schema/001_instance1_core.sql`;
- `PRODUCT_CATALOG_MODEL.md`;
- `docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md`.
