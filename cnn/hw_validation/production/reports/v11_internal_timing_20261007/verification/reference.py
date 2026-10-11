"""Independent numeric and handshake model for the v11 pre-round elastic cut."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path


PRE_FACTOR = (1, 3, 5)
PRE_SHIFT = (0, 2, 4)
POST_SHIFT = 4
GROUP_DEPTH = 2
META_DEPTH = 8
PRE_STAGES = 9
SILU_STAGES = 6
POST_STAGES = 9
MAX_OBLIGATIONS = GROUP_DEPTH * 3 + 1 + PRE_STAGES + SILU_STAGES + POST_STAGES
ROOT = Path(__file__).resolve().parent
FROZEN_SILU = (ROOT.parents[1] / "v8_reset_layer_tiles_20261007" /
               "layers" / "vectors" / "silu.hex")
FROZEN_SILU_SHA256 = "305db026a2961c891369dfe4c9191a27adc89cf80f6ad8b6ac5042e09cf2de43"


def round_shift(value: int, shift: int) -> int:
    if not 0 <= shift < 63:
        raise ValueError(f"illegal shift: {shift}")
    magnitude = abs(value)
    quotient, remainder = divmod(magnitude, 1 << shift)
    half = 0 if shift == 0 else 1 << (shift - 1)
    if shift and (remainder > half or (remainder == half and quotient & 1)):
        quotient += 1
    rounded = -quotient if value < 0 else quotient
    return max(-32768, min(32767, rounded))


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
    if value <= -2048:
        return 0
    if value >= 2048:
        return value
    address = round_shift(value, 2) + 512
    return 2047 if address == 1024 else SILU_TABLE[address]


def sat8(value: int) -> int:
    return max(-128, min(127, value))


def pack_tag(layer: int, position: int, channel: int) -> int:
    if not (0 <= layer < 2 and 0 <= position < 16 and 0 <= channel < 32):
        raise ValueError("tag field out of range")
    return (layer << 15) | (position << 11) | (channel << 6)


def unpack_tag(tag: int) -> tuple[int, int, int, int]:
    return tag >> 15, (tag >> 11) & 0xF, (tag >> 6) & 0x1F, tag & 0x3F


def quantize(accumulator: int, lane: int) -> tuple[int, int, int, int]:
    pre = round_shift(accumulator * PRE_FACTOR[lane], PRE_SHIFT[lane])
    activated = silu(pre)
    post = round_shift(activated, POST_SHIFT)
    return pre, activated, post, sat8(post)


@dataclass(frozen=True)
class Scalar:
    value: int
    tag: int


@dataclass(frozen=True)
class CutToken:
    product: int
    shift: int
    tag: int


@dataclass(frozen=True)
class ResultGroup:
    values: tuple[int, int, int]
    layer: int
    position: int
    channel_base: int
    lane_mask: int
    fault: bool = False

    def __post_init__(self) -> None:
        if not (0 <= self.position < 16 and self.channel_base % 3 == 0):
            raise ValueError("position or aligned channel base invalid")
        if self.layer == 0:
            if (self.channel_base > 15 or self.lane_mask not in (1, 2, 4) or
                    self.channel_base + self.lane_mask.bit_length() - 1 > 15):
                raise ValueError("DW lane shape invalid")
        elif self.layer == 1:
            if self.channel_base > 21 or self.lane_mask != 0b111:
                raise ValueError("PW lane shape invalid")
        else:
            raise ValueError("layer invalid")

    def scalars(self) -> tuple[Scalar, ...]:
        if self.fault:
            return ()
        return tuple(
            Scalar(value, pack_tag(self.layer, self.position, self.channel_base + lane))
            for lane, value in enumerate(self.values) if self.lane_mask & (1 << lane)
        )


class Pipe:
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


class ElasticPostprocessReference:
    """2 group FIFO -> elastic cut1 -> round9 -> SiLU6 -> round9."""

    def __init__(self, table_loaded: bool = False) -> None:
        self.cycle = 0
        self.groups: deque[deque[Scalar]] = deque()
        self.reserved = False
        self.cut: CutToken | None = None
        self.pre = Pipe(PRE_STAGES)
        self.silu_pipe = Pipe(SILU_STAGES)
        self.metadata: deque[int] = deque()
        self.post = Pipe(POST_STAGES)
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
        return (not self.groups and not self.reserved and self.cut is None and
                not self.metadata and all(item is None for item in
                                          self.pre.slots + self.silu_pipe.slots +
                                          self.post.slots))

    @property
    def scalar_obligations(self) -> int:
        return (sum(len(group) for group in self.groups) + int(self.cut is not None) +
                sum(item is not None for item in self.pre.slots) + len(self.metadata) +
                sum(item is not None for item in self.post.slots))

    @property
    def pre_occupancy(self) -> int:
        return int(self.cut is not None) + sum(item is not None for item in self.pre.slots)

    def table_ready(self, address: int) -> bool:
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
            raise BufferError("no atomic group reservation")
        self.reserved = True
        assert len(self.groups) + int(self.reserved) <= GROUP_DEPTH

    def accept_result(self, group: ResultGroup) -> None:
        if not self.reserved:
            raise RuntimeError("MAC result without reservation")
        self.reserved = False
        if group.fault:
            self._cancel_fault()
            return
        self.groups.append(deque(group.scalars()))
        assert len(self.groups) <= GROUP_DEPTH

    def _cancel_fault(self) -> None:
        self.fault = True
        self.groups.clear()
        self.cut = None
        self.metadata.clear()
        self.pre.clear()
        self.silu_pipe.clear()
        self.post.clear()

    def reset(self) -> None:
        self.__init__()

    def step(self, final_ready: bool = True) -> dict[str, object]:
        """Apply one edge; output_valid_after is NBA-visible state after that edge."""
        edge = self.cycle
        if self.fault:
            self.cycle += 1
            return {"edge": edge, "cut_accept": None, "round_accept": None,
                    "write": None, "output_valid_after": False,
                    "scalar_obligations": 0, "pre_occupancy": 0}

        final = self.post.output
        write = final is not None and final_ready
        post_advance = self.post.can_advance(final_ready)
        silu_out = self.silu_pipe.output
        silu_out_ready = post_advance and bool(self.metadata)
        silu_advance = self.silu_pipe.can_advance(silu_out_ready)
        pre_out = self.pre.output
        silu_in_ready = silu_advance and len(self.metadata) < META_DEPTH
        pre_advance = self.pre.can_advance(silu_in_ready)

        old_cut = self.cut
        cut_ready = old_cut is None or pre_advance
        cut_in = None
        if cut_ready and self.groups:
            raw = self.groups[0].popleft()
            lane = unpack_tag(raw.tag)[2] % 3
            cut_in = CutToken(raw.value * PRE_FACTOR[lane], PRE_SHIFT[lane], raw.tag)
            if not self.groups[0]:
                self.groups.popleft()

        round_in = None
        if old_cut is not None and pre_advance:
            round_in = Scalar(round_shift(old_cut.product, old_cut.shift), old_cut.tag)

        silu_in = None
        if pre_out is not None and silu_in_ready:
            self.metadata.append(pre_out.tag)
            silu_in = Scalar(silu(pre_out.value), 0)

        post_in = None
        if silu_out is not None and silu_out_ready:
            post_in = Scalar(round_shift(silu_out.value, POST_SHIFT),
                             self.metadata.popleft())

        if write:
            self.writes.append((edge, final.tag, sat8(final.value)))

        self.post.clock(post_in, post_advance)
        self.silu_pipe.clock(silu_in, silu_advance)
        self.pre.clock(round_in, pre_advance)
        if cut_ready:
            self.cut = cut_in
        self.cycle += 1

        assert len(self.groups) + int(self.reserved) <= GROUP_DEPTH
        assert len(self.metadata) <= META_DEPTH
        assert len(self.metadata) == sum(item is not None for item in self.silu_pipe.slots)
        assert self.pre_occupancy <= PRE_STAGES + 1
        assert self.scalar_obligations <= MAX_OBLIGATIONS
        return {
            "edge": edge,
            "cut_accept": cut_in,
            "round_accept": round_in,
            "write": (final.tag, sat8(final.value)) if write else None,
            "output_valid_after": self.post.output is not None,
            "output_after": ((self.post.output.tag, sat8(self.post.output.value))
                             if self.post.output is not None else None),
            "group_occupancy": len(self.groups),
            "cut_valid": self.cut is not None,
            "metadata_occupancy": len(self.metadata),
            "pre_occupancy": self.pre_occupancy,
            "scalar_obligations": self.scalar_obligations,
            "cut_ready": cut_ready,
        }


def self_check() -> dict[str, object]:
    assert round_shift(5, 1) == 2 and round_shift(7, 1) == 4
    assert round_shift(-5, 1) == -2 and round_shift(-7, 1) == -4
    assert silu(2046) == 2047 and silu(2047) == 2047 and silu(2048) == 2048
    assert MAX_OBLIGATIONS == 31

    # Numeric behavior is exactly the frozen v10 quantization contract.
    for lane in range(3):
        for value in (-2**31, -32769, -1, 0, 1, 32768, 2**31 - 1):
            pre, active, post, output = quantize(value, lane)
            assert output == sat8(post) and active == silu(pre)

    partial = ElasticPostprocessReference()
    for address in range(1023):
        assert partial.load_table(address)
    assert not partial.table_loaded and not partial.admission_ready
    assert partial.load_table(1023) and partial.admission_ready

    single = ElasticPostprocessReference(table_loaded=True)
    single.reserve()
    single.accept_result(ResultGroup((99, -48, 77), 0, 3, 0, 0b010))
    trace = [single.step() for _ in range(27)]
    assert trace[0]["cut_accept"] is not None and trace[0]["round_accept"] is None
    assert trace[1]["round_accept"] is not None
    assert not any(item["output_valid_after"] for item in trace[:24])
    assert trace[24]["output_valid_after"]
    assert trace[25]["write"] == (pack_tag(0, 3, 1), quantize(-48, 1)[3])

    # Empty/full same-edge replacement preserves scalar II=1.
    continuous = ElasticPostprocessReference(table_loaded=True)
    cut_edges = []
    round_edges = []
    accepted_groups = 0
    for _ in range(80):
        if accepted_groups < 12 and continuous.admission_ready:
            continuous.reserve()
            continuous.accept_result(ResultGroup(
                (accepted_groups * 3, accepted_groups * 3 + 1,
                 accepted_groups * 3 + 2), 1, accepted_groups % 16, 0, 0b111))
            accepted_groups += 1
        event = continuous.step(True)
        if event["cut_accept"] is not None:
            cut_edges.append(event["edge"])
        if event["round_accept"] is not None:
            round_edges.append(event["edge"])
        if len(continuous.writes) == 36:
            break
    assert len(cut_edges) == len(round_edges) == len(continuous.writes) == 36
    assert all(right - left == 1 for left, right in zip(cut_edges, cut_edges[1:]))
    assert all(right - left == 1 for left, right in zip(round_edges, round_edges[1:]))

    # A held output remains stable and backpressure can fill the new cut.
    held_model = ElasticPostprocessReference(table_loaded=True)
    held_model.reserve()
    held_model.accept_result(ResultGroup((1, 2, 3), 1, 4, 0, 0b111))
    for _ in range(25):
        held_model.step(False)
    held = held_model.step(False)["output_after"]
    for _ in range(11):
        assert held_model.step(False)["output_after"] == held
    assert held_model.step(True)["write"] == held

    # Held reload waits for the cut and every old-table stage to drain.
    reload_wait = ElasticPostprocessReference(table_loaded=True)
    reload_wait.reserve()
    reload_wait.accept_result(ResultGroup((7, 8, 9), 1, 2, 0, 0b111))
    waited = 0
    while not reload_wait.table_ready(0):
        assert not reload_wait.load_table(0)
        reload_wait.step(True)
        waited += 1
        assert waited < 80
    assert reload_wait.load_table(0) and not reload_wait.table_loaded

    # Terminal fault atomically cancels the cut and all older obligations.
    faulted = ElasticPostprocessReference(table_loaded=True)
    faulted.reserve()
    faulted.accept_result(ResultGroup((1, 2, 3), 1, 0, 0, 0b111))
    faulted.step(False)
    assert faulted.cut is not None
    faulted.reserve()
    faulted.accept_result(ResultGroup((4, 5, 6), 1, 1, 3, 0b111, fault=True))
    assert faulted.fault and faulted.scalar_obligations == 0
    faulted.reset()
    assert not faulted.fault and not faulted.table_loaded

    def pressure_fill(with_tail: bool) -> tuple[int, int, int, int, int]:
        model = ElasticPostprocessReference(table_loaded=True)
        if with_tail:
            model.post.slots[-1] = Scalar(0, pack_tag(1, 0, 0))
        accepted_scalars = 0
        maximum = model.scalar_obligations
        max_pre = model.pre_occupancy
        last_accept_edge = -1
        deny_streak = 0
        maximum_deny_streak = 0
        for edge in range(96):
            if model.admission_ready:
                model.reserve()
                model.accept_result(ResultGroup((edge, edge + 1, edge + 2),
                                                 1, edge % 16, 0, 0b111))
                accepted_scalars += 3
                last_accept_edge = edge
                deny_streak = 0
            else:
                deny_streak += 1
                maximum_deny_streak = max(maximum_deny_streak, deny_streak)
            event = model.step(False)
            maximum = max(maximum, event["scalar_obligations"])
            max_pre = max(max_pre, event["pre_occupancy"])
        assert last_accept_edge >= 0 and maximum <= MAX_OBLIGATIONS and max_pre <= 10
        assert maximum_deny_streak >= 32
        return last_accept_edge + 1, accepted_scalars, maximum, max_pre, maximum_deny_streak

    tail = pressure_fill(True)
    empty = pressure_fill(False)
    assert empty[2] <= MAX_OBLIGATIONS and tail[2] <= MAX_OBLIGATIONS

    return {
        "status": "REFERENCE_PASS",
        "cut": {
            "depth": 1,
            "payload": ["signed_product_64", "shift_6", "tag_16"],
            "ready": "not valid or pre_round_advance",
            "same_edge_replace": True,
        },
        "latency": {
            "scalar_accept_to_output_valid_after_nba": 24,
            "scalar_accept_to_first_write_edge": 25,
            "extra_accepted_advance_cycles_vs_v10": 1,
            "scalar_ii": 1,
        },
        "capacity": {
            "group_fifo": 2, "pre_cut_plus_round": 10,
            "metadata_silu": 6, "post_round": 9,
            "structural_scalar_obligation_upper_bound": MAX_OBLIGATIONS,
        },
        "pressure_model": {
            "tail_already_valid": {"denied_edge": tail[0], "accepted_scalars": tail[1],
                                   "max_obligations": tail[2], "max_pre": tail[3],
                                   "longest_deny_streak": tail[4]},
            "empty_pipeline": {"denied_edge": empty[0], "accepted_scalars": empty[1],
                               "max_obligations": empty[2], "max_pre": empty[3],
                               "longest_deny_streak": empty[4]},
        },
        "numeric": {
            "pre_factor": PRE_FACTOR, "pre_shift": PRE_SHIFT,
            "post_factor": 1, "post_shift": POST_SHIFT,
            "rounding": "nearest_even", "saturation": "int16_then_int8",
            "silu_table_sha256": FROZEN_SILU_SHA256,
        },
    }


if __name__ == "__main__":
    print(json.dumps(self_check(), sort_keys=True))
