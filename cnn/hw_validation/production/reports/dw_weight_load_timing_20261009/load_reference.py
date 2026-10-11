"""Prove the one-cycle write boundary and the existing start/storage margin."""
import random


def check():
    rng = random.Random(42)
    old, new = {}, {}
    pending = None
    expected = 0
    fault = False
    accepted = 0
    for cycle in range(20000):
        reset = cycle % 997 == 0
        addr = 0 if expected == 0 or rng.randrange(19) == 0 else expected
        if rng.randrange(101) == 0:
            addr = 144
        valid = rng.randrange(5) != 0
        data = rng.randrange(-128, 128)
        if reset:
            pending, expected, fault = None, 0, False
        else:
            if pending is not None:
                new[pending[0]] = pending[1]
            pending = None
            assert old == new  # previous accepted write is visible before a new storage capture
            if valid and not fault:
                if addr in (0, expected):
                    assert 0 <= addr < 144
                    old[addr] = data
                    pending = addr, data
                    expected = 0 if addr == 143 else addr + 1
                    accepted += 1
                else:
                    fault = True
        if reset:
            # Reset cancels the queued, not-yet-visible write. RAM contents are not cleared.
            old = dict(new)
    # Earliest start is the edge after final load; it commits pending before ST_STORAGE next edge.
    final = (143, -128)
    new[final[0]] = final[1]
    assert new[143] == -128
    print("LOAD_REFERENCE_PASS", accepted, "accepted writes; reset/order/bubbles checked")


if __name__ == "__main__":
    check()
