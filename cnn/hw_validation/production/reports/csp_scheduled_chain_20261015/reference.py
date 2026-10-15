"""Fixed first-CSP schedule vectors and handshake-only chain model."""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
DATA = REPORTS / "qat_g10_csp_first_data_20261015_v2"
SCHEDULE = REPORTS / "csp_tile_schedule_20261015" / "reference"
BASE = REPORTS / "csp_dw_cache_20261015"
SOURCE = REPORTS / "qat_g10_csp_first_closure_20261015_v2" / "vectors"
OUT = ROOT / "reference"
DW_BASE = 56_532_992
PW_BASE = 56_643_584


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_hex(path: Path) -> list[int]:
    return [int(word, 16) for word in path.read_text(encoding="ascii").split()]


def pack_lanes(values: list[int], bits: int) -> int:
    """Pack lane 0 in the least-significant field."""
    return sum(value << (bits * lane) for lane, value in enumerate(values))


def pack_descriptor(task_id: int, pw: bool, y: int, x: int, channel: int,
                    first: bool, last: bool, output_mask: int) -> int:
    word = (task_id << 17) | (int(pw) << 16) | (y << 14) | (x << 12) | (channel << 8)
    word |= (int(first) << 7) | (int(last) << 6) | (output_mask << 3)
    assert word < 1 << 25 and word & 7 == 0
    return word


def expected_tasks() -> list[tuple[str, int, int, int, int, list[list[int] | None]]]:
    tasks = []
    for y in range(4):
        for channel in range(12):
            for x in (0, 3):
                coordinates = ([[y, x + lane, channel] for lane in range(3)]
                               if x == 0 else [[y, 3, channel], None, None])
                tasks.append(("dw", y, x, channel, 7 if x == 0 else 1, coordinates))
    for y in range(4):
        for x in range(4):
            for channel in range(0, 12, 3):
                tasks.append(("pw", y, x, channel, 7,
                              [[y, x, channel + lane] for lane in range(3)]))
    return tasks


def derive() -> tuple[list[int], list[int], list[int], list[int]]:
    frozen_path = DATA / "mac_tasks.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    specs = expected_tasks()
    assert len(frozen["tasks"]) == len(specs) == 160
    assert frozen["valid_accumulators"] == 384

    tags, addresses, masks, descriptors = [], [], [], []
    for task_id, (actual, spec) in enumerate(zip(frozen["tasks"], specs)):
        layer, y, x, channel, output_mask, coordinates = spec
        assert actual["layer"] == layer, task_id
        assert actual["coordinates"] == coordinates, task_id
        assert actual["output_mask"] == output_mask, task_id
        if layer == "dw":
            lane_tags = [((y * 4 + x + lane) * 12 + channel) if output_mask & (1 << lane) else 0
                         for lane in range(3)]
            lane_addresses = [DW_BASE + tag if output_mask & (1 << lane) else 0
                              for lane, tag in enumerate(lane_tags)]
        else:
            lane_tags = [192 + (y * 4 + x) * 12 + channel + lane for lane in range(3)]
            lane_addresses = [PW_BASE + tag - 192 for tag in lane_tags]
        tags.append(pack_lanes(lane_tags, 16))
        addresses.append(pack_lanes(lane_addresses, 32))
        masks.append(output_mask)
        assert len(actual["groups"]) == 2
        for group in actual["groups"]:
            descriptors.append(pack_descriptor(task_id, layer == "pw", y, x, channel,
                                               group["first"], group["last"], output_mask))
    assert len(descriptors) == 320
    return tags, addresses, masks, descriptors


def compare_frozen(tags: list[int], addresses: list[int], masks: list[int],
                   descriptors: list[int]) -> dict[str, object]:
    legacy_tags = read_hex(SOURCE / "task_tags.hex")
    legacy_addresses = read_hex(SOURCE / "task_addresses.hex")
    legacy_masks = read_hex(SOURCE / "task_mask.hex")
    assert len(legacy_tags) == len(legacy_addresses) == len(legacy_masks) == 160
    for task, mask in enumerate(masks):
        for lane in range(3):
            valid = bool(mask & 1 << lane)
            actual_tag = legacy_tags[task] >> (16 * lane) & 0xFFFF
            expected_tag = tags[task] >> (16 * lane) & 0xFFFF
            assert actual_tag == expected_tag if valid else actual_tag == 0xFFFF
            actual_address = legacy_addresses[task] >> (32 * lane) & 0xFFFFFFFF
            expected_address = addresses[task] >> (32 * lane) & 0xFFFFFFFF
            assert actual_address == expected_address
    assert legacy_masks == masks
    assert read_hex(SCHEDULE / "descriptor.hex") == descriptors

    frozen = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    for name in ("task_tags.hex", "task_addresses.hex", "task_mask.hex"):
        path = SOURCE / name
        assert frozen[str(path)] == sha256(path)
    return {
        "base_report": BASE.name,
        "actual_vector_directory": str(SOURCE),
        "legacy_invalid_tag": "ffff only in masked lanes; generated invalid tag is 0000",
        "valid_lane_mismatches": 0,
        "address_mismatches": 0,
        "mask_mismatches": 0,
        "descriptor_mismatches": 0,
    }


