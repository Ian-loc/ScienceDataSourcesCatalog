# DEC — Instância 1 como catálogo de granularidade mínima suficiente

**Data:** 6 de agosto de 2026  
**Status:** proposta para incorporação  
**Escopo:** arquitetura, curadoria, pesquisa e métricas da Instância 1

## Contexto

O Marco 1 incorporou uma arquitetura relacional profunda capaz de distinguir organização, fonte, família, produto, release, distribuição, ativo e capacidade. A aplicação desse desenho ao DETER Cerrado demonstrou rastreabilidade, mas também revelou um custo e uma granularidade desproporcionais ao objetivo atual.

A curadoria passou a perseguir releases, arquivos, layers, bytes, schemas, checksums, endpoints e evidências atômicas que pertencem às próprias plataformas externas ou a futuros conectores. O resultado foi um PR grande, validadores específicos e dificuldade para definir quando uma entrada estava suficientemente concluída.

## Decisão

A Instância 1 passa a ser implementada como **catálogo relacional de fontes e ofertas de dados científicos**, orientado por granularidade mínima suficiente.

A entidade central será `catalog_entry`. Uma entrada poderá representar fonte, plataforma, coleção, produto ou serviço quando esse nível for útil para descoberta e compreensão.

O núcleo-alvo será:

- `organizations`;
- `catalog_entries`;
- `entry_variables`;
- `entry_evidence`;
- `connector_profiles` opcional.

A arquitetura profunda incorporada no Marco 1 não será apagada de forma destrutiva. Seus componentes poderão permanecer como legado técnico ou extensões futuras, mas deixarão de definir completude e prioridade.

## Consequências positivas

- reduz custo de curadoria;
- torna o escopo verificável;
- evita reconstruir catálogos externos;
- permite concluir entradas amplas como GEDI sem enumerar seus produtos internos;
- aproxima o modelo das necessidades do website;
- preserva caminho para conectores seletivos da Instância 2;
- reduz validadores específicos e conflitos semânticos artificiais.

## Custos e riscos

- parte do esquema atual ficará temporariamente subutilizada;
- será necessário criar uma migração compatível e não destrutiva;
- alguns detalhes técnicos deixarão de ser filtros estruturados;
- conectores futuros poderão exigir extensão localizada;
- documentos e scripts anteriores precisam ser reclassificados.

## Critério para expansão futura

Uma nova entidade, tabela, coluna, vocabulário ou validador somente será aceita quando necessária para:

1. descoberta;
2. interpretação mínima;
3. filtro ou apresentação no website;
4. conector selecionado.

Padrões externos e literatura não geram expansão automática.

## Disposição do PR #57

O PR #57 fica congelado e não deve ser ampliado nem mesclado sob a autorização anterior. Seu conteúdo permanece como evidência histórica de curadoria profunda e fonte seletiva de metadados.

Após incorporação desta decisão, deverá ser avaliado para encerramento como `superseded`. O encerramento exige ação humana explícita.

## Plano de implementação

1. alinhar documentos canônicos;
2. desenhar o esquema mínimo e a migração sem perda;
3. criar crosswalk entre estrutura atual e `catalog_entries`;
4. validar GEDI, DETER Cerrado, IBGE e ANA/SNIRH;
5. revisar um primeiro lote de entradas;
6. gerar exportação para o website;
7. auditar e promover o novo núcleo mediante autorização.

## Limites

Esta decisão não:

- altera ou publica Pages;
- copia dados externos;
- ativa a Instância 2;
- promove PostgreSQL a produção;
- remove tabelas existentes;
- fecha o PR #57 automaticamente;
- altera Drive ou visibilidade do repositório.
