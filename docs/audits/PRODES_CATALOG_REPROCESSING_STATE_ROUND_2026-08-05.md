# Auditoria — estado de reprocessamento do catálogo PRODES

**Data/hora:** 2026-08-05 22:23–22:31, `America/Sao_Paulo`  
**Família:** `PF000001`  
**Escopo:** catálogo de downloads TerraBrasilis e ativos PRODES Amazônia em pré-promoção

## Objetivo

Determinar o efeito curatorial do aviso público de reprocessamento exibido no catálogo TerraBrasilis, sem converter uma mensagem genérica de interface em release, estado definitivo de endpoint ou identidade de um ativo específico.

## Evidência oficial verificada

A página oficial de downloads informa que o Programa BiomasBR atualizou, em **3 de março de 2026**, os dados do monitoramento anual da supressão de vegetação nativa no Brasil. O aviso declara que a atualização impacta todos os arquivos relacionados à supressão e recomenda que usuários atualizem suas bases.

A mesma interface exibe atualmente a mensagem:

> Este arquivo está sendo reprocessado e será atualizado em breve.

O conteúdo recuperado não identifica inequivocamente qual arquivo é o alvo da mensagem. A página continua listando separadamente os componentes PRODES Amazônia e apresenta ações de metadado e download, mas a representação acessível não expõe URLs diretas verificáveis.

Também permanecem observáveis snapshots oficiais dos hosts com e sem `www` com datas diferentes para as mesmas entradas — `2026-06-16` e `2026-07-20`. Essas datas são sinais de atualização da interface, não identificadores científicos de release.

## Decisão curatorial

O aviso de reprocessamento é registrado como **estado contextual do catálogo**. Ele não autoriza concluir que:

- um componente específico está indisponível;
- todos os componentes estão indisponíveis;
- a indisponibilidade é permanente;
- a data do aviso ou da interface identifica uma release;
- o botão de download comprova endpoint operacional;
- os bytes atualmente servidos correspondem ao mesmo snapshot científico anteriormente observado.

Estado preservado:

```text
catalog entries = discoverable
catalog warning = present
individual endpoint state = unresolved
individual current release = unresolved
asset bytes = not inspected
promotion = blocked
```

## Ocorrência

**ID:** `I1-20260805-041`  
**Categoria:** inferência operacional indevida a partir de aviso genérico de reprocessamento  
**Severidade:** `medium`  
**Estado:** `corrected`

**Correção:** contrato e validador impedem transformar o aviso em `working`, `unavailable`, release ou vínculo individual de ativo.  
**Risco residual:** o catálogo pode alterar arquivos ou endpoints enquanto o reprocessamento estiver em curso; uma futura resolução exige teste individual e datado.

## Artefatos

- `database/mappings/prodes_catalog_reprocessing_state_guard_2026.json`;
- `scripts/validate_prodes_catalog_reprocessing_state_guard.py`;
- integração no gate geral `scripts/validate_prodes_product_targets.py`.

## Próxima ação

Resolver um componente por vez mediante URL oficial individual, status HTTP, redirecionamentos, cabeçalhos, nome e tamanho exatos; somente depois recuperar bytes, calcular checksum e relacionar o ativo à release ou snapshot científico correto.
