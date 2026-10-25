#!/usr/bin/env python3
"""Generate deterministic offline DDR boundary and byte-mask vectors.

This is a software reference only.  It does not model PAXI timing, DDR PHY
behavior, controller reordering, cancellation, or hardware capacity.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[5]
BASE_BYTE_ADDR = 0x03400000
END_BYTE_ADDR = 0x04000000
BLOCK_BYTES = 16
FULL_128 = (1 << 128) - 1

GRAPH_PATH = PROJECT / "cnn/hw_validation/production/graph_artifacts/graph.json"
BRIDGE_PATH = PROJECT / "cnn/hw_validation/ddr/paxi_single_outstanding_bridge.v"
DDR2_PATH = PROJECT / "user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v"
VIDEO_IN_PATH = PROJECT / "user_source/hdl_source/video_in.v"
VIDEO_OUT_PATH = PROJECT / "user_source/hdl_source/video_out.v"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _verilog_parameter(text: str, name: str) -> int | str:
    match = re.search(rf"\.{re.escape(name)}\s*\(\s*(?:\"([^\"]+)\"|(\d+))\s*\)", text)
    if not match:
        raise ValueError(f"missing Verilog parameter {name}")
    return match.group(1) if match.group(1) is not None else int(match.group(2))


def _video_bases(text: str) -> list[int]:
    found = re.findall(r"localparam\s+IMAGE_BASE_ADDR_(\d+)\s*=\s*25'd(\d+)", text)
    if len(found) != 4:
        raise ValueError("expected four video IMAGE_BASE_ADDR values")
    return [value for _, value in sorted((int(index), int(value)) for index, value in found)]


def apply_write_mask(old: int, new: int, mask: int) -> int:
    """Apply the bridge contract: mask bit 1 preserves that little-endian byte lane."""
    if old & ~FULL_128 or new & ~FULL_128 or mask & ~0xFFFF:
        raise ValueError("write values must fit 128 bits and mask must fit 16 bits")
    result = 0
    for lane in range(16):
        source = old if mask & (1 << lane) else new
        result |= ((source >> (8 * lane)) & 0xFF) << (8 * lane)
    return result


def _pattern(address: int, sequence: int) -> int:
    digest = hashlib.sha256(f"ddr:{address:08x}:{sequence}".encode("ascii")).digest()
    return int.from_bytes(digest[:16], "little")


def _build_addresses(graph: dict) -> tuple[list[int], list[int], dict[int, list[str]]]:
    tags: dict[int, list[str]] = {}

    def add(address: int, tag: str) -> None:
        if BASE_BYTE_ADDR <= address < END_BYTE_ADDR and address % BLOCK_BYTES == 0:
            tags.setdefault(address, []).append(tag)

    add(BASE_BYTE_ADDR, "reservation.head")
    add(END_BYTE_ADDR - BLOCK_BYTES, "reservation.tail")

    allocations = []
    for index, slot in enumerate(graph["memory"]["input_slots"]):
        allocations.append((f"input_slot[{index}]", slot["base"], slot["base"] + slot["allocated_bytes"]))
    for node in graph["nodes"]:
        storage = node.get("storage")
        if storage:
            allocations.append((f"storage[{node['index']}]:{node['name']}", storage["base"], storage["end"]))

    for name, begin, end in allocations:
        assert begin % BLOCK_BYTES == 0 and end % BLOCK_BYTES == 0 and begin < end
        assert BASE_BYTE_ADDR <= begin < end <= END_BYTE_ADDR
        add(begin, f"{name}.head")
        add(end - BLOCK_BYTES, f"{name}.tail")
        add(begin - BLOCK_BYTES, f"{name}.before")
        add(end, f"{name}.after")

    # Exercise carry changes at reservation-relative powers of two without
    # exploding the corpus at every 16-byte boundary.
    region_bytes = END_BYTE_ADDR - BASE_BYTE_ADDR
    for bit in range(4, region_bytes.bit_length() + 1):
        boundary = BASE_BYTE_ADDR + (1 << bit)
        if boundary >= END_BYTE_ADDR:
            break
        add(boundary - BLOCK_BYTES, f"relative_pow2[{bit}].before")
        add(boundary, f"relative_pow2[{bit}].after")

    # Also cover absolute MiB-and-larger binary address carries in the window.
    for bit in range(20, 32):
        step = 1 << bit
        boundary = ((BASE_BYTE_ADDR + step - 1) // step) * step
        while boundary < END_BYTE_ADDR:
            if boundary > BASE_BYTE_ADDR:
                add(boundary - BLOCK_BYTES, f"absolute_pow2[{bit}].before")
                add(boundary, f"absolute_pow2[{bit}].after")
            boundary += step

    valid = sorted(tags)
    invalid = [BASE_BYTE_ADDR + low for low in range(1, 16)]
    invalid += [0x00000000, BASE_BYTE_ADDR - BLOCK_BYTES, END_BYTE_ADDR,
                END_BYTE_ADDR + BLOCK_BYTES, 0x07400000, 0x80000000,
                0x83400000, 0xFFFFFFF0]
    invalid = list(dict.fromkeys(invalid))
    assert all(address not in tags for address in invalid)
    assert all(((address >> 1) & ((1 << 25) - 1)) == (BASE_BYTE_ADDR >> 1)
               for address in (0x07400000, 0x83400000))
    assert len(valid) + len(invalid) <= 1024
    return valid, invalid, tags


def _make_audit(graph: dict, valid: list[int], invalid: list[int],
                tags: dict[int, list[str]]) -> dict:
    bridge = BRIDGE_PATH.read_text(encoding="utf-8")
    ddr2 = DDR2_PATH.read_text(encoding="utf-8")
    video_in = VIDEO_IN_PATH.read_text(encoding="utf-8")
    video_out = VIDEO_OUT_PATH.read_text(encoding="utf-8")

    bridge_base = int(re.search(r"BASE_BYTE_ADDR\s*=\s*32'h([0-9a-fA-F]+)", bridge).group(1), 16)
    bridge_last = int(re.search(r"LAST_BYTE_ADDR\s*=\s*32'h([0-9a-fA-F]+)", bridge).group(1), 16)
    assert (bridge_base, bridge_last) == (BASE_BYTE_ADDR, END_BYTE_ADDR - BLOCK_BYTES)
    assert "i_req_byte_addr[25:1]" in bridge
    assert "i_req_byte_addr[3:0] == 4'b0000" in bridge

    ddr_config = {name: _verilog_parameter(ddr2, name) for name in (
        "DX_NUM", "BA_WIDTH", "ROW_WIDTH", "COL_WIDTH", "MC_ADDR_MAP",
        "MC_REORDER", "MC_ADDR_WIDTH", "MC_DATA_WIDTH", "MC_MASK_WIDTH")}
    input_bases = _video_bases(video_in)
    output_bases = _video_bases(video_out)
    assert input_bases == output_bases
    assert "O_ddr_user_addr <= O_ddr_user_addr + 'd8" in video_in
    assert "O_ddr_user_addr <= O_ddr_user_addr + 'd8" in video_out

    frame_bytes = 1280 * 720 * 4
    frame_native_words = frame_bytes // 2
    video_ranges = [{
        "bank": index,
        "native_16bit_word_base": base,
        "byte_range_assuming_720p_32bpp": [base * 2, base * 2 + frame_bytes],
    } for index, base in enumerate(input_bases)]

    storages = [node["storage"] for node in graph["nodes"] if node.get("storage")]
    return {
        "status": "PASS_static_reference_only",
        "boundary": (
            "Static source-derived address/mask audit only; not DDR simulation, RAW ordering, "
            "capacity measurement, timing closure, bitstream, Flash, or board evidence."
        ),
        "source_sha256": {
            str(path.relative_to(PROJECT)).replace("\\", "/"): _sha256(path)
            for path in (Path(__file__), GRAPH_PATH, BRIDGE_PATH, DDR2_PATH, VIDEO_IN_PATH, VIDEO_OUT_PATH)
        },
        "frozen_bridge_contract": {
            "byte_range_half_open": [f"0x{BASE_BYTE_ADDR:08x}", f"0x{END_BYTE_ADDR:08x}"],
            "block_bytes": BLOCK_BYTES,
            "native_address_expression": "byte_addr >> 1",
            "native_address_unit": "16-bit word",
            "data_bits": 128,
            "byte_order": "little; lane 0 is bits [7:0]",
            "mask_semantics": "mask bit 1 preserves (blocks write to) its byte lane",
            "source_sha256": _sha256(BRIDGE_PATH),
        },
        "generated_address_set": {
            "unique_total": len(valid) + len(invalid),
            "valid": len(valid),
            "invalid": len(invalid),
            "limit": 1024,
            "valid_tags": {f"0x{address:08x}": tags[address] for address in valid},
            "invalid_addresses": [f"0x{address:08x}" for address in invalid],
            "high_bit_truncation_aliases_to_0x03400000": ["0x07400000", "0x83400000"],
        },
        "graph": {
            "declared_address_unit": graph["memory"]["address_unit"],
            "reservation_byte_range": [f"0x{BASE_BYTE_ADDR:08x}", f"0x{graph['memory']['arena_end']:08x}"],
            "input_slots": graph["memory"]["input_slots"],
            "actual_storage_allocations": len(storages),
            "actual_storage_byte_range": [
                f"0x{min(item['base'] for item in storages):08x}",
                f"0x{max(item['end'] for item in storages):08x}",
            ],
            "note": "graph byte addresses remain marked unverified_do_not_enable_dma; vectors do not enable DMA",
        },
        "ddr2_generated_ip_configuration": {
            **ddr_config,
            "logical_span_from_MC_ADDR_WIDTH_and_16bit_native_unit_bytes": 1 << (int(ddr_config["MC_ADDR_WIDTH"]) + 1),
            "interpretation_limit": (
                "Values are read from the actual generated PH1P DDR2 wrapper. The logical span is width arithmetic, "
                "not measured board capacity and not proof of controller/DRAM RAW behavior."
            ),
            "vendor_diagram_limit": (
                "No IPUG035 DDR3/DDR4 row-bank diagram is imported as PH1P DDR2 measured mapping; "
                "MC_ADDR_MAP and MC_REORDER are reported exactly as configured."
            ),
        },
        "video_addressing": {
            "source_signal_unit_interpretation": "25-bit native 16-bit-word address",
            "unit_evidence": "bridge maps byte_addr[25:1], while each video 128-bit transfer increments the source address by 8",
            "base_addresses_native_16bit_words": input_bases,
            "base_addresses_bytes": [base * 2 for base in input_bases],
            "increment_per_128bit_transfer_native_words": 8,
            "normal_frame_assumption": {
                "width": 1280,
                "height": 720,
                "bits_per_pixel": 32,
                "frame_bytes": frame_bytes,
                "native_16bit_words": frame_native_words,
                "transfers_128bit": frame_bytes // BLOCK_BYTES,
                "byte_ranges": video_ranges,
            },
            "cnn_reservation_separated_under_assumption": video_ranges[-1]["byte_range_assuming_720p_32bpp"][1] <= BASE_BYTE_ADDR,
            "hard_limit_warning": (
                "The video address RTL resets at frame start and otherwise advances on accepted transfers; "
                "this arithmetic estimate is not proof of a hard full-frame address bound."
            ),
        },
    }


def generate(out_dir: str | Path) -> dict:
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    valid, invalid, tags = _build_addresses(graph)
    catalog = valid + invalid
    slot = {address: index for index, address in enumerate(catalog)}
    memory = {address: 0 for address in valid}
    vectors: list[tuple[int, int, int, int, int, int]] = []

    def emit(op: int, address: int, mask: int, data: int, expected: int) -> None:
        vectors.append((op, address, mask, data & FULL_128, expected & FULL_128, slot[address]))

    alias_rounds = []
    first_round = {address: _pattern(address, 0) for address in valid}
    assert len(set(first_round.values())) == len(valid)
    for round_index in range(2):
        patterns = {
            address: data if round_index == 0 else data ^ FULL_128
            for address, data in first_round.items()
        }
        assert len(set(patterns.values())) == len(valid)
        assert round_index == 0 or all(patterns[address] != first_round[address] for address in valid)
        for address in valid:
            memory[address] = apply_write_mask(memory[address], patterns[address], 0)
            emit(1, address, 0, patterns[address], memory[address])
        for address in reversed(valid):
            emit(0, address, 0, 0, memory[address])
        alias_rounds.append({
            "round": round_index,
            "writes": len(valid),
            "reverse_reads": len(valid),
            "data_relation": "sha256-derived" if round_index == 0 else "bitwise complement of round 0",
        })

    critical = list(dict.fromkeys([
        BASE_BYTE_ADDR,
        graph["memory"]["input_slots"][1]["base"],
        graph["memory"]["feature_begin"],
        END_BYTE_ADDR - BLOCK_BYTES,
    ]))
    special_masks = [("full_mask", 0xFFFF), ("alternating_even", 0xAAAA),
                     ("alternating_odd", 0x5555)]
    special_masks += [(f"single_open_lane_{lane}", 0xFFFF ^ (1 << lane)) for lane in range(16)]
    special_masks += [(f"single_mask_lane_{lane}", 1 << lane) for lane in range(16)]
    lane_masked = [0] * 16
    lane_written = [0] * 16
    special_case_counts = Counter()
    for address in critical:
        for name, mask in special_masks:
            old = memory[address]
            old_bytes = old.to_bytes(16, "little")
            data = old ^ FULL_128
            new_bytes = data.to_bytes(16, "little")
            assert all(old_bytes[lane] != new_bytes[lane] for lane in range(16))
            expected = apply_write_mask(old, data, mask)
            independent = bytes(old_bytes[lane] if mask & (1 << lane) else new_bytes[lane]
                                for lane in range(16))
            assert expected == int.from_bytes(independent, "little")
            memory[address] = expected
            emit(1, address, mask, data, expected)
            emit(0, address, 0, 0, expected)
            special_case_counts[name.split("_lane_")[0]] += 1
            for lane in range(16):
                if mask & (1 << lane):
                    lane_masked[lane] += 1
                else:
                    lane_written[lane] += 1

    memory_before_invalid = memory.copy()
    for address in invalid:
        emit(2, address, 0, 0, 0)
        emit(3, address, 0, _pattern(address, 0xBAD), 0)
    assert memory == memory_before_invalid

    assert set(address & 0xF for address in invalid) >= set(range(1, 16))
    assert all(BASE_BYTE_ADDR <= address < END_BYTE_ADDR and address % BLOCK_BYTES == 0 for address in valid)
    assert lane_masked and min(lane_masked) > 0 and min(lane_written) > 0
    assert len(catalog) == len(set(catalog)) <= 1024

    (out / "addresses.hex").write_text(
        "".join(f"{address:08x}\n" for address in catalog), encoding="ascii")
    (out / "vectors.txt").write_text(
        "".join(f"{op:x} {address:08x} {mask:04x} {data:032x} {expected:032x} {index:08x}\n"
                for op, address, mask, data, expected, index in vectors), encoding="ascii")

    audit = _make_audit(graph, valid, invalid, tags)
    _dump(out / "address_audit.json", audit)
    op_counts = Counter(op for op, *_ in vectors)
    summary = {
        "status": "PASS_reference_only",
        "contract": {
            "vector_fields": ["op", "byte_addr", "mask16", "write_data128", "expected_read128", "slot_index"],
            "op": {"0": "valid_read", "1": "valid_write", "2": "invalid_read", "3": "invalid_write"},
            "mask_bit_1": "preserve byte lane",
            "byte_lane_order": "little endian; lane 0 is write_data128[7:0]",
            "invalid_request": "must be rejected without memory access",
        },
        "counts": {
            "address_slots_total_including_invalid": len(catalog),
            "valid_address_slots": len(valid),
            "invalid_address_slots": len(invalid),
            "vectors": len(vectors),
            "valid_reads": op_counts[0],
            "valid_writes": op_counts[1],
            "invalid_reads": op_counts[2],
            "invalid_writes": op_counts[3],
            "alias_rounds": len(alias_rounds),
            "alias_round_writes": len(valid) * len(alias_rounds),
            "alias_round_reverse_reads": len(valid) * len(alias_rounds),
            "mask_write_read_pairs": len(critical) * len(special_masks),
        },
        "alias_round_details": alias_rounds,
        "mask_lane_coverage": {
            "critical_addresses": [f"0x{address:08x}" for address in critical],
            "write_data_relation": "each new byte lane equals old byte lane XOR 0xff",
            "all_new_bytes_differ_from_old": True,
            "special_case_counts": dict(sorted(special_case_counts.items())),
            "masked_write_occurrences_per_lane": lane_masked,
            "enabled_write_occurrences_per_lane": lane_written,
            "single_open_lanes": list(range(16)),
            "single_masked_lanes": list(range(16)),
        },
        "source_sha256": audit["source_sha256"],
        "generated_sha256": {
            "vectors.txt": _sha256(out / "vectors.txt"),
            "addresses.hex": _sha256(out / "addresses.hex"),
            "address_audit.json": _sha256(out / "address_audit.json"),
        },
        "boundary": audit["boundary"],
    }
    _dump(out / "reference.json", summary)
    return summary


if __name__ == "__main__":
    print(json.dumps(generate(Path(__file__).resolve().parent), indent=2, ensure_ascii=False))
