# Direção científica do projeto

**Sistema:** Simbiotrama — Catálogo de Dados Científicos do Brasil  
**Foco ativo:** Instância 1 — catálogo relacional de fontes e ofertas de dados  
**Princípio:** organizar o que é necessário para descobrir, compreender e acessar, sem reconstruir a fonte externa.

## 1. Missão

> Tornar fontes e ofertas de dados científicos mais encontráveis, compreensíveis e acessíveis, preservando a identidade, a terminologia e os links das instituições produtoras.

A Instância 1 deve ser útil como catálogo autônomo e sustentar uma interface dinâmica.

## 2. Objeto central

O objeto central é a **entrada de catálogo**.

Uma entrada pode representar fonte, plataforma, coleção, produto ou serviço quando esse nível for útil ao usuário.

O projeto não impõe a mesma genealogia a todas as plataformas. Não existe obrigação universal de separar família, produto, release, distribuição e ativo.

## 3. Conteúdo científico necessário

Cada entrada deve comunicar, conforme disponibilidade:

- o que oferece;
- quais modalidades de dados contém;
- quais temas e variáveis principais aparecem;
- onde e quando se aplica;
- qual resolução ou suporte é material;
- como acessar;
- onde encontrar metadados, método, licença e citação.

A descrição deve ser proporcional. Não é necessário reconstruir observações, estimands, populações-alvo, cadeias completas de transformação ou todos os produtos internos.

## 4. Escopo geográfico

A prioridade é o Brasil e produtos internacionais com cobertura sistemática do país.

Podem ser incluídas entradas com:

- dados espaciais explícitos;
- códigos territoriais;
- séries por unidades geográficas;
- cobertura nacional, regional ou local relevante;
- serviços que encaminham claramente a dados georreferenciados.

O catálogo descreve e aponta; não precisa hospedar os datasets.

## 5. Arquitetura científica mínima

```text
Organização
  └── Entrada de catálogo
        ├── temas e variáveis principais
        ├── metadados essenciais
        ├── evidências proporcionais
        └── conector opcional
```

PostgreSQL/PostGIS continua como banco-alvo. PostGIS apoia metadados geográficos e filtros, não armazenamento integral de rasters, vetores ou cubos externos.

## 6. Princípios permanentes

1. A fonte original permanece responsável pelos dados.
2. O Simbiotrama não copia nem arquiva datasets externos nesta fase.
3. A terminologia do produtor deve ser preservada.
4. Normalização serve à descoberta e aos filtros, não à reinvenção dos conceitos.
5. Nova entrada exige diferença material, não apenas novo arquivo ou layer.
6. Ausência de documentação permanece desconhecida.
7. Qualidade e incerteza são registradas quando materialmente documentadas.
8. Evidência deve ser proporcional ao campo sustentado.
9. Padrões e literatura são referências, não comandos de expansão arquitetural.
10. Instâncias 2 e 3 não devem atrasar a Instância 1.
11. O critério de parada deve ser explícito.
12. O sucesso é medido por fichas úteis prontas para o website.

## 7. Curadoria

A unidade de trabalho é uma entrada suficientemente descrita.

A curadoria termina quando:

- a granularidade está justificada;
- a ficha é compreensível;
- os campos essenciais disponíveis estão sustentados;
- os links principais funcionam;
- as lacunas relevantes estão explícitas;
- aprofundamento adicional não mudaria a apresentação pública.

## 8. Instância 2

**Estado:** `BACKLOG`.

Poderá usar conectores externos selecionados para visualização federada. Não exige armazenamento dos dados nem inventário completo das plataformas.

## 9. Instância 3

**Estado:** `BACKLOG`.

Poderá contextualizar entradas e visualizações por literatura científica curada. Não define o núcleo da Instância 1.

## 10. Gate de prioridade

Toda intervenção deve responder:

> Esta mudança melhora descoberta, interpretação mínima, filtro do website ou conector selecionado?

Sem resposta positiva demonstrável, a proposta permanece no backlog.

## 11. Critério de sucesso

A fase atual terá sucesso quando o catálogo permitir responder, de modo claro e verificável:

- quem oferece;
- o que oferece;
- quais dados e variáveis principais estão disponíveis;
- qual cobertura e período;
- como acessar;
- quais condições gerais se aplicam;
- onde consultar a documentação oficial.
