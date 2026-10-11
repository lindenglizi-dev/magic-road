"""Cross-check independently authored arithmetic vectors and cycle model."""
import json
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root / "core"))
    from road_mac_probe_reference import Group, MacProbeReference

    vectors = json.loads((root / "verification/stream_vectors.json").read_text(encoding="utf-8"))
    model = MacProbeReference()
    pending_accumulators = {}
    accepted = outputs = 0

    def tick(group=None, valid=False, ready=False):
        cycle = model.cycle
        state = model.step(group, valid, ready)
        if cycle in pending_accumulators:
            expected = pending_accumulators.pop(cycle)
            assert list(model.accumulator) == expected, (cycle, model.accumulator, expected)
        return state

    for vector in vectors["vectors"]:
        for _ in range(vector["gap"]):
            tick()
        assert model.input_ready and not model.result_valid
        group = Group(vector["activations"], vector["weights"], vector["mask"],
                      tuple(vector["bias"]), vector["first"], vector["last"])
        assert list(model.dot(group)) == vector["dots"]
        acceptance_cycle = model.cycle
        pending_accumulators[acceptance_cycle + 5] = vector["accumulator_after"]
        state = tick(group, True)
        accepted += 1
        if not vector["last"]:
            assert state[0]
            continue
        assert not state[0] and not state[1]
        for _ in range(8):
            state = tick()
            assert not state[0] and not state[1]
        state = tick()
        assert state == (False, True, tuple(vector["expected_data"]), vector["fault"])
        outputs += 1
        held = state
        for _ in range(vector["stall"]):
            state = tick(group, vector["blocked_input_probe"])
            assert state == held
        state = tick(ready=True)
        assert state[0] and not state[1]
    assert not pending_accumulators
    assert accepted == 123 and outputs == 17
    result = {"status": "INDEPENDENT_REFERENCE_AGREEMENT_PASS", "accepted_groups": accepted,
              "result_transactions": outputs, "last_accept_to_valid_cycles": 9,
              "comparison": "every dot, signed33 committed partial, atomic fault, final result, held payload",
              "scope": "Python contract cross-check, not RTL or physical proof"}
    (root / "independent_reference_agreement.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
