# Política de comparabilidade, evidência e inferência científica

**Status:** diretriz normativa do projeto  
**Aplicação:** catálogo, Explorador Federado, futura interface Simbioscópio, receitas analíticas, produtos derivados e comunicação pública  
**Princípio orientador:** **A vida acontece em relação. As relações precisam ser investigadas com evidência.**

## 1. Finalidade

Esta política estabelece limites científicos e requisitos computacionais para a seleção, sobreposição, combinação, comparação e análise de produtos de dados provenientes de fontes, disciplinas, escalas, períodos e métodos distintos.

O projeto reconhece que variáveis ambientais, ecológicas, sociais, epidemiológicas, econômicas, institucionais, políticas e territoriais podem representar dimensões interdependentes do mundo real. Essa interdependência, entretanto, não torna automaticamente comparáveis os respectivos conjuntos de dados e não autoriza inferências causais a partir de coincidências visuais ou correlações estatísticas.

A plataforma deve permitir exploração e descoberta sem transformar sobreposições cartográficas ou associações observadas em conclusões científicas indevidas.

## 2. Princípios obrigatórios

1. **Sobreposição não é harmonização.** Camadas exibidas juntas permanecem cientificamente independentes até que sua comparabilidade seja avaliada.
2. **Correlação não é mecanismo.** Uma associação estatística não demonstra como ou por que dois fenômenos se relacionam.
3. **Mecanismo plausível não é causalidade demonstrada.** A existência de uma explicação teórica ou biológica coerente não elimina confundimento, viés ou explicações alternativas.
4. **Metadados são condição de análise.** Produtos sem definição, escala, período, unidade, proveniência ou método suficientes não podem sustentar combinações analíticas automatizadas.
5. **A inferência deve ser proporcional à evidência.** A linguagem apresentada ao usuário não pode exceder o desenho dos dados, os diagnósticos realizados e a literatura disponível.
6. **Exploração livre e inferência científica são operações distintas.** A primeira pode ser ampla; a segunda exige controles progressivamente mais rigorosos.
7. **Proveniência e dependência entre produtos devem permanecer visíveis.** Releases, indicadores ou produtos derivados da mesma fonte não constituem observações independentes apenas por possuírem nomes diferentes.
8. **Discordância científica deve ser preservada.** A plataforma não deve resumir debates complexos em uma falsa nota única de consenso.
9. **Automação não substitui julgamento científico.** Regras computacionais podem bloquear incompatibilidades evidentes, sinalizar riscos e documentar pressupostos, mas não decidem sozinhas validade causal ou relevância científica.

## 3. Escopo

Esta política é obrigatória para:

- inclusão de camadas no Explorador Federado;
- futuras funções do Simbioscópio;
- comparação de produtos e releases;
- recortes, reprojeções, reamostragens, agregações e junções;
- cálculo de correlações, regressões, índices e indicadores compostos;
- receitas de integração e produtos derivados;
- visualizações que aproximem variáveis de diferentes domínios;
- relatórios, mapas, tabelas, APIs e manifestos produzidos pelo projeto;
- afirmações sobre associação, mecanismo, explicação ou causalidade.

## 4. Passaporte científico de produtos e variáveis

Nenhuma combinação analítica deve ser automatizada sem um conjunto mínimo de metadados legíveis por máquina.

Cada produto ou variável deverá registrar, quando aplicável:

- definição conceitual;
- unidade e possibilidade de conversão;
- tipo de dado: contínuo, categórico, ordinal, contagem, taxa ou proporção;
- população, fenômeno ou objeto observado;
- unidade de observação e suporte espacial;
- resolução, extensão e sistema de referência espacial;
- período representado, data de observação e frequência temporal;
- método de obtenção: medido, administrativo, declarado, classificado, modelado, interpolado ou derivado;
- versão ou release;
- incerteza, erro ou qualidade disponível;
- tratamento de valores ausentes e NoData;
- fonte primária e linhagem de derivação;
- limitações declaradas;
- licença e permissões para processamento e redistribuição.

Ausências críticas devem gerar estado **informação insuficiente**, e não preenchimento presumido.

## 5. Níveis de operação

### 5.1 Composição visual livre

O usuário pode sobrepor produtos sem harmonização analítica.

Requisitos:

