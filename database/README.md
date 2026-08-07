# Banco relacional da Instância 1

Este diretório contém o staging, o modelo profundo incorporado no Marco 1 e a futura migração para o núcleo mínimo da Instância 1.

## 1. Estado arquitetural

### Autoridade pública transitória

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`;
- artefatos JSON derivados usados pelo site atual.

### Staging preservado

O schema `staging` importa os CSVs sem reinterpretá-los e registra lotes, hashes, contagens e ocorrências.

### Modelo profundo do Marco 1

`schema/001_instance1_core.sql` continua executável e preservado. Ele demonstra integridade referencial, idempotência e separação de entidades, mas passa a ser classificado como **legado técnico/extensão futura**, não como requisito universal da Instância 1.

### Núcleo mínimo proposto

A arquitetura de destino passa a ser:

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles opcional
```

A implementação deve ser aditiva e não destrutiva.

## 2. Banco-alvo

- PostgreSQL 16 ou superior;
- PostGIS 3 ou superior;
- `pg_trgm` quando necessário para busca textual;
- Python 3.11 ou superior para cargas e validações.

O banco armazena metadados do catálogo. Não copia integralmente datasets externos.

## 3. Arquivos atuais

### Schemas

- `schema/001_instance1_core.sql` — modelo profundo do Marco 1, preservado;
- `schema/002_legacy_staging.sql` — staging sem perda;
- `schema/003_staging_batches.sql` — lotes e hashes.

### Mapeamentos e promoção piloto

Os arquivos em `mappings/` e `scripts/promote_instance1_pilot.py` permanecem como evidência da resolução inicial. Eles não definem que toda fonte deva ser decomposta em família, produto, release, distribuição ou ativo.

### Validação

- `scripts/load_instance1_staging.py`;
- `scripts/validate_instance1_database.py`;
- validadores do piloto e da estrutura profunda permanecem disponíveis para regressão.

## 4. Próxima migration

O próximo pacote executável deverá criar, sem remover tabelas atuais:

- `catalog.catalog_entries`;
- `catalog.entry_variables`;
- `catalog.entry_evidence`;
- `catalog.connector_profiles`.

O plano detalhado está em:

`docs/roadmap/INSTANCE_1_MINIMUM_SCHEMA_MIGRATION_PLAN.md`.

## 5. Crosswalk

| Estrutura atual | Tratamento no núcleo mínimo |
|---|---|
| organizações | preservar |
| fontes | converter em entradas `source` ou `platform` |
| famílias | criar entrada somente quando úteis ao usuário |
| produtos | converter quando materialmente distintos |
| releases | metadado adicional ou extensão excepcional |
| variáveis | importar somente variáveis principais |
| assertions | agregar em evidências proporcionais |
| distribuições | converter em links essenciais ou conector selecionado |
| ativos | não promover automaticamente |
| capacidades | resumir no acesso ou usar em conector selecionado |
| métodos e perfis | campos simples/JSONB, salvo necessidade repetida |

## 6. Regras de migração

- preservar todas as linhas originais;
- registrar IDs de origem;
- manter carga e promoção idempotentes;
- não sobrescrever curadoria manual silenciosamente;
- registrar conflitos;
- não criar entrada por arquivo, layer, banda ou endpoint;
- não converter toda distribuição em conector;
- manter desconhecidos como desconhecidos;
- permitir restauração do estado anterior.

## 7. Execução local atual

```bash
docker compose -f database/compose.yml up -d
python3 -m pip install -r database/requirements.txt
python3 scripts/load_instance1_staging.py --initialize
python3 scripts/promote_instance1_pilot.py
python3 scripts/validate_instance1_database.py
python3 scripts/validate_instance1_pilot.py
```

A conexão padrão de desenvolvimento é:

```text
postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog
```

A senha é exclusivamente local e não deve ser usada em produção.

## 8. Comando destrutivo

O comando abaixo remove o volume local:

```bash
docker compose -f database/compose.yml down -v
```

Deve ser usado apenas quando a perda do banco de desenvolvimento local for intencional. Não é etapa normal de validação.

## 9. Staging e lotes

As tabelas de staging preservam:

- arquivos de origem;
- hashes SHA-256;
- contagens;
- SHA do repositório;
- versão do carregador;
- horários;
- estado da carga;
- ocorrências.

Uma segunda execução com os mesmos hashes deve ser `no_op`.

## 10. Promoção piloto anterior

A promoção anterior de fontes, famílias, produtos, releases, distribuições e capacidades continua como teste do modelo profundo. Ela não representa a cobertura final do catálogo e não deve ser expandida até que a decisão de granularidade mínima seja incorporada.

## 11. Testes do núcleo mínimo

O futuro pacote deve testar:

- banco vazio e banco pós-Marco 1;
- idempotência;
- integridade referencial;
- preservação de IDs;
- ausência de duplicatas;
- exportação determinística;
- rollback/restauração;
- GEDI, DETER Cerrado, IBGE e ANA/SNIRH;
- caso adversarial contra criação de entrada por arquivo ou layer.

## 12. Integração contínua

O CI atual valida documentação, CSVs, interface, staging e modelo profundo. Durante a transição, ele deverá ganhar validações do núcleo mínimo sem remover prematuramente as regressões existentes.

CI verde comprova que os contratos executáveis passaram; não comprova fatos externos nem autoriza promoção ou merge.

## 13. Autoridade

O PostgreSQL/PostGIS somente substituirá os CSVs após:

- migration aditiva validada;
- crosswalk auditado;
- casos dourados aprovados;
- exportação reproduzível;
- CI verde;
- revisão concluída;
- autorização humana explícita.
