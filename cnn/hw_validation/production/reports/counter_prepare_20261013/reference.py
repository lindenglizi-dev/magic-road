"""只证明发行计数的二值可达状态等价；全RTL/四态/实际时序另行验证。"""
from collections import deque
from itertools import product

IDLE, STORAGE, SEND, DW_DRAIN, PW_DRAIN, DONE, FAULT = 0, 1, 2, 4, 5, 6, 7
INITIAL = (IDLE, 0, 0, 0, 0, 0)


def prepared_value(layer, position, output):
    if layer:
        if output < 7:
            return output + 1
        return 0 if position < 15 else output
    return output + 1 if output < 15 else 0


def old_counter(state, layer, position, output, last, accept, start, drained, fault):
    if fault:
        return output
    if state == IDLE and start:
        return 0
    if state == SEND and accept and last:
        if layer:
            if output < 7:
                return output + 1
            if position < 15:
                return 0
            return output
        if output < 15:
            return output + 1
        return 0
    if state == DW_DRAIN and drained:
        return 0
    return output


def self_check():
    queue, seen = deque([INITIAL]), {INITIAL}
    transitions = last_checks = resets = faults = 0
    final_pw_holds = dw_wraps = maximum_rate_pw = 0
    unique_last = set()
    while queue:
        current = queue.popleft()
        state, layer, position, output, group, prepared = current
        # ready includes the existing credit/valid guards; fault modes block input acceptance.
        for ready, start_mode, drained, fault in product((0, 1), (-1, 0, 1), (0, 1), (0, 1, 2, 3)):
            transitions += 1
            start = state == IDLE and start_mode >= 0 and not fault
            accept = state == SEND and bool(ready) and not fault
            last = group == (1 if layer else 2)
            if accept and last:
                assert prepared == prepared_value(layer, position, output), current
                last_checks += 1
                unique_last.add((layer, position, output, group, prepared))
                final_pw_holds += bool(layer and position == 15 and output == 7)
                dw_wraps += bool(not layer and output == 15)
            expected = old_counter(state, layer, position, output, last, accept, start, drained, fault)
            actual = output
            if not fault:
                if state == IDLE and start or state == DW_DRAIN and drained:
                    actual = 0
                elif state == SEND and accept and last:
                    actual = prepared
            assert actual == expected, (current, ready, start_mode, drained, fault)
            next_state, next_layer, next_position, next_group = state, layer, position, group
            if fault:
                next_state = FAULT
                faults += 1
            elif state == IDLE and start:
                next_state, next_layer, next_position, next_group = STORAGE, start_mode, 0, 0
            elif state == STORAGE:
                next_state = SEND
            elif state == SEND and accept:
                if not last:
                    next_group = group + 1
                    next_state = SEND if layer else STORAGE
                    maximum_rate_pw += bool(layer and group == 0)
                else:
                    next_group = 0
                    if layer:
                        if output == 7 and position == 15:
                            next_state = PW_DRAIN
                        elif output == 7:
                            next_position = position + 1
                    elif output == 15 and position == 15:
                        next_state = DW_DRAIN
                    else:
                        next_state = STORAGE
                        if output == 15:
                            next_position = position + (3 if position % 4 == 0 else 1)
            elif state == DW_DRAIN and drained:
                next_state, next_layer, next_position, next_group = STORAGE, 1, 0, 0
            elif state == PW_DRAIN and drained:
                next_state = DONE
            elif state == DONE:
                next_state = IDLE
            next_record = (next_state, next_layer, next_position, actual, next_group,
                           prepared_value(layer, position, output))
            if next_record not in seen:
                seen.add(next_record)
                queue.append(next_record)
        # Reset is permitted in every reachable issuer state, including fault and stalled last.
        resets += 1
        assert INITIAL[3] == INITIAL[5] == 0
    assert last_checks and final_pw_holds and dw_wraps and maximum_rate_pw
    # Broader single-edge binary decode proof, conditional on a correctly prepared value.
    decode_cases = 0
    for state, layer, position, output, accept, last, start, drained, fault in product(
            range(16), range(2), range(16), range(32), range(2), range(2), range(2), range(2), range(2)):
        expected = old_counter(state, layer, position, output, last, accept, start, drained, fault)
        actual = output
        if not fault:
            if state == IDLE and start or state == DW_DRAIN and drained:
                actual = 0
            elif state == SEND and accept and last:
                actual = prepared_value(layer, position, output)
        assert actual == expected
        decode_cases += 1
    assert len(unique_last) == 256
    return {"status": "PASS", "reachable_states": len(seen), "transitions": transitions,
            "legal_last_prepared_checks": last_checks, "unique_legal_last_states": len(unique_last),
            "reset_contract_checks": resets, "fault_edges": faults,
            "final_pw_holds": final_pw_holds, "dw_wraps": dw_wraps,
            "maximum_rate_pw_first_edges": maximum_rate_pw, "binary_decode_cases": decode_cases,
            "scope": "Issuer abstraction and binary recurrence; reset counts check only the declared initial contract, not RTL reset execution"}


if __name__ == "__main__":
    print(self_check())
