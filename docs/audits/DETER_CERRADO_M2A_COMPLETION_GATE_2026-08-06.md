# Gate de completude — I1-M2A DETER Cerrado

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Branch:** `agent/marco-2a-deter-cerrado`  
**PR:** #57

## Decisão

O pacote de auditoria científica e operacional do DETER Cerrado é considerado **completo com incompletude externa delimitada e fail-closed**.

Essa decisão significa que todas as dimensões previstas foram examinadas, sustentadas por evidência, testadas e classificadas como resolvidas ou explicitamente não resolvidas. Ela não significa que um produto, release, distribuição ou ativo esteja autorizado para promoção.

## Dimensões concluídas

### Identidade e fronteiras

- família e produto candidato delimitados;
- DETER Cerrado separado de DETER Amazônia, DETER Pantanal e PRODES;
- alerta operacional separado de taxa e inventário anual;
- início operacional desde 2018 preservado sem conversão em release.

### Metadado e esquema conceitual

- registro GeoNetwork corrente reconciliado como `e6e15388-4ca9-49b9-aec9-03891339a35e`;
- referência publicada antiga preservada como deriva documental;
- quinze campos do metadado documentados;
- classe `DESMATAMENTO_CR` resolvida no nível do registro específico;
- diferenças entre campos do Shapefile e do GeoServer preservadas.

### Método, espaço e tempo

- edição metodológica INPE de 28/03/2024 individualizada;
- sensores, satélites, resolução nominal, escala de interpretação e limiar documentados;
- latência típica, ciclo de observação e máscara operacional documentados;
- data da imagem separada da data real do evento;
- contexto geral atual separado do perfil específico da edição metodológica.

### Classes e validação

- classes operacionais por sensor e classe final `Aviso` resolvidas;
- cinco classes de validação resolvidas para a edição metodológica;
- `Resíduo` de validação separado do produto anual de resíduo PRODES;
- crosswalk para `DESMATAMENTO_CR` e esquema da release mantido negativo.

### Qualidade e incerteza

- controles operacionais e limitações documentados;
- resultado de 80% em raio de 10 km registrado como proximidade e utilidade operacional;
- precisão, revocação, omissão, comissão, matriz de confusão e incerteza da release mantidas não resolvidas;
- métricas do DETER Amazônia ou PRODES não foram herdadas.

### Acesso, licença e citação

- catálogo, registro de metadado, capacidade WFS genérica e acesso antecipado delimitados;
- licença CC-BY-SA-4.0 resolvida no nível do programa, não do pacote;
- orientação de citação documentada e corrigida quanto ao registro corrente;
- registro WMS oficial do plugin QGIS inspecionado sem inferência de inexistência do serviço;
- tentativas HTTP diretas foram bloqueadas por falha DNS instrumental, sem interpretação como indisponibilidade permanente.

## Incompletude externa preservada

Permanecem não resolvidos e bloqueados:

- identidade da release vigente;
- vínculo release–método;
- crosswalk das classes no esquema físico atual;
- métricas de acurácia e incerteza da edição distribuída;
- workspace e feature type WFS específicos;
- `DescribeFeatureType` e `GetFeature` contemporâneos;
- URL direta e resposta HTTP;
- nome, tamanho, `Content-Type` e `Content-Disposition`;
- bytes, inventário do pacote, CRS, geometria e esquema físico;
- checksum;
- licença e citação da release e do ativo;
- autorização de promoção.

## Regra de completude

Uma incompletude externa pode encerrar o pacote de auditoria quando:

1. a busca foi documentada nas superfícies autoritativas disponíveis;
2. nenhuma inferência foi usada para preencher a lacuna;
3. o estado negativo está estruturado e validado;
4. os riscos dependentes permanecem bloqueados;
5. a lacuna e o caminho de resolução futura estão explícitos.

Essas condições foram atendidas.

## Estado de promoção

```text
scientific_audit_package_complete = true
product_profile_complete_for_promotion = false
release_profile_complete_for_promotion = false
asset_profile_complete_for_promotion = false
promotion_authorized = false
```

## Estado de merge

O pacote pode ser apresentado para revisão humana após:

- CI verde no SHA exato;
- PR mesclável;
- ausência de revisão contrária ou thread aberta;
- congelamento do head;
- autorização humana explícita para o SHA final.

O merge do PR não promoverá PostgreSQL a produção, não alterará a autoridade dos CSVs públicos, não publicará Pages e não promoverá produto, release ou ativo DETER Cerrado.

## Trabalho futuro

A resolução futura de release ou ativo deve ocorrer em pacote próprio ou continuação explicitamente autorizada, preservando os estados negativos até que respostas e bytes oficiais sejam verificáveis.
