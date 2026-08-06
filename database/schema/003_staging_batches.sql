-- Instance 1 staging load batches and idempotent history
-- Target: PostgreSQL 16+

BEGIN;

CREATE TABLE IF NOT EXISTS staging.load_batches (
    batch_id bigserial PRIMARY KEY,
    status text NOT NULL CHECK (status IN ('loading', 'successful', 'failed')),
    loader_version text NOT NULL,
    repository_sha text,
    resource_file_name text NOT NULL,
    resource_file_hash text NOT NULL,
    resource_row_count integer NOT NULL CHECK (resource_row_count >= 0),
    product_file_name text NOT NULL,
    product_file_hash text NOT NULL,
    product_row_count integer NOT NULL CHECK (product_row_count >= 0),
    distribution_file_name text NOT NULL,
    distribution_file_hash text NOT NULL,
    distribution_row_count integer NOT NULL CHECK (distribution_row_count >= 0),
    started_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    notes text,
    UNIQUE (
        resource_file_hash,
        product_file_hash,
        distribution_file_hash,
        status
    )
);

ALTER TABLE staging.legacy_resources
ADD COLUMN IF NOT EXISTS load_batch_id bigint;

ALTER TABLE staging.legacy_products
ADD COLUMN IF NOT EXISTS load_batch_id bigint;

ALTER TABLE staging.legacy_distributions
ADD COLUMN IF NOT EXISTS load_batch_id bigint;

ALTER TABLE staging.migration_issues
ADD COLUMN IF NOT EXISTS load_batch_id bigint;

DO $$
DECLARE
    bootstrap_batch_id bigint;
BEGIN
    IF EXISTS (
        SELECT 1 FROM staging.legacy_resources WHERE load_batch_id IS NULL
    ) OR EXISTS (
        SELECT 1 FROM staging.legacy_products WHERE load_batch_id IS NULL
    ) OR EXISTS (
        SELECT 1 FROM staging.legacy_distributions WHERE load_batch_id IS NULL
    ) OR EXISTS (
        SELECT 1 FROM staging.migration_issues WHERE load_batch_id IS NULL
    ) THEN
        INSERT INTO staging.load_batches (
            status,
            loader_version,
            resource_file_name,
            resource_file_hash,
            resource_row_count,
            product_file_name,
            product_file_hash,
            product_row_count,
            distribution_file_name,
            distribution_file_hash,
            distribution_row_count,
            notes,
            completed_at
        )
        VALUES (
            'successful',
            'bootstrap-pre-batch',
            'unknown',
            'bootstrap-resources',
            (SELECT count(*) FROM staging.legacy_resources),
            'unknown',
            'bootstrap-products',
            (SELECT count(*) FROM staging.legacy_products),
            'unknown',
            'bootstrap-distributions',
            (SELECT count(*) FROM staging.legacy_distributions),
            'Created while upgrading a staging schema that already contained rows.',
            now()
        )
        RETURNING batch_id INTO bootstrap_batch_id;

        UPDATE staging.legacy_resources
        SET load_batch_id = bootstrap_batch_id
        WHERE load_batch_id IS NULL;

        UPDATE staging.legacy_products
        SET load_batch_id = bootstrap_batch_id
        WHERE load_batch_id IS NULL;

        UPDATE staging.legacy_distributions
        SET load_batch_id = bootstrap_batch_id
        WHERE load_batch_id IS NULL;

        UPDATE staging.migration_issues
        SET load_batch_id = bootstrap_batch_id
        WHERE load_batch_id IS NULL;
    END IF;
END
$$;

ALTER TABLE staging.legacy_resources
ALTER COLUMN load_batch_id SET NOT NULL;

ALTER TABLE staging.legacy_products
ALTER COLUMN load_batch_id SET NOT NULL;

ALTER TABLE staging.legacy_distributions
ALTER COLUMN load_batch_id SET NOT NULL;

