# Metodologia de curadoria

## 1. Escopo vigente

O foco ativo é a **Instância 1 — catálogo relacional de fontes e ofertas de dados científicos**.

A unidade de trabalho é uma entrada de catálogo de granularidade mínima suficiente. O objetivo é tornar a entrada útil para descoberta, compreensão e acesso, sem reproduzir toda a estrutura da fonte.

## 2. Unidades de registro

### Organização

Instituição, consórcio, rede ou iniciativa responsável.

### Entrada de catálogo

Fonte, plataforma, coleção, produto ou serviço exibido no catálogo.

### Variável ou tema

Conteúdo principal útil para busca e compreensão. Preserva o termo usado pela fonte.

### Evidência

Página oficial ou metadado que sustenta campos materiais.

### Conector

Configuração externa opcional para visualização futura.

## 3. Regra de granularidade

Criar nova entrada somente quando houver diferença material de significado, cobertura, método, finalidade, público ou acesso.

Não criar nova entrada apenas por arquivo, formato, layer, banda, endpoint, diretório ou atualização técnica.

## 4. Escopo geográfico

São prioritárias entradas com cobertura do Brasil ou associação territorial útil, incluindo:

- coordenadas, geometrias, pixels ou grades;
- bacias, biomas e unidades de conservação;
- códigos territoriais;
- séries por município, estado ou outra unidade geográfica;
- produtos internacionais com cobertura sistemática do país.

Uma tabela territorial pode ser georreferenciável mesmo em CSV ou XLSX.

## 5. Evidências

Priorizar:

1. página oficial;
2. metadados diretos;
3. documentação metodológica;
4. licença e termos;
5. citação recomendada;
6. documentação de API ou serviço apenas quando necessária.

Cada evidência sustenta apenas aquilo que documenta. Homepage não comprova automaticamente resolução, licença ou periodicidade.

## 6. Ficha essencial

Registrar, conforme disponibilidade:

- organização;
- nome oficial e acrônimo;
- tipo amplo;
- resumo e escopo científico;
- modalidades de dados;
- temas e variáveis principais;
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
- estado e data de verificação.

## 7. Significado científico proporcional

A descrição deve responder:

> O que a pessoa encontrará nesta fonte ou oferta de dados?

Não é necessário reconstruir a observação, o estimand, a população-alvo ou toda a cadeia metodológica. Registrar limitações somente quando evitam erro material de interpretação.

## 8. Espaço e tempo

Registrar cobertura, período, resolução ou suporte no nível em que a fonte os documenta e em que sejam úteis ao usuário.

Não transformar automaticamente cada conceito em entidade relacional. Texto estruturado é suficiente quando não há uso repetido em filtros.

## 9. Qualidade e incerteza

Registrar informações gerais de validação, qualidade ou incerteza quando forem apresentadas claramente pela fonte e forem relevantes para interpretar a entrada.

Não exigir perfil forense nem escore universal. `desconhecido` não equivale a `ausente`.

## 10. Acesso

Distinguir, quando possível:

- página oficial;
- metadados;
- acesso principal;
- metodologia;
- licença;
- citação.

Não é necessário enumerar todas as formas de download ou todos os endpoints.

`homepage_url` e `data_access_url` podem coincidir quando a mesma página realmente cumpre os dois papéis.

## 11. Conectores

APIs, WMS/WFS, STAC, Earth Engine e outros serviços são aprofundados somente para candidatos selecionados da Instância 2.

A existência de um conector não implica armazenamento ou harmonização do dataset.

## 12. Critério de parada

A curadoria termina quando:

1. a entrada é compreensível;
2. os campos essenciais disponíveis estão sustentados;
3. há caminho oficial para acesso;
4. lacunas relevantes estão explícitas;
5. detalhes adicionais não alterariam materialmente a ficha pública.

## 13. Estados curatoriais

- `needs_review`;
- `partially_verified`;
- `verified`;
- `not_found`;
- `not_applicable`.

Uma entrada pode ser verificada sem release, ativo, checksum, bytes ou schema físico.

## 14. Métricas

Medir:

- entradas prontas para o website;
- cobertura dos campos essenciais;
- links oficiais verificados;
- temas e variáveis identificados;
- duplicatas resolvidas;
- candidatos a conectores.

Não medir sucesso principalmente por quantidade de releases, assets, arquivos, claims, commits ou validadores.

## 15. Proibições

- não copiar dados externos;
- não reconstruir catálogos de terceiros;
- não inventariar arquivos e layers por padrão;
- não criar taxonomia universal do zero;
- não inferir valores ausentes;
- não transformar padrão ou literatura em expansão automática do esquema;
- não prolongar a curadoria apenas porque há mais documentação disponível.
