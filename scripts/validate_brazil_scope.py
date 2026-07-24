#!/usr/bin/env python3
"""Valida a camada curatorial de prioridade territorial do catálogo."""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "data_resources.csv"
REGISTRY = ROOT / "data" / "brazil_scope_priorities.json"

EXPECTED_TIER_ORDER = ["P0", "P1", "P2", "P3"]
EXPECTED = {
    "P0": {
        "source_origin": "brasileira",
        "brazil_scope_class": "fonte_brasileira",
        "inclusion_role": "núcleo",
    },
    "P1": {
        "source_origin": "internacional",
        "brazil_scope_class": "cobertura_brasil_sistematica",
        "inclusion_role": "complementar",
    },
    "P2": {
        "source_origin": "internacional",
        "brazil_scope_class": "cobertura_brasil_parcial",
        "inclusion_role": "contextual",
    },
    "P3": {
        "source_origin": "internacional",
        "brazil_scope_class": "referencia_sem_cobertura_brasil",
        "inclusion_role": "comparativa",
    },
}
REQUIRED_RULES = {
    "fontes_brasileiras_recebem_prioridade_maxima",
    "fontes_internacionais_exigem_cobertura_brasileira_demonstrável_ou_justificativa_estratégica",
    "ausência_de_cobertura_brasileira_não_autoriza_exclusão_automática",
    "prioridade_de_escopo_não_certifica_qualidade_científica_do_produto",
    "classificação_é_curatorial_e_não_deve_ser_inferida_apenas_pelo_domínio_da_url",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


if not REGISTRY.exists():
    fail("registro de prioridade Brasil ausente")

header, rows = read_csv(CANONICAL)
if len(header) != 34 or len(rows) != 51:
    fail("CSV canônico deve permanecer em 51 fontes × 34 campos")
canonical = {row["resource_id"].strip(): row for row in rows}
if len(canonical) != 51:
    fail("resource_id duplicado no CSV canônico")

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
if registry.get("registry_version") != "1.0.0":
    fail("registry_version inesperada")
if registry.get("tier_order") != EXPECTED_TIER_ORDER:
    fail("tier_order deve ser P0, P1, P2, P3")
if set(registry.get("rules", [])) != REQUIRED_RULES:
    fail("regras da política Brasil estão incompletas ou divergentes")
if not registry.get("scope_statement", "").strip():
    fail("scope_statement obrigatório")
try:
    reviewed_at = date.fromisoformat(registry.get("reviewed_at", ""))
except ValueError:
    fail("reviewed_at deve usar YYYY-MM-DD")
if reviewed_at > date.today():
    fail("reviewed_at não pode estar no futuro")

tiers = registry.get("tiers", [])
if [item.get("priority_tier") for item in tiers] != EXPECTED_TIER_ORDER:
    fail("tiers devem seguir a ordem P0–P3")

seen: set[str] = set()
counts: Counter[str] = Counter()
for tier in tiers:
    priority = tier.get("priority_tier")
    expected = EXPECTED[priority]
    for field, value in expected.items():
        if tier.get(field) != value:
            fail(f"{priority}: {field} deve ser {value}")
    for field in ("display_label", "description"):
        if not tier.get(field, "").strip():
            fail(f"{priority}: {field} obrigatório")
    resource_ids = tier.get("resource_ids", [])
    if not resource_ids or len(resource_ids) != len(set(resource_ids)):
        fail(f"{priority}: resource_ids vazio ou duplicado")
    for resource_id in resource_ids:
        if resource_id not in canonical:
            fail(f"{priority}: ID ausente no CSV canônico: {resource_id}")
        if resource_id in seen:
            fail(f"ID repetido entre prioridades: {resource_id}")
        seen.add(resource_id)
        counts[priority] += 1

        covers = canonical[resource_id]["covers_brazil"].strip()
        if priority in {"P0", "P1"} and covers != "sim":
            fail(f"{resource_id}: {priority} exige covers_brazil=sim")
        if priority == "P2" and covers not in {"sim", "parcial"}:
            fail(f"{resource_id}: P2 exige covers_brazil sim ou parcial")
        if priority == "P3" and covers != "não":
            fail(f"{resource_id}: P3 exige covers_brazil=não")

if seen != set(canonical):
    missing = sorted(set(canonical) - seen)
    extra = sorted(seen - set(canonical))
    fail(f"cobertura do registro diverge do CSV; faltantes={missing}; extras={extra}")
if counts["P0"] < counts["P3"]:
    fail("fontes brasileiras não podem ser menos numerosas que referências sem Brasil")

print(
    "OK: prioridade Brasil validada — "
    + ", ".join(f"{tier}={counts[tier]}" for tier in EXPECTED_TIER_ORDER)
    + "; 51 IDs cobertos; CSV 51 × 34 preservado"
)
