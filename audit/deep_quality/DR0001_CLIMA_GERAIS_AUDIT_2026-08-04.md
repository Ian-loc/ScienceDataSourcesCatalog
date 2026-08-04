# Auditoria aprofundada — DR0001 Clima Gerais

**Data da verificação:** 2026-08-04 16:23 BRT  
**Registro:** `DR0001`  
**Fonte auditada:** Plataforma Mineira para Adaptação às Mudanças Climáticas — Clima Gerais  
**Estado:** auditada com correções propostas; produtos internos ainda precisam ser individualizados

## 1. Identidade e natureza

A Clima Gerais é uma **plataforma pública estadual de apoio ao planejamento climático municipal**, apresentada como produto do Plano de Energia e Mudanças Climáticas de Minas Gerais. Sua missão institucional inclui compartilhar informações sobre mudanças climáticas em Minas Gerais, divulgar boas práticas e direcionar municípios a apoios técnicos e financeiros.

Não deve ser representada como um único dataset. A plataforma reúne ao menos os seguintes objetos distintos:

1. módulo de vulnerabilidade municipal e territorial;
2. estimativas municipais de gases de efeito estufa;
3. base de boas práticas;
4. diretório de apoios técnicos e financeiros;
5. material conceitual e institucional.

**Classificação recomendada do registro DR0001:** fonte/plataforma institucional. Os módulos com conteúdo estruturado devem ser registrados como produtos separados.

## 2. Produto de dados verificado nesta rodada

### Índice Mineiro de Vulnerabilidade Climática — resultados municipais e territoriais

A página oficial informa que o índice de vulnerabilidade é composto por:

- sensibilidade;
- exposição;
- capacidade de adaptação.

A consulta cobre os **853 municípios de Minas Gerais** e também territórios de desenvolvimento. A página oferece uma tabela XLSX do banco completo por link de download.

O próprio produtor adverte que o índice:

- não deve ser usado como parâmetro único de decisão;
- é ferramenta de apoio ao planejamento territorial;
- requer estudos locais mais detalhados.

A literatura técnica localizada descreve os indicadores como oriundos de bases estaduais e federais e padronizados para a faixa de 0 a 1. Essa informação deve ser confirmada na documentação metodológica original antes de migrar para campos canônicos de método.

## 3. Cobertura, suporte e temporalidade

- **Cobertura geográfica:** Estado de Minas Gerais.
- **Unidade espacial principal:** município; há também agregação por território de desenvolvimento.
- **Suporte espacial:** unidade administrativa/agregada, não pixel e não observação individual.
- **População/universo:** 853 municípios mineiros no módulo municipal.
- **Temporalidade:** o portal e materiais associados apontam origem do índice em 2014–2015. Não foi localizada nesta rodada uma política pública de atualização periódica do índice nem data de release claramente exposta na página do produto.
- **Data de publicação do portal:** rodapé `©2014-15`; isso não prova a data de atualização de cada indicador.

O registro não deve usar `varia conforme o indicador` como substituto de uma data ou release do produto. Deve declarar que a edição/data dos indicadores precisa ser verificada no arquivo e na metodologia.

## 4. Formatos e acesso

### Testes executados

| Recurso | Resultado em 2026-08-04 |
|---|---|
| Homepage `https://clima-gerais.meioambiente.mg.gov.br/` | página institucional indexada e operacional; uma tentativa automatizada apresentou timeout transitório |
| Vulnerabilidade territorial | página HTML acessível e com consulta municipal/territorial |
| Download da tabela completa | link XLSX identificado na página; o cliente automatizado não conseguiu concluir o download por falha de cache, portanto o conteúdo do arquivo ainda requer teste direto |
| API documentada | não localizada |
| WMS/WFS/STAC | não localizados |
| Autenticação | não exigida para consulta pública |

### Distinção de papéis dos links

