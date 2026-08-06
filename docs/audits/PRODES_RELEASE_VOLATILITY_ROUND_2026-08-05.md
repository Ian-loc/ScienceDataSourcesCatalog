# Auditoria PRODES — volatilidade operacional de distribuições

**Data/hora:** 05/08/2026 09:21 BRT  
**Escopo:** Instância 1; família `PF000001`; PR #54.  
**Autoridade preservada:** `main` permanece publicada; nenhuma promoção canônica, merge ou alteração da página pública foi realizada.

## Estado de entrada

O workflow #270 foi aprovado integralmente no SHA `6074ab9293cb963a0a71251c9414b672e74dbed7`. O inventário GeoNetwork com dez componentes PRODES Amazônia está, portanto, validado pelo CI.

## Evidência observada

A página oficial de downloads do TerraBrasilis, observada em 05/08/2026, exibe datas de atualização distintas para distribuições da mesma família operacional. No recorte Amazônia, os vetores de incremento, pequenos polígonos e o GeoPackage aparecem com atualização em 20/07/2026, enquanto o GeoTIFF completo aparece com atualização em 07/04/2026.

O catálogo GeoNetwork também informa que mosaicos Brasil e recortes por bioma podem receber atualizações em calendários independentes. Essas informações demonstram volatilidade por distribuição e impedem atribuir, por inferência, uma versão única a todos os ativos PRODES.

## Decisão de modelagem

A data exibida no catálogo é tratada como observação operacional da distribuição, não como `release_id`, versão científica ou comprovação de equivalência entre arquivos. Produto, release, distribuição e ativo permanecerão entidades distintas.

Foi criado `database/mappings/prodes_release_volatility_guard_2026.json` com quatro distribuições observadas e promoção bloqueada. O contrato exige URL direta, bytes recuperados, SHA-256, relação explícita produto–release–distribuição–ativo, política de atualização, licença e citação antes de qualquer promoção.

Foi criado `scripts/validate_prodes_release_volatility_guard.py` e integrado à cadeia `scripts/validate_prodes_operational_evidence.py`.

## Auditoria do próprio round

Verificações executadas por inspeção do diff lógico:

- família vinculada exclusivamente a `PF000001`;
- fonte classificada como `download_catalog`;
- quatro papéis operacionais preservados;
- datas distintas mantidas;
- identidade de release e ativo direto permanecem não resolvidas;
- promoção permanece desautorizada;
- nenhuma URL direta, checksum, licença ou citação foi inventada;
- calendário da Amazônia não foi generalizado para Brasil ou outros biomas.

## Ocorrência

`I1-20260805-020` — **high / corrected**: risco de transformar a data mutável exibida no catálogo em versão comum da família ou de supor sincronização entre distribuições e recortes territoriais.

A ocorrência só poderá ser marcada `closed` após CI integralmente verde no SHA final deste round.

## Risco residual e próxima unidade

Continuam pendentes URLs diretas específicas, respostas HTTP, bytes, checksums, esquema, CRS, geometrias, licença, citação e política formal de substituição. A próxima unidade deve resolver um registro GeoNetwork individual e selecionar um ativo manejável para inspeção material, sem depender da página agregadora como fonte automática.
