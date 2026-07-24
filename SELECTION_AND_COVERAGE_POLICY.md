# Política de seleção, exclusão, duplicidade e cobertura

## Objetivo

Explicitar por que uma fonte entra, como duplicidades são evitadas e quais lacunas permanecem. O catálogo não é declarado completo ou representativo de todo o universo ambiental.

## Escopo territorial prioritário

O **Brasil é o escopo territorial central e prioritário** do Science Data Sources Catalog.

A curadoria, a revisão factual, o detalhamento de produtos e a busca por novas fontes devem priorizar, nesta ordem:

1. fontes brasileiras com dados sobre o Brasil;
2. fontes internacionais com cobertura brasileira sistemática e diretamente pesquisável;
3. fontes internacionais em que a presença de dados brasileiros depende do dataset, depósito, sítio, coleção ou produto;
4. excepcionalmente, referências internacionais sem cobertura brasileira direta, quando houver valor metodológico, comparativo ou de infraestrutura claramente documentado.

A prioridade territorial não é uma nota de qualidade científica. Ela organiza o investimento de curadoria e a descoberta pública. A qualidade e a adequação continuam sendo avaliadas no nível da fonte, do produto e da distribuição.

## Classificação Brasil P0–P3

A camada curatorial `data/brazil_scope_priorities.json` classifica todos os registros canônicos:

| Prioridade | Classe | Papel |
|---|---|---|
| `P0` | `fonte_brasileira` | núcleo do catálogo |
| `P1` | `cobertura_brasil_sistematica` | complemento internacional prioritário |
| `P2` | `cobertura_brasil_parcial` | contexto dependente do produto ou coleção |
| `P3` | `referencia_sem_cobertura_brasil` | referência comparativa excepcional |

A classificação é manual e auditável. Não deve ser inferida apenas pelo domínio da URL, idioma da interface, nome da instituição ou alcance geográfico declarado.

### Regra para P0

Uma fonte é P0 quando sua governança principal é brasileira e ela disponibiliza dados, metadados, produtos ou serviços de descoberta pertinentes ao Brasil.

### Regra para P1

Uma fonte é P1 quando, embora internacional, inclui o Brasil de forma regular, sistemática ou diretamente consultável, e seus dados têm utilidade demonstrável para pesquisa sobre o país.

### Regra para P2

Uma fonte é P2 quando a presença de dados brasileiros é possível, mas depende de depósitos, sítios, coleções, projetos ou produtos específicos. A interface não deve sugerir cobertura brasileira uniforme.

### Regra para P3

Uma fonte sem dados brasileiros diretos somente pode permanecer como P3 quando:

1. oferece referência metodológica ou comparativa não substituída por fonte brasileira;
2. ajuda a compreender padrões, serviços ou arquiteturas relevantes para o catálogo;
3. sua função secundária é explicitamente apresentada;
4. não desloca fontes brasileiras da fila prioritária de revisão ou expansão.

## Unidade de seleção

A unidade elegível é uma **fonte de dados ou infraestrutura de informação** com identidade própria, responsável identificável e acesso verificável: base, repositório, catálogo, portal, plataforma, sistema, serviço, rede ou software de publicação.

## Critérios mínimos de inclusão

A fonte deve:

1. ser relevante para pesquisa, ensino ou extensão ambiental;
2. disponibilizar dados, metadados ou serviço de descoberta/acesso, não apenas conteúdo editorial;
3. possuir documentação oficial verificável;
4. ter governança identificável;
5. oferecer utilidade distinta ou reduzir lacuna;
6. permitir descrição no nível de fonte;
7. permitir registro honesto de acesso, licença, limitações e incertezas;
8. demonstrar vínculo com o escopo brasileiro ou justificar formalmente sua função estratégica secundária.

## Critérios de exclusão

Excluir do CSV canônico:

- notícias, blogs e materiais somente didáticos;
- artigos ou relatórios sem infraestrutura associada;
- dataset isolado pertencente a fonte já catalogada;
- ferramenta sem função de publicação, descoberta ou acesso;
- mirror sem governança própria;
- recurso descontinuado sem função independente;
- recurso cuja identidade ou função não tenha evidência suficiente;
- fonte internacional redundante, sem dados brasileiros e sem justificativa estratégica distinta.

## Recursos bibliométricos e editoriais

Bases de literatura, rankings e redes de citação exigem um portão de escopo antes da migração. A decisão deve avaliar reutilização estruturada, função de descoberta ambiental, governança, condições de acesso, utilidade distinta e destino adequado: catálogo principal, seção auxiliar, fusão ou exclusão.

### Regra derivada de G0

Um recurso bibliométrico pode permanecer no catálogo principal quando:

1. oferece dados ou metadados estruturados, busca, rede de citações ou função de descoberta reutilizável;
2. possui metodologia oficial e governança identificável;
3. tem utilidade distinta para pesquisa, ensino ou extensão ambiental;
4. permite registrar acesso, licença e limitações com honestidade;
5. não é apresentado como substituto de fontes ambientais primárias;
6. sua utilidade para o Brasil ou sua função estratégica secundária está documentada.

