# Roadmap de implementação do Simbioscópio

**Status:** roadmap governado da nova direção científica  
**Princípio:** **A vida acontece em relação. As relações precisam ser investigadas com evidência.**

## 1. Objetivo

Transformar progressivamente o catálogo atual em uma plataforma federada capaz de descobrir, visualizar e investigar interdependências entre sociedade, saúde, economia, governança, território e natureza, sem produzir comparações ou inferências cientificamente indevidas.

O roadmap preserva o catálogo 0.7.0 e introduz novos componentes em paralelo. Cada fase possui um portão de saída; a fase seguinte não deve ser tratada como consolidada antes do cumprimento do portão anterior.

## 2. Regras de execução

1. Nenhuma migração destrutiva do CSV canônico.
2. Novas entidades começam como contratos e tabelas paralelas.
3. Toda funcionalidade analítica deve declarar operação e teto de inferência.
4. CI deve bloquear regressões em controles científicos.
5. Dados sensíveis exigem governança ética antes de ingestão.
6. Backend será introduzido apenas quando a operação exigir.
7. Identidade visual não deve preceder contratos científicos fundamentais.

## Fase 0 — consolidação normativa e arquitetura de transição

### Entregas

- direção científica formal;
- política de comparabilidade e inferência;
- auditoria integral do projeto;
- contratos iniciais de passaporte, comparabilidade e evidência;
- nível N0 explícito no explorador atual;
- links públicos para a política;
- validador de integridade da direção.

### Portão de saída

- documentos normativos integrados à governança;
- CI valida contratos e limites atuais;
- nenhuma função analítica é oferecida no explorador N0;
- backlog P0 registrado.

## Fase 1 — catálogo de variáveis e passaportes científicos

### Objetivo

Representar o significado científico de cada variável, indicador, banda, classe ou métrica.

### Entregas

- tabela `variables`;
- tabela `product_variables`;
- tabela ou documento `scientific_passports`;
- vocabulário multidimensional de domínios;
- unidades normalizadas;
- perfis espaciais e temporais;
- registro de método, incerteza e limitações;
- página pública de busca por variável;
- casos dourados de variáveis ambientais, sociais, econômicas, de saúde e governança.

### Casos piloto recomendados

1. cobertura e uso da terra;
2. estoque de carbono;
3. renda e desigualdade;
4. segurança alimentar;
5. expectativa de vida ou mortalidade agregada;
6. estrutura produtiva agrícola;
7. presença de organizações da sociedade civil;
8. infraestrutura de saúde.

### Portão de saída

- 100% das variáveis piloto possuem passaporte válido;
- unidade, população, escala, período e proveniência não dependem de texto livre ambíguo;
- produtos multivariados não herdam indevidamente uma única definição.

## Fase 2 — motor de comparabilidade

### Objetivo

Avaliar se uma combinação é adequada para uma operação específica.

### Entregas

- registro `comparability_assessments`;
- regras A–E;
- avaliação por dimensão;
- operações controladas: composição, comparação descritiva, junção, agregação, correlação e regressão;
- recomendações de harmonização;
- bloqueios para incompatibilidades evidentes;
- relatório legível para usuários não especialistas;
- casos de teste positivos, condicionais e negativos.

### Regras mínimas

- semântica;
- população e unidade de observação;
- suporte e resolução espacial;
- período e granularidade temporal;
- método de obtenção;
- distribuição, incerteza e dados ausentes;
- proveniência e independência;
- licença, ética e privacidade.

### Portão de saída

- toda operação piloto recebe classe e justificativa;
- classe D bloqueia execução;
- classe E impede inferência e solicita metadados;
- transformações de classe B são reproduzíveis;
- classe C permanece restrita a visualização ou exploração preliminar.

## Fase 3 — linhagem, relações e Bússola de Evidências

### Objetivo

Representar como variáveis podem estar relacionadas e o que sustenta cada relação.

### Entregas

- `lineage_records` para dependência entre produtos;
- `scientific_relations`;
- `evidence_records`;
- mecanismos, mediadores e confundidores;
- evidência favorável, contrária e inconclusiva;
- avaliação separada de concordância, certeza, aplicabilidade e suporte mecanístico;
- interface da Bússola de Evidências;
- revisão humana versionada.

### Portão de saída

- produtos com origem compartilhada são identificados;
- nenhuma relação usa porcentagem única de consenso;
- evidência e discordância aparecem juntas;
- cada ficha informa população, escala e território de aplicabilidade;
- teto de inferência é derivado de regras explícitas e revisão.

