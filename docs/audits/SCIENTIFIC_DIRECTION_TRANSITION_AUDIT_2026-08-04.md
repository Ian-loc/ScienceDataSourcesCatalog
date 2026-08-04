# Auditoria da transição para a nova direção científica

**Data:** 2026-08-04  
**Escopo:** repositório, modelo de dados, documentação, interface, governança, validações, arquitetura e comunicação pública  
**Direção auditada:** evolução do catálogo para o **Simbioscópio**, uma plataforma federada para explorar interdependências entre sociedade, saúde, economia, governança, território e natureza.

## 1. Sumário executivo

O projeto possui uma base técnica e curatorial consistente para descoberta de fontes e produtos, mas ainda não contém as estruturas necessárias para analisar interdependências científicas entre variáveis de diferentes áreas.

O estado atual é adequado para:

- registrar fontes, produtos e distribuições;
- priorizar cobertura brasileira;
- comparar metadados gerais;
- abrir formas de acesso;
- realizar composição visual federada com proveniência;
- manter dados canônicos e derivados separados.

O estado atual ainda não é suficiente para:

- representar variáveis de forma computável;
- distinguir população, unidade de observação e suporte espacial;
- avaliar comparabilidade por operação;
- rastrear dependência entre produtos derivados;
- estruturar mecanismos e evidências científicas;
- calcular ou comunicar níveis de concordância e certeza;
- executar análises estatísticas protegidas contra relações espúrias;
- tratar dados de saúde e populações vulneráveis com governança específica.

A recomendação é preservar o catálogo 0.7.0 e construir uma camada paralela de transição. Uma migração imediata do CSV canônico seria prematura e aumentaria risco de inconsistência.

## 2. Critérios de prioridade

- **P0 — requisito de segurança científica:** deve existir antes de qualquer análise conjunta automatizada.
- **P1 — requisito estrutural:** necessário para a evolução coerente do produto.
- **P2 — aprimoramento de capacidade:** importante após os fundamentos.
- **P3 — refinamento posterior:** não bloqueia as primeiras fases.

## 3. Estado por componente

| Componente | Estado atual | Lacuna principal | Prioridade |
|---|---|---|---|
| Governança científica | Política geral e governança do catálogo | Faltavam regras formais de comparabilidade e inferência | P0 |
| Identidade do projeto | Nome e texto ainda centrados em catálogo de fontes | Não expressa interdependências, Saúde Única e múltiplos domínios | P1 |
| Modelo de fonte | Estruturado e canônico | Deve permanecer, sem absorver atributos de variável | Preservar |
| Modelo de produto | Produto e distribuição implementados | Faltam ativos, variáveis, linhagem e perfis espaço-temporais | P0/P1 |
| Taxonomia temática | Predominantemente ambiental e geoespacial | Insuficiente para saúde, sociedade, economia e governança | P1 |
| Explorador federado | Composição visual C e proveniência | Teto N0 e política ainda não estavam explícitos no contrato | P0 |
| Comparabilidade | Avisos editoriais e classe C | Não existe motor de avaliação por dimensão e operação | P0 |
| Evidência científica | Evidência por fonte e documentação | Não existe ficha de relação, mecanismo ou discordância | P1 |
| Análise estatística | Não implementada | Deve nascer com diagnósticos, múltiplos testes e análise espacial | P0 antes de uso |
| Proveniência | Boa no catálogo e manifesto visual | Falta linhagem compartilhada entre variáveis e derivados | P0/P1 |
| Ética e privacidade | Não é central no escopo atual | Essencial antes de saúde, microdados e populações vulneráveis | P0 |
| Backend | Interface estática bem delimitada | Processamento e autenticação exigirão serviço intermediário | P2 |
| CI | Valida estrutura atual | Precisa validar contratos científicos e limites de inferência | P0 |
| Comunicação pública | Limites do MVP visíveis | Direção futura e distinções científicas precisam ser consolidadas | P1 |

## 4. Achados detalhados

### 4.1 Identidade e missão

**Achado:** o nome e a apresentação pública ainda descrevem principalmente um catálogo de fontes. O repositório, porém, já inclui produtos, distribuições, visualização federada e propostas de processamento.

**Risco:** a identidade estreita pode orientar decisões de arquitetura para descoberta de links, em vez de investigação de relações.

**Ajuste necessário:** adotar uma arquitetura de marca em duas camadas:

