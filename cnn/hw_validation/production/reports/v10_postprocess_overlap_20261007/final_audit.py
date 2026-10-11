"""Read-only identity audit of the completed diagnostic stage, not signoff."""
import json
from pathlib import Path
from guard import ROOT, bounded, check, digest


def main():
    frozen = check()
    verification = json.loads((ROOT / "verification/verification_summary.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "verification/final_hash_manifest.json").read_text(encoding="utf-8"))
    physical = json.loads((ROOT / "physical/prebuild_manifest.json").read_text(encoding="utf-8"))
    gates = json.loads((ROOT / "gates/source_manifest.json").read_text(encoding="utf-8"))
    checked = 0
    for item in manifest["files"]:
        path = Path(item["path"])
        assert digest(path) == item["sha256"], f"Changed verification evidence: {path}"
        checked += 1
    for item in physical["source_read_order"]:
        path = (ROOT / "physical" / item["path"]).resolve()
        assert digest(path) == item["sha256"], f"Changed implemented RTL: {path}"
        checked += 1
    physical_manifest = json.loads((ROOT / "physical/physical_evidence_manifest.json").read_text(encoding="utf-8"))
    for section in ("sources", "functional_evidence", "implementation_databases",
                    "primary_raw_reports", "guard_receipts", "derived_reports"):
        for name, expected in physical_manifest[section].items():
            path = (ROOT / "physical" / name).resolve()
            assert digest(path) == expected, f"Changed physical evidence: {section}:{name}"
            checked += 1
    for path_string, item in gates.items():
        assert digest(Path(path_string)) == item["sha256"], path_string
        assert digest(bounded(item["snapshot"])) == item["sha256"], item["snapshot"]
        checked += 2
    for name, item in verification["fresh_regressions"].items():
        path = bounded(item["path"])
        assert digest(path) == item["sha256"], name
        log = path.read_text(encoding="utf-8", errors="replace")
        assert item["pass_marker"] in log, f"Missing actual pass marker: {name}"
        assert item["tool_errors"] == 0 and item["missing_file_indications"] == 0, name
    assert verification["same_vector_copy_audit"]["mismatches"] == 0
    assert verification["candidate"]["reset_ages"]["pass_count"] == 24
    assert verification["candidate"]["random_stress"]["groups"] == 48
    assert not list(ROOT.rglob("*.bit")), "Unexpected deployment bitstream"
    report = ROOT / "RoadYOLO_v10_后处理流水化最终对比报告_20261007.md"
    assert report.is_file()
    result = {
        "status": "DIAGNOSTIC_EVIDENCE_IDENTITY_PASS_NOT_PRODUCTION_SIGNOFF",
        "frozen_previous": frozen,
        "source_and_evidence_hash_checks": checked,
        "fresh_regression_markers": len(verification["fresh_regressions"]),
        "same_vector_copy_pairs": verification["same_vector_copy_audit"]["exact_copy_pairs"],
        "report_sha256": digest(report),
        "model_quantization_integrated": False,
        "network_5fps_verified": False,
        "physical_timing_signoff": False,
        "strict_delivery_ready": False,
        "bitstream_generated": False,
    }
    target = ROOT / "FINAL_AUDIT.json"
    with target.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    print(json.dumps(check()))


if __name__ == "__main__":
    main()
