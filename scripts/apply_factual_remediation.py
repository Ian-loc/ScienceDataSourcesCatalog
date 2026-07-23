#!/usr/bin/env python3
"""Aplica e valida correções factuais oficiais e uma escala tipográfica mais compacta."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORRECTIONS_PATH = ROOT / "data" / "factual_corrections_2026-07-23.json"
RESOURCE_PATH = ROOT / "data" / "data_resources.csv"
MARKER = "factual-remediation-compact-ui-2026-07-23"
NOTICE = (
    '<aside class="verification-notice wrap" role="note" aria-label="Estado da verificação factual">'
    '<strong>Transparência factual:</strong> as datas exibidas indicam a revisão do registro. '
    'Elas não certificam automaticamente todos os produtos mantidos pela fonte. '
    'Acesso, licença, versão e resolução devem ser confirmados no produto específico.'
    '</aside>'
)


def load_corrections() -> dict:
    return json.loads(CORRECTIONS_PATH.read_text(encoding="utf-8"))


def read_resources() -> tuple[list[str], list[dict[str, str]]]:
    with RESOURCE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_resources(fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with RESOURCE_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_resources(payload: dict) -> int:
    fieldnames, rows = read_resources()
    by_id = {row["resource_id"]: row for row in rows}
    changes = 0
    for item in payload["resources"]:
        resource_id = item["resource_id"]
        if resource_id not in by_id:
            raise SystemExit(f"ERRO: recurso inexistente: {resource_id}")
        row = by_id[resource_id]
        for field, value in item["fields"].items():
            if field not in fieldnames:
                raise SystemExit(f"ERRO: campo inexistente em {resource_id}: {field}")
            if row[field] != value:
                row[field] = value
                changes += 1
        if row["last_verified"] != payload["reviewed_at"]:
            row["last_verified"] = payload["reviewed_at"]
            changes += 1
    if changes:
        write_resources(fieldnames, rows)
    return changes


def replace_all(path: Path, replacements: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def apply_ui_and_docs() -> int:
    changes = 0
    style_path = ROOT / "assets" / "style.css"
    style = style_path.read_text(encoding="utf-8")
    if MARKER not in style:
        style += f'''\n\n/* {MARKER} */\nhtml{{font-size:15.5px}}\nh1{{font-size:clamp(2.15rem,5vw,4.05rem)}}\nh2{{font-size:clamp(1.55rem,3vw,2.25rem)}}\n.lead{{font-size:clamp(.96rem,1.5vw,1.12rem)}}\n.hero-grid{{padding:3.45rem 0}}\n.card h3{{font-size:1.12rem}}\n.verified-date{{font-size:.65rem}}\n.verification-notice{{margin-top:1rem;padding:.8rem 1rem;border:1px solid #d7c792;border-radius:10px;background:var(--amber);color:#5d4a14;font-size:.82rem}}\n.verification-notice strong{{color:#49390e}}\n@media(max-width:720px){{html{{font-size:15px}}.hero-grid{{padding:2.6rem 0}}}}\n'''
        style_path.write_text(style, encoding="utf-8")
        changes += 1

    replacements = {
        "Verificado em ": "Registro revisado em ",
        'detail("Última verificação",': 'detail("Registro revisado em",',
        "Verificação mais recente": "Revisão do registro mais recente",
    }
    for relative in ("assets/app.js", "assets/products.js", "index.html", "products.html"):
        if replace_all(ROOT / relative, replacements):
            changes += 1

    for page, main_id in (("index.html", "conteudo"), ("products.html", "produtos")):
        path = ROOT / page
        text = path.read_text(encoding="utf-8")
        if NOTICE not in text:
            marker = f'<main id="{main_id}">'
            if marker not in text:
                raise SystemExit(f"ERRO: marcador principal ausente em {page}")
            path.write_text(text.replace(marker, NOTICE + "\n" + marker, 1), encoding="utf-8")
            changes += 1

    if replace_all(ROOT / "CODEBOOK.md", {
        "| `last_verified` | Data efetiva da revisão, AAAA-MM-DD. |":
        "| `last_verified` | Data da revisão do registro, AAAA-MM-DD; não certifica integralmente todos os produtos ou campos da fonte. |"
    }):
        changes += 1

    about = ROOT / "about.html"
    about_text = about.read_text(encoding="utf-8")
    old = "A evidência acadêmica é representativa, não uma revisão sistemática completa das citações de cada infraestrutura."
    new = old + " A data exibida nos cards registra a revisão do registro; a confirmação factual é feita por afirmação e pode variar entre produtos e formas de acesso."
    if old in about_text and new not in about_text:
        about.write_text(about_text.replace(old, new, 1), encoding="utf-8")
        changes += 1

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    note = "> **Nota de verificação:** `last_verified` registra a revisão do registro. Não deve ser interpretado como certificação integral de todos os produtos, versões, licenças ou endpoints externos."
    if note not in readme_text:
        anchor = "O catálogo é uma camada de descoberta e triagem. Não hospeda os datasets externos nem substitui documentação, licença ou citação dos produtos originais."
        if anchor not in readme_text:
            raise SystemExit("ERRO: âncora do README não encontrada")
        readme.write_text(readme_text.replace(anchor, anchor + "\n\n" + note, 1), encoding="utf-8")
        changes += 1

    changelog = ROOT / "CHANGELOG.md"
    changelog_text = changelog.read_text(encoding="utf-8")
    heading = "## Não lançado — correções factuais e escala visual"
    if heading not in changelog_text:
        entry = (
            heading + "\n\n"
            "- corrigidos 11 registros com divergências confirmadas em autenticação, API, licença ou condições de acesso;\n"
            "- registradas as fontes oficiais em `data/factual_corrections_2026-07-23.json`;\n"
            "- redefinida a apresentação de `last_verified` como data de revisão do registro, não certificação integral;\n"
            "- adicionada advertência pública sobre variabilidade por produto e distribuição;\n"
            "- reduzida moderadamente a escala tipográfica e o tamanho máximo dos títulos;\n"
            "- preservados número de fontes, esquema 0.7.0 e bloqueio do DOI.\n\n"
        )
        changelog.write_text(changelog_text.replace("# Histórico de mudanças\n", "# Histórico de mudanças\n\n" + entry, 1), encoding="utf-8")
        changes += 1

    pages = ROOT / ".github" / "workflows" / "pages.yml"
    pages_text = pages.read_text(encoding="utf-8")
    command = "          python3 scripts/apply_factual_remediation.py --check\n"
    if command not in pages_text:
        target = "          python3 scripts/validate_product_catalog.py\n"
        if target not in pages_text:
            raise SystemExit("ERRO: ponto de inserção no workflow não encontrado")
        pages.write_text(pages_text.replace(target, target + command, 1), encoding="utf-8")
        changes += 1

    return changes


def check(payload: dict) -> None:
    _, rows = read_resources()
    by_id = {row["resource_id"]: row for row in rows}
    failures: list[str] = []
    for item in payload["resources"]:
        row = by_id.get(item["resource_id"])
        if row is None:
            failures.append(f"recurso ausente: {item['resource_id']}")
            continue
        for field, value in item["fields"].items():
            if row.get(field) != value:
                failures.append(f"{item['resource_id']}.{field} diverge")
        if row.get("last_verified") != payload["reviewed_at"]:
            failures.append(f"{item['resource_id']}.last_verified diverge")

    if MARKER not in (ROOT / "assets" / "style.css").read_text(encoding="utf-8"):
        failures.append("marcador de escala visual ausente")
    for page in ("index.html", "products.html"):
        if NOTICE not in (ROOT / page).read_text(encoding="utf-8"):
            failures.append(f"aviso factual ausente em {page}")
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in ("assets/app.js", "assets/products.js", "index.html", "products.html"))
    if "Verificado em " in combined or "Verificação mais recente" in combined:
        failures.append("linguagem de certificação integral ainda presente")
    if failures:
        raise SystemExit("ERRO: " + "; ".join(failures))
    print(f"OK: {len(payload['resources'])} fontes corrigidas, semântica de revisão e escala visual validadas")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = load_corrections()
    if args.check:
        check(payload)
        return
    resource_changes = apply_resources(payload)
    file_changes = apply_ui_and_docs()
    check(payload)
    print(f"OK: {resource_changes} valores factuais e {file_changes} arquivos de interface/documentação atualizados")


if __name__ == "__main__":
    main()
