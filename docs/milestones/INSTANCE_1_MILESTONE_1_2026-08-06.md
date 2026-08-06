# Simbiotrama — Instância 1 — Marco de execução 1

**Data de consolidação:** 6 de agosto de 2026  
**Fuso de referência:** `America/Sao_Paulo`  
**Repositório transitório:** `Ian-loc/ScienceDataSourcesCatalog`  
**Pull request de consolidação:** #54  
**Pull request de registro:** #55  
**Head auditado antes da incorporação:** `0c9acd2e255c53c73c5c8373470ee239740f8ec1`  
**Commit científico-arquitetural na `main`:** `3fd87900ee69d04f30bda8d085e848e990637295`  
**Commit do registro do marco:** `bda7ab32261c7f52621722ef88cc7a113d2a5ede`  
**Método de incorporação:** squash merge  
**Estado:** `INCORPORATED`

## 1. Declaração do marco

Este marco encerra o primeiro grande ciclo de consolidação da **Instância 1 — catálogo relacional científico-operacional de produtos de dados georreferenciados sobre o Brasil**.

A incorporação estabelece uma linha de base executável e auditada para a continuação do Simbiotrama. Ela não declara completude científica de todos os produtos catalogados, não promove o PostgreSQL a autoridade canônica de produção e não autoriza implementação das Instâncias 2 ou 3.

## 2. Escopo incorporado

O Marco 1 incorpora:

- arquitetura relacional PostgreSQL/PostGIS de destino;
- separação entre organização, fonte, família, produto, release, distribuição, ativo e capacidade de acesso;
- staging sem perda dos CSVs legados;
- carga determinística e idempotente;
- promoção normalizada seletiva em banco efêmero de teste;
- contratos científicos e operacionais;
- evidência por afirmação e revisão curatorial;
- validações de integridade, chaves, cardinalidades, duplicatas, órfãos e idempotência;
- fronteiras científicas e operacionais iniciais para TerraClass, Dynamic World, PRODES, DETER Amazônia e DETER Cerrado;
- registro de ocorrências, auditorias e gates executáveis;
- preservação da página pública e dos CSVs/JSON como autoridade pública durante a transição.

## 3. Dimensão do pacote consolidado

O PR #54 foi encerrado com:

- 239 commits de desenvolvimento condensados por squash;
- 139 arquivos alterados;
- 19.312 adições;
- 1.103 remoções;
- CI pré-merge aprovado no workflow `Validar e publicar catálogo`, execução #420;
- nenhuma revisão contrária;
- nenhuma thread de revisão aberta;
- merge protegido pelo SHA exato do head auditado.

O PR #55 registrou o marco e formalizou o regime de pacotes subsequentes.

## 4. Estado científico alcançado

A arquitetura passou a impedir, por contrato e validação, colapsos indevidos entre:

- plataforma, catálogo, serviço e produto científico;
- família, produto e release;
- metadado, distribuição, ativo e endpoint;
- máscara acumulada, incremento, resíduo, taxa, alerta e inventário;
- resolução, escala, grade e suporte;
- ausência de incerteza e incerteza não documentada;
- datas de interface, datas de acesso e edição científica;
- capacidades técnicas da fonte e propriedades científicas do produto.

Os produtos e famílias parcialmente modelados permanecem sob revisão. O marco confirma a validade da estrutura e dos controles, não a completude de cada perfil.

## 5. Autoridade após o marco

```text
main
= autoridade material incorporada do repositório transitório

CSV/JSON públicos
= autoridade pública corrente durante a transição

PostgreSQL/PostGIS
= arquitetura canônica de destino, ainda não promovida a produção

Instâncias 2 e 3
= backlog, fora do escopo ativo
```

As branches históricas do PR #54 não devem receber novo desenvolvimento.

## 6. Pendências preservadas

Permanecem fora da declaração de completude do Marco 1:

- fechamento científico integral de Dynamic World V1 e TerraClass Amazônia 2020;
- resolução completa de produtos, releases, ativos e perfis de PRODES;
- fechamento de DETER Amazônia, DETER Cerrado e DETER Pantanal;
- modelagem de vegetação secundária por bioma;
- modelagem aprofundada dos produtos MapBiomas;
- revisão e resolução de entidade das 51 fontes legadas;
- inspeção integral de DR0001 — Clima Gerais;
- auditoria transversal de prontidão canônica;
- promoção do PostgreSQL como autoridade;
- migração para o futuro repositório privado `Simbiotrama`.

## 7. Regime de execução subsequente

1. todo desenvolvimento parte da `main` corrente;
2. cada pacote coerente recebe branch e PR próprios;
3. famílias independentes não são misturadas;
4. mudanças transversais são isoladas;
5. cada PR possui critério explícito de completude;
6. o delta é auditado antes de congelar o head;
7. o CI deve estar verde no SHA exato;
8. merge requer ausência de revisão contrária e threads abertas;
9. merges futuros exigem autorização humana explícita;
10. squash merge é preferido para preservar legibilidade da `main`.

## 8. Próximo marco científico

Após a limpeza de sanidade pós-marco, o próximo pacote científico é:

> **Marco 2A — fechamento científico-operacional do DETER Cerrado.**

Seu critério de completude inclui identidade, produto e release, classes, método, limiar, perfis espacial e temporal, qualidade e limitações, distribuições, ativos, endpoints, capacidades, licença, citação, evidências por afirmação, revisão curatorial e gates executáveis.

DETER Amazônia, DETER Pantanal, PRODES, Clima Gerais, MapBiomas e outras famílias permanecerão fora desse PR, salvo dependência transversal mínima, explícita e demonstrada.

## 9. Decisão de governança

Este marco foi autorizado pelo responsável do projeto em 6 de agosto de 2026. Os merges dos PRs #54 e #55 foram executados e verificados. A execução contínua da Instância 1 permanece autorizada dentro dos contratos científicos, técnicos e de governança vigentes.
