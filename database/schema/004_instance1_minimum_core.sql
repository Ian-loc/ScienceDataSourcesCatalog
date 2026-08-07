-- Simbiotrama / Science Data Sources Catalog
-- Instance 1: additive minimum-sufficient catalog core
-- This migration is intentionally additive. Legacy/deep tables remain available
-- for transition and audit, but are not authority for the simplified core.

BEGIN;

CREATE TABLE IF NOT EXISTS catalog.catalog_entries (
    entry_id bigserial PRIMARY KEY,
    stable_id text NOT NULL UNIQUE,
    organization_id bigint REFERENCES catalog.organizations(organization_id),
    parent_entry_id bigint REFERENCES catalog.catalog_entries(entry_id),
    entry_type text NOT NULL CHECK (entry_type IN (
        'source','platform','collection','product','service'
    )),
    official_name text NOT NULL,
    acronym text,
    summary text NOT NULL,
    scientific_scope text,
    data_modalities text[] NOT NULL DEFAULT ARRAY[]::text[],
    geographic_coverage_text text,
    temporal_coverage_text text,
    spatial_resolution_text text,
    update_frequency_text text,
    access_level text NOT NULL DEFAULT 'unknown' CHECK (access_level IN (
        'open','partial','restricted','unknown','not_applicable'
    )),
    free_access text NOT NULL DEFAULT 'unknown' CHECK (free_access IN (
        'yes','partial','no','unknown','not_applicable'
    )),
    authentication_required text NOT NULL DEFAULT 'unknown' CHECK (authentication_required IN (
        'yes','partial','no','unknown','not_applicable'
    )),
    official_page_url text,
    metadata_url text,
    primary_access_url text,
    methodology_url text,
    license_text text,
    license_url text,
    citation_text text,
    citation_url text,
    curation_status text NOT NULL DEFAULT 'needs_review' CHECK (curation_status IN (
        'needs_review','partially_verified','verified'
    )),
    last_verified_at date,
    additional_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    source_record_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS catalog_entries_organization_idx
ON catalog.catalog_entries (organization_id);

CREATE INDEX IF NOT EXISTS catalog_entries_type_idx
ON catalog.catalog_entries (entry_type);

CREATE INDEX IF NOT EXISTS catalog_entries_status_idx
ON catalog.catalog_entries (curation_status);

CREATE TABLE IF NOT EXISTS catalog.entry_variables (
    entry_variable_id bigserial PRIMARY KEY,
    entry_id bigint NOT NULL REFERENCES catalog.catalog_entries(entry_id) ON DELETE CASCADE,
    term_role text NOT NULL DEFAULT 'variable' CHECK (term_role IN ('theme','variable')),
    source_label text NOT NULL,
    source_definition text,
    search_label text,
    variable_group text,
    unit_text text,
    verification_status text NOT NULL DEFAULT 'needs_review' CHECK (verification_status IN (
        'needs_review','partially_verified','verified','not_found','not_applicable'
    )),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (entry_id, term_role, source_label)
);

CREATE INDEX IF NOT EXISTS entry_variables_entry_idx
ON catalog.entry_variables (entry_id);

CREATE INDEX IF NOT EXISTS entry_variables_search_label_idx
ON catalog.entry_variables (search_label);

CREATE TABLE IF NOT EXISTS catalog.entry_evidence (
    evidence_id bigserial PRIMARY KEY,
    entry_id bigint NOT NULL REFERENCES catalog.catalog_entries(entry_id) ON DELETE CASCADE,
    field_name text,
    evidence_url text,
    evidence_role text NOT NULL CHECK (evidence_role IN (
        'official_page','official_metadata','methodology','license','citation','access','other'
    )),
    support_note text,
    verification_status text NOT NULL DEFAULT 'needs_review' CHECK (verification_status IN (
        'needs_review','partially_verified','verified','not_found','not_applicable'
    )),
    retrieved_at date,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (evidence_url IS NOT NULL OR verification_status IN ('not_found','not_applicable'))
);

CREATE INDEX IF NOT EXISTS entry_evidence_entry_idx
ON catalog.entry_evidence (entry_id);

CREATE INDEX IF NOT EXISTS entry_evidence_status_idx
ON catalog.entry_evidence (verification_status);

CREATE UNIQUE INDEX IF NOT EXISTS entry_evidence_proportional_unique_idx
ON catalog.entry_evidence (
    entry_id,
    COALESCE(field_name, ''),
    evidence_role,
    COALESCE(evidence_url, '')
);

INSERT INTO catalog.schema_migrations (version, description)
VALUES ('004', 'Additive minimum-sufficient Instance 1 catalog core')
ON CONFLICT (version) DO NOTHING;

COMMIT;
