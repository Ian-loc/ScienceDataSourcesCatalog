# Política de comparabilidade, evidência e inferência científica

**Status:** guardrail futuro; documento somente para leitura nesta fase  
**Aplicação ativa atual:** nenhuma operação analítica nova  
**Dependência:** consolidação da Instância 1 e definição posterior da Instância 2

## 1. Situação

Esta política preserva limites científicos para futuras capacidades de composição, comparação e análise. Ela não constitui um workstream ativo e não autoriza a implementação imediata de motores de compatibilidade, correlação, regressão, causalidade ou síntese automática de relações.

O foco vigente do projeto é a **Instância 1 — Catálogo relacional científico-operacional**.

A Instância 1 deve fornecer os metadados necessários para que decisões futuras sejam possíveis:

- definição do produto;
- variáveis e classes;
- população ou objeto observado;
- suporte espacial e temporal;
- método;
- qualidade e incerteza;
- versão;
- proveniência;
- licença;
- acesso operacional.

## 2. Princípios preservados

1. Sobreposição cartográfica não constitui harmonização.
2. Coincidência espacial não constitui associação estatística.
3. Associação não demonstra mecanismo ou causalidade.
4. Compatibilidade depende da operação e da pergunta, não é atributo absoluto de um par de produtos.
5. Escala, suporte, período, método e população fazem parte do significado do dado.
6. Produtos derivados da mesma fonte podem compartilhar dependências.
7. Evidência contraditória e limitações devem permanecer visíveis.
8. Automação não substitui julgamento científico.
9. Dados sociais e de saúde exigem proteção ética e contra reidentificação.
10. A linguagem pública deve ser proporcional à evidência.

## 3. Instância 2 — composição geográfica futura

Uma futura Instância 2 poderá permitir:

- composição visual;
- mapas sincronizados;
- perfis territoriais;
- recortes e transformações documentadas;
- verificação de executabilidade técnica;
- transparência de diferenças entre produtos.

A Instância 2 não deverá atribuir compatibilidade científica universal.

A execução técnica poderá considerar:

- georreferenciamento;
- CRS;
- formato;
- extensão;
- disponibilidade do endpoint;
- licença;
- recursos computacionais;
- necessidade de processamento.

Diferenças científicas deverão ser comunicadas por perfis e sinalizadores, não convertidas automaticamente em aprovação ou reprovação total.

## 4. Instância 3 — contexto científico futuro

Uma futura Instância 3 poderá apresentar sínteses breves e auditáveis da literatura sobre os fenômenos representados em uma composição escolhida pelo usuário.

Ela deverá:

- usar os perfis estruturados da Instância 1;
- considerar território, escala e período;
- priorizar literatura aplicável ao Brasil;
- distinguir evidência direta, análoga e metodológica;
- comunicar mecanismos discutidos, controvérsias e confundidores;
- não gerar perguntas para o usuário;
- não usar a visualização como evidência de associação;
- ligar afirmações a referências verificáveis.

## 5. Níveis conceituais preservados

Para comunicação futura, permanecem úteis as distinções:

- **N0 — composição visual:** produtos exibidos conjuntamente;
- **N1 — coocorrência descritiva:** coincidência espacial ou temporal descrita;
- **N2 — associação exploratória:** associação estimada em dados selecionados;
- **N3 — associação robusta condicionada:** persistência após diagnósticos;
- **N4 — mecanismo sustentado:** evidência teórica e empírica consistente;
- **N5 — inferência causal condicionada:** desenho e pressupostos explícitos.

A Instância 1 não atribui nenhum desses níveis. Ela apenas registra os metadados que poderão sustentar avaliações futuras.

## 6. Condições para reativação desta política

A política somente deve voltar ao estado ativo quando:

1. o PostgreSQL/PostGIS for promovido a fonte canônica;
2. produtos prioritários possuírem perfis científicos aprovados;
3. variáveis, métodos, escalas e incertezas estiverem estruturados;
4. a Instância 2 possuir escopo e operações explicitamente definidos;
5. casos de teste forem aprovados;
6. revisão científica humana estiver incorporada à governança.

## 7. Regra vigente

> Durante a consolidação da Instância 1, esta política serve apenas para impedir que o modelo de dados feche caminhos futuros ou autorize prematuramente interpretações analíticas.

A documentação ativa da fase atual está em `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`.
