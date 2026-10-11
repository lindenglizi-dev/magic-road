"""road_mac_probe 的最小整数与周期参考。"""

from dataclasses import dataclass
from typing import List, Sequence, Tuple


Vec3 = Tuple[int, int, int]


def signed(value: int, width: int) -> int:
    """把整数按给定位宽解释为二补码。"""
    value &= (1 << width) - 1
    return value - (1 << width) if value & (1 << (width - 1)) else value


@dataclass(frozen=True)
class Group:
    activations: Sequence[int]
    weights: Sequence[Sequence[int]]
    lane_mask: int
    bias: Vec3
    first: bool
    last: bool


@dataclass
class PendingAccumulation:
    due_cycle: int
    dot: Vec3
    bias: Vec3
    first: bool
    last: bool
    result_cycle: int


class MacProbeReference:
    """用上升沿后的可见状态描述单上下文 MAC。"""

    def __init__(self) -> None:
        self.cycle = 0
        self.accumulator: Vec3 = (0, 0, 0)
        self.input_ready = True
        self.result_valid = False
        self.result_data: Vec3 = (0, 0, 0)
        self.fault = False
        self._pending: List[PendingAccumulation] = []
        self._pending_result = None

    @staticmethod
    def dot(group: Group) -> Vec3:
        assert len(group.activations) == 8
        assert len(group.weights) == 3 and all(len(row) == 8 for row in group.weights)
        activations = [signed(value, 8) for value in group.activations]
        return tuple(
            sum(
                activations[lane] * signed(group.weights[channel][lane], 8)
                for lane in range(8)
                if group.lane_mask & (1 << lane)
            )
            for channel in range(3)
        )

    def step(self, group: Group = None, input_valid: bool = False,
             result_ready: bool = False, rstn: bool = True):
        """推进一个上升沿并返回沿后的 ready/valid/data/fault。"""
        if not rstn:
            self.__init__()
            return self.observe()

        accepted = bool(input_valid and self.input_ready)
        output_accepted = bool(self.result_valid and result_ready)
        if output_accepted:
            self.result_valid = False
            self.input_ready = True

        if accepted:
            assert group is not None
            self._pending.append(
                PendingAccumulation(
                    due_cycle=self.cycle + 5,
                    dot=self.dot(group),
                    bias=tuple(signed(value, 32) for value in group.bias),
                    first=group.first,
                    last=group.last,
                    result_cycle=self.cycle + 6,
                )
            )
            if group.last:
                self.input_ready = False

        due = [item for item in self._pending if item.due_cycle == self.cycle]
        assert len(due) <= 1
        if due:
            item = due[0]
            base = item.bias if item.first else self.accumulator
            candidate = tuple(base[index] + item.dot[index] for index in range(3))
            final_fault = item.last and any(
                value < -(1 << 31) or value > (1 << 31) - 1 for value in candidate
            )
            if not final_fault:
                self.accumulator = tuple(signed(value, 33) for value in candidate)
            if item.last:
                self._pending_result = (
                    item.result_cycle,
                    (0, 0, 0) if final_fault else tuple(signed(value, 32) for value in candidate),
                    final_fault,
                )
            self._pending.remove(item)

        if self._pending_result and self._pending_result[0] == self.cycle:
            _, self.result_data, self.fault = self._pending_result
            self.result_valid = True
            self._pending_result = None

        observed = self.observe()
        self.cycle += 1
        return observed

    def observe(self):
        return self.input_ready, self.result_valid, self.result_data, self.fault


def _group(value: int, first: bool, last: bool, bias: Vec3 = (0, 0, 0)) -> Group:
    weights = ([1] * 8, [2] * 8, [-1] * 8)
    return Group([value] * 8, weights, 0xFF, bias, first, last)


def self_check() -> None:
    model = MacProbeReference()
    accepted = []
    for index in range(24):
        ready, _, _, _ = model.step(_group(index + 1, index == 0, index == 23, (3, -4, 5)), True)
        assert ready is (index != 23)
        accepted.append(index)
    assert len(accepted) == 24
    for _ in range(5):
        ready, valid, _, _ = model.step()
        assert not ready and not valid
    ready, valid, data, fault = model.step()
    assert not ready and valid and not fault
    total = 8 * sum(range(1, 25))
    assert data == (3 + total, -4 + 2 * total, 5 - total)
    held = model.step(result_ready=False)
    assert held[1:] == (True, data, False)
    ready, valid, _, _ = model.step(result_ready=True)
    assert ready and not valid

    overflow = MacProbeReference()
    overflow.step(_group(1, True, True, ((1 << 31) - 4, 0, 0)), True)
    for _ in range(6):
        state = overflow.step()
    assert state[1:] == (True, (0, 0, 0), True)
    assert overflow.step(rstn=False) == (True, False, (0, 0, 0), False)


if __name__ == "__main__":
    self_check()
    print("road_mac_probe_reference: PASS")
