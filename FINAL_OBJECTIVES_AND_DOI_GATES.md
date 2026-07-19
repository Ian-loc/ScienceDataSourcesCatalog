# Objetivos finais e critérios obrigatórios antes do DOI

## 1. Produto final

O **Ecology Data Catalog: catálogo de fontes de dados ambientais para pesquisa, ensino e extensão** deve ser publicado como um conjunto de dados curado, versionado e citável que permita localizar, comparar e avaliar fontes de dados ambientais relevantes para atividades acadêmicas.

A unidade de registro é uma **fonte de dados ou infraestrutura de informação**, não um dataset individual. Cada linha descreve uma fonte e suas condições gerais de acesso, cobertura, produtos, formatos, governança, uso acadêmico, limitações e evidências.

## 2. Objetivo geral

Disponibilizar um catálogo público, verificável e reutilizável de fontes de dados sobre ecologia, biodiversidade, clima, carbono, solo, vegetação, espécies, biosfera, mudanças climáticas e temas relacionados, com informações suficientes para apoiar descoberta, seleção e uso responsável em pesquisa, ensino e extensão.

## 3. Objetivos específicos finais

1. **Descoberta:** permitir localizar fontes por tema, cobertura geográfica, formato, acesso gratuito e acesso programático.
2. **Comparação:** oferecer campos controlados que permitam comparar função do recurso, escala, formatos, protocolos, ferramentas e situação institucional.
3. **Avaliação científica:** registrar utilidade acadêmica, limitações, evidência representativa e data de verificação.
4. **Transparência:** distinguir autodescrição oficial, classificação curatorial e evidência usada na auditoria.
5. **Reprodutibilidade:** manter CSV canônico, contrato de esquema, validações automáticas, histórico de mudanças e releases imutáveis.
6. **Acessibilidade:** disponibilizar interface pública utilizável em desktop e dispositivos móveis, com navegação por teclado, sem dependências externas e com fallback sem JavaScript.
7. **Citação e preservação:** produzir uma versão estável arquivável como Dataset, com autoria, ORCID, licença, versão, data e DOI consistentes.
8. **Manutenção sustentável:** permitir inclusão e revisão de fontes por lotes auditáveis, sem duplicar a fonte canônica entre GitHub e Drive.

## 4. Limites deliberados

O catálogo não pretende:

- hospedar ou redistribuir todos os datasets das fontes;
- substituir documentação, metadados ou termos de uso dos provedores;
- garantir qualidade homogênea entre datasets de uma mesma fonte;
- atribuir DOI genérico a cada infraestrutura;
- registrar cada produto individual como uma linha;
- certificar que uma fonte é adequada a qualquer pergunta de pesquisa sem avaliação metodológica adicional.

## 5. Definição mínima de completude científica

Uma fonte só pode integrar a versão estável quando possuir:

- identificador único e nome verificável;
- identidade oficial e tipo funcional separados;
- descrição curatorial objetiva;
- homepage ou URL oficial de verificação;
- áreas de pesquisa e palavras-chave;
- produtos e formatos classificados sem mistura semântica;
- escala e cobertura geográfica coerentes;
- situação de download e acesso programático;
- protocolo, ferramenta ou justificativa quando houver acesso automatizado;
- instituição responsável e situação institucional;
- uso acadêmico e limitação principal;
- evidência acadêmica, técnica ou oficial representativa;
- data ISO de verificação;
- ausência de contradições bloqueantes entre campos.

Valores desconhecidos podem existir somente quando explicitamente marcados, justificados e não comprometerem os campos mínimos de decisão.

## 6. Critérios de qualidade da versão 1.0.0

### 6.1 Estrutura e dados

- esquema 0.8.0 ou posterior estabilizado e documentado;
- 51 IDs atuais preservados durante a migração;
- todos os registros com 38 campos válidos;
- nenhuma decisão de migração pendente;
- nenhum `other_documented` sem descrição ou exceção resolvida;
- nenhuma contradição semântica aceita pelo CI;
- CSV, JSON derivado e interface consistentes.

### 6.2 Auditoria das fontes

- todas as 51 fontes revisadas ao menos uma vez no esquema final;
- links principais e documentação de acesso conferidos;
- formatos, protocolos, ferramentas, cobertura do Brasil e licenças revisados;
- evidência e data de verificação registradas;
- incertezas mantidas como incertezas, sem preenchimento por inferência não documentada.

### 6.3 Interface pública

- busca, filtros, ordenação e URLs compartilháveis funcionais;
- todos os 38 campos disponíveis na interface ou em detalhes técnicos;
- acessibilidade estrutural validada;
- responsividade verificada;
- identificação pública de versão e commit;
- deploy da release confirmado por inspeção direta ou evidência equivalente.

### 6.4 Documentação e governança

- README, metodologia, codebook, licenças e CFF coerentes;
- changelog encerrado para a release;
- GitHub é a fonte canônica;
- Drive contém somente registro executivo e histórico;
- processo de inclusão, revisão e correção de fontes documentado;
- licença de dados separada da licença do código.

### 6.5 Arquivamento e citação

- `CITATION.cff` atualizado para `1.0.0` apenas na data da release;
- autoria `Lara, Ian` e ORCID `0000-0003-1164-9318` conferidos;
- GitHub tag e release `v1.0.0` criadas;
- pacote arquivado como **Dataset**;
- arquivos do depósito conferidos antes da publicação;
- DOI de versão e DOI de conceito registrados separadamente;
- DOI propagado para repositório, site, ORCID e currículos.

## 7. Portões obrigatórios para DOI

O DOI permanece bloqueado enquanto qualquer portão estiver incompleto:

1. **G1 — escopo científico:** objetivos, unidade de registro e limites aprovados.
2. **G2 — esquema:** 38 campos estabilizados e codebook concluído.
3. **G3 — migração:** 51 registros migrados sem perda e sem decisão pendente.
4. **G4 — validação semântica:** todas as regras cruzadas ativas no CI.
5. **G5 — revisão das fontes:** 51 registros auditados no esquema final.
6. **G6 — qualidade de acesso:** links e condições de acesso verificados.
7. **G7 — interface:** campos, filtros e acessibilidade validados.
8. **G8 — publicação:** deploy da release confirmado.
9. **G9 — documentação:** README, metodologia, codebook, changelog e licenças coerentes.
10. **G10 — metadados de citação:** autor, ORCID, título, versão e data conferidos.
11. **G11 — release imutável:** tag e GitHub Release `v1.0.0` publicadas.
12. **G12 — inspeção do depósito:** tipo Dataset, arquivos e metadados conferidos antes de publicar o DOI.

## 8. Regra de decisão

- **GO para v0.8.0:** somente após resolver todos os 35 registros em revisão manual e validar a migração completa.
- **GO para v1.0.0:** somente após concluir DATA1, revisão mínima das 51 fontes, interface e publicação verificável.
- **GO para DOI:** somente após G1–G12 estarem concluídos.
- **NO-GO:** qualquer falha de CI, link crítico não verificado, decisão pendente, divergência entre CSV/interface/metadados ou ausência de evidência de deploy.

## 9. Estado atual

- versão formal: 0.7.0;
- UX1–UX4: integrados e validados;
- DATA1-A e DATA1-B: integrados e validados;
- 16 registros prontos para futura migração;
- 35 registros em revisão manual;
- esquema 0.8.0: ainda não aplicado;
- versão 1.0.0: bloqueada;
- DOI: bloqueado.
