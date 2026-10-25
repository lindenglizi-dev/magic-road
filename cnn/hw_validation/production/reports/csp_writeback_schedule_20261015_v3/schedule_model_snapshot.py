"""首 CSP 写回候选的周期契约；仅 Python 模型，不改 RTL 或启动外部工具。"""
import hashlib
from itertools import permutations
import json
from pathlib import Path
import random
import re


BASE = Path(__file__).resolve().parent
PRIOR = BASE / "reports/qat_g10_csp_first_closure_20261015_v2"
OUT = BASE / "reports/csp_writeback_schedule_20261015_v3"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Writeback:
    """单任务、五级非停顿数据流；每路最多一个结果，末次写握手释放。"""

    def __init__(self):
        self.loaded = False
        self.fault = False
        self.owned = False
        self.pipe = [None] * 4  # M/S/A/C；第五级 W 为固定三路写回槽。
        self.bank = [None] * 3
        self.remaining = self.seen = 0

    def load_complete(self):
        # 完整装表事件抽象，不模拟 1024 项表协议；仍由已保留 RTL 回归证明。
        if self.owned or self.fault:
            raise ValueError("cannot publish table while owned/faulted")
        self.loaded = True

    def begin(self, mask, tags, addresses, bypass, residual):
        if not self.loaded or self.owned or self.fault:
            raise ValueError("task admission blocked")
        if not 0 <= mask <= 7 or any(len(x) != 3 for x in (tags, addresses, bypass)):
            raise ValueError("invalid task shape")
        if (any(not 0 <= x <= 65535 for x in tags)
                or any(not 0 <= x < 2**32 for x in addresses)
                or any(not -128 <= x <= 127 for x in bypass)):
            raise ValueError("invalid task width")
        active = [tags[lane] for lane in range(3) if mask & (1 << lane)]
        self.mask = self.remaining = mask
        self.seen = 0
        self.tags, self.addresses, self.bypass = map(tuple, (tags, addresses, bypass))
        self.residual = bool(residual)
        self.owned = True
        # 首组已被接受后的语义故障，不退回为“未接受”的调用错误。
        self.fault = mask == 0 or len(set(active)) != len(active)
        assert not any(self.pipe) and not any(self.bank)

    def pp_ready(self):
        return self.loaded and self.owned and not self.fault and self.seen != self.mask

    def output(self):
        if not self.owned or self.fault:
            return None
        lane = (self.remaining & -self.remaining).bit_length() - 1
        return self.bank[lane]

    def step(self, item=None, ready=True, reset=False, external_fault=False):
        """在边沿前观察握手，随后同时更新寄存器；item=(tag,int8,rawmode)。"""
        if reset:
            self.__init__()
            return False, None
        if external_fault or self.fault:
            self.fault = True
            self.pipe = [None] * 4
            self.bank = [None] * 3
            return False, None
        old_owned = self.owned
        old_ready = self.pp_ready()
        emitted = self.output() if ready else None
        if emitted is not None:
            lane = emitted[0]
            self.bank[lane] = None
            self.remaining &= ~(1 << lane)
            if not self.remaining:
                assert not any(self.pipe) and not any(self.bank)
                self.owned = False

        accepted = item is not None and old_ready
        match = None
        if item is not None and old_owned and not old_ready:
            # 全部期望项已真实接收；额外 valid 不是待接收的合法项。
            # 不计握手、不推进 seen；同步故障封锁下一任务，须共同复位。
            self.fault = True
            self.pipe = [None] * 4
            self.bank = [None] * 3
            return False, emitted
        if accepted:
            tag, value, rawmode = item
            lanes = [lane for lane in range(3)
                     if self.mask & (1 << lane) and self.tags[lane] == tag]
            if (len(lanes) != 1 or rawmode or not -128 <= value <= 127
                    or self.seen & (1 << lanes[0])):
                # 同步发现坏 token 不能追回该边沿前已合法完成的写握手。
                self.fault = True
                self.pipe = [None] * 4
                self.bank = [None] * 3
                return accepted, emitted
            lane = lanes[0]
            self.seen |= 1 << lane
            match = (lane, value)

        m, s, a, c = self.pipe
        if c is not None:
            lane, total, tag, address, high, low = c
            assert self.bank[lane] is None
            self.bank[lane] = (lane, 127 if high else -128 if low else total,
                               total, tag, address)
        next_c = None if a is None else (*a, a[1] > 127, a[1] < -128)
        next_a = None if s is None else (s[0], s[1] + s[2], s[3], s[4])
        next_s = None if m is None else (
            m[0], m[1], self.bypass[m[0]] if self.residual else 0,
            self.tags[m[0]], self.addresses[m[0]])
        self.pipe = [match, next_s, next_a, next_c]
        held = [token[0] for token in self.pipe + self.bank if token is not None]
        assert len(held) == len(set(held)) <= self.mask.bit_count() if old_owned else not held
        if old_owned:
            assert sum(1 << lane for lane in held) == self.seen & self.remaining
        return accepted, emitted


