from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPORTS = {
    "silu_original": HERE.parent / "v3_silu_stall_candidate_20261005" / "original_gate.json",
    "silu_candidate": HERE.parent / "v3_silu_stall_candidate_20261005" / "candidate_gate.json",
    "round_testbench": HERE.parent / "v3_round_stall_20261005" / "strict_gate_final.json",
}


def evidence_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for part in text.split("; "):
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key] = value
    return fields


def location(issue: dict) -> tuple[str, str, str]:
    loc = issue.get("location") or {}
    file_name = loc.get("file") or issue.get("path") or ""
    start = loc.get("line_start") or issue.get("line") or ""
    end = loc.get("line_end") or start
    match = re.fullmatch(r"(.+):(\d+)", str(file_name))
    if match:
        file_name, start, end = match.group(1), match.group(2), match.group(2)
    return str(file_name), str(start), str(end)


def target_of(issue: dict, fields: dict[str, str]) -> str:
    if fields.get("target"):
        return fields["target"]
    detail = str((issue.get("evidence") or {}).get("detail") or issue.get("detail") or "")
    code = issue.get("code", "")
    if code == "VG145" and ":" in detail:
        return detail.split(":", 1)[0]
    if code in {"VG085", "VG153"}:
        return detail
    quoted = re.search(r"`([^`]+)`", str(issue.get("message") or issue.get("problem") or ""))
    return quoted.group(1) if quoted else ""


def classify(dataset: str, issue: dict, target: str, fields: dict[str, str], candidate_only: bool) -> tuple[str, str, str, str]:
    code = issue.get("code", "")
    detail = str((issue.get("evidence") or {}).get("detail") or issue.get("detail") or "")
    if dataset == "round_testbench":
        if detail == "FORMATTER_AST_PARSE":
            return "RC-R-TB-ALWAYS-DELAY-PARSER", "parser_derived", "undetermined_due_parser", "fix_or_scope_parser_then_rerun"
        mapping = {
            "VG004": ("RC-R-TB-SPACE-INDENT", "real_style_nonconformance"),
            "VG007": ("RC-R-TB-HEADER", "real_style_nonconformance"),
            "VG068": ("RC-R-TB-HEADER", "real_style_nonconformance"),
            "VG025": ("RC-R-TB-BEGIN-END", "real_style_nonconformance"),
            "VG040": ("RC-R-TB-COMMENT-COVERAGE", "real_style_nonconformance"),
            "VG042": ("RC-R-TB-COMMENT-COVERAGE", "real_style_nonconformance"),
            "COMMENT_COMMENT_PLACEMENT": ("RC-R-TB-COMMENT-COVERAGE", "derived_comment_gate"),
            "VG069": ("RC-R-TB-DISPLAY-PREFIX", "real_testbench_style_nonconformance"),
        }
        root, category = mapping.get(code, ("RC-R-UNCLASSIFIED", "needs_manual_review"))
        return root, category, "applicable_to_strict_testbench_profile", "repair_testbench_style_then_rerun"

    if code in {"VG040", "VG060", "VG061", "VG062", "VG063", "VG065", "VG066", "COMMENT_COMMENT_PLACEMENT"}:
        return "RC-S-COMMENT-FORMAT", "real_style_nonconformance", "applicable", "mechanical_style_repair"
    if code == "VG013":
        return "RC-S-NAMING", "real_style_nonconformance", "applicable", "mechanical_naming_repair_with_behavior_check"
    if code in {"VG125", "VG138"}:
        return "RC-S-LITERAL-STYLE", "real_style_nonconformance", "applicable", "mechanical_literal_repair_with_width_check"
    if code in {"VG084", "VG137"}:
        return "RC-S-WIDTH-ANALYSIS-INCOMPLETE", "analysis_inconclusive", "applicable_but_unresolved", "supply_or_fix_width_evidence_then_rerun"
    if code == "VG085":
        return "RC-S-PARTSELECT-DROPPED", "checker_applicability_defect", "reported_expression_disagrees_with_source", "fix_checker_not_rtl_counter_width"
    if code == "VG097":
        return "RC-S-PH1P-INSTANCE-PARSE", "external_interface_evidence_gap", "applicable_but_unresolved", "use_governed_ph1p_interface_then_rerun"
    if code == "VG132":
        return "RC-S-PH1P-CLOCK-ROLE", "checker_applicability_defect", "clka_clkb_are_real_clock_ports", "resolve_instance_port_roles_then_rerun"
    if code == "VG153":
        return "RC-S-PH1P-OUTPUT-DRIVER", "external_interface_evidence_gap", "applicable_but_driver_unresolved", "resolve_doa_output_direction_then_rerun"
    if code == "VG122":
        return "RC-S-ARITH-WIDTH", "real_rtl_width_risk", "applicable", "manual_signed_width_review"
    if code == "VG145":
        return "RC-S-SOURCE-CONE", "real_comb_control_complexity", "applicable", "architecture_review_before_latency_change"
    if code in {"VG146", "VG147"}:
        reason = fields.get("inconclusive_reason", "")
        if candidate_only:
            return "RC-S-PH1P-CEA-UNKNOWN-BACKPROP", "checker_derived_from_unresolved_input_port", "rule_result_blocking_but_rtl_risk_not_proven", "resolve_input_sink_ownership_then_rerun"
        if "external interface has no implementation" in reason:
            return "RC-S-PH1P-EXTERNAL-CLOSURE", "external_interface_evidence_gap", "applicable_but_unresolved", "use_governed_ph1p_interface_then_rerun"
        if "missing storage data expression" in reason:
            return "RC-S-STORAGE-EXPR-EXTRACTION", "analysis_inconclusive", "applicable_but_unresolved", "fix_or_complete_formatter_ast_then_rerun"
        return "RC-S-OPERATION-BUDGET", "real_comb_control_complexity", "applicable", "architecture_review_before_latency_change"
    return "RC-S-UNCLASSIFIED", "needs_manual_review", "unknown", "manual_review"


