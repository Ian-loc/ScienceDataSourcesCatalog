# DEC — Núcleo simplificado e granularidade mínima suficiente da Instância 1

**Status:** proposta canônica para incorporação  
**Data:** 2026-08-06  
**Fuso:** `America/Sao_Paulo`

## Decisão

A Instância 1 do Simbiotrama será um **catálogo relacional de fontes e ofertas de dados científicos**, não uma reprodução interna dos catálogos, genealogias, releases, arquivos, layers, bandas ou endpoints mantidos por terceiros.

A entidade pública central será `catalog_entry`. Uma entrada representa o menor objeto que seja simultaneamente útil para descoberta, compreensível para o usuário e sustentável para curadoria. Ela pode corresponder a uma fonte, plataforma, coleção, produto de dados ou serviço, conforme a granularidade usada pela própria fonte e a utilidade para o catálogo.

## Arquitetura-alvo

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles  [opcional]
```

O núcleo pode ser implementado em PostgreSQL. PostGIS é opcional para metadados de cobertura e não implica ingestão dos dados externos.

## Regra de granularidade

Criar uma nova entrada somente quando houver diferença material em pelo menos um destes aspectos:

- significado científico;
- modalidade ou conjunto temático principal;
- cobertura geográfica;
- cobertura temporal;
- método;
- público ou finalidade;
- forma principal de acesso;
- identidade oficial claramente separada pela fonte.

Não criar uma nova entrada apenas porque existe outro:

- arquivo;
- formato;
- layer;
- banda;
- diretório;
- endpoint;
- tabela;
- atualização técnica;
- nome interno de download.

## Metadados mínimos

Cada entrada deve registrar, quando aplicável e disponível:

- organização responsável;
- nome oficial e sigla;
- tipo amplo da entrada;
- resumo e escopo científico;
- modalidades de dados;
- variáveis ou grupos de variáveis;
- cobertura espacial e temporal;
- resolução ou suporte quando material;
- frequência de atualização;
- acesso, gratuidade e autenticação;
- página oficial;
- página de metadados;
- página principal de acesso;
- metodologia;
- licença;
- citação;
- estado e data de verificação.

Nomes e definições do produtor devem ser preservados. Normalização serve à descoberta e aos filtros, não à substituição da terminologia original.

## Dados externos e custódia

Todos os dados e objetos acessíveis permanecem externos. O Simbiotrama:

- não copia datasets de terceiros;
- não mantém arquivos externos como acervo;
- não promete preservação dos bytes;
- não cria inventário integral de ativos;
- não assume autoria, hospedagem ou custódia;
- registra links e metadados diretos fornecidos pela fonte.

Downloads temporários para validação técnica não constituem acervo e devem ser descartados após a verificação.

## Instância 2

A Instância 2 será uma camada federada de visualização e consulta por APIs e outros conectores. `connector_profiles` registrará apenas a configuração externa necessária para operações selecionadas. A Instância 2 não exige que a Instância 1 tenha enumerado todos os arquivos ou layers da fonte.

## Consequências

- `product_families`, `product_releases`, `distributions`, `data_assets` e `access_capabilities` deixam de ser requisitos canônicos da Instância 1.
- O esquema relacional profundo incorporado no Marco 1 passa a ser `LEGACY_TRANSITIONAL`: preservado como evidência e fonte de componentes reutilizáveis, mas não ampliado como arquitetura-alvo.
- O PR #57 deve permanecer congelado e não ser mesclado; sua curadoria pode ser reutilizada seletivamente como evidência, sem transportar a arquitetura excessivamente profunda.
- O próximo pacote executável deve implementar o núcleo simplificado e demonstrá-lo com casos heterogêneos.

## Casos de validação

O modelo deve representar, sem proliferação de entidades:

1. GEDI — plataforma/coleção LiDAR com múltiplos produtos internos;
2. DETER Cerrado — oferta operacional de alertas;
3. IBGE — fonte de dados territoriais, estatísticos e tabulares;
4. ANA/SNIRH — plataforma hidrológica com páginas, arquivos, séries e serviços.

O modelo falha se exigir inventário integral, reconstrução de genealogia externa ou grande número de campos vazios para esses casos.