def run_task(mask, tags, addresses, bypass, residual, values, ready_fn, bubble_fn):
    model = Writeback()
    model.load_complete()
    model.begin(mask, tags, addresses, bypass, residual)
    active = [lane for lane in range(3) if mask & (1 << lane)]
    sent, received, accepts, writes = 0, [], [], []
    held = None
    for cycle in range(1000):
        before = model.output()
        if held is not None:
            assert before == held, "payload changed under backpressure"
        ready = ready_fn(cycle)
        item = None
        if sent < len(active) and not bubble_fn(cycle):
            lane = active[sent]
            item = (tags[lane], values[lane], False)
        accepted, emitted = model.step(item, ready)
        if accepted:
            accepts.append(cycle)
            sent += 1
        if emitted is not None:
            received.append(emitted)
            writes.append(cycle)
        held = before if before is not None and not ready else None
        if not model.owned:
            assert sent == len(active) == len(received)
            expected = [(lane, max(-128, min(127, values[lane] + (bypass[lane] if residual else 0))),
                         values[lane] + (bypass[lane] if residual else 0), tags[lane], addresses[lane])
                        for lane in active]
            assert received == expected
            return dict(accepts=accepts, writes=writes, outputs=len(received), cycles=cycle + 1)
    raise AssertionError("bounded source/sink did not retire task")


def vectors():
    root = PRIOR / "vectors"
    data = {p.stem: [int(x, 16) for x in p.read_text().split()]
            for p in root.glob("*.hex")}
    signed = lambda x, bits: x - (1 << bits) if x & (1 << (bits - 1)) else x
    tasks = []
    for prefix, count in (("", 160), ("sat_", 6)):
        for index in range(count):
            get = lambda name: data[prefix + "task_" + name][index]
            tags = [(get("tags") >> (16 * lane)) & 65535 for lane in range(3)]
            addresses = [(get("addresses") >> (32 * lane)) & 0xffffffff for lane in range(3)]
            bypass, values = [], []
            for lane, tag in enumerate(tags):
                if prefix:
                    bypass.append(signed((get("bypass") >> (8 * lane)) & 255, 8))
                else:
                    source = (get("bypass_indices") >> (16 * lane)) & 65535
                    bypass.append(0 if source == 65535 else signed(data["bypass"][source], 8))
                if not get("mask") & (1 << lane):
                    values.append(0)
                    continue
                value = (data["sat_post"][tag - 384] if prefix else
                         data["dw_post"][tag] if tag < 192 else data["pw_post"][tag - 192])
                values.append(signed(value & 255, 8))
                total = values[-1] + (bypass[-1] if get("residual") else 0)
                golden_sum = (signed(data["sat_sum"][tag - 384], 16) if prefix else
                              values[-1] if tag < 192 else signed(data["residual_sum"][tag - 192], 16))
                golden = (data["sat_output"][tag - 384] if prefix else
                          data["dw_post"][tag] if tag < 192 else data["residual_post"][tag - 192])
                assert total == golden_sum
                assert max(-128, min(127, total)) == signed(golden & 255, 8)
            tasks.append((get("mask"), tags, addresses, bypass, bool(get("residual")), values))
    return tasks


