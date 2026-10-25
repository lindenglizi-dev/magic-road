"""Reconstruct and audit the banked 8192x64 loader program from a real netlist."""
import argparse
import itertools
import re
from pathlib import Path

import run


PROGRAM_WORDS = 8192
WORD_BITS = 64
CONSTANT_ZERO_BITS = list(range(32, 46)) + [59, 63]
DYNAMIC_BITS = [bit for bit in range(WORD_BITS) if bit not in CONSTANT_ZERO_BITS]


def field(text, name):
    match = re.search(r"\." + name + r"\((.*?)\)", text, re.S)
    assert match, ("MISSING_FIELD", name)
    return "".join(match.group(1).split())


def optional_field(text, name, default=None):
    match = re.search(r"\." + name + r"\((.*?)\)", text, re.S)
    return "".join(match.group(1).split()) if match else default


def output_lanes(expression):
    tokens = [token.strip() for token in expression.strip("{}").split(",")]
    connected = [token for token in reversed(tokens) if not token.startswith("open_n")]
    assert all(re.fullmatch(r"\\u_sequence/ramread0_syn_\d+", token) for token in connected), connected
    return connected


def init_content(parameters, prefix, expected_indices):
    values = {
        int(index, 16): int(value, 16)
        for index, value in re.findall(
            r"\." + prefix + r"_([0-9A-F]{2})\(256'h([0-9A-F]+)\)", parameters
        )
    }
    assert set(values) == set(expected_indices), ("BAD_INIT_INDEX_SET", prefix, sorted(values))
    return sum(value << (index * 256) for index, value in values.items())


def metadata_before(text, primitive_start):
    matches = re.findall(r"// address_offset=[^\n]+", text[max(0, primitive_start - 512):primitive_start])
    assert matches, "PROGRAM_METADATA_MISSING"
    values = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", matches[-1])}
    for key in ("address_offset", "data_offset", "depth", "width", "section_size"):
        assert key in values, ("PROGRAM_METADATA_FIELD_MISSING", key)
    return values


def program_cells(text):
    marker = "PH1P_PHY_ERAM_V2 #("
    instance_pattern = re.compile(r"(?P<name>\\u_sequence/ramread0_syn_\d+)\s+\((?P<ports>.*?)\);", re.S)
    cells = []
    for match in instance_pattern.finditer(text):
        primitive_start = text.rfind(marker, 0, match.start())
        assert primitive_start >= 0, ("PROGRAM_PRIMITIVE_MISSING", match.group("name"))
        parameters = text[primitive_start + len(marker):match.start()].rstrip()
        assert parameters.endswith(")"), ("PROGRAM_PARAMETER_BOUNDARY", match.group("name"))
        parameters = parameters[:-1]
        cells.append({
            "name": match.group("name"),
            "parameters": parameters,
            "ports": match.group("ports"),
            "metadata": metadata_before(text, primitive_start),
        })
    assert len(cells) == 20, ("PROGRAM_CELL_COUNT", len(cells))
    return cells


def matches_port(expression, items):
    return re.fullmatch(r"\{" + ",".join(items) + r"\}", expression) is not None


