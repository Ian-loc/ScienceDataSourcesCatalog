# Auditoria do aviso oficial de atualização PRODES — 05/08/2026

Horário de consolidação: `05/08/2026 13:48 BRT` (`America/Sao_Paulo`).

## Objetivo

Registrar, sem promover produto, release, distribuição ou ativo, o significado curatorial do aviso oficial publicado na área de acesso a dados do TerraBrasilis:

- fonte: `https://terrabrasilis.dpi.inpe.br/en/data-access/`;
- operador: INPE / TerraBrasilis;
- aviso: atualização, em `03/03/2026`, dos dados anuais de monitoramento da supressão da vegetação nativa no Brasil;
- escopo declarado: todos os arquivos relacionados à supressão da vegetação nativa;
- orientação ao usuário: atualizar bases locais.

## Interpretação permitida

O aviso comprova um **evento oficial de atualização operacional e de proveniência**. Ele sustenta que bases locais anteriores podem ter se tornado obsoletas e que a curadoria precisa registrar data de recuperação, identidade do ativo e checksum dos bytes efetivamente usados.

## Interpretações proibidas

O aviso, isoladamente, não autoriza:

1. usar `2026-03-03` como `release_id` científico;
2. atribuir uma única versão a todos os arquivos PRODES;
3. presumir que Shapefile, GeoPackage e GeoTIFF foram substituídos simultaneamente;
4. presumir equivalência binária ou semântica entre recortes Brasil, Amazônia e outros biomas;
5. substituir inspeção direta de endpoint, redirecionamento, conteúdo, CRS, geometria, esquema de atributos, licença e citação;
6. promover ativos cujos bytes não foram recuperados e auditados.

## Evidência complementar de volatilidade

O catálogo de downloads observado em `05/08/2026` exibia datas operacionais diferentes entre distribuições, incluindo atualizações posteriores a março de 2026. Portanto, o aviso geral e as datas por arquivo devem ser modelados como eventos de proveniência distintos, não como uma versão científica comum.

## Implementação

Foram atualizados:

- `database/mappings/prodes_operational_evidence_2026.json` para a versão `1.1.0`, com `PRODES-OP-EV-003` e o bloco `catalog_update_notice`;
- `scripts/validate_prodes_operational_evidence.py`, que agora exige a nova evidência, sua data, sua interpretação restritiva e a proibição explícita de convertê-la em `release_id`.

## Validação

O workflow **Validar e publicar catálogo**, execução `#309`, foi aprovado integralmente no commit `a904db2d766aee8fb73d24c53de2fa4d22c4fe5b`.

## Estado científico e operacional

- família: `PF000001` — PRODES;
- estado: `pre_promotion_evidence`;
- promoção autorizada: `false`;
- release formal: não resolvido;
- URLs diretas e checksums: não resolvidos;
- algoritmo vigente e ajuste para áreas não observadas: não resolvidos;
- licença e citação por produto/release: não resolvidas.

## Próxima unidade segura

Resolver um ativo PRODES Amazônia por vez, começando pelo registro GeoNetwork do incremento anual (`b75b83db-8026-43f9-9537-ee1dfa308158`), mantendo separadas:

- identidade do metadado;
- identidade do release;
- endpoint direto;
- resposta e redirecionamentos;
- bytes e checksum;
- contrato geoespacial e de atributos;
- licença e citação.

Nenhuma alteração foi feita na `main`, no GitHub Pages, no deploy, na visibilidade do repositório ou na autoridade canônica.
