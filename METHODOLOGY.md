# Metodologia de curadoria

## Escopo

A unidade de registro é a **fonte**: plataforma, infraestrutura, repositório, rede, sistema, catálogo, software de publicação ou base de dados. O catálogo não registra cada dataset individual como uma linha.

## Evidências

A revisão prioriza: documentação oficial; páginas oficiais de acesso, API, licença e termos; documentação técnica do gestor; e artigos revisados por pares que descrevem ou utilizam a fonte.

Cada afirmação deve ser sustentada no nível adequado. Uma homepage pode comprovar identidade, mas não necessariamente API, formato, resolução, licença ou atualização. DATA1-BR-CLOSE usa uma tabela longa, permitindo várias evidências por fonte e dimensão.

## Áreas de pesquisa

`research_areas` usa nove categorias condensadas: Ciências Ambientais e Ecologia; Biodiversidade e Conservação; Clima e Ciências Atmosféricas; Geociências, Solos e Geografia Física; Recursos Hídricos e Oceanografia; Agricultura, Florestas e Uso da Terra; Sensoriamento Remoto e Geoinformação; Infraestruturas e Ciência de Dados; Planejamento Territorial e Políticas Públicas.

A estrutura foi inspirada, sem correspondência normativa, na CAPES e no Web of Science. O objetivo é navegação. Temas específicos permanecem em `keywords`.

## Acesso

`programmatic_access` informa se existe consulta ou transferência automatizada documentada. O esquema 0.8.0 separa:

- `access_protocols`: REST, OGC, STAC, S3, openEO, Earth Engine API, DataONE API, OAI-PMH e serviços equivalentes;
- `access_tools`: pacotes R/Python, clientes de linha de comando, ambientes em nuvem e exportadores web;
- `data_formats`: formatos dos arquivos ou representações entregues.

Pacote cliente não é, por si só, API do provedor. Serviço OGC não é REST API. Download manual não é acesso programático. Ausência de documentação resulta em `desconhecido`, não em `não`.

### Papéis dos links

- `homepage_url`: página institucional, página “Sobre” ou página oficial dedicada à fonte;
- `data_access_url`: catálogo, busca, visualizador, solicitação ou download;
- `access_documentation_url`: API, protocolo, credenciais ou instruções técnicas.

URLs iguais entram em revisão. A igualdade só pode permanecer como exceção documentada quando uma única página cumpre realmente os dois papéis. `data_access_url = não se aplica` é reservado a recursos sem dados próprios para consulta ou download.

## Cobertura do Brasil

`covers_brazil` usa: `sim`, `parcial`, `não`, `não se aplica` e `desconhecido`, conforme a cobertura explícita e a aplicabilidade territorial da fonte.

## Prioridade e execução

A prioridade científica usa somente impacto e risco científico comparáveis. Número de alertas, número de dimensões, ausência de documentação e problemas de links não aumentam a prioridade científica.

A ordem operacional é controlada separadamente por ondas. Portões de escopo, links e documentação podem antecipar o trabalho, mas não alteram a classificação científica.

## Limite da auditoria

“Verificado” significa confrontado com as evidências disponíveis na data indicada. Não certifica todos os datasets hospedados nem garante disponibilidade futura. CI verde demonstra coerência interna, não correção factual externa.