def classify_cell(cell):
    parameters = cell["parameters"]
    ports = cell["ports"]
    meta = cell["metadata"]
    width = int(field(parameters, "DATA_WIDTH_B").strip('"'))
    addrb = field(ports, "addrb")
    csa = field(ports, "csa")
    csb = field(ports, "csb")
    csa_config = tuple(field(parameters, f"CSA{index}") for index in range(3))
    csb_config = tuple(field(parameters, f"CSB{index}") for index in range(3))
    eq38 = re.escape(r"\u_sequence/eq38_syn_33")
    pc12 = re.escape(r"\u_sequence/cnt_program[12]")
    opened = r"open_n\d+"

    if width == 5:
        assert addrb == r"{\u_sequence/cnt_program[11:0],2'b11}", ("BAD_BANK_ADDRESS", cell["name"], addrb)
        if matches_port(csb, (eq38, pc12, opened)):
            bank = "low"
            expected_config = ('"1"', '"INV"', '"INV"')
            expected_offset = 0
            pattern = (eq38, pc12, opened)
        elif matches_port(csb, (eq38, opened, pc12)):
            bank = "high"
            expected_config = ('"SIG"', '"1"', '"INV"')
            expected_offset = 4096
            pattern = (eq38, opened, pc12)
        else:
            raise AssertionError(("BAD_BANK_CHIP_SELECT", cell["name"], csb))
        assert matches_port(csa, pattern), ("CSA_CSB_TOPOLOGY_MISMATCH", cell["name"], csa, csb)
        assert csa_config == expected_config and csb_config == expected_config, (
            "BAD_BANK_CHIP_SELECT_CONFIG", cell["name"], csa_config, csb_config
        )
        assert meta["address_offset"] == expected_offset
        assert meta["depth"] == 4096 and meta["width"] == 5 and meta["section_size"] == 48
        return bank, width, 4096

    assert width == 2, ("BAD_FULL_DEPTH_WIDTH", cell["name"], width)
    assert addrb == r"{\u_sequence/cnt_program,1'b1}", ("BAD_FULL_DEPTH_ADDRESS", cell["name"], addrb)
    pattern = (eq38, opened, opened)
    expected_config = ('"1"', '"1"', '"INV"')
    assert matches_port(csa, pattern) and matches_port(csb, pattern), (
        "BAD_FULL_DEPTH_CHIP_SELECT", cell["name"], csa, csb
    )
    assert csa_config == expected_config and csb_config == expected_config
    assert meta["address_offset"] == 0 and meta["depth"] == 8192 and meta["section_size"] == 48
    assert meta["width"] in (1, 2)
    return "full", width, 8192


def decode_cell(cell):
    bank, width, depth = classify_cell(cell)
    parameters = cell["parameters"]
    ports = cell["ports"]
    data = init_content(parameters, "INIT", range(64))
    main_width = 4 if width == 5 else width
    connected_main = output_lanes(field(ports, "dob"))
    expected_main = 4 if width == 5 else cell["metadata"]["width"]
    assert len(connected_main) == expected_main, ("BAD_DOB_WIDTH", cell["name"], connected_main)
    streams = []
    for lane, net in enumerate(connected_main):
        streams.append((net, [(data >> (address * main_width + lane)) & 1 for address in range(depth)]))
    if width == 5:
        parity = init_content(parameters, "INITP", range(16))
        connected_extra = output_lanes(field(ports, "dob_extra"))
        assert len(connected_extra) == 1, ("BAD_DOB_EXTRA_WIDTH", cell["name"], connected_extra)
        streams.append((connected_extra[0], [(parity >> address) & 1 for address in range(depth)]))
    return bank, streams


def map_lut_blocks(text):
    pattern = re.compile(
        r"AL_MAP_LUT(?P<inputs>\d+)\s*#\((?P<parameters>.*?)\)\s+"
        r"(?P<name>\\\S+)\s+\((?P<ports>.*?)\);", re.S
    )
    blocks = []
    for match in pattern.finditer(text):
        init_match = re.search(r"\.INIT\((\d+)'h([0-9A-Fa-f]+)\)", match.group("parameters"))
        if not init_match:
            continue
        ports = match.group("ports")
        pins = {pin: "".join(value.split()) for pin, value in re.findall(r"\.([a-f])\((.*?)\)", ports, re.S)}
        blocks.append({
            "inputs": int(match.group("inputs")),
            "init": int(init_match.group(2), 16),
            "name": match.group("name"),
            "pins": pins,
            "nets": set(pins.values()),
            "output": field(ports, "o"),
            "start": match.start(),
        })
    return blocks


def lslice_init(parameters, name):
    match = re.search(r"\." + name + r"\(32'([bBhH])([0-9A-Fa-f_]+)\)", parameters)
    if not match:
        return None
    return int(match.group(2).replace("_", ""), 2 if match.group(1).lower() == "b" else 16)


