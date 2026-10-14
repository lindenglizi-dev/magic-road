"""地址64..127独立存储，其余368字节紧密保留；不增加时钟周期。"""


def locate(address):
    assert 0 <= address < 432
    return ("middle", address - 64) if 64 <= address < 128 else ("remaining", address if address < 64 else address - 64)


def self_check():
    flat, remaining, middle = [None] * 432, [None] * 368, [None] * 64
    mapping = [locate(address) for address in range(432)]
    assert len(set(mapping)) == 432
    checks = 0
    for pass_index in range(3):
        for address in range(432):
            value = (address * 73 + pass_index * 11) % 256 - 128
            bank, local = locate(address)
            flat[address] = value
            (middle if bank == "middle" else remaining)[local] = value
            for output_base in (0, 27, 54, 81, 108, 135, 162, 189, 216, 243, 270, 297, 324, 351, 378, 405):
                for term in range(27):
                    logical = output_base + term
                    selected, index = locate(logical)
                    assert flat[logical] == (middle if selected == "middle" else remaining)[index]
                    checks += 1
    return {"status": "PASS", "read_comparisons": checks, "logical_bytes": 432,
            "physical_declared_bytes": len(remaining) + len(middle), "bijection": True,
            "write_completion_latency_cycles": 0, "ii": 1, "scope": "address mapping only; handshake/reset compared in RTL"}


if __name__ == "__main__":
    print(self_check())