- projeto e catálogo atual, preservados durante a transição;
- **Simbioscópio**, como nome de trabalho da interface científica de interdependências.

**Estado nesta intervenção:** direção formalizada; renomeação integral do repositório adiada até decisão de marca e plano de migração de URLs.

### 4.2 Escopo científico e taxonomia

**Achado:** as áreas atuais são úteis para ecologia, ambiente, sensoriamento remoto e infraestrutura de dados, mas não cobrem adequadamente saúde, demografia, epidemiologia, instituições, finanças, economia, alimentação, desigualdade e participação social.

**Risco:** forçar novos produtos em categorias ambientais ou em palavras-chave livres, produzindo baixa consistência semântica.

**Ajustes necessários:**

1. criar taxonomia multidimensional, não exclusiva;
2. separar domínio científico, fenômeno, setor, população e finalidade;
3. permitir múltiplos domínios por variável;
4. adotar identificadores estáveis e rótulos multilíngues;
5. manter a taxonomia atual enquanto a nova não estiver validada.

### 4.3 Modelo de dados

**Achado:** o modelo fonte–produto–distribuição está correto e deve ser preservado. Ele não foi desenhado para representar significado estatístico de variáveis ou relações entre elas.

**Entidades novas necessárias:**

- `data_assets` — arquivos, endpoints, camadas e objetos acessíveis;
- `variables` — variáveis, indicadores, bandas, classes e métricas;
- `product_variables` — relação produto–variável;
- `scientific_passports` — unidade, suporte, população, método e incerteza;
- `spatiotemporal_profiles` — escala, grade, período e frequência;
- `lineage_records` — origem e dependência entre produtos;
- `comparability_assessments` — avaliação A–E por operação;
- `scientific_relations` — hipóteses, associações e mecanismos;
- `evidence_records` — estudos favoráveis, contrários e inconclusivos;
- `integration_recipes` — transformações autorizadas;
- `processing_runs` e `generated_outputs` — execuções e resultados.

**Decisão:** introduzir contratos paralelos em versão 0.1 antes de criar tabelas canônicas.

### 4.4 Passaporte científico

**Achado:** os produtos já possuem descrição, resolução, período, método e limitações em nível geral, mas não existe uma unidade padronizada por variável.

**Risco:** produtos com várias variáveis podem herdar metadados indevidos; unidades e populações incompatíveis podem ser comparadas.

**Requisito P0:** nenhuma operação analítica automática sem definição, unidade, população/objeto, suporte espacial, período, método, versão, incerteza, proveniência e limitações.

### 4.5 Explorador federado

**Achado positivo:** a interface atual executa somente composição visual, mantém classe C, impede harmonização silenciosa e exporta proveniência.

**Lacunas:**

- o teto N0 não estava formalizado no registro;
- o manifesto não identificava a política normativa;
- cada camada não declarava explicitamente proibição de uso analítico;
- a interface não apresentava o Simbioscópio como direção científica.

**Ajustes implementados nesta intervenção:** contrato do registro elevado para incluir política, N0, uso analítico proibido e estado de evidência; interface e validador atualizados.

### 4.6 Motor de comparabilidade

**Achado:** não existe avaliação automática das dimensões semântica, populacional, espacial, temporal, metodológica, estatística, de proveniência e jurídico-ética.

**Requisito P0:** o futuro motor deve avaliar a operação solicitada, e não atribuir uma qualidade universal ao par de datasets.

Exemplo: dois produtos podem ser adequados para composição visual e inadequados para correlação.

### 4.7 Relações espúrias e diagnósticos

Antes de qualquer laboratório estatístico, o sistema deverá controlar:

- tendência temporal compartilhada;
- autocorrelação espacial;
- efeito da escala e do zoneamento;
- dependência entre produtos com origem comum;
- múltiplas comparações;
- dados ausentes e seleção territorial;
- confundidores, mediadores e colisores;
- relações não lineares e defasagens;
- instabilidade entre versões e especificações;
- falácia ecológica e limites de dados agregados.

**Decisão:** nenhuma função pública de correlação deve ser adicionada antes desses controles mínimos.

### 4.8 Evidência e consenso

**Achado:** o catálogo registra evidência sobre fontes, mas não sintetiza evidência sobre relações entre variáveis.

**Ajustes necessários:**

- ficha de relação científica;
- mecanismo proposto;
- direção esperada;
- mediadores e confundidores;
- literatura favorável, contrária e inconclusiva;
- avaliação separada de concordância, certeza, aplicabilidade e suporte mecanístico;
- revisão humana e data de atualização.

