"""校验冻结SCHEMA2 TEST包，并生成当前down2的确定性黄金向量。"""
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
LEGACY = ROOT.parent / "rom_down2_prefetch_20261010"
HALOS = ROOT.parent / "runtime_layer_integration_20261009/vectors/dynamic_original"
sys.path.insert(0, str(REPO))
from cnn import integer

STATUS = "TEST_ONLY_NOT_TRAINED_NOT_ACCURACY_EVIDENCE"
PAYLOAD_BYTES = 140522
PADDED_BYTES = 143360
PAYLOAD_SHA256 = "66284020976ae8a6decd841403a27c09b04ce5bbf4c8c6e3073368d8832abd43"
PADDED_SHA256 = "bc04290dd840e78713c0e576e754bd203ea7df88e7991c71dd93de8fdaf13017"
SCENES = ("interior", "edge", "bottom_right")

# name, destination kind, base address, item count, bytes/item, payload offset, dtype
FIELD_SPECS = (
    ("down2.dw.conv.weights", 2, 0, 144, 1, 581, "int8"),
    ("down2.dw.conv.bias", 3, 0, 16, 4, 725, "int32_le"),
    ("down2.pw.conv.weights", 4, 0, 384, 1, 874, "int8"),
    ("down2.pw.conv.bias", 5, 0, 24, 4, 1258, "int32_le"),
    ("down2.dw.conv.pre_multiplier", 6, 0, 16, 4, 789, "int32_le"),
    ("down2.pw.conv.pre_multiplier", 6, 16, 24, 4, 1354, "int32_le"),
    ("down2.dw.conv.pre_shift", 7, 0, 16, 1, 853, "uint8"),
    ("down2.pw.conv.pre_shift", 7, 16, 24, 1, 1450, "uint8"),
    ("down2.dw.conv.post_multiplier", 7, 40, 1, 4, 869, "int32_le"),
    ("down2.pw.conv.post_multiplier", 7, 41, 1, 4, 1474, "int32_le"),
    ("down2.dw.conv.post_shift", 7, 42, 1, 1, 873, "uint8"),
    ("down2.pw.conv.post_shift", 7, 43, 1, 1, 1478, "uint8"),
    ("shared.silu", 0, 0, 1024, 2, 135914, "<i2"),
)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha_bytes(path.read_bytes())


def emit(path, values, bits):
    path.parent.mkdir(parents=True, exist_ok=True)
    mask = (1 << bits) - 1
    path.write_text(
        "".join(f"{int(value) & mask:0{bits // 4}x}\n" for value in np.asarray(values).ravel()),
        encoding="ascii",
    )


def parse_dath(path, item_bytes, expected_items):
    words = path.read_text(encoding="ascii").split()
    assert len(words) == expected_items, (path, len(words), expected_items)
    assert all(len(word) == item_bytes * 2 and re.fullmatch(r"[0-9a-fA-F]+", word) for word in words), path
    return b"".join(int(word, 16).to_bytes(item_bytes, "little") for word in words)


