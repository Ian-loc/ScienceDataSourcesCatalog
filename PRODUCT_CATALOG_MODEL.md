# Modelo relacional do catálogo

## 1. Decisão

A unidade pública principal é a **entrada de catálogo** (`catalog_entry`). Ela representa o nível mais útil para descoberta e compreensão, sem reconstruir a estrutura interna da fonte.

Uma entrada pode ser:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

## 2. Estrutura mínima

```text
Organização
  1 ─── N Entrada de catálogo
              ├── N temas e variáveis principais
              ├── N evidências proporcionais
              └── 0..N conectores opcionais
```

## 3. Entidades

### Organização

Instituição, consórcio, rede ou iniciativa responsável pela oferta.

### Entrada de catálogo

Objeto exibido ao usuário. Deve ter identidade oficial, resumo, escopo, cobertura, modalidades, acesso e links suficientes.

Uma entrada pai opcional pode organizar subentradas materialmente distintas. Essa relação não deve ser usada para reproduzir cada diretório ou produto técnico de uma plataforma.

### Variável ou tema da entrada

Representa fenômenos, temas e variáveis principais úteis para busca. Preserva o nome da fonte e pode incluir um termo simplificado de pesquisa.

Não é inventário completo de colunas, bandas, classes ou flags.

### Evidência da entrada

URL oficial e nota curta que sustentam um ou mais campos materiais.

### Perfil de conector

Configuração opcional de API, serviço ou identificador externo selecionado para a futura Instância 2. Não implica armazenamento do dado.

## 4. Granularidade

Criar nova entrada somente quando houver diferença material em:

- significado científico;
- modalidade principal;
- cobertura;
- método ou finalidade;
- público ou uso;
- forma principal de acesso.

Não criar nova entrada somente por:

- versão técnica;
- arquivo;
- formato;
- layer;
- banda;
- endpoint;
- tabela interna;
- data de atualização da interface.

## 5. Metadados essenciais

`catalog_entries` deve permitir registrar:

- organização;
- tipo amplo;
- nome e acrônimo;
- resumo;
- escopo científico;
- modalidades de dados;
- cobertura espacial e temporal;
- resolução ou suporte quando material;
- atualização;
- gratuidade e autenticação;
- página oficial;
- metadados;
- acesso principal;
- metodologia;
- licença;
- citação;
- estado curatorial;
- data de verificação;
- metadados adicionais em JSONB.

## 6. Extensões não obrigatórias

Família, produto, release, distribuição, ativo, método versionado, perfis detalhados e capacidades podem existir como legado ou extensão. Não definem completude universal.

Uma extensão somente deve ser ativada quando houver caso de uso concreto para:

1. descoberta;
2. interpretação mínima;
3. filtro do website;
4. conector selecionado.

## 7. Exemplo GEDI

Uma entrada pode descrever GEDI como missão ou coleção de LiDAR orbital, com estrutura da vegetação, altura do dossel, waveform e biomassa entre os conteúdos principais.

Não é necessário cadastrar L1B, L2A, L2B, L4A, L4B, cada arquivo e cada versão como entradas separadas.

## 8. Exemplo de acesso

A entrada pode ter links distintos para:

- página oficial;
- metadados;
- acesso principal;
- metodologia;
- licença;
- citação.

O catálogo encaminha o usuário à fonte. Não precisa enumerar todas as formas de download.

## 9. Migração

O modelo incorporado no Marco 1 deve ser preservado durante a transição. A simplificação será implementada por migração idempotente, crosswalk e exportação, sem exclusão destrutiva inicial.

## 10. Critério de qualidade

O modelo é adequado quando representa fontes heterogêneas sem proliferação de tabelas e produz fichas úteis para o website.
