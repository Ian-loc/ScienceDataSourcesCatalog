# Science Data Sources Catalog

**Catálogo de fontes de dados científicos sobre o Brasil e fundamento do futuro Simbioscópio.**

O projeto reúne e descreve plataformas, repositórios, redes, sistemas, produtos e formas de acesso a dados científicos, com prioridade para fontes brasileiras e para fontes internacionais com cobertura efetiva do Brasil.

Sua direção de longo prazo é evoluir para o **Simbioscópio**: uma plataforma federada capaz de explorar interdependências entre sociedade, saúde, economia, governança, território e natureza, preservando comparabilidade, evidência, incerteza, proveniência e limites de inferência.

> **A vida acontece em relação. As relações precisam ser investigadas com evidência.**

## Acessar o catálogo

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Buscar e comparar produtos](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Abrir o Simbioscópio — Explorador Federado](https://ian-loc.github.io/ScienceDataSourcesCatalog/explorer.html)
- [Analisar a composição do catálogo](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Consultar método, escopo e citação](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Código, dados e documentação](https://github.com/Ian-loc/ScienceDataSourcesCatalog)
- [Baixar o CSV canônico](data/data_resources.csv)

O catálogo é uma camada de descoberta e triagem. Ele não hospeda integralmente os datasets externos e não substitui a documentação, a licença, a versão ou a citação dos produtos originais.

## Direção científica

A nova direção amplia o objeto do projeto de **fontes de dados** para **relações investigáveis entre variáveis de diferentes campos científicos**.

O escopo futuro inclui:

- ambiente, sustentabilidade e processos naturais;
- biodiversidade, clima, água, solo e uso da terra;
- Saúde Única, saúde pública, epidemiologia e demografia;
- sociedade, desigualdade, educação e condições de vida;
- instituições, governança, participação e articulação política;
- economia, finanças públicas, trabalho e infraestrutura;
- agricultura, sistemas alimentares e segurança alimentar.

Essa ampliação não autoriza combinações indiscriminadas. Sobreposição, associação, mecanismo e causalidade são operações e afirmações distintas.

A [Direção científica do projeto](docs/PROJECT_SCIENTIFIC_DIRECTION.md) define a missão e a arquitetura de longo prazo. A [auditoria da transição](docs/audits/SCIENTIFIC_DIRECTION_TRANSITION_AUDIT_2026-08-04.md) registra o que precisa ser ajustado no projeto. O [roadmap do Simbioscópio](docs/roadmap/SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md) organiza a implementação por fases e portões de segurança.

## Simbioscópio — Explorador Federado

O Explorador Federado é o fundamento técnico inicial do Simbioscópio. Ele permite sobrepor produtos científicos de diferentes provedores, mantendo separadamente fonte, produto, período, versão, método, licença, citação e acesso original.

A versão atual implementa:

- camadas WMS e WMTS;
- controle independente de visibilidade, ordem e transparência;
- configuração compartilhável por URL;
- manifesto JSON de proveniência;
- registro de falhas de serviços externos;
- classe de compatibilidade C — composição visual;
- teto de inferência N0;
- proibição explícita de uso analítico da sobreposição.

O registro público das camadas está em `data/federated_layers.json`. Novas camadas precisam de links oficiais, citação, aviso científico e classificação de compatibilidade antes de serem publicadas.

Combinações, comparações e futuras análises são governadas pela [Política de comparabilidade, evidência e inferência científica](docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md). O projeto permite exploração visual ampla, mas exige controles progressivos antes de autorizar associação, explicação ou inferência causal.

## Escopo territorial

A curadoria segue uma orientação **Brasil primeiro**:

1. fontes brasileiras com dados sobre o país;
2. fontes internacionais com cobertura sistemática do Brasil;
3. fontes com cobertura brasileira parcial ou dependente do produto;
4. referências comparativas mantidas apenas quando possuem justificativa científica explícita.

A classificação territorial organiza descoberta e prioridade de curadoria; ela não constitui uma nota de qualidade científica.

## Modelo de dados atual e extensão futura

O catálogo atual distingue três níveis:

```text
Fonte ou infraestrutura
  └── Produto, série ou coleção
        └── Distribuição ou forma de acesso
```

Essa separação evita atribuir à infraestrutura inteira propriedades que pertencem a um produto ou acesso específico, como resolução, versão, formato, autenticação e licença.

A nova direção acrescentará progressivamente:

```text
Distribuição ou ativo
  └── Variável, indicador, banda ou classe
        └── Passaporte científico

Variável A ── relação científica ── Variável B
                 ├── comparabilidade por operação
                 ├── mecanismo e evidências
                 ├── discordâncias e limitações
                 └── teto de inferência
```

Os contratos iniciais estão em:

- `schema/scientific-variable-passport-v0.1.json`;
- `schema/comparability-assessment-v0.1.json`;
- `schema/scientific-relation-evidence-v0.1.json`.

O esquema 0.7.0 permanece canônico. As novas entidades serão testadas em paralelo antes de qualquer migração.

## Autoridade dos dados

`data/data_resources.csv` na branch `main` é a fonte canônica do catálogo de fontes.

- JSONs e metadados do site são gerados automaticamente.
- `data/data_products.csv` e `data/product_distributions.csv` mantêm a camada de produtos e acessos.
- `data/federated_layers.json` mantém o registro operacional das camadas publicadas no explorador.
- Planilhas no Google Drive são espelhos derivados e devem ser regeneradas somente após integração e validação no GitHub.
- Evidências e auditorias não alteram silenciosamente o CSV canônico.

## Curadoria e qualidade

Cada registro combina documentação oficial, documentos técnicos, literatura científica representativa e avaliação curatorial. A data de revisão indica quando o registro foi inspecionado; não certifica automaticamente todos os produtos, endpoints ou condições de uso mantidos pela fonte.

Antes de usar um dataset, confirme no produto original:

- versão e período;
- resolução e cobertura;
- metodologia e incerteza;
- licença e requisitos de atribuição;
- condições de acesso e autenticação.

Antes de combinar produtos, confirme também:

- definição das variáveis;
- população ou objeto observado;
- suporte espacial e temporal;
- independência de proveniência;
- compatibilidade metodológica;
- riscos éticos e de privacidade;
- teto de inferência permitido.

## Estrutura do repositório

- `data/`: dados canônicos, produtos, distribuições e registro de camadas federadas;
- `assets/` e arquivos HTML: interface do catálogo e do explorador;
- `scripts/`: geração e validação;
- `schema/`: contratos atuais e extensões científicas em desenvolvimento;
- `docs/`: método, direção científica, governança, políticas, roadmap e auditorias;
- `.github/workflows/`: integração contínua e publicação.

## Documentação principal

- [Direção científica do projeto](docs/PROJECT_SCIENTIFIC_DIRECTION.md)
- [Política de comparabilidade, evidência e inferência científica](docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md)
- [Auditoria da transição científica](docs/audits/SCIENTIFIC_DIRECTION_TRANSITION_AUDIT_2026-08-04.md)
- [Roadmap de implementação do Simbioscópio](docs/roadmap/SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md)
- [Metodologia](METHODOLOGY.md)
- [Dicionário de variáveis](CODEBOOK.md)
- [Política de seleção e cobertura](SELECTION_AND_COVERAGE_POLICY.md)
- [Modelo fonte–produto–distribuição](PRODUCT_CATALOG_MODEL.md)
- [Governança](docs/GOVERNANCE.md)
- [Política de releases](docs/RELEASE_POLICY.md)
- [Como contribuir](CONTRIBUTING.md)
- [Histórico de mudanças](CHANGELOG.md)

## Citação

> CLEMENTE, Ian. *Science Data Sources Catalog: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Versão 0.7.0. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318)

A citação do catálogo não substitui a citação do dataset, produto e versão originais.

## Licenças

- código: [MIT](LICENSE);
- CSV, metadados e curadoria original: [CC BY 4.0](LICENSE-DATA.md);
- fontes externas: licenças e termos próprios.
