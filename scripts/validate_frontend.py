#!/usr/bin/env python3
"""Validação estrutural, de acessibilidade e de peso da interface estática."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PRODUCT_NAME = "Science Data Sources Catalog"
CANONICAL_SITE_URL = "https://ian-loc.github.io/ScienceDataSourcesCatalog/"
CANONICAL_REPOSITORY_URL = "https://github.com/Ian-loc/ScienceDataSourcesCatalog"
LEGACY_PUBLIC_TOKENS = ("Ecology Data Catalog", "Ian-loc/ecology-data-catalog", "github.io/ecology-data-catalog")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.local_refs: list[str] = []
        self.external_assets: list[str] = []
        self.tags: list[str] = []
        self.html_lang = ""
        self.has_viewport = False
        self.has_skip_link = False
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)

        if tag == "html":
            self.html_lang = values.get("lang") or ""
        if tag == "meta" and values.get("name") == "viewport":
            self.has_viewport = True
        if tag == "a" and "skip" in (values.get("class") or "").split() and (values.get("href") or "").startswith("#"):
            self.has_skip_link = True
        if values.get("id"):
            self.ids.append(values["id"] or "")

        reference = None
        if tag == "script":
            reference = values.get("src")
            if reference:
                self.scripts.append(reference)
        elif tag == "link" and values.get("rel") == "stylesheet":
            reference = values.get("href")
            if reference:
                self.stylesheets.append(reference)
        elif tag == "a":
            reference = values.get("href")

        if not reference or reference.startswith(("#", "mailto:", "tel:")):
            return
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc:
            if tag in {"script", "link"}:
                self.external_assets.append(reference)
            return
        path = parsed.path
        if path and not path.endswith("/"):
            self.local_refs.append(path)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def validate_page(filename: str, required_ids: set[str], require_noscript: bool = True) -> None:
    page_path = ROOT / filename
    if not page_path.exists():
        fail(f"página ausente: {filename}")

    content = page_path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(content)

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        fail(f"{filename}: IDs duplicados: {', '.join(duplicates)}")

    missing_ids = sorted(required_ids.difference(parser.ids))
    if missing_ids:
        fail(f"{filename}: IDs obrigatórios ausentes: {', '.join(missing_ids)}")

    if parser.html_lang != "pt-BR":
        fail(f"{filename}: atributo lang deve ser pt-BR")
    if not parser.has_viewport:
        fail(f"{filename}: meta viewport ausente")
    if not parser.has_skip_link:
        fail(f"{filename}: link para pular ao conteúdo ausente")
    if parser.tags.count("main") != 1:
        fail(f"{filename}: deve conter exatamente um elemento main")
    if parser.tags.count("h1") != 1:
        fail(f"{filename}: deve conter exatamente um h1")
    if require_noscript and "noscript" not in parser.tags:
        fail(f"{filename}: fallback noscript ausente")
    if parser.external_assets:
        fail(f"{filename}: dependências externas não permitidas: {', '.join(parser.external_assets)}")
    if "assets/style.css" not in parser.stylesheets or "assets/accessibility.css" not in parser.stylesheets:
        fail(f"{filename}: folhas de estilo locais obrigatórias ausentes")

    for reference in parser.local_refs:
        target = (page_path.parent / reference).resolve()
        if ROOT not in target.parents and target != ROOT:
            fail(f"{filename}: referência fora do repositório: {reference}")
        if not target.exists():
            fail(f"{filename}: referência local ausente: {reference}")

    required_tokens = {"aria-current", "theme-color", "color-scheme"}
    missing_tokens = sorted(token for token in required_tokens if token not in content)
    if missing_tokens:
        fail(f"{filename}: requisitos de navegação/metadados ausentes: {', '.join(missing_tokens)}")


def validate_public_identity() -> None:
    public_files = ("README.md", "index.html", "analytics.html", "about.html", "CITATION.cff")
    contents = {filename: (ROOT / filename).read_text(encoding="utf-8") for filename in public_files}

    for filename, content in contents.items():
        if CANONICAL_PRODUCT_NAME not in content:
            fail(f"{filename}: nome canônico do produto ausente")
        stale = sorted(token for token in LEGACY_PUBLIC_TOKENS if token in content)
        if stale:
            fail(f"{filename}: identidade ou URL legada presente: {', '.join(stale)}")

    for filename in ("README.md", "about.html", "CITATION.cff"):
        if CANONICAL_SITE_URL not in contents[filename]:
            fail(f"{filename}: URL canônica do site ausente")
        if CANONICAL_REPOSITORY_URL not in contents[filename]:
            fail(f"{filename}: URL canônica do repositório ausente")


def validate_catalog_fields() -> None:
    app_path = ROOT / "assets" / "app.js"
    content = app_path.read_text(encoding="utf-8")
    required_fields = {
        "resource_id", "resource_name", "acronym", "official_identity", "description",
        "homepage_url", "data_access_url", "research_areas", "keywords",
        "data_product_types", "data_formats", "visualization_types",
        "geographic_coverage", "covers_brazil", "spatial_resolution",
        "temporal_coverage", "temporal_resolution", "data_sources", "free_download",
        "access_conditions", "programmatic_access", "access_protocols",
        "authentication_required", "access_documentation_url", "license",
        "institutional_status", "owner_or_manager", "academic_uses", "limitations",
        "academic_evidence_type", "academic_evidence_url", "academic_evidence_note",
        "verification_url", "last_verified",
    }
    missing = sorted(field for field in required_fields if f"resource.{field}" not in content)
    if missing:
        fail(f"assets/app.js não referencia todos os campos do catálogo: {', '.join(missing)}")

    required_groups = {
        "Acesso", "Cobertura", "Produtos e dados", "Uso acadêmico",
        "Evidências", "Avaliação e governança",
    }
    missing_groups = sorted(group for group in required_groups if f'"{group}"' not in content)
    if missing_groups:
        fail(f"assets/app.js não contém todos os grupos técnicos: {', '.join(missing_groups)}")

    required_accessibility = {
        'role="listitem"', "aria-labelledby", "aria-describedby", "aria-busy",
        "prefers-reduced-motion", "noopener noreferrer", "catalogHeading.focus",
    }
    missing_accessibility = sorted(token for token in required_accessibility if token not in content)
    if missing_accessibility:
        fail(f"assets/app.js perdeu garantias de acessibilidade: {', '.join(missing_accessibility)}")


def validate_accessibility_css() -> None:
    path = ROOT / "assets" / "accessibility.css"
    if not path.exists():
        fail("assets/accessibility.css ausente")
    content = path.read_text(encoding="utf-8")
    required = {".sr-only", "prefers-reduced-motion", "forced-colors", ".noscript", "@media(max-width:1080px)"}
    missing = sorted(token for token in required if token not in content)
    if missing:
        fail(f"assets/accessibility.css incompleto: {', '.join(missing)}")


def validate_size_budget() -> None:
    limits = {
        "index.html": 20_000,
        "analytics.html": 12_000,
        "about.html": 20_000,
        "assets/style.css": 30_000,
        "assets/accessibility.css": 10_000,
        "assets/app.js": 50_000,
        "assets/analytics.js": 15_000,
        "assets/build-meta.js": 5_000,
    }
    total = 0
    for filename, limit in limits.items():
        path = ROOT / filename
        size = path.stat().st_size
        total += size
        if size > limit:
            fail(f"{filename}: {size} bytes excede o limite de {limit} bytes")
    if total > 120_000:
        fail(f"interface estática excede orçamento total: {total} > 120000 bytes")
    print(f"OK: orçamento da interface = {total} bytes")


validate_page(
    "index.html",
    {
        "conteudo", "areas", "areas-heading", "area-links", "catalogo", "catalog-heading",
        "hero-search", "search-help", "q", "filters", "filter-note", "area", "brazil",
        "download", "programmatic", "coverage", "format", "evidence", "sort",
        "advanced-filters", "advanced-count", "active-filters", "clear", "list", "empty",
        "count", "n-total", "n-free", "n-api", "n-br", "updated",
    },
)
validate_page("about.html", {"sobre"})
validate_page(
    "analytics.html",
    {
        "analise", "summary-heading", "summary", "chart-areas", "chart-download",
        "chart-programmatic", "chart-brazil", "chart-evidence", "chart-formats",
        "chart-visualizations",
    },
)
validate_public_identity()
validate_catalog_fields()
validate_accessibility_css()
validate_size_budget()

print("OK: HTML, acessibilidade estrutural, dependências, campos e desempenho validados")
