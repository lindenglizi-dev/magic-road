"""Real QAT-G10 first-three-layer vectors using unchanged four-tile format."""
from collections import defaultdict
import hashlib
import importlib.util
from pathlib import Path
import json
import shutil
import time

import numpy as np
import torch

from cnn.hw_validation.production import diagnose_quantization16 as diag
from cnn.hw_validation.production.trained_integer import load_package, conv_exact
from cnn.train import sha256

base = diag.base
OUT = base.PROJECT / "cnn/hw_validation/production/reports/qat_g10_front3_data_20261014_v1"
PACKAGE = base.PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
FOUR = OUT.parent / "stem_ddr_down2_four_20261014"
RGB = OUT.parent / "stem_down2_handoff_20261011/vectors/rgb.hex"
LAYERS = ("stem.conv", "down2.dw.conv", "down2.pw.conv")
PINNED = {
    PACKAGE / "manifest.json": "93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b",
    PACKAGE / "numeric_test.bin": "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145",
    PACKAGE / "numeric_test_padded.bin": "bab36c254dfeb21ad21f4c600018be962f9352ddde79dcb08e64e7bd117ec417",
    FOUR / "reference.py": "f856b1e05f5cfe0e57d5a74bf9bd6719a67dc674fe274cb38886e2afe2e1514d",
    FOUR / "tests/test_vectors.py": "4ecca4b4992fa325760a9a73f223cd91a6d99d22bbce21e0769159204ac4fb1a",
    RGB: "59aad398e6142fd6b53c3da5c99ba95faeb3cd5b40b8e62a39340e328612ed61",
}


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_bytes(physical, offset, length):
    """Read through 160-bit little-endian words, including unaligned crossings."""
    if offset < 0 or length < 0 or offset + length > len(physical) or len(physical) % 20:
        raise ValueError("physical ROM range/word size")
    result = bytearray()
    for address in range(offset, offset + length):
        word = int.from_bytes(physical[address // 20 * 20:address // 20 * 20 + 20], "little")
        result.append((word >> (address % 20 * 8)) & 255)
    return bytes(result)


def round_even(value, shift):
    """Independent Python-int signed RNE; not the deployment NumPy helper."""
    if not 0 <= shift <= 62:
        raise ValueError("shift outside 0..62")
    quotient, remainder = divmod(abs(int(value)), 1 << shift)
    divisor = 1 << shift
    quotient += 2 * remainder > divisor or (2 * remainder == divisor and quotient % 2 == 1)
    return -quotient if value < 0 else quotient


def oracle_requantize(values, multipliers, shifts, low, high):
    source, mul, shift = np.broadcast_arrays(values, multipliers, shifts)
    if (np.any(source < -(1 << 31)) or np.any(source >= 1 << 31)
            or np.any(mul < 0) or np.any(mul >= 1 << 31)
            or np.any(shift < 0) or np.any(shift > 62)):
        raise ValueError("invalid requantization operand")
    return np.array([min(high, max(low, round_even(int(v) * int(m), int(s))))
                     for v, m, s in zip(source.flat, mul.flat, shift.flat, strict=True)],
                    dtype=np.int64).reshape(source.shape)


def oracle_silu(values, lut, upper):
    if np.any(values < -32768) or np.any(values > 32767) or np.shape(lut) != (1024,):
        raise ValueError("invalid SiLU input/table")
    result = []
    for value in values.flat:
        value = int(value)
        if value <= -2048:
            output = 0
        elif value >= 2048:
            output = value
        else:
            address = round_even(value, 2) + 512
            output = int(upper if address == 1024 else lut[address])
        result.append(output)
    return np.array(result, dtype=np.int16).reshape(values.shape)


def stage(image, p, lut, upper, stride, padding, groups):
    accumulator = conv_exact(image, p["weights"], p["bias"], stride, padding, groups)
    pre = oracle_requantize(accumulator, p["pre_multiplier"], p["pre_shift"], -32768, 32767).astype(np.int16)
    silu = oracle_silu(pre, lut, upper)
    post = oracle_requantize(silu, p["post_multiplier"], p["post_shift"], -128, 127).astype(np.int8)
    return (accumulator, pre, silu, post)


def loader_fields(parameters):
    stem, dw, pw = (parameters[name] for name in LAYERS)
    return ({2: stem["weights"].ravel(), 3: stem["bias"], 4: stem["pre_multiplier"],
             5: stem["pre_shift"], 6: np.concatenate((stem["post_multiplier"], stem["post_shift"]))},
            {2: dw["weights"].ravel(), 3: dw["bias"], 4: pw["weights"].ravel(), 5: pw["bias"],
             6: np.concatenate((dw["pre_multiplier"], pw["pre_multiplier"])),
             7: np.concatenate((dw["pre_shift"], pw["pre_shift"], dw["post_multiplier"],
                                pw["post_multiplier"], dw["post_shift"], pw["post_shift"]))})


def verify_loader(program, parameters, lut):
    expected = loader_fields(parameters)
    actual = [defaultdict(list), defaultdict(list)]
    selected, table, stopped = 0, [], False
    for index, word in enumerate(program):
        op, address, kind = word >> 60, (word >> 49) & 2047, (word >> 46) & 7
        value = word & 0xffffffff
        value = value - (1 << 32) if value >= 1 << 31 else value
        if op == 7:
            if any(program[index + 1:]):
                raise ValueError("nonzero program after STOP")
            stopped = True
            break
        if op == 4:
            if selected or value != 1:
                raise ValueError("invalid/repeated down2 selection")
            selected = 1
        elif op == 0:
            table.append((address, value))
        elif op == 1:
            if kind in expected[selected]:
                actual[selected][kind].append((address, value))
            elif selected or kind not in (0, 1):
                raise ValueError("unexpected loader kind")
        elif op not in (2, 3, 5, 6):
            raise ValueError("unknown opcode")
    if not stopped or selected != 1 or table != list(enumerate(map(int, lut))):
        raise ValueError("table/selection/STOP mismatch")
    for mode in (0, 1):
        for kind, values in expected[mode].items():
            if actual[mode][kind] != list(enumerate(map(int, values))):
                raise ValueError(f"parameter roundtrip mismatch mode={mode} kind={kind}")
    return sum(len(values) for fields in expected for values in fields.values())


def emit(path, values, bits):
    path.write_text("".join(f"{int(v) & ((1 << bits) - 1):0{bits // 4}x}\n"
                            for v in np.asarray(values).ravel()), encoding="ascii")


def check_hashes(hashes):
    for path, expected in hashes.items():
        if sha256(Path(path)) != expected:
            raise ValueError(f"frozen input/source changed: {path}")


def run():
    started = time.perf_counter()
    check_hashes(PINNED)
    runtime = diag.runtime.native_runtime_identity()
    model, manifest = load_package(PACKAGE)
    export = base.read(PACKAGE.parent / "export_parity.json")
    checkpoint = base.PROJECT / "cnn/runs/qat_frozen_stem_g10_20261014_v1/last.pt"
    if (sha256(checkpoint) != export["checkpoint_sha256"] or manifest["payload_sha256"] != export["payload_sha256"]
            or manifest["provenance"]["identity"] != export["identity"]):
        raise ValueError("QAT checkpoint/export binding changed")
    frozen = {str(path): digest for path, digest in PINNED.items()}
    frozen[str(checkpoint)] = export["checkpoint_sha256"]
    frozen[str(PACKAGE.parent / "export_parity.json")] = sha256(PACKAGE.parent / "export_parity.json")
    for path in sorted(PACKAGE.iterdir()):
        if path.is_file():
            frozen[str(path)] = sha256(path)
    for root in (FOUR / "vectors", FOUR / "reused"):
        for path in sorted(root.iterdir()):
            if path.is_file():
                frozen[str(path)] = sha256(path)
    old_sources = base.read(diag.OUT / "identity.json")["sources"]
    sources = {str(base.PROJECT / name): digest for name, digest in old_sources.items()}
    for path in (Path(__file__), Path(__file__).with_name("test_export_qat_front3.py"),
                 base.PROJECT / "cnn/hw_validation/production/train_qat.py"):
        sources[str(path)] = sha256(path)
    check_hashes(sources)
    OUT.mkdir(parents=True, exist_ok=False)
    for folder in ("parameters", "oracle", "sources", "inputs"):
        (OUT / folder).mkdir()
    for path in list(sources) + [str(FOUR / "reference.py"), str(FOUR / "tests/test_vectors.py")]:
        target = OUT / "sources" / Path(path).relative_to(base.PROJECT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    for path in (PACKAGE / "manifest.json", PACKAGE / "numeric_test.bin", PACKAGE / "numeric_test_padded.bin"):
        shutil.copyfile(path, OUT / "inputs" / path.name)
    shutil.copyfile(RGB, OUT / "parameters/rgb.hex")
    base.save(OUT / "identity.json", dict(fixed_inputs=frozen, sources=sources, runtime=runtime,
        payload_sha256=manifest["payload_sha256"], checkpoint_sha256=export["checkpoint_sha256"],
        input_scope="unchanged synthetic TEST RGB; real QAT-G10 parameters; not camera/accuracy evidence"))
    base.save(OUT / "contract.json", dict(layers=LAYERS, training_updates=0, full_network_forwards=0,
        expected_stage_values=26624, expected_program_length=6092, expected_parameter_loads=1134,
        expected_write_words=256, expected_halo_reads=289, one_variable="all first3 QAT parameter fields",
        oracle="vectorized int64 convolution, Python-int RNE and payload SiLU LUT vs existing scalar integer generator",
        HDL_simulation=False, board_or_bitstream=False, formal_acceptance=False))
    physical = (PACKAGE / "numeric_test_padded.bin").read_bytes()
    dtype_map = {"int8": "i1", "int32_le": "<i4", "uint8": "u1", "<i2": "<i2"}
    extracted, field_rows = {}, []
    for segment in manifest["segments"]:
        name = segment["name"]
        if not (any(name.startswith(layer + ".") for layer in LAYERS) or name == "shared.silu"):
            continue
        raw = word_bytes(physical, segment["offset"], segment["length"])
        if hashlib.sha256(raw).hexdigest() != segment["sha256"]:
            raise ValueError("selected ROM segment hash mismatch")
        values = np.frombuffer(raw, dtype=dtype_map[segment["dtype"]]).copy().reshape(segment["shape"])
        if name != "shared.silu":
            layer, field = name.rsplit(".", 1)
            np.testing.assert_array_equal(values, model.parameters[layer][field])
        extracted[name] = values
        field_rows.append(dict(name=name, offset=segment["offset"], bytes=segment["length"],
                               items=segment["count"], sha256=segment["sha256"]))
    if len(field_rows) != 19 or sum(row["bytes"] for row in field_rows) != 3527:
        raise ValueError("selected18 fields plus SiLU byte closure differs")
    parameters = {name: {field: extracted[f"{name}.{field}"] for field in model.parameters[name]} for name in LAYERS}
    bounds = {}
    for name, p in parameters.items():
        bound = np.abs(p["bias"].astype(np.int64)) + 128 * np.abs(p["weights"].astype(np.int64)).sum((1, 2, 3))
        if np.any(bound >= 1 << 31):
            raise OverflowError("cannot prove first3 INT32 final/33-bit partial safety for all INT8 inputs")
        bounds[name] = dict(conservative_max_abs=int(bound.max()), signed33_partial_safe=True, INT32_final_safe=True)
    stem, dw, pw = (parameters[name] for name in LAYERS)
    filenames = {"weights": "weights", "bias": "biases", "pre_multiplier": "multipliers", "pre_shift": "shifts"}
    for field, suffix in filenames.items():
        emit(OUT / "parameters" / f"stem_{suffix}.hex", stem[field], 8 if field == "weights" else 32)
    emit(OUT / "parameters/stem_post.hex", np.concatenate((stem["post_multiplier"], stem["post_shift"])), 32)
    for prefix, p in (("dw", dw), ("pw", pw)):
        emit(OUT / "parameters" / f"{prefix}_weights.hex", p["weights"], 8)
        emit(OUT / "parameters" / f"{prefix}_biases.hex", p["bias"], 32)
    fields = loader_fields(parameters)
    emit(OUT / "parameters/multipliers.hex", fields[1][6], 32)
    emit(OUT / "parameters/controls.hex", fields[1][7], 32)
    lut = extracted["shared.silu"]
    emit(OUT / "parameters/silu.hex", lut, 16)
    rgb = np.array([int(v, 16) for v in RGB.read_text().split()], dtype=np.uint8).reshape(288, 512, 3)
    centered = (rgb[:32, :32].astype(np.int16) - 128).astype(np.int8)
    stem_stages = stage(centered, stem, lut, manifest["silu_upper"], 2, 1, 1)
    halo = np.pad(stem_stages[-1], ((1, 0), (1, 0), (0, 0)))
    dw_stages = stage(halo, dw, lut, manifest["silu_upper"], 2, 0, 16)
    pw_stages = stage(dw_stages[-1], pw, lut, manifest["silu_upper"], 1, 0, 1)
    np.save(OUT / "parameters/expected_stem_hwc.npy", stem_stages[-1], allow_pickle=False)
    np.save(OUT / "parameters/expected_pw_hwc.npy", pw_stages[-1], allow_pickle=False)
    np.savez_compressed(OUT / "oracle/stages.npz", **{f"{prefix}_{suffix}": array
        for prefix, arrays in (("stem", stem_stages), ("dw", dw_stages), ("pw", pw_stages))
        for suffix, array in zip(("acc", "pre", "silu", "post"), arrays, strict=True)})
    reference = import_file("frozen_four_reference", FOUR / "reference.py")
    reference.ROOT, reference.BASE = OUT, OUT / "parameters"
    receipt = reference.generate()
    # Correct only the NEW generated receipt's inherited label, never old evidence.
    receipt.update(parameters="RETAINED_QAT_G10_REAL_PARAMETERS_SYNTHETIC_INPUT", original_generator_label="FROZEN_TEST_ONLY",
                   actual_payload_sha256=manifest["payload_sha256"], formal_acceptance=False)
    (OUT / "reference.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    vectors = OUT / "vectors"
    read_hex = lambda name: [int(v, 16) for v in (vectors / name).read_text().split()]
    program = read_hex("program.hex")
    old_program = [int(v, 16) for v in (FOUR / "vectors/program.hex").read_text().split()]
    if len(program) != len(old_program) or any(a >> 32 != b >> 32 for a, b in zip(program, old_program, strict=True)):
        raise ValueError("instruction/op/address/kind layout changed")
    parameter_writes = verify_loader(program, parameters, lut)
    if parameter_writes != 1134:
        raise ValueError("parameter load count changed")
    validator = import_file("frozen_vector_validator", FOUR / "tests/test_vectors.py")
    validator.validate(program, read_hex("stem_addresses.hex"), read_hex("halo_map.hex"), read_hex("read_indices.hex"))
    comparisons = []
    for prefix, arrays, tiles in (("stem", stem_stages, [(y, x) for y in range(4) for x in range(4)]),
                                  ("dw", dw_stages, [(0, 0), (0, 1), (1, 0), (1, 1)]),
                                  ("pw", pw_stages, [(0, 0), (0, 1), (1, 0), (1, 1)])):
        for suffix, array, bits in zip(("acc", "pre", "silu", "post"), arrays, (32, 16, 16, 8), strict=True):
            expected = np.concatenate([array[y*4:y*4+4, x*4:x*4+4].ravel() for y, x in tiles]).astype(np.int64)
            raw = np.array(read_hex(f"{prefix}_{suffix}.hex"), dtype=np.int64)
            actual = np.where(raw >= 1 << (bits - 1), raw - (1 << bits), raw)
            np.testing.assert_array_equal(actual, expected)
            comparisons.append(dict(stage=f"{prefix}_{suffix}", values=int(expected.size), exact=True))
    if sum(row["values"] for row in comparisons) != 26624:
        raise ValueError("stage value count changed")
    for name in ("stem_addresses.hex", "halo_map.hex", "read_indices.hex", "once_constants.vh"):
        if (vectors / name).read_bytes() != (FOUR / "vectors" / name).read_bytes():
            raise ValueError("fixed layout/constants changed")
    check_hashes(frozen)
    check_hashes(sources)
    artifacts = {str(p.relative_to(OUT)).replace("\\", "/"): sha256(p)
                 for folder in ("parameters", "oracle", "vectors") for p in sorted((OUT / folder).iterdir()) if p.is_file()}
    base.save(OUT / "verification_receipt.json", dict(status="DATA_ONLY_VERIFIED_NOT_RTL",
        selected_fields=field_rows, selected_bytes=3527, parameter_writes=parameter_writes, table_writes=1024,
        stage_comparisons=comparisons, stage_values=26624, bounds=bounds,
        program_length=6092, program_capacity=8192, unchanged_opcode_address_kind=True,
        writes=256, reads=289, original_layout_files_exact=True, artifact_sha256=artifacts,
        input_sha256=sha256(RGB), payload_sha256=manifest["payload_sha256"], source_sha256=sha256(Path(__file__)),
        scalar_generator_and_independent_oracle_exact=True, RTL_compared=False, formal_acceptance=False))
    base.save(OUT / "status.json", dict(status="REAL_QAT_FRONT3_DATA_READY_FOR_RTL_SIMULATION",
        seconds=time.perf_counter() - started, training_updates=0, full_network_forwards=0,
        CUDA_initialized=torch.cuda.is_initialized(), RTL_changed=False, RTL_compared=False,
        simulation_or_synthesis_run=False, bitstream_or_board_operation=False, formal_acceptance=False,
        verification_receipt_sha256=sha256(OUT / "verification_receipt.json")))


if __name__ == "__main__":
    diag.runtime_guard()
    run()
