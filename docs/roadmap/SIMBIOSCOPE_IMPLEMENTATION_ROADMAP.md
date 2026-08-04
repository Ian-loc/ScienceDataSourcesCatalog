# Roadmap de implementação do Symbiotrama

**Status:** roadmap vigente  
**Foco ativo:** Instância 1 — Catálogo relacional científico-operacional  
**Instâncias 2 e 3:** registradas apenas como expansões futuras

## 1. Objetivo

Transformar o catálogo atual, ainda majoritariamente tabular e superficial, em um banco relacional aprofundado de produtos de dados georreferenciados sobre o Brasil.

A Instância 1 deve tornar explícitos:

- o objeto científico de cada produto;
- a informação que ele representa;
- as variáveis e classes contidas;
- a natureza observacional ou derivada;
- os perfis espacial e temporal;
- o método;
- a qualidade, a incerteza e os vieses;
- as versões;
- as distribuições e capacidades de acesso;
- as evidências que sustentam os metadados.

## 2. Regras de execução

1. Aprofundar antes de expandir funcionalidades.
2. Produto científico, infraestrutura e serviço devem permanecer separados.
3. Nenhuma migração destrutiva dos CSVs atuais durante a transição.
4. O PostgreSQL/PostGIS é a arquitetura canônica de destino.
5. CSVs e planilhas passarão a ser exportações após o portão de promoção.
6. Toda afirmação material deve possuir evidência rastreável.
7. Valores desconhecidos não devem ser inferidos.
8. Instâncias 2 e 3 não devem orientar trabalho ativo antes da consolidação da Instância 1.
9. A página pública atual permanece estável enquanto a base é reconstruída.
10. A curadoria segue prioridade Brasil primeiro.

## Fase I1.0 — consolidação normativa e relacional

### Entregas

- decisão formal de foco na Instância 1;
- definição canônica de fonte, família, produto, release, distribuição, ativo e variável;
- documento científico-operacional da Instância 1;
- esquema PostgreSQL/PostGIS versionado;
- estratégia de transição dos CSVs;
- workflow de curadoria;
- Instâncias 2 e 3 registradas como somente leitura conceitual.

### Portão de saída

- documentação harmonizada;
- esquema relacional executável;
- nenhuma ambiguidade normativa entre produto e infraestrutura;
- autoridade durante a transição definida.

## Fase I1.1 — staging e migração do piloto atual

### Objetivo

Migrar e reclassificar os registros atuais sem perda de informação.

### Entregas

- tabelas de staging para `data_resources.csv`, `data_products.csv` e `product_distributions.csv`;
- mapeamento de colunas;
- normalização de IDs;
- criação de releases explícitos;
- migração de distribuições para releases;
- separação dos registros que são catálogos, serviços e infraestruturas;
- relatório de inconsistências;
- testes de integridade referencial.

### Correções obrigatórias do piloto

- serviços interoperáveis TerraBrasilis não permanecem como produto científico;
- Earth Engine Public Data Catalog não permanece como produto científico;
- Publisher Catalogs não permanecem como produto científico;
- Earth Engine Processing and Export Service não permanece como produto científico;
- produtos por bioma e versão recebem escopo explícito;
- produtos experimentais preservam status e versão.

### Portão de saída

- todos os registros atuais resolvidos por entidade;
- nenhuma distribuição órfã;
- nenhuma versão implícita quando a documentação permite identificá-la;
- relatório de migração aprovado.

## Fase I1.2 — perfis científicos piloto

### Objetivo

Demonstrar o nível de profundidade exigido pelo novo catálogo.

### Famílias piloto

1. PRODES;
2. DETER;
3. TerraClass;
4. MapBiomas Cobertura e Uso da Terra;
5. Dynamic World;
6. produto municipal de saúde;
7. produto municipal socioeconômico;
8. produto de água ou clima.

### Entregas por produto

- objeto científico;
- mensagem informacional;
- não-representações;
- variáveis e classes;
- método;
- suporte espacial e temporal;
- qualidade e incerteza;
- versões;
- distribuições e capacidades;
- citação e licença;
- evidências por campo;
- revisão curatorial.

### Portão de saída

- perfis completos e auditados em múltiplos domínios;
- linguagem científica consistente;
- filtros básicos demonstráveis;
- lacunas do esquema identificadas e corrigidas.

## Fase I1.3 — expansão de fontes prioritárias

### Prioridade inicial

