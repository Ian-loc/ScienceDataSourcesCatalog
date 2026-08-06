# Banco relacional da Instância 1 — estado de transição

## Estado

O diretório `database/` contém a implementação profunda incorporada no Marco 1. Após a revisão de escopo de 6 de agosto de 2026, essa implementação passa a ser classificada como:

```text
LEGACY_TRANSITIONAL
```

Ela permanece preservada para:

- staging sem perda;
- hashes e lotes;
- idempotência;
- integridade referencial;
- evidências históricas;
- reaproveitamento seletivo de componentes.

Ela não é mais a arquitetura-alvo da Instância 1.

## Nova arquitetura-alvo

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles  [opcional]
```

O próximo pacote executável deverá criar um novo esquema ou migração simplificada, sem modificar silenciosamente `001_instance1_core.sql`.

## O que não deve continuar sendo ampliado

Até decisão arquitetural contrária formal, não ampliar como requisitos canônicos:

- `product_families`;
- `product_releases`;
- `distributions`;
- `data_assets`;
- `access_capabilities`;
- perfis espaciais, temporais, metodológicos e de qualidade como entidades obrigatórias;
- inventários de arquivos, layers, bandas ou endpoints;
- guards específicos por ativo externo.

## Dados externos

A Instância 1 não hospeda datasets de terceiros. Arquivos, layers, tabelas, coleções e endpoints permanecem nas fontes originais.

O banco deverá armazenar somente:

- entradas de catálogo;
- metadados essenciais;
- variáveis ou grupos de variáveis;
- evidências;
- links oficiais;
- conectores externos selecionados.

## Banco-alvo

- PostgreSQL 16 ou superior;
- PostGIS 3 ou superior somente quando necessário para metadados de cobertura;
- Python 3.11 ou superior para migração e validação.

PostGIS não implica ingestão de rasters ou vetores externos.

## Componentes preservados

### Staging

Os scripts e schemas de staging permanecem úteis para:

- carregar os CSVs atuais sem perda;
- registrar hashes;
- manter lotes imutáveis;
- detectar IDs órfãos;
- produzir manifestos;
- validar reexecução idempotente.

### Promoção piloto antiga

`promote_instance1_pilot.py` e os mapeamentos associados pertencem ao modelo profundo. Não devem ser usados como promoção canônica do novo núcleo.

### Esquema `001_instance1_core.sql`

É evidência executável do Marco 1. Não deve ser tratado como contrato atual da Instância 1 nem receber novos produtos profundamente normalizados.

## Próxima implementação

O pacote I1-R1 deverá:

1. criar o núcleo simplificado;
2. importar organizações e entradas;
3. migrar variáveis amplas e evidências;
4. condensar links de produtos e distribuições antigas;
5. preservar valores desconhecidos;
6. evitar inventário de ativos;
7. executar carga repetida sem duplicação;
8. gerar uma projeção JSON para o website;
9. manter a página atual sem alteração até autorização.

## Casos de validação

A implementação deverá representar:

- GEDI;
- DETER Cerrado;
- IBGE;
- ANA/SNIRH.

O teste falha se algum caso exigir reconstrução integral da plataforma ou criação de entidades específicas para cada arquivo ou layer.

## Execução do legado

Os comandos abaixo continuam disponíveis apenas para regressão do Marco 1:

```bash
python3 scripts/load_instance1_staging.py --check-only
python3 scripts/validate_instance1_database.py
python3 scripts/validate_instance1_pilot.py
```

Não executar promoção do piloto como etapa do novo catálogo sem revisão explícita.

O comando `docker compose down -v` remove volumes locais e é destrutivo para o banco de desenvolvimento. Não deve ser executado automaticamente.

## Autoridade

- CSV/JSON atuais: autoridade pública transitória;
- esquema profundo: `LEGACY_TRANSITIONAL`;
- decisão e política de escopo: direção canônica proposta;
- novo esquema simplificado: próximo pacote;
- PostgreSQL simplificado: autoridade futura somente após gate humano.