def lslice_lut_blocks(text):
    pattern = re.compile(
        r"PH1P_PHY_LSLICE\s*#\((?P<parameters>.*?)\)\s+"
        r"(?P<name>\\?\S+)\s+\((?P<ports>.*?)\);", re.S
    )
    blocks = []
    for match in pattern.finditer(text):
        parameters = match.group("parameters")
        ports = match.group("ports")
        if optional_field(parameters, "LUTMODE", '"DLUT5"') != '"DLUT5"':
            continue

        def input_net(name):
            return optional_field(ports, name, "1'b1")

        init_a = lslice_init(parameters, "INIT_LUT5A")
        output_a = optional_field(ports, "ofa")
        if init_a is not None and output_a and optional_field(parameters, "OFA_SD", '"QB"') == '"LUT5A"':
            c_source = "ima" if optional_field(parameters, "LUT5A_SD0", '"IC"') == '"IMA"' else "ic"
            e_source = {
                '"IE"': "ie", '"IMF"': "imf", '"FT_LUT5A"': "ft_lut5a"
            }[optional_field(parameters, "LUT5A_SD1", '"IE"')]
            pins = {
                "a": input_net("ia"), "b": input_net("ib"), "c": input_net(c_source),
                "d": input_net("id"), "e": input_net(e_source),
            }
            blocks.append({
                "inputs": 5, "init": init_a, "name": match.group("name") + "/LUT5A",
                "pins": pins, "nets": set(pins.values()), "output": output_a,
                "start": match.start(),
            })

        init_b = lslice_init(parameters, "INIT_LUT5B")
        output_b = optional_field(ports, "ofb")
        if init_b is not None and output_b and optional_field(parameters, "OFB_SD", '"LUTX"') == '"LUTX"':
            d_source = "imb" if optional_field(parameters, "LUT5B_SD2", '"ID"') == '"IMB"' else "id"
            pins = {
                "a": input_net("ia"), "b": input_net("ib"), "c": input_net("ic"),
                "d": input_net(d_source), "e": input_net("ie"),
            }
            blocks.append({
                "inputs": 5, "init": init_b, "name": match.group("name") + "/LUT5B",
                "pins": pins, "nets": set(pins.values()), "output": output_b,
                "start": match.start(),
            })
    return blocks


def is_bank_mux(block, low_net, high_net, select_net):
    inverse = {net: pin for pin, net in block["pins"].items()}
    if low_net not in inverse or high_net not in inverse or select_net not in inverse:
        return False
    low_index = ord(inverse[low_net]) - ord("a")
    high_index = ord(inverse[high_net]) - ord("a")
    pc_index = ord(inverse[select_net]) - ord("a")
    fixed = {
        ord(pin) - ord("a"): int(net[-1])
        for pin, net in block["pins"].items() if net in ("1'b0", "1'b1")
    }
    others = [
        index for index in range(block["inputs"])
        if index not in (low_index, high_index, pc_index) and index not in fixed
    ]
    low_depends = False
    high_depends = False
    for values in itertools.product((0, 1), repeat=len(others)):
        base = [0] * block["inputs"]
        for index, value in fixed.items():
            base[index] = value
        for index, value in zip(others, values):
            base[index] = value

        def output(pc_value, low_value, high_value):
            inputs = base[:]
            inputs[pc_index] = pc_value
            inputs[low_index] = low_value
            inputs[high_index] = high_value
            address = sum(value << index for index, value in enumerate(inputs))
            return (block["init"] >> address) & 1

        if any(output(0, low, 0) != output(0, low, 1) for low in (0, 1)):
            return False
        if any(output(1, 0, high) != output(1, 1, high) for high in (0, 1)):
            return False
        if any(output(0, selected, 0) != output(1, 0, selected) for selected in (0, 1)):
            return False
        low_depends |= output(0, 0, 0) != output(0, 1, 0)
        high_depends |= output(1, 0, 0) != output(1, 0, 1)
    return low_depends and high_depends


