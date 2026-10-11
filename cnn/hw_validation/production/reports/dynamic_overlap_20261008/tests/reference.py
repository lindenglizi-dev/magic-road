"""Numeric and ordered-retirement golden model for the overlapped postprocess core."""

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
REPORT = HERE.parent
REPORTS = REPORT.parent
PRODUCTION = REPORTS.parent
PROJECT = HERE.parents[5]
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PRODUCTION))

from cnn import integer  # noqa: E402


def unpack(value, width, count, signed=False):
    mask = (1 << width) - 1
    items = [(value >> (width * lane)) & mask for lane in range(count)]
    if signed:
        items = [item - (1 << width) if item & (1 << (width - 1)) else item
                 for item in items]
    return tuple(items)


@dataclass(frozen=True)
class Batch:
    accumulators: tuple[int, int, int]
    multipliers: tuple[int, int, int]
    shifts: tuple[int, int, int]
    post_multiplier: int
    post_shift: int
    activate: bool
    mask: int
    tags: tuple[int, int, int]
    input_fault: bool = False

    @property
    def active_lanes(self):
        return tuple(lane for lane in range(3) if self.mask & (1 << lane))


def bad_parameters(batch):
    return (not batch.active_lanes or
            any(batch.multipliers[lane] >= 1 << 31 or batch.shifts[lane] > 62
                for lane in batch.active_lanes) or
            batch.activate and (batch.post_multiplier >= 1 << 31 or batch.post_shift > 62))


def numeric_lanes(batch):
    """Return active lane results as {lane: (data, tag, output_int16)}."""
    if batch.input_fault or bad_parameters(batch):
        raise ValueError("fault batch has no numeric outputs")
    results = {}
    for lane in batch.active_lanes:
        pre = int(integer.requantize(np.array(batch.accumulators[lane]),
                                     batch.multipliers[lane], batch.shifts[lane],
                                     -32768, 32767))
        if batch.activate:
            activated = int(integer.silu(np.array(pre)))
            data = int(integer.requantize(np.array(activated),
                                          batch.post_multiplier, batch.post_shift))
        else:
            data = pre
        results[lane] = (data, batch.tags[lane], not batch.activate)
    return results


@dataclass
class Slot:
    sequence: int
    batch: Batch
    results: dict[int, tuple[int, int, bool]] = field(default_factory=dict)
    fault: bool = False
    emitted: int = 0

    @property
    def complete(self):
        return self.fault or all(lane in self.results for lane in self.batch.active_lanes)


class MetaFifo:
    """Eight-entry ready/valid FIFO with registered-capacity backpressure."""

    def __init__(self, depth=8):
        self.depth = depth
        self.items = deque()

    def cycle(self, push=None, pop_ready=False):
        push_ready = len(self.items) < self.depth
        popped = self.items.popleft() if pop_ready and self.items else None
        if push is not None and push_ready:
            self.items.append(push)
        return popped, push_ready


