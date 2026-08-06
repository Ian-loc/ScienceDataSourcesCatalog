# Auditoria — perfil específico de metadados do DETER Cerrado

**Data/hora:** 6 de agosto de 2026, 07h21–07h31, `America/Sao_Paulo`  
**Família:** `PF000003`  
**Produto candidato:** `PD-DETER-CER-ALERTS`  
**UUID de metadado:** `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830`

## Objetivo

Aprofundar a unidade DETER Cerrado com as afirmações específicas disponíveis no registro oficial, sem herdar automaticamente classes, sensores, limiares, latência ou esquema do DETER Amazônia e sem converter metadado, citação ou partições operacionais em release científica.

## Evidência oficial examinada

O registro GeoNetwork específico informa:

- título referente aos avisos no Cerrado desde 2018;
- objeto descrito como avisos de supressão da vegetação nativa com solo exposto;
- uso de imagens Landsat ou similares;
- classe documentada `DESMATAMENTO_CR`;
- significado da classe como supressão completa da vegetação nativa, independentemente de uso posterior;
- campos documentados `fid`, `classname` e `quadrant`;
- sufixos `_curr` e `_hist` para tabelas corrente e histórica;
- campo `quadrant` atualmente fora de uso para imagens CBERS.

A página programática do BiomasBR mantém a criação do DETER Cerrado em 2018 e fornece uma citação recomendada, publicada como exemplo em 2024, vinculada ao UUID do registro.

## Decisões curatoriais

### Classe específica

`DESMATAMENTO_CR` é a única classe comprovada pelo metadado específico recuperado. Isso não prova que o domínio integral da release atualmente distribuída contenha somente essa classe. Assim:

```text
classe documentada no metadado
≠ domínio completo da release vigente
```

Não foram herdadas classes de degradação, mineração ou exploração madeireira do DETER Amazônia.

### Perfil metodológico

A expressão “Landsat ou similares” foi preservada como declaração específica do registro. Ela não foi substituída pelo perfil geral contemporâneo do programa, que menciona Amazônia-1, CBERS-4, CBERS-4A e WFI.

O limiar geral atual de 3 ha também não foi promovido como fato específico deste registro. A metodologia versionada e o limiar individual do DETER Cerrado continuam não resolvidos.

### Identificadores e partições

Os sufixos `_curr` e `_hist` distinguem partições operacionais corrente e histórica. Eles não constituem releases científicas.

`fid` não foi promovido como chave persistente entre snapshots ou releases. O UUID GeoNetwork identifica o registro de metadados, não as feições do conjunto.

### Citação

O ano 2024 e a data de acesso de 2 de setembro de 2024 pertencem à citação recomendada exibida pelo produtor. Eles não identificam a release vigente nem substituem a data real de acesso futuro.

## Estados não resolvidos

- domínio integral de classes da release atual;
- método específico versionado;
- limiar mínimo específico;
- resolução espacial e suporte;
- release vigente;
- URL direta, HTTP e redirecionamentos;
- bytes, checksum, CRS, geometria e esquema integral;
- licença e citação da release efetivamente acessada.

## Ocorrência

**ID:** `I1-20260806-047`  
**Categoria:** herança interbiomas e promoção indevida de metadado/partição operacional como release  
**Severidade:** `high` para promoção da unidade  
**Estado:** `corrected`  
**Evidência:** metadado específico documenta somente `DESMATAMENTO_CR`, esquema parcial e partições `_curr/_hist`, enquanto o perfil geral do DETER contém atributos mais amplos.  
**Correção:** contrato e validador preservam o nível de evidência específico, bloqueiam heranças e mantêm release/ativo negativos.  
**Teste:** `scripts/validate_deter_cerrado_metadata_profile_guard.py`, encadeado ao gate científico DETER Cerrado.  
**Risco residual:** método, classes atuais completas, release, endpoint, bytes, qualidade, licença e citação continuam pendentes.

## Artefatos

- `database/mappings/deter_cerrado_metadata_profile_guard_2026.json`;
- `scripts/validate_deter_cerrado_metadata_profile_guard.py`;
- integração em `scripts/validate_deter_cerrado_scientific_boundary_guard.py`.

## Resultado

A unidade avançou de uma fronteira geral de produto/distribuição para um perfil específico de classe, esquema e identificadores. Nenhuma promoção foi autorizada e nenhuma propriedade do DETER Amazônia foi transferida automaticamente.
