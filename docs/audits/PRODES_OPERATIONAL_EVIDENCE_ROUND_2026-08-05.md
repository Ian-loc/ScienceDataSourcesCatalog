# Auditoria do round — evidência operacional PRODES

**Data e hora:** 05/08/2026, America/Sao_Paulo  
**Escopo:** Simbiotrama — Instância 1; PR #54; família `PF000001`  
**Autoridade publicada preservada:** `main`  
**Promoção normalizada:** não autorizada

## Unidade trabalhada

Aprofundamento operacional dos dois produtos-alvo já separados no contrato de pré-promoção:

- mapeamento anual PRODES Amazônia;
- taxa anual PRODES Amazônia.

## Evidência verificada

A página oficial de downloads do TerraBrasilis foi inspecionada como catálogo operacional. Ela distingue metadado e download e expõe famílias de ativos diferentes, incluindo incremento anual em Shapefile, incremento de polígonos entre 1 e 6,25 ha em distribuição separada, produto completo em GeoTIFF e produto completo em GeoPackage.

O portal científico oficial do INPE registra que as taxas anuais são estimadas a partir dos incrementos identificados nas imagens da Amazônia Legal, que a primeira apresentação anual ocorre como estimativa e que os dados consolidados são apresentados posteriormente. Também registra o uso combinado de imagens da classe Landsat para minimizar cobertura de nuvens.

## Decisões de modelagem

1. **Distribuições não são produtos:** Shapefile, GeoTIFF e GeoPackage foram registrados como famílias operacionais de distribuição, não como novos produtos científicos.
2. **Pequenos polígonos são uma distribuição distinta:** a publicação de polígonos entre 1 e 6,25 ha não foi usada como prova da unidade mínima vigente do produto principal.
3. **Estimativa e consolidação são estados ordenados:** `preliminary_estimate` antecede `consolidated_rate`; não foram modeladas como séries científicas independentes.
4. **Nuvens:** foi registrado apenas que a combinação de imagens busca minimizar cobertura de nuvens. O ajuste quantitativo vigente para áreas não observadas permanece desconhecido.
5. **Sem promoção:** nenhuma URL agregadora foi promovida como distribuição específica; nenhum release, CRS, esquema de atributos, licença ou citação foi inventado.

## Ocorrência

**I1-20260805-015**

- **categoria:** precisão operacional e controle de inferência;
- **severidade:** `high`;
- **estado:** `corrected`;
- **descrição:** havia risco de transformar o catálogo agregado de downloads em distribuições normalizadas específicas e de interpretar a distribuição de polígonos entre 1 e 6,25 ha como confirmação da unidade mínima vigente. Também havia risco de preencher o ajuste para áreas não observadas a partir de uma descrição geral sobre mitigação de nuvens;
- **correção:** criado contrato operacional complementar com papéis de distribuição, ciclo de vida da taxa, limitações por evidência, inferências proibidas e lista explícita de campos ainda não resolvidos;
- **verificação:** `scripts/validate_prodes_operational_evidence.py`, invocado pelo validador PRODES já integrado ao CI;
- **risco residual:** ainda faltam metodologia algorítmica vigente, regra quantitativa para áreas não observadas, endpoints diretos, metadados de ativos, licença, citação e identificadores formais de release.

## Arquivos

- `database/mappings/prodes_operational_evidence_2026.json`;
- `scripts/validate_prodes_operational_evidence.py`;
- `scripts/validate_prodes_product_targets.py`;
- `docs/audits/PRODES_OPERATIONAL_EVIDENCE_ROUND_2026-08-05.md`.

## Portão resultante

O contrato continua em `pre_promotion_evidence`, com `promotion_authorized=false`. O banco efêmero de CI continua sendo ambiente de teste, não autoridade canônica.
