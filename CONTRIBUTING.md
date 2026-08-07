# Como contribuir

Contribuições são bem-vindas para corrigir entradas, propor novas fontes ou ofertas de dados, melhorar a interface e fortalecer validações.

## 1. Princípios

1. A `main` é a autoridade incorporada.
2. Os CSV/JSON atuais continuam sustentando a interface pública durante a transição.
3. A unidade futura é `catalog_entry`, de granularidade mínima suficiente.
4. O Simbiotrama não copia datasets externos nem reconstrói catálogos de terceiros.
5. Evidência deve sustentar o campo material alterado.
6. Nomes e definições da fonte devem ser preservados.
7. Novas entradas devem possuir vínculo com o Brasil ou justificativa estratégica.
8. Mudanças significativas devem ocorrer em branch própria e PR revisável.

## 2. Gate de escopo

Antes de propor entidade, coluna, vocabulário ou novo nível de entrada, informe qual função será melhorada:

- descoberta no catálogo;
- interpretação mínima;
- filtro ou exibição no website;
- conector externo selecionado.

A proposta permanece fora do núcleo quando serve apenas para:

- reconstruir genealogia;
- enumerar arquivos, layers, bandas ou endpoints;
- modelar ontologia universal;
- antecipar harmonização ou análise;
- reproduzir metadados que já pertencem à fonte.

## 3. Propor uma entrada

A proposta deve incluir, conforme disponibilidade:

- organização responsável;
- nome oficial e tipo amplo;
- resumo do que oferece;
- modalidades, temas e variáveis principais;
- cobertura espacial e temporal;
- resolução ou suporte quando material;
- página oficial;
- metadados;
- acesso principal;
- gratuidade e autenticação;
- metodologia, licença e citação quando disponíveis;
- limitações relevantes;
- data da verificação.

Não é necessário enumerar todos os produtos, releases, arquivos ou serviços internos.

## 4. Justificar granularidade

Uma nova entrada somente deve ser criada quando existe diferença material de:

- significado científico;
- modalidade de dados;
- cobertura;
- método ou finalidade;
- público ou uso;
- caminho principal de acesso.

Outro arquivo, formato, layer, banda, endpoint ou atualização técnica não é justificativa suficiente.

## 5. Corrigir uma entrada

Informe:

- identificador afetado;
- campo atual;
- valor proposto;
- URL oficial;
- data de acesso;
- justificativa;
- impacto sobre a apresentação ou busca.

Artigo de aplicação não confirma automaticamente licença, autenticação ou disponibilidade atual.

## 6. Fluxo de desenvolvimento

1. consulte o SHA atual da `main`;
2. crie a branch;
3. confirme que a branch existe;
4. somente então escreva;
5. limite o escopo;
6. execute as validações;
7. inspecione o diff;
8. abra PR em draft;
9. aguarde CI e revisão completos;
10. corrija threads;
11. congele o head;
12. solicite autorização do SHA exato.

Nunca use a `main` como fallback quando uma branch não for encontrada.

## 7. Validações principais

```bash
python3 scripts/build_catalog.py
python3 scripts/validate_brazil_scope.py
python3 scripts/validate_product_catalog.py
python3 scripts/validate_scientific_direction.py
python3 scripts/validate_frontend.py
python3 scripts/build_site_artifact.py
```

Validadores adicionais devem ser proporcionais ao risco. Evite testes baseados apenas na presença de palavras quando uma regra estrutural puder ser testada diretamente.

## 8. Alterações de dados

Ao editar os CSVs atuais:

- preserve identificadores;
- não reutilize IDs removidos;
- mantenha o schema canônico vigente;
- atualize contratos vinculados;
- regenere derivados pelo workflow;
- atualize o changelog quando houver impacto público.

A existência de uma linha nos pilotos de produtos ou distribuições não obriga sua promoção como entrada futura.

## 9. Pull request

O PR deve declarar:

- objetivo;
- função pública melhorada;
- justificativa de granularidade;
- arquivos alterados;
- evidências;
- testes;
- casos adversariais relevantes;
- estados negativos e bloqueios;
- itens explicitamente fora do escopo.

Alterações arquiteturais, curadoria de entradas e interface devem ser separadas quando puderem ser revisadas independentemente.
