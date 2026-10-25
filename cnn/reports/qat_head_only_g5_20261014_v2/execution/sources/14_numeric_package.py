"""Build the frozen hardware TEST package, never export a trained model implicitly."""
import hashlib
import json
from pathlib import Path
import sys
import zlib

import numpy as np

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
sys.path.insert(0, str(PROJECT))
from cnn.integer import tables
from graph import build_graph


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build_package():
    graph = build_graph()
    rng = np.random.Generator(np.random.PCG64(42))
    payload = bytearray()
    segments = []
    layers = []

    def append(name, role, data, dtype, count):
        offset = len(payload)
        payload.extend(data)
        record = {"name": name, "role": role, "offset": offset,
                  "length": len(data), "dtype": dtype, "count": count,
                  "sha256": digest(data)}
        segments.append(record)
        return offset

    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        name = node["name"]
        channels = node["output_shape_hwc"][2]
        record = {"name": name, "graph_index": node["index"],
                  "output_dtype": node["dtype"], "fields": {}}
        weights = rng.integers(-128, 128, size=node["weights"],
                               dtype=np.int16).astype(np.int8).tobytes()
        fields = [
            ("weights", "weights_int8", weights, "int8", node["weights"]),
            ("bias", "folded_bias_int32", np.zeros(channels, dtype="<i4").tobytes(), "int32_le", channels),
            ("pre_multiplier", "accumulator_to_q7_8_per_channel", np.full(channels, 1 << 16, dtype="<i4").tobytes(), "int32_le", channels),
            ("pre_shift", "accumulator_to_q7_8_per_channel", np.full(channels, 24, dtype=np.uint8).tobytes(), "uint8", channels),
        ]
        if node["dtype"] == "int8":
            fields.extend([
                ("post_multiplier", "silu_to_int8_per_tensor", np.array([1 << 24], dtype="<i4").tobytes(), "int32_le", 1),
                ("post_shift", "silu_to_int8_per_tensor", bytes([31]), "uint8", 1),
            ])
        for field, role, data, dtype, count in fields:
            record["fields"][field] = append(name + "." + field, role, data, dtype, count)
        layers.append(record)

    lut = tables()
    for name, dtype in (("silu", "<i2"), ("sigmoid", "<u2"), ("exp", "<u2")):
        data = np.asarray(lut[name], dtype=dtype)
        append("shared." + name, "shared_lut", data.tobytes(), dtype, len(data))

    assert len(payload) == 140522 and len(layers) == 67
    padded = bytes(payload) + bytes(143360 - len(payload))
    manifest = {"schema_version": 2, "seed": 42,
                "status": "TEST_ONLY_NOT_TRAINED_NOT_ACCURACY_EVIDENCE",
                "graph_source_sha256": graph["source_sha256"],
                "generator_sha256": digest(Path(__file__).read_bytes()),
                "contract_sha256": digest((ROOT / "deployment_contract.json").read_bytes()),
                "payload_bytes": len(payload), "padding_bytes": len(padded) - len(payload),
                "payload_sha256": digest(payload), "physical_sha256": digest(padded),
                "physical_crc32": f"{zlib.crc32(padded) & 0xffffffff:08x}",
                "layout": {"word_bytes": 20, "words_per_group": 512,
                           "groups": 14, "lanes": 4, "lane_bytes": 5},
                "layers": layers, "segments": segments,
                "silu_upper": int(lut["silu_upper"]),
                "sigmoid_upper": int(lut["sigmoid_upper"])}
    return bytes(payload), padded, manifest


def write_package(output=ROOT / "numeric_artifacts"):
    payload, physical, manifest = build_package()
    output.mkdir(parents=True, exist_ok=True)
    (output / "numeric_test.bin").write_bytes(payload)
    (output / "numeric_test_padded.bin").write_bytes(physical)
    (output / "words.dath").write_text("".join(
        physical[start:start + 20][::-1].hex() + "\n"
        for start in range(0, len(physical), 20)), encoding="ascii", newline="\n")
    lane_files = []
    for group in range(14):
        for lane in range(4):
            name = f"group_{group:02d}_lane_{lane}.dath"
            content = "".join(physical[(group * 512 + word) * 20 + lane * 5:
                                      (group * 512 + word) * 20 + lane * 5 + 5][::-1].hex() + "\n"
                              for word in range(512))
            (output / name).write_text(content, encoding="ascii", newline="\n")
            lane_files.append({"name": name, "sha256": digest(content.encode("ascii"))})
    manifest["lane_files"] = lane_files
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in
                      ("status", "payload_bytes", "padding_bytes", "payload_sha256", "physical_crc32")}))
    return manifest


if __name__ == "__main__":
    write_package()
