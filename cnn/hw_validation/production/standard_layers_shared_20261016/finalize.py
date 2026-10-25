"""封存第七批组件收据；只核对，不重跑仿真/训练/综合。"""

import json
from pathlib import Path

from check_receipts import HERE, main as check_references, sha


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    check_references()
    head_path = HERE / "verification_head/final_summary.json"
    stream_path = HERE / "head/stream/verification/delivery.json"
    owner_path = HERE / "head/owner/handoff.json"
    head, stream, owner = map(read, (head_path, stream_path, owner_path))
    assert head["status"] == "PASS_31_FIXED_SELECTIONS_REPRESENTATIVE_NATIVE_FUNCTIONAL_ONLY"
    assert head["native_head_layers"] == 21 and head["native_head_tiles"] == 105 and head["total_nominal_tiles"] == 115
    assert head["native_protocol_modes"] == 12 and head["real_acc_checker_negative"] == 1
    assert all(head["source_hash_reverified"].values())
    assert head["arithmetic_owner_sha256"] == owner["owner_sha256"] == "244eb1939b68e91a88a21366fccde37026ac3ed2d502869d65df18b4d62aaf2d"
    assert sha(Path(owner["qualified_owner"])) == owner["owner_sha256"]
    assert sha(HERE / "head/owner/rtl/road_standard_arithmetic_owner.v") == owner["owner_sha256"]
    reports = {}
    verified_functional = {}
    for name, info in head["reports"].items():
        folder = Path(info["path"])
        receipt_path = folder / "summary.json"
        assert sha(receipt_path) == info["summary_sha256"], name
        receipt = read(receipt_path)
        assert receipt["status"] == "PASS" and receipt["snapshot_unchanged"] and receipt["original_unchanged"]
        assert len(receipt["tests"]) == info["tests"] and all(test["status"].startswith("PASS") for test in receipt["tests"])
        # 大golden快照由独立verify已逐项重读；主核对当前功能源、相同核和工具，不重做算术或穷举。
        for path, expected in receipt["original_sha256"].items():
            if Path(path).suffix in (".v", ".exe", ".bin"):
                assert sha(Path(path)) == expected, path
                verified_functional[path] = expected
        for tool in receipt["tools"].values():
            assert sha(Path(tool["path"])) == tool["sha256"]
        reports[name] = {"summary": str(receipt_path), "sha256": sha(receipt_path), "tests": len(receipt["tests"]), "independent_snapshot_reverified": info["snapshot_reverified"]}
    assert stream["status"] == "FUNCTIONAL_PASS_STRICT_NOT_READY" and stream["actual_modelsim"] == "PASS"
    assert len(stream["tests"]) == 11 and stream["snapshot_unchanged"] and stream["original_unchanged"]
    for path, expected in stream["source_sha256"].items():
        assert sha(Path(path)) == expected, path
    stream_receipt = read(Path(stream["functional_receipt"]))
    for path, expected in stream_receipt["original_sha256"].items():
        assert sha(Path(path)) == expected, path
    for case, info in owner["cases"].items():
        folder = Path(info["run"])
        assert sha(folder / "status.json") == info["status_sha256"]
        assert sha(folder / "binding.json") == info["binding_sha256"]
        binding = read(folder / "binding.json")
        for path, expected in binding["source_vector_sha256"].items():
            assert sha(folder / path) == expected, (case, path)
    sequence_path = HERE / "sequence/verification/reports/20261016_014753_201865/summary.json"
    sequence = read(sequence_path)
    assert sequence["status"] == "PASS" and sequence["snapshot_unchanged"] and sequence["current_sources_unchanged"]
    for path, expected in sequence["snapshot_sha256"].items():
        assert sha(Path(sequence["snapshot"]) / path) == expected
    for path, expected in sequence["original_sha256"].items():
        assert sha(Path(path)) == expected
    files = {"standard_tile_client": HERE / "head/client/rtl/road_standard_tile_client.v",
             "arithmetic_owner": Path(owner["qualified_owner"]),
             "head_cell_stream": HERE / "head/stream/rtl/road_head_cell_stream.v",
             "layer_sequence": HERE / "sequence/rtl/road_standard_layer_sequence.v",
             "C4_workstore": HERE.parent / "workstore_feature_20261016/storage_frozen/rtl/road_feature_workstore.v"}
    strict = {}
    for name, path in (("joint_native", Path(head["strict_report"])), ("owner", Path(owner["strict_gate"]["path"])),
                       ("sequence", HERE / "sequence/gates/initial.json"), ("sequence_tb", HERE / "sequence/gates/tb_initial.json")):
        gate = read(path)
        assert not gate["delivery_ready"]
        strict[name] = {"path": str(path), "sha256": sha(path), "checks": gate["checks"], "errors": gate["errors"], "strict_warnings": gate["strict_warnings"]}
    result = {"status": "COMPONENT_FUNCTIONAL_PASS_STRICT_AND_SYSTEM_OPEN", "branch": "work/roadyolo",
              "selected_sources": {name: {"path": str(path), "sha256": sha(path)} for name, path in files.items()},
              "component_handoffs": {str(path.relative_to(HERE)): sha(path) for path in (head_path, stream_path, owner_path, HERE / "verification_extended/final_summary.json")},
              "qualified_native_reports": reports, "main_reverified_functional_sources": verified_functional,
              "head_tiles": head["head_totals"], "raw_int16": head["raw_int16"], "total_native_nominal_tiles": 115,
              "stream_receipt": {"path": stream["functional_receipt"], "sha256": sha(Path(stream["functional_receipt"])), "tests": 11, "metrics": stream["normal_metrics"]},
              "owner_tests": len(owner["cases"]), "sequence_receipt": {"path": str(sequence_path), "sha256": sha(sequence_path), "metrics": sequence["metrics"]},
              "strict_gates": strict, "stream_eight_gates": stream["eight_gates"],
              "numerical_model": {"payload_sha256": "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145", "qualification": "PTQ_DIAGNOSTIC_NOT_BOARD_QUALIFIED; no accuracy/QAT acceptance"},
              "implementation": {"client_private_tile_or_weight_arrays": 0, "complete_prediction_RAM_added": False, "new_ERAM_or_DSP": "NOT_MAPPED; no target used as actual result"},
              "open": ["actual full-layer sequencing connected to compute and full tensor numerical output", "C7 application interface decision: unify raw16 and residual/bypass owner, never duplicate five kernels", "down3-CSP3-down4-CSP4 single-owner continuous chain", "runtime ROM parameters beyond down2 boot", "all67conv plus PAN/SPPF full graph", "actual DDR write visibility and live video integration", "strict gates and real integrated resources/timing", "whole-network1FPS/100M or original5FPS/accuracy acceptance"],
              "not_run": ["training", "TD", "production modification", "bitstream", "board/Flash", "commit/push", "timing exceptions"],
              "evidence_boundary": "Native workstore functional simulation only. Head/reference and stream planes are controlled CPU data; separate stream and sequence PASS do not prove a connected full-frame producer pipeline."}
    workflow = [HERE / "requirements.json", HERE / "codegen_plan.txt", HERE / "interface_review.txt", Path(__file__)]
    for directory in ("head/client", "head/stream", "sequence"):
        folder = HERE / directory
        workflow += [folder / "requirements.json", folder / "codegen_plan.txt", folder / "spec_input.json"]
        workflow += [path for path in (folder / "sc").rglob("*") if path.is_file()]
    workflow += [path for path in (HERE / "sequence/t").rglob("*") if path.is_file()]
    result["main_workflow_sha256"] = {str(path.relative_to(HERE)): sha(path) for path in workflow}
    (HERE / "final_receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"MAIN_FINAL_RECEIPT_PASS native_tiles=115 head_layers=21 owner_cases={len(owner['cases'])} cells=12096 sequenced_tiles=6240 strict_ready=false")


if __name__ == "__main__":
    main()