def verify_package():
    artifacts = ROOT / "artifacts"
    manifest_path = artifacts / "manifest.json"
    payload_path = artifacts / "numeric_test.bin"
    padded_path = artifacts / "numeric_test_padded.bin"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload = payload_path.read_bytes()
    padded = padded_path.read_bytes()

    assert manifest["schema_version"] == 2
    assert manifest["status"] == STATUS
    assert manifest["payload_bytes"] == PAYLOAD_BYTES == len(payload)
    assert manifest["padding_bytes"] == PADDED_BYTES - PAYLOAD_BYTES
    assert manifest["payload_sha256"] == PAYLOAD_SHA256 == sha_bytes(payload)
    assert manifest["physical_sha256"] == PADDED_SHA256 == sha_bytes(padded)
    assert len(padded) == PADDED_BYTES and padded[:PAYLOAD_BYTES] == payload
    assert padded[PAYLOAD_BYTES:] == bytes(PADDED_BYTES - PAYLOAD_BYTES)
    assert manifest["layout"] == {
        "word_bytes": 20,
        "words_per_group": 512,
        "groups": 14,
        "lanes": 4,
        "lane_bytes": 5,
    }

    segments = manifest["segments"]
    assert len({segment["name"] for segment in segments}) == len(segments)
    for segment in segments:
        start = segment["offset"]
        end = start + segment["length"]
        assert 0 <= start <= end <= len(payload), segment["name"]
        assert sha_bytes(payload[start:end]) == segment["sha256"], segment["name"]
    ordered = sorted((segment["offset"], segment["offset"] + segment["length"], segment["name"])
                     for segment in segments)
    assert all(left[1] <= right[0] for left, right in zip(ordered, ordered[1:]))

    words = parse_dath(artifacts / "words.dath", 20, 14 * 512)
    assert words == padded
    lane_chunks = {}
    lane_hashes = {}
    for group in range(14):
        for lane in range(4):
            path = artifacts / f"group_{group:02d}_lane_{lane}.dath"
            lane_chunks[group, lane] = parse_dath(path, 5, 512)
            lane_hashes[path.name] = sha_file(path)
    rebuilt = bytearray()
    for group in range(14):
        for word in range(512):
            for lane in range(4):
                chunk = lane_chunks[group, lane]
                rebuilt.extend(chunk[word * 5:(word + 1) * 5])
    assert bytes(rebuilt) == padded
    return manifest, payload, {
        "manifest_sha256": sha_file(manifest_path),
        "payload_sha256": sha_file(payload_path),
        "padded_sha256": sha_file(padded_path),
        "words_dath_sha256": sha_file(artifacts / "words.dath"),
        "lane_sha256": lane_hashes,
        "verified_segment_hashes": len(segments),
    }


def select_fields(manifest, payload):
    segments = {segment["name"]: segment for segment in manifest["segments"]}
    dtype = {"int8": "i1", "int32_le": "<i4", "uint8": "u1", "<i2": "<i2"}
    entries = []
    values = {}
    for name, kind, base, count, size, offset, expected_dtype in FIELD_SPECS:
        segment = segments[name]
        assert (segment["offset"], segment["count"], segment["length"], segment["dtype"]) == (
            offset, count, count * size, expected_dtype)
        data = payload[offset:offset + count * size]
        assert sha_bytes(data) == segment["sha256"]
        values[name] = np.frombuffer(data, dtype=dtype[expected_dtype]).astype(np.int64)
        entries.append({
            "name": name,
            "kind": kind,
            "base": base,
            "items": count,
            "size": size,
            "word": offset // 20,
            "byte": offset % 20,
            "offset": offset,
            "sha256": segment["sha256"],
        })
    assert len(entries) == 13
    assert np.array_equal(values["shared.silu"], integer.tables()["silu"].astype(np.int64))
    return entries, values


def verify_field_table(entries):
    expected = [
        f"4'd{index}: begin dec_word=13'd{entry['word']}; dec_byte=5'd{entry['byte']}; "
        f"dec_items=11'd{entry['items']}; dec_size=3'd{entry['size']}; dec_kind=3'd{entry['kind']}; "
        f"dec_base=11'd{entry['base']}; end"
        for index, entry in enumerate(entries)
    ]
    current_path = ROOT / "rtl/road_down2_parameter_prefetch.v"
    legacy_path = LEGACY / "rtl/road_down2_parameter_prefetch.v"
    current = current_path.read_text(encoding="utf-8")
    legacy = legacy_path.read_text(encoding="utf-8")
    assert sha_file(current_path) == sha_file(legacy_path)
    for line in expected:
        assert current.count(line) == 1, line
    pattern = re.compile(r"4'd\d+: begin dec_word=13'd\d+; dec_byte=5'd\d+; dec_items=11'd\d+; "
                         r"dec_size=3'd\d+; dec_kind=3'd\d+; dec_base=11'd\d+; end")
    assert pattern.findall(current) == expected
    assert pattern.findall(legacy) == expected
    return {
        "field_count": len(expected),
        "current_sha256": sha_file(current_path),
        "legacy_sha256": sha_file(legacy_path),
        "identical_to_legacy": True,
    }


