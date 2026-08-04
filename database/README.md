# Banco relacional da Instância 1

Este diretório contém a implementação de referência do núcleo relacional científico-operacional do catálogo.

## Banco-alvo

- PostgreSQL 16 ou superior;
- PostGIS 3 ou superior;
- `pg_trgm` para busca textual aproximada;
- Python 3.11 ou superior para os carregadores e validadores.

O banco armazena **metadados, significado científico, versões, acesso, evidências e curadoria**. Ele não pretende copiar integralmente os datasets externos.

## Arquivos

### Esquema

- `schema/001_instance1_core.sql` — esquema normalizado `catalog` e tabelas centrais;
- `schema/002_legacy_staging.sql` — importação sem perda dos CSVs atuais;
- `schema/003_staging_batches.sql` — lotes imutáveis, hashes, histórico e views do último lote bem-sucedido.

### Mapeamentos do piloto

- `mappings/pilot_entity_resolution.csv` — decide se cada linha antiga é produto, família, fonte ou capacidade de acesso;
- `mappings/pilot_sources.csv` — tipos e estratégias de enumeração das fontes piloto;
- `mappings/pilot_families.csv` — famílias científicas reconhecidas;
- `mappings/pilot_products.csv` — significado científico mínimo e releases dos produtos específicos promovidos.

### Execução

- `compose.yml` — PostgreSQL/PostGIS local reproduzível;
- `requirements.txt` — dependência Python do cliente PostgreSQL;
- `../scripts/load_instance1_staging.py` — valida e carrega os três CSVs em lote;
- `../scripts/promote_instance1_pilot.py` — promove apenas entidades já resolvidas;
- `../scripts/validate_instance1_database.py` — valida integridade do staging;
- `../scripts/validate_instance1_pilot.py` — valida o piloto no esquema normalizado.

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

## Execução local reproduzível

```bash
docker compose -f database/compose.yml up -d
python3 -m pip install -r database/requirements.txt
python3 scripts/load_instance1_staging.py --initialize
python3 scripts/promote_instance1_pilot.py
python3 scripts/validate_instance1_database.py
python3 scripts/validate_instance1_pilot.py
```

A conexão local padrão é:

```text
postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog
```

A senha acima existe somente para desenvolvimento local. Produção deverá usar segredo próprio e nunca versionado.

Para recriar o banco local desde o início:

```bash
docker compose -f database/compose.yml down -v
docker compose -f database/compose.yml up -d
```

## Carga sem banco

A estrutura dos CSVs, as chaves e o mapeamento de entidades podem ser validados sem PostgreSQL:

```bash
python3 scripts/load_instance1_staging.py --check-only
```

O comando informa:

- número de linhas;
- hashes SHA-256;
- chaves órfãs;
- cobertura do mapeamento;
- distribuição das decisões de entidade.

## Staging e lotes

O schema `staging` recebe os CSVs sem reinterpretá-los. Todos os valores permanecem textuais até que sejam resolvidos e validados.

As tabelas principais são:

- `staging.load_batches`;
- `staging.legacy_resources`;
- `staging.legacy_products`;
- `staging.legacy_distributions`;
- `staging.migration_issues`.

Cada carga registra:

- arquivos de origem;
- hashes SHA-256;
- número de linhas;
- SHA do repositório, quando disponível;
- versão do carregador;
- horário de início e conclusão;
- estado da carga.

Uma segunda execução com os mesmos três hashes é um `no_op`. A carga não duplica registros e não substitui silenciosamente lotes anteriores.

As views `v_latest_resources`, `v_latest_products` e `v_latest_distributions` expõem somente o último lote bem-sucedido.

## Resolução de entidade

O campo `resolved_entity_type` registra se uma linha antiga corresponde realmente a:

- produto;
- família;
- fonte;
- distribuição;
- capacidade de acesso;
- objeto ainda desconhecido.

A resolução atual do piloto é:

| Tipo resolvido | Quantidade |
|---|---:|
| Produto científico específico | 2 |
| Família de produtos | 5 |
| Fonte ou catálogo agregador | 2 |
| Capacidade de acesso/processamento | 2 |

Assim, serviços OGC, o catálogo público do Earth Engine e o serviço de processamento do Earth Engine não são promovidos como produtos científicos.

## Promoção piloto

A promoção inicial é intencionalmente limitada.

### Fontes promovidas

- `DR0011` — TerraBrasilis;
- `DR0019` — Google Earth Engine Data Catalog.

### Famílias promovidas

- PRODES;
- DETER Amazônia;
- DETER Cerrado;
- DETER Pantanal;
- Vegetação secundária por bioma.

### Produtos promovidos

- `DP000005` — TerraClass Amazônia 2020;
- `DP000011` — Dynamic World V1.

### Distribuições promovidas

- `DD000006` — TerraClass 2020, download;
- `DD000016` — Dynamic World, ImageCollection/API;
- `DD000017` — Dynamic World, registro de catálogo;
- `DD000018` — Dynamic World, visualizador;
- `DD000019` — Dynamic World, código e modelo.

O script registra ainda capacidades operacionais, revisões curatoriais em andamento e afirmações científicas iniciais com evidência e confiança explícitas.

## O que a promoção ainda não significa

O piloto normalizado ainda não está completo. Em especial, faltam:

- variáveis e classes detalhadas;
- métodos versionados;
- perfis espaciais;
- perfis temporais;
- qualidade, incerteza e validação;
- taxonomias aprofundadas;
- citações completas;
- evidências de alta confiança por campo;
- auditoria final de cada produto.

Por isso, os produtos permanecem com revisão `in_progress`, e o banco ainda não substitui os CSVs públicos.

## Estratégia de migração

1. preservar os CSVs atuais;
2. importar os CSVs para `staging`;
3. registrar lote, hashes e integridade;
4. resolver fonte, produto, versão, distribuição e serviço;
5. promover somente entidades suficientemente definidas;
6. criar releases explícitos;
7. enriquecer produtos com perfis científicos;
8. validar chaves, evidências e completude;
9. auditar o lote piloto;
10. somente então promover o banco a fonte canônica;
11. gerar CSVs e planilhas a partir do banco.

## Regras de modelagem

- infraestrutura não é produto científico;
- uma distribuição pertence a uma versão do produto;
- uma variável deve preservar o nome original no produto;
- a definição canônica da variável não substitui a definição fornecida pelo produtor;
- resolução deve ser associada ao suporte que descreve;
- incerteza desconhecida não equivale a incerteza ausente;
- texto livre complementa, mas não substitui valores controlados;
- afirmações importantes devem possuir evidência em `metadata_assertions`;
- registros incompletos permanecem em estado de curadoria;
- promoção e carga devem ser idempotentes;
- nenhuma linha é promovida apenas porque existia no CSV anterior.

## Integração contínua

O workflow do GitHub Actions executa dois grupos independentes:

1. validação documental, dos CSVs e da interface pública;
2. criação efêmera de um PostGIS, aplicação das migrações, carga, repetição idempotente, promoção do piloto e validação relacional.

O banco usado pelo CI é descartado ao final. Isso comprova reprodutibilidade, mas não equivale a provisionamento de produção.

## Autoridade durante a transição

Enquanto a migração não cumprir o Portão D definido em `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`, os CSVs públicos atuais permanecem canônicos para a versão publicada. O SQL representa a arquitetura canônica de destino, e o piloto normalizado permanece um artefato de migração auditável.
