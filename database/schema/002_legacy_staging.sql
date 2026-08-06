-- Instance 1 migration staging for the public CSV model
-- Target: PostgreSQL 16+
-- All legacy values remain text until they are normalized and validated.

BEGIN;

CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE staging.legacy_resources (
    load_id bigserial PRIMARY KEY,
    resource_id text,
    resource_name text,
    acronym text,
    official_identity text,
    description text,
    homepage_url text,
    data_access_url text,
    research_areas text,
    keywords text,
    data_product_types text,
    data_formats text,
    visualization_types text,
    geographic_coverage text,
    covers_brazil text,
    spatial_resolution text,
    temporal_coverage text,
    temporal_resolution text,
    data_sources text,
    free_download text,
    access_conditions text,
    programmatic_access text,
    access_protocols text,
    authentication_required text,
    access_documentation_url text,
    license text,
    institutional_status text,
    owner_or_manager text,
    academic_uses text,
    limitations text,
    academic_evidence_type text,
    academic_evidence_url text,
    academic_evidence_note text,
    verification_url text,
    last_verified text,
    source_filename text NOT NULL DEFAULT 'data/data_resources.csv',
    source_file_hash text,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    migrated_at timestamptz,
    migration_status text NOT NULL DEFAULT 'pending' CHECK (migration_status IN (
        'pending','mapped','migrated','blocked','rejected'
    )),
    migration_notes text
);

CREATE UNIQUE INDEX legacy_resources_resource_id_idx
ON staging.legacy_resources(resource_id)
WHERE resource_id IS NOT NULL;

CREATE TABLE staging.legacy_products (
    load_id bigserial PRIMARY KEY,
    product_id text,
    resource_id text,
    product_name text,
    product_acronym text,
    product_family text,
    product_kind text,
    product_description text,
    research_areas text,
    keywords text,
    geographic_coverage text,
    covers_brazil text,
    spatial_support text,
    spatial_resolution text,
    temporal_coverage text,
    temporal_resolution text,
    update_frequency text,
    product_status text,
    version_or_collection text,
    enumeration_scope text,
    product_page_url text,
    methodology_url text,
    primary_or_derived text,
    limitations text,
    last_verified text,
    resolved_entity_type text CHECK (resolved_entity_type IN (
        'product','product_family','source','distribution','access_capability','unknown'
    )),
    resolution_rationale text,
    source_filename text NOT NULL DEFAULT 'data/data_products.csv',
    source_file_hash text,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    migrated_at timestamptz,
    migration_status text NOT NULL DEFAULT 'pending' CHECK (migration_status IN (
        'pending','mapped','migrated','blocked','rejected'
    )),
    migration_notes text
);

CREATE UNIQUE INDEX legacy_products_product_id_idx
ON staging.legacy_products(product_id)
WHERE product_id IS NOT NULL;

CREATE INDEX legacy_products_resource_id_idx
ON staging.legacy_products(resource_id);

CREATE TABLE staging.legacy_distributions (
    load_id bigserial PRIMARY KEY,
    distribution_id text,
    product_id text,
    distribution_name text,
    access_url text,
    format text,
    access_protocol text,
    access_tool text,
    free_download text,
    authentication_required text,
    access_conditions text,
    license text,
    provider_attribution_required text,
    subset_support text,
    notes text,
    last_verified text,
    source_filename text NOT NULL DEFAULT 'data/product_distributions.csv',
    source_file_hash text,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    migrated_at timestamptz,
    migration_status text NOT NULL DEFAULT 'pending' CHECK (migration_status IN (
        'pending','mapped','migrated','blocked','rejected'
    )),
    migration_notes text
);

CREATE UNIQUE INDEX legacy_distributions_distribution_id_idx
ON staging.legacy_distributions(distribution_id)
WHERE distribution_id IS NOT NULL;

CREATE INDEX legacy_distributions_product_id_idx
ON staging.legacy_distributions(product_id);

CREATE TABLE staging.migration_issues (
    issue_id bigserial PRIMARY KEY,
    entity_type text NOT NULL CHECK (entity_type IN ('resource','product','distribution')),
    legacy_id text NOT NULL,
    issue_code text NOT NULL,
    severity text NOT NULL CHECK (severity IN ('info','warning','error','blocking')),
    field_name text,
    current_value text,
    issue_description text NOT NULL,
    proposed_action text,
    resolution_status text NOT NULL DEFAULT 'open' CHECK (resolution_status IN (
        'open','resolved','accepted','not_applicable'
    )),
    resolved_by text,
    resolved_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX migration_issues_entity_idx
ON staging.migration_issues(entity_type, legacy_id, resolution_status);

CREATE VIEW staging.v_unresolved_products AS
SELECT *
FROM staging.legacy_products
WHERE migration_status IN ('pending','blocked')
   OR resolved_entity_type IS NULL
   OR resolved_entity_type = 'unknown';

CREATE VIEW staging.v_blocking_issues AS
SELECT *
FROM staging.migration_issues
WHERE severity = 'blocking'
  AND resolution_status = 'open';

COMMENT ON SCHEMA staging IS
'Lossless import area for the current CSVs. Values remain textual until entity resolution, evidence review and normalization are complete.';

COMMENT ON COLUMN staging.legacy_products.resolved_entity_type IS
'Curatorial decision separating scientific products from sources, families, distributions and generic access capabilities.';

COMMIT;
