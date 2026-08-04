# Banco relacional da Instância 1

Este diretório contém a implementação de referência do núcleo relacional científico-operacional do catálogo.

## Banco-alvo

- PostgreSQL 16 ou superior;
- PostGIS 3 ou superior;
- `pg_trgm` para busca textual aproximada.

O banco armazena **metadados, significado científico, versões, acesso, evidências e curadoria**. Ele não pretende copiar integralmente os datasets externos.

## Arquivos

- `schema/001_instance1_core.sql` — criação do esquema normalizado `catalog` e das tabelas centrais;
- `schema/002_legacy_staging.sql` — área de importação sem perda dos CSVs públicos atuais e registro de problemas de migração.

## Entidades centrais

```text
organizations
  └── sources
        └── product_families
              └── products
                    └── product_releases
                          ├── product_variables
                          └── distributions
                                ├── data_assets
                                └── access_capabilities
```

Entidades científicas transversais:

- `variables`;
- `methods`;
- `spatial_profiles`;
- `temporal_profiles`;
- `quality_profiles`;
- `taxonomy_terms`;
- `citations`;
- `metadata_assertions`;
- `curation_reviews`.

## Por que PostgreSQL/PostGIS

O catálogo precisa de:

- integridade referencial;
- versionamento explícito;
- busca por texto e filtros estruturados;
- relações muitos-para-muitos;
- rastreabilidade de evidências;
- cobertura geográfica consultável;
- futura API;
- suporte às expansões geográficas sem armazenar todos os dados externos.

PostGIS é usado principalmente para metadados espaciais, como a extensão geográfica do produto. A ingestão de grandes rasters, vetores ou séries externas não é requisito da Instância 1.

## Execução local de referência

```bash
createdb science_data_catalog
psql science_data_catalog -f database/schema/001_instance1_core.sql
psql science_data_catalog -f database/schema/002_legacy_staging.sql
```

Em ambientes conteinerizados, deve-se usar uma imagem PostgreSQL com PostGIS.

## Staging e promoção

O schema `staging` recebe os CSVs sem reinterpretá-los. Todos os valores permanecem textuais até que sejam resolvidos e validados.

As tabelas são:

- `staging.legacy_resources`;
- `staging.legacy_products`;
- `staging.legacy_distributions`;
- `staging.migration_issues`.

O campo `resolved_entity_type` permite registrar se uma linha antiga corresponde realmente a:

- produto;
- família;
- fonte;
- distribuição;
- capacidade de acesso;
- objeto ainda desconhecido.

Nenhum registro deve ser promovido ao schema `catalog` enquanto houver problema bloqueante aberto.

## Estratégia de migração

1. preservar os CSVs atuais;
2. importar CSVs para `staging`;
3. registrar hash e data de carregamento;
4. separar fonte, produto, versão, distribuição e serviço;
5. criar releases explícitos;
6. mapear as colunas atuais para as tabelas relacionais;
7. enriquecer produtos com perfis científicos;
8. validar chaves, evidências e completude;
9. promover registros aprovados;
10. gerar CSVs e planilhas a partir do banco.

## Regras de modelagem

- infraestrutura não é produto científico;
- uma distribuição pertence a uma versão do produto;
- uma variável deve preservar o nome original no produto;
- a definição canônica da variável não substitui a definição fornecida pelo produtor;
- resolução deve ser associada ao suporte que descreve;
- incerteza desconhecida não equivale a incerteza ausente;
- texto livre complementa, mas não substitui valores controlados;
- afirmações importantes devem possuir evidência em `metadata_assertions`;
- registros incompletos permanecem em estado de curadoria.

## Autoridade durante a transição

Enquanto a migração não cumprir o Portão D definido em `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`, os CSVs públicos atuais permanecem canônicos para a versão publicada. O SQL representa a arquitetura canônica de destino.
