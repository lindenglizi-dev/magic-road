"""冻结模型的二字节ROM寻址参考及规格输入生成，不进行推理或训练。"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PACKAGE = ROOT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
HEAD = HERE.parent / "head_decode_topk_rtl_20261015"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate(offset: int) -> tuple[int, int]:
    """与RTL相同的18步除20；另外用Python divmod独立检查。"""
    assert 0 <= offset < (1 << 18)
    quotient = remainder = 0
    for bit in range(17, -1, -1):
        remainder = (remainder << 1) | ((offset >> bit) & 1)
        quotient <<= 1
        if remainder >= 20:
            remainder -= 20
            quotient |= 1
    assert (quotient, remainder) == divmod(offset, 20)
    return quotient, remainder


def fetch(words: list[int], offset: int) -> int:
    word, lane = locate(offset)
    low = (words[word] >> (lane * 8)) & 255
    high = ((words[word + 1] & 255) if lane == 19
            else ((words[word] >> ((lane + 1) * 8)) & 255))
    return low | (high << 8)


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ports(contract: dict) -> list[dict]:
    descriptions = {
        "clk": "统一100MHz上升沿时钟", "rstn": "共同低有效异步复位，本地两级同步释放",
        "cancel": "取消当前查表，已接受的ROM读必须排空后再接新任务",
        "abort": "共同取消本地候选及LUT事务，不代表DDR排空",
        "lut_req_valid": "查表请求有效，等待ready时所有请求字段保持",
        "lut_req_ready": "空闲且无旧ROM在途时允许一次查表传输",
        "lut_req_kind": "0为sigmoid，1为exp", "lut_req_address": "表内索引；exp只允许0至255",
        "lut_req_tag": "16位请求标签，响应原样回显", "lut_req_frame_token": "请求源帧任务标识，响应回显",
        "lut_req_model_id": "绑定完整模型payload的32位模型标识",
        "lut_rsp_valid": "查表完整响应有效，等ready时身份与数据保持",
        "lut_rsp_ready": "本拍允许消费一次完整查表响应", "lut_rsp_kind": "回显已接受请求的表类别",
        "lut_rsp_address": "回显已接受请求的原索引", "lut_rsp_tag": "回显已接受请求的16位标签",
        "lut_rsp_frame_token": "回显源帧标识，禁止旧响应串入新任务", "lut_rsp_model_id": "回显请求模型标识",
        "lut_rsp_data": "从冻结小端ROM字节提取的UINT16值", "lut_rsp_error": "范围/模型/ROM错误，错误数据为零",
        "rom_request_valid": "唯一ROM读口请求有效，等待ready时词地址保持",
        "rom_request_ready": "现有reader允许锁定一个13位物理词地址",
        "rom_request_addr": "20字节物理词号，合法0至7167",
        "rom_response_valid": "reader完整160位响应有效，不携带标签",
        "rom_response_ready": "消费当前ROM读响应；取消排空也必须握手",
        "rom_response_data": "低8位对应物理词第0字节的160位载荷", "rom_fault": "reader粘滞故障，只由共同复位清除",
        "fault": "本组件故障状态，不得发布为成功表",
        "sealed_valid": "所有排序/解码写回完成后封存有效，反压期间保持",
        "sealed_ready": "NMS同时接收源token和两类计数并获得只读所有权",
        "sealed_frame_token": "候选表归属的已锁定任务标识",
        "count_person": "封存的person TopK条数，0至128，包含无效几何条目",
        "count_vehicle": "封存的vehicle TopK条数，0至128，包含无效几何条目",
        "read_req_valid": "NMS单条候选读取请求有效", "read_req_ready": "NMS读取槽空闲时接收请求",
        "read_req_class": "NMS请求的类别地址位", "read_req_index": "类内排序后的0至127槽号",
        "read_rsp_valid": "完整DECODED160记录有效并保持至消费", "read_rsp_ready": "NMS消费完整候选响应",
        "read_rsp_class": "回显读请求类别", "read_rsp_index": "回显读请求槽号",
        "read_rsp_data": "PIF1固定DECODED160记录", "read_rsp_error": "读越界等错误，不发布部分成功结果",
        "finish_valid": "NMS结束并准备释放候选表", "finish_ready": "无未决读时允许释放所有权",
        "finish_frame_token": "必须匹配候选表源token的释放标识",
    }
    result = []
    for key, direction in (("inputs", "input"), ("outputs", "output")):
        for name, width in contract[key].items():
            suffix = name[2:]
            result.append({"name": name, "direction": direction, "width": width,
                           "role": suffix, "clock_domain": "i_clk",
                           "description": descriptions.get(suffix, f"{suffix}：按requirements中对应事务/计数合同使用")})
    return result


def specification(name: str, contract: dict, behavior: list[str], signals: list[dict]) -> dict:
    return {"feature": name, "name": name, "rtl_path": f"rtl/{name}.v",
            "interfaces": {"ports": ports(contract)},
            "clock": {"name": "i_clk", "frequency_hz": 100000000},
            "reset": {"name": "i_rstn", "assert": "async_low", "release": "local_sync_two_flops_or_owner_gating"},
            "parameters": contract.get("parameters", {}), "behavior": behavior,
            "constraints": ["Verilog-2001；一个未决事务；ready/valid握手；无TD/物理时序签核", "不改变冻结算术核/数值，不复制公共存储"],
            "corner_cases": ["复位、取消、背压、非法身份和边界地址；取消不能当成无标签外设已排空"],
            "verification_cases": contract.get("verification", ["11数值向量、protocol、phase_reset，逐项DECODED160对拍"]),
            "timing_diagrams": [{"id": "ownership", "title": "请求所有权与停顿", "scenario": "request-hold-response",
                                 "description": "协议示意：省略内部变长计算，用空白间隔表示；不是固定总时延。仅valid与ready同拍消费。",
                                 "wavejson": {"signal": signals}}]}


def main() -> None:
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    payload = (PACKAGE / "numeric_test.bin").read_bytes()
    physical = (PACKAGE / "numeric_test_padded.bin").read_bytes()
    assert hashlib.sha256(payload).hexdigest() == manifest["payload_sha256"]
    assert hashlib.sha256(physical).hexdigest() == manifest["physical_sha256"]
    assert manifest["layout"]["word_bytes"] == 20 and len(physical) == 143360
    words = [int.from_bytes(physical[n:n + 20], "little") for n in range(0, len(physical), 20)]
    entries = []
    tables = {s["name"]: s for s in manifest["segments"] if s["name"] in {"shared.sigmoid", "shared.exp"}}
    contract = json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))
    for kind, table in enumerate(("shared.sigmoid", "shared.exp")):
        segment = tables[table]
        assert contract["parameters"]["C_SIGMOID_BYTE_OFFSET" if kind == 0 else "C_EXP_BYTE_OFFSET"] == segment["offset"]
        table_bytes = payload[segment["offset"]:segment["offset"] + segment["length"]]
        assert hashlib.sha256(table_bytes).hexdigest() == segment["sha256"]
        for index in range(segment["count"]):
            offset = segment["offset"] + 2 * index
            word, lane = locate(offset)
            value = fetch(words, offset)
            assert value == int.from_bytes(payload[offset:offset + 2], "little")
            entries.append({"kind": kind, "index": index, "byte_offset": offset,
                            "word": word, "lane": lane, "crosses": lane == 19, "expected": value})
    # 独立奇数地址逐字节模式覆盖真实偶数表未触达的跨词路径。
    synthetic = bytes(n & 255 for n in range(400))
    synthetic_words = [int.from_bytes(synthetic[n:n + 20], "little") for n in range(0, 400, 20)]
    for offset in range(399):
        assert fetch(synthetic_words, offset) == int.from_bytes(synthetic[offset:offset + 2], "little")
    save(HERE / "reference/entries.json", entries)
    save(HERE / "reference/receipt.json", {"status": "PASS", "entries": len(entries),
         "physical_words": len(words), "production_crossword_entries": sum(e["crosses"] for e in entries),
         "synthetic_byte_offsets": 399, "manifest_sha256": digest(PACKAGE / "manifest.json"),
         "payload_sha256": digest(PACKAGE / "numeric_test.bin"), "physical_sha256": digest(PACKAGE / "numeric_test_padded.bin"),
         "reference_sha256": digest(Path(__file__)), "no_inference_or_training": True})
    save(HERE / "spec_input.json", specification("road_shared_lut_service", contract, [
        "IDLE接收并锁定所有身份；模型/exp范围错误返回error且不读ROM。18拍除20，注册word和lane。",
        "单个ROM请求等待ready；返回低字节在高lane19时请求相邻词并拼接第二字节，否则单读。",
        "LUT响应身份/数据/error保持至消费；不接第二条查询；ROM fault粘滞到共同复位。",
        "cancel立即屏蔽客户端，已接受的无标签ROM读进入DRAIN，握手丢弃旧返回后才ready；不复位reader。"
    ], [{"name": "i_clk", "wave": "p..........."}, {"name": "lut_req_valid", "wave": "01..0......."},
        {"name": "lut_req_ready", "wave": "0..10......."}, {"name": "rom_req_valid", "wave": "0....1.0...."},
        {"name": "rom_req_ready", "wave": "0......10..."}, {"name": "rom_rsp_valid", "wave": "0.......10.."},
        {"name": "lut_rsp_valid", "wave": "0........1.0"}, {"name": "lut_rsp_ready", "wave": "0.........10"}]))
    head_contract = json.loads((HEAD / "requirements.json").read_text(encoding="utf-8"))
    save(HEAD / "spec_input_head.json", specification("road_head_decode_topk", head_contract, [
        "start锁定token/model；12096个cell严格递增。共享sigmoid、精确RNE分数、每类最小堆Top128。",
        "SCAN/SORT/DECODE互斥占同一候选RAM，堆排序原地，decode写回可见后才SEALED。",
        "seal同时交token与两类count；NMS只能单未决读取DECODED160，finish匹配token才释放。",
        "复位共同取消本地事务；写回完成和读响应消费分别可观察。真实对拍和格式门失败分别记录。"
    ], [{"name": "i_clk", "wave": "p..........."}, {"name": "start_valid", "wave": "010........."},
        {"name": "start_ready", "wave": "01.0........"}, {"name": "sealed_valid", "wave": "0.....1..0.."},
        {"name": "sealed_ready", "wave": "0.......10.."}, {"name": "read_req_valid", "wave": "0........10."},
        {"name": "read_rsp_valid", "wave": "0.........10"}, {"name": "read_rsp_ready", "wave": "0.........10"}]))
    ram_contract = {"inputs": {"i_clk": 1, "i_rstn": 1, "i_cancel": 1, "i_clear_counters": 1,
        "i_req_valid": 1, "i_req_write": 1, "i_req_class": 1, "i_req_index": 7, "i_req_data": 160, "i_rsp_ready": 1},
        "outputs": {"o_req_ready": 1, "o_rsp_valid": 1, "o_rsp_class": 1, "o_rsp_index": 7, "o_rsp_data": 160,
        "o_rsp_error": 1, "o_read_words": 32, "o_write_words": 32}}
    save(HEAD / "spec_input_ram.json", specification("road_candidate_ram", ram_contract, [
        "1024×40bit唯一数组；地址class/index/word，不清数组；单次160bit记录写四拍、同步读八拍。",
        "整条响应回显类别和index，反压保持；消费后才接受下一请求；取消仅控制事务不声称DDR排空。"
    ], [{"name": "i_clk", "wave": "p.........."}, {"name": "req_valid", "wave": "010........"},
        {"name": "req_ready", "wave": "01.0......."}, {"name": "write_word", "wave": "x.====x....", "data": ["0", "1", "2", "3"]},
        {"name": "rsp_valid", "wave": "0.....1..0."}, {"name": "rsp_ready", "wave": "0.......10."}]))
    print("REFERENCE_PASS entries=1280 synthetic_offsets=399 production_crossword=0")


def finalize() -> None:
    """独立复核实际成功收据的源码、数据和工具闭包，不重启仿真。"""
    shared_path = HERE / "verification/reports/final_summary.json"
    head_path = HEAD / "verification/reports/escalated_attempt/summary.json"
    shared = json.loads(shared_path.read_text(encoding="utf-8"))
    head = json.loads(head_path.read_text(encoding="utf-8"))
    assert shared["qualified_run"]["compile_returncode"] == 0
    assert shared["qualified_run"]["simulation_returncode"] == 0
    assert head["compiler_returncode"] == 0 and len(head["results"]) == 13
    assert all(item["passed"] and item["returncode"] == 0 for item in head["results"])
    closure = {}
    for rel, expected in shared["source_sha256"].items():
        assert digest(HERE / rel) == expected, rel
        closure[str((HERE / rel).relative_to(ROOT))] = expected
    for rel, expected in shared["input_sha256"].items():
        assert digest(HERE / "verification" / rel) == expected, rel
        closure[str((HERE / "verification" / rel).relative_to(ROOT))] = expected
    head_sources = {"road_candidate_ram.v": HEAD / "rtl/road_candidate_ram.v",
        "road_head_decode_topk.v": HEAD / "rtl/road_head_decode_topk.v",
        "tb_road_head_decode_topk.v": HEAD / "verification/tb_road_head_decode_topk.v",
        "cases.json": HEAD / "verification/assets/cases.json",
        "sigmoid_lut_16.hex": HEAD / "verification/assets/sigmoid_lut_16.hex",
        "exp_lut_16.hex": HEAD / "verification/assets/exp_lut_16.hex"}
    for name, expected in head["source_sha256"].items():
        assert digest(head_sources[name]) == expected, name
        closure[str(head_sources[name].relative_to(ROOT))] = expected
    cases = json.loads(head_sources["cases.json"].read_text(encoding="utf-8"))
    for case in cases["cases"]:
        for key in ("heads", "decoded160"):
            assert digest(ROOT / case[key]) == case[key + "_sha256"], case["name"]
            closure[case[key]] = case[key + "_sha256"]
    tools = ROOT.parents[1] / ".tools/iverilog/bin"
    for name, expected in shared["tool_sha256"].items():
        assert digest(tools / name) == expected, name
    preserved = {"cnn/integer.py": "441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040",
        "cnn/hw_validation/production/deployment_contract.json": "5cff8d5a406dc235a0d5d35cbf72903c0d6b48477e99a0cabf58251331f3a681",
        "cnn/hw_validation/production/rom_reader_r1_20261015/rtl/road_numeric_rom_reader.v": "d22a4ffec8e3b8536408a117865394c38b8999f7d9bb621ca5ca11e193c79421"}
    for rel, expected in preserved.items():
        assert digest(ROOT / rel) == expected, rel
        closure[rel] = expected
    for path in (HERE / "requirements.json", HERE / "codegen_plan.txt", HERE / "spec_input.json", Path(__file__),
                 HEAD / "requirements.json", HEAD / "codegen_plan.txt", HEAD / "spec_input_head.json", HEAD / "spec_input_ram.json",
                 PACKAGE / "manifest.json", PACKAGE / "numeric_test.bin", PACKAGE / "numeric_test_padded.bin",
                 HERE.parent / "postprocess_golden_2fps_20261015/golden.py",
                 HERE.parent / "postprocess_golden_2fps_20261015/boundary_vectors.json"):
        closure[str(path.relative_to(ROOT))] = digest(path)
    head_gate_path = HEAD / "gates/attempt_01.json"
    shared_gate_path = HERE / "gates/attempt_01.json"
    head_gate = json.loads(head_gate_path.read_text(encoding="utf-8"))
    shared_gate = json.loads(shared_gate_path.read_text(encoding="utf-8"))
    assert not head_gate["delivery_ready"] and not shared_gate["delivery_ready"]
    # 所有测量状态分列；只有真实成功和已验证哈希才进入此收据。
    save(HERE / "final_receipt.json", {"status": "FUNCTIONAL_PASS_STRICT_GATES_OPEN_PHYSICAL_NOT_RUN",
        "shared_qualified_summary_sha256": digest(shared_path), "head_qualified_summary_sha256": digest(head_path),
        "reference_receipt_sha256": digest(HERE / "reference/receipt.json"), "source_input_closure": closure,
        "tool_sha256": shared["tool_sha256"], "shared_metrics": shared["metrics"],
        "head_regression_count": len(head["results"]), "head_real_image_metrics": head["results"][0]["metrics"],
        "strict_gates": {"head": {"sha256": digest(head_gate_path), "errors": head_gate["errors"], "checks": head_gate["checks"]},
                         "shared": {"sha256": digest(shared_gate_path), "errors": shared_gate["errors"], "checks": shared_gate["checks"]}},
        "targets_not_measured": {"fps": 1, "whole_frame_cycles": 100000000, "whole_postprocess_cycles": 2000000,
                                  "candidate_eram": 2, "service_added_eram": 0, "service_added_dsp": 0},
        "expiry_ms_unchanged": 500, "physical_mapping": "NOT_RUN", "real_rom_integration": "C7_NOT_RUN",
        "full_network_board_acceptance": False, "training_started": False})
    print(f"CLOSURE_PASS bound_sources_and_inputs={len(closure)} head_runs=13 shared_queries=2560 strict_delivery_ready=false")


if __name__ == "__main__":
    main()
    if "--finalize" in sys.argv[1:]:
        finalize()
