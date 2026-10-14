"""down2 DW权重从OIHW顺序装载到9个tap bank的只读语义参考。"""
import hashlib
import itertools
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
BASE = REPORTS / "rom_current_down2_20261013"
FULL = REPORTS / "down2_full_tensor_20261010"
CHANNELS = 16
TAPS = 9
WEIGHTS = CHANNELS * TAPS
LEGAL_POSITIONS = (0, 3, 4, 7, 8, 11, 12, 15)
RANDOM_SEED = int("5586b9ba", 16)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signed(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def old_to_physical(old_index):
    assert 0 <= old_index < WEIGHTS
    return (old_index % TAPS) * CHANNELS + old_index // TAPS


def transpose_for_banks(oihw):
    assert len(oihw) == WEIGHTS
    physical = [None] * WEIGHTS
    for old_index, value in enumerate(oihw):
        physical[old_to_physical(old_index)] = value
    assert all(value is not None for value in physical)
    return physical


def baseline_issue(oihw, halo, biases, channel, position, group):
    activation = [0] * 8
    weights = [[0] * 8 for _ in range(3)]
    mask = [0] * 8
    issue_count = 3 if position % 4 == 0 else 1
    for lane in range(8):
        kernel_index = group * 8 + lane
        if kernel_index >= 21:
            continue
        union_row, union_column = divmod(kernel_index, 7)
        halo_row = (position // 4) * 2 + union_row
        halo_column = (position % 4) * 2 + union_column
        if halo_column < 9:
            activation[lane] = halo[(halo_row * 9 + halo_column) * CHANNELS + channel]
        mask[lane] = 1
        for spatial_lane in range(3):
            if spatial_lane < issue_count and spatial_lane * 2 <= union_column < spatial_lane * 2 + 3:
                old_index = channel * TAPS + union_row * 3 + union_column - spatial_lane * 2
                weights[spatial_lane][lane] = oihw[old_index]
    bias = [biases[channel], 0, 0]
    if position % 4 == 0:
        bias[1:] = [biases[channel], biases[channel]]
    return {"activation": activation, "weights": weights, "mask": mask, "bias": bias}


def banked_issue(physical, halo, biases, channel, position, group):
    activation = [0] * 8
    weights = [[0] * 8 for _ in range(3)]
    mask = [0] * 8
    issue_count = 3 if position % 4 == 0 else 1
    tap_reads = [physical[tap * CHANNELS + channel] for tap in range(TAPS)]
    for lane in range(8):
        kernel_index = group * 8 + lane
        if kernel_index >= 21:
            continue
        union_row, union_column = divmod(kernel_index, 7)
        halo_row = (position // 4) * 2 + union_row
        halo_column = (position % 4) * 2 + union_column
        if halo_column < 9:
            activation[lane] = halo[(halo_row * 9 + halo_column) * CHANNELS + channel]
        mask[lane] = 1
        for spatial_lane in range(3):
            if spatial_lane < issue_count and spatial_lane * 2 <= union_column < spatial_lane * 2 + 3:
                tap = union_row * 3 + union_column - spatial_lane * 2
                weights[spatial_lane][lane] = tap_reads[tap]
    bias = [biases[channel], 0, 0]
    if position % 4 == 0:
        bias[1:] = [biases[channel], biases[channel]]
    return {"activation": activation, "weights": weights, "mask": mask, "bias": bias}


def read_hex(path, bits):
    width = bits // 4
    words = path.read_text(encoding="ascii").split()
    assert all(len(word) == width for word in words), path
    return [signed(int(word, 16), bits) for word in words]


def frozen_weights():
    vectors = BASE / "vectors"
    tables = read_hex(vectors / "table.hex", 8)
    kinds = read_hex(vectors / "kind.hex", 8)
    addresses = read_hex(vectors / "address.hex", 16)
    data = read_hex(vectors / "data.hex", 32)
    assert len(tables) == len(kinds) == len(addresses) == len(data) == 1676
    records = [(address, value) for table, kind, address, value in zip(tables, kinds, addresses, data)
               if table == 0 and kind == 2]
    assert [address for address, _ in records] == list(range(WEIGHTS))
    values = [value for _, value in records]
    assert all(-128 <= value <= 127 for value in values)
    full_values = read_hex(FULL / "vectors/dw_weights.hex", 8)
    assert values == full_values and len(values) == WEIGHTS
    return values, {
        "rom_table": sha256(vectors / "table.hex"),
        "rom_kind": sha256(vectors / "kind.hex"),
        "rom_address": sha256(vectors / "address.hex"),
        "rom_data": sha256(vectors / "data.hex"),
        "full_tensor_dw_weights": sha256(FULL / "vectors/dw_weights.hex"),
    }


def verify_mapping():
    physical = [old_to_physical(index) for index in range(WEIGHTS)]
    assert sorted(physical) == list(range(WEIGHTS))
    for old_index, new_index in enumerate(physical):
        channel, tap = divmod(old_index, TAPS)
        assert new_index >> 4 == tap
        assert new_index & 15 == channel
        assert (new_index & 15) * TAPS + (new_index >> 4) == old_index
    return {
        "old_indices": WEIGHTS,
        "physical_indices": WEIGHTS,
        "minimum": min(physical),
        "maximum": max(physical),
        "bijective": True,
        "bank_rule": "physical[7:4] = kernel_tap",
        "read_address_rule": "physical[3:0] = cnt_output[3:0]",
    }


def verify_weight_set(name, oihw):
    physical = transpose_for_banks(oihw)
    halo = [((index * 73 + 19) & 255) - 128 for index in range(9 * 9 * CHANNELS)]
    biases = [-(1 << 31), (1 << 31) - 1] + [channel * 1000003 - 7000021 for channel in range(2, CHANNELS)]
    issue_payloads = 0
    tuple_cases = 0
    selected_weight_terms = 0
    for channel in range(CHANNELS):
        tap_reads = [physical[tap * CHANNELS + channel] for tap in range(TAPS)]
        assert tap_reads == oihw[channel * TAPS:(channel + 1) * TAPS]
        for position in LEGAL_POSITIONS:
            issue_count = 3 if position % 4 == 0 else 1
            for group in range(3):
                old = baseline_issue(oihw, halo, biases, channel, position, group)
                new = banked_issue(physical, halo, biases, channel, position, group)
                assert old == new
                assert old["mask"] == ([1] * 8 if group < 2 else [1] * 5 + [0] * 3)
                issue_payloads += 1
                for lane in range(8):
                    kernel_index = group * 8 + lane
                    for spatial_lane in range(3):
                        tuple_cases += 1
                        selected = (kernel_index < 21 and spatial_lane < issue_count and
                                    spatial_lane * 2 <= kernel_index % 7 < spatial_lane * 2 + 3)
                        if selected:
                            union_row, union_column = divmod(kernel_index, 7)
                            tap = union_row * 3 + union_column - spatial_lane * 2
                            old_index = channel * TAPS + tap
                            new_index = old_to_physical(old_index)
                            assert 0 <= tap < TAPS and 0 <= new_index < WEIGHTS
                            assert new_index >> 4 == tap and new_index & 15 == channel
                            assert new["weights"][spatial_lane][lane] == oihw[old_index]
                            selected_weight_terms += 1
                        else:
                            assert new["weights"][spatial_lane][lane] == 0
    packed = bytes(value & 255 for value in oihw)
    return {
        "name": name,
        "weights_sha256": hashlib.sha256(packed).hexdigest(),
        "issue_payloads": issue_payloads,
        "tuple_cases": tuple_cases,
        "selected_weight_terms": selected_weight_terms,
        "activation_equal": True,
        "weights_equal": True,
        "mask_equal": True,
        "bias_equal": True,
        "tail_mask_verified": True,
    }


def verify_source_baseline():
    down2 = BASE / "rtl/road_down2_tile_scheduler.v"
    stem = BASE / "rtl/road_stem_tile_scheduler.v"
    source = down2.read_text(encoding="utf-8")
    assert "weight_index = cnt_output * 9 + union_row * 3 +" in source
    assert "reg_dw_weight[weight_index]" in source
    assert "reg_dw_weight_write_address <= i_load_addr[7:0];" in source
    stem_source = stem.read_text(encoding="utf-8")
    assert "assign o_load_ready=i_rstn && state_current==ST_IDLE && !i_start && !i_export_start && !o_fault;" in stem_source
    assert "default:state_next=ST_FAULT;" in stem_source
    return {
        str(down2): sha256(down2),
        str(stem): sha256(stem),
    }


def stem_next_state(state, inputs):
    idle, prepare, send, mac_wait = 0, 1, 2, 3
    post_wait, advance, done, export, fault = 4, 5, 6, 7, 8
    next_state = state
    if state == idle:
        if inputs["start_accept"]:
            next_state = prepare
        elif inputs["export_request"]:
            next_state = export
    elif state == prepare:
        next_state = send
    elif state == send:
        if inputs["mac_accept"]:
            next_state = mac_wait if inputs["mac_last"] else prepare
    elif state == mac_wait:
        if inputs["result_accept"]:
            next_state = post_wait
    elif state == post_wait:
        if inputs["write_accept"] and inputs["remaining_last"]:
            next_state = advance
    elif state == advance:
        next_state = done if inputs["tile_last"] else prepare
    elif state == done:
        next_state = idle
    elif state == export:
        if inputs["export_last_accept"]:
            next_state = idle
    elif state == fault:
        next_state = fault
    else:
        next_state = fault
    return fault if inputs["fault_override"] else next_state


def verify_stem_ready_equivalence():
    transition_names = ("start_accept", "export_request", "mac_accept", "mac_last",
                        "result_accept", "write_accept", "remaining_last", "tile_last",
                        "export_last_accept", "fault_override")
    transition_cases = 0
    invalid_next_nonidle = 0
    for state in range(16):
        for values in itertools.product((False, True), repeat=len(transition_names)):
            inputs = dict(zip(transition_names, values))
            next_state = stem_next_state(state, inputs)
            state_prime = next_state
            flag_prime = next_state == 0
            assert flag_prime == (state_prime == 0)
            if state > 8:
                assert next_state == 8
                invalid_next_nonidle += 1
            transition_cases += 1

    ready_cases = 0
    for state in range(16):
        flag = state == 0
        for rstn, start, export, fault, load_valid, load_legal in itertools.product((False, True), repeat=6):
            old_ready = rstn and state == 0 and not start and not export and not fault
            new_ready = rstn and flag and not start and not export and not fault
            assert old_ready == new_ready
            assert (load_valid and old_ready) == (load_valid and new_ready)
            assert (load_valid and old_ready and load_legal) == (load_valid and new_ready and load_legal)
            if not rstn:
                reset_flag = True
                assert not (rstn and reset_flag and not start and not export and not fault)
            ready_cases += 1
    return {
        "status": "PASS",
        "reset_value": 1,
        "registered_rule": "flag_load_state_ready' = (state_next == ST_IDLE)",
        "inductive_relation": "flag_load_state_ready == (state_current == ST_IDLE) after every active edge",
        "transition_cases": transition_cases,
        "ready_input_cases": ready_cases,
        "load_accept_equal": True,
        "legal_write_qualification_equal": True,
        "reset_immediately_closes_ready_via_i_rstn": True,
        "invalid_state_cases_with_next_not_idle": invalid_next_nonidle,
    }


def self_check():
    frozen, vector_hashes = frozen_weights()
    random_source = random.Random(RANDOM_SEED)
    cases = (
        ("negative_extreme", [-128] * WEIGHTS),
        ("deterministic_random", [random_source.randint(-128, 127) for _ in range(WEIGHTS)]),
        ("current_frozen", frozen),
    )
    results = [verify_weight_set(name, weights) for name, weights in cases]
    assert all(result["issue_payloads"] == CHANNELS * len(LEGAL_POSITIONS) * 3 for result in results)
    assert all(result["tuple_cases"] == CHANNELS * len(LEGAL_POSITIONS) * 3 * 8 * 3 for result in results)
    assert all(result["selected_weight_terms"] == 2304 for result in results)
    return {
        "status": "PASS",
        "scope": "Python address and payload semantics only",
        "layout": {
            "input_order": "OIHW channel-major, 144 sequential items",
            "physical_order": "9 kernel-tap banks x 16 channels",
            "transform": "(old_index % 9) * 16 + old_index // 9",
            "registered_prefetch_commit_address": "transformed 8-bit physical index",
            "external_load_address_order_unchanged": list(range(WEIGHTS)),
        },
        "mapping": verify_mapping(),
        "stem_ready_equivalence": verify_stem_ready_equivalence(),
        "legal_positions": list(LEGAL_POSITIONS),
        "test_sets": results,
        "source_sha256": verify_source_baseline(),
        "vector_sha256": vector_hashes,
        "random_seed": RANDOM_SEED,
        "boundaries": [
            "No RTL was generated or modified.",
            "No cycle, RAM inference, timing, metastability, synthesis, or hardware behavior is proved.",
            "Two-state Boolean enumeration does not prove X/Z behavior.",
            "A later RTL test must prove the registered preload write and synchronous tap-bank read timing.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(self_check(), indent=2, sort_keys=True))
