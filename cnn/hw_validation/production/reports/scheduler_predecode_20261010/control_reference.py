"""二值控制等价穷举：计数后继、原故障优先级和操作数捕获，不覆盖X/Z语义。"""
from itertools import product
import json
from pathlib import Path


def old_counter(state, count, position, pw, last, accept, start, drain, fault):
    clear, increment = False, False
    if state == 0:
        clear = start
    elif state == 2 and accept and last:
        if pw:
            if count < 7:
                increment = True
            elif position < 15:
                clear = True
        elif count < 15:
            increment = True
        else:
            clear = True
    elif state == 4:
        clear = drain
    return count if fault else 0 if clear else (count + 1) & 31 if increment else count


def new_counter(state, count, position, pw, last, accept, start, drain, fault):
    successor, update = 0, False
    if state == 0:
        update = start
    elif state == 2:
        update = accept and last
        if pw:
            successor = (count + 1) & 31 if count < 7 else 0 if position < 15 else count
        else:
            successor = (count + 1) & 31 if count < 15 else 0
    elif state == 4:
        update = drain
    return successor if update and not fault else count


def old_capture(state, count, position, pw, last, accept, fault):
    if fault:
        return False
    if state == 1:
        return True
    if state == 2 and accept:
        if last:
            return pw and not (count == 7 and position == 15)
        return pw
    return False


def new_capture(state, count, position, pw, last, accept, fault):
    eligible = pw and (not last or not (count == 7 and position == 15))
    return not fault and (state == 1 or (state == 2 and accept and eligible))


def main():
    counters = captures = 0
    # All representable state/count/position values, including unreachable states.
    for state, count, position, pw, last, accept, start, drain, fault in product(
            range(16), range(32), range(16), range(2), range(2), range(2), range(2), range(2), range(2)):
        args = state, count, position, pw, last, accept, start, drain, fault
        assert old_counter(*args) == new_counter(*args), args
        counters += 1
    for args in product(range(16), range(32), range(16), range(2), range(2), range(2), range(2)):
        assert old_capture(*args) == new_capture(*args), args
        captures += 1
    result = {"counter_cases": counters, "payload_capture_cases": captures, "mismatches": 0,
        "scope": "binary equations only; RTL simulation required; reset remains explicit async zero",
        "counter_fault_guard": "pp_fault OR flag_load_fault, unchanged",
        "payload_fault_guard": "flag_fault_flush, unchanged", "additional_pipeline_stages": 0}
    Path(__file__).with_name("control_reference.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
