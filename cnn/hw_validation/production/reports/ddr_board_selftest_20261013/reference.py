"""独占 DDR 自检向量；原生 PAXI 地址不解释为 CNN 字节地址。"""

ADDRESSES = (0, 8, 16, 24)
FULL_MASK = (1 << 128) - 1


def pattern(round_index, address_index):
    """每地址各字节有区别，第二轮取反；小端字节序与 PAXI 总线对应。"""
    value = int.from_bytes(bytes((lane * 13 + address_index * 37) & 255
                                 for lane in range(16)), "little")
    return value ^ (FULL_MASK if round_index else 0)


def transactions():
    """每轮先写四地址，再逆序读；禁止从握手推断生产写完成。"""
    for round_index in range(2):
        for index, address in enumerate(ADDRESSES):
            yield "write", address, pattern(round_index, index)
        for index in reversed(range(len(ADDRESSES))):
            yield "read", ADDRESSES[index], pattern(round_index, index)


def self_check():
    memory = {}
    sequence = list(transactions())
    assert len(sequence) == 16
    assert len({value for _, _, value in sequence}) == 8
    for operation, address, value in sequence:
        assert address % 8 == 0 and 0 <= address < (1 << 25)
        assert 0 <= value <= FULL_MASK
        if operation == "write":
            memory[address] = value
        else:
            assert memory[address] == value
    for index in range(4):
        assert pattern(0, index) ^ pattern(1, index) == FULL_MASK
    print("REFERENCE_PASS operations=16 writes=8 reads=8 compared_bytes=128")
    for round_index in range(2):
        for index, address in enumerate(ADDRESSES):
            print(f"VECTOR {round_index} {index} {address:07x} {pattern(round_index, index):032x}")


if __name__ == "__main__":
    self_check()
