# Avaliação rápida pós-consolidação e início da Fase 1

**Data:** 2026-08-04  
**Escopo:** estado após o merge da direção científica do Simbioscópio  
**Resultado:** Fase 0 consolidada; Fase 1 iniciada em branch própria

## 1. Avaliação do que foi implementado

A consolidação anterior foi adequada e coerente porque:

- preservou o catálogo canônico 0.7.0;
- formalizou a direção científica e a identidade de trabalho do Simbioscópio;
- transformou comparabilidade e inferência em política normativa;
- tornou o teto N0 e a proibição de uso analítico legíveis por máquina;
- criou contratos iniciais para passaportes, comparabilidade e evidências;
- fortaleceu governança, interface e integração contínua.

A principal limitação é que os contratos ainda eram abstratos. Não existia um registro operacional de variáveis, nenhuma ficha real validada contra um produto e nenhum vínculo executável entre produto, variável e passaporte.

## 2. O que precisa ser feito agora

### Prioridade imediata

1. criar o registro versionado de variáveis;
2. relacionar variáveis a produtos específicos;
3. preencher passaportes com definição, unidade, objeto observado, suporte espacial e temporal, método, incerteza, proveniência e limitações;
4. validar automaticamente IDs, vínculos e vocabulários;
5. produzir casos dourados de comparabilidade somente depois que existirem variáveis de domínios distintos e suficientemente documentadas.

### Próximos requisitos bloqueantes

- taxonomia multidimensional estável;
- linhagem entre produtos e variáveis;
- política de privacidade e sensibilidade;
- fontes e produtos piloto de saúde, sociedade, economia e governança;
- motor de comparabilidade por operação;
- casos adversariais contra falácia ecológica, escalas incompatíveis e produtos dependentes;
- Bússola de Evidências com revisão humana.

## 3. Intervenção iniciada

A Fase 1 começa com um piloto mínimo e verificável do produto `DP000011 — Dynamic World V1`:

- `VR000001`: rótulo top-1 de cobertura da terra;
- `VR000002`: probabilidade da classe árvores;
- uma ficha de passaporte por variável;
- vínculo explícito produto–variável;
- validador executável integrado ao CI.

O piloto usa duas saídas conceitualmente diferentes do mesmo produto para testar:

- variável categórica versus contínua;
- rótulo derivado versus banda de probabilidade;
- distinção entre probabilidade de classe, acurácia e incerteza;
- proveniência comum e ausência de independência entre saídas do mesmo modelo.

## 4. Limites preservados

- registros permanecem em estado `draft` até revisão científica;
- nenhuma função analítica é liberada;
- nenhuma correlação ou relação causal é criada;
- o piloto ambiental não define a taxonomia final do projeto;
- variáveis sociais, sanitárias, econômicas e institucionais somente serão adicionadas após curadoria de fontes e produtos correspondentes;
- o catálogo de fontes e produtos existente permanece canônico.

## 5. Critério para o próximo incremento

O próximo incremento deve adicionar ao menos um produto de outro domínio com documentação suficiente e construir o primeiro caso dourado de comparabilidade. A combinação deverá permanecer bloqueada para análise até que período, suporte espacial, população, método, unidade, linhagem e limitações estejam explicitamente avaliados.