- identidade, fonte, versão, período e licença de cada camada visíveis;
- aviso permanente de que composição visual não implica comparabilidade;
- proibição de apresentar estatísticas combinadas como resultado validado;
- manifesto de proveniência para visualizações compartilhadas ou exportadas.

### 5.2 Comparação orientada

O sistema avalia compatibilidade e, quando defensável, sugere período comum, unidade, resolução, território e transformações necessárias.

Toda transformação deve ser explicitada e reproduzível.

### 5.3 Análise exploratória

Correlação, regressão ou comparação quantitativa exploratória só pode ocorrer após avaliação técnica mínima e deve ser rotulada como exploratória.

O sistema deve registrar a pergunta, as variáveis, a escala, o período, os filtros, as transformações e o número de testes realizados.

### 5.4 Inferência científica condicionada

Interpretações explicativas ou causais exigem desenho científico explícito, pressupostos documentados, avaliação de confundidores, mecanismos e evidência publicada. Não devem ser liberadas automaticamente por uma correlação ou por um modelo estatístico isolado.

## 6. Semáforo de comparabilidade

Toda combinação deve receber uma classificação operacional:

- **A — diretamente comparável:** conceitos, população, período, escala, unidade e proveniência compatíveis para a operação solicitada;
- **B — comparável após harmonização explícita:** exige conversão, agregação, alinhamento temporal, reprojeção ou outra transformação documentada;
- **C — somente composição visual ou exploração preliminar:** relação potencialmente interessante, mas sem base técnica suficiente para análise conjunta direta;
- **D — inadequada para a operação solicitada:** incompatibilidade conceitual, espacial, temporal, populacional, metodológica ou jurídica impeditiva;
- **E — informação insuficiente:** metadados não permitem avaliar a combinação.

A classificação é específica da operação. Dois produtos podem ser classe C para correlação, mas adequados para visualização lado a lado.

## 7. Dimensões mínimas de compatibilidade

O sistema deve avaliar separadamente:

1. **semântica:** as variáveis representam o mesmo fenômeno ou fenômenos cuja relação foi corretamente definida?;
2. **população e suporte:** os valores se referem aos mesmos indivíduos, grupos, territórios ou unidades observacionais?;
3. **espacial:** extensão, resolução, grade, geometria, sistema de referência e unidade territorial;
4. **temporal:** período, frequência, defasagem, acumulado, média ou observação instantânea;
5. **metodológica:** medição, modelo, classificação, declaração administrativa, interpolação ou derivação;
6. **estatística:** distribuição, tamanho amostral, incerteza, dependência, ausência e censura;
7. **proveniência:** fontes primárias, versões compartilhadas e transformações comuns;
8. **jurídica e ética:** licença, privacidade, risco de reidentificação e uso de populações vulneráveis.

## 8. Controles contra relações espúrias

As análises futuras devem, conforme aplicável, diagnosticar e comunicar:

- tendências temporais comuns sem mecanismo demonstrado;
- autocorrelação espacial e ausência de independência entre unidades vizinhas;
- mudança de resultado conforme a escala ou zoneamento territorial;
- dependência entre produtos derivados da mesma fonte;
- diferenças de cobertura e seleção territorial;
- valores ausentes não aleatórios;
- múltiplas comparações e inflação de falsos positivos;
- confundimento, mediação e colisores;
- defasagens temporais plausíveis;
- relações não lineares e efeitos de limiar;
- instabilidade entre versões, períodos e especificações alternativas;
- paradoxo ecológico e limites de inferência de dados agregados para indivíduos.

Quando um diagnóstico necessário não puder ser realizado, essa ausência deve reduzir o teto de inferência e aparecer no resultado.

## 9. Bússola de evidências

Relações entre variáveis poderão possuir fichas científicas estruturadas contendo:

- mecanismo ou argumento proposto;
- direção esperada, inclusive relações não lineares ou contextuais;
- mediadores e confundidores conhecidos;
- escala espacial e temporal em que a relação é plausível;
- estudos favoráveis, contrários e inconclusivos;
- desenho e qualidade dos estudos;
- aplicabilidade ao Brasil e ao território selecionado;
- limitações e controvérsias;
- data e responsável pela revisão.

A plataforma deve separar, no mínimo:

