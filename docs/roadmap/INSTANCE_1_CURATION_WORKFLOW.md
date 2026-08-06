# Workflow de curadoria da Instância 1

## Objetivo

Curar entradas úteis de catálogo com o mínimo de profundidade necessário para descoberta, compreensão e acesso.

## 1. Unidade de trabalho

Uma unidade concluída é uma **entrada de catálogo suficientemente curada**.

Ela pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

A granularidade segue a identidade oficial e a utilidade para o usuário. Não segue automaticamente a estrutura interna completa da plataforma.

## 2. Sequência por entrada

### A. Delimitação

1. identificar a organização;
2. identificar a página oficial;
3. decidir o nível útil da entrada;
4. registrar por que esse nível é suficiente;
5. declarar o que ficará fora do escopo.

### B. Conteúdo

1. registrar nome e sigla;
2. escrever resumo objetivo;
3. registrar escopo científico;
4. identificar modalidades de dados;
5. registrar variáveis ou grupos de variáveis;
6. preservar rótulos originais quando úteis.

### C. Espaço e tempo

Registrar somente o que for material para descoberta e interpretação:

- cobertura geográfica;
- período;
- resolução ou suporte;
- frequência de atualização.

Não decompor esses campos em entidades separadas sem necessidade comprovada.

### D. Acesso

1. registrar página principal de acesso;
2. informar gratuidade;
3. informar autenticação;
4. registrar condições relevantes;
5. registrar formato ou protocolo somente quando útil ao usuário;
6. selecionar conector apenas quando houver caso de visualização aprovado.

### E. Metadados e evidência

Priorizar:

- página oficial;
- metadados diretos;
- metodologia;
- licença;
- citação.

Para cada campo material, registrar URL, nota de suporte e data de recuperação. Não perseguir todos os documentos ou links da plataforma.

### F. Revisão

Verificar:

- utilidade da entrada;
- suficiência dos metadados;
- coerência dos links;
- ausência de inferências;
- ausência de genealogia desnecessária;
- ausência de inventário de arquivos;
- adequação aos filtros públicos;
- clareza sobre o que permanece externo.

## 3. Critério de parada

Parar a pesquisa quando os campos essenciais estiverem suficientemente sustentados.

A existência de outros arquivos, releases, layers, bandas ou endpoints não prolonga automaticamente a curadoria.

Registrar como desconhecido quando uma informação essencial não puder ser confirmada.

## 4. Critério para nova entrada

Criar nova entrada somente diante de diferença material em:

- significado científico;
- modalidade principal;
- cobertura;
- período;
- método;
- público ou finalidade;
- acesso principal;
- identidade oficial separada.

Não criar nova entrada por diferença meramente técnica de arquivo, formato, layer, banda, diretório ou endpoint.

## 5. Variáveis

- registrar variáveis ou grupos relevantes para descoberta;
- preservar o nome da fonte;
- usar grupos amplos;
- não criar ontologia universal;
- não enumerar todas as colunas ou bandas quando uma síntese é suficiente;
- não inferir equivalência entre fontes.

## 6. Conectores

Um conector é opcional e pertence à preparação da Instância 2.

Registrar apenas:

- tipo;
- endpoint ou identificador externo;
- autenticação;
- operação suportada;
- estado e data do teste.

Conectores não criam automaticamente novas entradas.

## 7. Lotes

- trabalhar em lotes pequenos de 3 a 5 entradas heterogêneas;
- auditar granularidade antes de ampliar;
- corrigir padrões estruturais no mesmo lote;
- não expandir fontes inteiras por inércia;
- interromper o lote se surgir necessidade de nova entidade estrutural.

## 8. Saídas

- entradas normalizadas;
- variáveis ou grupos;
- evidências essenciais;
- lacunas explícitas;
- conectores selecionados, quando aplicável;
- relatório curto de escopo;
- exportação pública validada.

## 9. Indicadores

- entradas concluídas;
- tempo médio por entrada;
- campos essenciais sustentados;
- links oficiais válidos;
- retrabalho após revisão;
- entradas representáveis sem exceções estruturais;
- violações de escopo detectadas e corrigidas.

Não usar número de arquivos, releases, endpoints, commits ou linhas como indicador principal.

## 10. Proibições

- não copiar dados externos;
- não reconstruir catálogos de terceiros;
- não inventariar todos os ativos;
- não exigir release ou checksum como regra geral;
- não preencher por inferência;
- não transformar desconhecido em ausência;
- não criar tabela nova para um único caso sem revisão arquitetural;
- não misturar Instância 2 ou 3 ao pacote;
- não prolongar a pesquisa após atingir suficiência.
