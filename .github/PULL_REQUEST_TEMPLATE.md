## Resumo

Descreva a alteração e seu objetivo.

## Escopo

- [ ] dados canônicos
- [ ] produtos ou distribuições
- [ ] interface pública
- [ ] documentação
- [ ] validação ou infraestrutura

## Evidência e justificativa

Informe as fontes oficiais, decisões ou requisitos que sustentam a alteração. Para mudanças factuais, identifique os campos e registros afetados.

## Impacto

Explique o efeito para usuários, curadoria, esquema, derivados e releases.

## Validação

Liste os comandos executados e os resultados relevantes.

- [ ] `python3 scripts/build_catalog.py`
- [ ] `python3 scripts/validate_brazil_scope.py`
- [ ] `python3 scripts/validate_product_catalog.py`
- [ ] `python3 scripts/validate_frontend.py`
- [ ] `python3 scripts/build_site_artifact.py`

## Governança de dados

- [ ] editei arquivos-fonte, não JSONs derivados;
- [ ] preservei IDs e campos canônicos aplicáveis;
- [ ] atualizei classificações e contratos vinculados;
- [ ] não generalizei propriedades de produto para a fonte inteira;
- [ ] registrei a alteração pública no changelog.

## Fora do escopo

Registre explicitamente o que não foi alterado neste pull request.
