"""只读核对已有收据与完整数值/源闭包，不重启训练或仿真。"""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    previous = HERE.parent / "rom_two_client_20261015"
    final = json.loads((previous / "verification/final_summary.json").read_text(encoding="utf-8"))
    summary_path = previous / "verification" / final["receipt"]
    assert sha(summary_path) == final["receipt_sha256"]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    snapshot = Path(summary["snapshot"])
    assert summary["status"] == "PASS" and len(summary["tests"]) == 2
    assert all(test["status"] == "PASS" and test["returncode"] == 0 for test in summary["tests"].values())
    checked = 0
    for rel, expected in summary["closure_sha256"].items():
        assert sha(snapshot / rel) == expected, rel
        if rel.startswith(("rtl/", "artifacts/", "reference/")) or rel in ("requirements.json", "codegen_plan.txt", "top_ports.json"):
            assert sha(previous / rel) == expected, rel
        checked += 1
    for tool in summary["tools"].values():
        assert sha(Path(tool["path"])) == tool["sha256"]
    for test in summary["tests"].values():
        assert sha(Path(test["trace"])) == test["trace_sha256"]
    assert sha(Path(summary["parameter_stream"]["path"])) == summary["parameter_stream"]["sha256"]
    counts = {}
    for directory, layers, tiles in (("reference", 4, 20), ("reference_extended", 6, 30), ("reference_head", 21, 105)):
        folder = HERE / directory
        inputs = json.loads((folder / "input_binding.json").read_text(encoding="utf-8"))
        for path, expected in inputs["source_sha256"].items():
            assert sha(Path(path)) == expected, path
        artifacts = json.loads((folder / "artifact_manifest.json").read_text(encoding="utf-8"))
        for rel, expected in artifacts.items():
            assert sha(folder / rel) == expected, rel
        reference = json.loads((folder / "verification_receipt.json").read_text(encoding="utf-8"))
        assert reference["status"] == "PASS" and reference["layers"] == layers and reference["tiles"] == tiles
        assert reference["closure_sha256"] == inputs["closure_sha256"]
        counts[directory] = {"sources": len(inputs["source_sha256"]), "artifacts": len(artifacts)}
    print(f"READONLY_RECEIPTS_PASS previous_closure={checked} references={counts}")


if __name__ == "__main__":
    main()
