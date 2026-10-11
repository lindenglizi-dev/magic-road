"""仅修正 VG136 对 formatter 已确认 for 归纳更新的反馈误判。"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys

import scripts.python.quality as quality_package

from .vg_rule_models import VgEvaluation, VgFinding, failed, passed
from .vg_semantic_facts import VgFacts, iter_trusted_modules


def _load_upstream():
    """从 namespace package 中加载被本 overlay 遮蔽的原规则模块。"""

    current = Path(__file__).resolve()
    source = next(
        candidate
        for directory in quality_package.__path__
        if (candidate := (Path(directory) / current.name).resolve()) != current
        and candidate.is_file()
    )
    name = "scripts.python.quality._vg_structure_rules_upstream"
    spec = importlib.util.spec_from_file_location(name, source)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load upstream structure rules: {source}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_UPSTREAM = _load_upstream()


def _base_refs(str_expression: str) -> set[str]:
    """把 formatter 表达式引用归一到 module 局部信号基名。"""

    return {
        reference.split("[", 1)[0].split(".", 1)[0]
        for reference in _UPSTREAM._expression_signal_refs(str_expression, set())
    }


def evaluate_structure_gate(str_gate_id: str, facts: VgFacts) -> VgEvaluation:
    """只接管 VG136；其余编号原样委托已安装规则。"""

    if str_gate_id != "VG136":
        return _UPSTREAM.evaluate_structure_gate(str_gate_id, facts)
    return _comb_no_feedback(facts)


def _assignment(str_text: str) -> tuple[str, str] | None:
    """读取 formatter loop header 中的一条简单阻塞赋值。"""

    match = re.fullmatch(
        r"\s*(?:integer\s+)?([A-Za-z_]\w*)\s*=\s*(.+?)\s*",
        str_text,
        flags=re.DOTALL,
    )
    return (match.group(1), match.group(2)) if match else None


def _loop_contract(dict_node: dict[str, object]) -> tuple[str, bool] | None:
    """返回 formatter loop 的归纳变量及其是否为静态规范更新。"""

    if str(dict_node.get("kind") or "") != "loop":
        return None
    header = str(dict_node.get("header") or "")
    match = re.fullmatch(r"\s*for\s*\((.*)\)\s*", header, flags=re.DOTALL)
    if not match:
        return None
    clauses = match.group(1).split(";")
    if len(clauses) != 3:
        return None
    initial = _assignment(clauses[0])
    update = _assignment(clauses[2])
    if initial is None or update is None or initial[0] != update[0]:
        return None
    variable = initial[0]
    initial_match = re.fullmatch(r"\s*([+-]?\d+)\s*", initial[1])
    condition_match = re.fullmatch(
        rf"\s*{re.escape(variable)}\s*(<|<=|>|>=)\s*([+-]?\d+)\s*",
        clauses[1],
    )
    update_match = re.fullmatch(
        rf"\s*{re.escape(variable)}\s*([+-])\s*(\d+)\s*",
        update[1],
    )
    canonical = False
    if initial_match and condition_match and update_match:
        initial_value = int(initial_match.group(1))
        comparison = condition_match.group(1)
        bound = int(condition_match.group(2))
        step = int(update_match.group(2))
        direction = update_match.group(1)
        if -(2**31) <= initial_value <= 2**31 - 1 and -(2**31) <= bound <= 2**31 - 1 and step > 0:
            if direction == "+" and comparison in {"<", "<="} and initial_value <= bound:
                iterations = ((bound - initial_value - (1 if comparison == "<" else 0)) // step) + 1
                canonical = initial_value + iterations * step <= 2**31 - 1
            elif direction == "-" and comparison in {">", ">="} and initial_value >= bound:
                iterations = ((initial_value - bound - (1 if comparison == ">" else 0)) // step) + 1
                canonical = initial_value - iterations * step >= -(2**31)
    return variable, canonical


def _statement_target(str_text: str) -> str | None:
    """返回 formatter statement 的简单赋值左值基名。"""

    match = re.match(
        r"\s*([A-Za-z_]\w*)(?:\s*\[[^]]+\])?\s*(?<!<)=",
        str_text,
        flags=re.DOTALL,
    )
    return match.group(1) if match else None


def _safe_induction_variables(dict_module: dict[str, object]) -> set[str]:
    """找出仅在自身静态 for 范围内使用、且未在 body 赋值的归纳变量。"""

    loops: dict[int, tuple[str, bool]] = {}

    def collect(nodes: list[dict[str, object]]) -> None:
        for node in nodes:
            contract = _loop_contract(node)
            if contract is not None:
                loops[id(node)] = contract
            collect(node.get("children", []))
            collect(node.get("alternate", []))
            for item in node.get("items", []):
                collect(item.get("children", []))

    for always in dict_module.get("always", []):
        if str(always.get("trigger_kind") or "") == "comb":
            collect(always.get("nodes", []))

    candidates = {variable for variable, _ in loops.values()}
    integers = {
        str(declaration.get("name") or "")
        for declaration in dict_module.get("decls", [])
        if str(declaration.get("kind") or "") == "integer"
    }
    unsafe = {
        variable
        for variable in candidates
        if any(other == variable and not canonical for other, canonical in loops.values())
    } | (candidates - integers)

    def inspect(nodes: list[dict[str, object]], active: frozenset[str]) -> None:
        for node in nodes:
            contract = loops.get(id(node))
            own = contract[0] if contract is not None else None
            protected = active | ({own} if own else set())
            text = str(node.get("text") or "")
            header = str(node.get("header") or "")
            refs = _base_refs(text or header)
            unsafe.update((refs & candidates) - protected)
            target = _statement_target(text) if str(node.get("kind") or "") == "statement" else None
            if target in candidates:
                unsafe.add(target)
            child_active = frozenset(protected)
            inspect(node.get("children", []), child_active)
            inspect(node.get("alternate", []), child_active)
            for item in node.get("items", []):
                inspect(item.get("children", []), child_active)

    for always in dict_module.get("always", []):
        unsafe.update(
            {
                str(target).split("[", 1)[0]
                for target in always.get("targets", [])
            }
            & candidates
        )
        inspect(always.get("nodes", []), frozenset())

    for assign in dict_module.get("assigns", []):
        refs = _base_refs(
            f"{assign.get('lhs') or ''} {assign.get('rhs') or ''}",
        )
        unsafe.update(refs & candidates)

    for instance in dict_module.get("instances", []):
        for association in instance.get("port_associations", []):
            actual = association.get("actual") or {}
            unsafe.update(_base_refs(str(actual.get("text") or "")) & candidates)

    return candidates - unsafe


def _comb_no_feedback(facts: VgFacts) -> VgEvaluation:
    """保留原 VG136 图，仅删除已由 formatter 证明安全的 for 更新自边。"""

    findings: list[VgFinding] = []
    applicable = False
    for source_facts, dict_module, module_text, base_line in iter_trusted_modules(facts):
        dependencies = _UPSTREAM._dependency_graph(module_text)
        for variable in _safe_induction_variables(dict_module):
            if variable not in dependencies:
                continue
            dependencies[variable].discard(variable)
            if not dependencies[variable]:
                del dependencies[variable]
        applicable = applicable or bool(dependencies)
        feedback = _UPSTREAM._cycle_nodes(dependencies)
        if not feedback:
            continue
        target = sorted(feedback)[0]
        findings.append(
            _UPSTREAM._finding(
                source_facts,
                module_text,
                base_line,
                target,
                "组合逻辑依赖图中存在反馈环。",
                ", ".join(sorted(feedback)),
            )
        )
    return failed(*findings) if findings else passed(applicable=applicable)


def __getattr__(name: str):
    """保持私有诊断辅助函数对既有调用方可见。"""

    return getattr(_UPSTREAM, name)
