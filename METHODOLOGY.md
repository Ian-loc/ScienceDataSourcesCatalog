# Metodologia de curadoria

## 1. Escopo

O foco ativo é a Instância 1 simplificada: catálogo relacional de fontes e ofertas de dados científicos.

A unidade de trabalho é uma `catalog_entry`, não uma reconstrução obrigatória de família, produto, release, distribuição e ativo.

## 2. Pergunta orientadora

Antes de iniciar a pesquisa, definir:

> Qual informação mínima o usuário precisa para descobrir, compreender e acessar esta oferta?

O plano de coleta deve ser limitado a essa resposta.

## 3. Delimitação da entrada

Uma entrada pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

A decisão deve considerar:

- identidade usada pela própria fonte;
- utilidade para descoberta;
- coerência do resumo;
- estabilidade do canal de acesso;
- custo de manutenção.

Não criar entradas adicionais apenas por diferenças de arquivo, formato, layer, banda, endpoint, diretório ou data técnica.

## 4. Metadados essenciais

Coletar, quando aplicável:

- organização;
- nome e sigla;
- tipo amplo;
- resumo;
- escopo científico;
- modalidades de dados;
- variáveis ou grupos;
- cobertura espacial;
- cobertura temporal;
- resolução ou suporte material;
- frequência de atualização;
- acesso, gratuidade e autenticação;
- página oficial;
- metadados;
- metodologia;
- licença;
- citação;
- data de verificação.

## 5. Evidências

Prioridade:

1. página oficial;
2. metadados diretos;
3. página principal de acesso;
4. metodologia;
5. licença;
6. citação;
7. documentação de conector, quando aplicável.

Cada evidência sustenta apenas o campo correspondente.

Não é necessário copiar o documento nem examinar toda a árvore de páginas.

## 6. Variáveis

Registrar variáveis ou grupos úteis para busca.

- preservar rótulos originais;
- preservar definições quando disponíveis;
- registrar unidade somente quando material;
- usar grupo amplo para filtro;
- não enumerar todas as bandas ou colunas sem necessidade;
- não inferir equivalência sem evidência.

## 7. Espaço e tempo

Registrar no nível de detalhe necessário à interpretação da entrada.

Não é obrigatório separar resolução, suporte, escala, grade, CRS, janela, latência e agregação em entidades próprias. Campos textuais são aceitáveis enquanto forem claros e sustentados.

## 8. Acesso

Priorizar um canal principal e poucos links essenciais.

Registrar:

- acesso principal;
- gratuidade;
- autenticação;
- condições relevantes;
- formato ou protocolo quando útil;
- conector selecionado, quando aprovado.

Não inventariar todos os downloads ou serviços.

## 9. Conectores

Conectores são opcionais.

A investigação técnica deve ocorrer somente quando existir uma operação futura concreta, como visualizar uma coleção ou camada selecionada.

Registrar apenas endpoint, identificador, autenticação, operação e estado do teste.

## 10. Estados negativos

Usar estados explícitos:

- `unknown`;
- `not_found_after_bounded_search`;
- `not_applicable`;
- `inaccessible_in_current_environment`;
- `contradictory`.

Não converter ausência de documentação em ausência da propriedade.

## 11. Critério de parada

A pesquisa termina quando:

- os campos essenciais estão sustentados;
- o usuário consegue compreender a oferta;
- existe acesso oficial apropriado;
- lacunas relevantes estão explícitas;
- nova pesquisa produziria apenas inventário técnico ou genealogia.

## 12. Revisão

A revisão deve verificar:

- granularidade adequada;
- fidelidade à fonte;
- suficiência;
- clareza;
- utilidade para busca;
- ausência de inferência;
- ausência de replicação da plataforma;
- ausência de armazenamento externo;
- consistência com a política de escopo.

## 13. Exemplos

### GEDI

Registrar uma entrada ampla que comunique LiDAR orbital, estrutura da vegetação, altura, biomassa, qualidade, cobertura e acesso oficial. Não reproduzir todos os níveis, versões e granules.

### DETER Cerrado

Registrar a oferta de alertas, propósito, variáveis ou classes amplas, cobertura, método resumido, acesso e limitações. Não exigir release, layer, checksum ou pacote como condição geral.

### IBGE

Criar entradas específicas apenas quando a distinção melhora descoberta, como uma base estatística ou malha territorial claramente separada. Não enumerar cada tabela.

### ANA/SNIRH

Registrar plataforma ou coleção relevante, dados hidrológicos, cobertura e canal oficial. Arquivos e serviços permanecem na fonte.

## 14. Saída

Cada unidade deve produzir:

- entrada normalizada;
- variáveis ou grupos;
- evidências essenciais;
- lacunas;
- conector opcional;
- verificação de escopo.

Número de arquivos, endpoints ou links coletados não é produto da curadoria.
