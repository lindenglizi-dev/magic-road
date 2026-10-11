"""Integer and handshake reference for the overlapped convolution postprocess."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path


PRE_FACTOR = (1, 3, 5)
PRE_SHIFT = (0, 2, 4)
POST_FACTOR = 1
POST_SHIFT = 4
META_DEPTH = 8
GROUP_DEPTH = 2
ROOT = Path(__file__).resolve().parent
FROZEN_SILU = ROOT.parents[1] / "v8_reset_layer_tiles_20261007" / "layers" / "vectors" / "silu.hex"
FROZEN_SILU_SHA256 = "305db026a2961c891369dfe4c9191a27adc89cf80f6ad8b6ac5042e09cf2de43"


def round_shift(value: int, shift: int) -> int:
    """Nearest-even right shift followed by signed-16 saturation."""
    if not 0 <= shift < 63:
        raise ValueError(f"illegal shift: {shift}")
    magnitude = abs(value)
    quotient, remainder = divmod(magnitude, 1 << shift)
    half = 0 if shift == 0 else 1 << (shift - 1)
    if shift and (remainder > half or (remainder == half and quotient & 1)):
        quotient += 1
    result = -quotient if value < 0 else quotient
    return max(-32768, min(32767, result))


def load_silu_table() -> tuple[int, ...]:
    encoded = FROZEN_SILU.read_bytes()
    if hashlib.sha256(encoded).hexdigest() != FROZEN_SILU_SHA256:
        raise RuntimeError("frozen SiLU table hash mismatch")
    values = tuple(int(line, 16) for line in encoded.decode("ascii").splitlines())
    if len(values) != 1024:
        raise RuntimeError("frozen SiLU table length mismatch")
    return tuple(value - 65536 if value & 0x8000 else value for value in values)


SILU_TABLE = load_silu_table()


def silu(value: int) -> int:
    """Frozen Q7.8 lookup contract used by the unchanged SiLU block."""
    if value <= -2048:
        return 0
    if value >= 2048:
        return value
    address = round_shift(value, 2) + 512
    return 2047 if address == 1024 else SILU_TABLE[address]


def sat8(value: int) -> int:
    return max(-128, min(127, value))


def pack_tag(layer: int, position: int, channel: int, reserved: int = 0) -> int:
    """Pack {layer[0], position[3:0], channel[4:0], reserved[5:0]}."""
    if not (0 <= layer < 2 and 0 <= position < 16 and
            0 <= channel < 32 and 0 <= reserved < 64):
        raise ValueError("tag field out of range")
    return (layer << 15) | (position << 11) | (channel << 6) | reserved


def unpack_tag(tag: int) -> tuple[int, int, int, int]:
    return (tag >> 15, (tag >> 11) & 0xF, (tag >> 6) & 0x1F, tag & 0x3F)


def quantize(accumulator: int, lane: int) -> tuple[int, int, int, int]:
    pre = round_shift(accumulator * PRE_FACTOR[lane], PRE_SHIFT[lane])
    activated = silu(pre)
    post = round_shift(activated * POST_FACTOR, POST_SHIFT)
    return pre, activated, post, sat8(post)


@dataclass(frozen=True)
class Scalar:
    value: int
    tag: int


@dataclass(frozen=True)
class ResultGroup:
    values: tuple[int, int, int]
    layer: int
    position: int
    channel: int
    lane_mask: int
    fault: bool = False

    def __post_init__(self) -> None:
        if not (0 <= self.position < 16 and 0 <= self.channel < 24):
            raise ValueError("result identity out of range")
        if self.channel % 3:
            raise ValueError("channel base must be aligned to the three MAC lanes")
        if self.layer == 0:
            if self.channel > 15 or self.lane_mask not in (1, 2, 4):
                raise ValueError("DW requires one selected lane within channels 0..15")
            if self.channel + self.lane_mask.bit_length() - 1 > 15:
                raise ValueError("DW selected channel exceeds 15")
        elif self.layer == 1:
            if self.channel > 21 or self.lane_mask != 0b111:
                raise ValueError("24-channel PW requires aligned base 0..21 and all lanes")
        else:
            raise ValueError("unknown layer")

    def scalars(self) -> tuple[Scalar, ...]:
        if self.fault:
            return ()
        return tuple(Scalar(value, pack_tag(self.layer, self.position, self.channel + lane))
                     for lane, value in enumerate(self.values)
                     if self.lane_mask & (1 << lane))


class Pipe:
    """A globally-stalled ready/valid register pipeline."""

    def __init__(self, stages: int) -> None:
        self.slots: list[Scalar | None] = [None] * stages

    @property
    def output(self) -> Scalar | None:
        return self.slots[-1]

    def can_advance(self, output_ready: bool) -> bool:
        return self.output is None or output_ready

    def clock(self, incoming: Scalar | None, advance: bool) -> None:
        if advance:
            self.slots = [incoming] + self.slots[:-1]

    def clear(self) -> None:
        self.slots = [None] * len(self.slots)


class PostprocessReference:
    """Cycle model for 2-group FIFO -> round9 -> SiLU6 -> round9 -> write."""

    def __init__(self, table_loaded: bool = False) -> None:
        self.cycle = 0
        self.groups: deque[deque[Scalar]] = deque()
        self.reserved = False
        self.metadata: deque[int] = deque()
        self.pre = Pipe(9)
        self.silu_pipe = Pipe(6)
        self.post = Pipe(9)
        self.fault = False
        self.table_loaded = table_loaded
        self.table_fault = False
        self.table_expected = 1024 if table_loaded else 0
        self.writes: list[tuple[int, int, int]] = []

    @property
    def admission_ready(self) -> bool:
        return (self.table_loaded and not self.table_fault and not self.fault and
                not self.reserved and len(self.groups) < GROUP_DEPTH)

    @property
    def idle(self) -> bool:
        return (not self.groups and not self.reserved and not self.metadata and
                all(item is None for item in self.pre.slots + self.silu_pipe.slots +
                    self.post.slots))

    @property
    def scalar_obligations(self) -> int:
        return (sum(len(group) for group in self.groups) +
                sum(item is not None for item in self.pre.slots) +
                len(self.metadata) +
                sum(item is not None for item in self.post.slots))

    def table_ready(self, address: int) -> bool:
        """A held reload request waits for global drain without blocking that drain."""
        return (self.idle and not self.fault and
                (address == 0 or (not self.table_loaded and not self.table_fault)))

    def load_table(self, address: int) -> bool:
        if not self.table_ready(address):
            return False
        if address == 0:
            self.table_loaded = False
            self.table_fault = False
            self.table_expected = 1
        elif address != self.table_expected:
            self.table_fault = True
        else:
            self.table_expected += 1
            if address == 1023:
                self.table_loaded = True
        return True

    def reserve(self) -> None:
        if not self.admission_ready:
            raise BufferError("no atomic result-group reservation available")
        self.reserved = True
        assert len(self.groups) + int(self.reserved) <= GROUP_DEPTH

    def accept_result(self, group: ResultGroup) -> None:
        if not self.reserved:
            raise RuntimeError("MAC result arrived without a first-beat reservation")
        self.reserved = False
        if group.fault:
            self.fault = True
            self.groups.clear()
            self.metadata.clear()
            self.pre.clear()
            self.silu_pipe.clear()
            self.post.clear()
            return
        self.groups.append(deque(group.scalars()))
        assert len(self.groups) <= GROUP_DEPTH

    def reset(self) -> None:
        self.__init__()

    def step(self, final_ready: bool = True) -> dict[str, object]:
        """Apply one rising edge and report transfers plus post-edge visibility."""
        edge = self.cycle
        if self.fault:
            self.cycle += 1
            return {"edge": edge, "pre_accept": None, "write": None,
                    "output_valid_after": False, "output_after": None,
                    "group_occupancy": 0, "reserved": False,
                    "metadata_occupancy": 0}
        final = self.post.output
        write = final is not None and final_ready and not self.fault

        post_advance = self.post.can_advance(final_ready)
        silu_out = self.silu_pipe.output
        silu_out_ready = post_advance and bool(self.metadata)
        silu_advance = self.silu_pipe.can_advance(silu_out_ready)
        pre_out = self.pre.output
        silu_in_ready = silu_advance and len(self.metadata) < META_DEPTH
        pre_advance = self.pre.can_advance(silu_in_ready)

        pre_in = None
        if pre_advance and self.groups:
            raw = self.groups[0].popleft()
            lane = unpack_tag(raw.tag)[2] % 3
            pre_in = Scalar(round_shift(raw.value * PRE_FACTOR[lane], PRE_SHIFT[lane]), raw.tag)
            if not self.groups[0]:
                self.groups.popleft()

        silu_in = None
        if pre_out is not None and silu_in_ready:
            self.metadata.append(pre_out.tag)
            silu_in = Scalar(silu(pre_out.value), 0)  # SiLU itself has no tag port.

        post_in = None
        if silu_out is not None and silu_out_ready:
            post_in = Scalar(round_shift(silu_out.value * POST_FACTOR, POST_SHIFT),
                             self.metadata.popleft())

        if write:
            self.writes.append((edge, final.tag, sat8(final.value)))

        self.post.clock(post_in, post_advance)
        self.silu_pipe.clock(silu_in, silu_advance)
        self.pre.clock(pre_in, pre_advance)
        self.cycle += 1
        assert len(self.groups) + int(self.reserved) <= GROUP_DEPTH
        assert len(self.metadata) <= META_DEPTH
        assert len(self.metadata) == sum(item is not None for item in self.silu_pipe.slots)
        assert self.scalar_obligations <= 30
        return {
            "edge": edge,
            "pre_accept": pre_in,
            "write": (final.tag, sat8(final.value)) if write else None,
            "output_valid_after": self.post.output is not None and not self.fault,
            "output_after": (self.post.output.tag, sat8(self.post.output.value))
                            if self.post.output is not None and not self.fault else None,
            "group_occupancy": len(self.groups),
            "reserved": self.reserved,
            "metadata_occupancy": len(self.metadata),
            "scalar_obligations": self.scalar_obligations,
            "pre_input_ready": pre_advance and self.table_loaded,
            "group_pop": pre_in is not None and not self.groups,
        }


def self_check() -> dict[str, object]:
    assert round_shift(5, 1) == 2
    assert round_shift(7, 1) == 4
    assert round_shift(-5, 1) == -2
    assert round_shift(-7, 1) == -4
    assert sat8(-129) == -128 and sat8(128) == 127
    assert unpack_tag(pack_tag(1, 15, 31, 63)) == (1, 15, 31, 63)
    assert silu(2046) == 2047 and silu(2047) == 2047 and silu(2048) == 2048

    partial = PostprocessReference()
    for address in range(1023):
        assert partial.load_table(address)
    assert not partial.table_loaded and not partial.admission_ready
    assert partial.load_table(1023) and partial.admission_ready

    model = PostprocessReference(table_loaded=True)
    model.reserve()
    model.accept_result(ResultGroup((99, -48, 77), 0, 3, 0, 0b010))
    trace = [model.step() for _ in range(25)]
    assert trace[0]["pre_accept"] is not None
    assert not any(item["output_valid_after"] for item in trace[:23])
    assert trace[23]["output_valid_after"]
    assert trace[24]["write"] == (pack_tag(0, 3, 1), quantize(-48, 1)[3])

    stalled = PostprocessReference(table_loaded=True)
    stalled.reserve()
    stalled.accept_result(ResultGroup((1, 2, 3), 1, 4, 6, 0b111))
    for _ in range(24):
        stalled.step(False)
    held = stalled.step(False)["output_after"]
    for _ in range(11):
        assert stalled.step(False)["output_after"] == held
    assert stalled.step(True)["write"] == held

    full = PostprocessReference(table_loaded=True)
    for position in range(2):
        full.reserve()
        full.accept_result(ResultGroup((position, position + 1, position + 2),
                                       1, position, 0, 0b111))
    assert not full.admission_ready
    try:
        full.reserve()
    except BufferError:
        pass
    else:
        raise AssertionError("full two-entry group FIFO accepted a third reservation")

    faulted = PostprocessReference(table_loaded=True)
    faulted.reserve()
    faulted.accept_result(ResultGroup((1, 2, 3), 1, 0, 0, 0b111, fault=True))
    assert faulted.fault and not faulted.groups and not faulted.admission_ready
    faulted.reset()
    assert not faulted.admission_ready and not faulted.fault

    # Push while a non-last head scalar is consumed: no alpha duplication.
    continuous = PostprocessReference(table_loaded=True)
    continuous.reserve()
    continuous.accept_result(ResultGroup((10, 11, 12), 1, 0, 0, 0b111))
    assert continuous.step()["pre_accept"].tag == pack_tag(1, 0, 0)
    continuous.reserve()
    continuous.accept_result(ResultGroup((20, 21, 22), 1, 1, 3, 0b111))
    assert continuous.step()["pre_accept"].tag == pack_tag(1, 0, 1)
    while len(continuous.writes) < 6:
        continuous.step()
    assert [tag for _, tag, _ in continuous.writes] == [
        pack_tag(1, 0, 0), pack_tag(1, 0, 1), pack_tag(1, 0, 2),
        pack_tag(1, 1, 3), pack_tag(1, 1, 4), pack_tag(1, 1, 5),
    ]

    # All group FIFO edge combinations: idle, push-only, pop-only, push+pop.
    combos = PostprocessReference(table_loaded=True)
    assert not combos.step()["group_pop"]
    combos.reserve()
    combos.accept_result(ResultGroup((1, 2, 3), 1, 0, 0, 0b111))
    assert not combos.step()["group_pop"]
    pop_only = PostprocessReference(table_loaded=True)
    pop_only.reserve()
    pop_only.accept_result(ResultGroup((1, 2, 3), 0, 0, 0, 0b001))
    assert pop_only.step()["group_pop"]
    both = PostprocessReference(table_loaded=True)
    both.reserve()
    both.accept_result(ResultGroup((1, 2, 3), 0, 0, 0, 0b001))
    both.reserve()
    both.accept_result(ResultGroup((4, 5, 6), 1, 1, 3, 0b111))
    assert both.step()["group_pop"] is False  # Head pops, second group remains.
    assert len(both.groups) == 1 and both.groups[0][0].tag == pack_tag(1, 1, 3)

    # A held address-zero reload waits for every old-table result, but cannot
    # block draining those accepted results.
    reload_wait = PostprocessReference(table_loaded=True)
    reload_wait.reserve()
    reload_wait.accept_result(ResultGroup((7, 8, 9), 1, 2, 0, 0b111))
    waited = 0
    while not reload_wait.table_ready(0):
        assert not reload_wait.load_table(0)
        reload_wait.step(True)
        waited += 1
        assert waited < 64
    assert reload_wait.load_table(0) and not reload_wait.table_loaded

    def backpressure_fill(with_tail: bool) -> tuple[int, int, int]:
        pressure = PostprocessReference(table_loaded=True)
        if with_tail:
            pressure.post.slots[-1] = Scalar(0, pack_tag(1, 0, 0))
        accepted_scalars = 0
        maximum = pressure.scalar_obligations
        denied_edge = -1
        for edge in range(64):
            if edge % 3 == 0:
                if pressure.admission_ready:
                    pressure.reserve()
                    pressure.accept_result(ResultGroup((edge, edge + 1, edge + 2),
                                                       1, edge % 16, 0, 0b111))
                    accepted_scalars += 3
                else:
                    denied_edge = edge
                    break
            event = pressure.step(False)
            maximum = max(maximum, event["scalar_obligations"])
        assert 0 <= denied_edge <= 30 and maximum <= 30
        return denied_edge, accepted_scalars, maximum

    tail_response = backpressure_fill(True)
    empty_response = backpressure_fill(False)

    return {
        "status": "REFERENCE_PASS",
        "fixed_latency": {"pre_accept_to_valid": 23, "pre_accept_to_write": 24},
        "group_fifo_depth": GROUP_DEPTH,
        "metadata_fifo_depth": META_DEPTH,
        "backpressure": {
            "tail_already_valid": {"reservation_denied_edge": tail_response[0],
                                   "accepted_scalars": tail_response[1],
                                   "max_obligations": tail_response[2]},
            "empty_pipeline": {"reservation_denied_edge": empty_response[0],
                               "accepted_scalars": empty_response[1],
                               "max_obligations": empty_response[2]},
            "obligation_bound": 30,
        },
        "quantization": {
            "pre_factor": PRE_FACTOR,
            "pre_shift": PRE_SHIFT,
            "post_factor": POST_FACTOR,
            "post_shift": POST_SHIFT,
            "rounding": "nearest_even",
            "saturation": "int16_each_round_then_int8",
        },
    }


if __name__ == "__main__":
    print(json.dumps(self_check(), sort_keys=True))
