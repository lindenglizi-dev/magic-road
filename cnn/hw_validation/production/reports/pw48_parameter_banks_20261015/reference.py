"""仅证明48通道逻辑地址与三浅bank映射，算术黄金值复用冻结版本。"""
import json
from pathlib import Path
import random


def check():
    rng = random.Random(42)
    count = 0
    for trial in range(256):
        flat = [[None] * 48 for _ in range(2)]
        banks = [[[None] * 16 for _ in range(3)] for _ in range(2)]
        address, lane, row = [0, 0], [0, 0], [0, 0]
        for step in range(512):
            kind = rng.randrange(2)
            logical = 0 if rng.randrange(19) == 0 else address[kind]
            value = rng.randrange(-(1 << 31), 1 << 31)
            selected_lane = 0 if logical == 0 else lane[kind]
            selected_row = 0 if logical == 0 else row[kind]
            assert (selected_lane, selected_row) == (logical % 3, logical // 3)
            flat[kind][logical] = value
            banks[kind][selected_lane][selected_row] = value
            if logical == 0:
                lane[kind], row[kind] = 1, 0
            elif lane[kind] == 2:
                lane[kind], row[kind] = 0, (row[kind] + 1) & 15
            else:
                lane[kind] += 1
            address[kind] = (logical + 1) % 48
            assert flat[kind] == [banks[kind][i % 3][i // 3] for i in range(48)]
            count += 1
    receipt = {"status": "PASS", "accepted_records": count, "seed": 42,
               "mapping": "bank=channel%3,row=channel//3; read row=output_group",
               "scope": "storage mapping only; no new arithmetic/accuracy claim"}
    Path(__file__).with_name("bank_reference_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    check()