ALTER TABLE staging.migration_issues
ALTER COLUMN load_batch_id SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'legacy_resources_load_batch_fk'
    ) THEN
        ALTER TABLE staging.legacy_resources
        ADD CONSTRAINT legacy_resources_load_batch_fk
        FOREIGN KEY (load_batch_id)
        REFERENCES staging.load_batches(batch_id)
        ON DELETE RESTRICT;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'legacy_products_load_batch_fk'
    ) THEN
        ALTER TABLE staging.legacy_products
        ADD CONSTRAINT legacy_products_load_batch_fk
        FOREIGN KEY (load_batch_id)
        REFERENCES staging.load_batches(batch_id)
        ON DELETE RESTRICT;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'legacy_distributions_load_batch_fk'
    ) THEN
        ALTER TABLE staging.legacy_distributions
        ADD CONSTRAINT legacy_distributions_load_batch_fk
        FOREIGN KEY (load_batch_id)
        REFERENCES staging.load_batches(batch_id)
        ON DELETE RESTRICT;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'migration_issues_load_batch_fk'
    ) THEN
        ALTER TABLE staging.migration_issues
        ADD CONSTRAINT migration_issues_load_batch_fk
        FOREIGN KEY (load_batch_id)
        REFERENCES staging.load_batches(batch_id)
        ON DELETE RESTRICT;
    END IF;
END
$$;

DROP INDEX IF EXISTS staging.legacy_resources_resource_id_idx;
DROP INDEX IF EXISTS staging.legacy_products_product_id_idx;
DROP INDEX IF EXISTS staging.legacy_distributions_distribution_id_idx;

CREATE UNIQUE INDEX IF NOT EXISTS legacy_resources_batch_resource_idx
ON staging.legacy_resources(load_batch_id, resource_id)
WHERE resource_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS legacy_products_batch_product_idx
ON staging.legacy_products(load_batch_id, product_id)
WHERE product_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS legacy_distributions_batch_distribution_idx
ON staging.legacy_distributions(load_batch_id, distribution_id)
WHERE distribution_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS legacy_products_batch_resource_idx
ON staging.legacy_products(load_batch_id, resource_id);

CREATE INDEX IF NOT EXISTS legacy_distributions_batch_product_idx
ON staging.legacy_distributions(load_batch_id, product_id);

CREATE UNIQUE INDEX IF NOT EXISTS migration_issues_batch_code_idx
ON staging.migration_issues(
    load_batch_id,
    entity_type,
    legacy_id,
    issue_code
);

CREATE OR REPLACE VIEW staging.v_latest_successful_batch AS
SELECT *
FROM staging.load_batches
WHERE status = 'successful'
ORDER BY batch_id DESC
LIMIT 1;

CREATE OR REPLACE VIEW staging.v_latest_resources AS
SELECT r.*
FROM staging.legacy_resources r
JOIN staging.v_latest_successful_batch b
  ON b.batch_id = r.load_batch_id;

CREATE OR REPLACE VIEW staging.v_latest_products AS
SELECT p.*
FROM staging.legacy_products p
JOIN staging.v_latest_successful_batch b
  ON b.batch_id = p.load_batch_id;

CREATE OR REPLACE VIEW staging.v_latest_distributions AS
SELECT d.*
FROM staging.legacy_distributions d
JOIN staging.v_latest_successful_batch b
  ON b.batch_id = d.load_batch_id;

CREATE OR REPLACE VIEW staging.v_unresolved_products AS
SELECT p.*
FROM staging.v_latest_products p
WHERE p.migration_status IN ('pending', 'blocked')
   OR p.resolved_entity_type IS NULL
   OR p.resolved_entity_type = 'unknown';

CREATE OR REPLACE VIEW staging.v_blocking_issues AS
SELECT i.*
FROM staging.migration_issues i
JOIN staging.v_latest_successful_batch b
  ON b.batch_id = i.load_batch_id
WHERE i.severity = 'blocking'
  AND i.resolution_status = 'open';

COMMENT ON TABLE staging.load_batches IS
'Immutable manifest for each complete staging load. Identical successful hashes are treated as an idempotent no-op.';

COMMENT ON VIEW staging.v_latest_products IS
'Legacy product rows from the most recent successful load only.';

COMMIT;
