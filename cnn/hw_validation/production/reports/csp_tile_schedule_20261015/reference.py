"""Generate the fixed first-CSP tile task schedule used by the RTL testbench."""
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "qat_g10_csp_first_data_20261015_v2"
CHECKS = ROOT.parent / "qat_g10_csp_first_checks_20261015_v2"
OUT = ROOT / "reference"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_tasks():
    tasks = []
    for y in range(4):
        for channel in range(12):
            for x in (0, 3):
                coordinates = [[y, x + lane, channel] for lane in range(3)] if x == 0 else [[y, 3, channel], None, None]
                tasks.append(("dw", y, x, channel, 7 if x == 0 else 1, coordinates))
    for y in range(4):
        for x in range(4):
            for channel in range(0, 12, 3):
                coordinates = [[y, x, channel + lane] for lane in range(3)]
                tasks.append(("pw", y, x, channel, 7, coordinates))
    return tasks


def pack(task_id, pw, y, x, channel, first, last, output_mask):
    word = (task_id << 17) | (pw << 16) | (y << 14) | (x << 12) | (channel << 8)
    word |= (first << 7) | (last << 6) | (output_mask << 3)
    assert word < (1 << 25) and word & 7 == 0
    return word


def main():
    contract_path = DATA / "contract.json"
    tasks_path = DATA / "mac_tasks.json"
    checks_path = CHECKS / "status.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    frozen = json.loads(tasks_path.read_text(encoding="utf-8"))
    checks = json.loads(checks_path.read_text(encoding="utf-8"))
    expected = expected_tasks()

    assert contract["expected_MAC_tasks"] == len(expected) == 160
    assert contract["expected_MAC_groups"] == 320
    assert contract["expected_valid_MAC_results"] == frozen["valid_accumulators"] == 384
    assert checks["status"] == "PASS_CSP_FIRST_LOCAL_PROBE_16_OF_16"
    assert len(frozen["tasks"]) == len(expected)

    descriptors = []
    input_masks = []
    outputs = []
    for task_id, (actual, spec) in enumerate(zip(frozen["tasks"], expected)):
        layer, y, x, channel, output_mask, coordinates = spec
        assert actual["layer"] == layer, task_id
        assert actual["coordinates"] == coordinates, task_id
        assert actual["output_mask"] == output_mask, task_id
        outputs.extend((layer, *value) for value in coordinates if value is not None)

        expected_masks = (0xFF, 0x7F if layer == "dw" and x == 0 else 0x01 if layer == "dw" else 0x0F)
        assert len(actual["groups"]) == 2, task_id
        for group, (first, last, input_mask) in enumerate(((1, 0, expected_masks[0]), (0, 1, expected_masks[1]))):
            actual_group = actual["groups"][group]
            assert (actual_group["first"], actual_group["last"], actual_group["input_mask"]) == (
                bool(first), bool(last), input_mask), (task_id, group)
            descriptors.append(pack(task_id, layer == "pw", y, x, channel, first, last, output_mask))
            input_masks.append(input_mask)

    assert len(outputs) == len(set(outputs)) == 384
    assert len(descriptors) == len(input_masks) == 320
    assert descriptors[0] == 0x00000B8 and descriptors[-1] == 0x13FF978

    OUT.mkdir(exist_ok=True)
    descriptor_path = OUT / "descriptor.hex"
    mask_path = OUT / "input_mask.hex"
    descriptor_path.write_text("".join(f"{word:07x}\n" for word in descriptors), encoding="ascii")
    mask_path.write_text("".join(f"{mask:02x}\n" for mask in input_masks), encoding="ascii")

    receipt = {
        "status": "PASS",
        "scope": "fixed first-CSP 4x4x12 task descriptors only; no arithmetic or DDR access",
        "input_sha256": {
            str(contract_path): sha256(contract_path),
            str(tasks_path): sha256(tasks_path),
            str(checks_path): sha256(checks_path),
        },
        "checks_v2_status": checks["status"],
        "reference_sha256": sha256(Path(__file__).resolve()),
        "results": {"tasks": 160, "groups": 320, "unique_outputs": 384, "descriptor_width_bits": 25},
        "packing": "[24:17] task_id, [16] pw, [15:14] y, [13:12] x, [11:8] channel, [7] first, [6] last, [5:3] output_mask, [2:0] zero",
        "output_sha256": {"descriptor.hex": sha256(descriptor_path), "input_mask.hex": sha256(mask_path)},
        "arithmetic_executed": False,
        "ddr_executed": False,
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS tasks=160 groups=320 unique_outputs=384 descriptors=320")


if __name__ == "__main__":
    main()
