"""Exhaustive binary control equivalence, before RTL implementation."""
import itertools
import json
from pathlib import Path


def check():
    count = 0
    for read, masks, occupancy, accepted, last, lane in itertools.product(
            range(2), itertools.product(range(8), repeat=2), range(3), range(2), range(2), range(4)):
        entry, mask, valid = read, masks[read], occupancy != 0
        if accepted:
            if last:
                entry, mask, valid = 1 - read, masks[1 - read], occupancy > 1
            else:
                mask &= ~(1 << lane) & 7
        old = (valid, entry, mask, 0 if mask & 1 else 1 if mask & 2 else 2)
        head = (occupancy != 0, read, masks[read])
        following = (occupancy > 1, 1 - read, masks[1 - read]) if last else (
            occupancy != 0, read, masks[read] & (~(1 << lane) & 7))
        valid, entry, mask = following if accepted else head
        new = (valid, entry, mask, 0 if mask & 1 else 1 if mask & 2 else 2)
        assert old == new
        count += 1
    counter_cases = 0
    for state, start, accept, final, pw, output, position, drained, pp_fault, load_fault in itertools.product(
            range(10), range(2), range(2), range(2), range(2), range(16), range(16), range(2), range(2), range(2)):
        # Actual source contracts: start and MAC acceptance already include both fault guards.
        if (start or accept) and (pp_fault or load_fault):
            continue
        clear = (state == 0 and start) or (state == 4 and drained)
        increment = False
        if state == 2 and accept and final:
            if pw:
                increment = output < 7
                clear = output == 7 and position < 15
            else:
                increment = output < 15
                clear = output >= 15
        old = (clear, increment) if not (pp_fault or load_fault) else (False, False)
        new_clear = clear and not (state == 4 and (pp_fault or load_fault))
        assert old == (new_clear, increment)
        counter_cases += 1
    # No X/Z proof: real handshake/stall/fault/reset tests remain mandatory.
    result = {"selection_cases": count, "counter_cases": counter_cases,
              "mismatches": 0, "scope": "binary combinational equations under existing handshake guards"}
    print(json.dumps(result))
    Path(__file__).with_name("control_reference.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    check()
