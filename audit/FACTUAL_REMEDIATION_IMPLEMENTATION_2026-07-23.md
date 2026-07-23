# Factual remediation implementation — 2026-07-23

## Scope

This implementation corrects confirmed operational metadata for 11 canonical source records while preserving the catalogue at 51 sources × 34 fields and version 0.7.0.

Corrected dimensions include authentication, access conditions, API status, access documentation, licensing, limitations and official verification links. Each correction is recorded in `data/factual_corrections_2026-07-23.json`.

## Verification semantics

`last_verified` now represents the date on which the catalogue record was reviewed. It does not certify every dataset, product, version, endpoint or license maintained by an external source. The public interface uses the label “Registro revisado em” and provides a transparency notice.

## Interface scale

The root font size is 15.5 px on larger screens and 15 px on small screens. Main headings, card headings, lead text and hero spacing were reduced moderately without removing keyboard focus, semantic landmarks, responsive layouts or accessibility rules.

## Derived projections

`migration/data1bx_migration_matrix.csv` was regenerated from the corrected canonical CSV. Its confidence values remain `desconhecida`; regeneration synchronizes the projection but does not claim external validation.

## Release status

The DOI and version 1.0.0 remain blocked. Additional source-level and product-level factual review remains necessary before a stable scientific release.
