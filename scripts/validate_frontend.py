#!/usr/bin/env python3
"""Validação estrutural mínima da interface estática."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.local_refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        reference = values.get("src") if tag == "script" else values.get("href") if tag in {"a", "link"} else None
        if not reference or reference.startswith(("#", "mailto:", "tel:")):
            return
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc:
            return
        path = parsed.path
        if path and not path.endswith("/"):
            self.local_refs.append(path)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def validate_page(filename: str, required_ids: set[str]) -> None:
    page_path = ROOT / filename
    if not page_path.exists():
        fail(f"página ausente: {filename}")

    parser = PageParser()
    parser.feed(page_path.read_text(encoding="utf-8"))

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        fail(f"{filename}: IDs duplicados: {', '.join(duplicates)}")

    missing_ids = sorted(required_ids.difference(parser.ids))
    if missing_ids:
        fail(f"{filename}: IDs obrigatórios ausentes: {', '.join(missing_ids)}")

    for reference in parser.local_refs:
        target = (page_path.parent / reference).resolve()
        if ROOT not in target.parents and target != ROOT:
            fail(f"{filename}: referência fora do repositório: {reference}")
        if not target.exists():
            fail(f"{filename}: referência local ausente: {reference}")


validate_page(
    "index.html",
    {
        "conteudo", "areas", "area-links", "catalogo", "hero-search", "q", "filters",
        "area", "brazil", "download", "programmatic", "coverage", "format", "evidence",
        "sort", "advanced-filters", "advanced-count", "active-filters", "clear", "list",
        "empty", "count", "n-total", "n-free", "n-api", "n-br", "updated",
    },
)
validate_page("about.html", {"sobre"})
validate_page(
    "analytics.html",
    {
        "analise", "summary", "chart-areas", "chart-download", "chart-programmatic",
        "chart-brazil", "chart-evidence", "chart-formats", "chart-visualizations",
    },
)

print("OK: estrutura HTML, IDs da interface e referências locais validados")