def main() -> None:
    loaded = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in REPORTS.items()}
    original_targets = {
        (item.get("code"), evidence_fields(str((item.get("evidence") or {}).get("detail") or "")).get("target", ""))
        for item in loaded["silu_original"]["issues"]
        if item.get("code") in {"VG146", "VG147"}
    }
    rows = []
    records = []
    summaries = []
    additional_evidence = []
    for dataset, report in loaded.items():
        issues = report["issues"]
        summaries.append({
            "dataset": dataset,
            "source": str(REPORTS[dataset]),
            "reported_errors": report["errors"],
            "classified_issue_count": len(issues),
            "aggregate_only_error_count": report["errors"] - len(issues),
        })
        ast_files = report["quality_gate"]["ast_report"]["files"]
        formatter_facts = [
            {"file": item.get("relative_path", ""), "formatter_violation": item.get("formatter_violations", "")}
            for item in ast_files
            if item.get("formatter_violations")
        ]
        additional_evidence.append({
            "record_type": "run_level_formatter_error_not_an_issue_finding",
            "dataset": dataset,
            "count": report["errors"] - len(issues),
            "ast_error_count": report["checks"]["ast"]["errors"],
            "parse_error_count": report["checks"]["ast"]["parse_errors"],
            "formatter_error_count": report["checks"]["ast"]["formatter_errors"],
            "facts": formatter_facts,
            "rootcause": "RC-R-TB-ALWAYS-DELAY-PARSER" if dataset == "round_testbench" else "RC-S-FORMATTER-TEMPLATE-MISMATCH",
            "blocking": True,
        })
        for index, issue in enumerate(issues, 1):
            detail = str((issue.get("evidence") or {}).get("detail") or issue.get("detail") or "")
            fields = evidence_fields(detail)
            target = target_of(issue, fields)
            key = (issue.get("code"), target)
            candidate_only = dataset == "silu_candidate" and issue.get("code") in {"VG146", "VG147"} and key not in original_targets
            root, category, applicability, disposition = classify(dataset, issue, target, fields, candidate_only)
            file_name, line_start, line_end = location(issue)
            row = {
                "dataset": dataset,
                "raw_index": index,
                "source_layer": "comment_gate" if issue.get("source") == "current_module_issue" else "quality_gate",
                "rule": issue.get("code", ""),
                "rule_key": issue.get("rule_key") or issue.get("rule") or "",
                "raw_status": issue.get("status") or "failed",
                "severity": issue.get("severity", ""),
                "file": file_name,
                "target": target,
                "cone": detail if issue.get("code") in {"VG145", "VG146", "VG147"} else "",
                "start": line_start,
                "end": line_end,
                "definition_root": fields.get("definition_root", ""),
                "instance_path": fields.get("instance_path", ""),
                "specialization": fields.get("specialization", ""),
                "operation_count": fields.get("operation_count", ""),
                "limit": fields.get("limit", ""),
                "loop_presence": fields.get("loop_presence", ""),
                "inconclusive_reason": fields.get("inconclusive_reason", ""),
                "rootcause": root,
                "category": category,
                "applicability": applicability,
                "disposition": disposition,
                "blocking": True,
                "delta": "candidate_only" if candidate_only else ("shared_or_existing" if dataset.startswith("silu_") else "round_only"),
                "raw_message": issue.get("problem") or issue.get("message") or "",
                "raw_evidence": detail,
            }
            rows.append(row)
            records.append({"classification": row, "raw_issue": issue})

    assert [item["reported_errors"] for item in summaries] == [174, 242, 413]
    assert [item["classified_issue_count"] for item in summaries] == [173, 241, 412]
    assert len(rows) == 826
    assert sum(item["count"] for item in additional_evidence) == 3
    assert len(rows) + sum(item["count"] for item in additional_evidence) == 829
    assert Counter((row["rule"], row["delta"]) for row in rows)[("VG146", "candidate_only")] == 31
    assert Counter((row["rule"], row["delta"]) for row in rows)[("VG147", "candidate_only")] == 37

    (HERE / "finding_classification.json").write_text(
        json.dumps({"report_summaries": summaries, "issue_records": records, "additional_run_level_evidence": additional_evidence}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (HERE / "finding_classification.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    root_counts = Counter((row["dataset"], row["rootcause"], row["category"], row["applicability"], row["disposition"]) for row in rows)
    grouped = [
        {"dataset": key[0], "rootcause": key[1], "category": key[2], "applicability": key[3], "disposition": key[4], "count": count}
        for key, count in sorted(root_counts.items())
    ]
    (HERE / "root_cause_groups.json").write_text(json.dumps(grouped, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "additional_run_level_evidence.json").write_text(json.dumps(additional_evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"issue_rows": len(rows), "run_level_errors": 3, "total_error_accounting": 829, "summaries": summaries, "candidate_vg146_new": 31, "candidate_vg147_new": 37}, ensure_ascii=False))


if __name__ == "__main__":
    main()
