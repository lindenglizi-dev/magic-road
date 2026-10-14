"""PW48 4x4 小块的Python黄金模型与确定性向量。

只复用 cnn.integer 的部署整数算子；本文件负责冻结包切片、bank 映射和调度分组对拍。
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
ARTIFACTS = (ROOT / "cnn/hw_validation/production/reports"
             / "stem_post_overlap_20261014/artifacts")
MANIFEST_PATH = ARTIFACTS / "manifest.json"
PAYLOAD_PATH = ARTIFACTS / "numeric_test.bin"
CONTRACT_PATH = HERE / "执行契约.txt"

EXPECTED_MANIFEST_SHA256 = "3520e3ca6e82b01b2cbf671630a9d236f7f6096681c69d0d85067c103fcff45d"
EXPECTED_PAYLOAD_SHA256 = "66284020976ae8a6decd841403a27c09b04ce5bbf4c8c6e3073368d8832abd43"
STATUS = "TEST_ONLY_NOT_TRAINED_NOT_ACCURACY_EVIDENCE"

sys.path.insert(0, str(ROOT))
from cnn.integer import conv2d, requantize, silu, tables  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_hex(path: Path, values: np.ndarray, bits: int) -> dict[str, object]:
    data = np.asarray(values).reshape(-1).astype(np.int64)
    if np.any(data < -(1 << (bits - 1))) or np.any(data >= (1 << bits)):
        raise ValueError(f"{path.name}: 数值超出{bits}位容器")
    mask = (1 << bits) - 1
    digits = (bits + 3) // 4
    path.write_text("".join(f"{int(value) & mask:0{digits}x}\n" for value in data),
                    encoding="ascii")
    return {"name": path.name, "count": int(data.size), "bits": bits,
            "sha256": sha256(path)}


def load_segment(manifest: dict, payload: bytes, name: str) -> tuple[np.ndarray, dict]:
    segment = next(item for item in manifest["segments"] if item["name"] == name)
    raw = payload[segment["offset"]:segment["offset"] + segment["length"]]
    if hashlib.sha256(raw).hexdigest() != segment["sha256"]:
        raise AssertionError(f"冻结段哈希不匹配: {name}")
    dtypes = {"int8": np.dtype("i1"), "uint8": np.dtype("u1"),
              "int32_le": np.dtype("<i4"), "<i2": np.dtype("<i2")}
    data = np.frombuffer(raw, dtype=dtypes[segment["dtype"]]).copy()
    if data.size != segment["count"]:
        raise AssertionError(f"冻结段长度不匹配: {name}")
    return data, segment


def package_parameters(manifest: dict, payload: bytes, layer: str) -> tuple[dict, list[dict]]:
    values: dict[str, np.ndarray | int] = {}
    records = []
    for field in ("weights", "bias", "pre_multiplier", "pre_shift",
                  "post_multiplier", "post_shift"):
        data, segment = load_segment(manifest, payload, f"{layer}.{field}")
        values[field] = int(data[0]) if field.startswith("post_") else data
        records.append({key: segment[key] for key in
                        ("name", "offset", "length", "dtype", "count", "sha256")})
    values["weights"] = np.asarray(values["weights"], dtype=np.int8).reshape(48, 48)
    return values, records


def deterministic_input(kind: str) -> np.ndarray:
    position = np.arange(16, dtype=np.int64)[:, None]
    channel = np.arange(48, dtype=np.int64)[None, :]
    if kind == "cls_package":
        values = (position * 37 + channel * 19 + position * channel + 13) % 256 - 128
    elif kind == "reg_package":
        values = (position * 53 - channel * 31 + position * channel * 7 + 91) % 256 - 128
    elif kind == "extrema_channel_scale":
        extrema = np.array([-128, -127, 126, 127], dtype=np.int64)
        values = extrema[(position * 3 + channel) % 4]
    elif kind == "zero_bias_limits":
        values = np.zeros((16, 48), dtype=np.int64)
    else:
        raise ValueError(f"未知case: {kind}")
    return values.astype(np.int8)


def stress_parameters(kind: str) -> dict[str, np.ndarray | int]:
    if kind == "extrema_channel_scale":
        output = np.arange(48, dtype=np.int64)[:, None]
        channel = np.arange(48, dtype=np.int64)[None, :]
        extrema = np.array([-128, -127, 126, 127], dtype=np.int64)
        weights = extrema[(output * 5 + channel * 3) % 4].astype(np.int8)
        bias = ((np.arange(48, dtype=np.int64) - 24) * 50_000).astype(np.int32)
        multipliers = np.array([1, 3, 257, 65_537, 1 << 20, (1 << 30) - 1],
                               dtype=np.int64)
        shifts = np.array([0, 1, 8, 16, 24, 31], dtype=np.uint8)
        return {"weights": weights, "bias": bias,
                "pre_multiplier": np.resize(multipliers, 48),
                "pre_shift": np.resize(shifts, 48),
                "post_multiplier": 1 << 30, "post_shift": 30}
    if kind == "zero_bias_limits":
        limits = np.array([-(1 << 31), -(1 << 31) + 1, -2_147_483_000,
                           -1, 0, 1, 2_147_483_000, (1 << 31) - 2,
                           (1 << 31) - 1], dtype=np.int64)
        return {"weights": np.zeros((48, 48), dtype=np.int8),
                "bias": np.resize(limits, 48).astype(np.int32),
                "pre_multiplier": np.ones(48, dtype=np.int64),
                "pre_shift": np.zeros(48, dtype=np.uint8),
                "post_multiplier": 1, "post_shift": 0}
    raise ValueError(f"未知应力case: {kind}")


def verify_banks(inputs: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    activation_banks = np.empty((8, 96), dtype=np.int8)
    activation_seen = np.zeros((8, 96), dtype=bool)
    for position, channel in np.ndindex(16, 48):
        bank, address = channel % 8, position * 6 + channel // 8
        if activation_seen[bank, address]:
            raise AssertionError("激活bank映射非单射")
        activation_seen[bank, address] = True
        activation_banks[bank, address] = inputs[position, channel]
    weight_banks = np.empty((24, 96), dtype=np.int8)
    weight_seen = np.zeros((24, 96), dtype=bool)
    for output, channel in np.ndindex(48, 48):
        bank = (output % 3) * 8 + channel % 8
        address = (output // 3) * 6 + channel // 8
        if weight_seen[bank, address]:
            raise AssertionError("权重bank映射非单射")
        weight_seen[bank, address] = True
        weight_banks[bank, address] = weights[output, channel]
    if not activation_seen.all() or not weight_seen.all():
        raise AssertionError("bank映射非满射")
    return activation_banks, weight_banks


def golden_case(name: str, parameters: dict[str, np.ndarray | int]) -> tuple[dict, dict]:
    inputs = deterministic_input(name)
    weights = np.asarray(parameters["weights"], dtype=np.int8).reshape(48, 48)
    bias = np.asarray(parameters["bias"])
    pre_multiplier = np.asarray(parameters["pre_multiplier"])
    pre_shift = np.asarray(parameters["pre_shift"])
    post_multiplier = int(parameters["post_multiplier"])
    post_shift = int(parameters["post_shift"])
    if bias.shape != (48,) or pre_multiplier.shape != (48,) or pre_shift.shape != (48,):
        raise AssertionError("参数形状不是PW48")
    if np.any(pre_multiplier < 0) or np.any(pre_multiplier >= (1 << 31)):
        raise AssertionError("pre_multiplier超出uint31")
    if np.any(pre_shift > 62) or not 0 <= post_multiplier < (1 << 31) or not 0 <= post_shift <= 62:
        raise AssertionError("重定标参数越界")

    activation_banks, weight_banks = verify_banks(inputs, weights)
    products = inputs.astype(np.int64)[:, None, :] * weights.astype(np.int64)[None, :, :]
    term_prefix = np.cumsum(products, axis=2) + bias.astype(np.int64)[None, :, None]
    if np.any(term_prefix < -(1 << 32)) or np.any(term_prefix >= (1 << 32)):
        raise AssertionError("48项prefix超出signed33")

    group_matrix = np.empty((16, 16, 6, 3), dtype=np.int64)
    for position, output_group, input_group, lane in np.ndindex(16, 16, 6, 3):
        group_matrix[position, output_group, input_group, lane] = sum(
            int(activation_banks[input_lane, position * 6 + input_group])
            * int(weight_banks[lane * 8 + input_lane, output_group * 6 + input_group])
            for input_lane in range(8))
    expected_groups = products.reshape(16, 16, 3, 6, 8).sum(axis=4).transpose(0, 1, 3, 2)
    if not np.array_equal(group_matrix, expected_groups):
        raise AssertionError("bank分组矩阵与OIHW直接乘积不一致")
    group_prefix = np.cumsum(group_matrix, axis=2) + bias.reshape(16, 3)[None, :, None, :]
    if np.any(group_prefix < -(1 << 32)) or np.any(group_prefix >= (1 << 32)):
        raise AssertionError("6组prefix超出signed33")

    direct = conv2d(inputs.reshape(4, 4, 48), weights.reshape(48, 48, 1, 1),
                    bias).reshape(16, 48)
    grouped = group_prefix[:, :, -1, :].reshape(16, 48)
    if not np.array_equal(grouped, direct):
        raise AssertionError("6x8分组结果与直接1x1卷积不一致")
    if np.any(grouped < -(1 << 31)) or np.any(grouped >= (1 << 31)):
        raise AssertionError("最终累加超出INT32")

    pre = requantize(direct, pre_multiplier, pre_shift, -32768, 32767).astype(np.int16)
    activated = silu(pre)
    post = requantize(activated, post_multiplier, post_shift, -128, 127).astype(np.int8)
    arrays = {"input": inputs.astype(np.int32), "weights": weights, "bias": bias,
              "pre_multiplier": pre_multiplier, "pre_shift": pre_shift,
              "post_params": np.array([post_multiplier, post_shift], dtype=np.int64),
              "acc": direct, "pre": pre, "silu": activated, "post": post}
    checks = {
        "activation_bank_bijection_entries": 8 * 96,
        "weight_bank_bijection_entries": 24 * 96,
        "signed33_term_prefix_values": int(term_prefix.size),
        "signed33_term_prefix_min": int(term_prefix.min()),
        "signed33_term_prefix_max": int(term_prefix.max()),
        "signed33_group_prefix_values": int(group_prefix.size),
        "signed33_group_prefix_min": int(group_prefix.min()),
        "signed33_group_prefix_max": int(group_prefix.max()),
        "group_matrix_values_matched": int(group_matrix.size),
        "final_int32_values": int(direct.size),
        "direct_conv_match": True,
        "requantize_and_silu_from_cnn_integer": True,
    }
    return arrays, checks


def main() -> None:
    if sha256(MANIFEST_PATH) != EXPECTED_MANIFEST_SHA256:
        raise AssertionError("冻结manifest漂移")
    if sha256(PAYLOAD_PATH) != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError("冻结numeric_test.bin漂移")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    payload = PAYLOAD_PATH.read_bytes()
    if manifest["status"] != STATUS or manifest["payload_sha256"] != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError("冻结包状态或payload记录不一致")
    live_graph_hashes = {name: sha256(ROOT / name)
                         for name in manifest["graph_source_sha256"]}
    if live_graph_hashes != manifest["graph_source_sha256"]:
        raise AssertionError("冻结图源码已漂移")

    silu_table, silu_segment = load_segment(manifest, payload, "shared.silu")
    if not np.array_equal(silu_table, tables()["silu"]):
        raise AssertionError("冻结SiLU表与cnn.integer不一致")
    common_file = write_hex(HERE / "silu_table.hex", silu_table, 16)
    common_file.update({"signed": True, "ordering": "address_0_to_1023",
                        "source_segment_sha256": silu_segment["sha256"]})

    cls, cls_segments = package_parameters(manifest, payload, "head2.cls_pw.conv")
    reg, reg_segments = package_parameters(manifest, payload, "head2.reg_pw.conv")
    definitions = [
        ("cls_package", "frozen_test_package", cls, cls_segments,
         "formula: (p*37+c*19+p*c+13)%256-128"),
        ("reg_package", "frozen_test_package", reg, reg_segments,
         "formula: (p*53-c*31+p*c*7+91)%256-128"),
        ("extrema_channel_scale", "synthetic_stress", stress_parameters("extrema_channel_scale"), [],
         "extrema cycle [-128,-127,126,127], index=(3*p+c)%4"),
        ("zero_bias_limits", "synthetic_stress", stress_parameters("zero_bias_limits"), [],
         "all-zero activation and weights; bias includes both INT32 limits"),
    ]
    widths = {"input": 32, "weights": 8, "bias": 32, "pre_multiplier": 32,
              "pre_shift": 8, "post_params": 32, "acc": 32,
              "pre": 16, "silu": 16, "post": 8}
    signed = {"input", "weights", "bias", "acc", "pre", "silu", "post"}
    cases = []
    for case_id, (name, kind, parameters, segments, input_description) in enumerate(definitions):
        arrays, checks = golden_case(name, parameters)
        files = {}
        for field, values in arrays.items():
            record = write_hex(HERE / f"{name}_{field}.hex", values, widths[field])
            record["signed"] = field in signed
            files[field] = record
        cases.append({
            "case_id": case_id,
            "name": name,
            "kind": kind,
            "parameter_source": ("stem_post_overlap_20261014/artifacts/numeric_test.bin"
                                 if kind == "frozen_test_package" else "explicit synthetic boundary values"),
            "input_description": input_description,
            "source_segments": segments,
            "files": files,
            "ranges": {field: {"min": int(np.min(values)), "max": int(np.max(values))}
                       for field, values in arrays.items()},
            "checks": checks,
        })

    receipt = {
        "schema_version": 1,
        "status": STATUS,
        "baseline": {"branch": "work/roadyolo", "contract_commit": "2e872d9c"},
        "sources": {
            "reference.py": sha256(Path(__file__)),
            "execution_contract_sha256": sha256(CONTRACT_PATH),
            "package_manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "numeric_test_bin_sha256": EXPECTED_PAYLOAD_SHA256,
            "package_generator_sha256": manifest["generator_sha256"],
            "package_contract_sha256": manifest["contract_sha256"],
            "frozen_graph_source_sha256": manifest["graph_source_sha256"],
            "live_graph_source_sha256": live_graph_hashes,
        },
        "contract": {
            "shape": {"height": 4, "width": 4, "input_channels": 48,
                      "output_channels": 48},
            "input_layout": "HWC; flat index=position*48+input_channel",
            "weight_layout": "OIHW 48x48x1x1; flat index=output_channel*48+input_channel",
            "output_layout": "HWC; tag=position*48+output_channel",
            "task_order": "position_then_output_group; 256 tasks; 3 outputs per task",
            "reduction": "6 input groups x 8 input lanes",
            "activation_bank": "bank=ic%8,address=position*6+ic//8",
            "weight_bank": "bank=(oc%3)*8+ic%8,address=(oc//3)*6+ic//8",
        },
        "cases": cases,
        "common_files": {"silu_table": common_file},
        "verification": {
            "cases": len(cases),
            "outputs_per_case": 768,
            "tasks_per_case": 256,
            "signed33_term_prefix_values_per_case": 16 * 48 * 48,
            "signed33_group_prefix_values_per_case": 16 * 48 * 6,
            "all_bank_bijections": True,
            "all_group_matrices_match_direct_conv": True,
            "all_final_accumulators_int32": True,
            "no_training_run": True,
            "no_accuracy_claim": True,
        },
    }
    (HERE / "reference_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "cases": [item["name"] for item in cases],
                      "receipt": "reference_receipt.json"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
