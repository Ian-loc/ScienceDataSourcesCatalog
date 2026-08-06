# Política de escopo e granularidade da Instância 1

**Projeto:** Simbiotrama — Catálogo de Dados Científicos do Brasil  
**Status:** proposta normativa  
**Data:** 6 de agosto de 2026  
**Fuso dos relatórios humanos:** `America/Sao_Paulo`

## 1. Objetivo

A Instância 1 é um catálogo relacional de fontes e ofertas de dados científicos. Seu propósito é permitir que uma pessoa encontre, compreenda e acesse dados mantidos pelas instituições produtoras.

A regra central é operar com **granularidade mínima suficiente**: registrar apenas o nível necessário para descoberta, compreensão, filtragem e encaminhamento à fonte oficial.

O Simbiotrama não é, nesta fase:

- repositório ou arquivo de datasets externos;
- espelho de catálogos de terceiros;
- inventário exaustivo de arquivos, layers, bandas ou endpoints;
- reconstrução da genealogia completa de produtos;
- plataforma de harmonização ou análise de dados;
- ontologia universal de variáveis científicas.

## 2. Unidade central

A unidade central é a **entrada de catálogo** (`catalog_entry`). Uma entrada pode representar uma fonte, plataforma, coleção, produto de dados ou serviço quando esse nível for útil para descoberta e compreensão.

Uma nova entrada somente deve ser criada quando existir diferença material em pelo menos um dos seguintes aspectos:

- significado ou escopo científico;
- modalidade principal de dados;
- cobertura geográfica ou temporal;
- método ou finalidade;
- público ou uso principal;
- forma principal de acesso.

Não se cria nova entrada apenas porque existe outro arquivo, formato, layer, banda, diretório, endpoint ou atualização técnica.

## 3. Metadados mínimos suficientes

Uma entrada deve buscar, proporcionalmente ao que a fonte documenta:

- organização responsável;
- nome oficial e acrônimo;
- tipo amplo da entrada;
- resumo e escopo científico;
- modalidades de dados;
- temas e variáveis principais;
- cobertura espacial e temporal;
- resolução ou suporte quando material para interpretação;
- frequência de atualização quando disponível;
- gratuidade, autenticação e condições gerais de acesso;
- página oficial;
- página de metadados;
- acesso principal;
- metodologia, licença e citação quando disponíveis;
- estado e data da verificação curatorial.

Os nomes e definições do produtor devem ser preservados. Termos simplificados ou normalizados podem ser adicionados apenas para busca e filtros.

## 4. Arquitetura mínima

O núcleo ativo deve permanecer reduzido a:

- `organizations`;
- `catalog_entries`;
- `entry_variables`;
- `entry_evidence`;
- `connector_profiles`, opcional e orientado à futura Instância 2.

Metadados excepcionais podem permanecer em JSONB enquanto não houver caso de uso repetido que justifique normalização.

Não são entidades obrigatórias da Instância 1:

- famílias de produtos;
- releases;
- distribuições;
- ativos;
- capacidades detalhadas;
- observações primárias;
- esquemas completos de classes;
- linhagens de transformação;
- estimands ou populações-alvo;
- inventários de artefatos relacionados.

Esses conceitos podem ser representados como texto, metadado adicional ou extensão futura somente quando houver necessidade concreta.

## 5. Pesquisa proporcional

A pesquisa começa pela página oficial e pelos metadados diretos da fonte ou entrada. Documentação metodológica, licença e citação são examinadas no nível necessário para uma ficha confiável.

A investigação deve parar quando:

1. os campos essenciais estiverem sustentados;
2. o usuário puder compreender o que encontrará;
3. houver caminho oficial para acesso ou continuidade da busca;
4. lacunas restantes estiverem explicitamente registradas.

Não se exige como rotina:

- identificação de release vigente;
- inspeção de bytes;
- checksum;
- schema físico completo;
- enumeração de arquivos ou layers;
- validação de cada endpoint disponível;
- licença ou citação por arquivo.

Essas atividades só pertencem à Instância 1 quando indispensáveis para corrigir uma afirmação central. Para conectores específicos, pertencem ao perfil técnico da Instância 2.

## 6. Evidência e qualidade

Evidência deve ser suficiente e proporcional ao campo sustentado. Não é necessário criar um pacote forense ou uma afirmação independente para cada detalhe trivial.

Estados curatoriais recomendados:

- `verified`;
- `partially_verified`;
- `not_found`;
- `not_applicable`;
- `needs_review`.

Não haverá escore universal de qualidade ou completude. Ausência de documentação não deve ser convertida em ausência do fenômeno, método, licença ou incerteza.

## 7. Gate para expansão do esquema

Uma nova entidade, coluna, tabela, vocabulário ou validador somente pode entrar no núcleo se demonstrar necessidade direta para pelo menos uma destas funções:

1. descoberta no catálogo;
2. interpretação mínima da entrada;
3. filtro ou apresentação no website;
4. configuração de um conector selecionado.

Literatura, padrões externos, auditorias antigas e reflexões de outros ambientes são insumos, não autoridade arquitetural. Conceitos úteis apenas para ontologia, síntese, harmonização, genealogia ou análise permanecem em backlog.

## 8. Separação das instâncias

### Instância 1

Cataloga fontes e ofertas de dados, com metadados essenciais e links oficiais.

### Instância 2

Poderá usar APIs, serviços e outros conectores externos para visualização federada. Não exige armazenamento dos dados nem enumeração prévia de todos os objetos das plataformas.

### Instância 3

Poderá contextualizar produtos e visualizações com literatura científica curada. Não lidera a arquitetura da Instância 1.

## 9. Métricas de avanço

O progresso será medido por:

- entradas úteis concluídas;
- cobertura dos campos essenciais;
- links oficiais verificados;
- temas e variáveis identificados;
- prontidão para exibição no website;
- candidatos viáveis a conectores futuros.

Não serão métricas principais:

- número de releases;
- ativos enumerados;
- arquivos inspecionados;
- afirmações atômicas;
- commits;
- validadores específicos.

## 10. Teste de adequação

O modelo deve ser validado com entradas heterogêneas, inicialmente:

- GEDI;
- DETER Cerrado;
- IBGE;
- ANA/SNIRH.

Ele será considerado adequado se representar esses casos sem proliferação de tabelas, sem inventário integral, sem campos excessivamente vazios e sem perda do significado necessário ao usuário.