1. MapBiomas;
2. TerraBrasilis / INPE;
3. IBGE;
4. ANA / SNIRH;
5. DATASUS;
6. INMET;
7. Embrapa;
8. ICMBio e MMA;
9. fontes internacionais com cobertura sistemática do Brasil.

### Estratégias de enumeração

- `complete`;
- `family_level`;
- `external_index`;
- `representative_sample`;
- `selective`.

### Portão de saída

- fontes prioritárias com estratégia definida;
- produtos relevantes enumerados;
- equilíbrio entre ecologia, ambiente, saúde, sociedade e território;
- progresso medido por produtos aprovados, não apenas por linhas adicionadas.

## Fase I1.4 — taxonomias, busca e interface

### Objetivo

Substituir a página simplificada por uma interface sustentada pelos dados relacionais.

### Entregas

- filtros temáticos;
- filtros por variável e objeto observado;
- filtros espaciais e temporais;
- filtros de método e qualidade;
- filtros de acesso;
- perfil público do produto;
- perfil de release;
- lista de distribuições e capacidades;
- evidências e data de revisão;
- busca textual em português e termos alternativos;
- exportação de resultados.

### Portão de saída

- interface não depende de campos agregados ambíguos;
- usuário consegue distinguir fonte, produto, versão e acesso;
- produto informa claramente o que representa e não representa;
- filtros são derivados de valores estruturados.

## Fase I1.5 — promoção do banco relacional

### Objetivo

Tornar o PostgreSQL/PostGIS a fonte canônica.

### Entregas

- pipeline de importação e validação;
- pipeline de exportação para CSV e planilha;
- API ou camada de leitura;
- backups e migrações;
- controle de versões do esquema;
- testes automáticos;
- documentação operacional;
- espelho do Drive regenerado a partir do banco.

### Portão de saída

- banco relacional canônico;
- CSVs reproduzíveis;
- planilhas derivadas;
- página pública sincronizada;
- integridade e evidências validadas automaticamente.

## 3. Workstreams permanentes da Instância 1

### Curadoria científica

- significado do produto;
- variáveis;
- método;
- qualidade;
- limitações;
- literatura descritiva e de validação.

### Curadoria operacional

- URLs;
- formatos;
- APIs;
- serviços;
- autenticação;
- licenças;
- testes de acesso.

### Arquitetura de dados

- normalização;
- migrações;
- IDs;
- chaves;
- taxonomias;
- importação e exportação.

### Qualidade

- auditoria por lote;
- evidência por campo;
- detecção de duplicidade;
- separação de entidades;
- revisão de versões;
- monitoramento de endpoints.

### Experiência do usuário

- linguagem acessível;
- comparação de perfis;
- filtros claros;
- explicitação de desconhecidos;
- acesso direto à fonte autoritativa.

## 4. Instância 2 — backlog de longo prazo

A composição geográfica poderá incluir:

- camadas resolvidas;
- mapas sobrepostos ou sincronizados;
- perfis territoriais;
- verificação de executabilidade;
- transparência de escalas e métodos;
- processamento seletivo.

Não iniciar implementação ampla antes do Portão I1.5.

O explorador existente pode permanecer como protótipo, sem ser tratado como núcleo consolidado nem receber funções analíticas novas.

## 5. Instância 3 — backlog de longo prazo

A contextualização científica poderá incluir:

- recuperação de literatura por fenômeno, território, escala e período;
- sínteses breves e auditáveis;
- referências visíveis;
- mecanismos e controvérsias;
- distinção entre evidência direta e análoga;
- comunicação proporcional à evidência.

Não iniciar implementação antes de a Instância 1 fornecer perfis científicos consistentes e a Instância 2 possuir composições bem definidas.

## 6. Primeira sequência executável

1. consolidar a Fase I1.0;
2. criar staging dos CSVs atuais;
3. migrar e reclassificar o piloto;
4. preencher oito perfis científicos piloto;
5. auditar o esquema;
6. aprofundar MapBiomas e TerraBrasilis;
7. incorporar IBGE, ANA e DATASUS;
8. construir filtros sobre dados relacionais;
9. gerar nova interface de produtos;
10. promover o banco após validação.

## 7. Critério de sucesso

O sucesso será medido pela capacidade de responder:

- o que o produto representa;
- qual variável está disponível;
- como foi produzida;
- qual é o suporte espacial e temporal;
- qual versão está em uso;
- quais limitações e incertezas existem;
- como acessar;
- qual evidência sustenta o registro.

O número bruto de fontes, produtos ou camadas não é suficiente como métrica de qualidade.
