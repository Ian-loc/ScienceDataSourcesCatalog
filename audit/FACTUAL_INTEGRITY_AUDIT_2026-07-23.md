# Factual integrity audit — 2026-07-23

## Scope

This audit scrutinizes the factual accuracy, precision, current validity and evidentiary support of:

- all 51 source records and their 34 canonical fields in `data/data_resources.csv`;
- the 10 product records in `data/data_products.csv`;
- the 15 access distributions in `data/product_distributions.csv`;
- the meaning of verification dates, evidence labels and public quality indicators;
- the consistency between the public catalogue and project governance documents.

The audit uses current official documentation as the primary authority. A structurally valid row is not treated as factually valid merely because it passes CI.

The row-level findings are recorded in [`factual_audit_findings_2026-07-23.csv`](factual_audit_findings_2026-07-23.csv).

## Executive conclusion

The catalogue is a valuable and technically organized discovery interface, but its current public data cannot be described as externally verified or factually complete.

| Verdict | Sources | Meaning |
|---|---:|---|
| `C1_material_error` | 11 | At least one current catalogue value is contradicted by official evidence or is demonstrably obsolete. |
| `C2_partial_or_overgeneralized` | 26 | The source identity is generally real, but operational facts are incomplete, overgeneralized or belong at product/distribution level. |
| `C3_broadly_supported` | 12 | No material contradiction was found in the official checks performed, but the full 34-field row is not certified. |
| `C4_not_certifiable` | 2 | Current official evidence was inaccessible or insufficient for operational certification. |

**No source record is presently certifiable as correct across all 34 fields.** This is primarily a provenance and granularity failure, not evidence that every statement is false.

## Governance contradiction

`CODEBOOK.md` defines `last_verified` as the effective date of review. Every canonical row currently carries `2026-07-18`, but `WORKFLOW_STATUS.md` states that factual external review is still active and that zero external factual evidence records have been registered. The evidence CSV contains only its header.

Consequently, the public date currently communicates a stronger claim than the evidence system supports. It is best interpreted as an internal record-review date, not a completed external factual verification date.

Required correction:

1. rename or reinterpret the current field as `record_reviewed_at`;
2. introduce `factual_verification_status`;
3. record `access_checked_at`, `evidence_checked_at` and reviewer;
4. identify which fields each official source supports;
5. prevent the interface from presenting a single date as certification of the entire row.

## Confirmed material errors requiring immediate correction

### DR0006 — PANORAMA / CENSIPAM

The catalogue treats authentication and licensing as unknown. Official PANORAMA documentation shows that the meteorology API requires requested credentials/token, while the portal publishes a site-content license. Dataset licensing still requires product-level treatment.

### DR0013 — speciesLink

The official API is open for use but requires an API key. `authentication_required=desconhecido` is therefore materially wrong. Network textual data use CC BY 4.0, while individual collections can impose additional or conflicting conditions; a single source-level license is insufficient.

### DR0017 — HidroWeb

The ANA API requires credentials obtained through a request process. The catalogue says authentication is not required and access is simply open. The current download interface also showed an availability error during the audit.

### DR0018 — BDMEP

The current portal requires account/email confirmation. `authentication_required=não se aplica` is false and also inconsistent with the catalogue's own `access_conditions=cadastro`.

### DR0025 — IUCN Red List

The catalogue links API v3. Official IUCN documentation states that v3 is end-of-life and no longer receives current Red List updates. API v4 is current, token-based and limited to non-commercial use. Spatial downloads have separate terms and must not be conflated with the assessment API.

### DR0029 — NEON

This is the most serious freshness failure. From 30 June 2026, NEON downloads require sign-in/API token and the data license changed from CC0 to CC BY 4.0. The catalogue was dated 18 July 2026 but still described registration as optional and CC0 as applicable.

### DR0033 — Dryad

Current Dryad research data are published under CC0 and are publicly released without repository embargo/access restrictions. The catalogue's generic temporary-embargo statement and “CC0 unless indicated” formulation are not current for Dryad research data. Software or supplemental files routed elsewhere must be treated separately.

### DR0036 — FRED

FRED 3.0 access requires a form and an emailed token. `authentication_required=não se aplica` is false.

### DR0037 — SoilGrids

The 250 m maps, WMS, WCS and WebDAV remain available under CC BY 4.0, but the official documentation states that the beta REST API is temporarily paused. The catalogue presents the REST API as currently available without a service-status warning.

### DR0038 — WoSIS

Current official access documentation emphasizes WFS and GraphQL. The catalogue lists REST API and WCS. It also reduces a complex license structure—CC BY, CC BY-NC and restricted source datasets—to an overly simple CC BY formulation.

### DR0050 — ORNL DAAC

NASA Earthdata Login is generally required for actual data downloads/orders. The catalogue's `authentication_required=parcial` understates this. Discovery can be public, but discovery and data acquisition must be separate distributions. NASA-led data are generally CC0 unless specifically marked otherwise.

## Major partial or overgeneralized records

The following are not necessarily false in their core identity, but they should not remain as currently written without product- or service-level refinement:

