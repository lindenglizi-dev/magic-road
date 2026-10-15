"""Fixed 4x4x12 DW-to-PW cache contract and deterministic vectors."""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


PIXELS = 16
CHANNELS = 12
BANKS = 8
ROWS = 32
LOGICAL_BYTES = PIXELS * CHANNELS
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "qat_g10_csp_first_closure_20261015_v2" / "vectors"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_hex(path: Path, bits: int) -> list[int]:
    values = [int(word, 16) for word in path.read_text(encoding="ascii").split()]
    if any(value >= 1 << bits for value in values):
        raise ValueError(f"{path.name}: value exceeds {bits} bits")
    return values


def pack_bytes(values: list[int]) -> int:
    """Pack lane 0 in the least-significant byte."""
    return sum(value << (8 * lane) for lane, value in enumerate(values))


class DwCache:
    """Behavioral contract: 192 valid bytes in an uncleared 8x32 RAM."""

    def __init__(self, initial_ram: int = 0xA5) -> None:
        if not 0 <= initial_ram <= 0xFF:
            raise ValueError("initial RAM byte must be 0..255")
        self.ram = [[initial_ram] * ROWS for _ in range(BANKS)]
        self.reset()

    def reset(self) -> None:
        self.valid = [False] * LOGICAL_BYTES
        self.write_count = 0
        self.fault = False

    @property
    def loaded(self) -> bool:
        return self.write_count == LOGICAL_BYTES and not self.fault

    @property
    def write_ready(self) -> bool:
        return not self.loaded and not self.fault

    @staticmethod
    def location(index: int) -> tuple[int, int]:
        pixel, channel = divmod(index, CHANNELS)
        return channel % BANKS, pixel * 2 + channel // BANKS

    def write(self, index: int, data: int) -> bool:
        """Attempt one accepted write; return False only when write_ready is low."""
        if not 0 <= data <= 0xFF:
            raise ValueError("write data must be one byte")
        if not self.write_ready:
            return False
        if not 0 <= index < LOGICAL_BYTES or self.valid[index]:
            self.fault = True
            return True
        bank, row = self.location(index)
        self.ram[bank][row] = data
        self.valid[index] = True
        self.write_count += 1
        return True

    def read(self, pixel: int, group: int) -> tuple[int, int] | None:
        """Return (64-bit word, lane mask), or None until the full cache is ready."""
        if not 0 <= pixel < PIXELS or group not in (0, 1):
            raise ValueError("read must select pixel 0..15 and group 0/1")
        if not self.loaded:
            return None
        row = pixel * 2 + group
        valid_lanes = 8 if group == 0 else 4
        lanes = [self.ram[bank][row] if bank < valid_lanes else 0 for bank in range(BANKS)]
        return pack_bytes(lanes), (1 << valid_lanes) - 1


def expected_reads(dw: list[int]) -> list[int]:
    return [pack_bytes(dw[pixel * CHANNELS + group * 8:
                               pixel * CHANNELS + min(group * 8 + 8, CHANNELS)] +
                       ([0] * 4 if group else []))
            for pixel in range(PIXELS) for group in range(2)]


def verify(dw: list[int], groups: list[int]) -> dict[str, int]:
    if len(dw) != LOGICAL_BYTES:
        raise ValueError(f"dw_post.hex must contain {LOGICAL_BYTES} bytes")
    if len(groups) != 320:
        raise ValueError("group_activation.hex must contain 320 groups")
    reads = expected_reads(dw)
    locations = {DwCache.location(index) for index in range(LOGICAL_BYTES)}
    assert len(locations) == LOGICAL_BYTES
    assert all(0 <= bank < BANKS and 0 <= row < ROWS for bank, row in locations)
    if any(word >> 32 for word in reads[1::2]):
        raise AssertionError("group 1 upper four lanes must be zero")

    order = list(range(LOGICAL_BYTES))
    random.Random(0xC5D0).shuffle(order)
    cache = DwCache()
    for position, index in enumerate(order):
        assert cache.write(index, dw[index])
        if position != LOGICAL_BYTES - 1:
            assert not cache.loaded and cache.read(0, 0) is None
    assert cache.loaded and cache.write_count == LOGICAL_BYTES
    for pixel in range(PIXELS):
        for group in range(2):
            assert cache.read(pixel, group) == (reads[pixel * 2 + group], 0xFF if group == 0 else 0x0F)

    actual_pw = groups[192:]
    for task in range(64):
        pixel = task // 4
        assert actual_pw[task * 2:task * 2 + 2] == reads[pixel * 2:pixel * 2 + 2]

    missing = DwCache()
    for index in range(LOGICAL_BYTES - 1):
        assert missing.write(index, dw[index])
    assert missing.write_count == 191 and not missing.loaded and missing.read(15, 1) is None

    duplicate = DwCache()
    assert duplicate.write(0, dw[0]) and duplicate.write(0, dw[0])
    assert duplicate.fault and duplicate.write_count == 1 and not duplicate.write(1, dw[1])
    duplicate_ram = [row[:] for row in duplicate.ram]
    duplicate.reset()
    assert not duplicate.fault and duplicate.write_count == 0 and duplicate.ram == duplicate_ram
    for index in (192, 255):
        invalid = DwCache()
        assert invalid.write(index, 0) and invalid.fault and invalid.write_count == 0

    stale = DwCache()
    for index, value in enumerate(dw):
        assert stale.write(index, value)
    ram_before_reset = [row[:] for row in stale.ram]
    stale.reset()
    assert stale.ram == ram_before_reset
    assert stale.write_count == 0 and not stale.loaded and stale.read(0, 0) is None

    return {"logical_bytes": len(dw), "valid_physical_bytes": len(locations),
            "unused_physical_bytes": BANKS * ROWS - len(locations), "distinct_reads": len(reads),
            "real_pw_task_groups": len(actual_pw), "physical_bytes": BANKS * ROWS}


def main() -> None:
    dw_path = SOURCE / "dw_post.hex"
    group_path = SOURCE / "group_activation.hex"
    dw = read_hex(dw_path, 8)
    groups = read_hex(group_path, 64)
    checks = verify(dw, groups)
    reads = expected_reads(dw)
    out = ROOT / "reference"
    out.mkdir(exist_ok=True)
    (out / "dw.hex").write_text("".join(f"{value:02x}\n" for value in dw), encoding="ascii")
    (out / "pw_read.hex").write_text("".join(f"{value:016x}\n" for value in reads), encoding="ascii")
    receipt = {
        "status": "PASS",
        "contract": {
            "shape": "4x4x12",
            "layout": "bank=c%8,row=pixel*2+c//8",
            "physical": "8 banks x 32 rows; 256 bytes allocated, 192 valid",
            "read_order": "pixel 0..15, group 0 then 1; lane 0 is least-significant byte",
            "reset": "clears valid/count/fault, not RAM",
        },
        "checks": checks,
        "inputs": {
            "../qat_g10_csp_first_closure_20261015_v2/vectors/dw_post.hex": sha256(dw_path),
            "../qat_g10_csp_first_closure_20261015_v2/vectors/group_activation.hex": sha256(group_path),
        },
        "source_sha256": sha256(Path(__file__)),
        "artifacts": {"dw.hex": sha256(out / "dw.hex"), "pw_read.hex": sha256(out / "pw_read.hex")},
        "evidence_boundary": "development integration baseline only; not a deployment accuracy result",
    }
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS csp_dw_cache reference: 192 writes, 32 reads, 128 real PW groups")


if __name__ == "__main__":
    main()
