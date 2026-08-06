-- Symbiotrama / Science Data Sources Catalog
-- Instance 1: relational scientific and operational catalog
-- Target: PostgreSQL 16+ with PostGIS 3+
-- Scope: metadata, scientific meaning, access and curation. External datasets are not ingested here.

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SCHEMA IF NOT EXISTS catalog;

CREATE TABLE IF NOT EXISTS catalog.schema_migrations (
    version text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT now(),
    description text NOT NULL
);

INSERT INTO catalog.schema_migrations (version, description)
VALUES ('001', 'Instance 1 relational scientific and operational catalog')
ON CONFLICT (version) DO NOTHING;

CREATE TABLE catalog.organizations (
    organization_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    official_name text NOT NULL,
    acronym text,
    organization_type text,
    country_code char(2),
    homepage_url text,
    description text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.sources (
    source_id bigserial PRIMARY KEY,
    stable_id text NOT NULL UNIQUE CHECK (stable_id ~ '^DR[0-9]{4,}$'),
    organization_id bigint REFERENCES catalog.organizations(organization_id),
    source_name text NOT NULL,
    acronym text,
    source_type text NOT NULL CHECK (source_type IN (
        'portal','repository','catalog','platform','network','infrastructure',
        'data_service','program','observatory','other'
    )),
    official_identity text,
    description text NOT NULL,
    homepage_url text,
    primary_data_access_url text,
    access_documentation_url text,
    institutional_status text,
    owner_or_manager text,
    geographic_scope text,
    covers_brazil boolean,
    active_status text NOT NULL DEFAULT 'active' CHECK (active_status IN (
        'active','inactive','deprecated','unknown'
    )),
    enumeration_strategy text NOT NULL DEFAULT 'selective' CHECK (enumeration_strategy IN (
        'complete','family_level','external_index','representative_sample','selective'
    )),
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.product_families (
    product_family_id bigserial PRIMARY KEY,
    source_id bigint NOT NULL REFERENCES catalog.sources(source_id) ON DELETE CASCADE,
    stable_id text UNIQUE,
    family_name text NOT NULL,
    acronym text,
    description text,
    scientific_scope text,
    enumeration_scope text CHECK (enumeration_scope IN (
        'complete','family_level','external_index','representative_sample','selective'
    )),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, family_name)
);

CREATE TABLE catalog.products (
    product_id bigserial PRIMARY KEY,
    stable_id text NOT NULL UNIQUE CHECK (stable_id ~ '^DP[0-9]{6,}$'),
    source_id bigint NOT NULL REFERENCES catalog.sources(source_id),
    product_family_id bigint REFERENCES catalog.product_families(product_family_id),
    product_name text NOT NULL,
    acronym text,
    product_kind text NOT NULL CHECK (product_kind IN (
        'dataset','dataset_series','indicator_series','map_series','observation_collection',
        'model_output','administrative_statistics','survey_product','reference_geometry',
        'classification_product','derived_product','other'
    )),
    product_description text NOT NULL,
    scientific_object text NOT NULL,
    information_message text NOT NULL,
    intended_uses text,
    non_representations text,
    primary_or_derived text NOT NULL CHECK (primary_or_derived IN (
        'primary_observation','administrative_record','survey_estimate','classified',
        'modeled','interpolated','derived','mixed','unknown'
    )),
    geographic_coverage_text text,
    covers_brazil boolean NOT NULL DEFAULT false,
    product_status text NOT NULL DEFAULT 'active' CHECK (product_status IN (
        'active','experimental','legacy','deprecated','discontinued','unknown'
    )),
    official_product_page_url text,
    methodology_url text,
    citation_guidance_url text,
    limitations_summary text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.product_releases (
    release_id bigserial PRIMARY KEY,
    product_id bigint NOT NULL REFERENCES catalog.products(product_id) ON DELETE CASCADE,
    stable_id text UNIQUE,
    version_label text NOT NULL,
    release_date date,
    valid_from date,
    valid_to date,
    temporal_coverage_text text,
    release_status text NOT NULL DEFAULT 'current' CHECK (release_status IN (
        'current','superseded','experimental','withdrawn','unknown'
    )),
    change_summary text,
    release_notes_url text,
    checksum_or_identifier text,
    is_current boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (product_id, version_label)
);

CREATE UNIQUE INDEX product_one_current_release_idx
ON catalog.product_releases(product_id)
WHERE is_current;

CREATE TABLE catalog.spatial_profiles (
    spatial_profile_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    support_type text NOT NULL CHECK (support_type IN (
        'point','footprint','pixel','grid_cell','line','polygon','administrative_unit',
        'watershed','biome','protected_area','facility','farm','plot','trajectory',
        'network','mixed','unknown'
    )),
    support_description text NOT NULL,
    geometry_type text,
    nominal_resolution_value numeric,
    nominal_resolution_unit text,
    scale_denominator numeric,
    minimum_mapping_unit_value numeric,
    minimum_mapping_unit_unit text,
    crs text,
    grid_definition text,
    spatial_aggregation text,
    geographic_unit_type text,
    geographic_coverage_text text,
    coverage_geometry geometry(MultiPolygon, 4326),
    spatial_biases text,
    spatial_limitations text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX spatial_profiles_coverage_gix
ON catalog.spatial_profiles USING gist (coverage_geometry);

CREATE TABLE catalog.temporal_profiles (
    temporal_profile_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    representation_type text NOT NULL CHECK (representation_type IN (
        'instant','interval','event','daily','monthly','annual','cumulative',
        'moving_average','multi_year_average','static','irregular','unknown'
    )),
    support_description text NOT NULL,
    coverage_start date,
    coverage_end date,
    temporal_resolution text,
    observation_window text,
    update_frequency text,
    latency text,
    calendar_definition text,
    temporal_aggregation text,
    temporal_biases text,
    temporal_limitations text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.methods (
    method_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    method_name text NOT NULL,
    method_type text NOT NULL CHECK (method_type IN (
        'measurement','remote_sensing_classification','remote_sensing_retrieval',
        'administrative_record','survey','census','model','interpolation',
        'aggregation','composite_index','expert_mapping','mixed','other','unknown'
    )),
    description text NOT NULL,
    input_data text,
    processing_summary text,
    validation_summary text,
    method_version text,
    methodology_url text,
    limitations text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.quality_profiles (
    quality_profile_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    quality_status text NOT NULL DEFAULT 'partially_documented' CHECK (quality_status IN (
        'documented','partially_documented','not_documented','unknown'
    )),
    validation_design text,
    accuracy_metrics text,
    uncertainty_available boolean,
    uncertainty_type text,
    uncertainty_description text,
    quality_flags text,
    missing_data_definition text,
    collection_bias text,
    known_artifacts text,
    representativeness_limits text,
    quality_documentation_url text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.variables (
    variable_id bigserial PRIMARY KEY,
    stable_id text NOT NULL UNIQUE CHECK (stable_id ~ '^VR[0-9]{6,}$'),
    canonical_name text NOT NULL,
    display_name_pt text NOT NULL,
    display_name_en text,
    definition text NOT NULL,
    phenomenon text NOT NULL,
    object_observed text NOT NULL,
    population_or_universe text,
    default_data_type text CHECK (default_data_type IN (
        'continuous','integer','count','rate','proportion','percentage','index',
        'ordinal','nominal','binary','geometry','text','array','unknown'
    )),
    canonical_unit text,
    vocabulary_reference_url text,
    sensitivity_class text NOT NULL DEFAULT 'public' CHECK (sensitivity_class IN (
        'public','restricted','sensitive','highly_sensitive','unknown'
    )),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.product_variables (
    product_variable_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    release_id bigint NOT NULL REFERENCES catalog.product_releases(release_id) ON DELETE CASCADE,
    variable_id bigint NOT NULL REFERENCES catalog.variables(variable_id),
    source_variable_name text NOT NULL,
    variable_role text NOT NULL CHECK (variable_role IN (
        'primary_observation','primary_estimate','derived_variable','class_label',
        'probability','quality_flag','uncertainty','coordinate','dimension',
        'identifier','mask','auxiliary','other'
    )),
    source_definition text,
    unit text,
    data_type text,
    method_id bigint REFERENCES catalog.methods(method_id),
    spatial_profile_id bigint REFERENCES catalog.spatial_profiles(spatial_profile_id),
    temporal_profile_id bigint REFERENCES catalog.temporal_profiles(temporal_profile_id),
    quality_profile_id bigint REFERENCES catalog.quality_profiles(quality_profile_id),
    interpretation text NOT NULL,
    scientific_potential text,
    non_interpretations text,
    aggregation_semantics text,
    class_legend_url text,
    is_searchable boolean NOT NULL DEFAULT true,
    review_status text NOT NULL DEFAULT 'draft' CHECK (review_status IN (
        'draft','reviewed','approved','deprecated'
    )),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (release_id, source_variable_name)
);

CREATE TABLE catalog.distributions (
    distribution_id bigserial PRIMARY KEY,
    stable_id text NOT NULL UNIQUE CHECK (stable_id ~ '^DD[0-9]{6,}$'),
    release_id bigint NOT NULL REFERENCES catalog.product_releases(release_id) ON DELETE CASCADE,
    distribution_name text NOT NULL,
    distribution_role text NOT NULL CHECK (distribution_role IN (
        'direct_download','api','web_service','catalog_record','visualizer',
        'code_repository','documentation','request_form','other'
    )),
    access_url text NOT NULL,
    format text,
    media_type text,
    access_protocol text,
    access_tool text,
    free_access text CHECK (free_access IN ('yes','partial','no','unknown','not_applicable')),
    authentication_required text CHECK (authentication_required IN (
        'yes','partial','no','unknown','not_applicable'
    )),
    access_conditions text,
    license text,
    attribution_required boolean,
    subset_support text,
    service_level_notes text,
    access_status text NOT NULL DEFAULT 'unknown' CHECK (access_status IN (
        'working','degraded','unavailable','retired','unknown'
    )),
    last_access_tested_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.data_assets (
    asset_id bigserial PRIMARY KEY,
    stable_id text UNIQUE,
    distribution_id bigint NOT NULL REFERENCES catalog.distributions(distribution_id) ON DELETE CASCADE,
    asset_name text NOT NULL,
    asset_role text NOT NULL CHECK (asset_role IN (
        'data','metadata','legend','quality','uncertainty','documentation',
        'schema','thumbnail','tile_layer','feature_layer','coverage_layer','other'
    )),
    asset_url text,
    asset_identifier text,
    format text,
    media_type text,
    byte_size bigint,
    checksum text,
    machine_readable boolean,
    supports_range_requests boolean,
    supports_spatial_subset boolean,
    supports_temporal_subset boolean,
    crs text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.access_capabilities (
    capability_id bigserial PRIMARY KEY,
    distribution_id bigint NOT NULL REFERENCES catalog.distributions(distribution_id) ON DELETE CASCADE,
    capability_type text NOT NULL CHECK (capability_type IN (
        'discover','preview','visualize','query_attributes','spatial_subset',
        'temporal_subset','download','stream','process','export','open_in_qgis',
        'open_in_r','open_in_python','open_in_earth_engine','other'
    )),
    capability_status text NOT NULL CHECK (capability_status IN (
        'available','conditional','not_available','unknown'
    )),
    requirements text,
    documentation_url text,
    UNIQUE (distribution_id, capability_type)
);

CREATE TABLE catalog.taxonomy_terms (
    term_id bigserial PRIMARY KEY,
    scheme text NOT NULL,
    term_code text NOT NULL,
    preferred_label_pt text NOT NULL,
    preferred_label_en text,
    definition text,
    broader_term_id bigint REFERENCES catalog.taxonomy_terms(term_id),
    vocabulary_url text,
    UNIQUE (scheme, term_code)
);

CREATE TABLE catalog.product_terms (
    product_id bigint NOT NULL REFERENCES catalog.products(product_id) ON DELETE CASCADE,
    term_id bigint NOT NULL REFERENCES catalog.taxonomy_terms(term_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, term_id)
);

CREATE TABLE catalog.variable_terms (
    variable_id bigint NOT NULL REFERENCES catalog.variables(variable_id) ON DELETE CASCADE,
    term_id bigint NOT NULL REFERENCES catalog.taxonomy_terms(term_id) ON DELETE CASCADE,
    PRIMARY KEY (variable_id, term_id)
);

CREATE TABLE catalog.citations (
    citation_id bigserial PRIMARY KEY,
    citation_type text NOT NULL CHECK (citation_type IN (
        'dataset_citation','methodology','validation','data_descriptor','technical_document',
        'license','user_guide','related_science','other'
    )),
    title text NOT NULL,
    authors text,
    publication_year integer,
    publisher_or_journal text,
    doi text,
    url text,
    citation_text text,
    peer_reviewed boolean,
    notes text
);

CREATE TABLE catalog.product_citations (
    product_id bigint NOT NULL REFERENCES catalog.products(product_id) ON DELETE CASCADE,
    citation_id bigint NOT NULL REFERENCES catalog.citations(citation_id) ON DELETE CASCADE,
    relationship_type text NOT NULL,
    is_primary boolean NOT NULL DEFAULT false,
    PRIMARY KEY (product_id, citation_id, relationship_type)
);

CREATE TABLE catalog.release_citations (
    release_id bigint NOT NULL REFERENCES catalog.product_releases(release_id) ON DELETE CASCADE,
    citation_id bigint NOT NULL REFERENCES catalog.citations(citation_id) ON DELETE CASCADE,
    relationship_type text NOT NULL,
    is_primary boolean NOT NULL DEFAULT false,
    PRIMARY KEY (release_id, citation_id, relationship_type)
);

CREATE TABLE catalog.metadata_assertions (
    assertion_id bigserial PRIMARY KEY,
    entity_type text NOT NULL CHECK (entity_type IN (
        'source','product_family','product','release','distribution','asset',
        'variable','product_variable','method','quality_profile','spatial_profile','temporal_profile'
    )),
    entity_stable_id text NOT NULL,
    field_name text NOT NULL,
    asserted_value text,
    evidence_url text NOT NULL,
    evidence_type text NOT NULL CHECK (evidence_type IN (
        'official_page','official_documentation','technical_report','peer_reviewed_article',
        'metadata_record','license','api_response','curatorial_inference','other'
    )),
    support_note text NOT NULL,
    confidence text NOT NULL DEFAULT 'medium' CHECK (confidence IN ('high','medium','low')),
    retrieved_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE catalog.curation_reviews (
    review_id bigserial PRIMARY KEY,
    entity_type text NOT NULL,
    entity_stable_id text NOT NULL,
    review_status text NOT NULL CHECK (review_status IN (
        'not_started','in_progress','needs_evidence','reviewed','approved','deprecated'
    )),
    completeness_score numeric CHECK (completeness_score BETWEEN 0 AND 1),
    scientific_precision_score numeric CHECK (scientific_precision_score BETWEEN 0 AND 1),
    operational_precision_score numeric CHECK (operational_precision_score BETWEEN 0 AND 1),
    reviewer text,
    reviewed_at timestamptz,
    next_review_due date,
    findings text,
    corrections_required text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX sources_name_trgm_idx ON catalog.sources USING gin (source_name gin_trgm_ops);
CREATE INDEX products_name_trgm_idx ON catalog.products USING gin (product_name gin_trgm_ops);
CREATE INDEX products_description_trgm_idx ON catalog.products USING gin (product_description gin_trgm_ops);
CREATE INDEX variables_name_trgm_idx ON catalog.variables USING gin (display_name_pt gin_trgm_ops);
CREATE INDEX variables_definition_trgm_idx ON catalog.variables USING gin (definition gin_trgm_ops);
CREATE INDEX product_variables_release_idx ON catalog.product_variables(release_id);
CREATE INDEX product_variables_variable_idx ON catalog.product_variables(variable_id);
CREATE INDEX distributions_release_idx ON catalog.distributions(release_id);
CREATE INDEX assertions_entity_idx ON catalog.metadata_assertions(entity_type, entity_stable_id);
CREATE INDEX reviews_entity_idx ON catalog.curation_reviews(entity_type, entity_stable_id);

CREATE VIEW catalog.v_product_catalog AS
SELECT
    p.stable_id AS product_id,
    s.stable_id AS source_id,
    s.source_name,
    pf.family_name,
    p.product_name,
    p.acronym,
    p.product_kind,
    p.product_description,
    p.scientific_object,
    p.information_message,
    p.primary_or_derived,
    p.geographic_coverage_text,
    p.covers_brazil,
    p.product_status,
    p.official_product_page_url,
    p.methodology_url,
    p.limitations_summary
FROM catalog.products p
JOIN catalog.sources s ON s.source_id = p.source_id
LEFT JOIN catalog.product_families pf ON pf.product_family_id = p.product_family_id;

CREATE VIEW catalog.v_product_variable_profiles AS
SELECT
    p.stable_id AS product_id,
    pr.stable_id AS release_id,
    pr.version_label,
    v.stable_id AS variable_id,
    v.display_name_pt AS variable_name,
    v.definition AS canonical_definition,
    pv.source_variable_name,
    pv.variable_role,
    pv.unit,
    pv.data_type,
    pv.interpretation,
    pv.scientific_potential,
    pv.non_interpretations,
    sp.support_type,
    sp.support_description,
    sp.nominal_resolution_value,
    sp.nominal_resolution_unit,
    tp.representation_type AS temporal_representation,
    tp.support_description AS temporal_support,
    m.method_type,
    m.method_name,
    qp.uncertainty_available,
    qp.uncertainty_type,
    pv.review_status
FROM catalog.product_variables pv
JOIN catalog.product_releases pr ON pr.release_id = pv.release_id
JOIN catalog.products p ON p.product_id = pr.product_id
JOIN catalog.variables v ON v.variable_id = pv.variable_id
LEFT JOIN catalog.spatial_profiles sp ON sp.spatial_profile_id = pv.spatial_profile_id
LEFT JOIN catalog.temporal_profiles tp ON tp.temporal_profile_id = pv.temporal_profile_id
LEFT JOIN catalog.methods m ON m.method_id = pv.method_id
LEFT JOIN catalog.quality_profiles qp ON qp.quality_profile_id = pv.quality_profile_id;

CREATE VIEW catalog.v_operational_access AS
SELECT
    p.stable_id AS product_id,
    pr.version_label,
    d.stable_id AS distribution_id,
    d.distribution_name,
    d.distribution_role,
    d.access_url,
    d.format,
    d.access_protocol,
    d.free_access,
    d.authentication_required,
    d.access_status,
    array_remove(array_agg(ac.capability_type) FILTER (WHERE ac.capability_status = 'available'), NULL) AS available_capabilities,
    array_remove(array_agg(ac.capability_type) FILTER (WHERE ac.capability_status = 'conditional'), NULL) AS conditional_capabilities
FROM catalog.distributions d
JOIN catalog.product_releases pr ON pr.release_id = d.release_id
JOIN catalog.products p ON p.product_id = pr.product_id
LEFT JOIN catalog.access_capabilities ac ON ac.distribution_id = d.distribution_id
GROUP BY p.stable_id, pr.version_label, d.stable_id, d.distribution_name,
         d.distribution_role, d.access_url, d.format, d.access_protocol,
         d.free_access, d.authentication_required, d.access_status;

COMMENT ON SCHEMA catalog IS
'Instance 1: relational catalog of georeferenced scientific products, their meaning, releases, variables, access, evidence and curation.';

COMMENT ON TABLE catalog.products IS
'Scientifically coherent product. Portals, generic catalogs, visualizers and processing infrastructures belong in sources or distributions, not here.';

COMMENT ON COLUMN catalog.products.information_message IS
'Plain-language statement of the scientific information conveyed by the product.';

COMMENT ON COLUMN catalog.products.non_representations IS
'Phenomena or interpretations that the product does not directly provide.';

COMMENT ON TABLE catalog.metadata_assertions IS
'Field-level evidence supporting curated metadata. Unknown facts remain unknown rather than being inferred.';

COMMIT;
