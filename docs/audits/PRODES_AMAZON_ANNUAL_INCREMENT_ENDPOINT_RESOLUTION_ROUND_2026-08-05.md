# Auditoria de resolução do endpoint — incremento anual PRODES Amazônia

**Data:** 2026-08-05  
**Fuso:** America/Sao_Paulo  
**Família:** `PF000001`  
**Produto-alvo:** `PD-PRODES-AMZ-ANNUAL-MAP`  
**Ativo-alvo:** `PRODES-ASSET-ANNUAL-INCREMENT-SHP`  
**UUID de metadado:** `b75b83db-8026-43f9-9537-ee1dfa308158`

## Objetivo

Resolver, sem inferência ou adivinhação, a URL direta do Shapefile de incremento anual no desmatamento da Amazônia e determinar se o ativo já poderia avançar de `unresolved / not_inspected` para um estado operacional verificado.

## Evidência oficial confirmada

O catálogo de downloads do TerraBrasilis lista a distribuição **“Incremento anual no desmatamento - Shapefile (desde 2008)”**. O registro agregado **“GeoPackage - PRODES Amazônia”** associa o componente de incremento anual ao UUID `b75b83db-8026-43f9-9537-ee1dfa308158`.

Essas evidências confirmam:

- existência catalogada da distribuição;
- formato declarado como Shapefile;
- relação do componente com a família PRODES Amazônia;
- identidade do registro de metadados.

Elas não confirmam, por si só:

- URL direta vigente;
- estabilidade do endpoint;
- identidade ou versão dos bytes;
- checksum;
- conteúdo do pacote;
- release científica aplicável.

## Tentativas de resolução

### Rota de API do GeoNetwork

Foi consultada a rota oficial baseada no UUID:

`https://terrabrasilis.dpi.inpe.br/geonetwork/srv/api/records/b75b83db-8026-43f9-9537-ee1dfa308158`

A tentativa retornou **HTTP 500 Internal Server Error** no cliente de recuperação utilizado nesta rodada.

Esse resultado é uma observação operacional datada. Ele não prova que o registro foi removido, que o ativo está indisponível permanentemente ou que outra URL possa ser construída por padrão presumido.

### Interface de metadados

A interface pública de metadados permanece identificável pelo UUID, mas o conteúdo recuperado não forneceu uma URL direta verificável para o pacote Shapefile.

### Catálogo de downloads

A página oficial confirma a distribuição e oferece uma ação de download na interface. Entretanto, a representação recuperada da página não expôs o destino como URL estável e legível por máquina. A marca de disponibilidade no catálogo agregado não é suficiente para promover `endpoint_state`.

## Decisão curatorial

Estado mantido:

```text
metadata_state = verified_metadata_identifier
endpoint_state = unresolved
asset_state = not_inspected
promotion_authorized = false
```

Não foram preenchidos:

- `direct_download_url`;
- cadeia de redirecionamentos;
- status HTTP do arquivo;
- nome e tamanho exatos;
- checksum;
- CRS;
- geometria;
- esquema de atributos;
- release.

## Ocorrência

| Campo | Valor |
|---|---|
| ID | `I1-20260805-029` |
| Categoria | resolução de endpoint externo |
| Severidade | `medium` |
| Estado | `accepted_limitation` |
| Evidência | catálogo oficial, UUID oficial e tentativa da rota de API |
| Correção | criação de contrato e validador que impedem inferência ou promoção prematura |
| Risco residual | o ativo pode continuar acessível por mecanismo dinâmico não exposto ao cliente atual |

## Requisitos para a próxima promoção

Antes de resolver o endpoint, é necessário obter de fonte oficial verificável:

1. URL direta do ativo;
2. status HTTP e cadeia de redirecionamentos;
3. `Content-Type` e `Content-Disposition`;
4. nome e tamanho exatos;
5. vínculo inequívoco entre URL, UUID e componente anual;
6. política de autenticação, se houver.

Antes de promover o ativo, ainda serão necessários recuperação autorizada dos bytes, checksum, inventário do pacote, CRS, geometria, atributos, cobertura, licença, citação e relação explícita com produto e release.

## Conclusão

A unidade avançou de “endpoint ainda não tentado” para **“endpoint investigado e bloqueio operacional documentado”**. O bloqueio é externo e localizado; não afeta o restante do catálogo nem autoriza relaxar os gates científicos e técnicos.
