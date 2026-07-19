# Histórico de mudanças

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
