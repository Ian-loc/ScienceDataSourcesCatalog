# Política de releases

## Objetivo

Releases transformam o estado contínuo do catálogo em versões identificáveis, citáveis e reproduzíveis. O site pode continuar evoluindo entre releases, mas toda citação deve indicar uma versão ou commit verificável.

## Versionamento

O projeto utiliza versionamento semântico:

- **patch** (`0.7.1`): correções factuais, editoriais, de interface ou validação sem mudança incompatível de esquema;
- **minor** (`0.8.0`): novos campos, recursos ou mudanças compatíveis que exigem migração documentada;
- **major** (`1.0.0`): primeira versão científica estável com critérios de completude e governança formalmente atendidos.

## Requisitos mínimos

Toda release deve incluir:

1. dados canônicos validados;
2. artefatos derivados regenerados a partir do commit da release;
3. changelog consolidado;
4. `CITATION.cff` coerente;
5. interface funcional e artefato Pages inspecionado;
6. licenças e documentação pública coerentes;
7. tag anotada e release no GitHub.

## Patch releases

Patch releases podem incluir:

- correção de links;
- atualização de metadados factuais;
- novas fontes no esquema vigente;
- correção de identidade, autoria ou citação;
- melhoria de acessibilidade e apresentação;
- correção ou ampliação de testes;
- higiene de repositório e publicação.

A inclusão de uma fonte nova deve preservar o esquema, passar pelos validadores e atualizar classificações vinculadas.

## Minor releases

Uma minor release exige:

- contrato de esquema atualizado;
- plano de migração;
- compatibilidade documentada;
- codebook e metodologia atualizados;
- migração integral dos registros;
- atualização coordenada da interface, scripts e espelhos.

## Major release e DOI

A versão `1.0.0` representa estabilidade científica e operacional, não o encerramento da curadoria. Um DOI deve identificar uma release imutável arquivada como dataset e não apenas a página dinâmica.

A criação do DOI exige, além dos requisitos de release:

- ausência de erros materiais conhecidos sem tratamento;
- escopo e método consolidados;
- autoria, licença e citação verificadas;
- depósito inspecionado antes da publicação;
- correspondência exata entre o arquivo arquivado e a tag da release.

## Espelhos do Google Drive

Planilhas do Drive são regeneradas após a integração em `main` e devem declarar:

- versão;
- esquema;
- commit-fonte;
- data de geração;
- dimensões verificadas;
- resultado da comparação com o CSV canônico.

Um espelho não deve ser anunciado como sincronizado sem essa verificação.
