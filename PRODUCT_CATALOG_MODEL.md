# Modelo relacional simplificado do catálogo

## 1. Decisão

A Instância 1 não reconstruirá a genealogia completa de plataformas externas. O núcleo deve representar entradas úteis para descoberta, compreensão e acesso.

A unidade central é `catalog_entry`, não uma cadeia obrigatória de família → produto → release → distribuição → ativo.

## 2. Estrutura canônica

```text
organization
  1 ─── N catalog_entry
               ├── N entry_variable
               ├── N entry_evidence
               └── N connector_profile  [opcional]
```

## 3. Organização

Instituição, rede, consórcio ou iniciativa responsável pela oferta.

Campos essenciais:

- nome oficial;
- sigla;
- país;
- página institucional;
- descrição curta.

Uma entrada pode ter mais de uma organização associada em implementação futura, mas isso não é requisito do primeiro núcleo.

## 4. Entrada de catálogo

Objeto público suficientemente estável e útil para o usuário.

Pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

A entrada deve responder:

- o que é;
- quem oferece;
- que tipos de dados contém;
- quais variáveis ou grupos são relevantes;
- onde e quando se aplica;
- como acessar;
- quais condições de uso existem;
- onde consultar os metadados oficiais.

## 5. Granularidade

Criar nova entrada quando houver diferença material em:

- significado científico;
- modalidade principal;
- cobertura espacial;
- cobertura temporal;
- método;
- finalidade;
- acesso principal;
- identidade oficial separada.

Não criar nova entrada apenas por existir outro arquivo, formato, layer, banda, endpoint, diretório, tabela ou atualização técnica.

## 6. Variáveis

`entry_variables` serve à descoberta.

Cada registro pode preservar:

- rótulo da fonte;
- definição da fonte;
- unidade, quando material;
- grupo amplo de busca;
- nota de escopo.

Não se exige inventário completo de bandas ou colunas. Não se cria taxonomia universal nesta fase.

## 7. Evidências

`entry_evidence` vincula campos materiais a páginas oficiais ou documentos diretos.

Campos mínimos:

- entrada;
- campo sustentado;
- URL;
- tipo de evidência;
- nota de suporte;
- data de recuperação;
- confiança.

O catálogo não precisa copiar o documento. A URL e a nota devem permitir auditoria.

## 8. Conectores

`connector_profiles` é opcional e prepara a Instância 2.

Pode registrar:

- tipo do conector;
- endpoint ou identificador externo;
- autenticação;
- operação selecionada;
- configuração mínima;
- estado e data do teste.

Um conector não é inventário de ativos. O endpoint ou layer necessário à visualização não cria automaticamente nova entrada.

## 9. Links

Priorizar poucos papéis:

- página oficial;
- metadados;
- acesso principal;
- metodologia;
- licença;
- citação.

Não se deve cadastrar toda a árvore de links da fonte.

## 10. Metadados adicionais

Informações específicas podem permanecer em `additional_metadata_json` quando:

- não justificam nova tabela;
- não são filtro recorrente;
- preservam estrutura fornecida pela fonte;
- não comprometem validação dos campos essenciais.

## 11. Dados externos

Arquivos, datasets, layers, tabelas e serviços permanecem nas fontes originais.

O Simbiotrama não:

- hospeda;
- arquiva;
- replica;
- promete preservação;
- enumera integralmente;
- assume custódia.

## 12. Exemplo: GEDI

Uma entrada suficiente pode registrar:

```text
Nome: GEDI — Global Ecosystem Dynamics Investigation
Organização: NASA
Tipo: collection
Modalidade: LiDAR orbital
Conteúdo: estrutura vertical da vegetação, altura do dossel, biomassa, qualidade e geolocalização
Cobertura: conforme metadados oficiais
Acesso: portal oficial
Variáveis: grupos amplos relevantes
Conector: apenas quando uma visualização específica for aprovada
```

Não é necessário reproduzir L1B, L2A, L2B, L4A, L4B, versões, granules e arquivos individuais como entradas independentes.

## 13. Migração

Os CSVs atuais serão mapeados para `catalog_entries`.

- registros amplos de fonte podem permanecer como uma entrada;
- registros de produtos úteis podem permanecer como entradas separadas;
- distribuições antigas serão condensadas em links principais ou conectores selecionados;
- nenhum ativo externo será materializado como entidade obrigatória;
- o esquema profundo do Marco 1 será preservado como `LEGACY_TRANSITIONAL`.

## 14. Busca e website

Filtros iniciais:

- organização;
- tipo de entrada;
- tema;
- modalidade;
- variável ou grupo;
- cobertura geográfica;
- período;
- resolução;
- acesso gratuito;
- autenticação;
- conector disponível.

A interface deve ser simples e não exigir que o usuário compreenda a arquitetura interna da fonte.
