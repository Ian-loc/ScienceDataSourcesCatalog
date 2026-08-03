#!/usr/bin/env python3
"""Build the curated static artifact published by GitHub Pages.

The public website must contain only user-facing HTML, assets and catalog data.
Operational documentation, audits, migration files, scripts and workflows remain
available in the GitHub repository but are not copied to the Pages artifact.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"

REQUIRED_FILES = (
    "index.html",
    "products.html",
    "explorer.html",
    "analytics.html",
    "about.html",
    "LICENSE",
    "LICENSE-DATA.md",
    "data/data_resources.csv",
    "data/data_resources.json",
    "data/data_products.csv",
    "data/data_products.json",
    "data/product_distributions.csv",
    "data/brazil_scope_priorities.json",
    "data/federated_layers.json",
    "data/build-meta.json",
)

OPTIONAL_FILES = (
    "404.html",
    "CNAME",
    "favicon.ico",
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
    "data/product_distributions.json",
)

REQUIRED_DIRECTORIES = ("assets",)


def copy_file(relative_path: str, *, required: bool) -> None:
    source = ROOT / relative_path
    if not source.exists():
        if required:
            raise SystemExit(f"ERRO: arquivo público obrigatório ausente: {relative_path}")
        return
    destination = OUTPUT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)

    for relative_path in REQUIRED_FILES:
        copy_file(relative_path, required=True)
    for relative_path in OPTIONAL_FILES:
        copy_file(relative_path, required=False)

    for relative_path in REQUIRED_DIRECTORIES:
        source = ROOT / relative_path
        if not source.is_dir():
            raise SystemExit(f"ERRO: diretório público obrigatório ausente: {relative_path}")
        shutil.copytree(source, OUTPUT / relative_path)

    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")

    forbidden = (
        "WORKFLOW_STATUS.md",
        "IMPLEMENTATION_WORKFLOW.md",
        "DOCUMENTATION_CONSISTENCY_AUDIT.md",
        "migration",
        "scripts",
        ".github",
        "audit",
        "schema",
        "release",
    )
    leaked = [name for name in forbidden if (OUTPUT / name).exists()]
    if leaked:
        raise SystemExit("ERRO: artefato público contém material interno: " + ", ".join(leaked))

    files = sum(1 for path in OUTPUT.rglob("*") if path.is_file())
    print(f"OK: artefato público criado em {OUTPUT} com {files} arquivos")


if __name__ == "__main__":
    main()
