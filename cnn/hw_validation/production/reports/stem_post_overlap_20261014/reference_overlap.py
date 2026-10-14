"""Stem任务与按序提交的最小语义参考；不模拟算术或宣称RTL周期。"""
from collections import deque
import json
from pathlib import Path
import random


TASKS = tuple((position, channel, min(3, 16 - channel))
              for position in range(16) for channel in range(0, 16, 3))


def self_check():
    tags = [position * 16 + channel + lane for position, channel, count in TASKS for lane in range(count)]
    assert len(TASKS) == 96 and tags == list(range(256))
    runs = []
    for seed in range(16):
        rng = random.Random(seed)
        pending = deque()
        accepted = committed = 0
        overlap = False
        for tick in range(10000):
            if pending and rng.randrange(4) != 0:
                tag, parameter = pending.popleft()
                assert tag == committed and parameter == (tag % 16 + 1)
                committed += 1
            if accepted < len(TASKS):
                position, channel, count = TASKS[accepted]
                # 以8项标量积压作有界语义夹具；不是实际PP的8个batch槽容量。
                if len(pending) + count <= 8 and rng.randrange(4) != 0:
                    snapshot = [(position * 16 + channel + lane, channel + lane + 1) for lane in range(count)]
                    pending.extend(snapshot)
                    accepted += 1
                    overlap |= committed < position * 16 + channel
            assert 0 <= committed <= 256 and 0 <= len(pending) <= 8
            if committed == 256:
                assert accepted == 96 and not pending
                break
        else:
            raise AssertionError("No progress")
        assert overlap
        # 任意位置取消后没有待提交身份；完整性重建后才能发布。
        pending.extend(((0, 1), (1, 2)))
        pending.clear()
        accepted = committed = 0
        assert not pending and accepted == committed == 0
        runs.append({"seed": seed, "abstract_ticks": tick + 1, "overlap": overlap})
    return {"status": "PASS", "tasks": len(TASKS), "ordered_tags": len(tags), "runs": runs,
            "scope": "Task identity/parameter ownership only; abstract ticks are not RTL cycle predictions"}


if __name__ == "__main__":
    result = self_check()
    Path(__file__).with_name("overlap_reference_receipt.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
