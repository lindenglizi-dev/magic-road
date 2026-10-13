"""Cycle reference for the shared-core one-entry SiLU table command buffer."""

from dataclasses import dataclass
import json
import random


@dataclass(frozen=True)
class Cycle:
    ready: bool
    push: bool
    pop: bool
    blocked: bool
    pp_valid: bool
    pp_addr: int
    pp_data: int


class TableBuffer:
    def __init__(self) -> None:
        self.pending = False
        self.addr = 0
        self.data = 0

    def step(
        self,
        *,
        rstn: bool = True,
        admission: bool = True,
        valid: bool = False,
        addr: int = 0,
        data: int = 0,
        pp_ready: bool = False,
        table_loaded: bool = False,
    ) -> Cycle:
        if not 0 <= addr < 1024 or not -(1 << 15) <= data < (1 << 15):
            raise ValueError("table command is outside the RTL payload width")

        legal = addr == 0 or (
            not table_loaded and not (self.pending and self.addr == 1023)
        )
        ready = rstn and admission and (not self.pending or pp_ready) and legal
        push = valid and ready
        pop = rstn and self.pending and pp_ready
        cycle = Cycle(
            ready=ready,
            push=push,
            pop=pop,
            blocked=rstn and self.pending,
            pp_valid=rstn and self.pending,
            pp_addr=self.addr,
            pp_data=self.data,
        )

        if not rstn:
            self.pending = False
            self.addr = 0
            self.data = 0
        elif push:
            self.pending = True
            self.addr = addr
            self.data = data
        elif pop:
            self.pending = False
        return cycle


class TableSink:
    def __init__(self) -> None:
        self.loaded = False
        self.fault = False
        self.expected = 0
        self.writes: list[tuple[int, int]] = []

    def ready(self, valid: bool, addr: int) -> bool:
        return not self.fault and (not valid or addr == 0 or not self.loaded)

    def accept(self, cycle: Cycle) -> None:
        if not cycle.pop:
            return
        self.writes.append((cycle.pp_addr, cycle.pp_data))
        if cycle.pp_addr == 0:
            self.loaded = False
            self.fault = False
            self.expected = 1
        elif cycle.pp_addr != self.expected:
            self.loaded = False
            self.fault = True
            self.expected = 0
        elif cycle.pp_addr == 1023:
            self.loaded = True
            self.expected = 0
        else:
            self.expected += 1

    def reset(self) -> None:
        self.loaded = False
        self.fault = False
        self.expected = 0
        self.writes.clear()


def transfer(
    buffer: TableBuffer,
    sink: TableSink,
    *,
    valid: bool,
    addr: int,
    data: int,
    admission: bool = True,
    force_ready: bool | None = None,
) -> Cycle:
    pp_ready = (
        sink.ready(buffer.pending, buffer.addr)
        if force_ready is None
        else force_ready
    )
    cycle = buffer.step(
        admission=admission,
        valid=valid,
        addr=addr,
        data=data,
        pp_ready=pp_ready,
        table_loaded=sink.loaded,
    )
    sink.accept(cycle)
    return cycle


def load_table(
    buffer: TableBuffer, sink: TableSink, rng: random.Random
) -> tuple[int, int]:
    address = 0
    cycles = 0
    simultaneous = 0
    while address < 1024 or buffer.pending:
        cycles += 1
        offer = address < 1024 and rng.randrange(4) != 0
        cycle = transfer(
            buffer,
            sink,
            valid=offer,
            addr=address if address < 1024 else 0,
            data=((address * 73 + 19) & 0xFFFF) - 0x8000,
        )
        if cycle.push:
            address += 1
        simultaneous += cycle.push and cycle.pop
        assert cycles < 4096
    assert sink.loaded and not sink.fault
    assert [addr for addr, _ in sink.writes] == list(range(1024))
    return cycles, simultaneous


def self_check() -> dict[str, int | str]:
    seed = 20261013
    rng = random.Random(seed)
    buffer, sink = TableBuffer(), TableSink()

    first = transfer(buffer, sink, valid=True, addr=0, data=-123)
    assert first.push and not first.pop and not first.blocked and not first.pp_valid
    held = transfer(
        buffer, sink, valid=True, addr=1, data=456, force_ready=False
    )
    assert not held.ready and not held.pop and held.pp_addr == 0 and held.pp_data == -123
    reset = buffer.step(rstn=False, valid=True, addr=1, data=456)
    sink.reset()
    assert not reset.ready and not reset.pp_valid and not reset.blocked
    assert not buffer.pending and not sink.loaded

    cycles, simultaneous = load_table(buffer, sink, rng)
    assert cycles > 1025 and simultaneous > 700

    illegal = transfer(buffer, sink, valid=True, addr=7, data=7)
    assert not illegal.ready and not illegal.push and not illegal.blocked
    held_during_compute = transfer(
        buffer, sink, admission=False, valid=True, addr=0, data=11
    )
    assert not held_during_compute.ready and not held_during_compute.blocked

    restart = transfer(buffer, sink, valid=True, addr=0, data=11)
    assert restart.push and not restart.blocked and sink.loaded
    restart_pop = transfer(buffer, sink, valid=True, addr=1, data=12)
    assert not restart_pop.push and restart_pop.pop and not sink.loaded
    restart_one = transfer(buffer, sink, valid=True, addr=1, data=12)
    assert restart_one.push and not restart_one.pop

    while buffer.addr < 1023:
        next_addr = buffer.addr + 1
        cycle = transfer(buffer, sink, valid=True, addr=next_addr, data=next_addr)
        assert cycle.push and cycle.pop
    rejected_after_last = transfer(buffer, sink, valid=True, addr=1, data=99)
    assert rejected_after_last.pop and not rejected_after_last.push
    assert sink.loaded and not buffer.pending
    rejected_loaded = transfer(buffer, sink, valid=True, addr=1, data=99)
    assert not rejected_loaded.ready and not rejected_loaded.blocked
    accepted_restart = transfer(buffer, sink, valid=True, addr=0, data=99)
    assert accepted_restart.push

    buffer.step(rstn=False)
    sink.reset()
    reload_cycles, reload_simultaneous = load_table(buffer, sink, rng)
    result = {
        "status": "PASS",
        "seed": seed,
        "first_load_cycles": cycles,
        "first_same_cycle_push_pop": simultaneous,
        "reload_cycles": reload_cycles,
        "reload_same_cycle_push_pop": reload_simultaneous,
        "writes_per_complete_table": len(sink.writes),
    }
    print("TABLE_COMMAND_REFERENCE_PASS " + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    self_check()
