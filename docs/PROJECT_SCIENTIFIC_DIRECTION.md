# Direção científica do projeto

**Status:** decisão estratégica e científica do projeto  
**Nome de trabalho da interface:** **Simbioscópio**  
**Assinatura:** **A vida acontece em relação.**  
**Princípio científico complementar:** **As relações precisam ser investigadas com evidência.**

## 1. Decisão central

O projeto evolui de um catálogo de fontes de dados para uma plataforma federada de descoberta, acesso, visualização e investigação de interdependências entre fenômenos naturais, sociais, sanitários, econômicos, institucionais e territoriais.

O catálogo atual permanece como fundamento canônico. A nova direção não elimina a arquitetura existente; acrescenta camadas científicas e computacionais que permitam compreender o que cada produto representa, quando produtos podem ser comparados e quais afirmações são sustentadas pelas evidências disponíveis.

## 2. Objeto científico

O objeto central deixa de ser apenas a fonte ou o dataset isolado e passa a incluir as relações entre:

- sistemas naturais, processos bióticos e abióticos;
- saúde humana, animal, vegetal e ecossistêmica;
- pessoas, populações, famílias e comunidades;
- instituições, políticas públicas e capacidade estatal;
- governança, participação social e articulação política;
- economia, finanças, renda, trabalho e desigualdade;
- agricultura, sistemas alimentares e segurança alimentar;
- clima, território, uso da terra e infraestrutura;
- produção, distribuição e acesso a recursos, serviços, informação e conhecimento.

Esses domínios não constituem compartimentos independentes. A plataforma deve permitir que sejam investigados como componentes de sistemas interdependentes, sem presumir que toda coocorrência represente associação válida ou causalidade.

## 3. Missão

> Organizar e conectar dados científicos sobre o Brasil para tornar exploráveis as interdependências entre sociedade, saúde, economia, governança, território e natureza, preservando proveniência, comparabilidade, evidência, incerteza e limites de inferência.

## 4. Papel do Simbioscópio

O Simbioscópio é o nome de trabalho da interface científica que deverá permitir:

1. localizar fontes, produtos, variáveis e formas de acesso;
2. visualizar produtos de diferentes provedores sem perder autoria e proveniência;
3. avaliar se uma combinação é tecnicamente comparável para uma operação específica;
4. mostrar mecanismos propostos, evidências favoráveis, discordâncias e lacunas;
5. distinguir composição visual, coocorrência, associação, mecanismo e causalidade;
6. gerar produtos e análises somente por operações documentadas e reproduzíveis;
7. comunicar de forma explícita o teto de inferência de cada resultado.

A versão atual do Explorador Federado constitui o fundamento técnico inicial do Simbioscópio e permanece limitada a composição visual de nível N0.

## 5. Arquitetura científica do produto

A evolução passa a reconhecer, além de fonte, produto e distribuição, as seguintes unidades:

```text
Fonte ou infraestrutura
  └── Produto, série ou coleção
        └── Distribuição, serviço ou ativo
              └── Variável, indicador, banda ou classe
                    └── Passaporte científico

Variável A ── relação proposta ── Variável B
                 ├── mecanismo
                 ├── evidências
                 ├── discordâncias
                 ├── confundidores e mediadores
                 ├── comparabilidade operacional
                 └── teto de inferência
```

## 6. Escopo temático

A taxonomia futura deverá ser multidimensional e permitir, no mínimo, os seguintes eixos:

- ambiente e sustentabilidade;
- natureza, biodiversidade e processos ecológicos;
- clima e riscos;
- água, solo, atmosfera e geociências;
- saúde e Saúde Única;
- população, demografia e epidemiologia;
- sociedade, desigualdade e condições de vida;
- instituições, governança e políticas públicas;
- participação social e articulação política;
- economia, finanças públicas e trabalho;
- agricultura, alimentação e sistemas produtivos;
- educação, conhecimento e acesso à informação;
- território, infraestrutura e planejamento.

Uma variável poderá pertencer a múltiplos eixos. A taxonomia não deverá forçar fenômenos interdisciplinares a uma única categoria.

## 7. Princípios científicos permanentes

1. A realidade é relacional, mas dados distintos não são automaticamente comparáveis.
2. Sobreposição cartográfica não constitui harmonização.
3. Correlação não demonstra mecanismo ou causalidade.
4. Produtos derivados da mesma fonte não constituem evidências independentes.
5. Escala espacial, período, população, método e unidade fazem parte do significado do dado.
6. Evidência favorável e contraditória devem permanecer visíveis.
7. A ausência de metadados deve reduzir a operação permitida, nunca ser preenchida por suposição.
8. Quanto mais forte a afirmação, maiores os requisitos de diagnóstico, evidência e revisão humana.
9. Dados sociais e de saúde exigem avaliação ética, privacidade e proteção contra reidentificação.
10. A plataforma apoia investigação e decisão; não substitui desenho de pesquisa nem julgamento científico.

A aplicação operacional desses princípios é definida na [Política de comparabilidade, evidência e inferência científica](policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md).

## 8. Continuidade com o catálogo atual

O catálogo atual permanece:

- fonte canônica de descoberta de infraestruturas;
- registro de produtos e distribuições já curados;
- interface pública estável;
- ponto de acesso às fontes autoritativas;
- base para construção progressiva dos passaportes científicos.

Não serão realizadas alterações destrutivas no esquema 0.7.0. Novas entidades serão introduzidas em tabelas e contratos paralelos, validadas antes de qualquer migração canônica.

## 9. Produtos futuros

A direção autoriza, de forma progressiva:

- catálogo de variáveis e indicadores;
- perfis territoriais socioecológicos;
- explorador de Saúde Única;
- mapas de interdependências;
- fichas de evidência e mecanismos;
- semáforo de comparabilidade;
- laboratório de nexos e análises reproduzíveis;
- pacotes territoriais com proveniência;
- API para descoberta e avaliação de compatibilidade.

Esses produtos somente poderão ser publicados quando cumprirem os requisitos de comparabilidade, proveniência, evidência e segurança definidos pela governança.

## 10. Limites de identidade e comunicação

O nome geral definitivo do projeto permanece sujeito a decisão posterior. **Simbioscópio** é adotado como nome de trabalho da interface de exploração das interdependências.

O projeto não deve se apresentar como:

- repositório integral de todos os dados externos;
- certificador universal da qualidade das fontes;
- mecanismo automático de descoberta causal;
- substituto das instituições produtoras;
- sistema governamental oficial;
- ferramenta que transforma qualquer combinação de variáveis em resultado científico válido.

## 11. Regra de evolução

Toda nova funcionalidade deverá responder, antes da implementação:

1. qual objeto científico representa;
2. quais metadados exige;
3. qual operação autoriza;
4. qual risco de relação espúria introduz;
5. como preserva proveniência;
6. quais evidências sustentam a relação apresentada;
7. qual é o teto de inferência;
8. qual revisão humana permanece obrigatória.

A direção científica prevalece sobre conveniência de interface, velocidade de expansão ou disponibilidade isolada de tecnologia.