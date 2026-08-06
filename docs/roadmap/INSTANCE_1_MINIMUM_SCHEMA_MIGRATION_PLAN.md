# Plano de migração para o núcleo mínimo da Instância 1

**Status:** proposta executável após incorporação do PR de direção  
**Princípio:** migração sem perda, idempotente e reversível.

## 1. Objetivo

Migrar progressivamente a arquitetura incorporada no Marco 1 para um núcleo centrado em entradas de catálogo, sem apagar staging, evidências ou estruturas profundas antes de sua disposição formal.

## 2. Estrutura-alvo

- `catalog.organizations`;
- `catalog.catalog_entries`;
- `catalog.entry_variables`;
- `catalog.entry_evidence`;
- `catalog.connector_profiles` opcional.

## 3. Estratégia

### Fase A — extensão aditiva

Criar novas tabelas por migration aditiva. Não remover ou renomear tabelas existentes.

### Fase B — crosswalk

Mapear registros existentes:

| Estrutura atual | Destino proposto |
|---|---|
| `organizations` | `organizations` preservada ou adaptada |
| `sources` | `catalog_entries` com `entry_type = source/platform` |
| `product_families` | entrada apenas quando útil; caso contrário, metadado ou relação histórica |
| `products` | `catalog_entries` quando forem unidades públicas materialmente distintas |
| `product_releases` | metadado adicional, subentrada excepcional ou extensão histórica |
| `variables` / `product_variables` | `entry_variables`, limitadas às variáveis principais |
| `metadata_assertions` | `entry_evidence`, agregada proporcionalmente |
| `distributions` | links essenciais da entrada ou candidato a conector |
| `data_assets` | não promovido ao núcleo; preservado como legado histórico |
| `access_capabilities` | resumo de acesso ou `connector_profiles` quando selecionado |
| métodos e perfis | campos simples/JSONB, salvo uso repetido comprovado |

## 4. Regras de transformação

1. nenhuma linha original é apagada;
2. cada entrada derivada preserva IDs de origem em `source_record_ids`;
3. a mesma carga não cria duplicatas;
4. alterações manuais posteriores não são sobrescritas silenciosamente;
5. conflitos são registrados para revisão;
6. relações profundas não são convertidas em novas entradas sem decisão de granularidade;
7. links são classificados por papel, sem inventário integral;
8. valores desconhecidos permanecem desconhecidos.

## 5. Tabela `catalog_entries`

Campos iniciais propostos:

- `entry_id`;
- `stable_id`;
- `organization_id`;
- `parent_entry_id` opcional;
- `entry_type`;
- `official_name`;
- `acronym`;
- `summary`;
- `scientific_scope`;
- `data_modalities`;
- `geographic_coverage_text`;
- `temporal_coverage_text`;
- `spatial_resolution_text`;
- `temporal_resolution_text`;
- `update_frequency_text`;
- `access_level`;
- `authentication_required`;
- `official_page_url`;
- `metadata_url`;
- `primary_access_url`;
- `methodology_url`;
- `license_text`;
- `license_url`;
- `citation_text`;
- `citation_url`;
- `curation_status`;
- `last_verified_at`;
- `additional_metadata` JSONB;
- `source_record_ids` JSONB;
- timestamps.

## 6. Variáveis

`entry_variables` deve armazenar somente conteúdos úteis para busca:

- `source_label`;
- `source_definition`;
- `search_label` opcional;
- `variable_group`;
- `unit_text` opcional;
- `evidence_id` opcional;
- estado curatorial.

Não importar automaticamente cada banda, classe ou coluna do modelo profundo.

## 7. Evidências

`entry_evidence` pode sustentar um campo ou grupo de campos:

- URL;
- papel da evidência;
- nota de suporte;
- data de recuperação;
- estado de verificação.

Não migrar afirmações atômicas sem avaliar sua utilidade no perfil público.

## 8. Conectores

`connector_profiles` só recebe candidatos selecionados. Distribuições e ativos existentes não são convertidos automaticamente em conectores.

## 9. Compatibilidade transitória

Durante a migração:

- CSV/JSON públicos permanecem inalterados;
- views podem expor o novo núcleo sem substituir o site;
- scripts antigos continuam disponíveis para regressão;
- o novo exportador deve ser testado lado a lado;
- nenhuma promoção a produção ocorre sem autorização.

## 10. Testes obrigatórios

- migration aplicada em banco vazio;
- migration aplicada após Marco 1;
- idempotência da carga;
- integridade de FKs;
- ausência de duplicação de entradas;
- preservação de IDs de origem;
- rollback ou restauração documentada;
- exportação determinística;
- casos GEDI, DETER Cerrado, IBGE e ANA/SNIRH;
- teste adversarial contra criação de entrada por arquivo/layer.

## 11. Critério de saída

O pacote executável será aceito quando:

- o núcleo mínimo estiver materializado;
- nenhum dado legado tiver sido removido;
- os quatro casos forem representáveis;
- o exportador produzir fichas úteis;
- o CI estiver verde;
- revisão não identificar expansão indevida;
- houver autorização humana para merge.
