"""只导入既有G10物理导出和已冻结RTL；独立反向重建检查，不运行网络。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parent
ROOT = HERE.parents[3]
SOURCE = ROOT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
R1 = PRODUCTION / "rom_reader_r1_20261015"
LUT = PRODUCTION / "shared_lut_service_1fps_20261015"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze(source: Path, destination: Path) -> str:
    """已有目标只能相同，不覆盖不同的用户文件。"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        assert destination.read_bytes() == source.read_bytes(), str(destination)
    else:
        shutil.copyfile(source, destination)
    assert sha(source) == sha(destination)
    return sha(destination)


def main() -> None:
    required = json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))
    manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    old_manifest = json.loads((R1 / "artifacts/manifest.json").read_text(encoding="utf-8"))
    assert old_manifest["payload_sha256"] == required["old_R1_payload_not_target"]
    assert old_manifest["payload_sha256"] != required["payload_sha256"]
    assert manifest["payload_sha256"] == required["payload_sha256"]
    assert manifest["physical_sha256"] == required["physical_sha256"]
    assert sha(SOURCE / "numeric_test.bin") == manifest["payload_sha256"]
    assert sha(SOURCE / "numeric_test_padded.bin") == manifest["physical_sha256"]
    payload = (SOURCE / "numeric_test.bin").read_bytes()
    physical = (SOURCE / "numeric_test_padded.bin").read_bytes()
    assert len(payload) == 140522 and physical == payload + bytes(2838)
    assert manifest["layout"] == {"word_bytes": 20, "words_per_group": 512, "groups": 14, "lanes": 4, "lane_bytes": 5}

    # 直接复用已经由trained_integer.write_package拆出的lane，不再次生成模型或lane文件。
    lane_hashes = {item["name"]: item["sha256"] for item in manifest["lane_files"]}
    assert len(lane_hashes) == 56
    reconstruction = bytearray()
    frozen_artifacts = {}
    for group in range(14):
        lanes = []
        for lane in range(4):
            name = f"group_{group:02d}_lane_{lane}.dath"
            path = SOURCE / name
            assert sha(path) == lane_hashes[name], name
            rows = path.read_text(encoding="ascii").splitlines()
            assert len(rows) == 512 and all(len(row) == 10 for row in rows), name
            lanes.append([bytes.fromhex(row)[::-1] for row in rows])
            frozen_artifacts[name] = freeze(path, HERE / "artifacts" / name)
        for word in range(512):
            reconstruction.extend(b"".join(lanes[lane][word] for lane in range(4)))
    assert bytes(reconstruction) == physical
    rows = (SOURCE / "words.dath").read_text(encoding="ascii").splitlines()
    assert len(rows) == 7168 and b"".join(bytes.fromhex(row)[::-1] for row in rows) == physical
    for name in ("manifest.json", "numeric_test.bin", "numeric_test_padded.bin", "words.dath"):
        frozen_artifacts[name] = freeze(SOURCE / name, HERE / "artifacts" / name)

    frozen_sources = {}
    for name in ("road_numeric_rom_reader.v", "road_yolo_numeric_rom_group.v", "road_shared_lut_service.v"):
        source = (LUT if name == "road_shared_lut_service.v" else R1) / "rtl" / name
        assert sha(source) == required["immutable_sources"][name], name
        frozen_sources[name] = freeze(source, HERE / "rtl" / name)
    # 规格是既有行为解释，不因为换模型包重写历史RTL或历史门禁。
    companion_sources = {
        "road_shared_lut_service_spec.md": LUT / "spec_checked/spec/road_shared_lut_service/road_shared_lut_service_spec.md",
        "road_yolo_numeric_rom_group_spec.md": R1 / "rtl/road_yolo_numeric_rom_group_spec.md",
    }
    for name, source in companion_sources.items():
        freeze(source, HERE / "reused_specs" / name)
    proof = {
        "status": "FROZEN_G10_EXPORT_IMPORT_AND_RECONSTRUCTION_PASS",
        "source_package": str(SOURCE), "payload_sha256": sha(SOURCE / "numeric_test.bin"),
        "physical_sha256": sha(SOURCE / "numeric_test_padded.bin"),
        "old_R1_manifest_sha256": sha(R1 / "artifacts/manifest.json"),
        "old_R1_payload_sha256": old_manifest["payload_sha256"],
        "manifest_sha256": sha(SOURCE / "manifest.json"), "physical_bytes_reconstructed": len(reconstruction),
        "words": len(rows), "lane_files": len(lane_hashes), "padding_bytes": 2838,
        "frozen_artifacts": frozen_artifacts, "frozen_sources": frozen_sources,
        "reuse": "Import byte-identical existing trained_integer.write_package outputs; no re-encoding or alternate splitter",
        "splitter_source_sha256": sha(PRODUCTION / "trained_integer.py"),
        "stage_script_sha256": sha(Path(__file__)), "requirements_sha256": sha(HERE / "requirements.json"),
        "spec_reference_sha256": sha(LUT / "reference.py"), "no_inference_training_td_or_board": True,
    }
    (HERE / "package_receipt.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    # 规格对象复用已完成的描述生成器，不另造规格/RTL解析器。
    module_spec = importlib.util.spec_from_file_location("frozen_lut_reference", LUT / "reference.py")
    reference = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(reference)
    top_spec = reference.specification("road_real_model_lut_top", required, [
        "一个冻结ROM-R1 reader连接一个冻结共享LUT服务；无额外缓存、时钟、参数变换或流水。",
        "reader的14组/56lane只加载G10初始化；i_cancel只进入服务，绝不当作reader复位。",
        "真实reader接受后等待原cnt_wait7；服务保持动态身份、跨词聚合和取消排空合同。"
    ], [{"name": "i_clk", "wave": "p..........."}, {"name": "lut_req_valid", "wave": "010........."},
        {"name": "lut_req_ready", "wave": "01.0........"}, {"name": "rom_req_valid", "wave": "0....10....."},
        {"name": "rom_rsp_valid", "wave": "0.......10.."}, {"name": "lut_rsp_valid", "wave": "0........1.0"},
        {"name": "lut_rsp_ready", "wave": "0.........10"}])
    top_spec["timing_diagrams"][0]["description"] = "动态请求握手示意，省略18步地址定位和reader固定等待；不是按图格数换算实际总时延。反压时身份/数值保持。"
    reference.save(HERE / "spec_input_top.json", top_spec)
    reader_contract = {"inputs": {"i_clk": 1, "i_rstn": 1, "i_request_valid": 1, "i_request_addr": 13, "i_response_ready": 1},
                       "outputs": {"o_request_ready": 1, "o_response_valid": 1, "o_response_data": 160, "o_fault": 1}}
    reader_spec = reference.specification("road_numeric_rom_reader", reader_contract, [
        "冻结reader源码完全相同；一个未决13位词号，地址0..7167，非法地址粘滞故障。",
        "接受时锁定地址，原WAIT计数0..7后注册完整160位；响应保持至ready，不缩短等待。",
        "共同i_rstn清valid/state；取消排空由外部LUT服务处理，不增加reader cancel端口。"
    ], [{"name": "i_clk", "wave": "p..........."}, {"name": "request_valid", "wave": "010........."},
        {"name": "request_ready", "wave": "01.0........"}, {"name": "response_valid", "wave": "0........1.0"},
        {"name": "response_ready", "wave": "0.........10"}])
    reader_spec["reset"]["release"] = "Unchanged reader input reset; requester service waits for its own two-stage release"
    reference.save(HERE / "spec_input_reader.json", reader_spec)
    group_contract = {"inputs": {"i_clk": 1, "i_rstn": 1, "i_word_addr": 9}, "outputs": {"o_word_data": 160},
                      "parameters": {f"C_LANE_{name}_FILE": "NONE" for name in ("ALPHA", "BETA", "GAMMA", "DELTA")}}
    group_spec = reference.specification("road_yolo_numeric_rom_group", group_contract, [
        "原R1四个PH1P_LOGIC_ERAM输出40位lane；低/高各80位寄存拼接后直接连160位输出。",
        "不恢复已删除的第二级160位寄存器，不推进R2；初始化参数由reader固定14组路径选择。",
        "实测由真实PH1P厂商模型执行；文档不证明实际Slice、ERAM映射或时序。"
    ], [{"name": "i_clk", "wave": "p......"}, {"name": "word_addr", "wave": "=......", "data": ["held A"]},
        {"name": "eram_lane", "wave": "x.=....", "data": ["ROM[A]"]},
        {"name": "registered_pairs", "wave": "x..=...", "data": ["lower/upper"]},
        {"name": "word_data", "wave": "x..=...", "data": ["concatenated pairs"]}])
    group_spec["reset"]["release"] = "Existing asynchronous pair-register reset; vendor ERAM contents are initialization data, not array-reset"
    reference.save(HERE / "spec_input_group.json", group_spec)
    freeze(LUT / "spec_input.json", HERE / "spec_input_service.json")
    print("PACKAGE_PASS lanes=56 words=7168 bytes=143360 padding=2838 old_payload_rejected=true")


def verify_actual(report_path: Path) -> None:
    """从厂商仿真的实际逐词/逐项CSV再独立核对，不重新启动工具。"""
    report_path = report_path.resolve()
    assert report_path.is_relative_to(HERE / "verification/reports")
    proof = json.loads(report_path.read_text(encoding="utf-8"))
    assert proof["status"] == "PASS" and proof["snapshot_unchanged"]
    assert len(proof["tests"]) == 2 and all(item["status"] == "PASS" for item in proof["tests"].values())
    assert all(command["returncode"] == 0 for command in proof["commands"])
    snapshot = report_path.parent / "inputs"
    for rel, expected in proof["closure_sha256"].items():
        assert sha(snapshot / rel) == expected, rel
        if rel.startswith(("rtl/", "artifacts/", "verification/")):
            assert sha(HERE / rel) == expected, rel
    for name, tool in proof["tools"].items():
        assert sha(Path(tool["path"])) == tool["sha256"], name
    physical = (HERE / "artifacts/numeric_test_padded.bin").read_bytes()
    with (report_path.parent / "tb_real_model_rom_reader.csv").open(newline="", encoding="ascii") as stream:
        reader_rows = list(csv.DictReader(stream))
    assert len(reader_rows) == 7168
    actual = bytearray()
    for index, row in enumerate(reader_rows):
        assert int(row["word"]) == index
        assert int(row["latency_cycles"]) == 8
        actual.extend(int(row["data"], 16).to_bytes(20, "little"))
    assert bytes(actual) == physical and hashlib.sha256(actual).hexdigest() == proof["physical_sha256"]
    assert actual[140522:] == bytes(2838)
    with (report_path.parent / "tb_real_model_lut.csv").open(newline="", encoding="ascii") as stream:
        lut_rows = list(csv.DictReader(stream))
    assert len(lut_rows) == 1287
    for position, row in enumerate(lut_rows):
        kind, index, error = (int(row[name]) for name in ("kind", "address", "error"))
        model = int(row["model_id"], 16)
        if position < 1280:
            assert (kind, index) == ((0, position) if position < 1024 else (1, position - 1024))
            assert int(row["tag"], 16) == (0x1000 + index if kind == 0 else 0x4000 + index)
            assert int(row["frame_token"], 16) == (0x20000000 + index if kind == 0 else 0x21000000 + index)
        if error:
            assert model != 0xB35D4A66 or (kind == 1 and index >= 256)
            assert int(row["rom_reads"]) == 0 and int(row["data"], 16) == 0
        else:
            assert model == 0xB35D4A66 and (kind == 0 or index < 256)
            offset = (137962 if kind == 0 else 140010) + 2 * index
            assert int(row["data"], 16) == int.from_bytes(physical[offset:offset + 2], "little")
            assert int(row["latency_cycles"]) == 29 and int(row["rom_reads"]) == 1
    gate_path = HERE / "gates/closure.json"
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    result = {"status": "ACTUAL_VENDOR_ROM_AND_LUT_FUNCTION_PASS_STRICT_OPEN_PHYSICAL_NOT_RUN",
        "actual_simulation_report": str(report_path.relative_to(HERE)), "report_sha256": sha(report_path),
        "package_receipt_sha256": sha(HERE / "package_receipt.json"),
        "actual_readback_words": len(reader_rows), "actual_readback_bytes": len(actual),
        "actual_readback_physical_sha256": hashlib.sha256(actual).hexdigest(),
        "payload_sha256": proof["payload_sha256"], "physical_sha256": proof["physical_sha256"],
        "lut_exhaustive_entries": 1280, "lut_all_trace_rows": len(lut_rows),
        "reader_latency_cycles": 8, "lut_latency_cycles": 29, "cancel_drain_cycles": 8,
        "tools": proof["tools"], "source_input_closure": proof["closure_sha256"],
        "gate_sha256": sha(gate_path), "strict_delivery_ready": gate["delivery_ready"],
        "strict_errors": gate["errors"], "strict_warnings": gate["strict_warnings"], "eight_gates": gate["checks"],
        "real_rom_arbitration": "NOT_CONNECTED", "resource_mapping_timing": "NOT_RUN",
        "whole_network_1fps": "NOT_MEASURED", "expiry_ms_unchanged": 500,
        "no_training_td_bitstream_board_or_production_edit": True}
    (HERE / "final_receipt.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("ACTUAL_CLOSURE_PASS words=7168 bytes=143360 lut_entries=1280 no_new_simulation=true strict_ready=false")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-report", type=Path)
    arguments = parser.parse_args()
    main()
    if arguments.verify_report:
        verify_actual(arguments.verify_report)