def boot_step(state, *, reset=False, selected=False, pref_valid=False, pref_payload=None,
              core_ready=False, table_valid=False, table_payload=None, table_ready=False,
              pref_done=False, table_loaded=False, fault=False):
    """单项参数保持和所有权切换的逐拍契约；返回下一状态及本拍组合输出。"""
    if reset:
        return {"pending": False, "payload": None, "owner": False, "fault": False}, {
            "pref_ready": False,
            "core_load_valid": False,
            "core_load_payload": None,
            "core_table_valid": False,
            "core_table_payload": None,
            "pref_table_ready": False,
            "external_owner": False,
            "fault": False,
        }
    stopped = state["fault"] or fault
    enabled = selected and not stopped
    outputs = {
        "pref_ready": enabled and not state["pending"] and not state["owner"],
        "core_load_valid": enabled and state["pending"],
        "core_load_payload": state["payload"] if enabled and state["pending"] else None,
        "core_table_valid": enabled and table_valid,
        "core_table_payload": table_payload if enabled and table_valid else None,
        "pref_table_ready": enabled and table_ready,
        "external_owner": enabled and state["owner"],
        "fault": stopped,
    }
    next_state = dict(state)
    if fault:
        next_state["fault"] = True
        next_state["pending"] = False
        next_state["owner"] = False
    elif not state["fault"]:
        if state["pending"] and enabled and core_ready:
            next_state["pending"] = False
            next_state["payload"] = None
        elif pref_valid and outputs["pref_ready"]:
            next_state["pending"] = True
            next_state["payload"] = pref_payload
        if (not state["owner"] and selected and pref_done and not state["pending"]
                and table_loaded):
            next_state["owner"] = True
    return next_state, outputs


def verify_boot_contract():
    tests = []

    def check(name, condition):
        assert condition, name
        tests.append(name)

    empty = {"pending": False, "payload": None, "owner": False, "fault": False}
    payload_a = (2, 17, -9)
    payload_b = (4, 23, 81)
    table = (511, -123)

    state, out = boot_step(empty, selected=True, pref_valid=True, pref_payload=payload_a)
    check("empty_slot_accepts_one_parameter", out["pref_ready"] and state["payload"] == payload_a)
    state, out = boot_step(state, selected=True, pref_valid=True, pref_payload=payload_b)
    check("pending_payload_holds_under_backpressure",
          not out["pref_ready"] and out["core_load_payload"] == payload_a and state["payload"] == payload_a)
    state, out = boot_step(state, selected=True, pref_valid=True, pref_payload=payload_b, core_ready=True)
    check("pop_does_not_replace_on_same_edge",
          out["core_load_payload"] == payload_a and not out["pref_ready"] and not state["pending"])
    state, out = boot_step(state, selected=True, pref_valid=True, pref_payload=payload_b)
    check("replacement_requires_later_edge", out["pref_ready"] and state["payload"] == payload_b)

    _, out = boot_step(empty, selected=True, table_valid=True, table_payload=table, table_ready=False)
    check("table_payload_forwards_during_backpressure",
          out["core_table_valid"] and out["core_table_payload"] == table and not out["pref_table_ready"])
    _, out = boot_step(empty, selected=True, table_valid=True, table_payload=table, table_ready=True)
    check("table_ready_returns_to_prefetch", out["core_table_valid"] and out["pref_table_ready"])
    _, out = boot_step(empty, selected=False, table_valid=True, table_payload=table, table_ready=True)
    check("unselected_path_is_quiet", not any((out["core_table_valid"], out["pref_table_ready"], out["pref_ready"])))

    wait_pref, _ = boot_step(empty, selected=True, table_loaded=True)
    wait_table, _ = boot_step(empty, selected=True, pref_done=True)
    occupied = {"pending": True, "payload": payload_a, "owner": False, "fault": False}
    wait_empty, _ = boot_step(occupied, selected=True, pref_done=True, table_loaded=True)
    check("owner_waits_for_pref_done", not wait_pref["owner"])
    check("owner_waits_for_table_loaded", not wait_table["owner"])
    check("owner_waits_for_empty_parameter_slot", not wait_empty["owner"])
    drained, _ = boot_step(occupied, selected=True, core_ready=True, pref_done=True, table_loaded=True)
    check("drain_edge_does_not_handoff_early", not drained["pending"] and not drained["owner"])
    owned, out = boot_step(drained, selected=True, pref_done=True, table_loaded=True)
    check("owner_handoff_is_registered", not out["external_owner"] and owned["owner"])
    _, out = boot_step(owned, selected=True)
    check("external_owner_opens_after_registered_handoff", out["external_owner"])
    still_owned, out = boot_step(owned, selected=True, pref_valid=True, pref_payload=payload_a)
    check("owner_blocks_later_parameter_acceptance",
          not out["pref_ready"] and not still_owned["pending"] and still_owned["owner"])

    faulted, out = boot_step(owned, selected=True, pref_valid=True, pref_payload=payload_a,
                             table_valid=True, table_payload=table, table_ready=True, fault=True)
    check("fault_immediately_gates_load_table_and_owner",
          out["fault"] and not any((out["pref_ready"], out["core_load_valid"],
                                    out["core_table_valid"], out["external_owner"])))
    check("fault_cancels_owner_valid_state", faulted["fault"] and not faulted["owner"])
    faulted_pending, out = boot_step(occupied, selected=True, fault=True)
    check("fault_cancels_pending_but_payload_bits_are_irrelevant",
          faulted_pending["fault"] and not faulted_pending["pending"]
          and faulted_pending["payload"] == payload_a and not out["core_load_valid"])
    faulted, out = boot_step(faulted, selected=True)
    check("fault_is_sticky_until_reset", faulted["fault"] and out["fault"] and not out["external_owner"])
    reset, out = boot_step(faulted, reset=True, selected=True, pref_valid=True, pref_payload=payload_a)
    check("reset_cancels_pending_owner_and_fault",
          reset == empty and not any((out["pref_ready"], out["core_load_valid"], out["fault"])))
    wrapper_path = ROOT / "rtl/road_rom_current_down2_top.v"
    wrapper_source = wrapper_path.read_text(encoding="utf-8")
    bound_signals = ("reg_pref_kind", "reg_pref_address", "reg_pref_data",
                     "flag_pref_pending", "flag_external_owner")
    assert all(re.search(rf"\b{name}\b", wrapper_source) for name in bound_signals)
    return {
        "pending_depth": 1,
        "pref_ready_rule": "!flag_pref_pending && !flag_external_owner && selected_down2 && !fault",
        "same_edge_replacement": False,
        "table_forwarding": "prefetch_to_existing_core_table_buffer",
        "owner_handoff_rule": "registered_after_pref_done && !flag_pref_pending && table_loaded",
        "fault_state_rule": "fault_clears_pending_and_owner_valid_bits; retained_payload_bits_are_invalid",
        "fault_recovery": "reset_only",
        "wrapper_source_sha256": sha_file(wrapper_path),
        "bound_signals": list(bound_signals),
        "tests": tests,
        "passed": len(tests),
    }


