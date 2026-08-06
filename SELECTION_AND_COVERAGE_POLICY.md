# Política de seleção, duplicidade e cobertura

## 1. Objetivo

Definir quais entradas pertencem ao Simbiotrama, qual granularidade é útil e como evitar duplicação ou reconstrução de plataformas externas.

O catálogo não é declarado completo ou representativo de todo o universo científico.

## 2. Escopo territorial

O Brasil é o escopo prioritário.

Ordem de prioridade:

1. instituições e ofertas brasileiras;
2. ofertas internacionais com cobertura sistemática do Brasil;
3. ofertas internacionais com dados brasileiros dependentes de coleção ou projeto;
4. referências internacionais sem cobertura direta apenas quando houver valor estratégico documentado.

A prioridade territorial organiza curadoria; não é nota de qualidade.

## 3. Unidade de seleção

A unidade elegível é uma **entrada de catálogo** com identidade reconhecível e utilidade para descoberta.

Pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

A seleção não exige que todas as ofertas internas de uma plataforma sejam cadastradas.

## 4. Critérios mínimos de inclusão

Uma entrada deve:

1. oferecer dados, metadados ou acesso estruturado relevante;
2. possuir organização ou governança identificável;
3. ter página oficial ou metadado verificável;
4. ter utilidade distinta para pesquisa, ensino, extensão ou decisão;
5. poder ser descrita com granularidade sustentável;
6. permitir registro honesto de cobertura e acesso;
7. demonstrar vínculo com o Brasil ou justificar função secundária.

## 5. Critérios de exclusão

Excluir ou não criar entrada própria para:

- notícias, blogs ou material apenas editorial;
- documentos sem oferta de dados associada;
- arquivo isolado de uma entrada já suficiente;
- layer, banda ou tabela sem identidade e utilidade pública próprias;
- endpoint técnico que serve apenas como conector;
- mirror sem governança própria;
- item descontinuado sem função independente;
- duplicata de nome ou URL;
- subdivisão cuja inclusão apenas reproduz a árvore da fonte.

## 6. Granularidade

Criar entrada separada quando houver diferença material de:

- significado científico;
- modalidade principal;
- cobertura geográfica;
- cobertura temporal;
- método;
- finalidade;
- acesso principal;
- identidade oficial.

Não criar entrada separada apenas por:

- arquivo;
- formato;
- layer;
- banda;
- diretório;
- endpoint;
- tabela;
- versão técnica;
- atualização de interface.

## 7. Fonte ampla e produto específico

Uma plataforma ampla pode ser suficiente quando sua função e seus dados são compreensíveis como conjunto.

Criar entrada específica de produto somente quando:

- o produtor o apresenta como oferta distinta;
- a distinção melhora substancialmente a busca;
- cobertura, método ou conteúdo diferem de forma relevante;
- o custo de manutenção permanece proporcional.

Exemplo: GEDI pode ser uma entrada ampla para descoberta de dados LiDAR, sem reprodução de todos os níveis e granules. Um produto específico só deve ganhar entrada própria se houver uso recorrente e identidade pública clara.

## 8. Duplicidade

### Mesmo objeto, nomes diferentes

Manter uma entrada e registrar siglas ou nomes alternativos.

### Instituição e plataforma

Podem coexistir porque possuem papéis diferentes: organização e entrada de catálogo.

### Plataforma e coleção

Manter separadas somente quando a coleção possui identidade, conteúdo e acesso claramente próprios.

### Agregador e provedor

Podem coexistir se a distinção melhora descoberta. Preservar a fonte original e evitar dupla contagem.

### Sucessor

Manter o sucessor ativo e registrar o anterior como histórico quando necessário.

## 9. Candidatos

Candidatos entram em staging com:

- nome;
- URL;
- tipo amplo;
- organização;
- justificativa;
- cobertura do Brasil;
- possível duplicidade;
- evidência;
- decisão.

Uma URL fornecida autoriza triagem, não publicação automática.

## 10. Prioridade Brasil P0–P3

A classificação P0–P3 pode ser mantida para ordenar a fila:

- `P0`: oferta brasileira;
- `P1`: cobertura brasileira sistemática;
- `P2`: cobertura brasileira parcial ou dependente de coleção;
- `P3`: referência estratégica sem cobertura direta.

Ela deve ser manual e auditável.

## 11. Cobertura e lacunas

A matriz de lacunas deve considerar:

- tema;
- modalidade de dados;
- variável ou grupo;
- região, bioma ou unidade territorial;
- cobertura temporal;
- tipo de organização;
- acesso gratuito;
- autenticação;
- conector potencial.

Não usar número de arquivos, layers ou releases como medida de cobertura.

## 12. Estratégia de enumeração

Usar apenas quando necessário:

- `single_entry`: uma entrada ampla é suficiente;
- `selective_entries`: poucas entradas específicas complementam a fonte;
- `external_index`: o índice integral permanece externo;
- `representative_sample`: amostra de teste explicitamente incompleta.

`complete` não deve ser padrão para plataformas extensas.

## 13. Revisão

Antes de aprovar uma entrada, verificar:

- identidade;
- utilidade;
- granularidade;
- duplicidade;
- cobertura;
- acesso;
- evidência;
- ausência de inventário desnecessário;
- ausência de cópia de dados externos.

## 14. Escopo negativo

O catálogo não deve:

- reproduzir a árvore de produtos de terceiros;
- enumerar todos os arquivos de uma coleção;
- criar entrada para cada layer ou banda;
- usar conectores como justificativa para decomposição geral;
- confundir cobertura do catálogo com volume de itens cadastrados.
