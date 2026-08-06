# DETER Cerrado — ambiguidade do identificador de metadado

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** I1-M2A  
**Entidade:** `PD-DETER-CER-ALERTS`

## Achado

O UUID `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830`, anteriormente observado em contexto oficial associado ao DETER Cerrado, também aparece em uma página oficial indexada do BIG GeoNetwork como referência ao componente **Incrementos no desmatamento** de um GeoPackage PRODES Amazônia Legal.

Os dois contextos são institucionalmente oficiais, mas semanticamente incompatíveis como identidade única de produto ou release.

## Interpretação segura

O achado comprova conflito contextual ou deriva de indexação. Ele não comprova:

- comprometimento da plataforma;
- reutilização intencional do registro;
- identidade do ativo;
- identidade da release atual;
- erro definitivo do produtor.

Até que o registro GeoNetwork seja recuperado diretamente e reconciliado, o UUID deve ser tratado somente como uma referência documental ambígua e datada.

## Impacto curatorial

O UUID não pode ser promovido como:

- identificador do produto DETER Cerrado;
- identificador de release;
- identificador de distribuição ou ativo;
- identificador de feição;
- prova suficiente de vínculo entre metodologia, pacote e release.

A promoção dependente permanece bloqueada.

## Evidências oficiais

1. Página do Programa BiomasBR sobre DETER, que apresenta o conjunto e sua orientação de citação no contexto do Cerrado.
2. Índice BIG GeoNetwork filtrado por GeoPackage, que associa o mesmo UUID ao componente de incrementos do PRODES Amazônia Legal.

## Correção implementada

Foi criado o contrato `database/mappings/deter_cerrado_metadata_identifier_ambiguity_guard_2026.json` e o validador `scripts/validate_deter_cerrado_metadata_identifier_ambiguity_guard.py`.

O gate exige:

- preservação dos dois contextos;
- ausência de escolha silenciosa entre eles;
- estados negativos para unicidade, estabilidade e identidade de produto/release/ativo;
- inspeção direta do registro GeoNetwork antes de qualquer promoção.

## Risco residual

Persistem sem resolução:

- assunto atual do registro GeoNetwork;
- causa do conflito;
- estabilidade histórica do UUID;
- vínculo com a release vigente;
- endpoint direto, bytes, checksum, licença e citação da release.
