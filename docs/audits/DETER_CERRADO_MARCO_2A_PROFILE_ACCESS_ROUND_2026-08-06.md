# Marco 2A — DETER Cerrado — perfil específico, citação, licença e acesso

**Data:** 6 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Pacote:** `I1-M2A-DETER-CERRADO`  
**Estado:** parcial, auditável, sem promoção

## 1. Objetivo

Aprofundar o produto candidato `PD-DETER-CER-ALERTS` usando somente evidência oficial específica ou contexto geral explicitamente qualificado, sem transformar metadado, citação, licença do programa ou capacidade da fonte em release ou ativo.

## 2. Identidade preservada

- família: `PF000003 — DETER Cerrado`;
- produto candidato: `PD-DETER-CER-ALERTS`;
- registro específico: `a5220c18-f7fa-4e3e-b39b-feeb3ccc4830`;
- objeto: avisos de supressão da vegetação nativa com solo exposto no bioma Cerrado;
- início operacional documentado: 2018;
- finalidade: suporte à fiscalização e ao controle ambiental;
- não é taxa mensal ou anual;
- não é inventário anual completo;
- não é release PRODES Cerrado.

## 3. Classe e esquema do metadado

O registro específico documenta uma única classe:

- `DESMATAMENTO_CR` — supressão completa da vegetação nativa, independentemente de evidência de uso posterior.

O inventário documental contém quinze campos:

| Campo | Semântica operacional principal |
|---|---|
| `fid` | identificador com sufixos de partição corrente ou histórica |
| `classname` | classe do aviso, documentada como `DESMATAMENTO_CR` |
| `quadrant` | campo fora de uso para CBERS; referência histórica a AWFI |
| `path_row` | órbita/ponto da imagem |
| `view_date` | data da imagem usada na identificação |
| `sensor` | sensor da imagem |
| `satellite` | satélite da imagem |
| `areauckm` | área da porção em unidade de conservação |
| `uc` | unidade de conservação |
| `areamunkm` | área da porção municipal; campo indicado para soma |
| `municipality` | município |
| `geocodibge` | identificador municipal do IBGE |
| `uf` | unidade da federação |
| `areatotkm` | área anterior à fragmentação; não deve ser somada; canal cadastrado de Shapefile |
| `publish_month` | dimensão temporal do GeoServer; ausente do Shapefile de download |

### Fronteiras

- o inventário é completo no nível do registro de metadados;
- tipos físicos, nulabilidade, domínios observados, CRS, geometria e esquema real dos bytes não foram verificados;
- nomes de campos do Shapefile podem ser truncados para dez caracteres;
- `_curr` e `_hist` identificam partições operacionais, não releases;
- `fid` não foi comprovado como chave persistente entre releases;
- o UUID do GeoNetwork não é identificador de feição ou ativo.

## 4. Perfil espacial e temporal

Documentado:

- domínio geográfico: bioma Cerrado;
- representação: vetorial;
- frequência de manutenção declarada: diária;
- escala declarada no catálogo: 1:250.000;
- ajuste ao recorte de biomas publicado pelo IBGE em 2019;
- origem de imagem específica: Landsat ou similares;
- `publish_month` como mecanismo de dimensão temporal do GeoServer.

Não resolvido:

- CRS atual;
- geometria e tipos físicos verificados nos bytes;
- resolução espacial específica;
- área mínima específica;
- latência pública específica;
- história completa de sensores;
- release vigente.

A escala 1:250.000 não foi convertida em resolução ou unidade mínima mapeável. O contexto geral atual do DETER — WFI, Amazônia-1/CBERS-4/CBERS-4A e 3 ha — permanece contexto geral e não foi herdado como perfil específico do Cerrado.

## 5. Citação

A orientação oficial específica foi registrada:

> INSTITUTO NACIONAL DE PESQUISAS ESPACIAIS (INPE). Bioma Cerrado – Deter (Avisos): Avisos no Bioma Cerrado – Shapefile (desde 2018). 2024. Disponível no registro GeoNetwork específico.

