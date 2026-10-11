"""Keep gate objects distinct; classification does not waive a finding."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    reports = root.parent
    objects = {
        "frozen_chain": (reports / "v7_onchip_chain_20261006/strict_gate.json", 374),
        "original_low_io_shell": (reports / "v7_low_io_physical_20261006/shell/strict_shell.json", 667),
        "original_testbench": (reports / "v7_low_io_physical_20261006/shell/strict_tb_included.json", 219),
    }
    priority = {"VG098", "VG104", "VG122", "VG125", "VG141", "VG153", "VG155"}
    style = {"VG013", "VG020", "VG025", "VG030", "VG031", "VG054", "VG060",
             "VG061", "VG063", "VG066", "VG068", "VG070", "VG157",
             "COMMENT_COMMENT_PLACEMENT", "FORMATTER_TEMPLATE_MISMATCH"}
    result = {}
    for label, (path, expected) in objects.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        counts = data["delivery_issues_by_rule"]
        assert data["strict"] and not data["delivery_ready"]
        assert data["errors"] == expected == sum(counts.values())
        classes = {"priority_semantics": {}, "style_and_structure": {}, "other_unclosed": {}}
        for rule, count in counts.items():
            bucket = "priority_semantics" if rule in priority else (
                "style_and_structure" if rule in style else "other_unclosed")
            classes[bucket][rule] = count
        assert sum(sum(group.values()) for group in classes.values()) == expected
        result[label] = {
            "report": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "errors": expected, "strict_warnings": data["strict_warnings"],
            "public_gates": {key: value["status"] for key, value in data["checks"].items()},
            "classification": classes,
            "priority_findings": [item for item in data["issues"]
                                  if item.get("code") in priority],
            "delivery_ready": False,
        }
    payload = {"status": "HISTORICAL_FAILURES_RETAINED_NOT_WAIVED",
               "scope": "Immutable historical report objects; category counts are diagnostics, not counts of independent functional defects. AST-generated failures may not appear as separate issues entries.",
               "objects": result}
    (root / "retained_gate_audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value["errors"] for key, value in result.items()}))


if __name__ == "__main__":
    main()