class OrderedScheduler:
    """Logical scheduler contract; pipeline latency is intentionally not modeled."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.ingress = deque()
        self.retirement = deque()
        self.slots = {}
        self.next_sequence = 0
        self.stop = False
        self.fault = False

    @property
    def input_ready(self):
        return not self.stop and len(self.ingress) < 2 and len(self.retirement) < 8

    def accept(self, batch):
        if not self.input_ready:
            return None
        sequence = self.next_sequence
        self.next_sequence += 1
        slot = Slot(sequence, batch)
        self.slots[sequence] = slot
        self.retirement.append(sequence)  # reservation is atomic with acceptance
        if batch.input_fault or bad_parameters(batch):
            self.detect_fault(sequence)
        else:
            self.ingress.append(sequence)
        return sequence

    def take_ingress(self):
        return self.ingress.popleft() if self.ingress else None

    def complete_numeric(self, sequence):
        slot = self.slots.get(sequence)
        if slot is not None and not slot.fault:
            slot.results.update(numeric_lanes(slot.batch))
        try:
            self.ingress.remove(sequence)
        except ValueError:
            pass

    def writeback(self, raw=None, post=None):
        """Single result port: post wins; a colliding raw result must retry."""
        selected = post if post is not None else raw
        if selected is not None:
            sequence, lane, value = selected
            slot = self.slots.get(sequence)
            if slot is not None and not slot.fault:
                slot.results[lane] = value
        return raw is not None and post is None, post is not None

    def detect_fault(self, sequence):
        slot = self.slots.get(sequence)
        if slot is None:
            return
        slot.fault = True
        slot.results.clear()
        self.stop = True
        # Already accepted younger work may still issue, but ordered retirement
        # keeps it invisible and flushes it only when this fault reaches the head.

    def _promote_fault(self):
        if self.retirement and self.slots[self.retirement[0]].fault:
            sequence = self.retirement.popleft()
            self.slots.pop(sequence)
            self.retirement.clear()
            self.slots.clear()
            self.ingress.clear()
            self.fault = True

    def output(self):
        self._promote_fault()
        if self.fault or not self.retirement:
            return None
        slot = self.slots[self.retirement[0]]
        if not slot.complete:
            return None
        lane = slot.batch.active_lanes[slot.emitted]
        return slot.results[lane]

    def step_output(self, ready):
        value = self.output()
        if value is None or not ready:
            return value
        slot = self.slots[self.retirement[0]]
        slot.emitted += 1
        if slot.emitted == len(slot.batch.active_lanes):
            sequence = self.retirement.popleft()
            self.slots.pop(sequence)
            self._promote_fault()
        return value


def parse_batches(path):
    batches = []
    packed_expected = []
    for line in path.read_text(encoding="ascii").splitlines():
        acc, mul, shifts, post_mul, post_shift, activate, mask, tags, expected = (
            int(item, 16) for item in line.split())
        batches.append(Batch(unpack(acc, 32, 3, True), unpack(mul, 32, 3),
                             unpack(shifts, 6, 3), post_mul, post_shift,
                             bool(activate), mask, unpack(tags, 16, 3)))
        packed_expected.append(unpack(expected, 16, 3, True))
    return batches, packed_expected


def self_check():
    diagnostic = REPORTS / "diagnostic_repair_20261008" / "candidate_sim"
    old = REPORTS / "dynamic_control_timing_20261008" / "candidate"
    # production/numeric_package.py re-exports this table but imports training-only
    # graph dependencies; use its existing numeric source directly for this RTL test.
    table = integer.tables()["silu"]
    table_words = [int(line, 16) for line in (diagnostic / "table.hex").read_text().splitlines()]
    assert table_words == [int(value) & 0xffff for value in table]

    batches, expected = parse_batches(diagnostic / "batches.txt")
    actual = []
    for batch, packed in zip(batches, expected):
        results = numeric_lanes(batch)
        assert all(results[lane][0] == packed[lane] for lane in batch.active_lanes)
        actual.extend((results[lane][1], results[lane][0], int(results[lane][2]))
                      for lane in batch.active_lanes)
    saved = [tuple(map(int, line.split(',')))
             for line in (old / "results.csv").read_text().splitlines()]
    assert actual == saved
    assert len(batches) == 330 and len(actual) == 604
    assert {batch.mask for batch in batches} == set(range(1, 8))

    raw = Batch((5, 7, -5), (1, 1, 1), (1, 1, 1), 1, 0, False, 7,
                (0x22, 0x22, 0x22))
    activated = Batch((256, -256, 2048), (1, 3, 5), (0, 1, 2), 3, 1, True, 7,
                      (0x22, 0x22, 0x22))
    scheduler = OrderedScheduler()
    first = scheduler.accept(raw)
    second = scheduler.accept(activated)
    assert first == 0 and second == 1 and not scheduler.input_ready
    scheduler.complete_numeric(second)  # younger may finish first
    scheduler.complete_numeric(first)
    held = scheduler.output()
    for _ in range(100):
        assert scheduler.step_output(False) == held
    retired = [scheduler.step_output(True) for _ in range(6)]
    assert retired == [numeric_lanes(raw)[lane] for lane in raw.active_lanes] + [
        numeric_lanes(activated)[lane] for lane in activated.active_lanes]

    # Fault is detected behind a half-emitted older batch: finish old batch, then publish fault.
    scheduler.reset()
    good = scheduler.accept(raw)
    late_fault = scheduler.accept(activated)
    scheduler.complete_numeric(good)
    assert scheduler.step_output(True) == numeric_lanes(raw)[0]
    scheduler.detect_fault(late_fault)
    assert not scheduler.input_ready and not scheduler.fault
    assert scheduler.step_output(True) == numeric_lanes(raw)[1]
    assert scheduler.step_output(True) == numeric_lanes(raw)[2]
    assert scheduler.fault and scheduler.output() is None

    # Already accepted younger work may finish, but is flushed only at fault retirement.
    scheduler.reset()
    older = scheduler.accept(raw)
    scheduler.take_ingress()
    fault_candidate = scheduler.accept(raw)
    scheduler.take_ingress()
    younger = scheduler.accept(activated)
    scheduler.detect_fault(fault_candidate)
    assert younger in scheduler.slots and not scheduler.input_ready
    scheduler.complete_numeric(younger)
    scheduler.complete_numeric(older)
    for lane in raw.active_lanes:
        assert scheduler.step_output(True) == numeric_lanes(raw)[lane]
    assert scheduler.fault and younger not in scheduler.slots

    # One writeback port gives POST priority; the colliding raw result retries.
    scheduler.reset()
    a = scheduler.accept(Batch((1, 0, 0), (1, 1, 1), (0, 0, 0), 1, 0,
                               False, 1, (1, 1, 1)))
    scheduler.take_ingress()
    b = scheduler.accept(Batch((0, 2, 0), (1, 1, 1), (0, 0, 0), 1, 0,
                               True, 2, (2, 2, 2)))
    raw_accepted, post_accepted = scheduler.writeback(
        raw=(a, 0, (1, 1, True)), post=(b, 1, (2, 2, False)))
    assert not raw_accepted and post_accepted and not scheduler.slots[a].complete
    assert scheduler.writeback(raw=(a, 0, (1, 1, True))) == (True, False)
    assert scheduler.slots[a].complete and scheduler.slots[b].complete

    fifo = MetaFifo()
    for item in range(8):
        assert fifo.cycle(item)[1]
    assert not fifo.cycle(99)[1]
    popped, pushed = fifo.cycle(8, True)
    assert (popped, pushed, tuple(fifo.items)) == (0, False, tuple(range(1, 8)))

    # Eight accepted batches reserve all retirement slots even after leaving ingress.
    scheduler.reset()
    for _ in range(8):
        assert scheduler.accept(raw) is not None
        scheduler.take_ingress()
    assert not scheduler.input_ready and scheduler.accept(raw) is None
    scheduler.reset()
    assert scheduler.input_ready and not scheduler.fault and not scheduler.retirement

    print("REFERENCE_PASS batches=330 outputs=604 masks=7 retire_depth=8 ingress_depth=2 meta_depth=8")


if __name__ == "__main__":
    self_check()
