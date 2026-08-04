#!/usr/bin/env python3
"""Validate the first comparability golden cases without executing analysis."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "comparability_golden_cases.json"
VARIABLES_PATH = ROOT / "data" / "scientific_variables.csv"
SCHEMA_PATH = ROOT / "schema" / "comparability-assessment-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


for path in (CASES_PATH, VARIABLES_PATH, SCHEMA_PATH):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")

with VARIABLES_PATH.open(encoding="utf-8-sig", newline="") as handle:
    variables = list(csv.DictReader(handle))
variable_ids = {row["variable_id"] for row in variables}
product_by_variable = {row["variable_id"]: row["product_id"] for row in variables}

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
properties = schema["properties"]
required = set(schema["required"])
allowed = set(properties)
operation_enum = set(properties["operation_type"]["enum"])
class_enum = set(properties["compatibility_class"]["enum"])
inference_enum = set(properties["inference_ceiling"]["enum"])
review_enum = set(properties["review"]["properties"]["status"]["enum"])
diagnostic_enum = set(properties["diagnostics_required"]["items"]["enum"])
dimension_names = set(properties["dimensions"]["required"])
dimension_status_enum = set(schema["$defs"]["dimensionAssessment"]["properties"]["status"]["enum"])

cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
if not isinstance(cases, list) or len(cases) < 4:
    fail("o piloto exige ao menos quatro casos dourados")

seen_ids: set[str] = set()
classes_seen: set[str] = set()
operations_seen: set[str] = set()
for index, case in enumerate(cases, start=1):
    if not isinstance(case, dict):
        fail(f"caso {index}: objeto JSON inválido")
    missing = sorted(required - set(case))
    extra = sorted(set(case) - allowed)
    if missing:
        fail(f"caso {index}: campos obrigatórios ausentes: {', '.join(missing)}")
    if extra:
        fail(f"caso {index}: campos não permitidos: {', '.join(extra)}")

    assessment_id = case["assessment_id"]
    if not re.fullmatch(r"CA\d{6}", assessment_id):
        fail(f"caso {index}: assessment_id inválido")
    if assessment_id in seen_ids:
        fail(f"caso duplicado: {assessment_id}")
    seen_ids.add(assessment_id)

    operation = case["operation_type"]
    compatibility_class = case["compatibility_class"]
    inference_ceiling = case["inference_ceiling"]
    if operation not in operation_enum:
        fail(f"{assessment_id}: operation_type inválido")
    if compatibility_class not in class_enum:
        fail(f"{assessment_id}: compatibility_class inválida")
    if inference_ceiling not in inference_enum:
        fail(f"{assessment_id}: inference_ceiling inválido")
    operations_seen.add(operation)
    classes_seen.add(compatibility_class)

    inputs = case["input_variable_ids"]
    if not isinstance(inputs, list) or len(inputs) < 2 or len(inputs) != len(set(inputs)):
        fail(f"{assessment_id}: input_variable_ids inválido")
    unknown_inputs = sorted(set(inputs) - variable_ids)
    if unknown_inputs:
        fail(f"{assessment_id}: variáveis desconhecidas: {', '.join(unknown_inputs)}")

    dimensions = case["dimensions"]
    if set(dimensions) != dimension_names:
        fail(f"{assessment_id}: dimensões incompletas ou adicionais")
    for dimension_name, assessment in dimensions.items():
        if assessment.get("status") not in dimension_status_enum:
            fail(f"{assessment_id}: status inválido em {dimension_name}")
        if len(str(assessment.get("rationale", "")).strip()) < 5:
            fail(f"{assessment_id}: justificativa insuficiente em {dimension_name}")

    diagnostics = case.get("diagnostics_required", [])
    if not set(diagnostics).issubset(diagnostic_enum):
        fail(f"{assessment_id}: diagnóstico fora do vocabulário")
    if not case["warnings"]:
        fail(f"{assessment_id}: avisos obrigatórios ausentes")

    review = case["review"]
    if review.get("status") not in review_enum:
        fail(f"{assessment_id}: status de revisão inválido")

    if compatibility_class in {"D", "E"} and case["analytical_use_allowed"]:
        fail(f"{assessment_id}: classes D/E não podem liberar uso analítico")
    if operation == "visual_overlay":
        if compatibility_class != "C" or inference_ceiling != "N0" or case["analytical_use_allowed"]:
            fail(f"{assessment_id}: composição visual do MVP deve permanecer C/N0/não analítica")
    if inference_ceiling == "N5" and review.get("status") != "approved":
        fail(f"{assessment_id}: N5 exige aprovação humana explícita")

    shared_products = {product_by_variable[variable_id] for variable_id in inputs}
    if len(shared_products) == 1 and operation in {"correlation", "regression"}:
        if "shared_lineage" not in diagnostics:
            fail(f"{assessment_id}: análise entre saídas do mesmo produto exige diagnóstico de linhagem")

expected_classes = {"B", "C", "D", "E"}
if not expected_classes.issubset(classes_seen):
    fail(f"casos dourados não cobrem classes: {', '.join(sorted(expected_classes - classes_seen))}")
expected_operations = {"side_by_side_description", "correlation", "visual_overlay", "spatial_join"}
if not expected_operations.issubset(operations_seen):
    fail(f"casos dourados não cobrem operações: {', '.join(sorted(expected_operations - operations_seen))}")

case_index = {case["assessment_id"]: case for case in cases}
if case_index["CA000002"]["compatibility_class"] != "D":
    fail("CA000002 deve permanecer bloqueio D por dependência matemática")
if case_index["CA000004"]["compatibility_class"] != "E":
    fail("CA000004 deve permanecer E até fixar edição e suporte PRODES")

print(
    "OK: casos dourados de comparabilidade validados — "
    f"{len(cases)} casos, classes {','.join(sorted(classes_seen))} e nenhuma análise executada"
)