- **concordância:** proporção e direção dos resultados;
- **certeza:** robustez dos métodos e desenhos;
- **aplicabilidade:** pertinência ao território, população e escala analisados;
- **suporte mecanístico:** coerência teórica, biológica, social ou institucional;
- **discordância:** existência e natureza de resultados contraditórios.

Não deve ser exibida uma porcentagem única de consenso como substituto dessas dimensões.

## 10. Teto de inferência

Cada resultado deve informar o nível máximo de afirmação permitido:

- **N0 — composição visual:** produtos aparecem juntos;
- **N1 — coocorrência:** fenômenos coincidem no espaço ou no tempo;
- **N2 — associação exploratória:** associação observada nos dados selecionados;
- **N3 — associação robusta condicionada:** persistência após diagnósticos e análises de sensibilidade;
- **N4 — mecanismo sustentado:** associação coerente com teoria e evidência publicada, sem eliminar explicações alternativas;
- **N5 — inferência causal condicionada:** desenho e pressupostos explícitos permitem interpretação causal delimitada.

N5 exige avaliação científica humana e não pode ser atribuído automaticamente pelo sistema.

## 11. Diagramas de relações e causalidade

A futura representação de relações deve distinguir visualmente:

- associação observada;
- hipótese;
- mecanismo plausível;
- mediação;
- confundimento;
- influência bidirecional;
- evidência causal;
- evidência contraditória;
- relação desconhecida.

Diagramas causais são representações de pressupostos, não provas. Qualquer análise baseada neles deve preservar autoria, versão e justificativa das relações desenhadas.

## 12. Proveniência, versões e independência

Todo resultado combinado deverá registrar:

- produtos e arquivos de entrada;
- fonte primária;
- versão ou release;
- data de acesso;
- parâmetros e transformações;
- código ou receita utilizada;
- produtos intermediários;
- limitações;
- citações e licenças.

O sistema deverá detectar, quando possível, produtos que compartilham insumos, modelos, censos, sensores, grades, indicadores ou versões. Essa dependência deve ser apresentada ao usuário e considerada em qualquer síntese de evidência.

## 13. Regras de comunicação

A interface e os relatórios devem preferir linguagem proporcional à evidência:

- “aparece junto”, para composição visual;
- “coocorre”, para coincidência espacial ou temporal;
- “está associado”, para associação estatística;
- “é consistente com”, para mecanismo plausível;
- “pode contribuir”, quando persistem explicações alternativas;
- “efeito causal estimado”, somente quando o desenho e os pressupostos justificarem.

Expressões como “prova”, “determina”, “causa” ou “explica” não podem ser geradas apenas por correlação, sobreposição ou significância estatística.

## 14. Implementação progressiva

### Fase 1 — fundamento obrigatório

- passaportes científicos;
- semáforo de comparabilidade;
- proveniência por camada e produto;
- separação entre visualização e análise;
- bloqueio de incompatibilidades evidentes.

### Fase 2 — diagnósticos computacionais

- alinhamento espacial e temporal;
- detecção de dependência entre produtos;
- autocorrelação espacial;
- estabilidade entre escalas;
- múltiplas comparações;
- relatórios automáticos de limitações.

### Fase 3 — evidência estruturada

- fichas de relações;
- literatura favorável e contraditória;
- mecanismos, mediadores e confundidores;
- avaliação humana de certeza e aplicabilidade.

### Fase 4 — laboratório de nexos

- diagramas causais versionados;
- análises reproduzíveis;
- testes de sensibilidade;
- teto de inferência executável;
- produtos derivados com manifesto completo.

## 15. Governança e mudanças

Alterações nesta política, nas classes de comparabilidade, no teto de inferência ou nas regras que autorizem análises devem:

1. ser propostas em branch e pull request próprios;
2. apresentar justificativa científica e impacto computacional;
3. incluir casos de teste ou exemplos de aplicação;
4. ser revisadas pelo responsável científico;
5. ser registradas no histórico do projeto.

Mudanças de interface não podem enfraquecer silenciosamente avisos, bloqueios ou limites definidos nesta política.

## 16. Regra de decisão resumida

> O sistema pode permitir ampla exploração visual. Quanto mais forte a operação ou a afirmação pretendida, maiores devem ser os requisitos de comparabilidade, diagnóstico, evidência, proveniência e revisão humana.

Esta política transforma a prevenção de correlações espúrias e inferências indevidas em requisito de arquitetura, e não apenas em advertência editorial.