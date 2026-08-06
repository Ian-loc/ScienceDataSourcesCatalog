# Auditoria — fronteira científica inicial do DETER Cerrado

**Data/hora:** 6 de agosto de 2026, 02h22–02h34, `America/Sao_Paulo`  
**Família:** `PF000003 — DETER Cerrado`  
**Produto científico candidato:** `PD-DETER-CER-ALERTS`  
**UUID de metadado:** `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830`

## Objetivo

Resolver a identidade inicial do DETER Cerrado e impedir que seus avisos operacionais sejam assimilados a uma taxa, inventário anual PRODES, distribuição amazônica ou perfil metodológico herdado de outra família.

## Evidências oficiais

1. A página atual do DETER/BiomasBR informa que o sistema produz alertas de supressão da vegetação nativa no Cerrado, que o DETER Cerrado foi criado em 2018 e que o contexto geral atual utiliza Amazônia-1, CBERS-4 e CBERS-4A/WFI com área mínima declarada de 3 ha.
2. A mesma página fornece citação recomendada para `Bioma Cerrado — Deter (Avisos): Avisos no Bioma Cerrado — Shapefile (desde 2018)` e identifica o metadado `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830`.
3. O catálogo TerraBrasilis lista separadamente a distribuição `Avisos de supressão da vegetação nativa — Shapefile (desde 2018)` e exibe, no snapshot observado, atualização em 28/07/2026.
4. O MMA descreve o DETER como levantamento rápido de alertas para fiscalização, sem finalidade de medir precisamente as áreas desmatadas, atribuição do PRODES anual.
5. O BiomasBR afirma que suas metodologias são adaptadas às características de cada bioma; por isso, o perfil amazônico não deve ser transferido automaticamente ao Cerrado.

## Decisões científicas

### Alertas não são inventário anual

```text
alerta DETER Cerrado
≠ taxa mensal
≠ taxa anual
≠ inventário anual completo
≠ release PRODES Cerrado
```

A unidade representa evidências espaciais de supressão para resposta operacional. O uso em análise de tendências exige cautela e não converte o conjunto em estimativa precisa ou inventário consolidado.

### O perfil geral atual é contexto, não herança integral

Foram registrados como contexto geral atual do programa:

- monitoramento diário;
- área mínima declarada de 3 ha;
- Amazônia-1, CBERS-4 e CBERS-4A;
- sensor WFI.

Permanecem não resolvidos especificamente para o produto Cerrado:

- versão metodológica adaptada ao bioma;
- resolução espacial específica;
- latência pública;
- domínio atual de classes;
- política de revisão e substituição;
- release vigente.

### Datas não identificam release

O ano de 2018 representa o início operacional documentado. A data de 28/07/2026 é apenas o valor exibido pela interface do catálogo no snapshot observado. Nenhuma delas foi promovida como identificador de release, período científico integral ou identidade dos bytes.

### Metadado, distribuição e ativo permanecem separados

O UUID identifica o registro de metadados. Ele não constitui:

- URL direta;
- resposta HTTP;
- ativo baixado;
- checksum;
- release;
- esquema integral.

## Estados não resolvidos

- release atual;
- método específico do Cerrado;
- classes e variáveis completas;
- URL direta e redirecionamentos;
- bytes, nome, tamanho e checksum;
- CRS, geometria e esquema integral;
- qualidade, validação, incerteza, nuvens, vieses e ausências;
- licença, atribuição e citação da release.

## Ocorrência

**ID:** `I1-20260806-045`  
**Categoria:** colapso entre alertas operacionais, inventário anual e herança interbiomas  
**Severidade:** `high` para promoção da unidade  
**Estado:** `corrected`  
**Evidência:** fontes oficiais distinguem a finalidade operacional do DETER, o inventário anual PRODES e a adaptação metodológica por bioma.  
**Correção:** contrato e validador preservam identidade, distribuição, UUID, fronteiras interpretativas e estados negativos de promoção.  
**Teste:** `scripts/validate_deter_cerrado_scientific_boundary_guard.py`, encadeado ao CI.  
**Risco residual:** método específico, release, endpoint, bytes, perfil científico completo, licença e citação continuam pendentes.

## Artefatos

- `database/mappings/deter_cerrado_scientific_boundary_guard_2026.json`;
- `scripts/validate_deter_cerrado_scientific_boundary_guard.py`;
- integração no workflow `Validar e publicar catálogo`;
- registro cumulativo da ocorrência `I1-20260806-045`.

## Resultado

A família legada `PF000003` avançou para um candidato de produto científico-operacional com distribuição e metadado individualizados, sem promoção ao núcleo relacional, sem herança automática de outra família e sem alteração da autoridade pública.
