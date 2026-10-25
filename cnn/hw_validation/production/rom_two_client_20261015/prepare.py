"""冻结双客户源/既有G10导出，生成参数golden、仲裁参考和剩余层描述。"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PRODUCTION = HERE.parent
PREVIOUS = PRODUCTION / "rom_lut_real_model_20261015"
LUT = PRODUCTION / "shared_lut_service_1fps_20261015"
R1 = PRODUCTION / "rom_reader_r1_20261015"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_helper(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transition(phase: str, owner: int, prefer: int, address: int, signals: dict) -> tuple:
    """周期控制参考：只在admission锁存，在owner真实返回消费后退休。"""
    param, lut = signals["param_valid"], signals["lut_valid"]
    chosen = prefer if param == lut else int(lut)
    accept = phase == "IDLE" and (lut if chosen else param)
    consume = phase == "WAIT" and signals["response_valid"] and signals["response_ready"][owner]
    if signals.get("reset", False):
        return "IDLE", 0, 0, 0, False, False
    if signals.get("fault", False) or phase == "FAULT":
        return "FAULT", owner, prefer, address, False, False
    if accept:
        return "REQUEST", chosen, 1 - chosen, signals["address"][chosen], True, False
    if phase == "REQUEST" and signals["rom_ready"]:
        return "WAIT", owner, prefer, address, False, False
    if consume:
        return "IDLE", owner, prefer, address, False, True
    return phase, owner, prefer, address, False, False


def reference_test() -> None:
    rng = random.Random(42)
    phase, owner, prefer, address = "IDLE", 0, 0, 0
    admitted, retired = [], []
    for cycle in range(4096):
        signals = {"param_valid": True, "lut_valid": True,
                   "address": (cycle & 8191, (cycle + 177) & 8191), "rom_ready": rng.randrange(4) != 0,
                   "response_valid": rng.randrange(4) != 0, "response_ready": (rng.randrange(4) != 0, rng.randrange(4) != 0)}
        old_phase, old_owner, old_address = phase, owner, address
        phase, owner, prefer, address, accepted, consumed = transition(phase, owner, prefer, address, signals)
        if old_phase != "IDLE":
            assert (owner, address) == (old_owner, old_address)
        if accepted:
            admitted.append(owner)
            assert owner == (len(admitted) - 1) % 2
        if consumed:
            retired.append(owner)
            assert owner == admitted[len(retired) - 1]
    assert len(admitted) > 300 and len(admitted) - len(retired) in (0, 1)
    # 非owner的ready不能消费，即使所有新请求都因客户取消而撤掉。
    for owner in (0, 1):
        signals = {"param_valid": False, "lut_valid": False, "address": (0, 0), "rom_ready": True,
                   "response_valid": True, "response_ready": (owner == 1, owner == 0)}
        assert transition("WAIT", owner, 1 - owner, 91, signals) == ("WAIT", owner, 1 - owner, 91, False, False)
        signals["response_ready"] = (True, True)
        assert transition("WAIT", owner, 1 - owner, 91, signals)[0] == "IDLE"
    save(HERE / "reference/arbiter_receipt.json", {"status": "PASS", "cycles": 4096,
         "admitted": len(admitted), "retired": len(retired), "seed": 42,
         "boundary": "Control semantics only, no synthesis or actual reader cycles"})


def main() -> None:
    required = json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))
    previous_helper = load_helper("real_rom_staging", PREVIOUS / "stage_package.py")
    manifest = json.loads((PREVIOUS / "artifacts/manifest.json").read_text(encoding="utf-8"))
    assert manifest["payload_sha256"] == required["payload_sha256"]
    assert manifest["physical_sha256"] == required["physical_sha256"]
    artifacts = {}
    for path in (PREVIOUS / "artifacts").iterdir():
        if path.is_file():
            artifacts[path.name] = previous_helper.freeze(path, HERE / "artifacts" / path.name)
    assert len(artifacts) == 60 and sha(HERE / "artifacts/numeric_test_padded.bin") == required["physical_sha256"]
    frozen = {}
    for name in ("road_numeric_rom_reader.v", "road_yolo_numeric_rom_group.v", "road_shared_lut_service.v"):
        frozen[name] = previous_helper.freeze(PREVIOUS / "rtl" / name, HERE / "rtl" / name)
    frozen["road_down2_parameter_prefetch.v"] = previous_helper.freeze(R1 / "rtl/road_down2_parameter_prefetch.v", HERE / "rtl/road_down2_parameter_prefetch.v")
    assert frozen["road_down2_parameter_prefetch.v"] == "cd20611a1c9493c5fcbc3f30b0188e8bb3815b7f80b3e14f0fefb64a9511dd80"
    payload = (HERE / "artifacts/numeric_test.bin").read_bytes()
    segments = {segment["name"]: segment for segment in manifest["segments"]}
    # 明确复用原prefetch的13字段范围，不解释成运行时任意层加载。
    fields = [
        ("down2.dw.conv.weights", 2, 0, 29, 1), ("down2.dw.conv.bias", 3, 0, 36, 5),
        ("down2.pw.conv.weights", 4, 0, 43, 14), ("down2.pw.conv.bias", 5, 0, 62, 18),
        ("down2.dw.conv.pre_multiplier", 6, 0, 39, 9), ("down2.pw.conv.pre_multiplier", 6, 16, 67, 14),
        ("down2.dw.conv.pre_shift", 7, 0, 42, 13), ("down2.pw.conv.pre_shift", 7, 16, 72, 10),
        ("down2.dw.conv.post_multiplier", 7, 40, 43, 9), ("down2.pw.conv.post_multiplier", 7, 41, 73, 14),
        ("down2.dw.conv.post_shift", 7, 42, 43, 13), ("down2.pw.conv.post_shift", 7, 43, 73, 18),
        ("shared.silu", 0, 0, 6795, 14)]
    expected = []
    for name, kind, base, word, lane in fields:
        segment = segments[name]
        assert segment["offset"] == word * 20 + lane, name
        size = segment["length"] // segment["count"]
        for index in range(segment["count"]):
            begin = segment["offset"] + size * index
            signed = kind in (2, 3, 4, 5) or name == "shared.silu"
            value = int.from_bytes(payload[begin:begin + size], "little", signed=signed)
            expected.append({"field": name, "is_table": name == "shared.silu", "kind": kind,
                             "address": base + index, "data_u32": value & 0xFFFFFFFF})
    assert len(expected) == 1676 and sum(not row["is_table"] for row in expected) == 652
    save(HERE / "reference/prefetch_expected.json", expected)
    (HERE / "reference/prefetch_expected_47.hex").write_text("".join(
        f"{(int(row['is_table']) << 46) | (row['kind'] << 43) | (row['address'] << 32) | row['data_u32']:012x}\n"
        for row in expected), encoding="ascii")
    for table in ("sigmoid", "exp"):
        segment = segments["shared." + table]
        data = payload[segment["offset"]:segment["offset"] + segment["length"]]
        assert hashlib.sha256(data).hexdigest() == segment["sha256"]
        (HERE / "reference" / (table + "_expected_16.hex")).write_text("".join(
            f"{int.from_bytes(data[index:index + 2], 'little'):04x}\n" for index in range(0, len(data), 2)), encoding="ascii")
    reference_test()
    spec_helper = load_helper("lut_spec_reference", LUT / "reference.py")
    signals = [{"name": "i_clk", "wave": "p........."}, {"name": "param_req_valid", "wave": "01......0."},
               {"name": "lut_req_valid", "wave": "01......0."}, {"name": "client_accept", "wave": "010.....10"},
               {"name": "owner", "wave": "=.......=.", "data": ["PARAM", "LUT"]},
               {"name": "rom_req_valid", "wave": "0.10.....1"}, {"name": "owner_rsp_valid", "wave": "0....1..0."},
               {"name": "owner_rsp_ready", "wave": "0......10."}]
    spec = spec_helper.specification(required["module"], required, [
        required["admission"], required["retirement"], required["round_robin"], required["cancel"], required["fault"]], signals)
    spec["timing_diagrams"][0]["description"] = "客户端接受和物理reader接受分拍；图省略reader实际等待。owner响应保持到消费才允许下一客户，不能以非owner ready释放。"
    save(HERE / "spec_input_arbiter.json", spec)
    lut_contract = json.loads((LUT / "requirements.json").read_text(encoding="utf-8"))
    top = {"inputs": {name: width for name, width in lut_contract["inputs"].items() if not name.startswith("i_rom_")},
           "outputs": {name: width for name, width in lut_contract["outputs"].items() if not name.startswith("o_rom_")}}
    top["inputs"].update({"i_load_ready": 1, "i_table_ready": 1})
    top["outputs"].update({"o_load_valid": 1, "o_load_kind": 3, "o_load_addr": 11, "o_load_data": 32,
                           "o_table_valid": 1, "o_table_addr": 10, "o_table_data": 16, "o_prefetch_done": 1,
                           "o_prefetch_cycles": 32})
    save(HERE / "top_ports.json", top)
    top_spec = spec_helper.specification("road_rom_two_client_top", top, [
        "原prefetch启动即顺序加载down2两层652项及1024SiLU；输出反压不改变已发参数。",
        "动态LUT服务与prefetch通过单事务仲裁访问唯一G10 reader；取消只进LUT服务，所有模块共同复位。",
        "prefetch无ROMfault输入，顶层全局fault必须阻断成功发布并共同复位；不是67层加载器。"
    ], signals)
    save(HERE / "spec_input_top.json", top_spec)
    remaining_layers(manifest)
    save(HERE / "prepare_receipt.json", {"status": "PASS", "payload_sha256": required["payload_sha256"],
        "physical_sha256": required["physical_sha256"], "artifact_hashes": artifacts, "frozen_sources": frozen,
        "prefetch_items": len(expected), "parameters": 652, "silu_items": 1024,
        "prepare_sha256": sha(Path(__file__)), "no_inference_training_or_full_rom_simulation": True})
    print("PREPARE_PASS prefetch_items=1676 params=652 silu=1024 arbiter_reference=PASS descriptors=31")


def remaining_layers(manifest: dict) -> None:
    graph = manifest["graph"]
    assert graph["nodes"] == json.loads((PRODUCTION / "graph_artifacts/graph.json").read_text(encoding="utf-8"))["nodes"]
    assert len([node for node in graph["nodes"] if node["op"] == "conv"]) == 67
    layers = {layer["name"]: layer for layer in manifest["layers"]}
    segments = {segment["name"]: segment for segment in manifest["segments"]}
    result = []
    for node in graph["nodes"]:
        name = node["name"]
        if node["op"] != "conv" or not (name.startswith(("down3.", "down4.", "down3_bu.", "down4_bu.", "head")) or name in {"lateral4.conv", "lateral3.conv"}):
            continue
        family = "head" if name.startswith("head") else ("lateral" if name.startswith("lateral") else "DSDown")
        cin, cout = node["input_shape_hwc"][2], node["output_shape_hwc"][2]
        depthwise = node["groups"] == cin and node["kernel"] == [3, 3]
        notes = ["仅描述，未在本批执行计算/DDR", "原固定down2预取无此层入口，须共享运行时参数描述；不能复制加载/工作RAM"]
        notes.append("DW通道/空间循环适配，不按PW归约Cin" if depthwise else f"PW归约{(cin + 7) // 8}组，尾输入mask按Cin，三输出lane按Cout")
        if node["dtype"] == "int16_q7_8":
            notes.append("预测头INT16，走pre重定标并旁路SiLU/post，不加载不存在的post字段")
            notes.append("cls_out输出2路：最后输出lane mask=0x3；reg_out输出5路：3+2，末mask=0x3；按现7项head顺序合并")
        else:
            notes.append("INT8输出沿原动态pre/SiLU/post")
        if node["output_shape_hwc"][0] % 4:
            notes.append("S16末tile只有两有效行，禁止写y18/19；物理空槽0，卷积越界0")
        fields = []
        for field, offset in layers[name]["fields"].items():
            segment = segments[name + "." + field]
            assert segment["offset"] == offset
            fields.append({"field": field, "byte_offset": offset, "length": segment["length"],
                           "count": segment["count"], "dtype": segment["dtype"], "first_word": offset // 20,
                           "first_byte_lane": offset % 20})
        result.append({"family": family, "name": name, "graph_index": node["index"], "inputs": node["inputs"],
            "input_shape_hwc": node["input_shape_hwc"], "output_shape_hwc": node["output_shape_hwc"],
            "kernel": node["kernel"], "stride": node["stride"], "padding": node["padding"], "groups": node["groups"],
            "dtype": node["dtype"], "macs": node["macs"], "storage": node["storage"], "parameters": fields,
            "pw_input_groups": None if depthwise else (cin + 7) // 8,
            "pw_last_input_lane_mask": None if depthwise else (1 << ((cin - 1) % 8 + 1)) - 1,
            "pw_output_groups": None if depthwise else (cout + 2) // 3,
            "pw_last_output_lane_mask": None if depthwise else (1 << ((cout - 1) % 3 + 1)) - 1,
            "tail_tile_valid_rows": (node["output_shape_hwc"][0] - 1) % 4 + 1,
            "adaptation_notes": notes})
    assert len(result) == 31 and {family: sum(row["family"] == family for row in result) for family in ("DSDown", "lateral", "head")} == {"DSDown": 8, "lateral": 2, "head": 21}
    save(HERE / "remaining_layers.json", {"status": "DESCRIPTORS_ONLY_NOT_EXECUTED", "layers": result,
         "graph_sha256": sha(PRODUCTION / "graph_artifacts/graph.json"), "manifest_sha256": sha(PREVIOUS / "artifacts/manifest.json")})
    with (HERE / "remaining_layers.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["family", "name", "input_HWC", "output_HWC", "kernel", "stride", "groups", "dtype", "parameter_byte_offsets", "adaptation_notes"])
        for row in result:
            writer.writerow([row["family"], row["name"], row["input_shape_hwc"], row["output_shape_hwc"], row["kernel"], row["stride"], row["groups"], row["dtype"],
                             "; ".join(f"{field['field']}={field['byte_offset']}" for field in row["parameters"]), "; ".join(row["adaptation_notes"])])


if __name__ == "__main__":
    main()
