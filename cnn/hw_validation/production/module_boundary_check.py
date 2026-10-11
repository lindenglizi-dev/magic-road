"""Diagnose VG153 instance-output false positives without changing the gate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
RTL_ROOT = ROOT / "round_internal_probe" / "rtl"
EXPECTED_MODULES = {
    "road_round_internal_probe",
    "road_round_internal_probe_core",
    "road_round_reset_gen",
    "road_round_shift",
}

codex_root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
skill_root = codex_root / "skills" / "readable-verilog-generator"
if str(skill_root) not in sys.path:
    sys.path.insert(0, str(skill_root))

from scripts.python.quality.formatter_ast import create_formatter_backend  # noqa: E402
from scripts.python.quality.formatter_backend.banners import (  # noqa: E402
    extract_banner_title,
    is_banner_line,
)
from scripts.python.quality.vg_contract_liveness import (  # noqa: E402
    _module_signal_facts,
    evaluate_liveness_gate,
)
from scripts.python.quality.vg_semantic_facts import build_vg_facts  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_sha256(source) -> str | None:
    path = getattr(source, "path", None)
    return sha256(path) if isinstance(path, Path) and path.is_file() else None


def static_width(item: dict) -> int | None:
    """Return a numeric packed width; reject parameters and unpacked arrays."""
    if str(item.get("unpacked") or "").strip():
        return None
    text = re.sub(r"\s+", "", str(item.get("width") or ""))
    if not text:
        return 1
    match = re.fullmatch(r"\[(\d+):(\d+)\]", text)
    return abs(int(match.group(1)) - int(match.group(2))) + 1 if match else None


def exact_region_order(lines: tuple[str, ...], backend) -> dict:
    """Check exact configured titles; substring matches are deliberately absent."""
    order = list(backend.config["structure"]["region_order"])
    title_to_rank = {backend.REGION_LABELS[key]: index for index, key in enumerate(order)}
    titles = [
        extract_banner_title(line)
        for line in lines
        if is_banner_line(line) and extract_banner_title(line) in title_to_rank
    ]
    ranks = [title_to_rank[title] for title in titles]
    return {
        "passed": ranks == sorted(ranks),
        "titles": titles,
        "configured_keys": order,
    }


def module_catalog(facts) -> dict[str, dict]:
    catalog = {}
    for source in facts.sources:
        for module in source.report.get("modules", []):
            name = str(module.get("name") or "")
            if not name or name in catalog:
                raise ValueError(f"duplicate or empty module definition: {name!r}")
            catalog[name] = {"module": module, "source": source}
    if set(catalog) != EXPECTED_MODULES:
        raise ValueError(f"expected exactly four probe modules, got {sorted(catalog)}")
    return catalog


def bare_actual(actual: dict, signal: str) -> bool:
    expression = actual.get("expression") or {}
    return (
        actual.get("kind") == "expression"
        and str(actual.get("text") or "").strip() == signal
        and list(actual.get("references") or []) == [signal]
        and expression.get("node_kind") == "identifier"
        and str(expression.get("name") or expression.get("text") or "") == signal
        and list(actual.get("static_lvalue_segments") or []) == [{"name": signal}]
    )


def resolve_driver(catalog: dict[str, dict], parent_name: str, signal: str) -> dict:
    """Prove exactly one known, static child output drives a parent wire."""
    parent_entry = catalog[parent_name]
    parent = parent_entry["module"]
    declarations = _module_signal_facts(parent, parent_entry["source"].lines)["declarations"]
    declaration = declarations.get(signal)
    if declaration is None or declaration["object"].get("kind") != "wire":
        return {"status": "unresolved", "reasons": ["parent_actual_not_plain_wire"]}
    if parent.get("generates"):
        return {"status": "unresolved", "reasons": ["parent_contains_generate"]}

    drivers = []
    blockers = []
    for instance in parent.get("instances", []) or []:
        for association in instance.get("port_associations", []) or []:
            actual = association.get("actual") or {}
            if signal not in set(actual.get("references") or []):
                continue
            child_name = str(instance.get("module_name") or "")
            child_entry = catalog.get(child_name)
            if child_entry is None:
                blockers.append("unknown_child")
                continue
            child = child_entry["module"]
            if child.get("generates"):
                blockers.append("child_contains_generate")
                continue
            formal = str(association.get("formal_name") or "")
            ports = [port for port in child.get("ports", []) or [] if port.get("name") == formal]
            if len(ports) != 1:
                blockers.append("unknown_formal_or_direction")
                continue
            direction = str(ports[0].get("direction") or "")
            if direction == "input":
                continue
            if direction != "output":
                blockers.append("inout_or_unknown_direction")
                continue
            if (
                not instance.get("parse_complete")
                or instance.get("has_params")
                or instance.get("parameter_overrides")
                or str(instance.get("array_range_text") or "")
                or instance.get("association_style") != "named"
            ):
                blockers.append("parameterized_array_or_incomplete_instance")
                continue
            if not bare_actual(actual, signal):
                blockers.append("non_bare_output_actual")
                continue
            parent_width = static_width(declaration["object"])
            child_width = static_width(ports[0])
            if parent_width is None or child_width is None or parent_width != child_width:
                blockers.append("unknown_or_mismatched_width")
                continue
            if bool(declaration["object"].get("signed")) != bool(ports[0].get("signed")):
                blockers.append("signedness_mismatch")
                continue
            drivers.append({
                "parent_module": parent_name,
                "parent_signal": signal,
                "parent_source": parent_entry["source"].relative_path,
                "parent_line": declaration["line"],
                "child_module": child_name,
                "child_source": child_entry["source"].relative_path,
                "instance": instance.get("instance_name"),
                "formal_output": formal,
                "width_bits": parent_width,
                "instance_line": instance.get("line_start"),
                "parent_sha256": source_sha256(parent_entry["source"]),
                "child_sha256": source_sha256(child_entry["source"]),
                "evidence": f"{child_name}.{formal} -> {parent_name}.{signal}",
            })

    if blockers:
        return {"status": "unresolved", "reasons": sorted(set(blockers))}
    if len(drivers) != 1:
        reason = "no_known_output_driver" if not drivers else "multiple_known_output_drivers"
        return {"status": "unresolved", "reasons": [reason]}
    return {"status": "proven_instance_output_driver", "driver": drivers[0]}


def self_check(backend) -> dict[str, bool]:
    def source(lines=()):
        return type("Source", (), {"lines": tuple(lines), "relative_path": "selfcheck.v"})()

    parent_decl = {"kind": "wire", "name": "net", "width": "[7:0]", "signed": False,
                   "unpacked": "", "init": "", "line_start": 1}
    base_actual = {
        "kind": "expression", "text": "net", "references": ["net"],
        "static_lvalue_segments": [{"name": "net"}],
        "expression": {"node_kind": "identifier", "name": "net"},
    }
    base_instance = {
        "module_name": "child", "instance_name": "child_Inst", "parse_complete": True,
        "has_params": False, "parameter_overrides": [], "array_range_text": "",
        "association_style": "named", "line_start": 2,
        "port_associations": [{"formal_name": "o_data", "actual": base_actual}],
    }
    parent = {"name": "parent", "decls": [parent_decl], "ports": [],
              "comb_expressions": [], "instances": [base_instance], "generates": []}
    child = {"name": "child", "ports": [{"name": "o_data", "direction": "output",
                                            "width": "[7:0]", "signed": False, "unpacked": ""}]}
    catalog = {"parent": {"module": parent, "source": source(("wire [7:0] net;",))},
               "child": {"module": child, "source": source()}}

    known_output = resolve_driver(catalog, "parent", "net")["status"] == "proven_instance_output_driver"
    child["ports"][0]["direction"] = "input"
    input_rejected = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    child["ports"][0]["direction"] = "inout"
    inout_rejected = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    child["ports"][0]["direction"] = "output"
    catalog.pop("child")
    unknown_child = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    catalog["child"] = {"module": child, "source": source()}
    child["ports"][0]["direction"] = ""
    unknown_direction = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    child["ports"][0]["direction"] = "output"
    child["ports"][0]["width"] = "[WIDTH-1:0]"
    unknown_width = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    child["ports"][0]["width"] = "[7:0]"
    base_actual["text"] = "{net}"
    non_bare = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    base_actual["text"] = "net"
    base_instance["has_params"] = True
    parameterized = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    base_instance["has_params"] = False
    parent["generates"] = [{"line_start": 1, "line_end": 3}]
    generated = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    parent["generates"] = []
    child["generates"] = [{"line_start": 1, "line_end": 3}]
    child_generated = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    child["generates"] = []
    child["ports"][0]["width"] = "[6:0]"
    width_mismatch = resolve_driver(catalog, "parent", "net")["status"] == "unresolved"
    child["ports"][0]["width"] = "[7:0]"

    orphan_module = {
        "name": "orphan_parent",
        "decls": [{"kind": "wire", "name": "orphan", "width": "", "signed": False,
                   "unpacked": "", "init": "", "line_start": 1}],
        "ports": [], "instances": [], "generates": [],
        "comb_expressions": [{"target": "sink", "expression": {"node_kind": "identifier",
                                                                  "name": "orphan"}}],
    }
    orphan_facts = _module_signal_facts(orphan_module, ("wire orphan;", "assign sink = orphan;"))
    real_undriven = "orphan" in orphan_facts["reads"] and "orphan" not in orphan_facts["drivers"]

    other_signal = backend.REGION_TITLES["other_signal"]
    other_assign = backend.REGION_TITLES["other_assign"]
    wrong_banner_order = not exact_region_order((other_assign, other_signal), backend)["passed"]
    exact_title_order = exact_region_order((other_signal, other_assign), backend)["passed"]
    return {
        "real_undriven_remains_failed": real_undriven,
        "known_output_proven": known_output,
        "input_not_driver": input_rejected,
        "inout_unresolved": inout_rejected,
        "unknown_child_unresolved": unknown_child,
        "unknown_direction_unresolved": unknown_direction,
        "unknown_width_unresolved": unknown_width,
        "non_bare_actual_unresolved": non_bare,
        "parameterized_instance_unresolved": parameterized,
        "generate_scope_unresolved": generated,
        "child_generate_unresolved": child_generated,
        "width_mismatch_unresolved": width_mismatch,
        "wrong_banner_order_rejected": wrong_banner_order,
        "other_signal_title_not_substring_matched": exact_title_order,
    }


def main() -> int:
    facts = build_vg_facts(RTL_ROOT, include_testbench=False)
    catalog = module_catalog(facts)
    backend = create_formatter_backend(profile="formatter-normalize")
    checks = self_check(backend)
    if not all(checks.values()):
        raise AssertionError(f"self-check failed: {checks}")

    original = evaluate_liveness_gate(facts, "VG153")
    findings = []
    proven = []
    unresolved = []
    for finding in original.findings:
        metadata = dict(finding.metadata)
        item = {
            "module": metadata.get("module"), "symbol": metadata.get("symbol"),
            "path": finding.path, "line": finding.line, "message": finding.message,
            "driver_state": metadata.get("driver_state"), "read_state": metadata.get("read_state"),
        }
        findings.append(item)
        result = resolve_driver(catalog, str(item["module"]), str(item["symbol"]))
        (proven if result["status"] == "proven_instance_output_driver" else unresolved).append(
            {**item, **result}
        )

    regions = {
        source.relative_path: exact_region_order(source.lines, backend)
        for source in facts.sources
    }
    source_hashes = {source.relative_path: sha256(source.path) for source in facts.sources}
    report = {
        "schema": "road-module-boundary-diagnostic-v1",
        "mode": "diagnostic-only",
        "gate_modified": False,
        "rtl_modified": False,
        "root": str(RTL_ROOT),
        "source_sha256": source_hashes,
        "original_vg153": {
            "status": original.status,
            "applicable": original.applicable,
            "finding_count": len(findings),
            "findings": findings,
        },
        "boundary_resolution": {
            "proven_false_positive_count": len(proven),
            "proven_false_positives": proven,
            "unresolved_count": len(unresolved),
            "unresolved": unresolved,
        },
        "region_order": regions,
        "self_check": {"passed": all(checks.values()), "checks": checks},
    }
    report["current_four_module_fixture_proven"] = (
        len(findings) == 12
        and len(proven) == 12
        and not unresolved
        and all(item["passed"] for item in regions.values())
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["current_four_module_fixture_proven"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
