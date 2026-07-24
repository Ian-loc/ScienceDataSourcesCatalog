# Histórico de mudanças

## Não lançado — escopo Brasil-primeiro

- definido o Brasil como escopo territorial central do catálogo;
- criada classificação curatorial P0–P3 para todas as 51 fontes, sem alterar o CSV canônico 0.7.0;
- adicionada ordenação padrão que apresenta primeiro fontes brasileiras e depois fontes internacionais com cobertura sistemática do Brasil;
- adicionados filtro territorial, atalhos, indicadores públicos e marcas de prioridade nos cards;
- adicionados detalhes de origem da fonte e papel no catálogo;
- criada validação automática da cobertura integral dos 51 `resource_id` pela política territorial;
- fortalecida a política de seleção para exigir vínculo com o Brasil ou justificativa estratégica explícita;
- reordenada a fila de candidatos, reduzindo a prioridade de agregadores globais gerais;
- adicionadas oito infraestruturas brasileiras de alta prioridade: Brazil Data Cube, SNIF, Flora e Funga do Brasil, GeoInfo Embrapa, SIAGAS, SiMCosta, SEEG e PPBio;
- preservados o bloqueio de inclusões automáticas, a versão 0.7.0 e os portões de DOI.

## Não lançado — correções factuais e escala visual

- corrigidos 11 registros com divergências confirmadas em autenticação, API, licença ou condições de acesso;
- registradas as fontes oficiais em `data/factual_corrections_2026-07-23.json`;
- redefinida a apresentação de `last_verified` como data de revisão do registro, não certificação integral;
- adicionada advertência pública sobre variabilidade por produto e distribuição;
- reduzida moderadamente a escala tipográfica e o tamanho máximo dos títulos;
- preservados número de fontes, esquema 0.7.0 e bloqueio do DOI.

## Não lançado — UX6 descoberta e comparação de produtos

- criada página pública separada para produtos, preservando a diferença entre fonte, produto e distribuição;
- integrado o piloto de 10 produtos ou famílias e 15 distribuições de TerraBrasilis e Google Earth Engine;
- adicionada geração automática de `data/data_products.json` com identidade da fonte e formas de acesso aninhadas;
- adicionada busca textual com sinônimos em português e inglês;
- adicionados filtros compartilháveis por fonte, área, Brasil, tipo, formato, protocolo, autenticação, estado e origem;
- adicionada comparação lado a lado de dois ou três produtos;
- expostas resolução, cobertura, versão, limitações, metodologia e distribuições específicas;
- ampliados testes de integridade, acessibilidade, orçamento de peso e artefatos publicáveis;
- atualizado workflow do GitHub Pages para `upload-pages-artifact@v4` e validação explícita dos artefatos;
- preservados CSV canônico de fontes 51 × 34, versão 0.7.0 e bloqueio do DOI.

## Não lançado — identidade pública e URL canônica

- consolidado o nome **Science Data Sources Catalog** após a renomeação do repositório;
- atualizados página inicial, análise, página Sobre, README e metadados de citação;
- substituídas URLs do repositório e do GitHub Pages que ainda apontavam para `ecology-data-catalog`;
- adicionada validação automática contra regressões do nome e das URLs públicas;
- preservados CSV canônico com 51 fontes × 34 campos, versão 0.7.0, workflow W1A e bloqueio do DOI.

## Não lançado — objetivos finais, prontidão para DOI e DATA1-BR

- definido o produto final como catálogo científico de fontes, com unidade de registro `source`;
- estabelecidos objetivo geral, oito objetivos específicos e limites deliberados;
- definida a completude científica mínima de cada registro;
- criados 12 portões obrigatórios antes do DOI;
- criado contrato legível por máquina em `release/doi_readiness.json`;
- organizado o DATA1-BR em cinco lotes de sete registros;
- adicionado `scripts/validate_doi_readiness.py` ao GitHub Actions;
- preservados CSV com 51 fontes × 34 campos, versão 0.7.0 e bloqueio do DOI.

## Não lançado — DATA1-B matriz de migração

- criada matriz explícita para os 51 `resource_id`, sem duplicar os campos atuais do CSV;
- propostas classificações para `resource_type` e `geographic_scope` em todos os registros;
- propostas normalizações de formatos, protocolos, ferramentas e situação institucional;
- mantidas vazias as URLs de orientação de citação até confirmação oficial específica;
- classificadas 24 decisões como alta confiança e 27 como confiança média;
- separados 16 registros prontos para futura migração e 35 dependentes de revisão manual;
- nenhuma decisão de baixa confiança foi aceita;
- adicionadas exceções codificadas para recursos híbridos e valores `other_documented`;
- criado `scripts/validate_migration_matrix.py` para conferir a matriz contra o CSV e o contrato 0.8.0;
- CSV canônico permanece com 51 fontes e 34 campos; versão formal permanece 0.7.0.

## Não lançado — DATA1 auditoria do esquema 0.8.0

- auditados os 34 campos e as 51 fontes antes de qualquer migração;
- documentada a separação entre identidade oficial e função controlada do recurso;
- proposta evolução mínima de 34 para 38 campos;
- propostos `resource_type`, `geographic_scope`, `access_tools` e `citation_guidance_url`;
- definidos vocabulários preliminares para tipos, escala, formatos, protocolos, ferramentas, origem e situação institucional;
- classificada preliminarmente a função principal e a escala geográfica das 51 fontes;
- definidas 14 regras de validação cruzada e uma sequência de migração atômica;
- criado contrato legível por máquina em `schema/v0.8.0-draft.json`;
- criado teste que impede alteração prematura do CSV e exige a preservação das 51 fontes e 34 campos durante a auditoria;
- versão formal permanece 0.7.0; DOI continua bloqueado.

## Não lançado — UX4 acessibilidade, responsividade e desempenho

- reforçados landmarks, fieldsets, títulos associados e nomes acessíveis;
- adicionados estados de carregamento e anúncios para resultados e gráficos;
- adicionados foco previsível após busca e remoção de filtros;
- links externos passam a informar abertura em nova aba;
- adicionados fallbacks úteis para uso sem JavaScript;
- adicionada camada específica para leitores de tela, alto contraste e movimento reduzido;
- refinados layouts em larguras intermediárias e móveis;
- adicionados testes de estrutura semântica, dependências externas e orçamento de peso;
