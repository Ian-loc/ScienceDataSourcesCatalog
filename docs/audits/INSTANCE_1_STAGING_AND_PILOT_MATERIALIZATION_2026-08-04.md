# Auditoria da materialização do staging e do piloto da Instância 1

**Executado em:** 04/08/2026, horário de São Paulo  
**Repositório:** `Ian-loc/ScienceDataSourcesCatalog`  
**Branch:** `agent/consolidate-instance-1-relational-catalog`  
**PR:** #54  
**Estado de autoridade:** proposta em branch; não incorporada à `main`

## 1. Objetivo

Comprovar que a arquitetura relacional da Instância 1 pode ser executada de modo reproduzível e que os CSVs atuais podem ser carregados sem perda, resolvidos por tipo de entidade e parcialmente promovidos para o esquema normalizado sem confundir produtos científicos, fontes, famílias e capacidades de acesso.

## 2. Intervenções executadas

Foram adicionados:

- ambiente PostgreSQL/PostGIS reproduzível em `database/compose.yml`;
- dependência Python em `database/requirements.txt`;
- migration `003_staging_batches.sql`;
- carregador `scripts/load_instance1_staging.py`;
- validador `scripts/validate_instance1_database.py`;
- mapeamento integral das 11 linhas piloto em `pilot_entity_resolution.csv`;
- mapeamentos separados de fontes, famílias e produtos;
- promotor normalizado `scripts/promote_instance1_pilot.py`;
- validador do piloto `scripts/validate_instance1_pilot.py`;
- job dedicado `instance1-database` no GitHub Actions.

## 3. Carga sem perda

O carregador validou e inseriu no staging:

| Arquivo | Registros |
|---|---:|
| `data/data_resources.csv` | 51 |
| `data/data_products.csv` | 11 |
| `data/product_distributions.csv` | 19 |

Foram verificados:

- cabeçalhos completos e na ordem esperada;
- IDs não vazios;
- ausência de IDs duplicados;
- todos os `resource_id` dos produtos existentes;
- todos os `product_id` das distribuições existentes;
- hashes SHA-256 dos três arquivos;
- preservação textual dos valores legados.

A repetição com os mesmos hashes foi reconhecida como `no_op`, sem duplicação ou substituição silenciosa do lote anterior.

## 4. Resolução de entidade

As 11 linhas da tabela piloto de produtos foram reclassificadas:

| Tipo real | Quantidade | Registros |
|---|---:|---|
| Produto científico específico | 2 | TerraClass Amazônia 2020; Dynamic World V1 |
| Família de produtos | 5 | PRODES; DETER Amazônia; DETER Cerrado; DETER Pantanal; vegetação secundária por bioma |
| Fonte ou catálogo agregador | 2 | Earth Engine Public Data Catalog; Earth Engine Publisher Data Catalogs |
| Capacidade de acesso/processamento | 2 | serviços interoperáveis TerraBrasilis; processamento e exportação Earth Engine |

Essa resolução impede que serviços OGC, megacatálogos e infraestrutura computacional sejam promovidos como produtos científicos.

## 5. Promoção normalizada

Foram promovidos ao schema `catalog`:

- 2 fontes;
- 5 famílias de produtos;
- 2 produtos científicos;
- 2 releases;
- 5 distribuições;
- 17 capacidades operacionais de acesso;
- 6 afirmações iniciais de metadados científicos;
- 2 revisões curatoriais em estado `in_progress`.

### Produtos promovidos

#### TerraClass Amazônia 2020

Foi registrado como produto classificado específico, com release 2020 e declaração explícita de:

- objeto científico;
- mensagem informacional;
- usos potenciais;
- fenômenos que não são diretamente representados;
- distribuição de download.

#### Dynamic World V1

Foi registrado como produto classificado específico, com release V1 e declaração explícita de:

- probabilidades de classes e classe principal por pixel;
- natureza derivada de imagens Sentinel-2;
- usos exploratórios potenciais;
- não equivalência entre classe principal e verdade territorial direta;
- distribuições separadas para API/ImageCollection, catálogo, visualizador e código/modelo.

## 6. Objetos deliberadamente não promovidos como produtos

Os seguintes IDs permaneceram fora de `catalog.products`:

- `DP000007` — serviços interoperáveis TerraBrasilis;
- `DP000008` — Earth Engine Public Data Catalog;
- `DP000009` — Earth Engine Publisher Data Catalogs;
- `DP000010` — Earth Engine Processing and Export Service.

Sua ausência da tabela de produtos é um resultado esperado e obrigatório do modelo.

## 7. Idempotência

Foram executadas duas formas de repetição:

1. nova carga dos mesmos CSVs;
2. nova promoção do mesmo piloto.

Resultados:

- a segunda carga retornou `no_op`;
- a segunda promoção manteve as mesmas contagens;
- não foram duplicadas fontes, famílias, produtos, releases, distribuições, capacidades, afirmações ou revisões.

## 8. Validação automatizada

A execução #216 do workflow **Validar e publicar catálogo** foi concluída com sucesso.

### Job `validate`

Aprovou:

- documentação e direção científica;
- scripts Python;
- estrutura e relações dos CSVs;
- interface pública;
- geração do artefato estático;
- exclusão do diretório `database` do site publicado.

### Job `instance1-database`

Aprovou:

- inicialização do container PostGIS;
- instalação do cliente PostgreSQL;
- aplicação das migrations 001–003;
- carga completa do staging;
- idempotência da carga;
- promoção do piloto;
- idempotência da promoção;
- integridade do staging;
- integridade do catálogo normalizado.

## 9. Limites e pendências

O piloto normalizado ainda não possui profundidade suficiente para promoção canônica.

Permanecem pendentes:

- variáveis, bandas e classes detalhadas;
- métodos versionados;
- perfis espaciais e temporais;
- qualidade, incerteza, validação e vieses;
- taxonomias;
- citações estruturadas;
- evidências de alta confiança por campo;
- teste dos endpoints e formas de acesso;
- auditoria científica integral de TerraClass e Dynamic World;
- enumeração de produtos MapBiomas;
- promoção controlada das demais fontes e famílias.

## 10. Decisão de estado

**Resultado técnico:** PASS.  
**Banco em produção:** não.  
**Fonte canônica alterada:** não.  
**Página pública alterada:** não.  
**Merge autorizado:** não solicitado nesta auditoria.

O PostgreSQL/PostGIS permanece como arquitetura canônica de destino e artefato executável da branch. Os CSVs da `main` permanecem como autoridade material publicada até conclusão dos perfis científicos, auditoria do piloto, autorização humana e merge.

## 11. Próxima ação

A próxima unidade de trabalho é aprofundar os dois produtos promovidos, iniciando por:

1. variáveis e classes;
2. método;
3. suporte espacial e temporal;
4. qualidade, incerteza e limitações;
5. evidências oficiais e científicas por campo;
6. teste das cinco distribuições;
7. auditoria final do perfil de cada produto.

Em paralelo, deve-se iniciar a enumeração relacional dos produtos MapBiomas, sem tratá-lo como um único produto homogêneo.
