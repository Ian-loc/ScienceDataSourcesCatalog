# Auditoria — contrato operacional do Dynamic World V1

**Data e horário:** 2026-08-05 12:25 America/Sao_Paulo  
**PR:** #54  
**Branch:** `agent/consolidate-instance-1-relational-catalog`

## Objetivo

Fechar o portão documental e operacional do Dynamic World V1 sem confundir catálogo web, asset científico, visualizador, registro secundário e software de inferência, e sem promover prematuramente o produto para aprovação curatorial.

## Resultado material

Foi criado `database/mappings/dynamic_world_operational_contract_2026.json`, vinculado a `DP000011` e `PR000011`, com:

- asset canônico `GOOGLE/DYNAMICWORLD/V1`;
- tipo `Earth Engine ImageCollection`;
- data inicial de 27/06/2015 e atualização contínua;
- dez bandas e duas propriedades de versionamento do algoritmo;
- requisitos de autenticação e acesso via Earth Engine;
- capacidades de recorte espacial, temporal, por banda e probabilidade;
- licença CC BY 4.0, atribuição obrigatória e aviso upstream do Sentinel;
- DOI do artigo descritor;
- separação explícita das quatro distribuições legadas;
- restrições de interpretação e requisitos antes de aprovação curatorial.

O estado operacional do pipeline de ingestão do asset foi verificado como `OK` na página oficial de status do Earth Engine. Esse estado é uma observação datada e não uma garantia permanente de disponibilidade.

## Decisões científicas e operacionais

1. O identificador do asset é armazenado separadamente da URL da página de catálogo.
2. A ImageCollection não é descrita como arquivo de download direto.
3. A data final exibida dinamicamente no catálogo não é promovida como término científico do produto; o release é continuamente atualizado.
4. O registro WRI é metadado secundário, não hospedagem dos rasters.
5. O explorador visual não substitui acesso analítico reproduzível.
6. Código e modelos mantêm licença de software separada da licença do dataset.
7. O rótulo top-1 não é tratado como verdade de campo nem como probabilidade universal de correção.
8. Composições temporais e mapas finais exigem regras explícitas do usuário.

## Auditoria de delta

Foi criado `scripts/validate_dynamic_world_operational_contract.py`, integrado ao job `validate` do workflow principal. O validador exige:

- IDs estáveis corretos;
- promoção desautorizada;
- asset e tipo corretos;
- URLs HTTPS;
- status observado `OK`;
- data inicial, pixel, bandas e propriedades completas;
- autenticação e ausência de download direto;
- restrições científicas mínimas;
- licença, atribuição, aviso Sentinel e DOI;
- exatamente quatro distribuições com papéis distintos;
- portão pré-aprovação completo;
- quatro categorias de evidência.

O validador também foi incluído no caminho de geração pública para impedir que uma futura execução em `main` ignore o contrato. Nenhum dado do contrato é copiado para `_site` pela mudança atual.

## Evidências

- catálogo oficial do Earth Engine para o Dynamic World V1;
- página oficial de status de ingestão do Earth Engine;
- documentação oficial do projeto Dynamic World;
- artigo descritor revisado por pares.

## Ocorrências

Nenhuma nova não conformidade material foi identificada na auditoria de delta antes da execução do CI. A aprovação do pacote permanece condicionada ao workflow verde no SHA final.

## Estado curatorial

`in_progress`.

O contrato fecha a documentação operacional, mas não autoriza sozinho a aprovação curatorial. Ainda é necessário comprovar, no banco normalizado, que os quatro papéis de distribuição, o asset, a licença, a atribuição, o DOI e as condições de acesso foram materializados sem perda semântica.

## Próxima unidade

1. verificar o workflow no SHA final;
2. confrontar o contrato com as linhas normalizadas de `distributions`, `data_assets` e `access_capabilities`;
3. corrigir qualquer divergência por enriquecimento idempotente;
4. executar novamente o validador integral do piloto;
5. avançar em paralelo para inspeção direta do ativo TerraClass se nenhuma divergência estrutural for encontrada.
