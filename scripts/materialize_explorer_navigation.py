#!/usr/bin/env python3
"""Add the federated explorer to existing public navigation and action areas."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "index.html": [
        (
            '<a href="products.html">Produtos</a><a href="analytics.html">Análise</a>',
            '<a href="products.html">Produtos</a><a href="explorer.html">Explorador</a><a href="analytics.html">Análise</a>',
        ),
        (
            '<a href="products.html">Buscar produtos específicos</a><a href="analytics.html">Analisar o catálogo</a>',
            '<a href="products.html">Buscar produtos específicos</a><a href="explorer.html">Abrir explorador federado</a><a href="analytics.html">Analisar o catálogo</a>',
        ),
    ],
    "products.html": [
        (
            '<a href="products.html" aria-current="page">Produtos</a><a href="analytics.html">Análise</a>',
            '<a href="products.html" aria-current="page">Produtos</a><a href="explorer.html">Explorador</a><a href="analytics.html">Análise</a>',
        ),
        (
            '<a href="index.html#catalogo">Explorar fontes</a><a href="data/data_products.csv" download>',
            '<a href="index.html#catalogo">Explorar fontes</a><a href="explorer.html">Visualizar camadas</a><a href="data/data_products.csv" download>',
        ),
    ],
    "analytics.html": [
        (
            '<a href="products.html">Produtos</a><a href="analytics.html" aria-current="page">Análise</a>',
            '<a href="products.html">Produtos</a><a href="explorer.html">Explorador</a><a href="analytics.html" aria-current="page">Análise</a>',
        ),
        (
            '<a class="btn" href="products.html">Buscar produtos</a><a class="btn" href="about.html">Método e citação</a>',
            '<a class="btn" href="products.html">Buscar produtos</a><a class="btn" href="explorer.html">Abrir explorador</a><a class="btn" href="about.html">Método e citação</a>',
        ),
    ],
    "about.html": [
        (
            '<a href="products.html">Produtos</a><a href="analytics.html">Análise</a>',
            '<a href="products.html">Produtos</a><a href="explorer.html">Explorador</a><a href="analytics.html">Análise</a>',
        ),
        (
            '<a class="btn" href="products.html">Buscar produtos</a><a class="btn" href="analytics.html">Analisar o catálogo</a>',
            '<a class="btn" href="products.html">Buscar produtos</a><a class="btn" href="explorer.html">Abrir explorador</a><a class="btn" href="analytics.html">Analisar o catálogo</a>',
        ),
    ],
}


def main() -> None:
    for filename, replacements in REPLACEMENTS.items():
        path = ROOT / filename
        content = path.read_text(encoding="utf-8")
        if content.count('href="explorer.html"') >= 1:
            print(f"OK: {filename} já contém o explorador")
            continue
        for old, new in replacements:
            if old not in content:
                raise SystemExit(f"ERRO: padrão não localizado em {filename}: {old}")
            content = content.replace(old, new, 1)
        path.write_text(content, encoding="utf-8")
        print(f"OK: navegação atualizada em {filename}")


if __name__ == "__main__":
    main()
