"""Cycle model for the one-entry ROM-to-runner ingress register."""

from dataclasses import dataclass


Word = tuple[int, int, int]


@dataclass
class Ingress:
    pending: Word | None = None
    external_owner: bool = False

    def step(
        self,
        *,
        rstn: bool = True,
        fault: bool = False,
        pref_valid: bool = False,
        pref_word: Word = (0, 0, 0),
        pref_done: bool = False,
        table_loaded: bool = False,
        external_valid: bool = False,
        external_word: Word = (0, 0, 0),
        runner_ready: bool = False,
    ) -> dict[str, object]:
        enabled = rstn and not fault
        was_empty = self.pending is None
        pref_ready = enabled and not self.external_owner and self.pending is None
        capture = pref_valid and pref_ready
        consume = enabled and not self.external_owner and self.pending is not None and runner_ready
        runner_valid = enabled and (external_valid if self.external_owner else self.pending is not None)
        runner_word = external_word if self.external_owner else self.pending
        result = {
            "pref_ready": pref_ready,
            "capture": capture,
            "consume": consume,
            "runner_valid": runner_valid,
            "runner_word": runner_word,
            "external_ready": enabled and self.external_owner and runner_ready,
            "external_owner": self.external_owner,
        }

        if not enabled:
            self.pending = None
            self.external_owner = False
            return result

        if capture:
            self.pending = pref_word
        elif consume:
            self.pending = None

        # Ownership changes only after the registered entry was already empty.
        if pref_done and table_loaded and was_empty and not capture:
            self.external_owner = True
        return result


def check() -> None:
    ingress = Ingress()
    first = (3, 17, 0x12345678)
    second = (5, 31, -9)

    ingress.step(rstn=False, pref_valid=True, pref_word=first, runner_ready=True)
    assert ingress.pending is None and not ingress.external_owner

    out = ingress.step(pref_valid=True, pref_word=first, runner_ready=True)
    assert out["capture"] and not out["runner_valid"] and ingress.pending == first

    for _ in range(4):
        out = ingress.step(pref_valid=True, pref_word=second, runner_ready=False)
        assert not out["pref_ready"] and not out["capture"]
        assert out["runner_valid"] and out["runner_word"] == first
        assert ingress.pending == first

    out = ingress.step(pref_valid=True, pref_word=second, runner_ready=True)
    assert out["consume"] and not out["capture"] and out["runner_word"] == first
    assert ingress.pending is None

    ingress.step(pref_valid=True, pref_word=second)
    assert ingress.pending == second
    ingress.step(pref_done=True, table_loaded=True)
    assert not ingress.external_owner and ingress.pending == second
    ingress.step(pref_done=True, table_loaded=True, runner_ready=True)
    assert not ingress.external_owner and ingress.pending is None
    ingress.step(pref_done=True, table_loaded=True)
    assert ingress.external_owner

    out = ingress.step(external_valid=True, external_word=first, runner_ready=False)
    assert out["runner_valid"] and out["runner_word"] == first and not out["external_ready"]
    out = ingress.step(external_valid=True, external_word=first, runner_ready=True)
    assert out["runner_valid"] and out["external_ready"]

    out = ingress.step(fault=True, external_valid=True, external_word=second, runner_ready=True)
    assert not out["runner_valid"] and not out["external_ready"]
    assert ingress.pending is None and not ingress.external_owner

    ingress.step(pref_valid=True, pref_word=first)
    assert ingress.pending == first
    ingress.step(rstn=False)
    assert ingress.pending is None and not ingress.external_owner
    print("INGRESS_REFERENCE_PASS capacity=1 stall=4 cancel=2 drain=1 no_same_cycle_refill=1")


if __name__ == "__main__":
    check()
