# Metodologia de curadoria

## Escopo

A unidade de registro é a **fonte**: plataforma, infraestrutura, repositório, rede, sistema, catálogo, software de publicação ou base de dados. O catálogo não registra cada dataset individual como uma linha.

## Evidências

A revisão usa quatro camadas, em ordem de prioridade:

1. autodescrição e documentação oficial;
2. páginas oficiais de acesso, API, licença e termos;
3. documentação técnica do órgão gestor;
4. artigos revisados por pares que descrevem ou utilizam a fonte.

A identidade oficial preserva o vocabulário da própria fonte. A evidência acadêmica é representativa e serve para confrontar autodescrição, uso efetivo, formatos e limitações; ela não constitui revisão sistemática completa de todas as citações.

Cada linha informa o tipo, URL e síntese da evidência acadêmica/técnica. Quando não foi localizada publicação específica robusta, a documentação oficial é mantida e essa limitação é declarada.

## Áreas de pesquisa

O campo `research_areas` usa nove categorias condensadas:

- Ciências Ambientais e Ecologia
- Biodiversidade e Conservação
- Clima e Ciências Atmosféricas
- Geociências, Solos e Geografia Física
- Recursos Hídricos e Oceanografia
- Agricultura, Florestas e Uso da Terra
- Sensoriamento Remoto e Geoinformação
- Infraestruturas e Ciência de Dados
- Planejamento Territorial e Políticas Públicas

A estrutura foi inspirada, sem correspondência normativa, na [Tabela de Áreas do Conhecimento/Avaliação da CAPES](https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/avaliacao/instrumentos/documentos-de-apoio/tabela-de-areas-de-conhecimento-avaliacao) e nas [Research Areas do Web of Science](https://webofscience.help.clarivate.com/en-us/Content/research-areas.html). O objetivo é navegação, não enquadramento institucional. Temas específicos permanecem em `keywords`.

## Acesso

`programmatic_access` não significa apenas REST API. O campo informa se existe forma documentada de consulta ou transferência automatizada. `access_protocols` discrimina REST, OGC, STAC, S3, openEO, Earth Engine, pacotes R/Python, downloads HTTP e outros mecanismos.

Serviços OGC não são rotulados como REST API. Download manual não é acesso programático. Ausência de documentação resulta em `desconhecido`, não em `não`.

## Cobertura do Brasil

`covers_brazil` responde se a fonte possui dados aplicáveis ao território brasileiro:

- `sim`: cobertura explícita, global ou continental que inclui o Brasil;
- `parcial`: presença possível ou dependente dos datasets depositados;
- `não`: cobertura declarada exclui o Brasil;
- `não se aplica`: software ou base sem cobertura geográfica pertinente;
- `desconhecido`: evidência insuficiente.

## Utilidade e limitações

A utilidade acadêmica considera descoberta, ensino, download, integração, séries temporais, reprodutibilidade, escala e comparação entre estudos. As limitações destacam viés amostral, resolução, atualização, cobertura desigual, produtos modelados, credenciais, cotas, licenças e ausência de acesso integral.

## Limite da auditoria

“Verificado” significa confrontado com as evidências disponíveis na data indicada. Não significa certificação da qualidade de todos os datasets hospedados, nem garante disponibilidade futura de serviços externos.
