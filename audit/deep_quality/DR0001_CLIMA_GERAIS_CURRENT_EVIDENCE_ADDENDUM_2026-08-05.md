# Adendo de evidência atual — DR0001 Clima Gerais / IMVC

**Data e hora da verificação:** 2026-08-05 15:24:52, `America/Sao_Paulo`  
**Registro legado:** `DR0001`  
**Estado:** evidência atual ampliada; sem promoção e sem substituição da linha canônica

## 1. Achados oficiais novos

A página atual da SEMAD/SISEMA dedicada ao **Índice Mineiro de Vulnerabilidade Climática (IMVC)** informa que:

- o IMVC foi atualizado em junho de 2024;
- o produto representa vulnerabilidade municipal às mudanças climáticas;
- a construção segue três dimensões: sensibilidade, exposição e capacidade de adaptação;
- a página oferece acesso separado a metadados dos anos 2024, 2017 e 2015;
- os resultados de 2024 são apresentados como edição própria e não como simples atualização indistinta da plataforma Clima Gerais.

Fonte oficial verificada:

- `https://meioambiente.mg.gov.br/w/indice-mineiro-de-vulnerabilidade-climatica-1`

A página legada de vulnerabilidade territorial da Clima Gerais continua operacional e expõe uma URL direta de planilha XLSX:

- página: `https://clima-gerais.meioambiente.mg.gov.br/vulnerabilidade-territorial`;
- planilha: `https://clima-gerais.meioambiente.mg.gov.br/arquivos/tabela%20vulnerabilidade/Clima_Gerais_I%CC%81ndice_de_Vulnerabilidade_Municipal_MG_versa%CC%84o_completa.xlsx`.

A resposta HTTP identificada para o recurso é compatível com XLSX (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`). O arquivo não foi inspecionado nesta rodada; portanto, nomes de abas, variáveis, datas, fórmulas, valores, tamanho, checksum e licença permanecem não verificados.

## 2. Consequência para resolução de entidade

O estado anterior que tratava a temporalidade do IMVC como não localizada deve ser refinado:

- **Clima Gerais** permanece classificada como fonte/plataforma;
- **IMVC 2024** deve ser modelado como produto ou release individualizado;
- **IMVC 2017** e **IMVC 2015** devem ser tratados como edições históricas próprias, condicionadas à inspeção de seus metadados;
- a planilha XLSX legada deve ser tratada como distribuição/ativo candidato, sem pressupor que corresponda automaticamente à edição 2024;
- a data de atualização da página ou do portal não pode substituir a data/versão do produto.

## 3. Campos agora resolvidos com evidência oficial

Para o futuro produto IMVC:

- `producer_scope`: SEMAD/SISEMA / Governo de Minas Gerais;
- `scientific_object`: vulnerabilidade climática municipal;
- `primary_spatial_support`: município;
- `dimensions`: sensibilidade, exposição e capacidade de adaptação;
- `verified_release_years`: 2024, 2017 e 2015, como edições/metadados anunciados separadamente;
- `current_release_note`: atualização de junho de 2024;
- `decision_support_role`: apoio técnico a políticas públicas de adaptação, sem uso como parâmetro único.

## 4. Campos ainda bloqueados

Permanecem sem promoção:

- correspondência entre a planilha XLSX legada e a edição 2024;
- definição e lista integral dos indicadores;
- fontes, anos e regras de atualização dos indicadores;
- normalização, ponderação e fórmula vigentes;
- tratamento de dados ausentes e incerteza;
- documentação metodológica original versionada;
- licença de reutilização e redistribuição;
- citação recomendada;
- checksum, tamanho e estrutura interna da planilha;
- módulo de estimativas municipais de GEE.

## 5. Decisão curatorial

Este adendo reduz a incerteza temporal e confirma que o IMVC possui edições separáveis, mas não autoriza promoção. A correção futura do registro legado deve deixar de afirmar apenas “índice desenvolvido em 2014–2015” e registrar que existe edição atualizada em junho de 2024, mantendo 2017 e 2015 como edições históricas anunciadas.

A linha canônica pública não foi alterada. A próxima etapa segura é inspecionar os metadados oficiais de 2024 e, separadamente, a planilha XLSX, antes de criar o produto/release normalizado.
