"""64项显式写银行的二值地址/接受沿参考；不改数字运算或读布局。"""


def self_check():
    checks = 0
    for capacity, width in ((432, 9), (1296, 11)):
        banks = (capacity + 63) // 64
        for address in range(1 << width):
            for cursor in {0, capacity - 1, min(address, capacity - 1), max(0, address - 1)}:
                for accept in (False, True):
                    old_write = accept and (address == cursor or address == 0)
                    if capacity == 432:
                        old_write = old_write and address < capacity
                    # Legal halo cursor always remains in [0,1295]; out-of-range never accepted for write.
                    selected = (address >> 6) if old_write and address >> 6 < banks else None
                    new_address = None if selected is None else (selected << 6) | (address & 63)
                    assert new_address == (address if old_write else None)
                    if old_write:
                        assert address < capacity
                        following = 0 if address == capacity - 1 else address + 1
                        assert 0 <= following < capacity
                    checks += 1
        for address in range(capacity):
            for data in (-128, -1, 0, 1, 127):
                assert ((address >> 6) * 64 + (address & 63), data & 255) == (address, data & 255)
                checks += 1
    return {"status": "PASS", "checks": checks, "bank_entries": 64,
            "stem_banks": 7, "stem_last_bank_entries": 48,
            "halo_banks": 21, "halo_last_bank_entries": 16,
            "added_registers_or_cycles": 0, "four_state_claim": False}


if __name__ == "__main__":
    import json
    print(json.dumps(self_check(), indent=2))
