"""固定down2字段映射与整数黄金值；只读取冻结包和已有halo。"""
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[4]))
from cnn import integer


def emit(path, values, bits):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(f"{int(v) & ((1 << bits) - 1):0{bits // 4}x}\n" for v in np.asarray(values).ravel()), encoding="ascii")


def prepare():
    manifest = json.loads((ROOT / "artifacts/manifest.json").read_text(encoding="utf-8"))
    raw = (ROOT / "artifacts/numeric_test_padded.bin").read_bytes()
    fields = {r["name"]: r for r in manifest["segments"]}
    def value(name):
        r = fields[name]
        dtype = {"int8": "i1", "int32_le": "<i4", "uint8": "u1"}.get(r["dtype"], r["dtype"])
        return np.frombuffer(raw[r["offset"]:r["offset"] + r["length"]], dtype=dtype).astype(np.int64)
    entries = []
    for name, kind, base in (("down2.dw.conv.weights", 2, 0), ("down2.dw.conv.bias", 3, 0),
            ("down2.pw.conv.weights", 4, 0), ("down2.pw.conv.bias", 5, 0),
            ("down2.dw.conv.pre_multiplier", 6, 0), ("down2.pw.conv.pre_multiplier", 6, 16),
            ("down2.dw.conv.pre_shift", 7, 0), ("down2.pw.conv.pre_shift", 7, 16),
            ("down2.dw.conv.post_multiplier", 7, 40), ("down2.pw.conv.post_multiplier", 7, 41),
            ("down2.dw.conv.post_shift", 7, 42), ("down2.pw.conv.post_shift", 7, 43),
            ("shared.silu", 0, 0)):
        field = fields[name]
        size = field["length"] // field["count"]
        entries.append({"name": name, "kind": kind, "base": base, "items": field["count"], "size": size,
                        "word": field["offset"] // 20, "byte": field["offset"] % 20, "offset": field["offset"]})
    lines = []
    writes = []
    for idx, e in enumerate(entries):
        lines.append(f"4'd{idx}: begin dec_word=13'd{e['word']}; dec_byte=5'd{e['byte']}; "
                     f"dec_items=11'd{e['items']}; dec_size=3'd{e['size']}; dec_kind=3'd{e['kind']}; "
                     f"dec_base=11'd{e['base']}; end // {e['name']}")
        for n, v in enumerate(value(e["name"])):
            writes.append((int(idx == 12), e["kind"], e["base"] + n, int(v)))
    (ROOT / "rtl/parameter_fields.vh").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # The gate parser does not expand case-item includes. Check the explicit RTL table against the generated contract.
    rtl = (ROOT / "rtl/road_down2_parameter_prefetch.v").read_text(encoding="utf-8")
    for line in lines:
        assert line.split(" // ")[0] in rtl, line
    for column, name, bits in ((0, "table", 8), (1, "kind", 8), (2, "address", 16), (3, "data", 32)):
        emit(ROOT / "vectors" / (name + ".hex"), [r[column] for r in writes], bits)
    emit(ROOT / "vectors/rom_words.hex", [int.from_bytes(raw[n:n+20], "little") for n in range(0, len(raw), 20)], 160)
    original = ROOT.parent / "runtime_layer_integration_20261009/vectors/dynamic_original"
    dw_weights = value("down2.dw.conv.weights").reshape(16, 3, 3)
    pw_weights = value("down2.pw.conv.weights").reshape(24, 16)
    for scene in ("interior", "edge", "bottom_right"):
        halo = np.array([int(x, 16) for x in (original / (scene + "_halo.hex")).read_text().split()], dtype=np.uint8).view(np.int8).astype(np.int64).reshape(9, 9, 16)
        dw_acc = np.zeros((4, 4, 16), dtype=np.int64)
        for y in range(4):
            for x in range(4):
                dw_acc[y, x] = np.einsum("hwc,chw->c", halo[y*2:y*2+3, x*2:x*2+3], dw_weights) + value("down2.dw.conv.bias")
        all_stages = []
        outputs = []
        acc = dw_acc
        for layer in ("down2.dw.conv", "down2.pw.conv"):
            if layer.endswith("pw.conv"):
                acc = np.einsum("hwc,oc->hwo", outputs[0], pw_weights) + value(layer + ".bias")
            assert np.all((acc >= -(1 << 31)) & (acc < (1 << 31)))
            pre = integer.requantize(acc, value(layer + ".pre_multiplier"), value(layer + ".pre_shift"), -32768, 32767)
            active = integer.silu(pre)
            out = integer.requantize(active, value(layer + ".post_multiplier")[0], value(layer + ".post_shift")[0])
            all_stages.extend(np.stack((pre, active, out), axis=-1).ravel())
            outputs.append(out)
            emit(ROOT / "vectors" / (scene + ("_dw_acc.hex" if layer.endswith("dw.conv") else "_pw_acc.hex")), acc, 32)
        emit(ROOT / "vectors" / (scene + "_halo.hex"), halo, 8)
        emit(ROOT / "vectors" / (scene + "_output.hex"), outputs[1], 8)
        emit(ROOT / "vectors" / (scene + "_stages.hex"), all_stages, 32)
    (ROOT / "reference_receipt.json").write_text(json.dumps({"test_only": True, "fields": entries,
        "load_items": len(writes) - 1024, "table_items": 1024, "bytes": sum(e["size"]*e["items"] for e in entries),
        "scenes": ["interior", "edge", "bottom_right"], "all_int32_accumulators_legal": True}, indent=2), encoding="utf-8")
    assert len(writes) == 1676 and sum(e["size"]*e["items"] for e in entries) == 2946
    print("REFERENCE_PASS", len(writes), flush=True)


if __name__ == "__main__":
    prepare()