A data de acesso apresentada pela fonte é exemplo histórico e deve ser substituída pela data real do novo acesso.

O ano 2024 da orientação bibliográfica não constitui release vigente.

## 6. Licença

Foi localizada licença no nível do **Programa de monitoramento dos biomas brasileiros**:

- Creative Commons Attribution-ShareAlike 4.0 International;
- identificador operacional: `CC-BY-SA-4.0`;
- atribuição requerida;
- compartilhamento pela mesma licença aplicável ao trabalho licenciado no nível do programa.

Não foram promovidos como resolvidos:

- licença específica da release;
- licença específica do pacote de bytes;
- termos específicos de redistribuição do pacote;
- termos específicos para produtos derivados do ativo.

## 7. Canais de acesso

Resolvidos como capacidades ou páginas:

- catálogo público de downloads;
- registro específico de metadados;
- URL genérica WFS `https://terrabrasilis.dpi.inpe.br/geoserver/ows`;
- canal cadastrado de Shapefile documentado pelo campo `areatotkm`;
- acesso antecipado mediante credenciais para instituições de fiscalização.

Não resolvidos:

- workspace WFS específico;
- nome da camada ou feature type;
- `DescribeFeatureType` atual;
- URL direta do pacote;
- status HTTP e redirecionamentos;
- nome, tamanho, media type e Content-Disposition;
- bytes e checksum.

O acesso antecipado restrito não foi interpretado como autenticação obrigatória de todo download público.

## 8. Evidências oficiais

- INPE / BiomasBR — definição, método-base e orientação de citação do DETER;
- INPE / TerraBrasilis GeoNetwork — perfil específico, classe, esquema, canais e ajuste territorial;
- INPE / TerraBrasilis — citação e licença de uso;
- INPE / TerraBrasilis FAQ — WFS e política de credenciais antecipadas;
- IBGE — publicação do recorte de biomas de 2019.

## 9. Artefatos e gates

Atualizados:

- `database/mappings/deter_cerrado_metadata_profile_guard_2026.json`;
- `scripts/validate_deter_cerrado_metadata_profile_guard.py`;
- `scripts/validate_deter_cerrado_scientific_boundary_guard.py`.

Criados:

- `database/mappings/deter_cerrado_access_license_citation_guard_2026.json`;
- `scripts/validate_deter_cerrado_access_license_citation_guard.py`.

Ocorrências:

- `I1-20260806-049` — completude documental versus inspeção de bytes;
- `I1-20260806-050` — nível de citação/licença e capacidade versus ativo.

## 10. Estado do critério de completude

| Componente | Estado |
|---|---|
| identidade e fronteira alerta/inventário | verificado |
| classe do registro específico | verificado |
| inventário do esquema no metadado | verificado |
| semântica dos canais | verificado |
| citação recomendada | verificada como orientação |
| licença do programa | verificada |
| release vigente | não resolvida |
| método específico versionado | não resolvido |
| limiar, resolução e latência específicos | não resolvidos |
| qualidade, validação e incerteza | não resolvidas |
| workspace/layer WFS | não resolvidos |
| URL direta e estado HTTP | não resolvidos |
| bytes, pacote, CRS, geometria e checksum | não verificados |
| licença/citação da release | não resolvidas |
| promoção | não autorizada |

## 11. Próxima fila

1. localizar workspace e camada específicos sem inferência por analogia com DETER Amazônia;
2. tentar `GetCapabilities` e `DescribeFeatureType` por canal oficial;
3. localizar URL direta oficial do Shapefile;
4. testar resposta HTTP, redirecionamento e cabeçalhos;
5. inspecionar pacote e calcular checksum quando os bytes forem acessíveis;
6. buscar documentação do método específico, limiar, resolução, latência e qualidade;
7. resolver identidade da release antes de promoção.
