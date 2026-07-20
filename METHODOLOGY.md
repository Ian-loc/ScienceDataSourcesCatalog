# Metodologia de curadoria

## Escopo

A unidade de registro é a **fonte**: plataforma, infraestrutura, repositório, rede, sistema, catálogo, software de publicação ou base de dados. O catálogo não registra cada dataset individual como uma linha.

## Evidências

A revisão prioriza documentação oficial, páginas de acesso/API/licença/termos, documentação técnica do gestor e artigos revisados por pares que descrevem ou utilizam a fonte.

Cada afirmação deve ser sustentada no nível adequado. Homepage pode comprovar identidade, mas não necessariamente API, formato, resolução, licença ou atualização. DATA1-EXT usa tabela longa, permitindo várias evidências por fonte e dimensão.

## Áreas de pesquisa

`research_areas` usa nove categorias condensadas: Ciências Ambientais e Ecologia; Biodiversidade e Conservação; Clima e Ciências Atmosféricas; Geociências, Solos e Geografia Física; Recursos Hídricos e Oceanografia; Agricultura, Florestas e Uso da Terra; Sensoriamento Remoto e Geoinformação; Infraestruturas e Ciência de Dados; Planejamento Territorial e Políticas Públicas.

A estrutura é inspirada, sem correspondência normativa, na CAPES e no Web of Science. Serve à navegação; temas específicos permanecem em `keywords`.

## Acesso

`programmatic_access` informa se existe consulta ou transferência automatizada documentada. Ausência de documentação resulta em `desconhecido`, não em `não`.

No esquema canônico **0.7.0**, `access_protocols` ainda reúne protocolos e alguns clientes ou pacotes porque `access_tools` não existe. Na proposta **0.8.0**:

- `access_protocols`: REST, OGC, STAC, S3, openEO, OData, WebDAV, OAI-PMH, DataONE API, Earthdata CMR API, Earth Engine API e mecanismos técnicos equivalentes;
- `access_tools`: pacotes R/Python, clientes de linha de comando, Google Earth Engine, exportadores web e ambientes em nuvem;
- `data_formats`: somente formatos de arquivo, serialização ou pacote;
- `visualization_types`: somente formas de apresentação.

Pacote cliente não é, por si só, API do provedor. Serviço OGC não é REST API. Download manual não é acesso programático.

### Papéis dos links

- `homepage_url` — **Site oficial**: página institucional ou página Sobre;
- `data_access_url` — **Acessar dados**: catálogo, busca, visualizador, solicitação ou download;
- `access_documentation_url`: API, protocolo, autenticação ou instruções técnicas.

URLs iguais entram em revisão. A igualdade só pode permanecer como exceção documentada quando uma única página cumpre realmente os dois papéis. `data_access_url = não se aplica` é reservado a recursos sem dados próprios.

## Cobertura do Brasil

`covers_brazil` usa `sim`, `parcial`, `não`, `não se aplica` e `desconhecido`, conforme a cobertura explícita e a aplicabilidade territorial.

## Prioridade e execução

A prioridade científica usa somente impacto e risco comparáveis. Número de alertas, número de dimensões, ausência de documentação e problemas de links não aumentam a prioridade científica.

A ordem operacional é controlada por ondas. Portões de escopo, links e documentação podem antecipar o trabalho, mas não alteram a classificação científica.

## Limite da auditoria

“Verificado” significa confrontado com as evidências registradas na data indicada. Não certifica todos os datasets nem garante disponibilidade futura. CI verde demonstra coerência interna, não correção factual externa.