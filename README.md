# Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão

Catálogo público e pesquisável de plataformas, repositórios, redes e sistemas para ecologia, biodiversidade, clima, carbono, solos, vegetação e temas relacionados.

## Produto

- [Buscar fontes](https://ian-loc.github.io/ecology-data-catalog/#catalogo)
- [Analisar o catálogo](https://ian-loc.github.io/ecology-data-catalog/analytics.html)
- [Sobre, método e citação](https://ian-loc.github.io/ecology-data-catalog/about.html)
- [CSV canônico](data/data_resources.csv)

O catálogo é uma camada de descoberta e triagem. Não hospeda os datasets externos nem substitui documentação, licença ou citação dos produtos originais.

## Fonte única

`data/data_resources.csv` é a única fonte canônica. O JSON do site é gerado no workflow. A planilha nativa e o `.xlsx` do Google Drive são espelhos derivados e históricos; não constituem uma segunda fonte de edição ou publicação. O `project_changelog` do Drive mantém o registro executivo.

A versão 0.7.0 reúne 51 fontes e 34 campos. A proposta 0.8.0 acrescenta quatro campos, mas ainda não foi aplicada. Os espelhos históricos de 22 campos não devem ser usados para avaliar a completude da versão atual.

## Estado da curadoria

- 16 registros estão preparados estruturalmente para futura migração;
- 35 registros permanecem em revisão manual;
- BR1–BR5 concluíram a auditoria interna desses 35 casos;
- a revisão externa usa fila separada e evidências por afirmação;
- nenhuma correção externa é aplicada automaticamente ao CSV;
- 18 candidatos permanecem fora do catálogo;
- v1.0.0 e DOI estão bloqueados.

## Atualização

1. use documentação oficial atual e literatura representativa;
2. registre evidências em `migration/external_review_evidence.csv`;
3. atualize fila, proposta e decisão;
4. altere o CSV somente em ciclo autorizado e revisado;
5. execute a suíte de validação;
6. abra pull request, confirme CI e registre o merge no Drive;
7. regenere os espelhos somente a partir de um commit validado de `main`.

## Documentação

- [Estado atual](WORKFLOW_STATUS.md)
- [Workflow de implementação](IMPLEMENTATION_WORKFLOW.md)
- [Workflow de qualidade](QUALITY_CORRECTION_WORKFLOW.md)
- [Contrato de espelhamento do Drive](DRIVE_MIRROR_CONTRACT.md)
- [Auditoria de consistência documental](DOCUMENTATION_CONSISTENCY_AUDIT.md)
- [Metodologia](METHODOLOGY.md)
- [Codebook](CODEBOOK.md)
- [Workflow de auditoria](AUDIT_WORKFLOW.md)
- [Política de seleção](SELECTION_AND_COVERAGE_POLICY.md)
- [Objetivos e portões de DOI](FINAL_OBJECTIVES_AND_DOI_GATES.md)

## Como citar

> LARA, Ian. *Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão*. Versão 0.7.0. GitHub, 2026. https://ian-loc.github.io/ecology-data-catalog/

ORCID: [0000-0003-1164-9318](https://orcid.org/0000-0003-1164-9318). A citação do catálogo não substitui a citação do dataset, produto e versão originais.

## Licenças

- código: MIT;
- CSV, metadados e curadoria original: CC BY 4.0;
- fontes externas: licenças e termos próprios.

A futura release será arquivada como **Dataset** somente após os portões G1–G12.
