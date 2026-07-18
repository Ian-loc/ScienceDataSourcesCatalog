# Workflow de verificação do catálogo

## Governança

A única fonte canônica é `data/data_resources.csv`. O JSON do site é gerado no build. A planilha do Drive não deve ser mantida em paralelo.

## Revisão por fonte

1. confirmar nome, identidade, objetivo e responsável na documentação oficial;
2. testar página institucional, acesso aos dados e documentação programática;
3. conferir produtos, formatos, visualizações, cobertura e resoluções;
4. distinguir download manual, acesso programático, autenticação e restrições;
5. localizar artigo revisado por pares que descreva ou use a fonte;
6. registrar evidência técnica quando não houver artigo específico robusto;
7. revisar utilidade acadêmica e limitações;
8. atualizar `last_verified` apenas na linha efetivamente conferida.

## Evidência

Não usar um artigo apenas porque menciona o tema. A publicação deve descrever a infraestrutura, usar dados identificáveis da fonte ou avaliar suas condições. O tipo de evidência deve diferenciar artigo revisado por pares, artigo técnico, documentação técnica oficial e documentação oficial.

## Controle automático

Execute:

```bash
python3 scripts/build_catalog.py
```

O script bloqueia esquema divergente, campos obrigatórios vazios, IDs ou nomes duplicados, URLs essenciais inválidas, categorias fora dos valores controlados, áreas de pesquisa desconhecidas e datas malformadas. O workflow repete a validação em todo pull request e antes do deploy.

## Frequência

- trimestral: links, acesso, autenticação e disponibilidade;
- anual: conteúdo, evidência acadêmica, versões e áreas;
- imediata: mudança de licença, API, formato, cobertura ou responsável;
- por pull request: validação estrutural e inspeção científica do diff.

A checagem de links deve interpretar 401, 403 e 429 com cautela: bloqueio a robôs não prova indisponibilidade para usuários.