def generate_vectors(entries, values):
    writes = []
    for index, entry in enumerate(entries):
        for item, value in enumerate(values[entry["name"]]):
            writes.append((int(index == 12), entry["kind"], entry["base"] + item, int(value)))
    assert len(writes) == 1676
    assert sum(entry["items"] for entry in entries[:-1]) == 652
    assert entries[-1]["items"] == 1024
    assert sum(entry["size"] * entry["items"] for entry in entries) == 2946
    assert [row[2] for row in writes[-1024:]] == list(range(1024))
    for column, name, bits in ((0, "table", 8), (1, "kind", 8), (2, "address", 16), (3, "data", 32)):
        emit(ROOT / "vectors" / f"{name}.hex", [row[column] for row in writes], bits)

    padded = (ROOT / "artifacts/numeric_test_padded.bin").read_bytes()
    emit(ROOT / "vectors/rom_words.hex",
         [int.from_bytes(padded[offset:offset + 20], "little") for offset in range(0, len(padded), 20)], 160)

    dw_weights = values["down2.dw.conv.weights"].reshape(16, 3, 3)
    pw_weights = values["down2.pw.conv.weights"].reshape(24, 16)
    scene_shapes = {}
    for scene in SCENES:
        source = HALOS / f"{scene}_halo.hex"
        halo = np.array([int(word, 16) for word in source.read_text(encoding="ascii").split()],
                        dtype=np.uint8).view(np.int8).astype(np.int64).reshape(9, 9, 16)
        dw_acc = np.zeros((4, 4, 16), dtype=np.int64)
        for y in range(4):
            for x in range(4):
                dw_acc[y, x] = (np.einsum("hwc,chw->c", halo[y * 2:y * 2 + 3, x * 2:x * 2 + 3],
                                           dw_weights) + values["down2.dw.conv.bias"])
        assert np.all((dw_acc >= -(1 << 31)) & (dw_acc < (1 << 31)))
        dw_pre = integer.requantize(dw_acc, values["down2.dw.conv.pre_multiplier"],
                                    values["down2.dw.conv.pre_shift"], -32768, 32767)
        dw_silu = integer.silu(dw_pre)
        dw_post = integer.requantize(dw_silu, values["down2.dw.conv.post_multiplier"][0],
                                     values["down2.dw.conv.post_shift"][0])
        pw_acc = np.einsum("hwc,oc->hwo", dw_post, pw_weights) + values["down2.pw.conv.bias"]
        assert np.all((pw_acc >= -(1 << 31)) & (pw_acc < (1 << 31)))
        pw_pre = integer.requantize(pw_acc, values["down2.pw.conv.pre_multiplier"],
                                    values["down2.pw.conv.pre_shift"], -32768, 32767)
        pw_silu = integer.silu(pw_pre)
        pw_post = integer.requantize(pw_silu, values["down2.pw.conv.post_multiplier"][0],
                                     values["down2.pw.conv.post_shift"][0])

        arrays = {
            "halo": (halo, 8),
            "dw_acc": (dw_acc, 32),
            "dw_pre": (dw_pre, 16),
            "dw_silu": (dw_silu, 16),
            "dw_post": (dw_post, 8),
            "pw_acc": (pw_acc, 32),
            "pw_pre": (pw_pre, 16),
            "pw_silu": (pw_silu, 16),
            "pw_post": (pw_post, 8),
            "export": (pw_post, 8),
            "output": (pw_post, 8),
        }
        for stage, (array, bits) in arrays.items():
            emit(ROOT / "vectors" / f"{scene}_{stage}.hex", array, bits)
        legacy_stages = np.concatenate((
            np.stack((dw_pre, dw_silu, dw_post), axis=-1).ravel(),
            np.stack((pw_pre, pw_silu, pw_post), axis=-1).ravel(),
        ))
        emit(ROOT / "vectors" / f"{scene}_stages.hex", legacy_stages, 32)
        scene_shapes[scene] = {
            "halo": list(halo.shape),
            "dw_acc_pre_silu_post": [list(array.shape) for array in (dw_acc, dw_pre, dw_silu, dw_post)],
            "pw_acc_pre_silu_post_export": [list(array.shape) for array in (pw_acc, pw_pre, pw_silu, pw_post, pw_post)],
            "halo_source_sha256": sha_file(source),
        }
    return scene_shapes


