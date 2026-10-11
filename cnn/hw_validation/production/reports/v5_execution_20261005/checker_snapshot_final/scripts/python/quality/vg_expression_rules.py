"""Project-local relational-width fix over the installed VG expression rules."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

from . import vg_value_facts
from .vg_rule_models import VgEvaluation, VgFinding, failed, inconclusive, passed
from .vg_semantic_facts import VgFacts, iter_trusted_modules


def _load_upstream_module():
    """Load the installed implementation so every unaffected gate stays upstream."""

    path_current = Path(__file__).resolve()
    package = sys.modules[__package__]
    for path_entry in package.__path__:
        path_candidate = (Path(path_entry) / path_current.name).resolve()
        if path_candidate == path_current or not path_candidate.is_file():
            continue
        str_name = f"{__package__}._installed_vg_expression_rules"
        spec = importlib.util.spec_from_file_location(str_name, path_candidate)
        if spec is None or spec.loader is None:
            break
        module = importlib.util.module_from_spec(spec)
        sys.modules[str_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError("installed vg_expression_rules.py was not found")


_upstream = _load_upstream_module()
SIZED_LITERAL = _upstream.SIZED_LITERAL


def evaluate_expression_gate(str_gate_id: str, facts: VgFacts) -> VgEvaluation:
    """Use the local slice-aware VG085 implementation and delegate all other gates."""

    if str_gate_id == "VG085":
        return _relational_width(facts)
    return _upstream.evaluate_expression_gate(str_gate_id, facts)


def _relational_width(facts: VgFacts) -> VgEvaluation:
    """Compare widths of trusted simple relational operands, including fixed selects."""

    bool_applicable = False
    bool_unknown = False
    list_findings: list[VgFinding] = []
    str_identifier = r"[A-Za-z_]\w*"
    str_select = rf"{str_identifier}\s*\[\s*[^\[\]]+?\s*\]"
    str_plain_identifier = rf"{str_identifier}(?!\s*\[)"
    str_operand = rf"(?:{SIZED_LITERAL}|{str_select}|{str_plain_identifier})"
    str_pattern = rf"(?<!['\w])({str_operand})\s*(==|!=|<|>)\s*({str_operand})"

    for source_facts, dict_module, str_module_text, int_base_line in iter_trusted_modules(facts):
        dict_widths = vg_value_facts.module_widths(dict_module)
        dict_parameter_values = vg_value_facts.module_instance_parameter_values(dict_module)
        for obj_match in re.finditer(str_pattern, str_module_text):
            bool_applicable = True
            str_left = obj_match.group(1)
            str_right = obj_match.group(3)
            int_left_width = _expression_width(str_left, dict_widths, dict_parameter_values)
            int_right_width = _expression_width(str_right, dict_widths, dict_parameter_values)
            if int_left_width is None or int_right_width is None:
                bool_unknown = True
                continue
            if int_left_width == int_right_width:
                continue
            int_line = int_base_line + str_module_text.count("\n", 0, obj_match.start())
            list_findings.append(
                VgFinding(
                    source_facts.relative_path,
                    int_line,
                    "表达式两侧位宽不一致。",
                    obj_match.group(0).strip(),
                )
            )

    if list_findings:
        return failed(*list_findings)
    if bool_unknown:
        return inconclusive("存在无法静态确定的表达式位宽。")
    return passed(applicable=bool_applicable)


def _expression_width(
    str_expression: str,
    dict_widths: dict[str, int | None],
    dict_parameter_values: dict[str, int],
) -> int | None:
    """Reuse shared width facts, adding parameter-resolved fixed part-select bounds."""

    int_width = vg_value_facts.expression_width(str_expression, dict_widths)
    if int_width is not None:
        return int_width
    obj_select = re.fullmatch(r"[A-Za-z_]\w*\s*(\[[^\[\]]+\])", str_expression.strip())
    if obj_select is None or ":" not in obj_select.group(1):
        return None
    return vg_value_facts.parse_width(obj_select.group(1), dict_parameter_values)
