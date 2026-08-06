# Política de escopo e granularidade da Instância 1

## Finalidade

Evitar expansão indevida de escopo, reconstrução de plataformas externas e proliferação de entidades durante a construção do catálogo.

## Pergunta de controle

Antes de pesquisar, criar ou alterar uma entrada, responder:

> Qual informação mínima o usuário precisa para descobrir, compreender e acessar esta oferta de dados científicos?

Qualquer trabalho além dessa resposta exige justificativa explícita.

## Critério de entrada concluída

Uma entrada está suficientemente curada quando o catálogo consegue informar, com evidência proporcional:

1. quem oferece;
2. o que é;
3. quais tipos de dados oferece;
4. quais variáveis ou grupos de variáveis inclui;
5. onde e quando se aplica;
6. como acessar;
7. se o acesso é gratuito e se exige autenticação;
8. quais links oficiais sustentam a ficha;
9. qual licença e citação se aplicam no nível informado;
10. se existe conector selecionado para uso futuro.

Não são requisitos gerais de conclusão:

- release atual inequívoca;
- enumeração de arquivos;
- inventário de layers;
- checksum;
- inspeção de bytes;
- esquema físico completo;
- licença por arquivo;
- citação por ativo;
- genealogia integral do produto.

Esses itens só entram quando forem indispensáveis para a compreensão da entrada ou para um conector específico.

## Limite de pesquisa

A pesquisa deve seguir esta ordem:

1. página oficial da instituição ou oferta;
2. metadados diretos fornecidos pela fonte;
3. página principal de acesso;
4. metodologia, licença e citação quando necessárias à ficha;
5. documentação de conector somente quando houver caso de uso aprovado.

Parar quando os campos essenciais estiverem sustentados. Não perseguir todas as ramificações, downloads e serviços da plataforma.

## Regra de classificação

Usar apenas tipos amplos:

- `source`;
- `platform`;
- `collection`;
- `data_product`;
- `data_service`.

Classificações mais específicas devem permanecer como texto ou metadado adicional, salvo necessidade comprovada de filtro recorrente.

## Regra de variáveis

- preservar o rótulo e a definição da fonte;
- usar grupos amplos para busca;
- não criar taxonomia universal do zero;
- não inferir equivalência entre variáveis de fontes diferentes;
- não enumerar todas as bandas ou colunas quando uma descrição agregada é suficiente.

## Regra de links

Priorizar poucos links com papéis claros:

- página oficial;
- metadados;
- acesso principal;
- metodologia;
- licença;
- citação.

Não cadastrar todos os links internos disponíveis. Um único link pode cumprir mais de um papel quando a própria página os reúne.

## Regra de conectores

Conectores são opcionais e preparados para a Instância 2. Devem registrar somente:

- tipo do conector;
- endpoint ou identificador externo;
- autenticação;
- operação selecionada;
- estado e data do teste.

A existência de conector não transforma endpoint, layer ou arquivo em nova entrada obrigatória do catálogo.

## Escopo negativo permanente

A Instância 1 não deve:

- copiar ou hospedar dados externos;
- reconstruir catálogos de terceiros;
- enumerar portfólios completos sem justificativa;
- criar genealogias detalhadas;
- modelar cada arquivo, layer, banda ou endpoint;
- inventar classificações não oferecidas pela fonte;
- converter desconhecido em `não`;
- tratar documentação técnica como obrigação de catalogação integral;
- expandir Instâncias 2 ou 3 dentro de pacotes da Instância 1.

## Gate de prevenção de escopo

Todo PR da Instância 1 deve declarar:

- qual entrada ou regra mínima está sendo alterada;
- por que cada nova tabela ou campo é necessário;
- quais alternativas mais simples foram consideradas;
- quais partes da plataforma externa foram deliberadamente deixadas fora;
- como o delta melhora descoberta, compreensão ou acesso;
- por que o pacote não reconstrói a fonte externa.

Sem essa declaração, o PR permanece bloqueado.
