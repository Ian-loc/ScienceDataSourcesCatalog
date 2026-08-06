# Direção científica do Simbiotrama

**Status:** direção estratégica vigente após revisão de escopo  
**Foco ativo:** Instância 1 — catálogo relacional simplificado

## 1. Missão

O Simbiotrama deve tornar fontes e ofertas de dados científicos mais fáceis de encontrar, compreender e acessar, preservando a autoria, os metadados e os canais mantidos pelas instituições originais.

A Instância 1 não pretende reconstruir plataformas externas nem armazenar seus dados.

## 2. Princípio central

> Estruturar somente o conhecimento necessário para descoberta, compreensão e acesso; referenciar a fonte original para o restante.

Precisão não significa decomposição ilimitada. Um catálogo pode ser cientificamente rigoroso sem reproduzir todas as releases, bandas, layers, arquivos ou endpoints de uma plataforma.

## 3. Objeto do catálogo

O objeto público central é a **entrada de catálogo**.

Uma entrada pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

A granularidade deve seguir a identidade usada pela fonte e a utilidade para o usuário.

## 4. Informação científica necessária

Cada entrada deve permitir compreender, quando aplicável:

- que informação geral está disponível;
- quais modalidades de dados são oferecidas;
- quais variáveis ou grupos de variáveis estão presentes;
- qual cobertura espacial e temporal é declarada;
- qual resolução ou suporte é material;
- como acessar;
- quais condições, licença e citação são informadas;
- onde consultar os metadados oficiais.

Não é necessário reproduzir o esquema integral dos arquivos ou a genealogia técnica da oferta.

## 5. Granularidade mínima suficiente

Uma entrada adicional só é necessária quando existe diferença material em:

- significado científico;
- modalidade principal;
- cobertura;
- período;
- método;
- finalidade;
- acesso principal;
- identidade oficial separada.

Outro arquivo, formato, layer, banda, endpoint, diretório, tabela ou data técnica não constitui diferença suficiente por si só.

## 6. Variáveis

O catálogo registra rótulos e grupos úteis para descoberta.

- preservar nomes do produtor;
- usar grupos amplos;
- não construir ontologia universal nesta fase;
- não inferir equivalência entre fontes;
- não enumerar todas as bandas ou colunas quando uma síntese é suficiente.

## 7. Dados permanecem externos

O Simbiotrama não:

- copia datasets de terceiros;
- mantém arquivos externos como acervo;
- espelha catálogos completos;
- promete preservação;
- assume custódia;
- substitui metadados oficiais.

Links e metadados são registrados para direcionar o usuário às fontes originais.

## 8. Arquitetura científica

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles  [opcional]
```

PostgreSQL é adequado para integridade, busca e manutenção. PostGIS pode ser usado para metadados de cobertura, sem ingestão dos datasets externos.

## 9. Curadoria

A unidade de trabalho é uma entrada suficientemente curada.

A curadoria deve:

- começar pela página oficial e metadados diretos;
- registrar somente campos necessários à ficha;
- preservar terminologia original;
- indicar lacunas sem inferência;
- parar quando houver suficiência;
- evitar genealogia e inventário técnico desnecessários.

## 10. Instância 2

A Instância 2 permanece em backlog e deverá funcionar como visualização federada por APIs e conectores externos.

Ela poderá carregar uma seleção de camadas ou coleções sem que a Instância 1 tenha previamente inventariado todos os objetos da plataforma.

## 11. Instância 3

A Instância 3 permanece em backlog e deverá usar literatura científica curada para contextualizar entradas e composições.

Não haverá busca web irrestrita por padrão.

## 12. Princípios permanentes

1. A fonte original continua autoritativa para os dados.
2. O catálogo registra metadados essenciais, não todo o conteúdo disponível.
3. Precisão e simplicidade devem ser otimizadas conjuntamente.
4. Desconhecido não equivale a ausente.
5. Metadados devem ser proporcionais ao nível da entrada.
6. A página principal de acesso pode ser suficiente.
7. Conector não é ativo armazenado.
8. Visualização não exige replicação da base externa.
9. Instâncias 2 e 3 não ampliam o núcleo da Instância 1.
10. Toda nova entidade deve demonstrar necessidade recorrente.

## 13. Sucesso

O catálogo é bem-sucedido quando o usuário consegue:

- descobrir uma fonte ou oferta relevante;
- entender que dados poderá encontrar;
- reconhecer cobertura e condições básicas;
- seguir para o canal oficial correto;
- identificar oportunidades de visualização futura.

Se a manutenção exigir reproduzir a árvore interna de cada plataforma, o escopo está incorreto.
