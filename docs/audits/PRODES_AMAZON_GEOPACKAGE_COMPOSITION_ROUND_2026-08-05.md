# Auditoria da composição do GeoPackage PRODES Amazônia — 2026-08-05

## Escopo

Esta rodada verifica apenas a composição declarada do registro oficial **GeoPackage - PRODES Amazônia** no catálogo GeoNetwork/TerraBrasilis. Não recupera o arquivo, não valida bytes e não autoriza promoção de distribuição ou ativo.

Horário de referência: 2026-08-05 15:24:52, `America/Sao_Paulo`.

## Evidência oficial consultada

- Catálogo GeoNetwork/TerraBrasilis: `https://terrabrasilis.dpi.inpe.br/geonetwork/srv/search?any=2025&fast=index`.
- Registro exibido: **GeoPackage - PRODES Amazônia**.
- Formato declarado: GeoPackage.
- Tipo de representação declarado: vetorial.
- Tamanho aproximado declarado: `~820MB`.
- Frequência de atualização apresentada pelo catálogo: anual.
- Ano do registro observado no índice: 2026.

O registro oficial declara que o pacote agrega dez componentes, cada qual apontando para um UUID de metadado próprio:

1. máscara acumulada de supressão da vegetação nativa;
2. máscara acumulada de supressão em não floresta;
3. incremento anual no desmatamento;
4. incremento de supressão em não floresta;
5. incremento anual entre 1 e 6,25 ha;
6. resíduo anual da supressão da vegetação nativa;
7. resíduo anual da supressão em não floresta;
8. hidrografia;
9. hidrografia em não floresta;
10. não floresta.

## Decisão de modelagem

O GeoPackage deve ser tratado como **distribuição agregada** do alvo cartográfico PRODES Amazônia, e não como substituto semântico dos conjuntos de dados componentes. Os UUIDs componentes preservam identidades de metadado independentes.

A evidência permite registrar:

- existência do registro de pacote no catálogo;
- formato e natureza vetorial declarados;
- composição declarada;
- tamanho apenas aproximado;
- frequência anual apenas como propriedade apresentada pelo registro de catálogo.

A evidência não permite registrar como verificados:

- URL direta estável;
- tamanho exato em bytes;
- checksum;
- nome efetivo do arquivo;
- tabelas ou camadas internas;
- CRS e tipos de geometria;
- esquema e semântica dos atributos;
- integridade entre o pacote e os dez registros componentes;
- identificador de release;
- política de substituição/versionamento;
- licença e citação específicas do ativo recuperado.

## Artefatos produzidos

- `database/mappings/prodes_amazon_geopackage_composition_guard_2026.json`;
- `scripts/validate_prodes_amazon_geopackage_composition_guard.py`;
- integração do novo gate em `scripts/validate_prodes_product_targets.py`.

## Estado

`catalog_package_composition_verified`, com `promotion_authorized=false` e `asset_inspected=false`.

## Próxima ação

Resolver a URL direta do pacote ou de um ativo componente, registrar redirecionamentos e recuperar os bytes somente quando houver endpoint oficial tecnicamente acessível. Depois, calcular tamanho e checksum, inspecionar estrutura interna e reconciliar o ativo com produto, release, distribuição e metadados componentes.
