# Política de seleção, exclusão, duplicidade e cobertura

## Objetivo

Tornar explícito por que uma fonte entra no catálogo, como duplicidades são evitadas e quais lacunas permanecem. A política orienta expansão futura, mas não declara o catálogo completo ou representativo de todo o universo de fontes ambientais.

## Unidade de seleção

A unidade elegível é uma **fonte de dados ou infraestrutura de informação** com identidade própria, responsável identificável e acesso público verificável. Exemplos incluem base de dados, repositório, catálogo, portal, plataforma, sistema de informação, sistema de monitoramento, serviço de dados, rede de dados ou software de publicação.

## Critérios mínimos de inclusão

Uma fonte candidata deve atender a todos os requisitos:

1. possuir finalidade relevante para pesquisa, ensino ou extensão em temas ambientais;
2. disponibilizar dados, metadados ou serviços de descoberta/acesso, e não apenas conteúdo editorial;
3. possuir página oficial ou documentação institucional verificável;
4. ter responsável, mantenedor ou arranjo de governança identificável;
5. apresentar utilidade acadêmica distinta ou cobertura que reduza uma lacuna do catálogo;
6. permitir descrição no nível de fonte sem exigir uma linha por dataset;
7. aceitar registro honesto de condições de acesso, licença, limitações e incertezas.

## Critérios de exclusão

Excluir do CSV canônico:

- páginas de notícias, blogs e materiais exclusivamente didáticos;
- artigos, relatórios ou livros sem infraestrutura de dados associada;
- um dataset isolado que pertence claramente a uma fonte já catalogada;
- ferramentas de análise sem função de publicação, descoberta ou acesso a dados;
- cópias não oficiais ou mirrors sem governança própria;
- páginas descontinuadas sem sucessor acessível, salvo quando mantidas em registro histórico separado;
- recursos sem evidência suficiente para confirmar identidade e função.

## Duplicidade e relação entre recursos

### Mesmo recurso, nomes diferentes

Manter uma única linha quando siglas, marcas ou URLs representam a mesma infraestrutura e a mesma governança.

### Portal e base subjacente

Manter linhas separadas somente quando:

- possuem funções decisórias distintas para o usuário;
- têm documentação, acesso ou governança próprios;
- a separação melhora a descoberta sem duplicar integralmente o conteúdo.

### Agregador e provedor

Um agregador pode coexistir com provedores originais. A descrição e as limitações devem alertar sobre possível dupla contagem de datasets.

### Versões regionais

Criar linha própria apenas quando a versão regional possui governança, documentação, cobertura e acesso próprios. Páginas traduzidas ou filtros regionais da mesma infraestrutura não justificam nova linha.

### Recurso sucessor

Quando um recurso substitui outro:

- manter o sucessor no catálogo ativo;
- registrar a relação no histórico ou nas limitações;
- não manter duas linhas ativas se o recurso anterior apenas redireciona e não preserva função independente.

## Candidatos

Novas fontes devem entrar primeiro em uma fila de candidatos separada do CSV canônico. A triagem mínima deve registrar:

- nome e URL;
- motivo da candidatura;
- tema e cobertura presumidos;
- possível duplicidade;
- evidência oficial inicial;
- prioridade;
- decisão: incluir, excluir, fundir, aguardar evidência.

Nenhum candidato deve ser publicado diretamente sem passar por revisão de elegibilidade e completude.

## Matriz de lacunas

A cobertura do catálogo deve ser descrita, não presumida. A análise de lacunas deve cruzar pelo menos:

- área de pesquisa;
- escala geográfica;
- tipo funcional;
- natureza institucional;
- download gratuito;
- acesso programático;
- presença de dados aplicáveis ao Brasil.

A matriz serve para orientar busca de novas fontes. Ela não estabelece cotas artificiais e não transforma frequência de registros em medida de importância científica.

## Critérios de prioridade para expansão

Prioridade maior para fontes que:

1. reduzem lacunas brasileiras ou latino-americanas;
2. são oficiais, acadêmicas ou intergovernamentais e possuem documentação estável;
3. oferecem acesso gratuito, formatos reutilizáveis ou API documentada;
4. cobrem temas pouco representados;
5. têm uso científico demonstrável e limitações identificáveis.

Prioridade menor para fontes redundantes, pouco documentadas, estritamente comerciais ou cuja utilidade já seja coberta por outro recurso mais estável.

## Revisão da seleção

- antes de cada lote de expansão: revisar duplicidades e lacunas;
- anualmente: reavaliar recursos descontinuados, incorporados ou renomeados;
- imediatamente: atualizar quando houver fusão, sucessão ou mudança institucional importante.

## Estado atual

A política orienta a expansão futura. Enquanto DATA1 e DATA2 não estiverem concluídos, a inclusão de novas fontes no CSV canônico permanece bloqueada; apenas a fila de candidatos pode crescer.
