#!/usr/bin/env python3
"""Event-driven reference for a single outstanding ROI task and display snapshot.

The model specifies transaction semantics before RTL exists.  A source mailbox
payload remains stable from publish through synchronized acknowledgement.  The
destination copies it on request acceptance, but acknowledgement is generated
only after an explicit RAM-last-read event.  HDMI results are pending until a
VSYNC boundary and remain frozen for the whole displayed frame.
"""
from __future__ import annotations

import argparse
import copy
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    transaction_id: int
    frame_id: int
    bank_id: int
    bank_generation: int
    payload: object


@dataclass
class Bank:
    state: str = "FREE"
    frame_id: int | None = None
    generation: int = 0
    payload: object | None = None


class SingleTaskProtocolModel:
    """Two-bank storage with at most one published/destination task."""

    def __init__(self, request_sync_cycles: int = 2, ack_sync_cycles: int = 2,
                 display_sync_cycles: int = 2, frame_bits: int = 32,
                 transaction_bits: int = 32, bank_generation_bits: int = 32):
        if min(request_sync_cycles, ack_sync_cycles, display_sync_cycles) < 1:
            raise ValueError("CDC delivery latency must be positive")
        self.request_sync_cycles = request_sync_cycles
        self.ack_sync_cycles = ack_sync_cycles
        self.display_sync_cycles = display_sync_cycles
        self.frame_bits = frame_bits
        self.transaction_bits = transaction_bits
        self.bank_generation_bits = bank_generation_bits
        self.frame_modulus = 1 << frame_bits
        self.transaction_modulus = 1 << transaction_bits
        self.bank_generation_modulus = 1 << bank_generation_bits
        self.time = 0
        self.next_transaction_id = 0
        self.generation = 0
        self.events: list[tuple[int, str, object]] = []
        self.log: list[dict[str, object]] = []
        self.counters: dict[str, int] = {}
        self.banks = [Bank(), Bank()]
        self.capturing_bank: int | None = None
        self.next_bank_hint = 0
        self.dropped_capture_frame: int | None = None
        self.outstanding: Task | None = None
        self.destination_task: Task | None = None
        self.visible_request: Task | None = None
        self.destination_read_done = False
        self.last_completed: Task | None = None
        self.pending_display: dict[str, object] | None = None
        self.active_display: dict[str, object] | None = None
        self.display_frame_id: int | None = None

    def _count(self, name: str) -> None:
        self.counters[name] = self.counters.get(name, 0) + 1

    def _log(self, event: str, **values: object) -> None:
        self.log.append({"time": self.time, "event": event, **values})

    def _schedule(self, delay: int, kind: str, value: object) -> None:
        self.events.append((self.time + delay, kind, copy.deepcopy(value)))

    @staticmethod
    def same_task(left: Task | None, right: Task | None) -> bool:
        return left is not None and right is not None and (
            left.transaction_id, left.frame_id, left.bank_id, left.bank_generation) == (
                right.transaction_id, right.frame_id, right.bank_id, right.bank_generation)

    def coordinated_reset(self) -> None:
        """Reset all modeled domains together and invalidate in-flight CDC events."""
        self.generation += 1
        self.events.clear()
        self.banks = [Bank(), Bank()]
        self.capturing_bank = None
        self.next_bank_hint = 0
        self.dropped_capture_frame = None
        self.outstanding = None
        self.destination_task = None
        self.visible_request = None
        self.destination_read_done = False
        self.last_completed = None
        self.pending_display = None
        self.active_display = None
        self.display_frame_id = None
        self._count("coordinated_reset")
        self._log("coordinated_reset", generation=self.generation)

    def source_sof(self, frame_id: int, payload: object) -> bool:
        frame_id %= self.frame_modulus
        if self.capturing_bank is not None or self.dropped_capture_frame is not None:
            raise ValueError("new SOF before prior frame EOF")
        order = [(self.next_bank_hint + offset) % len(self.banks) for offset in range(len(self.banks))]
        free = next((index for index in order if self.banks[index].state == "FREE"), None)
        if free is None:
            self.dropped_capture_frame = frame_id
            self._count("busy_frame_drop")
            self._log("source_sof_drop", frame_id=frame_id, reason="no_free_bank")
            return False
        bank = self.banks[free]
        bank.generation = (bank.generation + 1) % self.bank_generation_modulus
        bank.state, bank.frame_id, bank.payload = "CAPTURING", frame_id, copy.deepcopy(payload)
        self.capturing_bank = free
        self.next_bank_hint = (free + 1) % len(self.banks)
        self._log("source_sof_capture", frame_id=frame_id, bank_id=free,
                  bank_generation=bank.generation)
        return True

    def source_eof(self, frame_id: int, publish_payload: object | None = None) -> Task | None:
        frame_id %= self.frame_modulus
        if self.dropped_capture_frame is not None:
            if frame_id != self.dropped_capture_frame:
                raise ValueError("dropped frame EOF identity mismatch")
            self.dropped_capture_frame = None
            self._log("source_eof_drop", frame_id=frame_id)
            return None
        if self.capturing_bank is None:
            raise ValueError("EOF without captured SOF")
        bank_id = self.capturing_bank
        bank = self.banks[bank_id]
        if bank.frame_id != frame_id or bank.state != "CAPTURING":
            raise ValueError("captured EOF/state mismatch")
        if self.outstanding is not None:
            # There is no second mailbox slot.  A frame may be captured into
            # the other bank while the prior task is reading; if its ack has
            # still not arrived by EOF, discard the whole captured frame.
            bank.state, bank.frame_id, bank.payload = "FREE", None, None
            self.capturing_bank = None
            self._count("publish_busy_frame_drop")
            self._log("source_eof_drop", frame_id=frame_id,
                      reason="single_mailbox_still_outstanding")
            return None
        if publish_payload is not None:
            bank.payload = copy.deepcopy(publish_payload)
        task = Task(self.next_transaction_id, frame_id, bank_id, bank.generation,
                    copy.deepcopy(bank.payload))
        self.next_transaction_id = (self.next_transaction_id + 1) % self.transaction_modulus
        bank.state = "PUBLISHED"
        self.capturing_bank = None
        self.outstanding = task
        self._schedule(self.request_sync_cycles, "request_arrival", task)
        self._count("published_task")
        self._log("source_publish", transaction_id=task.transaction_id,
                  frame_id=frame_id, bank_id=bank_id, bank_generation=task.bank_generation)
        return task

    def destination_ram_read_done(self, transaction_id: int) -> None:
        task = self.destination_task
        if task is None or task.transaction_id != transaction_id or self.destination_read_done:
            raise ValueError("RAM-read-done does not match one active unread task")
        self.destination_read_done = True
        self._schedule(self.ack_sync_cycles, "ack_arrival", task)
        self._count("ram_read_done")
        self._log("destination_ram_read_done", transaction_id=transaction_id,
                  frame_id=task.frame_id, bank_id=task.bank_id)

    def destination_done(self, transaction_id: int, result: object) -> None:
        task = self.destination_task
        if task is None or task.transaction_id != transaction_id:
            raise ValueError("algorithm done does not match active task")
        if not self.destination_read_done:
            raise ValueError("algorithm done before explicit RAM-last-read")
        display_payload = {"transaction_id": task.transaction_id, "source_frame_id": task.frame_id,
                           "result": copy.deepcopy(result)}
        self._schedule(self.display_sync_cycles, "display_arrival", display_payload)
        self.last_completed = task
        self.destination_task = None
        self.destination_read_done = False
        self._count("algorithm_done")
        self._log("destination_done", transaction_id=transaction_id, frame_id=task.frame_id)
        self._try_accept_visible()

    def inject_duplicate_request(self, task: Task, delay: int = 1) -> None:
        self._schedule(delay, "request_arrival", task)

    def inject_duplicate_ack(self, task: Task, delay: int = 1) -> None:
        self._schedule(delay, "ack_arrival", task)

    def _request_arrival(self, task: Task) -> None:
        if self.destination_task is not None:
            if self.same_task(self.destination_task, task):
                self._count("duplicate_request")
                self._log("duplicate_request_ignored", transaction_id=task.transaction_id)
                return
            if self.visible_request is not None:
                if self.same_task(self.visible_request, task):
                    self._count("duplicate_request")
                    self._log("visible_request_duplicate_ignored", transaction_id=task.transaction_id)
                    return
                raise AssertionError("more than one unconsumed mailbox transaction")
            if not self.same_task(self.outstanding, task):
                self._count("stale_request")
                self._log("stale_request_ignored", transaction_id=task.transaction_id)
                return
            self.visible_request = copy.deepcopy(task)
            self._count("request_wait_busy")
            self._log("request_visible_waiting_for_executor", transaction_id=task.transaction_id,
                      frame_id=task.frame_id, bank_id=task.bank_id,
                      bank_generation=task.bank_generation)
            return
        if self.same_task(self.last_completed, task):
            self._count("duplicate_request")
            self._log("completed_request_duplicate_ignored", transaction_id=task.transaction_id)
            return
        if not self.same_task(self.outstanding, task):
            self._count("stale_request")
            self._log("stale_request_ignored", transaction_id=task.transaction_id)
            return
        self.visible_request = copy.deepcopy(task)
        self._try_accept_visible()

    def _try_accept_visible(self) -> None:
        if self.destination_task is not None or self.visible_request is None:
            return
        task = self.visible_request
        if not self.same_task(self.outstanding, task):
            self._count("stale_request")
            self._log("stale_visible_request_ignored", transaction_id=task.transaction_id)
            self.visible_request = None
            return
        # This is the mailbox data-copy point.  No acknowledgement occurs here.
        self.destination_task = copy.deepcopy(task)
        self.visible_request = None
        self.destination_read_done = False
        self._count("destination_accept")
        self._log("destination_accept_and_copy", transaction_id=task.transaction_id,
                  frame_id=task.frame_id, bank_id=task.bank_id,
                  bank_generation=task.bank_generation)

    def _ack_arrival(self, task: Task) -> None:
        if not self.same_task(self.outstanding, task):
            self._count("duplicate_or_stale_ack")
            self._log("duplicate_or_stale_ack_ignored", transaction_id=task.transaction_id)
            return
        bank = self.banks[task.bank_id]
        if (bank.state != "PUBLISHED" or bank.frame_id != task.frame_id or
                bank.generation != task.bank_generation):
            raise AssertionError("ack identity does not own the published bank")
        bank.state, bank.frame_id, bank.payload = "FREE", None, None
        self.outstanding = None
        self._count("ack_release")
        self._log("source_ack_release", transaction_id=task.transaction_id,
                  frame_id=task.frame_id, bank_id=task.bank_id,
                  bank_generation=task.bank_generation)

    def _display_arrival(self, payload: dict[str, object]) -> None:
        if self.pending_display is not None:
            self._count("display_pending_overwrite")
            self._log("display_pending_overwrite",
                      replaced_source_frame_id=self.pending_display["source_frame_id"],
                      new_source_frame_id=payload["source_frame_id"])
        self.pending_display = copy.deepcopy(payload)
        self._count("display_pending_update")
        self._log("display_pending_update", source_frame_id=payload["source_frame_id"])

    def hdmi_vsync(self, display_frame_id: int) -> None:
        display_frame_id %= self.frame_modulus
        if self.pending_display is not None:
            self.active_display = self.pending_display
            self.pending_display = None
            source_frame_id = int(self.active_display["source_frame_id"])
            self.active_display["effective_display_frame_id"] = display_frame_id
            self.active_display["frame_id_modulo_delta"] = (
                display_frame_id - source_frame_id) % self.frame_modulus
            self._count("display_swap")
            self._log("display_vsync_swap", display_frame_id=display_frame_id,
                      source_frame_id=source_frame_id,
                      frame_id_modulo_delta=self.active_display["frame_id_modulo_delta"])
        else:
            self._log("display_vsync_hold", display_frame_id=display_frame_id)
        self.display_frame_id = display_frame_id

    def tick(self, *, reset: bool = False, sof: tuple[int, object] | None = None,
             eof: int | tuple[int, object] | None = None, vsync: int | None = None) -> None:
        """Advance one model cycle with a defined same-cycle priority.

        Priority is coordinated reset; synchronized CDC arrivals (request,
        acknowledgement, display); source SOF; source EOF; HDMI VSYNC.  Thus an
        acknowledgement arriving with SOF releases its bank before allocation,
        and a display update arriving with VSYNC becomes active on that VSYNC.
        """
        self.time += 1
        if reset:
            self.coordinated_reset()
            self._assert_invariants()
            return
        due = sorted((event for event in self.events if event[0] <= self.time),
                     key=lambda event: {"request_arrival": 0, "ack_arrival": 1,
                                        "display_arrival": 2}[event[1]])
        self.events = [event for event in self.events if event[0] > self.time]
        for _, kind, value in due:
            if kind == "request_arrival":
                self._request_arrival(value)
            elif kind == "ack_arrival":
                self._ack_arrival(value)
            else:
                self._display_arrival(value)
        if sof is not None:
            self.source_sof(*sof)
        if eof is not None:
            if isinstance(eof, tuple):
                self.source_eof(*eof)
            else:
                self.source_eof(eof)
        if vsync is not None:
            self.hdmi_vsync(vsync)
        self._assert_invariants()

    def _assert_invariants(self) -> None:
        published = [index for index, bank in enumerate(self.banks) if bank.state == "PUBLISHED"]
        if self.outstanding is None:
            assert not published
        else:
            assert published == [self.outstanding.bank_id]
            bank = self.banks[self.outstanding.bank_id]
            assert bank.frame_id == self.outstanding.frame_id
            assert bank.generation == self.outstanding.bank_generation
            assert bank.payload == self.outstanding.payload
        if self.destination_task is not None:
            # After last RAM read, the copied task can remain in HOG/SVM while
            # its source bank has already been acknowledged and reused.
            if not self.destination_read_done:
                assert self.same_task(self.destination_task, self.outstanding)
        if self.visible_request is not None:
            assert self.same_task(self.visible_request, self.outstanding)
        if self.capturing_bank is not None:
            assert self.banks[self.capturing_bank].state == "CAPTURING"

    def contract(self) -> dict[str, object]:
        return {
            "status": "executable_protocol_reference_not_RTL",
            "single_outstanding": True,
            "mailbox_payload_stability": "source holds transaction/frame/bank/payload until matching synchronized ack",
            "publish_payload": "frame/object payload is frozen at source EOF publication; SOF payload is capture metadata/default only",
            "destination_copy_point": "request arrival after request synchronizer",
            "ack_point": "destination explicit RAM-last-read; ack arrival releases only the source bank while the copied task may remain in HOG/SVM",
            "busy_destination_mailbox": "one synchronized request remains visible and stable while the old copied task finishes; it is accepted immediately when the executor becomes idle",
            "algorithm_done": "may occur only after RAM-last-read and creates display CDC update",
            "same_cycle_priority": ["coordinated reset", "CDC arrivals", "source SOF", "source EOF", "HDMI VSYNC"],
            "busy_policy": "a free second bank may capture while one task is outstanding; if matching ack has not arrived by EOF, that whole captured frame is discarded instead of queued",
            "duplicate_policy": "duplicates whose full identity differs are counted and ignored; finite-width full-tuple wrap cannot distinguish an arbitrarily delayed old ack",
            "reset": "coordinated reset clears banks, mailboxes, destination task, queued CDC events and display tables",
            "nominal_identity_widths": {"source_frame_id": self.frame_bits,
                                        "transaction_id": self.transaction_bits,
                                        "bank_generation": self.bank_generation_bits},
            "identity_width_status": "Python nominal values only; arch_lead must freeze RTL widths from frame rate and maximum stale-message lifetime",
            "frame_wrap": f"frame IDs compare modulo {self.frame_modulus}; transaction identity remains independent until the complete identity tuple aliases",
            "bank_generation": f"each round-robin bank allocation increments its own generation modulo {self.bank_generation_modulus}; transaction/frame/bank/generation all participate in ack matching",
            "wrap_safety_requirement": "the maximum lifetime of any synchronized request/ack must be strictly shorter than the minimum full-identity alias interval; use a level/toggle handshake plus coordinated reset flushing, and prove this bound before RTL",
            "HDMI": "CDC result writes pending; the latest completed snapshot before the modeled VSYNC boundary event wins; VSYNC atomically replaces active, records both display/source frame IDs plus frame_id_modulo_delta, and active is frozen until another VSYNC; the delta is not latency unless the two counters share a measured epoch/cadence; RTL must freeze the physical VSYNC edge/polarity",
        }


