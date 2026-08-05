# Auditoria — metadados GeoNetwork específicos do PRODES

**Data e horário:** 2026-08-05 07:21:41 America/Sao_Paulo  
**Round:** Instância 1 — PRODES, metadados específicos  
**PR:** #54  
**Branch:** `agent/consolidate-instance-1-relational-catalog`

## Objetivo

Substituir a dependência da página agregadora de downloads por identificadores específicos e verificáveis do catálogo oficial GeoNetwork, sem promover prematuramente ativos, distribuições ou releases.

## Resultado material

Foi criado `database/mappings/prodes_geonetwork_metadata_registry_2026.json` com seis UUIDs específicos do PRODES Amazônia:

- incremento anual no desmatamento;
- incremento anual entre 1 e 6,25 ha;
- máscara acumulada de supressão;
- resíduo anual;
- hidrografia;
- não floresta.

Os registros permanecem em estado pré-promoção. URLs diretas de download, checksums, CRS, geometrias, esquema de campos, licença, citação e identificadores de release continuam nulos ou explicitamente pendentes.

## Decisão arquitetural

O GeoPackage agregado não é tratado como um único objeto científico homogêneo. Ele é uma embalagem operacional que reúne componentes com identidades e metadados próprios. O UUID do GeoNetwork identifica o registro de metadado e não deve ser convertido em `release_id`, checksum ou identificador do ativo.

## Auditoria de qualidade

Verificações executadas no contrato e no validador:

- vínculo exclusivo com `PF000001`;
- seis UUIDs únicos e sintaticamente válidos;
- URLs HTTPS em domínio oficial do INPE;
- correspondência entre UUID declarado e URL do registro;
- distinção entre incremento principal e distribuição complementar de pequenos polígonos;
- ativos mantidos como `not_downloaded`;
- ausência de URLs diretas, checksums e releases inventados;
- pendências obrigatórias de CRS, geometria, licença, citação e release;
- promoção mantida como não autorizada.

## Ocorrência

### I1-20260805-018

- **Severidade:** `high`
- **Estado:** `corrected`
- **Categoria:** identidade de metadado, distribuição e ativo
- **Entidades afetadas:** família PRODES; GeoPackage e Shapefiles PRODES Amazônia
- **Descrição:** a etapa anterior conhecia famílias de distribuição, mas ainda não possuía identificadores específicos de metadados. Isso criava risco de usar a página agregadora comprometida como origem operacional ou de tratar o GeoPackage como objeto científico indivisível.
- **Evidência:** registros oficiais do TerraBrasilis GeoNetwork com UUIDs próprios para incremento anual, pequenos polígonos, máscara acumulada, resíduo, hidrografia e não floresta.
- **Correção aplicada:** registro legível por máquina, validador dedicado e integração à cadeia de validação PRODES.
- **Teste de verificação:** `python3 scripts/validate_prodes_geonetwork_metadata_registry.py`, chamado por `scripts/validate_prodes_operational_evidence.py`.
- **Risco residual:** endpoints diretos e bytes dos ativos ainda não foram recuperados; CRS, esquema, checksums, licença, citação e release continuam bloqueados.

## Próxima unidade

1. obter links de distribuição associados a cada UUID por API ou registro específico;
2. verificar resposta HTTP, redirecionamentos e tipo de conteúdo;
3. recuperar um ativo de tamanho manejável;
4. calcular SHA-256 dos bytes;
5. inspecionar CRS, geometrias, campos e domínios;
6. manter o GeoPackage agregado de aproximadamente 820 MB para etapa posterior com capacidade apropriada.
