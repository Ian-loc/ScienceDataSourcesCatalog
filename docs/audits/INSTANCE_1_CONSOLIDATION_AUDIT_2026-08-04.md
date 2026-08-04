# Auditoria de consolidação da Instância 1

**Data:** 2026-08-04  
**Escopo:** direção científica, modelo de dados, roadmap, documentação e transição  
**Resultado:** direção consolidada; migração de dados ainda pendente

## 1. Mudança auditada

O projeto foi recentrado na **Instância 1 — Catálogo relacional científico-operacional**.

As capacidades anteriormente discutidas de composição geográfica e síntese científica foram preservadas como Instâncias 2 e 3, mas retiradas do workstream ativo.

## 2. Problemas anteriores

### Mistura de instâncias

Documentos tratavam catálogo, visualização, comparabilidade, relações científicas, causalidade e backend como uma única progressão imediata.

### Mistura de entidades

O piloto de produtos continha produtos científicos, catálogos, serviços interoperáveis e infraestrutura de processamento na mesma tabela.

### Profundidade insuficiente

A base descrevia nome, cobertura e acesso, mas ainda não possuía estrutura relacional para:

- releases;
- mensagem informacional;
- não-representações;
- variáveis;
- métodos;
- perfis espaciais e temporais;
- qualidade e incerteza;
- evidência por campo;
- revisão curatorial.

### Autoridade tabular limitada

CSV e planilha são adequados para intercâmbio, mas insuficientes como arquitetura final de uma base com relações, versões e evidências.

## 3. Intervenções realizadas

- criado documento canônico da Instância 1;
- criada decisão estratégica;
- criado workflow de curadoria;
- implementado esquema PostgreSQL/PostGIS;
- implementado staging sem perda dos CSVs;
- atualizados README, direção científica, roadmap, modelo de produtos, metodologia, codebook e changelog;
- política de comparabilidade movida para estado futuro e somente leitura;
- Instâncias 2 e 3 explicitamente adiadas.

## 4. Avaliação da nova arquitetura

### Integridade conceitual

**Estado:** satisfatório.

A arquitetura separa:

- organização;
- fonte;
- família;
- produto;
- release;
- distribuição;
- ativo;
- variável;
- método;
- suporte;
- qualidade;
- evidência.

### Adequação científica

**Estado:** satisfatório como contrato inicial.

O modelo registra o significado do produto e suas limitações, evitando reduzir a curadoria a propriedades técnicas.

### Adequação operacional

**Estado:** satisfatório como arquitetura de destino.

Distribuições e capacidades permitem distinguir descoberta, visualização, consulta, recorte, processamento e exportação.

### Preparação para expansão

**Estado:** satisfatório.

A estrutura preserva caminhos para API, busca por variável, filtros geográficos, composição futura e contextualização científica, sem implementá-los agora.

## 5. Limitações remanescentes

1. O SQL ainda não foi aplicado em um servidor PostgreSQL/PostGIS de produção.
2. Os CSVs ainda não foram carregados no staging.
3. O piloto ainda não foi reclassificado linha por linha.
4. Releases explícitos ainda não foram criados para os produtos existentes.
5. Variáveis piloto ainda não foram preenchidas no banco.
6. A interface pública ainda lê a estrutura simplificada atual.
7. Não existe ainda pipeline automático banco → CSV → planilha → site.
8. Taxonomias controladas precisam de desenho e testes adicionais.
9. Campos e restrições podem exigir ajustes após os primeiros produtos completos.
10. A documentação antiga de transição permanece como registro histórico e não deve ser tratada como prioridade vigente.

## 6. Próximo bloco executável

### P0 — infraestrutura mínima

- iniciar PostgreSQL/PostGIS;
- aplicar `001_instance1_core.sql`;
- aplicar `002_legacy_staging.sql`;
- criar rotina de carga dos CSVs;
- registrar hashes e problemas.

### P0 — resolução do piloto

- classificar as 11 linhas atuais;
- retirar serviços e catálogos do conjunto de produtos científicos;
- criar releases;
- migrar distribuições;
- produzir relatório de reconciliação.

### P1 — perfis piloto

- PRODES;
- DETER;
- TerraClass;
- Dynamic World;
- MapBiomas;
- produto municipal de saúde;
- produto socioeconômico;
- produto de água ou clima.

### P1 — validação

- testar consultas;
- avaliar duplicação;
- revisar valores controlados;
- medir completude;
- ajustar o schema antes da expansão em escala.

## 7. Conclusão

A nova direção está documentada e implementada como arquitetura relacional de destino. A Instância 1 está conceitualmente consolidada, mas a base ainda precisa ser materialmente migrada e preenchida.

O próximo avanço correto não é ampliar o explorador. É carregar, reconciliar e aprofundar os produtos atuais no banco relacional.