def validate_muxes(text, outputs):
    if "AL_MAP_LUT" in text:
        blocks = map_lut_blocks(text)
        primitive = "AL_MAP_LUT"
    else:
        blocks = lslice_lut_blocks(text)
        primitive = "PH1P_PHY_LSLICE"
    assert blocks, "PROGRAM_MUX_PRIMITIVES_MISSING"
    direct_bits = list(range(1, 16)) + list(range(49, 59))
    pair_candidates = []
    select_options = []
    for compressed_bit in range(45):
        logical_bit = DYNAMIC_BITS[compressed_bit]
        low_net = outputs[("low", compressed_bit)]
        high_net = outputs[("high", compressed_bit)]
        candidates = [block for block in blocks if low_net in block["nets"] and high_net in block["nets"]]
        options = {
            net for block in candidates for net in block["nets"] - {low_net, high_net, "1'b0", "1'b1"}
            if is_bank_mux(block, low_net, high_net, net)
        }
        assert options, ("BANK_MUX_SELECT_NOT_FOUND", logical_bit, low_net, high_net)
        pair_candidates.append((logical_bit, low_net, high_net, candidates))
        select_options.append(options)
    common_select = set.intersection(*select_options)
    assert len(common_select) == 1, ("BANK_MUX_SELECT_AMBIGUOUS", sorted(common_select))
    select_net = next(iter(common_select))

    evidence = []
    for logical_bit, low_net, high_net, candidates in pair_candidates:
        matches = [block for block in candidates if is_bank_mux(block, low_net, high_net, select_net)]
        assert matches, ("BANK_MUX_NOT_FOUND", logical_bit, low_net, high_net, select_net)
        if primitive == "AL_MAP_LUT" and logical_bit in direct_bits:
            destination = rf"\u_sequence/reg_command[{logical_bit}]"
            direct = [block for block in matches if block["output"] == destination]
            assert direct, ("DIRECT_REG_COMMAND_MUX_NOT_FOUND", logical_bit, low_net, high_net)
            selected = direct[0]
        else:
            selected = matches[0]
        evidence.append({
            "logical_bit": logical_bit,
            "low_net": low_net,
            "high_net": high_net,
            "lut": selected["name"],
            "output": selected["output"],
            "line": text.count("\n", 0, selected["start"]) + 1,
        })
    return direct_bits if primitive == "AL_MAP_LUT" else [], evidence, primitive, select_net


def validate_expected(words):
    assert len(words) == PROGRAM_WORDS, ("PROGRAM_WORD_COUNT", len(words))
    assert all(0 <= word < (1 << WORD_BITS) for word in words), "PROGRAM_WORD_WIDTH"
    zero_bits = [bit for bit in range(WORD_BITS) if all(((word >> bit) & 1) == 0 for word in words)]
    assert zero_bits == CONSTANT_ZERO_BITS, ("CONSTANT_ZERO_BITS", zero_bits)


def compare_words(actual, expected):
    mismatches = [index for index, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1]]
    assert len(actual) == len(expected) == PROGRAM_WORDS
    assert not mismatches, (
        "PROGRAM_INIT_MISMATCH", mismatches[0], f"{actual[mismatches[0]]:016x}", f"{expected[mismatches[0]]:016x}"
    )


def negative_checks(actual, expected):
    results = {}

    def must_fail(name, action):
        try:
            action()
        except AssertionError:
            results[name] = "caught"
            return
        raise AssertionError(("NEGATIVE_TEST_DID_NOT_FAIL", name))

    bad_constant = expected[:]
    bad_constant[0] |= 1 << CONSTANT_ZERO_BITS[0]
    must_fail("constant_zero_bit", lambda: validate_expected(bad_constant))
    must_fail("truncated_program", lambda: validate_expected(expected[:-1]))
    bad_init = actual[:]
    bad_init[0] ^= 1
    must_fail("init_bit_flip", lambda: compare_words(bad_init, expected))
    banked_mask = sum(1 << DYNAMIC_BITS[index] for index in range(45))
    inverted_bank = [
        (actual[address] & ~banked_mask) | (actual[address ^ 4096] & banked_mask)
        for address in range(PROGRAM_WORDS)
    ]
    must_fail("pc12_bank_inversion", lambda: compare_words(inverted_bank, expected))
    return results


def select_netlist(physical):
    for name in ("routed_netlist.v", "gate_netlist.v"):
        candidate = physical / name
        if candidate.is_file():
            return candidate
    raise AssertionError(("PROGRAM_NETLIST_MISSING", str(physical)))


