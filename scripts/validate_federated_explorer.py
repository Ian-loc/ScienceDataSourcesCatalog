#!/usr/bin/env python3
"""Validate the public federated explorer and its governed layer registry."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "explorer.html"
REGISTRY_PATH = ROOT / "data" / "federated_layers.json"
JS_PATH = ROOT / "assets" / "explorer.js"
CSS_PATH = ROOT / "assets" / "explorer.css"
CANONICAL_PATH = ROOT / "data" / "data_resources.csv"
POLICY_PATH = ROOT / "docs" / "policies" / "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md"

ALLOWED_LAYER_TYPES = {"wms_raster", "raster_tiles"}
ALLOWED_CATALOG_STATUS = {"cataloged", "external_product_pending_registration"}
REQUIRED_LAYER_FIELDS = {
    "layer_id", "title", "short_title", "provider", "product", "catalog_status",
    "catalog_note", "resource_id", "layer_type", "default_visible", "default_opacity",
    "min_zoom", "max_zoom", "tile_size", "tiles", "period", "version",
    "spatial_resolution", "license", "operation_scope", "compatibility_class",
    "compatibility_label", "inference_ceiling", "analytical_use_allowed",
    "evidence_status", "scientific_warning", "official_source_url", "product_url",
    "data_access_url", "methodology_url", "metadata_url", "citation_text",
    "attribution", "legend",
}
REQUIRED_HTML_IDS = {
    "explorador", "scientific-notice", "share-view", "download-manifest", "reset-view",
    "layers-heading", "visible-count", "layer-list", "layer-empty", "map-heading", "map",
    "map-status", "visible-attribution", "inspection-heading", "inspection-content",
    "compatibility-summary", "mvp-heading", "direction-heading",
}
EXTERNAL_ASSETS = {
    "https://unpkg.com/maplibre-gl@5.12.0/dist/maplibre-gl.css",
    "https://unpkg.com/maplibre-gl@5.12.0/dist/maplibre-gl.js",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def is_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


class ExplorerParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.external_assets: set[str] = set()
        self.scripts: list[str] = []
        self.styles: list[str] = []
        self.tags: list[str] = []
        self.lang = ""
        self.viewport = False
        self.skip = False

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
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"] or "")
        if tag == "link" and values.get("rel") == "stylesheet" and values.get("href"):
            self.styles.append(values["href"] or "")
        reference = values.get("src") if tag == "script" else values.get("href") if tag == "link" else None
        if reference and is_https(reference):
            self.external_assets.add(reference)


for path in (HTML_PATH, REGISTRY_PATH, JS_PATH, CSS_PATH, CANONICAL_PATH, POLICY_PATH):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"artefato ausente ou vazio: {path.relative_to(ROOT)}")

canonical_ids = set()
with CANONICAL_PATH.open(encoding="utf-8-sig") as handle:
    header = handle.readline().rstrip("\n").split(",")
    resource_id_index = header.index("resource_id")
    for line in handle:
        if not line.strip():
            continue
        canonical_ids.add(line.split(",", resource_id_index + 1)[resource_id_index])

registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
if registry.get("operation_mode") != "visual_composition_only":
    fail("o MVP deve permanecer em visual_composition_only")
if registry.get("registry_version") != "0.2.0":
    fail("registro governado deve usar versão 0.2.0")
if registry.get("inference_ceiling") != "N0":
    fail("o MVP deve declarar teto de inferência N0")
if registry.get("analytical_use_allowed") is not False:
    fail("o MVP deve proibir uso analítico")
if registry.get("evidence_status") != "not_assessed":
    fail("o MVP deve declarar evidência not_assessed")
policy = registry.get("scientific_policy", {})
if policy.get("document_path") != "docs/policies/SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md":
    fail("registro deve referenciar a política científica")
if policy.get("comparability_model") != "A-E" or policy.get("inference_model") != "N0-N5":
    fail("registro deve declarar modelos A-E e N0-N5")
if not is_https(registry.get("base_map", {}).get("style_url", "")):
    fail("mapa-base deve usar URL HTTPS")
if not registry.get("disclaimer"):
    fail("registro deve declarar limite científico")

layers = registry.get("layers", [])
if len(layers) < 2:
    fail("explorador federado exige ao menos duas camadas científicas")
ids = [layer.get("layer_id") for layer in layers]
if len(ids) != len(set(ids)):
    fail("layer_id duplicado")
providers = {layer.get("provider") for layer in layers}
if len(providers) < 2:
    fail("MVP deve demonstrar federação entre ao menos dois provedores")

for index, layer in enumerate(layers, start=1):
    missing = sorted(REQUIRED_LAYER_FIELDS.difference(layer))
    if missing:
        fail(f"camada {index}: campos ausentes: {', '.join(missing)}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]+", layer["layer_id"]):
        fail(f"camada {index}: layer_id inválido")
    if layer["catalog_status"] not in ALLOWED_CATALOG_STATUS:
        fail(f"camada {index}: catalog_status inválido")
    if not layer["catalog_note"].strip():
        fail(f"camada {index}: catalog_note obrigatório")
    resource_id = layer["resource_id"]
    if layer["catalog_status"] == "cataloged":
        if not isinstance(resource_id, str) or not re.fullmatch(r"DR\d{4}", resource_id):
            fail(f"camada {index}: camada catalogada exige resource_id válido")
        if resource_id not in canonical_ids:
            fail(f"camada {index}: resource_id não encontrado no CSV canônico")
    elif resource_id is not None:
        fail(f"camada {index}: produto externo pendente deve usar resource_id nulo")
    if layer["layer_type"] not in ALLOWED_LAYER_TYPES:
        fail(f"camada {index}: layer_type não permitido")
    if not isinstance(layer["default_visible"], bool):
        fail(f"camada {index}: default_visible deve ser booleano")
    if not 0 <= float(layer["default_opacity"]) <= 1:
        fail(f"camada {index}: opacidade fora do intervalo 0–1")
    if layer["min_zoom"] > layer["max_zoom"]:
        fail(f"camada {index}: intervalo de zoom invertido")
    if not layer["tiles"]:
        fail(f"camada {index}: tiles ausentes")
    for tile in layer["tiles"]:
        if not is_https(tile):
            fail(f"camada {index}: tile deve usar HTTPS")
        if layer["layer_type"] == "wms_raster" and "{bbox-epsg-3857}" not in tile:
            fail(f"camada {index}: WMS deve declarar bbox-epsg-3857")
        if layer["layer_type"] == "raster_tiles" and not all(token in tile for token in ("{z}", "{x}", "{y}")):
            fail(f"camada {index}: mosaico deve declarar z/x/y")
    for field in (
        "official_source_url", "product_url", "data_access_url", "methodology_url", "metadata_url"
    ):
        if not is_https(layer[field]):
            fail(f"camada {index}: {field} deve usar HTTPS")
    if layer["operation_scope"] != ["visual_overlay"]:
        fail(f"camada {index}: escopo atual deve ser somente visual_overlay")
    if layer["compatibility_class"] != "C":
        fail(f"camada {index}: MVP deve permanecer em compatibilidade C")
    if layer["inference_ceiling"] != "N0":
        fail(f"camada {index}: teto deve ser N0")
    if layer["analytical_use_allowed"] is not False:
        fail(f"camada {index}: uso analítico deve estar bloqueado")
    if layer["evidence_status"] != "not_assessed":
        fail(f"camada {index}: evidência deve permanecer not_assessed")
    if not layer["scientific_warning"].strip() or not layer["citation_text"].strip():
        fail(f"camada {index}: aviso científico e citação são obrigatórios")

parser = ExplorerParser()
html = HTML_PATH.read_text(encoding="utf-8")
parser.feed(html)
if parser.lang != "pt-BR" or not parser.viewport or not parser.skip:
    fail("explorer.html perdeu requisitos básicos de acessibilidade")
if parser.tags.count("main") != 1 or parser.tags.count("h1") != 1 or "noscript" not in parser.tags:
    fail("explorer.html deve conter um main, um h1 e fallback noscript")
missing_ids = sorted(REQUIRED_HTML_IDS.difference(parser.ids))
if missing_ids:
    fail(f"explorer.html: IDs obrigatórios ausentes: {', '.join(missing_ids)}")
if len(parser.ids) != len(set(parser.ids)):
    fail("explorer.html contém IDs duplicados")
if parser.external_assets != EXTERNAL_ASSETS:
    fail("dependências externas do explorador divergem da lista fixada")
for required in ("assets/style.css", "assets/accessibility.css", "assets/explorer.css"):
    if required not in parser.styles:
        fail(f"explorer.html não carrega {required}")
if "assets/explorer.js" not in parser.scripts:
    fail("explorer.html não carrega assets/explorer.js")
for token in (
    "Simbioscópio", "N0 — composição visual",
    "SCIENTIFIC_COMPARABILITY_AND_INFERENCE_POLICY.md",
    "nenhuma inferência estatística ou causal",
):
    if token not in html:
        fail(f"explorer.html perdeu controle científico: {token}")

js = JS_PATH.read_text(encoding="utf-8")
required_js = {
    "data/federated_layers.json", "visual_overlay", "analytical_harmonization_performed: false",
    "inference_ceiling", "analytical_use_allowed", "evidence_status", "scientific_policy",
    "history.replaceState", "navigator.clipboard", "downloadManifest", "scientific_warning",
    "official_source_url", "product_url", "data_access_url", "methodology_url",
    "metadata_url", "raster-opacity", "setLayoutProperty", "moveLayer", "maplibregl.Popup",
}
missing_js = sorted(token for token in required_js if token not in js)
if missing_js:
    fail(f"assets/explorer.js incompleto: {', '.join(missing_js)}")

css = CSS_PATH.read_text(encoding="utf-8")
required_css = {
    ".explorer-shell", ".layer-card", ".map-panel #map", ".compatibility-summary",
    ".map-attribution-panel", "@media(max-width:980px)", "prefers-reduced-motion",
}
missing_css = sorted(token for token in required_css if token not in css)
if missing_css:
    fail(f"assets/explorer.css incompleto: {', '.join(missing_css)}")

limits = {
    HTML_PATH: 18_000,
    JS_PATH: 40_000,
    CSS_PATH: 16_000,
    REGISTRY_PATH: 18_000,
}
for path, limit in limits.items():
    if path.stat().st_size > limit:
        fail(f"{path.relative_to(ROOT)} excede o orçamento de {limit} bytes")

cataloged = sum(1 for layer in layers if layer["catalog_status"] == "cataloged")
external = len(layers) - cataloged
print(
    "OK: Simbioscópio federado validado — "
    f"{len(layers)} camadas, {len(providers)} provedores, {cataloged} catalogada(s), "
    f"{external} externa(s), composição visual C, teto N0 e proveniência exportável"
)