- `homepage_url`: homepage da plataforma;
- `data_access_url`: página específica de vulnerabilidade territorial;
- futuro ativo/distribuição: URL direta da tabela XLSX;
- metodologia: deve receber link próprio quando localizado;
- licença: deve receber link ou texto próprio quando localizado.

## 5. Licença e redistribuição

A página exibe aviso de direitos reservados de concepção e produção. Não foi localizada licença aberta explícita para redistribuição da tabela ou criação de derivados. Portanto:

- não registrar simplesmente `público` como licença;
- separar `acesso público` de `licença de reutilização`;
- usar estado controlado `não localizada` até obter termos oficiais;
- evitar republicar o XLSX sem confirmação de permissão.

## 6. Autoria e gestão

- plataforma associada à FEAM/SISEMA/Governo de Minas Gerais;
- a homepage informa apoio da Agência Francesa de Desenvolvimento;
- página temática atual da SEMAD/SISEMA lista Clima Gerais e o IMVC entre os trabalhos estaduais de sustentabilidade, energia e mudanças climáticas.

A autoria de cada produto e edição deve ser registrada no nível do produto/documento, não herdada genericamente para todos os módulos.

## 7. Evidência e usos científicos

Uso defensável:

- planejamento territorial climático;
- ensino e comunicação sobre vulnerabilidade e adaptação;
- seleção preliminar de municípios/territórios para estudos locais;
- estudos metodológicos sobre índices compostos, desde que a edição e as variáveis sejam fixadas.

Usos que exigem cautela:

- comparação temporal, porque não foi verificada uma série versionada;
- inferência individual, porque o suporte é municipal/territorial;
- uso como medida única de risco ou vulnerabilidade;
- combinação analítica sem recuperar os anos, fontes e regras de normalização dos indicadores.

## 8. Não conformidades do registro canônico atual

1. `official_identity` é genérico e não informa que se trata de produto do PEMC.
2. `description` reduz a plataforma ao módulo de indicadores.
3. `data_product_types` mistura mapas, indicadores e visualizações sem distinguir módulos.
4. `data_formats` omite a tabela XLSX explicitamente oferecida.
5. `spatial_resolution` e campos temporais são vagos demais para o produto verificado.
6. `programmatic_access=desconhecido` e `access_protocols=não documentado` podem ser substituídos por `não localizado` após pesquisa.
7. `license=público` confunde acesso público com licença; deve ser `não localizada`.
8. `academic_uses` menciona emissões locais sem que o módulo tenha sido auditado nesta rodada.
9. `last_verified` precisa ser atualizado somente após incorporação das correções.

## 9. Correção proposta para DR0001

A correção estruturada está em:

`audit/deep_quality/DR0001_CLIMA_GERAIS_CORRECTION_PROPOSAL_2026-08-04.csv`

Ela mantém DR0001 como plataforma/fonte, limita afirmações ao que foi verificado e prepara a individualização posterior dos produtos.

## 10. Pendências antes de marcar a fonte como integralmente concluída

1. baixar e inspecionar a tabela XLSX completa;
2. localizar e auditar a metodologia original do IMVC;
3. registrar o módulo IMVC como produto próprio, com release e distribuição;
4. auditar separadamente as estimativas municipais de GEE;
5. auditar a base de boas práticas e diretórios de apoio;
6. confirmar termos de uso/licença e citação recomendada;
7. reconciliar a planilha canônica após a correção ser incorporada à autoridade material.

## 11. Fontes oficiais consultadas

- https://clima-gerais.meioambiente.mg.gov.br/
- https://clima-gerais.meioambiente.mg.gov.br/vulnerabilidade-territorial
- https://clima-gerais.meioambiente.mg.gov.br/conceitos-basicos
- https://meioambiente.mg.gov.br/w/sustentabilidade-energia-e-mudancas-climaticas

## 12. Fontes de apoio

- Plano Estadual de Ação Climática de Minas Gerais, 2023 — contextualiza a plataforma e o IMVC;
- estudo posterior de análise fatorial do IMVC — usado somente como evidência secundária e não como substituto da metodologia original.
