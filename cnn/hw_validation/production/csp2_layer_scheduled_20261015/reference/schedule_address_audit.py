"""Assert the bounded 72x128 CSP2 schedule, addresses, and lifetimes.

Standard-library only.  This reuses immutable C2 real-road/reference manifests;
it does not regenerate convolution goldens or infer a physical native bus.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parents[1]
PROJECT = ROOT.parents[4]
GRAPH_PATH = PRODUCTION / "graph_artifacts/graph.json"
OLD = PRODUCTION / "csp2_complete_20261015"
OLD_REFERENCE = OLD / "reference"
ROAD_REFERENCE = OLD_REFERENCE / "road_input"
PACKAGE = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
HEIGHT, WIDTH, TILE = 72, 128, 4
TILES = (HEIGHT // TILE) * (WIDTH // TILE)
LEGACY_DIAGNOSTIC_BASE = 0x03600000

STAGE_NAMES = (
    "csp2.blocks.0.dw.conv",
    "csp2.blocks.0.pw.conv",
    "csp2.blocks.1.dw.conv",
    "csp2.blocks.1.pw.conv",
    "csp2.out.conv",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_hashes(base: Path, hashes: dict[str, str]) -> int:
    for relative, expected in hashes.items():
        path = base / relative
        assert path.is_file(), path
        assert sha256(path) == expected, path
    return len(hashes)


def logical_address(storage: dict, y: int, x: int, channel: int) -> int:
    """Frozen graph tile4x4_hwc logical byte address, not a native-bus guess."""
    channels = storage["channels_stored"]
    assert 0 <= y < HEIGHT and 0 <= x < WIDTH and 0 <= channel < channels
    tile = (y // 4) * (WIDTH // 4) + x // 4
    pixel = (y % 4) * 4 + x % 4
    return storage["base"] + (tile * 16 * channels + pixel * channels + channel)


def add_output(coverage: bytearray, digest, y: int, x: int, channel: int,
               channels: int, storage: dict) -> int:
    logical = (y * WIDTH + x) * channels + channel
    assert coverage[logical] == 0, (y, x, channel)
    coverage[logical] = 1
    address = logical_address(storage, y, x, channel)
    digest.update(f"{y},{x},{channel},{address}\n".encode("ascii"))
    return address


def tile_addresses(storage: dict, y0: int, x0: int, channels: range) -> set[int]:
    return {logical_address(storage, y, x, channel)
            for y in range(y0, y0 + 4) for x in range(x0, x0 + 4)
            for channel in channels}


def halo_addresses(storage: dict, y0: int, x0: int, channels: range) -> set[int]:
    return {logical_address(storage, y, x, channel)
            for y in range(max(0, y0 - 1), min(HEIGHT, y0 + 5))
            for x in range(max(0, x0 - 1), min(WIDTH, x0 + 5))
            for channel in channels}


def update_task(digest, values: tuple) -> None:
    digest.update((json.dumps(values, separators=(",", ":")) + "\n").encode("ascii"))


def audit_dw(label: str, input_storage: dict, input_channels: range,
             output_storage: dict) -> dict:
    coverage = bytearray(HEIGHT * WIDTH * 12)
    task_digest = hashlib.sha256()
    output_digest = hashlib.sha256()
    halo_digest = hashlib.sha256()
    task_count = group_count = output_count = input_visits = 0
    cache_bytes = []
    block16_footprints = []
    block16_requests = 0
    last_line = None
    address_min = None
    address_max = None
    normal_tasks = tail_tasks = 0

    for y0 in range(0, HEIGHT, 4):
        for x0 in range(0, WIDTH, 4):
            cached = halo_addresses(input_storage, y0, x0, input_channels)
            used = set()
            for address in sorted(cached):
                halo_digest.update(f"{y0},{x0},{address}\n".encode("ascii"))
            cache_bytes.append(len(cached))
            block16_footprints.append(len({address & ~15 for address in cached}))
            for source_y in range(y0 - 1, y0 + 5):
                for source_x in range(x0 - 1, x0 + 5):
                    for source_channel in input_channels:
                        if not (0 <= source_y < HEIGHT and 0 <= source_x < WIDTH):
                            continue
                        line = logical_address(input_storage, source_y, source_x,
                                               source_channel) & ~15
                        if line != last_line:
                            block16_requests += 1
                            last_line = line

            for row in range(4):
                y = y0 + row
                for group_name, offsets in (("normal3", (0, 1, 2)),
                                            ("tail1", (3,))):
                    for channel in range(12):
                        outputs = [(y, x0 + offset, channel) for offset in offsets]
                        inputs = set()
                        for oy, ox, _channel in outputs:
                            for iy in range(oy - 1, oy + 2):
                                for ix in range(ox - 1, ox + 2):
                                    if 0 <= iy < HEIGHT and 0 <= ix < WIDTH:
                                        inputs.add(logical_address(
                                            input_storage, iy, ix,
                                            input_channels.start + channel))
                        assert len(inputs) <= (15 if group_name == "normal3" else 9)
                        used.update(inputs)
                        input_visits += len(inputs)
                        addresses = []
                        for oy, ox, output_channel in outputs:
                            address = add_output(coverage, output_digest, oy, ox,
                                                 output_channel, 12, output_storage)
                            addresses.append(address)
                            address_min = address if address_min is None else min(address_min, address)
                            address_max = address if address_max is None else max(address_max, address)
                        update_task(task_digest, (y0, x0, row, group_name, channel,
                                                  tuple(sorted(inputs)), tuple(addresses)))
                        task_count += 1
                        group_count += 2  # both 15-slot normal and 9-slot tail need two 8-byte groups
                        output_count += len(outputs)
                        if group_name == "normal3":
                            normal_tasks += 1
                        else:
                            tail_tasks += 1
            assert used == cached, (label, y0, x0)

    assert all(value == 1 for value in coverage)
    assert task_count == 55_296 and normal_tasks == tail_tasks == 27_648
    assert group_count == 110_592 and output_count == 110_592
    assert sum(cache_bytes) == 241_680 and min(cache_bytes) == 300 and max(cache_bytes) == 432
    return {
        "stage": label,
        "kind": "DW3x3_stride1_padding1",
        "tiles": TILES,
        "tasks": task_count,
        "normal3_tasks": normal_tasks,
        "tail1_tasks": tail_tasks,
        "normal3_union": "3x5 per channel, at most 15 bytes, two 8-byte groups",
        "tail1_union": "3x3 per channel, at most 9 bytes, separate task with two 8-byte groups",
        "tail_cache_policy": "this audit reuses the full tile halo; RTL that discards it must reload",
        "eight_byte_groups": group_count,
        "outputs_exactly_once": output_count,
        "output_address_min": address_min,
        "output_address_max": address_max,
        "task_sha256": task_digest.hexdigest(),
        "output_address_sha256": output_digest.hexdigest(),
        "full_halo_address_sha256": halo_digest.hexdigest(),
        "task_union_input_address_visits": input_visits,
        "cache_fill_slots_written": 432 * TILES,
        "cache_fill_inbounds_useful_bytes": sum(cache_bytes),
        "cache_fill_zero_padding_bytes": 432 * TILES - sum(cache_bytes),
        "scalar_one_byte_fill_cycles_model": 432 * TILES,
        "cache_bytes_per_tile_min_max": [min(cache_bytes), max(cache_bytes)],
        "logical_aligned16_unique_block_footprint": sum(block16_footprints),
        "logical_aligned16_block_requests": block16_requests,
        "logical_aligned16_transfer_bytes": 16 * block16_requests,
        "aligned16_model": "one retained line, exact scalar prefetch order; logical addresses only",
    }


def audit_pw(label: str, compute_sources: list[tuple[dict, range]],
             output_storage: dict, output_channels: int,
             bypass: tuple[dict, range] | None = None) -> dict:
    coverage = bytearray(HEIGHT * WIDTH * output_channels)
    task_digest = hashlib.sha256()
    output_digest = hashlib.sha256()
    cache_digest = hashlib.sha256()
    task_count = group_count = output_count = 0
    cache_bytes = []
    block16_footprints = []
    block16_requests = 0
    last_line = None
    address_min = None
    address_max = None
    input_channels = sum(len(channels) for _storage, channels in compute_sources)

    for y0 in range(0, HEIGHT, 4):
        for x0 in range(0, WIDTH, 4):
            cached = set()
            for storage, channels in compute_sources:
                cached.update(tile_addresses(storage, y0, x0, channels))
            if bypass:
                cached.update(tile_addresses(bypass[0], y0, x0, bypass[1]))
            for address in sorted(cached):
                cache_digest.update(f"{y0},{x0},{address}\n".encode("ascii"))
            cache_bytes.append(len(cached))
            block16_footprints.append(len({address & ~15 for address in cached}))
            ordered = []
            if bypass is not None:
                for storage, channels in [*compute_sources, bypass]:
                    ordered.extend(logical_address(storage, y, x, channel)
                                   for y in range(y0, y0 + 4)
                                   for x in range(x0, x0 + 4)
                                   for channel in channels)
            else:
                ordered.extend(logical_address(storage, y, x, channel)
                               for y in range(y0, y0 + 4)
                               for x in range(x0, x0 + 4)
                               for storage, channels in compute_sources
                               for channel in channels)
            assert len(ordered) == 384
            for address in ordered:
                line = address & ~15
                if line != last_line:
                    block16_requests += 1
                    last_line = line

            for row in range(4):
                y = y0 + row
                for column in range(4):
                    x = x0 + column
                    inputs = tuple(logical_address(storage, y, x, channel)
                                   for storage, channels in compute_sources
                                   for channel in channels)
                    for channel0 in range(0, output_channels, 3):
                        output_group = range(channel0, min(channel0 + 3, output_channels))
                        bypass_addresses = () if bypass is None else tuple(
                            logical_address(bypass[0], y, x,
                                            bypass[1].start + channel)
                            for channel in output_group)
                        addresses = []
                        for channel in output_group:
                            address = add_output(coverage, output_digest, y, x, channel,
                                                 output_channels, output_storage)
                            addresses.append(address)
                            address_min = address if address_min is None else min(address_min, address)
                            address_max = address if address_max is None else max(address_max, address)
                        update_task(task_digest, (y0, x0, row, column, channel0,
                                                  inputs, bypass_addresses, tuple(addresses)))
                        task_count += 1
                        group_count += (input_channels + 7) // 8
                        output_count += len(addresses)

    expected_tasks = HEIGHT * WIDTH * ((output_channels + 2) // 3)
    assert all(value == 1 for value in coverage)
    assert task_count == expected_tasks
    assert output_count == HEIGHT * WIDTH * output_channels
    assert min(cache_bytes) == max(cache_bytes) == 384
    return {
        "stage": label,
        "kind": "PW1x1_three_outputs_per_task",
        "tiles": TILES,
        "tasks": task_count,
        "eight_byte_groups": group_count,
        "outputs_exactly_once": output_count,
        "output_address_min": address_min,
        "output_address_max": address_max,
        "task_sha256": task_digest.hexdigest(),
        "output_address_sha256": output_digest.hexdigest(),
        "tile_cache_address_sha256": cache_digest.hexdigest(),
        "cache_fill_slots_written": sum(cache_bytes),
        "cache_fill_inbounds_useful_bytes": sum(cache_bytes),
        "scalar_one_byte_fill_cycles_model": sum(cache_bytes),
        "cache_bytes_per_tile_min_max": [min(cache_bytes), max(cache_bytes)],
        "logical_aligned16_unique_block_footprint": sum(block16_footprints),
        "logical_aligned16_block_requests": block16_requests,
        "logical_aligned16_transfer_bytes": 16 * block16_requests,
        "aligned16_model": "one retained line, exact scalar prefetch order; logical addresses only",
    }


def graph_audit(graph: dict) -> tuple[dict[str, dict], dict]:
    by_name = {node["name"]: node for node in graph["nodes"]}
    source = by_name["down2.pw.conv"]
    stage_nodes = [by_name[name] for name in STAGE_NAMES]
    expected = (
        (0x035B4000, 221_184, 24),
        (0x035EA000, 110_592, 12),
        (0x03605000, 110_592, 12),
        (0x03620000, 110_592, 12),
        (0x0363B000, 110_592, 12),
        (0x03656000, 221_184, 24),
    )
    for node, (base, size, channels) in zip([source, *stage_nodes], expected, strict=True):
        storage = node["storage"]
        assert node["output_shape_hwc"] == [HEIGHT, WIDTH, channels]
        assert (storage["base"], storage["raw_bytes"], storage["channels_stored"]) == (
            base, size, channels)
        assert storage["end"] == base + size and storage["allocated_bytes"] == size
        assert storage["layout"] == "tile4x4_hwc" and storage["bytes_per_element"] == 1

    split = by_name["split.00"]
    residual0 = by_name["residual.00"]
    residual1 = by_name["residual.01"]
    concat = by_name["concat.00"]
    assert split["inputs"] == ["down2.pw.conv"]
    assert split["outputs"] == [
        {"output": "split.00.0", "channel_offset": 0, "channels": 12},
        {"output": "split.00.1", "channel_offset": 12, "channels": 12},
    ]
    assert residual0["storage_alias"] == STAGE_NAMES[1]
    assert residual1["storage_alias"] == STAGE_NAMES[3]
    assert concat["inputs"] == ["split.00.0", "residual.01"]
    assert graph["memory"]["liveness_reuse"] is False

    allocations = []
    for node in graph["nodes"]:
        if "storage" not in node:
            continue
        storage = node["storage"]
        allocations.append({
            "node": node["name"], "op": node["op"], "base": storage["base"],
            "end": storage["end"], "raw_bytes": storage["raw_bytes"],
            "allocated_bytes": storage["allocated_bytes"],
        })
    allocations.sort(key=lambda item: item["base"])
    assert len(allocations) == graph["summary"]["allocations"] == 70
    assert len({item["base"] for item in allocations}) == 70
    assert allocations[0]["base"] == graph["memory"]["feature_begin"]
    assert allocations[-1]["end"] == graph["memory"]["feature_end"]
    for previous, current in zip(allocations, allocations[1:]):
        assert previous["end"] <= current["base"], (previous, current)
    for item in allocations:
        assert item["base"] % graph["memory"]["allocation_alignment"] == 0
        assert item["raw_bytes"] <= item["allocated_bytes"] == item["end"] - item["base"]

    containing = [item for item in allocations
                  if item["base"] <= LEGACY_DIAGNOSTIC_BASE < item["end"]]
    assert len(containing) == 1 and containing[0]["node"] == STAGE_NAMES[0]
    graph_result = {
        "graph_sha256": sha256(GRAPH_PATH),
        "architecture_sha256": graph["architecture_sha256"],
        "address_unit": graph["memory"]["address_unit"],
        "layout": graph["layout"]["name"],
        "allocation_count": len(allocations),
        "allocations_unique_and_nonoverlapping": True,
        "allocations": allocations,
        "legacy_diagnostic_base": LEGACY_DIAGNOSTIC_BASE,
        "legacy_diagnostic_base_overlap": containing[0],
        "legacy_diagnostic_base_allowed_as_independent_scratch": False,
    }
    return {"source": source["storage"],
            **{f"stage{index}": node["storage"] for index, node in enumerate(stage_nodes)}}, graph_result


def reference_audit() -> dict:
    manifest_path = OLD_REFERENCE / "manifest.json"
    road_manifest_path = ROAD_REFERENCE / "manifest.json"
    manifest = load_json(manifest_path)
    road_manifest = load_json(road_manifest_path)
    assert manifest["status"] == "TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED"
    assert manifest["artifact_count"] == len(manifest["artifacts"]) == 230
    assert road_manifest["artifact_count"] == len(road_manifest["artifacts"]) == 65
    assert road_manifest["model_package_copied"] is False
    counts = {
        "old_reference_artifacts": verify_hashes(OLD_REFERENCE, manifest["artifacts"]),
        "old_reference_sources": verify_hashes(PROJECT, manifest["source_files"]),
        "frozen_package_files": verify_hashes(PACKAGE, manifest["package_files"]),
        "real_road_artifacts": verify_hashes(ROAD_REFERENCE, road_manifest["artifacts"]),
        "real_road_sources": verify_hashes(PROJECT, road_manifest["source_sha256"]),
    }
    assert load_json(ROAD_REFERENCE / "status.json")["status"] == "PASS_REAL_IMAGE_C2_LAYOUT_IMPORT"
    return {
        "reuse_only": True,
        "new_convolution_or_golden_generation": False,
        "old_reference_manifest_sha256": sha256(manifest_path),
        "real_road_manifest_sha256": sha256(road_manifest_path),
        "real_road_image_sha256": road_manifest["image_sha256"],
        "package_payload_sha256": manifest["package_payload_sha256"],
        "verified_hash_counts": counts,
    }


def cycle_audit() -> dict:
    ledger_path = OLD / "cycle_ledger.json"
    ledger = load_json(ledger_path)
    interior = ledger["real_road_interior"]
    run = interior["runs"][0]
    states = {item["state"]: item["cycles"] for item in interior["states"]}
    assert len(interior["runs"]) == 1
    assert (run["cycles"], run["reads"], run["groups"], run["tasks"], run["outputs"]) == (
        104_966, 9_504, 1_280, 576, 1_632)
    assert sum(states.values()) == run["cycles"]
    assert states[2] == 1_280 and states[3] == 5_120
    classes = [
        {"class": "corners", "tiles": 4, "cycles_per_representative_tile": 89_874},
        {"class": "top_bottom_noncorner", "tiles": 60, "cycles_per_representative_tile": 95_774},
        {"class": "left_right_noncorner", "tiles": 32, "cycles_per_representative_tile": 97_814},
        {"class": "interior", "tiles": 480, "cycles_per_representative_tile": 104_966},
    ]
    projection = sum(item["tiles"] * item["cycles_per_representative_tile"]
                     for item in classes)
    assert sum(item["tiles"] for item in classes) == TILES and projection == 59_619_664
    return {
        "ledger_sha256": sha256(ledger_path),
        "interior_measured_endpoint": run,
        "mutually_exclusive_state_cycles": states,
        "state_cycles_sum_equals_endpoint_cycles": True,
        "read_transactions_exact": 9_504,
        "parameter_request_state_cycles": 1_280,
        "parameter_request_fraction_of_endpoint": 1_280 / 104_966,
        "parameter_request_plus_wait_fraction_of_endpoint": (1_280 + 5_120) / 104_966,
        "old_full_frame_mechanical_projection": {
            "cycles": projection,
            "tile_classes": classes,
            "measured_full_frame": False,
            "description": "sum of representative per-tile endpoints; not a scheduled full-frame run",
        },
        "new_full_frame_cycle_or_fps_claim": False,
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError("assertions must be enabled")
    graph = load_json(GRAPH_PATH)
    storage, graph_result = graph_audit(graph)
    source_branch0 = (storage["source"], range(0, 12))
    source_branch1 = (storage["source"], range(12, 24))
    residual0 = (storage["stage1"], range(0, 12))
    residual1 = (storage["stage3"], range(0, 12))

    stages = [
        audit_dw("DW0", *source_branch1, storage["stage0"]),
        audit_pw("PW0_residual0", [(storage["stage0"], range(12))],
                 storage["stage1"], 12, source_branch1),
        audit_dw("DW1", *residual0, storage["stage2"]),
        audit_pw("PW1_residual1", [(storage["stage2"], range(12))],
                 storage["stage3"], 12, residual0),
        audit_pw("fuse", [source_branch0, residual1], storage["stage4"], 24),
    ]
    assert [item["tasks"] for item in stages] == [55_296, 36_864, 55_296, 36_864, 73_728]
    assert [item["outputs_exactly_once"] for item in stages] == [
        110_592, 110_592, 110_592, 110_592, 221_184]
    assert sum(item["tasks"] for item in stages) == 258_048
    assert sum(item["eight_byte_groups"] for item in stages) == 589_824
    assert sum(item["outputs_exactly_once"] for item in stages) == 663_552

    lifetimes = [
        {"tensor": "down2.pw.conv", "base": storage["source"]["base"],
         "aliases": ["split.00.0", "split.00.1"],
         "retain_through": "fuse final source-branch read response consumption"},
        {"tensor": STAGE_NAMES[0], "base": storage["stage0"]["base"], "aliases": [],
         "retain_through": "PW0 final input read response consumption"},
        {"tensor": "residual.00", "base": storage["stage1"]["base"],
         "aliases": [STAGE_NAMES[1]],
         "retain_through": "DW1 input and PW1 residual-source final read response consumption"},
        {"tensor": STAGE_NAMES[2], "base": storage["stage2"]["base"], "aliases": [],
         "retain_through": "PW1 final input read response consumption"},
        {"tensor": "residual.01", "base": storage["stage3"]["base"],
         "aliases": [STAGE_NAMES[3]],
         "retain_through": "fuse final residual-branch read response consumption"},
        {"tensor": STAGE_NAMES[4], "base": storage["stage4"]["base"],
         "aliases": ["csp2.fuse.conv semantic name"],
         "retain_through": "final layer visibility barrier, then downstream ownership"},
    ]
    for lifetime, key in zip(lifetimes, ("source", "stage0", "stage1", "stage2", "stage3", "stage4"), strict=True):
        lifetime.update({name: storage[key][name] for name in
                         ("raw_bytes", "allocated_bytes", "end")})

    local_storage = {
        "activation_cache_max_bytes": 432,
        "pw_or_fuse_data_plus_residual_bytes": 384,
        "resident_weight_bytes": 96,
        "resident_weight_derivation": "four 192-bit DW window/group registers",
        "parameter_bits": 248,
        "parameter_bytes_ceil": 31,
        "line_bytes": 16,
        "modeled_max_total_bytes": 432 + 96 + 31 + 16,
        "four_ERAM_raw_capacity_bytes": 10_240,
        "capacity_only_not_synthesis_or_port_proof": True,
        "local_activation_read_port_bits": 8,
        "local_activation_read_bytes_per_cycle": 1,
        "eight_byte_operand_assembly_cycles": 8,
        "assembly_cycles_are_planned_serial_local_reads_not_measured_endpoint": True,
        "excluded_from_capacity_sum": "tags, counters, control, metadata registers, and memory implementation overhead",
    }
    assert local_storage["modeled_max_total_bytes"] <= local_storage["four_ERAM_raw_capacity_bytes"]

    report = {
        "status": "PASS_BOUNDED_CSP2_FULL_STAGE_SCHEDULE_ADDRESS_AUDIT",
        "scope": "Python/graph scheduling and logical-byte address audit only",
        "shape_hwc": [HEIGHT, WIDTH, 24],
        "tile_shape_hw": [4, 4],
        "tiles": TILES,
        "schedule": {
            "stages": stages,
            "tasks_total": 258_048,
            "eight_byte_groups_total": 589_824,
            "outputs_total_exactly_once": 663_552,
        },
        "storage_lifetimes": lifetimes,
        "graph": graph_result,
        "cache_and_ports": local_storage,
        "reused_immutable_reference": reference_audit(),
        "old_cycle_evidence": cycle_audit(),
        "boundaries": {
            "logical_aligned16_cache_model_is_RTL_measurement": False,
            "physical_native_address_or_bus_inferred": False,
            "full_frame_RTL_measured": False,
            "resource_synthesized": False,
            "timing_measured": False,
            "FPS_claimed": False,
            "training_or_golden_generation_or_RTL_or_TB_or_board": False,
        },
        "source_sha256": {
            "schedule_address_audit.py": sha256(Path(__file__)),
            "graph_artifacts/graph.json": sha256(GRAPH_PATH),
            "csp2_complete_20261015/cycle_ledger.json": sha256(OLD / "cycle_ledger.json"),
        },
    }
    output_json = ROOT / "schedule_address_lifetime.json"
    output_txt = ROOT / "schedule_address_lifetime.txt"
    output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        report["status"],
        "scope: Python schedule/logical-byte audit; no new convolution golden, RTL, synthesis, timing, or FPS claim",
        f"frame: {HEIGHT}x{WIDTH}; tiles: {TILES} (18x32)",
        "stage tasks: DW0=55296 PW0=36864 DW1=55296 PW1=36864 fuse=73728; total=258048",
        "stage outputs: 110592,110592,110592,110592,221184; total=663552; each address exactly once",
        "eight-byte groups: DW0=110592 PW0=73728 DW1=110592 PW1=73728 fuse=221184; total=589824",
        "DW cache: useful 300..432 B/tile; PW/fuse data including separate residual/source branch: 384 B/tile",
        "local cache port model: one byte/cycle; eight-byte assembly takes 8 planned cycles (not measured)",
        "local storage upper model: 432+96+31+16=575 B; 4 ERAM raw=10240 B, capacity only; tags/control/overhead excluded",
        f"graph: source=0x{storage['source']['base']:08X}; 70 allocations unique/non-overlapping; address unit remains unverified logical byte",
        "legacy diagnostic 0x03600000 overlaps DW0 [0x035EA000,0x03605000); not independent scratch",
        "lifetime: source retained through fuse; DW intermediates through the next PW; residual0 through DW1/PW1; residual1 through fuse",
        "old measured interior tile: cycles=104966 reads=9504; mutually-exclusive states sum exactly to cycles",
        f"old parameter request state: 1280 cycles ({100 * 1280 / 104966:.6f}%); request+wait={100 * 6400 / 104966:.6f}%",
        "old 59619664-cycle full-frame value is a 4/60/32/480 tile-class mechanical projection, not measurement",
        "immutable prior reference and C2 real-road manifests: all recorded hashes verified; assets reused in place",
    ]
    output_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report["status"])


if __name__ == "__main__":
    main()
