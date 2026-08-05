# Auditoria de integridade do catálogo PRODES — 05/08/2026

Horário de referência: `05/08/2026 06:25 BRT` (`America/Sao_Paulo`).

## Escopo

Inspeção do entrypoint público `https://terrabrasilis.dpi.inpe.br/downloads/` antes de resolver URLs diretas, metadados e ativos PRODES.

## Ocorrência I1-20260805-017

- **Round:** 13
- **Entidade/arquivo afetado:** catálogo público de downloads do TerraBrasilis; `database/mappings/prodes_catalog_integrity_guard_2026.json`
- **Categoria:** integridade e confiança de endpoint
- **Severidade:** `high`
- **Estado:** `accepted_limitation`
- **Descrição:** o HTML público do catálogo exibiu conteúdo externo não relacionado aos dados científicos e um link para o domínio não oficial `dentoxol.com`. A coexistência desse conteúdo com rótulos válidos do catálogo impede usar a página como fonte automática confiável de URLs diretas, licença, citação, release ou metadados críticos.
- **Evidência:** inspeção direta do HTML público em 05/08/2026; o conteúdo externo aparece entre o título `Downloads` e o menu de produtos.
- **Correção aplicada:** criado portão legível por máquina que define `integrity_state=suspended_for_automatic_extraction`, bloqueia extração automática e exige resolução independente por registro no GeoNetwork e por camada/serviço oficial específico. O validador foi integrado à cadeia PRODES já executada pelo CI.
- **Teste de verificação:** `scripts/validate_prodes_catalog_integrity_guard.py`, chamado por `scripts/validate_prodes_operational_evidence.py`.
- **Risco residual:** a página pode continuar exibindo rótulos operacionais válidos junto a conteúdo comprometido. Ela pode ser usada apenas para confirmação visual limitada de categorias, nunca para preencher automaticamente endpoints ou metadados de promoção.

## Controles instalados

1. Não seguir ou registrar domínios externos não oficiais encontrados no HTML.
2. Não derivar URL direta, licença, citação, checksum ou release da página afetada.
3. Resolver metadados por identificador próprio no GeoNetwork oficial.
4. Resolver camadas ou serviços por endpoint oficial específico.
5. Manter `endpoint_state=unresolved` e `asset_state=not_inspected` até inspeção direta.
6. Calcular checksum apenas sobre bytes recuperados de endpoint verificado.

## Continuidade não bloqueante

A ocorrência bloqueia somente a colheita automática a partir da página agregadora. A curadoria pode continuar com segurança usando:

- GeoNetwork oficial do TerraBrasilis;
- índice oficial de geosserviços;
- documentação técnica e científica do INPE;
- inspeção direta de cada resposta, redirecionamento, metadado e ativo.

## Efeito sobre autoridade e publicação

Nenhuma alteração foi feita na `main`, no GitHub Pages, no deploy, na visibilidade do repositório ou na autoridade canônica. Nenhum produto, release, distribuição ou ativo PRODES foi promovido.
