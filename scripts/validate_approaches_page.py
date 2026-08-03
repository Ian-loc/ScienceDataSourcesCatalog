#!/usr/bin/env python3
"""Validate the standalone alternatives page without coupling it to main navigation."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "abordagens.html"
CSS_PATH = ROOT / "assets" / "approaches.css"

REQUIRED_IDS = {
    "abordagens",
    "decision-heading",
    "comparison-heading",
    "architecture-heading",
    "path-heading",
    "guardrails-heading",
}
REQUIRED_TOKENS = {
    "Catálogo público preservado",
    "Acesso executável e download assistido",
    "Visualização federada",
    "Compositor territorial reproduzível",
    "Esta página não altera o conjunto canônico nem a interface principal.",
    'href="index.html"',
    'href="explorer.html"',
    'aria-current="page"',
}
REQUIRED_CSS = {
    ".approaches-hero",
    ".approach-grid",
    ".approach-card",
    ".comparison",
    ".architecture-grid",
    ".path-list",
    ".guardrails",
    "@media(max-width:900px)",
    "prefers-reduced-motion",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.tags: list[str] = []
        self.lang = ""
        self.viewport = False
        self.skip = False
        self.local_refs: list[str] = []
        self.external_assets: list[str] = []
        self.styles: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = values.get("lang") or ""
        if tag == "meta" and values.get("name") == "viewport":
            self.viewport = True
        if tag == "a" and "skip" in (values.get("class") or "").split():
            self.skip = True
        if values.get("id"):
            self.ids.append(values["id"] or "")

        reference = None
        if tag == "script" and values.get("src"):
            reference = values["src"]
            self.scripts.append(reference)
        elif tag == "link" and values.get("rel") == "stylesheet" and values.get("href"):
            reference = values["href"]
            self.styles.append(reference)
        elif tag == "a" and values.get("href"):
            reference = values["href"]

        if not reference or reference.startswith(("#", "mailto:", "tel:")):
            return
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc:
            if tag in {"script", "link"}:
                self.external_assets.append(reference)
            return
        if parsed.path and not parsed.path.endswith("/"):
            self.local_refs.append(parsed.path)


for path in (HTML_PATH, CSS_PATH):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"artefato ausente ou vazio: {path.relative_to(ROOT)}")

html = HTML_PATH.read_text(encoding="utf-8")
parser = PageParser()
parser.feed(html)

if parser.lang != "pt-BR" or not parser.viewport or not parser.skip:
    fail("abordagens.html perdeu requisitos básicos de acessibilidade")
if parser.tags.count("main") != 1 or parser.tags.count("h1") != 1 or "noscript" not in parser.tags:
    fail("abordagens.html deve conter um main, um h1 e fallback noscript")
if len(parser.ids) != len(set(parser.ids)):
    fail("abordagens.html contém IDs duplicados")
missing_ids = sorted(REQUIRED_IDS.difference(parser.ids))
if missing_ids:
    fail(f"abordagens.html: IDs obrigatórios ausentes: {', '.join(missing_ids)}")
missing_tokens = sorted(token for token in REQUIRED_TOKENS if token not in html)
if missing_tokens:
    fail(f"abordagens.html: conteúdo obrigatório ausente: {', '.join(missing_tokens)}")
if parser.external_assets or parser.scripts:
    fail("abordagens.html deve permanecer estática e sem dependências externas ou scripts")
for stylesheet in ("assets/style.css", "assets/accessibility.css", "assets/approaches.css"):
    if stylesheet not in parser.styles:
        fail(f"abordagens.html não carrega {stylesheet}")
for reference in parser.local_refs:
    target = (ROOT / reference).resolve()
    if ROOT not in target.parents and target != ROOT:
        fail(f"referência fora do repositório: {reference}")
    if not target.exists():
        fail(f"referência local ausente: {reference}")

css = CSS_PATH.read_text(encoding="utf-8")
missing_css = sorted(token for token in REQUIRED_CSS if token not in css)
if missing_css:
    fail(f"assets/approaches.css incompleto: {', '.join(missing_css)}")

if HTML_PATH.stat().st_size > 22_000:
    fail("abordagens.html excede 22 KB")
if CSS_PATH.stat().st_size > 9_000:
    fail("assets/approaches.css excede 9 KB")

print("OK: página separada de alternativas validada; catálogo principal permanece desacoplado")
