"""固定 CSP2/3/4 选择控制参考；不模拟计算延迟或真实 DDR 完成。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BLOCKS = {2: (72, 128, 12, 5), 3: (36, 64, 24, 7), 4: (18, 32, 48, 7)}


class Selector:
    """同一时钟域，reset 优先；fault 占有持续到共同复位。"""

    def __init__(self) -> None:
        self.state, self.block_id, self.stage = "IDLE", 0, 0
        self.line_valid = False

    def outputs(self) -> dict:
        return {"state": self.state, "block_id": self.block_id, "stage": self.stage,
                "busy": self.state != "IDLE", "start_ready": self.state == "IDLE",
                "done": self.state == "DONE", "fault": self.state == "FAULT",
                "traffic_permitted": self.state == "ACTIVE", "line_valid": self.line_valid}

    def tick(self, *, reset: bool = False, start: bool = False, block_id: int = 0,
             parameter_response_block_id: int | None = None,
             barrier_block_id: int | None = None) -> dict:
        """参数/屏障事件表示各通道的实际消费；返回沿之后可见输出。"""
        if reset:
            self.__init__()
        elif self.state == "IDLE":
            if start:
                self.block_id, self.stage, self.line_valid = block_id & 15, 0, False
                self.state = "ACTIVE" if self.block_id in BLOCKS else "FAULT"
        elif self.state == "ACTIVE":
            wrong_parameter = (parameter_response_block_id is not None
                               and parameter_response_block_id != self.block_id)
            wrong_barrier = barrier_block_id is not None and barrier_block_id != self.block_id
            if wrong_parameter or wrong_barrier:
                self.state = "FAULT"
            elif barrier_block_id is not None:
                if self.stage == BLOCKS[self.block_id][3] - 1:
                    self.state = "DONE"
                else:
                    self.stage += 1
        elif self.state == "DONE":
            self.state = "IDLE"
        return self.outputs()


def verify_trace(trace: list[dict], block: int) -> None:
    """检查锁存身份、末层 done/busy 和下一拍 idle 的可见合同。"""
    assert all(row["block_id"] == block for row in trace), "busy changed owner"
    assert all(row["busy"] and not row["start_ready"] for row in trace[:-1]), "early release"
    assert trace[-2]["done"] and trace[-2]["busy"], "done must retain busy"
    assert trace[-1]["start_ready"] and not trace[-1]["done"], "idle must follow done"


def self_check() -> dict:
    model, traces = Selector(), []
    for repeat in range(2):
        if repeat:
            assert model.tick(reset=True)["block_id"] == 0
        for block in BLOCKS:
            trace = [model.tick(start=True, block_id=block)]
            for disturbance in (0, 15, 2, 3, 4):
                trace.append(model.tick(start=True, block_id=disturbance,
                                        parameter_response_block_id=block))
            for _ in range(BLOCKS[block][3]):
                trace.append(model.tick(start=True, block_id=15, barrier_block_id=block))
            trace.append(model.tick(start=True, block_id=2))
            verify_trace(trace, block)
            traces.append({"repeat": repeat, "block_id": block, "trace": trace})
    faults = []
    for event in ({"start": True, "block_id": 15},
                  {"parameter_response_block_id": 3}, {"barrier_block_id": 4}):
        model.tick(reset=True)
        if "start" not in event:
            model.tick(start=True, block_id=2)
        out = model.tick(**event)
        assert out["fault"] and out["busy"] and not out["traffic_permitted"]
        for _ in range(3):
            assert model.tick(start=True, block_id=3)["fault"]
        faults.append({"event": event, "output": out, "sticky_cycles_checked": 3})
        assert model.tick(reset=True)["start_ready"]
    negatives = []
    for name, field, value in (("live_id_switch", "block_id", 15),
                               ("done_releases_busy", "busy", False),
                               ("done_allows_start", "start_ready", True)):
        mutated = [dict(row) for row in traces[0]["trace"]]
        index = 2 if field == "block_id" else -2
        mutated[index][field] = value
        try:
            verify_trace(mutated, 2)
        except AssertionError as error:
            negatives.append({"mutation": name, "rejected": True, "reason": str(error)})
        else:
            raise AssertionError(f"negative escaped: {name}")
    return {"status": "PASS", "scope": "CPU_CONTROL_ONLY_NOT_RTL_NOT_DDR_VISIBILITY",
            "positive_sequences": traces, "fault_cases": faults, "real_negative_checks": negatives,
            "cuda_imported": False, "training": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main() -> None:
    contract = {"schema": 1, "module": "road_feature_blocks_client", "clock_domain": "100MHz",
                "legal_blocks": {str(k): dict(zip(("height", "width", "half_channels", "stages"), v))
                                 for k, v in BLOCKS.items()},
                "start": "Only i_start && o_start_ready in IDLE latches i_block_id[3:0]; clear line valid.",
                "busy": "Ignore i_start and i_block_id until after DONE. One owner and one fixed graph case.",
                "parameter_response": "On consumed response compare i_parameter_response_block_id to latched o_block_id.",
                "barrier": "On consumed barrier compare i_barrier_block_id to latched o_block_id; advance stage only after old core retires.",
                "done": "Final matching barrier enters DONE for one cycle: busy=1, done=1, start_ready=0; next cycle IDLE.",
                "fault": "Accepted illegal ID or wrong response/barrier identity: sticky fault, busy=1, no further traffic until common reset.",
                "priority": "common reset > fault identity check > matching barrier > held state; DONE ignores start.",
                "reset": "Common reset clears control, identity and line valid; service cancels old responses and reloads SiLU; arrays not reset.",
                "storage": {"work_bytes": 3072, "weight_banks": 24, "weight_bits": 192,
                            "quantization_bytes": 31, "read_line_bytes": 16, "total_data_bytes": 3695,
                            "owners": 1, "byte_cache_accesses_per_cycle_max": 1, "eram_mapping": "UNPROVEN"},
                "widths": {"block": 4, "parameter_channel": 7, "parameter_group": 5,
                           "layer": 3, "window": 3, "byte_address": 32, "read_data": 128},
                "io": "Single in-flight aligned16 read, exact response address match; existing visibility barrier only.",
                "limits": ["No arbitrary shape/layer list", "CSP2 Cin12 last mask 0x0f",
                           "CSP4 tail y16/17 only; no y18/19 writes", "No independent reset/late-return guarantee"],
                "verification_boundary": "Selector checks control events, not arithmetic/stage duration/cache data/RTL; use frozen CSP vectors for numerical validation."}
    report = self_check()
    for name, content in (("control_contract.json", contract), ("selector_report.json", report)):
        (ROOT / name).write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS: 6 block traces, 3 sticky faults, 3 real rejected trace mutations")


if __name__ == "__main__":
    main()
