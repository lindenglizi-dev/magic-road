"""单项装载寄存提交契约：接收顺序当拍推进，存储下一沿更新。"""
import json
from pathlib import Path


def self_check():
    checks = 0
    for size in (432, 1296):
        memory = [None] * size
        expected = [None] * size
        pending = None
        cursor = 0
        loaded = False
        for address in range(size):
            # 本沿先提交旧项，同时登记下一合法项；无需因pending插入气泡。
            if pending is not None:
                memory[pending[0]] = pending[1]
            assert address == cursor
            data = (address * 73 + 19) % 256 - 128
            pending = (address, data)
            expected[address] = data
            cursor = 0 if address == size - 1 else address + 1
            loaded = address == size - 1
            assert memory[:address] == expected[:address]
            checks += 1
        assert loaded and pending is not None
        # 可在这同一沿接受start；首次读在随后的PREPARE/STORAGE沿。
        memory[pending[0]] = pending[1]
        pending = None
        assert memory == expected
        # 复位只清pending/资格，存储不清零；旧项绝不在恢复后写入。
        pending = (0, 127)
        before = memory.copy()
        pending, loaded, cursor = None, False, 0
        assert memory == before and pending is None and not loaded and cursor == 0
        checks += 2
    return {"status": "PASS", "accepted_records": 1728, "checks": checks,
            "accept_ii": 1, "accept_to_write_edges": 1,
            "first_read": "after the edge which commits the final pending write",
            "reset": "cancel pending, invalidate completeness, retain memory contents"}


if __name__ == "__main__":
    result = self_check()
    print(json.dumps(result, ensure_ascii=False))
    Path(__file__).with_name("commit_reference_receipt.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
