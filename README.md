# Science Data Sources Catalog - Catálogo de fontes de dados científicos
# Dados científicos para pesquisa, ensino e extensão

Catálogo público e pesquisável de plataformas, repositórios, redes, sistemas, produtos e formas de acesso para ecologia, biodiversidade, clima, carbono, solos, vegetação e temas relacionados.

## Produto

- [Buscar fontes](https://ian-loc.github.io/ScienceDataSourcesCatalog/#catalogo)
- [Buscar e comparar produtos](https://ian-loc.github.io/ScienceDataSourcesCatalog/products.html)
- [Analisar o catálogo](https://ian-loc.github.io/ScienceDataSourcesCatalog/analytics.html)
- [Sobre, método e citação](https://ian-loc.github.io/ScienceDataSourcesCatalog/about.html)
- [Código, dados e documentação](https://github.com/Ian-loc/ScienceDataSourcesCatalog)
- [CSV canônico de fontes](data/data_resources.csv)
- [CSV de produtos](data/data_products.csv)
- [CSV de distribuições](data/product_distributions.csv)

O catálogo é uma camada de descoberta e triagem. Não hospeda os datasets externos nem substitui documentação, licença ou citação dos produtos originais.

> **Nota de verificação:** `last_verified` registra a revisão do registro. Não deve ser interpretado como certificação integral de todos os produtos, versões, licenças ou endpoints externos.

## Fonte única e artefatos derivados

`data/data_resources.csv` é a única fonte canônica do catálogo de fontes. Os JSONs do site são gerados no workflow. A planilha nativa e o `.xlsx` do Google Drive são espelhos derivados; não constituem uma segunda fonte de edição ou publicação. O `project_changelog` do Drive mantém o registro executivo.

A versão 0.7.0 reúne 51 fontes e 34 campos. A proposta 0.8.0 acrescenta quatro campos, mas ainda não foi aplicada. A planilha nativa foi verificada com os 34 campos canônicos. O `.xlsx` permanece histórico, com 22 campos, até substituição e nova verificação.

## Camada fonte → produto → distribuição

A camada de produtos evita confundir uma infraestrutura com os datasets e serviços que ela oferece:

```text
Fonte / infraestrutura
  1 ─── N Produto ou série
              1 ─── N Distribuição ou forma de acesso
```

O piloto atual contém 10 produtos ou famílias e 15 distribuições ligadas a TerraBrasilis e Google Earth Engine. A página de produtos oferece:

- busca textual com sinônimos em português e inglês;
- filtros por fonte, área, cobertura do Brasil, tipo, formato, protocolo, autenticação, estado e origem;
- URLs compartilháveis para buscas filtradas;
- comparação lado a lado de dois ou três produtos;
- exposição de resolução, versão, cobertura, limitações e formas de acesso.

O modelo e suas regras científicas estão em [PRODUCT_CATALOG_MODEL.md](PRODUCT_CATALOG_MODEL.md).

## Estado da curadoria

- 16 registros estão preparados estruturalmente para futura migração;
- 35 registros concluíram auditoria interna e permanecem sujeitos à revisão factual externa antes de correções canônicas;
- BR1–BR5 cobrem os 35 casos de revisão manual;
- Project COSMOS permanece no catálogo principal como infraestrutura bibliométrica, sem ser apresentado como fonte direta de medições ambientais;
- 17 fontes candidatas foram consideradas elegíveis para futura inclusão controlada;
- SINITOX permanece pendente por indisponibilidade do portal durante a verificação;
- nenhuma fonte candidata é inserida silenciosamente no CSV 0.7.0;
- v1.0.0 e DOI permanecem bloqueados.

Recursos bibliométricos podem ser elegíveis quando oferecem dados ou metadados estruturados, metodologia, governança e utilidade ambiental distinta. Eles não devem ser apresentados como substitutos de fontes ambientais primárias. A decisão detalhada de COSMOS está em [G0_COSMOS_SCOPE_DECISION.md](G0_COSMOS_SCOPE_DECISION.md).

## Atualização

1. use documentação oficial atual e literatura representativa;
2. registre evidências em `migration/external_review_evidence.csv`;
3. atualize fila, proposta e decisão;
4. altere o CSV somente em ciclo autorizado e revisado;
5. execute a suíte de validação;
6. abra pull request, confirme CI e registre o merge no Drive;
7. regenere os JSONs e espelhos somente a partir de um commit validado de `main`;
8. não declare um espelho sincronizado sem verificar cabeçalhos, IDs e valores.

## Documentação

- [Estado atual](WORKFLOW_STATUS.md)
- [Workflow de implementação](IMPLEMENTATION_WORKFLOW.md)
- [Workflow de qualidade](QUALITY_CORRECTION_WORKFLOW.md)
- [Modelo do catálogo de produtos](PRODUCT_CATALOG_MODEL.md)
- [Decisão G0 do Project COSMOS](G0_COSMOS_SCOPE_DECISION.md)
- [Contrato de espelhamento do Drive](DRIVE_MIRROR_CONTRACT.md)
- [Auditoria de consistência documental](DOCUMENTATION_CONSISTENCY_AUDIT.md)
- [Metodologia](METHODOLOGY.md)
- [Codebook](CODEBOOK.md)
- [Workflow de auditoria](AUDIT_WORKFLOW.md)
- [Política de seleção](SELECTION_AND_COVERAGE_POLICY.md)
- [Objetivos e portões de DOI](FINAL_OBJECTIVES_AND_DOI_GATES.md)

## Como citar

> LARA, Ian. *Science Data Sources Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Versão 0.7.0. GitHub, 2026. https://ian-loc.github.io/ScienceDataSourcesCatalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318). A citação do catálogo não substitui a citação do dataset, produto e versão originais.

## Licenças

- código: MIT;
- CSV, metadados e curadoria original: CC BY 4.0;
- fontes externas: licenças e termos próprios.

A futura release será arquivada como **Dataset** somente após os portões G1–G12.
