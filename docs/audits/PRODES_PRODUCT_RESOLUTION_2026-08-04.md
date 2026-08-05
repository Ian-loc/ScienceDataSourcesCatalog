# Resolução científica e operacional da família PRODES

**Projeto:** Simbiotrama — Instância 1  
**Data de auditoria:** 04/08/2026 23:23 BRT (`America/Sao_Paulo`)  
**Branch:** `agent/consolidate-instance-1-relational-catalog`  
**Estado:** decisão curatorial ativa; nenhuma promoção canônica autorizada

## Problema

O registro legado `DP000001` foi corretamente resolvido como a família `PF000001 — PRODES`. Entretanto, a família não pode ser promovida diretamente como um único produto científico. A documentação institucional descreve pelo menos dois objetos informacionais distintos:

1. **mapeamento anual de áreas de desflorestamento/supressão**, representado por geometrias ou camadas espaciais;
2. **estimativa anual da taxa de desflorestamento**, representada por uma série estatística agregada.

Esses objetos possuem suportes, unidades, métodos de cálculo, distribuições e interpretações diferentes. A taxa não é apenas um atributo intercambiável do mapa, e o mapa não deve ser descrito como se fosse a própria taxa anual oficial.

## Evidência oficial usada

- O INPE informa que o PRODES produz, desde 1988, estimativas anuais das taxas de desflorestamento da Amazônia Legal, organizadas por estado.
- A documentação do DETER distingue explicitamente alertas operacionais da taxa anual oficial fornecida pelo PRODES.
- A documentação institucional também descreve o PRODES como sistema de monitoramento por satélite e fonte de mapeamento das áreas desflorestadas.

Fontes verificadas:

- https://www.gov.br/inpe/pt-br/acesso-a-informacao/perguntas-frequentes/principais-produtos-e-servicos-do-inpe/monitoramento-do-territorio-florestas/como-se-monitora-o-desmatamento
- https://www.gov.br/inpe/pt-br/area-conhecimento/unidade-amazonia/projetos-e-pesquisas/deter/deter
- https://www.gov.br/inpe/pt-br/area-conhecimento/unidade-amazonia/projetos-e-pesquisas/terraclass/terraclass

## Decisão de modelagem

A família `PF000001` deve permanecer como agrupadora. A enumeração inicial deve distinguir, no mínimo:

### Produto A — mapeamento anual PRODES Amazônia

**Tipo proposto:** `map_series`  
**Objeto científico:** áreas mapeadas como desflorestamento por corte raso/supressão segundo o protocolo e a máscara de monitoramento do PRODES.  
**Suporte esperado:** polígonos ou raster de mapeamento anual, conforme a distribuição específica.  
**Não representa:** alerta em tempo real, data exata da ocorrência, causa do desmatamento, legalidade, taxa mensal ou observação de campo.

### Produto B — taxa anual PRODES Amazônia

**Tipo proposto:** `indicator_series`  
**Objeto científico:** estimativa anual agregada da área desflorestada na Amazônia Legal segundo o procedimento estatístico e cartográfico do PRODES.  
**Suporte esperado:** unidade territorial e período anual PRODES.  
**Não representa:** soma simples e necessariamente idêntica de qualquer arquivo vetorial baixado, taxa mensal, alerta operacional ou probabilidade pixel a pixel.

## Pendências antes da promoção

1. verificar a documentação metodológica específica da série vigente;
2. identificar o calendário anual PRODES e distinguir ano de referência, data de aquisição e data de divulgação;
3. identificar limiar/unidade mínima de mapeamento e suas mudanças históricas;
4. verificar separadamente as distribuições de incremento anual, máscara acumulada, estatísticas e dashboards;
5. confirmar quais biomas possuem séries próprias e evitar generalização do PRODES Amazônia para Cerrado ou outros biomas;
6. registrar versões/releases sem presumir que cada ano civil corresponde diretamente a uma versão homogênea;
7. testar endpoints e downloads no TerraBrasilis;
8. registrar licença, citação e documentação no nível correto de produto ou release.

## Resultado da auditoria

- `DP000001` permanece corretamente classificado como família no staging.
- Nenhum produto ou release PRODES foi criado neste round, evitando promoção prematura.
- A próxima operação segura é criar um mapeamento explícito de produtos-alvo e somente então implementar a promoção idempotente.
- O banco PostgreSQL/PostGIS continua arquitetura de destino; os CSVs e a página pública permanecem autoridades materiais durante a transição.
