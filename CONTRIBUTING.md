# Como contribuir

Contribuições são bem-vindas para corrigir registros, propor novas fontes, melhorar a interface, ampliar a camada de produtos e fortalecer validações.

## Princípios

1. `data/data_resources.csv` na branch `main` é a fonte canônica.
2. JSONs e metadados derivados não devem ser editados manualmente.
3. Uma evidência deve sustentar a afirmação específica que será alterada.
4. Propriedades de produto ou distribuição não devem ser generalizadas para a fonte inteira.
5. Novas fontes devem demonstrar vínculo com o Brasil ou justificativa científica explícita.
6. Alterações significativas devem ocorrer em branch própria e pull request revisável.

## Propor uma nova fonte

A proposta deve incluir:

- nome oficial e instituição responsável;
- página institucional e página de acesso aos dados;
- vínculo territorial com o Brasil;
- descrição objetiva dos dados oferecidos;
- formatos e condições de acesso confirmados;
- licença ou indicação explícita de que ela não foi localizada;
- documentação oficial atual;
- evidência científica ou técnica representativa, quando disponível;
- limitações relevantes para uso acadêmico.

A proposta não entra automaticamente no CSV canônico. Ela deve passar por avaliação de escopo, revisão factual, validação e pull request.

## Corrigir um registro

Toda correção factual deve informar:

- `resource_id` afetado;
- campo atual;
- valor proposto;
- URL da evidência oficial;
- data de acesso;
- justificativa curta;
- impacto em produtos ou distribuições relacionados.

Artigos que demonstram uso científico não são evidência suficiente para confirmar licença, autenticação, endpoint ou versão atual. Para esses campos, prefira documentação oficial contemporânea.

## Fluxo de desenvolvimento

1. crie uma branch a partir de `main`;
2. limite o escopo da alteração;
3. edite somente arquivos-fonte;
4. execute as validações relevantes;
5. abra um pull request com resumo, motivação, impacto e testes;
6. aguarde CI verde e revisão antes da integração.

## Validações principais

```bash
python3 scripts/build_catalog.py
python3 scripts/validate_brazil_scope.py
python3 scripts/validate_product_catalog.py
python3 scripts/validate_frontend.py
python3 scripts/build_site_artifact.py
```

Validadores adicionais podem ser exigidos conforme o escopo da alteração.

## Alterações de dados

Ao editar `data/data_resources.csv`:

- preserve os `resource_id` existentes;
- não reutilize identificadores removidos;
- mantenha o número e a ordem dos campos canônicos;
- use valores coerentes com o codebook;
- atualize classificações e contratos vinculados;
- regenere artefatos derivados somente pelo workflow;
- atualize o changelog quando houver impacto público.

## Pull request

O pull request deve declarar:

- o que mudou;
- por que mudou;
- quais usuários ou registros são afetados;
- quais evidências sustentam a mudança;
- quais comandos de validação foram executados;
- o que permanece fora do escopo.

Alterações não relacionadas devem ser separadas em pull requests distintos.