def selftest():
    continuous = run_task(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), False,
                          (4, 5, 6), lambda c: True, lambda c: False)
    assert continuous["accepts"] == [0, 1, 2] and continuous["writes"] == [5, 6, 7]
    review_contract(Writeback)
    for value in range(-128, 128):
        for bypass in range(-128, 128):
            trace = run_task(1, (11, 22, 33), (100, 101, 102), (bypass, 0, 0), True,
                             (value, 0, 0), lambda c: True, lambda c: False)
            assert trace["writes"] == [5]
    traces = []
    for task in vectors():
        traces.append(run_task(*task, lambda c: True, lambda c: False))
        rng = random.Random(42)
        run_task(*task, lambda c: c >= 37 and rng.randrange(4) != 0,
                 lambda c: rng.randrange(5) == 0)
    mask_trials = 0
    for mask in range(1, 8):
        for pattern in range(64):
            run_task(mask, (3, 7, 9), (10, 20, 30), (-128, 127, 1), True,
                     (127, 127, -128), lambda c: c >= 6 or bool(pattern & (1 << c)),
                     lambda c: c % 3 == 1)
            mask_trials += 1
    cancellation = 0
    for reset in (False, True):
        for age in range(1, 6):
            model = Writeback()
            model.load_complete()
            model.begin(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), True)
            model.step((1, 2, False), ready=False)
            for _ in range(age - 1):
                model.step(ready=False)
            assert model.step(ready=True, reset=reset, external_fault=not reset) == (False, None)
            assert model.output() is None
            assert not any(model.pipe) and not any(model.bank)
            if reset:
                assert not model.loaded and not model.owned and not model.fault
                model.load_complete()
                model.begin(1, (1, 2, 3), (10, 20, 30), (0, 0, 0), False)
                model.step((1, 99, False))
                emitted = [model.step()[1] for _ in range(5)]
                assert emitted[-1][1] == 99 and all(x is None for x in emitted[:-1])
            else:
                assert model.fault and model.owned
                try:
                    model.load_complete()
                except ValueError:
                    pass
                else:
                    raise AssertionError("fault silently resumed")
            cancellation += 1
    for bad in ((99, 1, False), (1, 1, True), (1, 128, False), (1, 1, False)):
        model = Writeback()
        model.load_complete()
        model.begin(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), True)
        if bad == (1, 1, False):
            model.step(bad)
        assert model.step(bad)[1] is None and model.fault
        assert model.step((2, 1, False))[0] is False
    model = Writeback()
    model.load_complete()
    model.begin(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), True)
    model.step((1, 5, False))
    for _ in range(4):
        model.step(ready=False)
    accepted, emitted = model.step((99, 0, False))
    assert accepted and emitted[1] == 5 and model.fault
    permutation_trials = 0
    for mask in range(1, 8):
        active = [lane for lane in range(3) if mask & (1 << lane)]
        for order in permutations(active):
            model = Writeback()
            model.load_complete()
            model.begin(mask, (1, 2, 3), (10, 20, 30), (0, 0, 0), False)
            for lane in order:
                assert model.step((lane + 1, lane + 10, False), ready=False)[0]
            emitted = []
            for cycle in range(20):
                item = model.step(ready=cycle >= 6)[1]
                if item is not None:
                    emitted.append(item)
            assert [x[0] for x in emitted] == active and not model.owned
            permutation_trials += 1
    model = Writeback()
    for attempt in ("before_load", "while_owned", "after_fault"):
        if attempt == "while_owned":
            model.load_complete()
            model.begin(1, (1, 2, 3), (10, 20, 30), (0, 0, 0), False)
        if attempt == "after_fault":
            model.step(external_fault=True)
        try:
            model.begin(1, (1, 2, 3), (10, 20, 30), (0, 0, 0), False)
        except ValueError:
            pass
        else:
            raise AssertionError("task admitted without permission")
    model = Writeback()
    model.load_complete()
    for value in (7, -9):
        model.begin(1, (1, 2, 3), (10 + value, 20, 30), (0, 0, 0), False)
        assert model.step((1, value, False)) == (True, None)
        observed = [model.step()[1] for _ in range(5)]
        assert observed[-1] == (0, value, value, 1, 10 + value)
        assert all(x is None for x in observed[:-1]) and not model.owned
    normal_tasks = vectors()[:160]
    model = Writeback()
    model.load_complete()
    serial_cycles = 0
    for mask, tags, addresses, bypass, residual, values in normal_tasks:
        model.begin(mask, tags, addresses, bypass, residual)
        active = [lane for lane in range(3) if mask & (1 << lane)]
        received = []
        for cycle in range(20):
            item = (tags[active[cycle]], values[active[cycle]], False) if cycle < len(active) else None
            accepted, emitted = model.step(item)
            assert accepted == (item is not None)
            serial_cycles += 1
            if emitted is not None:
                received.append(emitted)
            if not model.owned:
                assert [x[0] for x in received] == active
                break
        else:
            raise AssertionError("serial task not released")
    # 基线为单寄存写槽的理想边界计数，不含冻结核的计算事件。
    ideal_single_slot_cycles = sum(mask.bit_count() + 1 for mask, *_ in normal_tasks)
    assert serial_cycles - ideal_single_slot_cycles == 160 * 4
    return dict(int8_pairs=65536, frozen_tasks=166, frozen_outputs=sum(x["outputs"] for x in traces),
                frozen_tasks_with_stalls=166, mask_ready_patterns=mask_trials,
                cancellation_positions=cancellation, invalid_token_cases=4,
                synchronous_error_with_prior_commit=1, first_write_latency=5,
                arrival_permutations=permutation_trials, blocked_task_admissions=3,
                reused_same_tag_tasks=2, continuous_three_lane_writes=continuous["writes"],
                review_contract_cases=4, serial_tasks=160, serial_candidate_boundary_cycles=serial_cycles,
                ideal_single_slot_boundary_cycles=ideal_single_slot_cycles,
                conditional_serial_added_cycles=serial_cycles - ideal_single_slot_cycles,
                task_traces=traces)


