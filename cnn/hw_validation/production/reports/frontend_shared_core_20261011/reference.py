"""单算子所有权参考：只在空闲、排空且结果已导出后交接。"""


def select_ready(reset, idle, unexported, pending, fault, command):
    return reset and idle and not (unexported or pending or fault or command)


def check():
    assert select_ready(True, True, False, False, False, False)
    for field in range(6):
        args = [True, True, False, False, False, False]
        args[field] = not args[field]
        assert not select_ready(*args), (field, args)
    owner = 0
    # start、在途、done待导出、导出反压、最后导出、空闲，只有最后一步可换主。
    for idle, unexported, pending, command in (
        (True, False, False, True), (False, False, True, False),
        (True, True, False, False), (False, True, False, False),
        (True, True, False, False), (True, False, False, False),
    ):
        if select_ready(True, idle, unexported, pending, False, command):
            owner = 1
    assert owner == 1
    print("OWNERSHIP_REFERENCE_PASS")


if __name__ == "__main__":
    check()