def audit(physical, expected_path):
    words = [int(line, 16) for line in expected_path.read_text(encoding="utf-8").splitlines()]
    validate_expected(words)
    netlist = select_netlist(physical)
    text = netlist.read_text(encoding="utf-8")
    cells = program_cells(text)
    topology = {}
    outputs = {}
    reconstructed = [0] * PROGRAM_WORDS
    cell_names = []
    for cell in cells:
        bank, streams = decode_cell(cell)
        offset = cell["metadata"]["data_offset"]
        key = (bank, offset)
        assert key not in topology, ("DUPLICATE_PROGRAM_SECTION", key)
        topology[key] = cell["name"]
        cell_names.append(cell["name"])
        base = 4096 if bank == "high" else 0
        for lane, (net, stream) in enumerate(streams):
            compressed_bit = offset + lane
            assert compressed_bit < len(DYNAMIC_BITS), ("PROGRAM_DATA_OFFSET", cell["name"], compressed_bit)
            output_key = (bank, compressed_bit)
            assert output_key not in outputs, ("DUPLICATE_PROGRAM_OUTPUT", output_key)
            outputs[output_key] = net
            logical_bit = DYNAMIC_BITS[compressed_bit]
            for address, value in enumerate(stream):
                reconstructed[base + address] |= value << logical_bit

    offsets = set(range(0, 45, 5))
    assert {offset for bank, offset in topology if bank == "low"} == offsets
    assert {offset for bank, offset in topology if bank == "high"} == offsets
    assert {offset for bank, offset in topology if bank == "full"} == {45, 47}
    assert set(outputs) == (
        {("low", bit) for bit in range(45)}
        | {("high", bit) for bit in range(45)}
        | {("full", bit) for bit in range(45, 48)}
    )
    direct_bits, mux_evidence, mux_primitive, pc_bank_net = validate_muxes(text, outputs)
    for compressed_bit in range(45, 48):
        assert text.count(outputs[("full", compressed_bit)]) >= 3, (
            "FULL_DEPTH_OUTPUT_HAS_NO_CONSUMER", outputs[("full", compressed_bit)]
        )
    compare_words(reconstructed, words)
    negative = negative_checks(reconstructed, words)
    receipt = {
        "passed": True,
        "program_words": PROGRAM_WORDS,
        "word_bits": WORD_BITS,
        "compared_bits": PROGRAM_WORDS * WORD_BITS,
        "expected_sha256": run.sha(expected_path),
        "netlist_sha256": run.sha(netlist),
        "netlist_file": netlist.name,
        "bank_topology": {
            "program_cells": len(cells),
            "banked_4096x5_cells": 18,
            "full_depth_8192x2_cells": 1,
            "full_depth_8192x1_cells": 1,
            "physical_output_planes": len(outputs),
            "logical_dynamic_bits": len(DYNAMIC_BITS),
            "constant_zero_bits": CONSTANT_ZERO_BITS,
            "low_bank_pc12": 0,
            "high_bank_pc12": 1,
            "bank_mux_pairs": len(mux_evidence),
            "bank_mux_primitive": mux_primitive,
            "pc_bank_net": pc_bank_net,
            "direct_reg_command_bits": direct_bits,
            "cells": cell_names,
            "mux_evidence": mux_evidence,
        },
        "boundary": {
            "4095": {"actual": f"{reconstructed[4095]:016x}", "expected": f"{words[4095]:016x}"},
            "4096": {"actual": f"{reconstructed[4096]:016x}", "expected": f"{words[4096]:016x}"},
        },
        "negative_checks": negative,
        "scope": "Actual ERAM INIT/address/CS/DOB and LUT bank mux reconstruction; excludes silicon readback",
    }
    run.save(physical / "program_audit.json", receipt)
    print(
        f"PROGRAM_INIT_PASS words={PROGRAM_WORDS} bits={PROGRAM_WORDS * WORD_BITS} "
        f"cells={len(cells)} netlist={netlist.name}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("physical", type=Path)
    parser.add_argument("--expected", type=Path, default=run.ROOT / "vectors/program.hex")
    arguments = parser.parse_args()
    audit(arguments.physical.resolve(), arguments.expected.resolve())