def review_contract(factory):
    """复核发现的反例：额外结果零握手，首组语义错误仍取得所有权。"""
    model = factory()
    model.load_complete()
    model.begin(1, (1, 2, 3), (10, 20, 30), (0, 0, 0), False)
    assert model.step((1, 4, False), ready=False)[0]
    accepted, emitted = model.step((1, 4, False), ready=False)
    assert not accepted and emitted is None and model.fault and model.owned
    assert not any(model.pipe) and not any(model.bank)
    for _ in range(3):
        assert model.step((1, 4, False), ready=False) == (False, None)
    for mask, tags in ((0, (1, 2, 3)), (3, (1, 1, 3))):
        model = factory()
        model.load_complete()
        model.begin(mask, tags, (10, 20, 30), (0, 0, 0), False)
        assert model.fault and model.owned and model.output() is None
        assert model.step((1, 5, False)) == (False, None)
        model.step(reset=True)
        assert not model.fault and not model.owned and not model.loaded
    model = factory()
    model.load_complete()
    model.begin(1, (1, 2, 3), (10, 20, 30), (0, 0, 0), False)
    model.step((1, 4, False))
    for _ in range(4):
        model.step(ready=False)
    accepted, emitted = model.step((1, 4, False))
    assert not accepted and emitted[1] == 4 and model.fault


def main():
    if OUT.exists():
        raise FileExistsError("keep prior result; select a new explicit report directory")
    seal = json.loads((PRIOR / "execution_checks.json").read_text(encoding="utf-8"))
    for name, expected in seal["report_sha256"].items():
        if digest(PRIOR / name) != expected:
            raise ValueError(f"retained input changed: {name}")
    live = BASE / "csp_first_closure/rtl/road_csp_first_probe.v"
    assert digest(live) == digest(PRIOR / "rtl/road_csp_first_probe.v")
    gate = json.loads((PRIOR / "wrapper_afterfix_gate.json").read_text(encoding="utf-8"))
    inventory = []
    for finding in gate["findings"]:
        if finding["code"] not in ("VG146", "VG147"):
            continue
        detail = finding["evidence"]["detail"]
        target = re.search(r"target=([^;]+)", detail)
        count = re.search(r"operation_count=(\d+)", detail)
        inventory.append(dict(rule=finding["code"], line=finding["line"],
                              target=target[1] if target else None, evidence=detail,
                              known_operations=int(count[1]) if count else None))
    results = selftest()
    OUT.mkdir()
    report = dict(status="PASS_PYTHON_SCHEDULE_ONLY_RTL_NOT_CHANGED", checks=results,
                  input_seal_sha256=digest(PRIOR / "execution_checks.json"),
                  retained_files_rechecked=len(seal["report_sha256"]),
                  model_source_sha256=digest(Path(__file__)), wrapper_sha256=digest(live),
                  prior_public_gates=gate["checks"], prior_gate_errors=gate["errors"],
                  cone_inventory=inventory, new_rtl=False, simulation_rerun=False,
                  physical_timing_or_resources=False, full_network=False,
                  limits=["PP-to-write boundary only; no MAC/quantizer cycle model",
                          "no actual table loading/DMA/DDR; reset/reload is an event abstraction",
                          "latency is candidate Python evidence, not implemented RTL measurement",
                          "metadata immutable during ownership; no overlapping tasks",
                          "no gate waiver, synthesis, bitstream, board work or training"])
    (OUT / "schedule_model_snapshot.py").write_bytes(Path(__file__).read_bytes())
    with (OUT / "schedule_checks.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("SCHEDULE_PASS pairs=65536 tasks=166 masks=448 cancel=10 latency=5 RTL_NOT_CHANGED")


if __name__ == "__main__":
    main()
