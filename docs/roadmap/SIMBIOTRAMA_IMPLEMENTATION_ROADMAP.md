# Roadmap de implementação do Simbiotrama

**Status:** vigente após incorporação  
**Foco ativo:** Instância 1 — catálogo relacional simplificado  
**Instâncias 2 e 3:** backlog

## 1. Objetivo atual

Entregar um catálogo relacional funcional de fontes e ofertas de dados científicos, com metadados essenciais, links oficiais, variáveis e temas pesquisáveis, pronto para alimentar uma interface dinâmica.

A unidade de progresso é uma **entrada de catálogo útil e suficientemente verificada**, não um produto ou release integralmente decomposto.

## 2. Princípios de execução

1. Normalizar somente o necessário para descoberta, interpretação, filtro e conexão futura.
2. Preservar terminologia e links oficiais da fonte.
3. Não copiar datasets externos nem reconstruir catálogos de terceiros.
4. Não criar entradas apenas por arquivo, layer, banda, formato ou endpoint.
5. Não exigir release, ativo, bytes, checksum ou schema completo como regra universal.
6. Registrar lacunas sem inferência.
7. Trabalhar em PRs pequenos e auditáveis.
8. Manter Instâncias 2 e 3 fora do caminho crítico.
9. Validar o modelo com casos heterogêneos antes de expandir.
10. Medir utilidade pública, não profundidade documental acumulada.

## 3. Marcos da Instância 1

### I1-M1 — núcleo relacional e staging

**Estado:** `COMPLETED`  
**Incorporação:** PRs #54 e #55; sanity no PR #56.

O Marco 1 demonstrou staging, idempotência, integridade relacional e separação conceitual inicial. A arquitetura profunda incorporada permanece como histórico técnico e fonte de componentes reutilizáveis, mas não define mais a granularidade obrigatória da Instância 1.

### I1-S1 — simplificação governada

**Estado:** `ACTIVE`

Entregas:

- política de escopo e granularidade mínima suficiente;
- `catalog_entry` como unidade central;
- ficha mínima e critério de parada;
- revisão dos documentos canônicos;
- classificação do PR #57 como pacote congelado e candidato a `superseded`;
- plano de migração sem perda da estrutura anterior;
- gate contra expansão arquitetural não justificada.

### I1-S2 — desenho executável mínimo

**Estado:** `NEXT`

Entregas propostas:

- modelo mínimo para `organizations`, `catalog_entries`, `entry_variables` e `entry_evidence`;
- `connector_profiles` como extensão opcional;
- mapeamento dos registros existentes para o novo núcleo;
- compatibilidade de leitura com o staging e os CSVs atuais;
- migração idempotente e reversível;
- exportação apropriada ao website.

O desenho deve evitar remoções destrutivas. Tabelas profundas existentes podem permanecer como legado técnico ou extensão inativa até decisão de migração posterior.

### I1-S3 — validação com casos heterogêneos

**Estado:** `PLANNED`

Casos iniciais:

1. GEDI — missão e coleção com muitos produtos internos;
2. DETER Cerrado — monitoramento operacional;
3. IBGE — fonte territorial e estatística ampla;
4. ANA/SNIRH — plataforma com séries, tabelas, arquivos e serviços.

Critério de aprovação:

- nenhuma necessidade de inventário integral;
- ausência de proliferação de entidades;
- campos essenciais preenchíveis;
- significado suficiente para o usuário;
- links oficiais úteis;
- possibilidade de identificar conectores sem ativar a Instância 2.

### I1-S4 — revisão das entradas atuais

**Estado:** `PLANNED`

Objetivos:

- classificar os 51 registros legados como entradas de catálogo;
- consolidar duplicatas reais;
- preservar entradas amplas quando forem úteis;
- criar subentradas apenas por diferença material;
- identificar variáveis, temas, cobertura e acesso;
- registrar lacunas e estado curatorial;
- evitar enumeração completa das plataformas.

O primeiro lote deve ser pequeno e representar diferentes tipos de entrada.

### I1-S5 — website dinâmico

**Estado:** `BLOCKED_BY_MODEL_VALIDATION`

Entregas:

- busca textual;
- filtros por organização, tema, modalidade, variável, cobertura, período e acesso;
- fichas de entrada;
- links oficiais diferenciados;
- indicação simples de conectividade futura;
- exportação de metadados do catálogo.

Não inclui visualização federada de dados externos.

### I1-S6 — autoridade relacional

**Estado:** `BLOCKED_BY_GATES`

Entregas:

- auditoria transversal do modelo simplificado;
- migração e exportação reproduzíveis;
- backup e recuperação;
- integração do website;
- decisão humana de promoção.

Somente após esse gate o PostgreSQL poderá substituir os CSVs como autoridade canônica.

### I1-S7 — migração privada controlada

**Estado:** `BLOCKED_BY_I1_COMPLETION`

Preparar inventário, hashes, backup, baseline limpa, CI, proteção de branch e separação entre núcleo privado e presença pública autorizada. Criação, visibilidade e encerramento de repositório exigem autorização humana explícita.

## 4. Workflow permanente

### Curadoria de entradas

Identidade, resumo, modalidades, variáveis, temas, cobertura, resolução material, atualização, acesso, licença, citação e links oficiais.

### Evidência proporcional

Registrar suporte suficiente para os campos materiais, sem produzir pacotes forenses por entrada.

### Arquitetura mínima

Manter integridade, IDs, migrações, staging, exportações e critérios de expansão do esquema.

### Qualidade e governança

Auditar escopo, duplicidade, links, estados curatoriais, CI e gates humanos.

## 5. Backlog

### Instância 2 — visualização federada

Poderá usar APIs, WMS/WFS, STAC, Earth Engine e outros conectores para carregar dados externos. Cada conector será implementado seletivamente e não exigirá inventário prévio da plataforma inteira.

### Instância 3 — literatura científica

Poderá usar corpus curado para contextualizar entradas e visualizações. Não define a granularidade da Instância 1.

### Extensões semânticas

EBV, EESV, DCAT, STAC, SOSA/SSN, PROV-O, EML e Darwin Core podem orientar crosswalks futuros. Não devem ampliar automaticamente o núcleo.

## 6. Critério de sucesso

A Instância 1 terá sucesso quando o usuário puder responder:

- quem oferece os dados;
- o que a entrada oferece;
- quais temas, modalidades e variáveis principais estão presentes;
- onde e quando os dados se aplicam;
- qual resolução ou suporte é material para interpretação;
- como acessar;
- se o acesso é gratuito ou requer autenticação;
- onde encontrar metadados, método, licença e citação;
- se existe candidato a conector futuro.

Não é requisito responder toda a genealogia, todas as versões ou todos os arquivos disponíveis na fonte.
