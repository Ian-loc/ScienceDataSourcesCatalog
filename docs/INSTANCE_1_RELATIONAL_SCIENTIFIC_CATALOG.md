# Instância 1 — Catálogo relacional simplificado

**Status:** direção canônica proposta  
**Prioridade:** foco ativo  
**Escopo:** fontes e ofertas de dados científicos relevantes ao Brasil  
**Banco-alvo:** PostgreSQL; PostGIS apenas quando útil para metadados de cobertura

## 1. Missão

A Instância 1 deve permitir que o usuário:

- encontre fontes e ofertas de dados;
- compreenda que tipo de informação está disponível;
- identifique variáveis ou grupos de variáveis;
- reconheça cobertura espacial e temporal;
- compreenda condições básicas de acesso;
- abra a página ou o canal oficial adequado;
- encontre licença, citação e metodologia quando disponíveis;
- saiba se existe conector selecionado para visualização futura.

Ela não deve reconstruir a arquitetura interna das plataformas externas.

## 2. Entidade central

A entidade central é `catalog_entry`.

Uma entrada pode representar:

- `source`;
- `platform`;
- `collection`;
- `data_product`;
- `data_service`.

O tipo é amplo e serve à descoberta. O catálogo não precisa resolver ontologicamente cada diferença interna de uma plataforma.

## 3. Arquitetura mínima

```text
organizations
  └── catalog_entries
        ├── entry_variables
        ├── entry_evidence
        └── connector_profiles  [opcional]
```

### `organizations`

Instituições, consórcios, redes ou iniciativas responsáveis.

### `catalog_entries`

Entradas públicas do catálogo. Devem conter somente metadados necessários para descoberta, compreensão e acesso.

### `entry_variables`

Rótulos originais, grupos temáticos e definições úteis para busca. Não constituem taxonomia universal.

### `entry_evidence`

Links e notas que sustentam campos materiais da ficha.

### `connector_profiles`

Configurações externas selecionadas para uso futuro pela Instância 2. São opcionais e não representam armazenamento.

## 4. Granularidade mínima suficiente

A entrada deve corresponder ao menor nível que:

- tenha identidade reconhecível;
- seja útil ao usuário;
- permita descrição coerente;
- possua canal de acesso oficial;
- não exija reconstrução da plataforma.

Criar nova entrada somente diante de diferença material de significado científico, modalidade, cobertura, período, método, finalidade ou acesso principal.

Não criar nova entrada apenas por existir outro arquivo, formato, layer, banda, diretório, endpoint, tabela ou atualização técnica.

## 5. Perfil mínimo

### Identidade

- organização;
- nome oficial;
- sigla;
- tipo amplo;
- estado.

### Conteúdo

- resumo;
- escopo científico;
- modalidades de dados;
- variáveis ou grupos;
- usos potenciais apresentados com cautela.

### Espaço e tempo

- cobertura geográfica;
- cobertura temporal;
- resolução ou suporte quando material;
- frequência de atualização.

### Acesso

- página oficial;
- metadados;
- acesso principal;
- gratuidade;
- autenticação;
- condições relevantes;
- formato ou protocolo apenas quando útil.

### Referência

- metodologia;
- licença;
- citação;
- data de verificação;
- evidência principal.

## 6. Dados externos

Todos os datasets, arquivos, layers, coleções e endpoints permanecem externos.

O Simbiotrama não:

- copia ou hospeda dados;
- mantém espelhos silenciosos;
- promete preservação;
- inventaria integralmente ativos;
- assume custódia;
- substitui metadados oficiais.

## 7. Metadados do produtor

O catálogo deve usar prioritariamente:

- página oficial;
- metadados diretos;
- página principal de acesso;
- metodologia;
- licença;
- citação.

A regra é:

```text
normalizar o necessário para descoberta
+
preservar o necessário para interpretação
+
referenciar a fonte para o restante
```

## 8. Variáveis

- preservar o nome usado pela fonte;
- registrar grupos amplos de busca;
- evitar inventário de bandas e colunas sem utilidade pública;
- não inferir equivalência entre fontes;
- não criar ontologia universal nesta fase.

## 9. Conectores e Instância 2

A Instância 2 será uma visualização federada por APIs e outros conectores.

Um conector pode registrar:

- tipo;
- endpoint ou identificador;
- autenticação;
- operação selecionada;
- estado e data do teste.

A entrada não precisa conter todos os layers ou arquivos para que um conector específico funcione.

## 10. Transição

Os CSV/JSON atuais permanecem autoridade pública transitória.

O esquema profundo do Marco 1 passa a `LEGACY_TRANSITIONAL`. Ele poderá fornecer:

- staging;
- padrões de IDs;
- validações de integridade;
- componentes de migração;
- evidências históricas.

Ele não deve continuar como arquitetura-alvo nem exigir família, release, distribuição, ativo ou capacidade para concluir uma entrada.

## 11. Validação do modelo

O núcleo simplificado deve representar:

- GEDI;
- DETER Cerrado;
- IBGE;
- ANA/SNIRH.

A validação falha se:

- exigir inventário integral;
- proliferar tabelas específicas;
- criar muitos campos vazios;
- perder o significado necessário ao usuário;
- misturar catálogo e visualização;
- sugerir armazenamento de dados externos.

## 12. Critério de sucesso

A Instância 1 é bem-sucedida quando o usuário consegue encontrar uma entrada, compreender seu conteúdo e chegar à fonte correta sem que o Simbiotrama reproduza o catálogo original.
