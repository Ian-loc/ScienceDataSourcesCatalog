#!/usr/bin/env python3
"""Validate the materialized Instance 1 staging database."""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://catalog:catalog_dev_only@localhost:5432/science_data_catalog",
)


def csv_count(path: Path) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def import_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "psycopg não instalado. Execute: "
            "python -m pip install -r database/requirements.txt"
        ) from exc
    return psycopg


def scalar(connection, query: str, params: tuple[object, ...] = ()) -> int:
    return int(connection.execute(query, params).fetchone()[0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    args = parser.parse_args()

    expected = {
        "resources": csv_count(ROOT / "data" / "data_resources.csv"),
        "products": csv_count(ROOT / "data" / "data_products.csv"),
        "distributions": csv_count(ROOT / "data" / "product_distributions.csv"),
    }

    psycopg = import_psycopg()
    with psycopg.connect(args.database_url) as connection:
        batch = connection.execute(
            """
            SELECT batch_id, resource_row_count, product_row_count,
                   distribution_row_count
            FROM staging.v_latest_successful_batch
            """
        ).fetchone()
        if batch is None:
            print("ERRO: nenhum lote bem-sucedido no staging", file=sys.stderr)
            return 1

        batch_id = int(batch[0])
        declared = {
            "resources": int(batch[1]),
            "products": int(batch[2]),
            "distributions": int(batch[3]),
        }
        actual = {
            "resources": scalar(
                connection,
                "SELECT count(*) FROM staging.v_latest_resources",
            ),
            "products": scalar(
                connection,
                "SELECT count(*) FROM staging.v_latest_products",
            ),
            "distributions": scalar(
                connection,
                "SELECT count(*) FROM staging.v_latest_distributions",
            ),
        }

        failures: list[str] = []
        for name in expected:
            if declared[name] != expected[name]:
                failures.append(
                    f"{name}: manifesto={declared[name]} CSV={expected[name]}"
                )
            if actual[name] != expected[name]:
                failures.append(
                    f"{name}: banco={actual[name]} CSV={expected[name]}"
                )

        duplicate_checks = {
            "resource_id": """
                SELECT count(*) FROM (
                    SELECT resource_id
                    FROM staging.v_latest_resources
                    GROUP BY resource_id
                    HAVING count(*) > 1
                ) x
            """,
            "product_id": """
                SELECT count(*) FROM (
                    SELECT product_id
                    FROM staging.v_latest_products
                    GROUP BY product_id
                    HAVING count(*) > 1
                ) x
            """,
            "distribution_id": """
                SELECT count(*) FROM (
                    SELECT distribution_id
                    FROM staging.v_latest_distributions
                    GROUP BY distribution_id
                    HAVING count(*) > 1
                ) x
            """,
        }
        for label, query in duplicate_checks.items():
            count = scalar(connection, query)
            if count:
                failures.append(f"{label}: {count} duplicata(s)")

        orphan_products = scalar(
            connection,
            """
            SELECT count(*)
            FROM staging.v_latest_products p
            LEFT JOIN staging.v_latest_resources r
              ON r.resource_id = p.resource_id
            WHERE r.resource_id IS NULL
            """,
        )
        orphan_distributions = scalar(
            connection,
            """
            SELECT count(*)
            FROM staging.v_latest_distributions d
            LEFT JOIN staging.v_latest_products p
              ON p.product_id = d.product_id
            WHERE p.product_id IS NULL
            """,
        )
        unresolved = scalar(
            connection,
            "SELECT count(*) FROM staging.v_unresolved_products",
        )
        blocking = scalar(
            connection,
            "SELECT count(*) FROM staging.v_blocking_issues",
        )
        if orphan_products:
            failures.append(f"{orphan_products} produto(s) órfão(s)")
        if orphan_distributions:
            failures.append(f"{orphan_distributions} distribuição(ões) órfã(s)")
        if unresolved:
            failures.append(f"{unresolved} linha(s) piloto sem resolução de entidade")
        if blocking:
            failures.append(f"{blocking} problema(s) bloqueante(s) aberto(s)")

        resolution = dict(
            connection.execute(
                """
                SELECT resolved_entity_type, count(*)
                FROM staging.v_latest_products
                GROUP BY resolved_entity_type
                ORDER BY resolved_entity_type
                """
            ).fetchall()
        )

        if failures:
            print("ERRO: staging inválido", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 1

        print(
            "OK: staging materializado e íntegro — "
            f"batch={batch_id}; fontes={actual['resources']}; "
            f"produtos_legados={actual['products']}; "
            f"distribuições={actual['distributions']}; "
            f"resolução={resolution}"
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
