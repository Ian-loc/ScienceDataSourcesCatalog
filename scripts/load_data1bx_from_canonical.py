#!/usr/bin/env python3
"""Materializa ou confere a projeção inicial DATA1-BX a partir do CSV 0.7.0.

A projeção copia valores existentes sem promover a confiança ou alegar revisão
externa. As cinco dimensões continuam explicitamente pendentes.
"""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data" / "data_resources.csv"
TARGET_PATH = ROOT / "migration" / "data1bx_migration_matrix.csv"

DIMENSIONS = [
    "data_product_types",
    "visualization_types",
    "data_sources",
    "temporal_resolution",
    "access_conditions",
]
HEADER = ["resource_id"]
for field in DIMENSIONS:
    HEADER.extend([f"{field}_proposed", f"{field}_confidence"])
HEADER.extend([
    "bx_review_status",
    "bx_evidence_basis",
    "bx_evidence_url",
    "bx_last_verified",
    "bx_reviewer",
    "bx_unresolved_fields",
    "bx_notes",
])
UNRESOLVED = " | ".join(DIMENSIONS)
NOTE = "Valor copiado do CSV canônico 0.7.0; requer verificação externa por dimensão."


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def build_projection() -> str:
    with SOURCE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            fail("CSV canônico sem cabeçalho")
        missing = [field for field in ["resource_id", *DIMENSIONS] if field not in reader.fieldnames]
        if missing:
            fail(f"CSV canônico sem campos DATA1-BX: {', '.join(missing)}")
        source_rows = list(reader)

    if len(source_rows) != 51:
        fail(f"esperadas 51 fontes; encontradas {len(source_rows)}")

    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=HEADER, lineterminator="\n")
    writer.writeheader()

    for source in source_rows:
        row: dict[str, str] = {"resource_id": source["resource_id"].strip()}
        for field in DIMENSIONS:
            value = source[field].strip()
            if not value:
                fail(f"{source['resource_id']}: campo canônico vazio: {field}")
            row[f"{field}_proposed"] = value
            row[f"{field}_confidence"] = "desconhecida"
        row.update({
            "bx_review_status": "carregado_do_csv",
            "bx_evidence_basis": "canonical_csv",
            "bx_evidence_url": "",
            "bx_last_verified": "",
            "bx_reviewer": "",
            "bx_unresolved_fields": UNRESOLVED,
            "bx_notes": NOTE,
        })
        writer.writerow(row)

    return output.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="substitui a matriz pela projeção canônica")
    args = parser.parse_args()
    expected = build_projection()

    if args.write:
        TARGET_PATH.write_text(expected, encoding="utf-8")
        print("OK: matriz DATA1-BX materializada com 51 valores canônicos e confiança desconhecida")
        return

    current = TARGET_PATH.read_text(encoding="utf-8-sig")
    if current != expected:
        fail("matriz DATA1-BX diverge da projeção canônica; execute com --write ou revise a etapa")
    print("OK: matriz DATA1-BX corresponde à projeção canônica 51 × 5; revisão externa ainda pendente")


if __name__ == "__main__":
    main()
