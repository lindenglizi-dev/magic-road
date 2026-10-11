"""Check observable refill and valid-qualified MAC behavior before RTL changes."""
import itertools
import json
from pathlib import Path
import random


def selected(read, masks, count, use_successor, last, lane):
    entry, mask, valid = read, masks[read], count != 0
    if use_successor:
        if last:
            entry, mask, valid = 1 - read, masks[1 - read], count > 1
        else:
            mask &= ~(1 << lane) & 7
    return valid, entry, mask, 0 if mask & 1 else 1 if mask & 2 else 2


def check():
    cases = 0
    for read, masks, count, buffered, ready, last, lane in itertools.product(
            range(2), itertools.product(range(8), repeat=2), range(3), range(2), range(2), range(2), range(4)):
        accepted = buffered and ready
        if not buffered or accepted:
            assert selected(read, masks, count, accepted, last, lane) == selected(
                read, masks, count, buffered, last, lane)
            cases += 1
    rng = random.Random(42)
    old_data = held_data = (0, 0, 0)
    old_valid = held_valid = False
    valid_products = 0
    for tick in range(10000):
        reset = tick % 137 == 0
        accepted = bool(rng.randrange(3))
        payload = (rng.randrange(-128, 128), rng.randrange(-128, 128), rng.randrange(2))
        # Existing A1 may compute an invalid product; it must never own a token.
        assert old_valid == held_valid
        if old_valid:
            assert old_data[0] * old_data[1] * old_data[2] == held_data[0] * held_data[1] * held_data[2]
            valid_products += 1
        if reset:
            old_data = held_data = (0, 0, 0)
            old_valid = held_valid = False
        elif accepted:
            old_data = held_data = payload
            old_valid = held_valid = True
        else:
            old_data = (0, 0, 0)
            old_valid = held_valid = False
    result = {"observable_selection_cases": cases, "mac_input_cycles": 10000,
        "valid_products_compared": valid_products, "mismatches": 0,
        "scope": "binary local control model; not X/Z, RTL, or physical timing proof"}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    check()