class ChainModel:
    """One outstanding group transaction; no modeled arithmetic latency."""

    def __init__(self, tags: list[int], addresses: list[int], masks: list[int],
                 descriptors: list[int]) -> None:
        self.tags, self.addresses, self.masks, self.descriptors = tags, addresses, masks, descriptors
        self.silu_loaded = False
        self.silu_load_count = 0
        self.provider_clear_required = True
        self.active = False
        self.cycle = 0

    def load_silu(self) -> None:
        if self.provider_clear_required:
            raise AssertionError("provider must clear old responses before SiLU load")
        self.silu_loaded = True
        self.silu_load_count += 1

    def provider_clear(self) -> None:
        self.provider_clear_required = False

    def start_tile(self) -> None:
        assert not self.active and not self.provider_clear_required and self.silu_loaded
        self.active = True
        self.task = self.group = self.completed_tasks = 0
        self.cache_tags: set[int] = set()
        self.phase = "group"
        self.outstanding = False
        self.weight_latched = self.cache_latched = False
        self.writes_remaining = 0
        self.cycle = 0

    def reset(self) -> None:
        self.active = False
        self.provider_clear_required = True
        self.silu_loaded = False
        self.outstanding = False
        self.weight_latched = self.cache_latched = False
        self.phase = "cancelled"

    @property
    def descriptor(self) -> int:
        return self.descriptors[self.task * 2 + self.group]

    @property
    def pw(self) -> bool:
        return bool(self.descriptor >> 16 & 1)

    @property
    def request_valid(self) -> bool:
        return self.active and self.phase == "group" and not self.outstanding

    @property
    def mac_valid(self) -> bool:
        return (self.active and self.phase == "group" and self.outstanding and self.weight_latched
                and (self.cache_latched or not self.pw))

    @property
    def write_valid(self) -> bool:
        return self.active and self.phase == "write" and self.writes_remaining > 0

    @property
    def write_lane(self) -> int:
        done = self.masks[self.task].bit_count() - self.writes_remaining
        return [lane for lane in range(3) if self.masks[self.task] & 1 << lane][done]

    @property
    def write_tag(self) -> int:
        return self.tags[self.task] >> (16 * self.write_lane) & 0xFFFF

    @property
    def write_address(self) -> int:
        return self.addresses[self.task] >> (32 * self.write_lane) & 0xFFFFFFFF

    def step(self, *, request_ready: bool = False, weight_valid: bool = False,
             weight_descriptor: int | None = None, cache_valid: bool = False,
             cache_descriptor: int | None = None, mac_ready: bool = False,
             write_ready: bool = False) -> dict[str, object]:
        if self.provider_clear_required and (weight_valid or cache_valid):
            raise AssertionError("provider returned a stale response after reset")
        events: dict[str, object] = {}
        was_outstanding = self.active and self.phase == "group" and self.outstanding
        expected = self.descriptor if self.active and self.phase == "group" else None
        if weight_valid:
            assert was_outstanding and not self.weight_latched
            assert weight_descriptor == expected
            self.weight_latched = True
            events["weight_accept"] = expected
        if cache_valid:
            assert was_outstanding and self.pw and not self.cache_latched
            assert cache_descriptor == expected
            self.cache_latched = True
            events["cache_accept"] = expected
        if self.request_valid and request_ready:
            self.outstanding = True
            events["request_accept"] = expected
            if self.pw:
                assert len(self.cache_tags) == 192
                events["cache_request"] = ((expected >> 14 & 3) * 4 + (expected >> 12 & 3)) * 2 + self.group
        if self.mac_valid and mac_ready:
            events["mac_accept"] = expected
            last = bool(expected >> 6 & 1)
            self.outstanding = self.weight_latched = self.cache_latched = False
            if last:
                self.phase = "write"
                self.writes_remaining = self.masks[self.task].bit_count()
            else:
                self.group += 1
        if self.write_valid and write_ready:
            events["write_accept"] = (self.write_tag, self.write_address)
            if not self.pw:
                self.cache_tags.add(self.write_tag)
            self.writes_remaining -= 1
            if self.writes_remaining == 0:
                events["task_done"] = self.task
                self.completed_tasks += 1
                self.task += 1
                self.group = 0
                self.phase = "group"
                if self.task == 160:
                    assert len(self.cache_tags) == 192
                    self.active = False
                    self.phase = "done"
        self.cycle += 1
        return events


