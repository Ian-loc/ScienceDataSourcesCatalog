# Governança do projeto

## Finalidade

O Science Data Sources Catalog é um projeto científico contínuo de descoberta, descrição e comparação de fontes de dados com prioridade para o Brasil. Sua direção de longo prazo é evoluir, de forma controlada, para o **Simbioscópio**: uma plataforma federada capaz de explorar interdependências entre sociedade, saúde, economia, governança, território e natureza.

A governança preserva rastreabilidade, revisão factual, limites de inferência e separação entre dados canônicos, artefatos derivados, documentação operacional e hipóteses científicas.

## Autoridade

A autoridade canônica é composta por:

1. branch `main` do repositório;
2. `data/data_resources.csv` para o catálogo de fontes;
3. `data/data_products.csv` e `data/product_distributions.csv` para produtos e acessos;
4. contratos de esquema e validadores executáveis;
5. [Direção científica do projeto](PROJECT_SCIENTIFIC_DIRECTION.md);
6. políticas científicas e operacionais versionadas em `docs/policies/`;
7. releases identificadas e histórico de pull requests.

Em caso de divergência, os arquivos canônicos validados em `main` prevalecem sobre planilhas, cópias locais, documentos históricos e conversas de trabalho. A direção científica e as políticas normativas prevalecem sobre conveniência de interface ou velocidade de expansão.

## Estado de transição

O esquema 0.7.0 permanece canônico para fontes. Novas entidades científicas — variáveis, passaportes, comparabilidade, relações, evidências, linhagem e receitas — devem ser introduzidas inicialmente em contratos e tabelas paralelas.

Nenhuma migração destrutiva do catálogo atual pode ocorrer sem:

- contrato versionado;
- plano de migração;
- casos de teste;
- validação automatizada;
- inspeção científica;
- preservação de IDs e proveniência;
- decisão explícita do responsável científico.

## Artefatos derivados

São derivados:

- JSONs da interface;
- metadados de build;
- website publicado;
- planilha nativa e arquivo XLSX no Google Drive;
- relatórios, perfis, mapas ou visualizações produzidos a partir do catálogo;
- avaliações automáticas ainda não revisadas;
- produtos analíticos gerados por receitas.

Derivados devem registrar, quando aplicável, versão, commit-fonte, data de geração, entradas, parâmetros, código, limitações e teto de inferência. Eles não constituem uma segunda fonte de edição.

## Papéis

### Responsável científico e mantenedor

- define escopo e critérios de inclusão;
- decide interpretações científicas;
- aprova mudanças canônicas, políticas e releases;
- responde pela identidade, autoria e citação do projeto;
- aprova qualquer atribuição de inferência causal;
- decide quando uma extensão experimental pode tornar-se pública.

### Contribuidores

- apresentam evidências e propostas rastreáveis;
- limitam alterações ao escopo declarado;
- executam ou documentam validações;
- não tratam CI verde como prova de verdade factual externa;
- distinguem observação, hipótese, associação, mecanismo e causalidade;
- registram evidência contraditória quando relevante.

### Revisores especializados

A ampliação para saúde, sociedade, economia e governança exige revisão interdisciplinar. Conforme o conteúdo, devem ser envolvidos especialistas em:

- saúde pública e epidemiologia;
- estatística espacial, temporal e causal;
- ciências sociais e antropologia;
- economia, finanças e políticas públicas;
- ética, privacidade e proteção de dados;
- ecologia, clima, agricultura e sistemas naturais.

### Automação

- valida estrutura, contratos e consistência;
- gera artefatos derivados;
- sinaliza incompatibilidades e riscos;
- publica somente o artefato público permitido;
- não decide elegibilidade científica;
- não altera silenciosamente valores canônicos;
- não atribui N5 nem causalidade sem revisão humana.

## Ciclo de mudança

Uma mudança canônica deve percorrer:

1. identificação da necessidade;
2. evidência e proposta explícita;
3. branch dedicada;
4. alteração dos arquivos-fonte;
5. validação automática e inspeção científica;
6. pull request;
7. integração em `main`;
8. regeneração dos derivados;
9. registro em changelog e, quando aplicável, release.

Mudanças científicas, estruturais, executáveis ou públicas devem declarar impacto sobre comparabilidade, proveniência, ética e inferência.

## Decisões científicas e técnicas

Decisões duradouras devem ser registradas em documentação estável, contrato de esquema, issue, pull request ou registro de decisão. Logs de sessão, tentativas temporárias e falhas operacionais podem ser arquivados, mas não devem dominar a documentação pública.

A [Direção científica do projeto](PROJECT_SCIENTIFIC_DIRECTION.md) define missão, escopo e arquitetura de longo prazo. O [roadmap do Simbioscópio](roadmap/SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md) define a ordem de execução. A [auditoria de transição](audits/SCIENTIFIC_DIRECTION_TRANSITION_AUDIT_2026-08-04.md) registra lacunas e prioridades.

### Comparabilidade, evidência e inferência

A [Política de comparabilidade, evidência e inferência científica](policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md) é normativa para o Explorador Federado, a futura interface Simbioscópio, receitas de integração e qualquer produto derivado.

Nenhuma funcionalidade pode tratar sobreposição como harmonização, correlação como mecanismo ou associação como causalidade sem os controles, metadados, diagnósticos, evidências e níveis de revisão definidos nessa política. Mudanças de interface, esquema, API ou processamento não podem enfraquecer silenciosamente avisos, bloqueios ou limites de inferência.

### Saúde, dados sociais e privacidade

Antes de incorporar microdados, pequenas contagens ou informações potencialmente sensíveis, o projeto deverá estabelecer política específica para:

- minimização de dados;
- agregação e supressão;
- risco de reidentificação;
- estigmatização territorial;
- populações vulneráveis;
- bases legais e termos de uso;
- retenção e descarte;
- revisão ética quando aplicável.

## Auditorias

Auditorias são evidência de controle de qualidade, não componentes da interface pública. Devem informar:

- escopo;
- data;
- método;
- evidências consultadas;
- achados;
- correções aceitas;
- limitações e pendências.

Achados não alteram automaticamente os dados canônicos. Avaliações automáticas de comparabilidade ou evidência permanecem rascunhos até revisão exigida pela política.

## Segurança editorial

O GitHub Pages publica apenas arquivos copiados para `_site`. Scripts, workflows, matrizes de migração, auditorias e documentação interna permanecem acessíveis no repositório, mas não são incluídos no artefato do website, salvo decisão explícita de publicação.
