#!/usr/bin/env python3
"""Validate Dynamic World endpoint statuses against available operational evidence."""
from __future__ import annotations

import argparse
import os
import sys

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)

EXPECTED = {
    "DD000016": ("api", "working", True),
    "DD000017": ("catalog_record", "unknown", False),
    "DD000018": ("visualizer", "working", True),
    "DD000019": ("code_repository", "unknown", False),
}


def psycopg_module():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit("Instale database/requirements.txt") from exc
    return psycopg


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DATABASE_URL)
    args = parser.parse_args()
    psycopg = psycopg_module()
    failures: list[str] = []

    with psycopg.connect(args.database_url) as connection:
        rows = connection.execute(
            """
            SELECT stable_id, distribution_role, access_status, last_access_tested_at
            FROM catalog.distributions
            WHERE stable_id IN ('DD000016','DD000017','DD000018','DD000019')
            """
        ).fetchall()
        by_id = {str(row[0]): row for row in rows}
        for stable_id, (role, status, tested) in EXPECTED.items():
            row = by_id.get(stable_id)
            if row is None:
                failures.append(f"{stable_id}: ausente")
                continue
            if row[1] != role:
                failures.append(f"{stable_id}: role={row[1]}; esperado={role}")
            if row[2] != status:
                failures.append(f"{stable_id}: status={row[2]}; esperado={status}")
            if tested != (row[3] is not None):
                failures.append(
                    f"{stable_id}: timestamp de teste incompatível com estado de evidência"
                )

        overclaimed = int(connection.execute(
            """
            SELECT count(*)
            FROM catalog.distributions
            WHERE stable_id IN ('DD000017','DD000019')
              AND (access_status='working' OR last_access_tested_at IS NOT NULL)
            """
        ).fetchone()[0])
        if overclaimed:
            failures.append(
                f"{overclaimed} endpoint(s) apenas classificado(s) marcado(s) como testado(s)"
            )

    if failures:
        print("ERRO: força da evidência operacional Dynamic World inconsistente", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("OK: estado operacional Dynamic World proporcional à evidência")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
