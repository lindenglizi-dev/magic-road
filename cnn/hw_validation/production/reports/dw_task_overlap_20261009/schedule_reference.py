"""冻结 down2 DW 的身份/credit参考；不冒充数值模型或性能预测。"""
from collections import deque
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
TASKS = [(row * 4 + x, ch) for row in range(4) for x in (0, 3) for ch in range(16)]


def check(seed, reset=False, fault_task=None):
    rng = random.Random(seed)
    meta, pipe, results = deque(), deque(), deque()
    active = None
    task = group = 0
    preparing = True
    reduction_open = False
    emitted = []
    epoch = 0
    counts = {"full": 0, "push_pop": 0, "active_replace": 0}
    for cycle in range(20000):
        if reset and cycle == 500:
            meta.clear(); pipe.clear(); results.clear()
            active = None
            task = group = 0
            preparing = True
            reduction_open = False
            emitted.clear()
            epoch += 1
            assert not meta and not pipe and not results and active is None
        while pipe and pipe[0][0] <= cycle:
            _, identity = pipe.popleft()
            results.append(identity)
        fault = bool(results) and results[0][1] == fault_task
        if fault:
            assert meta[0] == results[0]
            assert all(index != fault_task for _, index, _ in emitted)
            return {"fault": True, "cycles_not_performance": cycle, **counts}
        pp_accept = active is not None and cycle % 700 >= 300 and rng.randrange(4) != 0
        active_last = pp_accept and active[2] + 1 == (3 if TASKS[active[1]][0] % 4 == 0 else 1)
        pop = bool(results) and (active is None or active_last)
        first = task < 128 and not preparing and group == 0
        accept = task < 128 and not preparing and (group != 0 or len(meta) < 4 or pop)
        counts["full"] += len(meta) == 4
        counts["push_pop"] += bool(first and accept and pop)
        counts["active_replace"] += bool(active_last and pop)
        if pp_accept:
            assert active[0] == epoch
            emitted.append(tuple(active))
            active = None if active_last else [active[0], active[1], active[2] + 1]
        if pop:
            identity = results.popleft()
            assert meta.popleft() == identity
            active = [identity[0], identity[1], 0]
        if accept:
            identity = (epoch, task)
            if first:
                assert not reduction_open
                meta.append(identity)
                reduction_open = True
            if group == 2:
                assert reduction_open
                pipe.append((cycle + 7, identity))
                reduction_open = False
                task += 1
                group = 0
            else:
                group += 1
            preparing = True
        elif preparing and task < 128:
            preparing = False
        assert 0 <= len(meta) <= 4
        assert len(meta) == len(pipe) + len(results) + int(reduction_open)
        if task == 128 and not meta and active is None:
            expected = [(epoch, index, lane) for index, (position, _) in enumerate(TASKS)
                        for lane in range(3 if position % 4 == 0 else 1)]
            assert emitted == expected and len(emitted) == 256
            assert not pipe and not results and not reduction_open
            return {"fault": False, "scalar_identities": 256, **counts}
    raise AssertionError("Control reference failed to drain")


if __name__ == "__main__":
    runs = [check(seed, reset=bool(seed % 2)) for seed in range(8)]
    runs += [check(seed, fault_task=37) for seed in range(4)]
    assert all(runs[i]["full"] and runs[i]["push_pop"] and runs[i]["active_replace"] for i in range(8))
    result = {"scope": "Ownership only; existing frozen vectors remain numeric golden", "tasks": 128,
              "mac_credit_limit": 4, "existing_active_triplet_slots": 1, "runs": runs}
    (ROOT / "schedule_reference.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("SCHEDULE_REFERENCE_PASS runs=12 full/push_pop/active_replace covered; no FPS claim")