**Regra:** não utilizar porcentagem única de consenso como substituto de avaliação multidimensional.

### 4.9 Saúde Única

**Oportunidade:** Saúde Única pode funcionar como um módulo integrador entre ambiente, produção, alimentação, saúde humana, saúde animal, clima e governança.

**Riscos:** mistura de escalas, inferência individual a partir de dados agregados, exposição não observada, privacidade, estigmatização territorial e reidentificação.

**Pré-condições:** protocolo ético, classificação de sensibilidade, agregação mínima, supressão de pequenas contagens e revisão especializada.

### 4.10 Governança e revisão interdisciplinar

A ampliação exige revisão que não seja exclusivamente ecológica ou computacional. Devem ser previstos papéis para:

- epidemiologia e saúde pública;
- ciências sociais e antropologia;
- economia e políticas públicas;
- estatística espacial e causal;
- ética e proteção de dados;
- especialistas nos sistemas naturais e produtivos estudados.

### 4.11 Infraestrutura

**Decisão:** preservar GitHub Pages para descoberta e composição visual. Backend deve ser introduzido somente quando houver necessidade real de:

- autenticação;
- tarefas assíncronas;
- processamento pesado;
- cache;
- controle de quotas;
- armazenamento temporário;
- auditoria de execuções.

PostgreSQL/PostGIS continua adequado ao núcleo relacional futuro. Um banco de grafos ou RDF pode ser avaliado depois que a estrutura de relações estiver validada; não é requisito inicial.

### 4.12 CI e validação

**Achado:** a CI é forte para o escopo atual, porém não validava a nova direção.

**Ajustes implementados:**

- contratos JSON de passaporte, comparabilidade e evidência;
- validador da direção científica;
- integração à CI;
- checagem de N0 e proibição de análise no explorador atual.

## 5. Intervenções realizadas nesta rodada

1. política normativa de comparabilidade, evidência e inferência;
2. documento de direção científica;
3. auditoria integral de transição;
4. roadmap de implementação do Simbioscópio;
5. três contratos JSON de base;
6. validador computacional da direção;
7. integração do validador à CI;
8. fortalecimento do registro de camadas com N0 e proibição analítica;
9. atualização do explorador e da documentação pública;
10. integração da direção ao README, metodologia, modelo de produtos e governança.

## 6. Backlog priorizado

### P0 — antes de qualquer análise conjunta

- consolidar contratos de passaporte e comparabilidade;
- criar registro de variáveis;
- implementar linhagem e dependência entre produtos;
- definir política ética e de privacidade;
- criar casos dourados de combinação A–E;
- definir diagnósticos estatísticos mínimos;
- impedir funções de correlação sem avaliação prévia.

### P1 — estrutura do primeiro Simbioscópio

- ampliar taxonomia temática;
- criar busca por variável;
- criar ficha de relação e evidência;
- implementar painel de comparabilidade;
- criar perfis territoriais multitemáticos;
- definir governança interdisciplinar.

### P2 — capacidade analítica

- adaptadores de acesso;
- receitas territoriais reproduzíveis;
- backend e filas de processamento;
- API pública;
- diagramas causais versionados;
- análises de sensibilidade.

### P3 — refinamentos

- identidade visual definitiva;
- modo Simbionauta com percursos didáticos;
- visualizações de rede avançadas;
- personalização de painéis;
- internacionalização completa.

## 7. Critérios para considerar a direção acomodada

A transição será considerada estruturalmente consolidada quando:

- toda variável analítica possuir passaporte validado;
- toda combinação receber avaliação por operação;
- a interface exibir teto de inferência;
- produtos relacionados tiverem linhagem rastreável;
- relações científicas possuírem evidência e discordância documentadas;
- análises gerarem receita, parâmetros e proveniência;
- dados sensíveis cumprirem protocolo ético;
- CI impedir regressões nos controles científicos.

## 8. Conclusão

O projeto não precisa abandonar sua base atual. A arquitetura existente é um núcleo sólido de descoberta e proveniência. A mudança necessária é adicionar uma camada científica explícita entre os dados e as interpretações.

O diferencial do Simbioscópio não deverá ser permitir o maior número possível de sobreposições. Deverá ser permitir que diferentes ciências se encontrem sem apagar diferenças de significado, escala, método, evidência e incerteza.