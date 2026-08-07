# Workflow contínuo de curadoria da Instância 1

**Objetivo:** concluir entradas de catálogo úteis, verificáveis e prontas para o website sem reconstruir plataformas externas.

## 1. Unidade de trabalho

Uma unidade concluída corresponde a **uma entrada de catálogo suficientemente descrita**.

A entrada pode representar fonte, plataforma, coleção, produto de dados ou serviço, conforme a granularidade mais útil ao usuário.

Não é requisito concluir todas as versões, arquivos, layers, bandas, distribuições ou endpoints associados.

## 2. Ficha essencial

A curadoria deve buscar:

- organização responsável;
- nome oficial e acrônimo;
- tipo amplo da entrada;
- resumo e escopo científico;
- modalidades de dados;
- temas e variáveis principais;
- cobertura espacial e temporal;
- resolução ou suporte quando material;
- frequência de atualização quando disponível;
- gratuidade, autenticação e condições gerais de acesso;
- página oficial;
- página de metadados;
- acesso principal;
- metodologia, licença e citação quando disponíveis;
- estado e data de verificação.

## 3. Sequência por entrada

### Etapa A — resolução mínima

1. identificar a organização e a página oficial;
2. decidir qual nível é útil: fonte, plataforma, coleção, produto ou serviço;
3. verificar se a entrada oferece dados científicos ou encaminha claramente para eles;
4. evitar subdivisão baseada apenas em arquivos, layers, bandas ou versões técnicas;
5. registrar o tipo e a justificativa de granularidade.

### Etapa B — descrição científica suficiente

1. explicar o que a entrada oferece;
2. registrar modalidades de dados;
3. listar temas e variáveis principais sem inventário exaustivo;
4. preservar os nomes usados pelo produtor;
5. registrar o que não deve ser inferido apenas quando houver risco real de interpretação.

### Etapa C — espaço, tempo e atualização

1. registrar cobertura geográfica;
2. registrar cobertura temporal;
3. registrar resolução ou suporte somente quando material;
4. distinguir período dos dados de data de publicação ou atualização da página;
5. manter desconhecidos como desconhecidos.

### Etapa D — acesso e documentação

1. registrar a página oficial;
2. registrar a página de metadados quando distinta;
3. registrar um caminho principal de acesso;
4. registrar gratuidade e autenticação quando documentadas;
5. registrar metodologia, licença e citação quando disponíveis;
6. testar apenas os links essenciais.

### Etapa E — evidência proporcional

Para campos materiais, registrar:

- campo ou conjunto de campos sustentados;
- URL oficial;
- nota curta de suporte;
- data de recuperação;
- estado de evidência do campo.

Não é necessário produzir uma afirmação atômica para cada detalhe trivial.

### Etapa F — revisão

Verificar:

- utilidade para descoberta;
- clareza da descrição;
- ausência de subdivisão excessiva;
- ausência de inferência não sustentada;
- funcionamento dos links essenciais;
- coerência com a política de escopo;
- prontidão para o website.

## 4. Critério de parada

A investigação deve encerrar quando:

1. a pessoa consegue compreender o que encontrará;
2. os campos essenciais disponíveis foram registrados;
3. existe caminho oficial para acesso ou continuidade;
4. lacunas relevantes estão explícitas;
5. aprofundamento adicional não mudaria materialmente a ficha pública.

O fato de existirem mais arquivos, layers, versões ou páginas não prolonga automaticamente a curadoria.

## 5. Quando aprofundar

Aprofundamento adicional é permitido somente quando:

- corrige uma ambiguidade central da entrada;
- é necessário para um filtro importante do website;
- diferencia duas entradas materialmente distintas;
- prepara um conector selecionado da Instância 2;
- responde a problema de licença, atribuição ou acesso.

Inspeção de bytes, schema, CRS, checksum, bandas e endpoints não é rotina da Instância 1.

## 6. Lotes e casos de validação

Primeiro ciclo:

1. GEDI;
2. DETER Cerrado;
3. IBGE;
4. ANA/SNIRH.

Após validar o modelo, trabalhar em lotes de 5 a 10 entradas. Cada lote deve incluir revisão de escopo antes de ampliar.

## 7. Saídas por lote

- entradas concluídas;
- variáveis e temas principais;
- evidências mínimas;
- links oficiais verificados;
- lacunas relevantes;
- candidatos a conectores;
- ocorrências de escopo ou duplicidade;
- exportação de teste para o website.

## 8. Indicadores de progresso

- entradas prontas para exibição;
- percentual de campos essenciais cobertos;
- links essenciais verificados;
- temas e variáveis identificados;
- duplicatas consolidadas;
- entradas com granularidade revisada;
- candidatos a conectores futuros.

Não usar como indicadores principais:

- releases resolvidos;
- ativos enumerados;
- quantidade de arquivos inspecionados;
- número de afirmações;
- número de commits ou validadores.

## 9. Proibições

- não reconstruir o catálogo da fonte;
- não copiar ou hospedar dados externos;
- não criar entrada apenas por formato, arquivo, layer, banda ou endpoint;
- não exigir release ou ativo como condição universal;
- não criar taxonomia científica universal do zero;
- não promover metadados adicionais sem utilidade pública demonstrável;
- não confundir acesso a uma plataforma com inventário de seus produtos;
- não preencher lacunas por inferência;
- não transformar literatura ou padrão externo em expansão automática do esquema;
- não declarar a entrada incompleta apenas porque a fonte contém mais detalhes.

## 10. Estados de curadoria e evidência

### Estado da entrada

Usar apenas:

- `needs_review` — ficha ainda não revisada;
- `partially_verified` — ficha útil, mas com campo material ainda pendente ou evidência insuficiente;
- `verified` — ficha essencial sustentada e pronta para exibição.

### Estado de evidência do campo

Usar:

- `needs_review`;
- `partially_verified`;
- `verified`;
- `not_found`;
- `not_applicable`.

`not_found` e `not_applicable` qualificam campos ou evidências; não são estados globais da entrada.

Uma entrada pode ser `verified` mesmo sem release, ativo, checksum ou inventário integral, desde que sua ficha essencial esteja sustentada e seu escopo seja claro.
