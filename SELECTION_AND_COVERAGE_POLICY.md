# Política de seleção, granularidade e cobertura

## 1. Objetivo

Explicitar por que uma entrada pertence ao catálogo, qual granularidade é útil, como duplicidades são evitadas e quais lacunas permanecem.

O catálogo não é declarado completo ou representativo de todo o universo de dados científicos.

## 2. Escopo territorial

O Brasil é o escopo central.

Prioridade:

1. organizações e fontes brasileiras;
2. ofertas internacionais com cobertura sistemática do Brasil;
3. ofertas com presença brasileira dependente de coleção ou projeto;
4. referências internacionais sem cobertura direta apenas quando possuem função estratégica documentada.

A prioridade territorial organiza a curadoria; não é nota de qualidade.

## 3. Unidade de seleção

A unidade elegível é uma **entrada de catálogo** com identidade oficial, governança identificável, utilidade científica e caminho verificável para dados ou metadados.

A entrada pode representar:

- fonte;
- plataforma;
- coleção;
- produto de dados;
- serviço de dados.

## 4. Critérios mínimos de inclusão

A entrada deve:

1. ter utilidade para pesquisa, ensino, extensão ou decisão baseada em dados;
2. oferecer dados, metadados ou descoberta estruturada;
3. possuir documentação oficial verificável;
4. ter organização ou governança identificável;
5. reduzir uma lacuna ou possuir função distinta;
6. permitir descrição honesta de escopo, acesso e limitações;
7. ter vínculo com o Brasil ou justificativa estratégica.

## 5. Granularidade

Criar subentrada somente quando existir diferença material em:

- significado ou escopo científico;
- modalidade de dados;
- cobertura espacial ou temporal;
- método ou finalidade;
- público ou uso;
- forma principal de acesso.

Não criar subentrada apenas por:

- arquivo;
- formato;
- layer;
- banda;
- endpoint;
- tabela interna;
- diretório;
- atualização técnica;
- release sem impacto material para descoberta.

Uma plataforma ampla pode permanecer como única entrada quando essa representação é suficiente para orientar o usuário.

## 6. Critérios de exclusão

Excluir ou não criar entrada para:

- notícias, blogs e páginas apenas editoriais;
- artigos isolados sem infraestrutura ou oferta de dados associada;
- mirror sem governança própria;
- ferramenta sem função de publicação, descoberta ou acesso;
- recurso descontinuado sem função independente;
- objeto cuja identidade não possui evidência suficiente;
- subdivisão técnica que apenas reproduz o catálogo da fonte;
- fonte internacional redundante e sem função estratégica.

## 7. Duplicidade e relação entre recursos

### Mesmo recurso, nomes diferentes

Manter uma entrada e preservar aliases.

### Organização e plataforma

Podem coexistir quando a plataforma possui identidade e utilidade próprias. Caso contrário, a organização pode ser apenas responsável pela entrada.

### Plataforma e coleção

Criar coleção separada somente quando melhora materialmente a descoberta e possui identidade oficial clara.

### Agregador e provedor

Podem coexistir, preservando a fonte original e evitando sugestão de equivalência.

### Sucessão

Manter a entrada ativa e registrar a anterior como histórica quando o recurso antigo apenas redireciona.

## 8. Brasil P0–P3

A classificação territorial continua auditável:

| Prioridade | Classe | Papel |
|---|---|---|
| `P0` | `fonte_brasileira` | núcleo |
| `P1` | `cobertura_brasil_sistematica` | complemento prioritário |
| `P2` | `cobertura_brasil_parcial` | presença dependente da entrada |
| `P3` | `referencia_sem_cobertura_brasil` | exceção estratégica |

A classificação não deve ser inferida apenas por domínio, idioma ou nome institucional.

## 9. Recursos bibliométricos e editoriais

Recursos bibliométricos, bases de literatura e redes de citação podem entrar apenas quando oferecem dados ou metadados estruturados com utilidade distinta para descoberta científica. Não devem ser apresentados como fontes de observações ambientais, nem receber decomposição interna em periódicos, artigos, arquivos ou índices técnicos.

Conteúdo apenas editorial, noticioso ou didático permanece fora do catálogo principal.

## 10. Candidatos

Novas entradas devem passar por triagem de:

- identidade;
- organização;
- tipo amplo;
- utilidade;
- cobertura do Brasil;
- duplicidade;
- granularidade;
- evidência oficial;
- decisão: incluir, fundir, excluir ou aguardar.

Uma URL fornecida autoriza triagem, não publicação automática.

## 11. Matriz de lacunas

A cobertura pode ser avaliada por:

- tema;
- região, bioma ou ecossistema;
- modalidade de dados;
- escala geográfica;
- natureza institucional;
- gratuidade e autenticação;
- presença de acesso programático;
- origem brasileira ou internacional.

Não é necessário medir quantidade de produtos, releases ou ativos internos da fonte.

## 12. Critérios de prioridade para expansão

Prioridade máxima:

- fontes públicas brasileiras;
- cobertura nacional ou de biomas brasileiros;
- lacunas em biodiversidade, clima, água, solo, florestas, agricultura, oceanografia, saúde ambiental, emissões e socioecologia;
- documentação estável;
- metadados reutilizáveis;
- utilidade demonstrável.

## 13. Revisão

- revisar duplicidades e granularidade antes de novos lotes;
- confirmar P0–P3 em cada ciclo;
- reavaliar anualmente recursos descontinuados ou renomeados;
- atualizar imediatamente sucessão e mudança institucional;
- justificar entradas P3 antes de uma versão estável.

## 14. Estado transitório

Os 51 registros atuais permanecem como autoridade pública transitória. A migração para `catalog_entries` deve preservar IDs, evidências e histórico, sem ampliar automaticamente cada fonte em múltiplos produtos internos.