## Fase 4 — perfis territoriais e módulo de Saúde Única

### Objetivo

Demonstrar utilidade pública e científica sem iniciar por análises causais complexas.

### Entregas

- perfis municipais ou regionais;
- seleção de território e período;
- painéis para natureza, saúde, sociedade, economia, produção e governança;
- módulo de Saúde Única;
- comparação descritiva com compatibilidade visível;
- exportação de fontes, versões e limitações;
- protocolo ético e de privacidade.

### Portão de saída

- perfis não confundem agregado territorial com indivíduo;
- pequenas contagens e dados sensíveis são protegidos;
- toda variável possui fonte, versão e período;
- qualquer aproximação entre indicadores é rotulada por nível de inferência.

## Fase 5 — Laboratório de Nexos

### Objetivo

Permitir análises exploratórias e confirmatórias limitadas por regras científicas.

### Entregas

- seleção explícita de exposição, resultado e covariáveis;
- registro de pergunta e hipótese;
- correlação e regressão com diagnósticos;
- autocorrelação espacial;
- estabilidade entre escalas;
- tendências temporais e defasagens;
- controle de múltiplas comparações;
- análises de sensibilidade;
- diagramas causais versionados;
- receitas e ambientes reproduzíveis.

### Portão de saída

- nenhum resultado é publicado sem relatório de diagnósticos;
- número de testes permanece registrado;
- limitações ausentes reduzem o teto de inferência;
- N5 nunca é atribuído automaticamente;
- resultados podem ser reproduzidos a partir de manifesto e código.

## Fase 6 — backend, API e processamento federado

### Objetivo

Escalar operações que não cabem de forma segura no navegador.

### Condições para iniciar

- volume ou duração inviável no cliente;
- necessidade de autenticação protegida;
- filas assíncronas;
- cache e controle de quotas;
- armazenamento temporário;
- auditoria de execuções.

### Entregas

- PostgreSQL/PostGIS;
- API do catálogo e dos passaportes;
- serviço de comparabilidade;
- registro de receitas e execuções;
- adaptadores de fontes;
- filas de processamento;
- monitoramento e segurança;
- política de retenção de resultados.

### Portão de saída

- operações são idempotentes ou versionadas;
- credenciais não aparecem no cliente ou repositório;
- falhas e custos são monitorados;
- resultados temporários têm ciclo de vida definido;
- API respeita as mesmas regras da interface.

## Fase 7 — identidade, educação e expansão

### Entregas possíveis

- marca definitiva do projeto;
- consolidação pública do nome Simbioscópio;
- modo **Simbionauta** com percursos guiados;
- materiais didáticos sobre correlação, causalidade e escala;
- narrativas interativas de Saúde Única;
- internacionalização;
- parcerias institucionais e revisão interdisciplinar.

## 3. Workstreams permanentes

### Dados e curadoria

- expansão Brasil-primeiro;
- verificação periódica;
- qualidade de links e licenças;
- definição de variáveis;
- linhagem e versões.

### Ciência e evidência

- critérios de relação;
- síntese de literatura;
- controvérsias;
- mecanismos;
- atualização de evidências.

### Estatística e causalidade

- diagnósticos;
- modelos espaciais e temporais;
- múltiplas comparações;
- DAGs;
- sensibilidade.

### Ética e sociedade

- privacidade;
- reidentificação;
- estigmatização territorial;
- populações vulneráveis;
- participação e governança dos dados.

### Engenharia

- contratos;
- CI;
- adaptadores;
- API;
- observabilidade;
- segurança.

### Experiência do usuário

- linguagem proporcional à evidência;
- explicações acessíveis;
- acessibilidade;
- transparência de limitações;
- prevenção de interpretação indevida.

## 4. Primeira sequência executável

1. consolidar Fase 0;
2. escolher oito variáveis piloto;
3. preencher passaportes;
4. criar dez combinações douradas, incluindo incompatibilidades;
5. implementar comparabilidade sem cálculo estatístico;
6. publicar painel de justificativas;
7. somente então testar perfis territoriais;
8. manter Laboratório de Nexos bloqueado até diagnósticos P0.

## 5. Critério de sucesso

O sucesso não será medido pelo número de camadas que podem ser sobrepostas. Será medido pela capacidade de:

- encontrar dados adequados;
- compreender o que representam;
- saber quando podem ser comparados;
- reconhecer incerteza e dependência;
- acessar evidências favoráveis e contraditórias;
- produzir resultados reproduzíveis;
- evitar afirmações mais fortes que os dados permitem.