- **MapBiomas:** Collection 10.1, 1985–2024 and 30 m are valid for a specific Landsat land-cover product, not the whole platform. The platform also has a 10 m beta collection. Direct downloads do not universally require authentication, while Earth Engine does. Current terms state CC BY.
- **TerraBrasilis:** official downloads, metadata and web services are real, but generic links and source-level format/protocol claims are too broad. PRODES, DETER and TerraClass require separate evidence and versioning.
- **CEMADEN:** institutional products are real, but open-data availability and service claims need enumeration by product.
- **Portal Brasileiro de Dados Abertos:** public catalogue queries and authenticated operations should not be compressed into one authentication value.
- **GBIF:** current bulk formats include tab-separated simple downloads, Darwin Core Archive and Parquet; authentication and licenses vary by operation/dataset.
- **WorldClim and CHELSA:** version, time period, resolution, format and license are product properties, not stable source properties.
- **Protected Planet:** release month/year and non-commercial/redistribution conditions are scientifically and legally essential.
- **eBird:** raw EBD observations, APIs and modeled Status & Trends products have distinct access procedures and terms.
- **DataONE:** it is a federation, not one repository; member dataset terms remain authoritative.
- **PANGAEA:** authentication is not universally absent because restricted datasets can require token access.
- **iNaturalist:** geoprivacy caveats are sound, but the catalogue links an older API version and must separate observation, image and sound licenses.
- **BIEN:** database release date must not be confused with the date or freshness of contributed occurrence records.
- **FLUXNET:** current Shuttle access and legacy FLUXNET2015 should be distinct products.
- **Global Carbon Atlas:** free availability does not create blanket publication permission; each module inherits original sources and citation rules.
- **EDGAR:** the 2025 GHG edition and 1970–2024 coverage are current, but the exact official formats and CC BY 4.0 license should replace generic wording.
- **ESGF:** MetaGrid is transitional/beta and access control remains project- and node-specific.

## Records broadly supported, but not fully certified

The audit found no material current contradiction in the core descriptions of CNUC, AppEEARS, Copernicus Climate Data Store, OBIS, KNB, Climate Data Guide, GBIF IPT, TRY, AmeriFlux, Copernicus Data Space Ecosystem, ILTER/DEIMS and Project COSMOS.

This verdict does **not** mean that every one of their 34 fields is independently verified. It means that the current official checks support the main identity, access model and central caveats without revealing a material contradiction.

## Product layer audit

### TerraBrasilis products DP000001–DP000007

The separation of PRODES, DETER, TerraClass, secondary vegetation and interoperable services is scientifically sound. The warnings against equating DETER alerts with annual PRODES results are correct.

Remaining weaknesses:

- most `product_page_url` values point to the generic download page rather than a stable product landing page;
- most methodology links point to a broad BiomasBR page rather than product/version documentation;
- product-specific spatial resolution, minimum mapping unit, temporal start and citation are still absent;
- `last_verified=2026-07-22` is not tied to field-level evidence;
- the WMS/WFS/WCS/CSW distributions use one generic documentation URL instead of exact service endpoints;
- the statement `portal CC BY-SA 4.0` in DD000001 requires direct evidence and must not be treated as the license of PRODES files.

The official TerraBrasilis statement that BiomasBR files were updated on 3 March 2026 supports DP000001's update claim and the experimental status of DETER Pantanal.

### Earth Engine products DP000008–DP000010

The distinction among public catalogue, publisher catalogues, and processing/export service is correct. Provider, version, resolution and license correctly remain dataset-level.

Remaining weaknesses:

- DD000012 and DD000013 mark authentication as required for the public web catalogues. Browsing/discovery is public; authentication is required for Earth Engine use, processing and export. Discovery and use should be separate distributions.
- access conditions should encode the current 2026 tier/quota model, including the possibility of billing for higher non-commercial tiers and commercial use;
- `free_download=parcial` combines data-provider license, Earth Engine eligibility and export quota in one field and should be decomposed.

## Structural causes of factual error

### 1. Source-level fields are overloaded

Fields such as resolution, temporal coverage, formats, authentication and license often vary by product or access route. A single value at source level inevitably becomes either false or vague.

### 2. Boolean-like access fields are too coarse

A platform may allow public browsing, require login for bulk downloads, require an API key for automated access and impose a separate approval workflow for restricted datasets. `sim/parcial/não` cannot preserve this logic without distributions.

### 3. Evidence does not support every claim

An article demonstrating scientific use of a platform does not validate its current API, license, formats, ownership or authentication requirements. Evidence must be linked to the exact claim and field it supports.

### 4. Verification date lacks scope

A single date does not reveal whether the reviewer checked the homepage, data download, API, license, version, citation guidance or every field.

### 5. Current and legacy products are conflated

Examples include IUCN API v3/v4, FLUXNET2015/current Shuttle, WorldClim versions, MapBiomas collections and changing NEON policies.

## Required remediation sequence

### P0 — public factual safety

Correct the 11 confirmed material-error records immediately and display a temporary catalogue notice that source-level operational metadata remains under factual re-verification.

### P1 — verification semantics

Implement at minimum:

- `factual_verification_status`;
- `record_reviewed_at`;
- `access_checked_at`;
- `license_checked_at`;
- `verification_scope` or per-field evidence links;
- `reviewer`;
- `evidence_source_type`;
- `supports_current_value`.

Do not use `last_verified` as a whole-row certification date.

### P2 — source/product/distribution migration

Move resolution, period, version, format, protocol, authentication and license to the most specific level supported by evidence. Retain source-level values only as explicitly labelled summaries derived from verified child records.

### P3 — external evidence completion

Populate `migration/external_review_evidence.csv` with one row per claim and dimension. A correction should not enter the canonical CSV until its official evidence, access date, reviewer and proposed value are recorded.

### P4 — release and DOI gates

Do not release v1.0.0 or create a DOI while material factual errors remain or while public verification dates overstate the evidence status.

## Decision

The catalogue should remain online as a **discovery catalogue under active factual review**, not as a fully verified scientific reference database. Its architecture and interpretive warnings are promising, but its factual authority currently varies substantially by record and field.

This audit branch intentionally does not modify `data/data_resources.csv`, product CSVs or the published interface. Canonical corrections should be implemented in a separate reviewed remediation pull request derived from this evidence matrix.