def verify_legacy_vectors():
    names = ["table.hex", "kind.hex", "address.hex", "data.hex", "rom_words.hex"]
    for scene in SCENES:
        names.extend(f"{scene}_{suffix}.hex" for suffix in ("halo", "dw_acc", "pw_acc", "output", "stages"))
    for name in names:
        assert (ROOT / "vectors" / name).read_bytes() == (LEGACY / "vectors" / name).read_bytes(), name
    return names


def prepare():
    manifest, payload, package_hashes = verify_package()
    entries, values = select_fields(manifest, payload)
    field_table = verify_field_table(entries)
    boot_contract = verify_boot_contract()
    scene_shapes = generate_vectors(entries, values)
    legacy_matches = verify_legacy_vectors()
    vector_hashes = {path.name: sha_file(path) for path in sorted((ROOT / "vectors").glob("*.hex"))}
    receipt = {
        "test_only": True,
        "schema_version": 2,
        "package_status": STATUS,
        "package": package_hashes,
        "fields": entries,
        "field_table": field_table,
        "load_items": 652,
        "table_items": 1024,
        "total_writes": 1676,
        "selected_bytes": 2946,
        "scenes": list(SCENES),
        "scene_shapes": scene_shapes,
        "all_int32_accumulators_legal": True,
        "wrapper_boot_contract": boot_contract,
        "legacy_vector_matches": legacy_matches,
        "legacy_vector_match_count": len(legacy_matches),
        "vector_sha256": vector_hashes,
        "reference_sha256": sha_file(Path(__file__)),
    }
    (ROOT / "reference_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("REFERENCE_PASS", len(entries), len(legacy_matches), boot_contract["passed"], flush=True)


if __name__ == "__main__":
    prepare()