def exercise_model(tags: list[int], addresses: list[int], masks: list[int],
                   descriptors: list[int]) -> dict[str, int]:
    rng = random.Random(0xC5_20261015)
    model = ChainModel(tags, addresses, masks, descriptors)
    model.provider_clear()
    model.load_silu()
    model.start_tile()
    pending_weight = pending_cache = None
    request_accepts = cache_requests = mac_accepts = write_accepts = task_done = 0
    hold_checks = 0
    for _ in range(20_000):
        before = (model.task, model.group, model.completed_tasks)
        send_weight = pending_weight is not None and pending_weight[0] == model.cycle
        send_cache = pending_cache is not None and pending_cache[0] == model.cycle
        events = model.step(
            request_ready=rng.random() < 0.65,
            weight_valid=send_weight,
            weight_descriptor=pending_weight[1] if send_weight else None,
            cache_valid=send_cache,
            cache_descriptor=pending_cache[1] if send_cache else None,
            mac_ready=rng.random() < 0.7,
            write_ready=rng.random() < 0.6,
        )
        if send_weight:
            pending_weight = None
        if send_cache:
            pending_cache = None
        if "request_accept" in events:
            descriptor = int(events["request_accept"])
            pending_weight = (model.cycle + rng.randrange(1, 5), descriptor)
            if "cache_request" in events:
                pending_cache = (model.cycle + rng.randrange(1, 5), descriptor)
                cache_requests += 1
            request_accepts += 1
        mac_accepts += "mac_accept" in events
        write_accepts += "write_accept" in events
        task_done += "task_done" in events
        if not events:
            assert (model.task, model.group, model.completed_tasks) == before
            hold_checks += 1
        if not model.active:
            break
    assert not model.active and model.completed_tasks == 160
    assert (request_accepts, cache_requests, mac_accepts, write_accepts, task_done) == (320, 128, 320, 384, 160)
    observed_cycles = model.cycle

    silu_load_count = model.silu_load_count
    model.start_tile()
    assert not model.cache_tags and model.silu_load_count == silu_load_count
    model.step(request_ready=True)
    accepted = model.descriptor
    model.reset()
    try:
        model.step(weight_valid=True, weight_descriptor=accepted)
    except AssertionError:
        pass
    else:
        raise AssertionError("stale response was not rejected")
    model.provider_clear()
    assert not model.silu_loaded

    probe = ChainModel(tags, addresses, masks, descriptors)
    probe.provider_clear()
    probe.load_silu()
    probe.start_tile()
    try:
        probe.step(weight_valid=True, weight_descriptor=probe.descriptor)
    except AssertionError:
        pass
    else:
        raise AssertionError("response before request_accept was not rejected")
    probe.step(request_ready=True)
    try:
        probe.step(weight_valid=True, weight_descriptor=probe.descriptor ^ 8)
    except AssertionError:
        pass
    else:
        raise AssertionError("response descriptor mismatch was not rejected")
    return {
        "random_seed": 0xC5_20261015,
        "observed_cycles": observed_cycles,
        "request_accepts": request_accepts,
        "pw_cache_requests": cache_requests,
        "mac_accepts": mac_accepts,
        "write_accepts": write_accepts,
        "task_done": task_done,
        "bubble_and_backpressure_hold_checks": hold_checks,
        "stale_response_rejections": 1,
        "early_response_rejections": 1,
        "descriptor_mismatch_rejections": 1,
        "tile_restart_without_silu_reload": 1,
    }


def main() -> None:
    tags, addresses, masks, descriptors = derive()
    comparison = compare_frozen(tags, addresses, masks, descriptors)
    model_checks = exercise_model(tags, addresses, masks, descriptors)
    OUT.mkdir(exist_ok=True)
    outputs = {
        "tags.hex": (tags, 12),
        "address.hex": (addresses, 24),
        "descriptor.hex": (descriptors, 7),
    }
    for name, (values, width) in outputs.items():
        (OUT / name).write_text("".join(f"{value:0{width}x}\n" for value in values), encoding="ascii")
    inputs = [
        DATA / "mac_tasks.json", DATA / "contract.json", SCHEDULE / "descriptor.hex",
        BASE / "frozen.json", SOURCE / "task_tags.hex", SOURCE / "task_addresses.hex",
        SOURCE / "task_mask.hex",
    ]
    receipt = {
        "status": "PASS",
        "scope": "fixed first-CSP schedule/address derivation and handshake-only control model",
        "source_sha256": sha256(Path(__file__)),
        "input_sha256": {str(path): sha256(path) for path in inputs},
        "comparison": comparison,
        "results": {"tasks": 160, "groups": 320, "valid_writes": 384},
        "packing": {
            "descriptor": "[24:17] task_id [16] pw [15:14] y [13:12] x [11:8] channel [7] first [6] last [5:3] output_mask [2:0] zero",
            "tags": "3 x 16-bit fields; lane0 least-significant; invalid lane=0",
            "addresses": "3 x 32-bit byte addresses; lane0 least-significant; invalid lane=0",
        },
        "address_rules": {
            "dw": "56532992 + ((y*4+x+lane)*12+c)",
            "pw": "56643584 + ((192+(y*4+x)*12+c+lane)-192)",
        },
        "model_checks": model_checks,
        "cycle_boundary": "counts only explicit valid/ready handshakes under randomized stimulus; no arithmetic latency or performance claim",
        "reset_boundary": "reset cancels the transaction, requires provider_clear, and requires SiLU reload; a new tile only clears local DW cache",
        "output_sha256": {name: sha256(OUT / name) for name in outputs},
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS tasks=160 groups=320 writes=384 frozen_vectors_match handshake_model_pass")


if __name__ == "__main__":
    main()
