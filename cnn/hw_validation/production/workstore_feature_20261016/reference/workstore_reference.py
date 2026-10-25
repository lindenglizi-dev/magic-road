"""WIF1整数存储参考；只验证显式覆盖的数据，不使用RAM初值。"""

import argparse
import hashlib
import json
from pathlib import Path


WORD_MASK = (1 << 80) - 1
WEIGHT_MASK = (1 << 192) - 1


def pack_weight(value):
    """低位在前，最后80位word只使用低32位。"""
    if not 0 <= value <= WEIGHT_MASK:
        raise ValueError("weight payload must be unsigned 192 bits")
    return tuple((value >> (80 * word)) & WORD_MASK for word in range(3))


def unpack_weight(words):
    """检查三个80位word及第三word的48位零填充。"""
    if len(words) != 3 or any(not 0 <= word <= WORD_MASK for word in words):
        raise ValueError("expected three unsigned 80 bit words")
    if words[2] >> 32:
        raise ValueError("last word high 48 bits must be zero")
    return sum(word << (80 * index) for index, word in enumerate(words))


class WorkstoreReference:
    """逻辑参考，不模拟native延迟；读前覆盖属于client前提。"""

    def __init__(self):
        self.byte_memory = {}
        self.weight_memory = {}
        self.reset()

    def reset(self):
        """取消本任务覆盖资格，保留内容；RTL reset仅取消事务。"""
        self.fault = False
        self.byte_covered = set()
        self.weight_covered = set()

    def byte(self, write, address, data=0):
        """返回(data,error)；非法地址不访问或改变存储。"""
        if not 0 <= address < 3072:
            self.fault = True
            return 0, True
        location = address >> 11, address & 2047
        if write:
            if not 0 <= data < 256:
                raise ValueError("byte payload must be unsigned 8 bits")
            self.byte_memory[location] = data
            self.byte_covered.add(location)
            return 0, False
        if location not in self.byte_covered:
            raise ValueError("client must overwrite byte before read")
        return self.byte_memory[location], False

    def weight(self, write, group, data=0):
        """24个group，各自独占三个连续native地址。"""
        if not 0 <= group < 24:
            self.fault = True
            return 0, True
        addresses = tuple(3 * group + index for index in range(3))
        if write:
            for address, word in zip(addresses, pack_weight(data)):
                self.weight_memory[address] = word
            self.weight_covered.add(group)
            return 0, False
        if group not in self.weight_covered:
            raise ValueError("client must overwrite entire group before read")
        return unpack_weight(tuple(self.weight_memory[a] for a in addresses)), False


def self_check():
    """完整地址覆盖、覆盖重写、位行走、越界隔离及reset资格。"""
    store = WorkstoreReference()
    checks = 0
    for operation in (lambda: store.byte(False, 0), lambda: store.weight(False, 0)):
        try:
            operation()
        except ValueError:
            checks += 1
        else:
            raise AssertionError("uncovered read accepted by reference")
    for generation in range(2):
        for address in range(3072):
            value = (address * 53 + generation * 91) & 255
            assert store.byte(True, address, value) == (0, False)
            assert store.byte(False, address) == (value, False)
            checks += 2
        for group in range(24):
            value = ((group + 1) * 0x123456789abcdef123456789abcdef123456789abcdef) & WEIGHT_MASK
            value ^= WEIGHT_MASK if generation else 0
            assert store.weight(True, group, value) == (0, False)
            assert store.weight(False, group) == (value, False)
            assert store.weight_memory[3 * group + 2] >> 32 == 0
            checks += 3
    for bit in range(192):
        assert unpack_weight(pack_weight(1 << bit)) == 1 << bit
        checks += 1
    before = store.byte_memory.copy(), store.weight_memory.copy()
    for address in (-1, 3072, 4095):
        for write in (False, True):
            assert store.byte(write, address, 255) == (0, True)
            checks += 1
    for group in (-1, 24, 31):
        for write in (False, True):
            assert store.weight(write, group, WEIGHT_MASK) == (0, True)
            checks += 1
    assert before == (store.byte_memory, store.weight_memory) and store.fault
    store.reset()
    assert before == (store.byte_memory, store.weight_memory) and not store.fault
    assert not store.byte_covered and not store.weight_covered
    assert store.byte(True, 3071, 0xA7) == (0, False)
    assert store.byte(False, 3071) == (0xA7, False)
    assert store.weight(True, 23, WEIGHT_MASK) == (0, False)
    assert store.weight(False, 23) == (WEIGHT_MASK, False)
    for words in ((0, 0, 1 << 32), (0, 0, 0, 0), (1 << 80, 0, 0)):
        try:
            unpack_weight(words)
        except ValueError:
            checks += 1
        else:
            raise AssertionError("invalid native word accepted")
    return {"status": "PASS", "checks": checks + 7, "byte_addresses": 3072,
            "weight_groups": 24, "native_weight_addresses": 72,
            "boundary": "Python integer/storage semantics only; no native RAM latency, RTL simulation, TD mapping or silicon guarantee"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    arguments = parser.parse_args()
    result = self_check()
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if arguments.report:
        arguments.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
