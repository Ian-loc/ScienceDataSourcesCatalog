#!/usr/bin/env python3
"""Correct Dynamic World access-test states to match the strength of evidence."""
from __future__ import annotations

import argparse
import os
import sys

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)

EXPECTED = {
    "DD000016": ("working", True),
    "DD000017": ("unknown", False),
    "DD000018": ("working", True),
    "DD000019": ("unknown", False),
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

    with psycopg.connect(args.database_url) as connection:
        connection.execute(
            """
            UPDATE catalog.distributions
            SET access_status='unknown',
                last_access_tested_at=NULL,
                service_level_notes=concat_ws(
                    ' ', service_level_notes,
                    'Endpoint role classified, but no direct operational test is asserted.'
                ),
                updated_at=now()
            WHERE stable_id IN ('DD000017','DD000019')
            """
        )
        rows = connection.execute(
            """
            SELECT stable_id, access_status, last_access_tested_at
            FROM catalog.distributions
            WHERE stable_id IN ('DD000016','DD000017','DD000018','DD000019')
            """
        ).fetchall()
        by_id = {str(row[0]): row for row in rows}
        if set(by_id) != set(EXPECTED):
            raise ValueError(f"distribuições divergentes: {sorted(by_id)}")
        for stable_id, (status, tested) in EXPECTED.items():
            row = by_id[stable_id]
            if row[1] != status:
                raise ValueError(f"{stable_id}: status={row[1]}; esperado={status}")
            if tested != (row[2] is not None):
                raise ValueError(
                    f"{stable_id}: estado de last_access_tested_at incompatível com evidência"
                )

    print("OK: estados de teste operacional Dynamic World corrigidos")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