def randomized_trial(seed: int, cycles: int = 2000) -> dict[str, object]:
    rng = random.Random(seed)
    model = SingleTaskProtocolModel(frame_bits=4, transaction_bits=6)
    next_frame = 0
    active_end: int | None = None
    read_delay = done_delay = None
    display_frame = 0
    for cycle in range(cycles):
        if rng.random() < 0.006:
            model.tick(reset=True)
            active_end = read_delay = done_delay = None
            continue
        sof = eof = vsync = None
        if active_end is None and rng.random() < 0.18:
            sof = (next_frame, {"objects": [next_frame, seed]})
            active_end = cycle + rng.randint(1, 3)
        if active_end == cycle:
            eof = next_frame
            next_frame = (next_frame + 1) % model.frame_modulus
            active_end = None
        if cycle % 17 == 0:
            vsync = display_frame
            display_frame = (display_frame + 1) % model.frame_modulus
        model.tick(sof=sof, eof=eof, vsync=vsync)
        if (model.destination_task is not None and not model.destination_read_done and
                read_delay is None and done_delay is None):
            read_delay = rng.randint(1, 5)
        if read_delay is not None:
            read_delay -= 1
            if read_delay == 0 and model.destination_task is not None:
                transaction = model.destination_task.transaction_id
                model.destination_ram_read_done(transaction)
                done_delay = rng.randint(1, 4)
                read_delay = None
        if done_delay is not None:
            done_delay -= 1
            if done_delay == 0 and model.destination_task is not None:
                transaction = model.destination_task.transaction_id
                model.destination_done(transaction, {"class": transaction & 1})
                done_delay = None
        if model.outstanding is not None and rng.random() < 0.01:
            model.inject_duplicate_request(model.outstanding)
    return {"seed": seed, "cycles": cycles, "counters": model.counters,
            "event_count": len(model.log), "contract": model.contract()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 7, 23, 101])
    parser.add_argument("--cycles", type=int, default=2000)
    args = parser.parse_args()
    if args.cycles < 1:
        raise ValueError("--cycles must be positive")
    trials = [randomized_trial(seed, args.cycles) for seed in args.seeds]
    args.output.mkdir(parents=True, exist_ok=True)
    result = {"status": "pass", "trials": trials,
              "randomized_test_configuration": {
                  "frame_bits": 4, "transaction_bits": 6,
                  "bank_generation_bits": 8, "purpose": "accelerated wrap/reset stress only"},
              "contract": SingleTaskProtocolModel().contract()}
    (args.output / "protocol_contract.json").write_text(
        json.dumps(result["contract"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "randomized_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "seeds": args.seeds,
                      "cycles_per_seed": args.cycles}, ensure_ascii=False))


if __name__ == "__main__":
    main()
