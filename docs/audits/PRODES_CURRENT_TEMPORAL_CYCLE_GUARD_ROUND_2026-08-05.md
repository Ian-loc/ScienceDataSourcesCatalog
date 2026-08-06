# PRODES Amazônia — portão de confirmação do ciclo temporal vigente

**Data/hora de referência:** 2026-08-05, America/Sao_Paulo  
**Escopo:** Instância 1, família `PF000001`  
**Estado:** correção curatorial preventiva; promoção não autorizada

## Ocorrência identificada

O contrato `prodes_product_targets.json` declara corretamente que evidência histórica não deve definir automaticamente o método vigente. Entretanto, o período anual de 1 de agosto a 31 de julho aparece nos campos resolvidos dos dois produtos-alvo iniciais — mapa anual e taxa anual — enquanto a evidência citada para esse campo é uma publicação oficial histórica.

A informação histórica é relevante e pode permanecer documentada. O problema é o seu uso potencial como contrato temporal atual de alta confiança sem uma metodologia vigente, versionada e explicitamente vinculada ao produto e ao release correspondente.

## Correção aplicada

Foi criado o contrato `database/mappings/prodes_current_temporal_cycle_guard_2026.json`, que:

- classifica a evidência disponível como `historical_only` para fins de método atual;
- bloqueia a promoção do campo `temporal_cycle` dos dois produtos-alvo;
- exige metodologia oficial vigente, versão, data e URL persistente;
- impede transferência automática do ciclo entre mapa, taxa, estados preliminares, outros biomas ou distribuições;
- distingue data de atualização operacional do arquivo e período científico representado.

A correção não apaga a evidência histórica nem altera silenciosamente o contrato principal. Ela cria um portão explícito e auditável até que a fonte metodológica vigente seja localizada e verificada.

## Risco evitado

Sem o portão, o catálogo poderia promover como propriedade atual uma regra temporal sustentada apenas por evidência histórica. Isso violaria a própria política do projeto, que proíbe herança automática de método, temporalidade e release.

## Próxima ação

1. localizar a metodologia oficial vigente do PRODES Amazônia;
2. confirmar o período anual de referência e seu escopo;
3. vincular a afirmação ao produto e ao release correto;
4. reconciliar `prodes_product_targets.json` apenas depois da confirmação;
5. manter a promoção bloqueada até a passagem do validador.
