# Histórico de mudanças

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
- mantidos todos os 34 campos e o CSV canônico sem alterações.

## Não lançado — UX3 redesenho dos cards

- reorganizada a leitura dos cards em identidade, descrição, acesso, utilidade, limitação, ações e detalhes;
- identidade oficial movida para uma linha secundária;
- adicionados estados semânticos para download, API e cobertura do Brasil;
- utilidade acadêmica e principal limitação passam a aparecer antes dos detalhes técnicos;
- ação `Acessar dados` priorizada em relação aos links auxiliares;
- detalhes agrupados em Acesso, Cobertura, Produtos e dados, Uso acadêmico, Evidências e Avaliação e governança;
- preservados todos os campos e links do esquema atual;
- CSV canônico mantido sem alterações.

## Não lançado — UX2 filtros e resultados

- separados filtros essenciais e avançados;
- adicionadas contagens por opção de filtro;
- adicionados filtros avançados por cobertura, formato e tipo de evidência;
- adicionados filtros ativos removíveis;
- adicionada ordenação por relevância, nome e verificação mais recente;
- busca, filtros e ordenação passam a ser representados na URL;
- seleção por área passa a indicar estado ativo;
- ampliada a validação estrutural para os novos controles.

## Não lançado — UX1 e preparação documental

- adotado o título oficial **Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão**;
- reorganizada a página inicial para apresentar busca, benefício e exploração temática antes da lista completa;
- criada navegação consistente entre catálogo, análise e documentação;
- adicionados atalhos de busca e exploração dinâmica pelas áreas de pesquisa;
- revisados rótulos de busca, filtros, indicadores e detalhes técnicos;
- reduzida a competição entre ações no hero e refinada a hierarquia visual;
- adicionado ORCID do autor ao `CITATION.cff`, preservando a versão 0.7.0;
- criada `LICENSE-DATA.md` para separar CC BY 4.0 da licença MIT do código;
- criado workflow explícito para UX, revisão científica, release estável e DOI;
- adicionadas validações automáticas da estrutura HTML e da sintaxe JavaScript;
- mantidos `v1.0.0` e DOI bloqueados até o fechamento técnico, científico e documental.

## Não lançado — fechamento operacional

- adicionada identificação verificável do build com versão, commit, data, número de fontes e número de variáveis;
- versão e commit publicados passam a ser exibidos no catálogo e na página Sobre;
- adicionada proteção contra versionamento acidental do JSON e dos metadados derivados;
- criado `WORKFLOW_STATUS.md` para registrar backlog, estados e critérios de conclusão enquanto GitHub Issues permanecer desativado;
- alinhamento final com o Google Drive condicionado à validação, integração e publicação deste ciclo.

## 0.7.0 — 2026-07-18

- cruzada a documentação oficial com evidência acadêmica ou técnica representativa;
- adicionadas 38 evidências de artigos revisados por pares, dois artigos técnicos e 11 documentos oficiais/técnicos;
- condensados os temas em nove áreas de pesquisa inspiradas em CAPES e Web of Science;
- preservadas palavras-chave específicas para busca;
- separado acesso programático de download e de API REST;
- adicionados protocolos, autenticação, visualizações e cobertura do Brasil;
- criada página analítica com gráficos do acervo;
- criada página Sobre com escopo, método e forma de citação;
- adicionados metodologia, dicionário de variáveis e CITATION.cff;
- ampliado o esquema de 26 para 34 variáveis.

## 0.6.0 — 2026-07-18

- definido o CSV do GitHub como única fonte canônica;
- removida a sincronização manual com a planilha do Drive;
- ampliado o esquema de 22 para 26 variáveis;
- substituída a classificação normalizada por identidade autodeclarada;
- revisadas as 51 fontes, utilidades e limitações;
- corrigidos links e dados de acesso;
- incluída validação automática e geração do JSON.
