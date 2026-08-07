# Instância 1 — Catálogo relacional de fontes e ofertas de dados científicos

**Status:** direção canônica proposta  
**Prioridade:** foco ativo  
**Banco-alvo:** PostgreSQL com PostGIS  
**Princípio:** descrever o suficiente para descobrir, compreender e acessar dados mantidos pelas fontes originais.

## 1. Decisão funcional

A Instância 1 é um catálogo relacional, não um repositório de dados externos e não uma réplica das plataformas catalogadas.

Ela deve permitir ao usuário:

1. encontrar fontes, plataformas, coleções, produtos ou serviços relevantes;
2. compreender o que cada entrada oferece;
3. identificar modalidades, temas e variáveis principais;
4. reconhecer cobertura espacial e temporal;
5. encontrar resolução ou suporte quando material;
6. saber como acessar os dados;
7. localizar metadados, metodologia, licença e citação;
8. reconhecer candidatos a conectores futuros.

Não é objetivo da Instância 1 enumerar integralmente versões, arquivos, layers, bandas, endpoints ou genealogias.

## 2. Unidade central

A entidade pública principal é `catalog_entry`.

Uma entrada pode ser classificada amplamente como:

- `source`;
- `platform`;
- `collection`;
- `data_product`;
- `data_service`.

Essa classificação organiza a interface; não pretende reproduzir a ontologia interna de cada instituição.

Uma entrada adicional é criada apenas quando existe diferença material de significado, método, cobertura, finalidade ou forma principal de acesso.

## 3. Núcleo relacional mínimo

### `organizations`

Instituições produtoras, mantenedoras ou responsáveis.

Campos essenciais:

- identificador;
- nome oficial;
- acrônimo;
- país;
- homepage;
- descrição curta.

### `catalog_entries`

Fonte, plataforma, coleção, produto ou serviço exibido no catálogo.

Campos essenciais:

- identificador;
- organização;
- entrada pai opcional;
- tipo amplo;
- nome oficial e acrônimo;
- resumo;
- escopo científico;
- modalidades de dados;
- cobertura espacial e temporal;
- resolução ou suporte em texto;
- frequência de atualização;
- gratuidade e autenticação;
- página oficial;
- página de metadados;
- acesso principal;
- metodologia;
- licença;
- citação;
- estado curatorial;
- data de verificação;
- metadados adicionais em JSONB.

### `entry_variables`

Temas, fenômenos e variáveis principais que ajudam busca e compreensão.

Campos essenciais:

- entrada;
- nome usado pela fonte;
- definição da fonte quando disponível;
- termo simplificado de busca opcional;
- grupo temático amplo;
- unidade em texto quando material;
- evidência.

Não é necessário enumerar cada coluna, banda, classe ou atributo.

### `entry_evidence`

Evidência proporcional para campos materiais.

Campos essenciais:

- entrada;
- campo ou conjunto de campos;
- URL oficial;
- tipo de evidência;
- nota de suporte;
- data de recuperação;
- estado de evidência do campo.

### `connector_profiles`

Extensão opcional para candidatos selecionados da Instância 2.

Pode registrar:

- tipo de conector;
- endpoint ou identificador externo;
- autenticação;
- operações suportadas;
- configuração;
- data e resultado do último teste.

A presença de um conector não implica armazenamento dos dados.

## 4. Metadados adicionais

Informações específicas podem permanecer em JSONB ou texto quando não sustentam busca, filtro ou integração repetida.

Somente normalizar um conceito adicional quando:

1. aparece repetidamente;
2. possui significado estável;
3. melhora uma função pública concreta;
4. reduz ambiguidade de maneira demonstrável.

## 5. Conceitos não obrigatórios

Não são requisitos universais:

- família de produtos;
- release;
- distribuição;
- ativo;
- capacidade detalhada;
- observação primária;
- feature of interest;
- estimand;
- população-alvo;
- linhagem completa;
- schema físico;
- checksum;
- inventário de arquivos;
- perfil forense de qualidade.

Quando úteis, esses conceitos podem ser registrados como texto ou extensão opcional. Não devem bloquear a conclusão de uma entrada.

## 6. Pesquisa e curadoria

A curadoria começa por páginas e metadados oficiais. O trabalho deve parar quando a ficha essencial estiver suficientemente sustentada e houver um caminho oficial para acesso ou continuidade.

A ausência de documentação deve ser registrada como lacuna. Não deve ser convertida em inferência.

### Estado global da entrada

Usar apenas:

- `needs_review`;
- `partially_verified`;
- `verified`.

### Estado de evidência por campo

Usar:

- `needs_review`;
- `partially_verified`;
- `verified`;
- `not_found`;
- `not_applicable`.

`not_found` e `not_applicable` qualificam campos ou evidências; não são estados globais da entrada.

## 7. Exemplo GEDI

A entrada pública pode representar a missão ou coleção GEDI e informar:

- NASA como organização;
- LiDAR orbital como modalidade;
- estrutura da vegetação, altura do dossel, waveform e biomassa como conteúdos principais;
- cobertura e período gerais;
- gratuidade e autenticação;
- página principal, metadados, metodologia e acesso.

Não é necessário cadastrar cada nível, arquivo, tabela, variável interna ou versão como entrada separada.

Um identificador técnico específico só deve entrar em `connector_profiles` quando uma visualização futura realmente o utilizar.

## 8. Separação das instâncias

### Instância 1

Descoberta, compreensão e encaminhamento para as fontes originais.

### Instância 2

Visualização federada seletiva por APIs e conectores externos. Não constitui um armazém central de datasets.

### Instância 3

Contextualização por literatura curada. Não impõe ontologia ou profundidade à Instância 1.

## 9. Transição

Os CSV/JSON atuais continuam sustentando a versão pública enquanto o modelo simplificado é validado.

A migração deve:

- preservar staging e proveniência;
- evitar remoção destrutiva das estruturas incorporadas;
- mapear progressivamente registros para `catalog_entries`;
- manter extensões profundas como legado inativo quando necessário;
- gerar exportações compatíveis com o website;
- ser idempotente e reversível.

## 10. Critério de completude

Uma entrada está concluída quando:

- sua granularidade foi justificada;
- a descrição é útil e clara;
- temas, modalidades e variáveis principais foram identificados;
- cobertura e acesso estão suficientemente documentados;
- links essenciais foram verificados;
- lacunas relevantes foram registradas;
- está pronta para exibição pública.

A existência de documentação ou arquivos adicionais na fonte não torna automaticamente a entrada incompleta.
