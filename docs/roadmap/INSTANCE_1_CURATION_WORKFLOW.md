# Workflow contínuo de curadoria da Instância 1

**Objetivo:** aprofundar o catálogo fonte por fonte e produto por produto, com precisão científica, operacional e documental.

## 1. Unidade de trabalho

Uma unidade concluída corresponde a **um produto integralmente inspecionado**, incluindo:

- identidade e versão;
- significado científico;
- variáveis e classes relevantes;
- método;
- perfil espacial e temporal;
- qualidade, incerteza e limitações;
- distribuições e capacidades de acesso;
- evidências e revisão.

Cadastrar apenas o nome do produto não constitui conclusão.

## 2. Sequência por produto

### Etapa A — resolução do objeto

1. identificar a fonte;
2. confirmar o produtor primário;
3. distinguir plataforma, família, produto, versão e distribuição;
4. verificar se o objeto contém informação geográfica ou associação territorial inequívoca;
5. definir estratégia de enumeração.

### Etapa B — identidade científica

1. registrar nome oficial e acrônimo;
2. definir o objeto científico;
3. formular a mensagem informacional;
4. registrar o que o produto não representa;
5. identificar usos potenciais sem transformá-los em garantias de adequação.

### Etapa C — variáveis e estrutura

1. enumerar variáveis principais;
2. registrar classes, probabilidades, indicadores, flags e incertezas;
3. separar variável científica de coordenada, identificador e qualidade;
4. registrar unidade, tipo de dado e definição original;
5. preservar o nome usado pelo produtor.

### Etapa D — método e observação

1. classificar a natureza de produção;
2. documentar dados de entrada;
3. descrever processamento;
4. identificar método de validação;
5. registrar versão do método;
6. identificar dependência de outros produtos.

### Etapa E — espaço e tempo

1. registrar tipo de geometria;
2. definir suporte espacial;
3. registrar resolução e seu significado;
4. registrar CRS, grade e unidade geográfica;
5. registrar extensão;
6. registrar cobertura, janela e resolução temporal;
7. distinguir frequência dos dados de frequência de atualização do portal.

### Etapa F — qualidade e limitações

1. registrar métricas de qualidade disponíveis;
2. registrar incerteza e seu tipo;
3. registrar flags;
4. registrar ausências e máscaras;
5. identificar viés amostral ou de detecção;
6. identificar erros de classificação ou modelagem;
7. explicitar limitações de aplicação e interpretação.

### Etapa G — acesso operacional

1. registrar página do produto;
2. registrar download, API e serviços;
3. separar documentação, visualizador e acesso aos dados;
4. registrar formato, protocolo e autenticação;
5. verificar gratuidade, licença e atribuição;
6. verificar suporte a recorte, consulta e exportação;
7. testar links e registrar data e resultado.

### Etapa H — evidência

Para cada afirmação material, registrar:

- campo sustentado;
- valor;
- URL;
- tipo de evidência;
- nota explicativa;
- data de recuperação;
- confiança curatorial.

### Etapa I — auditoria

Avaliar separadamente:

- completude;
- precisão científica;
- precisão operacional;
- coerência interna;
- separação correta das entidades;
- qualidade das evidências;
- adequação da linguagem pública.

O produto somente pode ser promovido a `reviewed` ou `approved` após correções.

## 3. Prioridade de curadoria

### Prioridade P0

- produtos brasileiros de alta relevância;
- produtos com cobertura nacional;
- fontes públicas e institucionais;
- produtos com acesso operacional documentado;
- lacunas temáticas críticas do catálogo.

### Fontes iniciais recomendadas

1. MapBiomas;
2. TerraBrasilis / INPE;
3. IBGE;
4. ANA / SNIRH;
5. DATASUS;
6. INMET;
7. Embrapa;
8. ICMBio e MMA;
9. produtos internacionais com cobertura sistemática do Brasil.

## 4. Lotes e checkpoints

Recomendação operacional:

- lotes de 5 a 10 produtos, conforme complexidade;
- auditoria integral ao final de cada lote;
- nenhum novo lote antes de corrigir erros estruturais detectados;
- produtos de uma mesma família podem compartilhar evidências institucionais, mas não herdar silenciosamente resolução, período, método ou licença.

## 5. Saídas de cada lote

- registros normalizados;
- relatório de auditoria;
- evidências de metadados;
- lista de campos desconhecidos;
- lista de endpoints testados;
- correções do dicionário ou vocabulário;
- atualização das exportações públicas somente após validação.

## 6. Indicadores de progresso

- fontes com estratégia de enumeração definida;
- produtos resolvidos;
- releases explícitos;
- produtos com mensagem informacional válida;
- produtos com variáveis enumeradas;
- produtos com perfis espacial e temporal completos;
- produtos com qualidade e incerteza documentadas;
- distribuições testadas;
- afirmações materiais com evidência;
- registros aprovados.

O total bruto de linhas não deve ser usado isoladamente como indicador de avanço.

## 7. Proibições

- não tratar serviço ou catálogo como produto científico;
- não copiar descrições promocionais sem análise;
- não preencher resolução por inferência visual;
- não presumir gratuidade ou licença;
- não generalizar um produto para toda a fonte;
- não generalizar uma versão para a série completa;
- não registrar uso potencial como propriedade medida;
- não afirmar ausência de incerteza quando a documentação é desconhecida;
- não promover registros sem revisão.