Materiais apenas narrativos, noticiosos ou didáticos, sem infraestrutura estruturada, continuam excluídos.

A natureza bibliométrica deve ser explícita. Cobertura de publicações e citações não deve ser confundida com cobertura espacial ou temporal de observações ambientais.

### Decisão do Project COSMOS

G0 confirmou a elegibilidade do Project COSMOS para o catálogo principal como infraestrutura bibliométrica. A decisão completa está em `G0_COSMOS_SCOPE_DECISION.md`.

A permanência não implica que a base integral seja aberta, que exista API pública ou que o recurso forneça medições ambientais. Esses atributos permanecem descritos com suas limitações e sujeitos à revisão factual final.

## Duplicidade e relação entre recursos

### Mesmo recurso, nomes diferentes

Manter uma linha quando nomes, siglas ou URLs representam a mesma infraestrutura e governança.

### Portal e base subjacente

Manter linhas separadas somente quando possuem função, documentação, acesso ou governança próprios e a separação melhora a descoberta sem duplicação integral.

### Agregador e provedor

Podem coexistir, mas devem alertar sobre dupla contagem e preservar o provedor original. Quando houver alternativa brasileira original, ela recebe prioridade de descoberta sobre o agregador internacional.

### Versões regionais

Criar linha própria somente com governança, documentação, cobertura e acesso próprios.

### Recurso sucessor

Manter o sucessor ativo, registrar a relação e não conservar duas linhas quando o anterior apenas redireciona.

## Candidatos

Novas fontes entram primeiro em `candidates/source_candidates.csv`, com nome, URL, justificativa, tema, cobertura, duplicidade, evidência, prioridade e decisão: incluir, excluir, fundir ou aguardar evidência.

Uma URL fornecida pelo usuário autoriza triagem inicial, não decisão final. Nenhum candidato é publicado sem revisão de elegibilidade e completude.

### Ordem da fila de expansão

A fila deve ser executada nesta ordem:

1. candidatos brasileiros de prioridade alta;
2. candidatos internacionais de prioridade alta com dados sistemáticos sobre o Brasil;
3. candidatos brasileiros de prioridade média;
4. candidatos internacionais com cobertura brasileira parcial;
5. metacatálogos e referências globais;
6. recursos sem cobertura brasileira direta, somente após justificativa de exceção.

O rótulo de prioridade do candidato deve refletir simultaneamente lacuna científica, relevância territorial, estabilidade documental e utilidade distinta.

## Matriz de lacunas

A cobertura deve cruzar:

- área de pesquisa;
- bioma, ecossistema ou região brasileira;
- escala geográfica;
- tipo funcional de fonte;
- natureza institucional;
- download gratuito;
- acesso programático;
- presença e profundidade de dados do Brasil;
- origem brasileira ou internacional;
- representação de produtos e distribuições.

A matriz orienta busca; não cria cotas e frequência de registros não mede importância científica.

## Critérios de prioridade para expansão

### Prioridade máxima

- fontes federais, estaduais, municipais, universitárias ou de redes científicas brasileiras;
- fontes de cobertura nacional ou de biomas brasileiros;
- fontes que reduzam lacunas em biodiversidade, clima, água, solo, florestas, agricultura, oceanografia, saúde ambiental, emissões e dados socioecológicos;
- infraestruturas com documentação estável, identificadores, metadados reutilizáveis, API ou downloads bem definidos;
- fontes com uso científico demonstrável e produtos distinguíveis.

### Prioridade complementar

- fontes internacionais que incluam o Brasil sistematicamente;
- fontes latino-americanas com forte cobertura brasileira ou interoperabilidade regional útil;
- repositórios gerais com volume relevante de dados brasileiros e meios confiáveis de descoberta.

### Prioridade baixa ou excepcional

- recursos redundantes;
- fontes pouco documentadas;
- recursos estritamente comerciais;
- metacatálogos globais já cobertos por fonte mais estável;
- fontes sem dados brasileiros diretos e sem função estratégica distinta.

## Revisão da seleção

- antes de expansão: revisar duplicidades, escopo e lacunas brasileiras;
- a cada ciclo de inclusão: confirmar classificação P0–P3;
- anualmente: reavaliar recursos descontinuados, incorporados ou renomeados;
- imediatamente: atualizar fusão, sucessão ou mudança institucional;
- antes da migração: resolver portões de escopo pendentes;
- antes da versão 1.0.0: justificar individualmente todos os registros P3.

## Estado atual

O CSV 0.7.0 permanece com 51 fontes e 34 campos. A camada P0–P3 não altera o esquema canônico; ela adiciona uma classificação curatorial vinculada por `resource_id` e validada no CI.

Enquanto DATA1 e DATA2 não estiverem concluídos, novas fontes permanecem fora do CSV. O portão G0 do Project COSMOS está resolvido com decisão `manter_confirmado`; W1A é o próximo ciclo de DATA1-EXT. Nenhuma inclusão automática no CSV 0.7.0 é autorizada por esta política.
