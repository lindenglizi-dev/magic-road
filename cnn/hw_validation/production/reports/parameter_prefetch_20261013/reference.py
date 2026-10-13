"""Cycle reference for down2 parameter snapshots carried by the MAC owner ring."""

from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Parameters:
    pre_multipliers: tuple[int, int, int]
    pre_shifts: tuple[int, int, int]
    post_multiplier: int
    post_shift: int

    def packed(self) -> int:
        return (
            self.pre_multipliers[0]
            | (self.pre_multipliers[1] << 32)
            | (self.pre_multipliers[2] << 64)
            | (self.pre_shifts[0] << 96)
            | (self.pre_shifts[1] << 102)
            | (self.pre_shifts[2] << 108)
            | (self.post_multiplier << 114)
            | (self.post_shift << 146)
        )


@dataclass(frozen=True)
class Task:
    pw: bool
    position: int
    channel: int
    epoch: int


@dataclass(frozen=True)
class Owner:
    task: Task
    parameters: Parameters


class ParameterBank:
    def __init__(self, generation: int = 0) -> None:
        self.load(generation)

    def load(self, generation: int) -> None:
        self.generation = generation
        self.pre_multipliers = [
            0x10000 + generation * 0x1000 + channel * 0x101
            for channel in range(40)
        ]
        self.pre_shifts = [
            (generation * 11 + channel * 7) % 63 for channel in range(40)
        ]
        self.post_multipliers = [
            0x20000 + generation * 0x2000 + layer * 0x111
            for layer in range(2)
        ]
        self.post_shifts = [
            (generation * 13 + layer * 17) % 63 for layer in range(2)
        ]

    def lookup(self, task: Task) -> Parameters:
        if task.pw:
            if task.channel not in range(0, 24, 3):
                raise ValueError("PW channel must be a three-channel group base")
            base = 16 + task.channel
            layer = 1
        else:
            if task.channel not in range(16):
                raise ValueError("DW channel is outside the 16-channel tile")
            base = (task.channel // 3) * 3
            layer = 0
        return Parameters(
            tuple(self.pre_multipliers[base : base + 3]),
            tuple(self.pre_shifts[base : base + 3]),
            self.post_multipliers[layer],
            self.post_shifts[layer],
        )


class OwnerRing:
    """Four existing ownership slots; payload arrays are intentionally not reset."""

    def __init__(self) -> None:
        self.slots: list[Owner | None] = [None] * 4
        self.read = 0
        self.write = 0
        self.count = 0

    def head(self) -> Owner:
        if not self.count:
            raise RuntimeError("ownership ring is empty")
        owner = self.slots[self.read]
        assert owner is not None
        return owner

    def step(
        self,
        offered: Owner | None = None,
        *,
        pop: bool = False,
        rstn: bool = True,
    ) -> tuple[bool, Owner | None]:
        old_head = self.head() if pop and self.count else None
        push = offered is not None and (self.count < 4 or pop)
        if pop and old_head is None:
            raise RuntimeError("cannot pop an empty ownership ring")

        if not rstn:
            self.read = self.write = self.count = 0
            return False, old_head

        # Read-before-write preserves the old head when a full ring pops and pushes one slot.
        if push:
            self.slots[self.write] = offered
            self.write = (self.write + 1) & 3
        if pop:
            self.read = (self.read + 1) & 3
        self.count += int(push) - int(pop)
        return push, old_head


class Reference:
    def __init__(self, bank: ParameterBank, epoch: int = 0) -> None:
        self.bank = bank
        self.epoch = epoch
        self.ring = OwnerRing()
        self.active: Owner | None = None
        self.active_lane = 0
        self.terminal_fault = False

    def offer(self, task: Task, *, pop: bool = False) -> tuple[bool, Owner | None]:
        if self.terminal_fault:
            raise RuntimeError("terminal fault blocks new ownership")
        if task.epoch != self.epoch:
            raise ValueError("task epoch is stale")
        owner = Owner(task, self.bank.lookup(task))
        return self.ring.step(owner, pop=pop)

    def pop_pw(self) -> Owner:
        if self.terminal_fault:
            raise RuntimeError("terminal fault blocks result transfer")
        _, owner = self.ring.step(pop=True)
        assert owner is not None and owner.task.pw
        return owner

    def pop_dw(self) -> Owner:
        if self.terminal_fault:
            raise RuntimeError("terminal fault blocks result transfer")
        _, owner = self.ring.step(pop=True)
        assert owner is not None and not owner.task.pw
        self.active = owner
        self.active_lane = 0
        return owner

    def dw_view(self) -> Owner:
        if self.active is None:
            raise RuntimeError("DW active slot is empty")
        return self.active

    def accept_dw_scalar(self) -> None:
        owner = self.dw_view()
        count = 3 if owner.task.position % 4 == 0 else 1
        self.active_lane += 1
        if self.active_lane == count:
            self.active = None
            self.active_lane = 0

    def reset(self, epoch: int) -> None:
        self.epoch = epoch
        self.ring.step(rstn=False)
        self.active = None
        self.active_lane = 0
        self.terminal_fault = False

    def fault(self) -> None:
        self.terminal_fault = True
        self.active = None
        self.active_lane = 0


def assert_legacy_match(bank: ParameterBank, owner: Owner) -> None:
    expected = bank.lookup(owner.task)
    assert owner.parameters == expected
    packet = owner.parameters.packed()
    assert packet.bit_length() <= 152
    assert tuple((packet >> (32 * lane)) & 0xFFFFFFFF for lane in range(3)) == expected.pre_multipliers
    assert tuple((packet >> (96 + 6 * lane)) & 0x3F for lane in range(3)) == expected.pre_shifts
    assert (packet >> 114) & 0xFFFFFFFF == expected.post_multiplier
    assert (packet >> 146) & 0x3F == expected.post_shift


def self_check() -> dict[str, int | str]:
    bank = ParameterBank()
    model = Reference(bank)
    comparisons = transfers = 0

    # Frozen legacy lookup and prefetched records agree for every DW channel/position.
    for channel in range(16):
        for origin in (0, 3, 4, 7, 8, 11, 12, 15):
            task = Task(False, origin, channel, 0)
            pushed, _ = model.offer(task)
            assert pushed
            owner = model.pop_dw()
            transfers += 1
            scalar_count = 3 if origin % 4 == 0 else 1
            for lane in range(scalar_count):
                view = model.dw_view()
                assert view.task.position + lane in range(16)
                assert_legacy_match(bank, view)
                comparisons += 1
                model.accept_dw_scalar()

    # PW-only traffic covers every output group and position with stalls on the head.
    for position in range(16):
        for channel in range(0, 24, 3):
            task = Task(True, position, channel, 0)
            pushed, _ = model.offer(task)
            assert pushed
            held = model.ring.head()
            for _ in range((position + channel) % 3):
                assert model.ring.head() == held
                assert_legacy_match(bank, held)
                comparisons += 1
            owner = model.pop_pw()
            assert owner == held
            assert_legacy_match(bank, owner)
            comparisons += 1
            transfers += 1

    # Full-ring backpressure, simultaneous old-head pop/new-tail push, and pointer wrap.
    expected: list[Owner] = []
    for index in range(4):
        task = Task(True, index, (index % 8) * 3, 0)
        pushed, _ = model.offer(task)
        assert pushed
        expected.append(model.ring.slots[(model.ring.write - 1) & 3])
    stalled = Task(True, 9, 0, 0)
    before = (model.ring.read, model.ring.write, model.ring.count)
    pushed, popped = model.offer(stalled)
    assert not pushed and popped is None
    assert (model.ring.read, model.ring.write, model.ring.count) == before
    for index in range(12):
        task = Task(True, index & 15, ((index + 4) % 8) * 3, 0)
        new_owner = Owner(task, bank.lookup(task))
        pushed, popped = model.ring.step(new_owner, pop=True)
        assert pushed and popped == expected.pop(0) and model.ring.count == 4
        assert_legacy_match(bank, popped)
        expected.append(new_owner)
        comparisons += 1
        transfers += 1
    assert model.ring.read == model.ring.write == 0
    while model.ring.count:
        popped = model.pop_pw()
        assert popped == expected.pop(0)
        transfers += 1

    # Reload is legal only outside work: old accepted owners retain the old snapshot.
    old_task = Task(True, 2, 6, 0)
    assert model.offer(old_task)[0]
    old_owner = model.ring.head()
    old_parameters = old_owner.parameters
    bank.load(1)  # Deliberate test injection; RTL loads are forbidden while busy.
    assert model.ring.head().parameters == old_parameters
    assert model.ring.head().parameters != bank.lookup(old_task)
    assert model.pop_pw() == old_owner
    new_task = Task(True, 2, 6, 0)
    assert model.offer(new_task)[0]
    assert_legacy_match(bank, model.pop_pw())
    comparisons += 2
    transfers += 2

    # Semantic predecessor/successor ownership; the TB covers exact same-edge replacement.
    first = Task(False, 3, 5, 0)
    second = Task(False, 4, 14, 0)
    assert model.offer(first)[0] and model.offer(second)[0]
    assert model.pop_dw().task == first
    model.accept_dw_scalar()
    assert model.active is None
    assert model.pop_dw().task == second
    for _ in range(3):
        assert_legacy_match(bank, model.dw_view())
        comparisons += 1
        model.accept_dw_scalar()
    assert model.active is None
    transfers += 2

    # Fault is terminal until reset; raw ring payload/count remain but cannot become valid.
    assert model.offer(Task(True, 1, 0, 0))[0]
    stale_slot = model.ring.slots[model.ring.read]
    stale_count = model.ring.count
    model.fault()
    assert model.ring.count == stale_count and model.active is None and stale_slot is not None
    try:
        model.offer(Task(False, 0, 0, 0))
        raise AssertionError("terminal fault accepted new ownership")
    except RuntimeError:
        pass
    model.reset(0)
    assert model.offer(Task(False, 0, 0, 0))[0]
    model.pop_dw()
    stale_active = model.active
    model.reset(1)
    assert model.ring.count == 0 and model.active is None and stale_active is not None
    try:
        model.offer(Task(True, 0, 0, 0))
        raise AssertionError("stale epoch was accepted")
    except ValueError:
        pass
    assert model.offer(Task(True, 0, 0, 1))[0]
    assert_legacy_match(bank, model.pop_pw())
    comparisons += 1
    transfers += 1

    result = {
        "status": "PASS",
        "record_bits": 152,
        "legacy_prefetch_comparisons": comparisons,
        "accepted_result_transfers": transfers,
        "full_ring_same_cycle_pop_push": 12,
        "epochs_checked": 2,
    }
    print("PARAMETER_PREFETCH_REFERENCE_PASS " + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    self_check()
