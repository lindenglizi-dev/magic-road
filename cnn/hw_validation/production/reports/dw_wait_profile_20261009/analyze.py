"""Classify the observed frozen-DUT cycles; no inferred acceleration model."""
import csv
import json
from collections import Counter, deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
STATES = {0: "idle", 1: "storage", 2: "mac_send", 3: "mac_wait", 4: "dw_drain",
          5: "pw_drain", 6: "done", 7: "fault", 8: "export", 9: "dw_post"}


def rows(path):
    with path.open(encoding="utf-8") as stream:
        result = []
        for row in csv.DictReader(stream):
            converted = {}
            for key, value in row.items():
                if value.lower() == "x":
                    # Invalid output payload is don't-care, never silently replace a valid X by zero.
                    guard = {"commit_tag": "commit_valid", "pp_position": "pp_valid", "pp_channel": "pp_valid"}
                    assert key in guard and row[guard[key]] == "0", row
                    converted[key] = None
                else:
                    converted[key] = int(value)
            result.append(converted)
        return result


def histogram(values):
    return {str(key): value for key, value in sorted(Counter(values).items())}


def reason(row):
    state = row["state"]
    if state == 2:
        if row["mac_accept"]:
            return "send_accepted"
        if row["group"] == 0 and not row["can_reserve"]:
            return "send_capacity_wait"
        if row["mac_valid"] and not row["mac_ready"]:
            return "send_mac_backpressure"
        return "send_guard_wait"
    if state == 3:
        if row["mac_result_accept"]:
            return "result_captured"
        return "result_blocked" if row["mac_result_valid"] else "result_pipeline_wait"
    if state == 9:
        if row["pp_accept"]:
            return "dw_scalar_accepted"
        return "dw_post_capacity_wait"
    return STATES[state]


def layer_profile(data):
    states = Counter(STATES[row["state"]] for row in data)
    reasons = Counter(reason(row) for row in data)
    activity = Counter(row["pre_busy"] + 2 * row["silu_busy"] + 4 * row["post_busy"] for row in data)
    assert sum(states.values()) == sum(reasons.values()) == sum(activity.values()) == len(data)
    firsts = [r["cycle"] for r in data if r["mac_accept"] and r["group"] == 0]
    pending, last_to_pop, first_to_pop = deque(), [], []
    batch_to_commit, accepted_tags = [], {}
    events = Counter()
    for r in data:
        for event in ("mac_accept", "mac_result_accept", "pp_accept", "pre_accept", "silu_accept",
                      "post_accept", "post_complete", "commit_accept"):
            events[event] += r[event]
        for accept, valid, ready in (("mac_accept", "mac_valid", "mac_ready"),
                                     ("mac_result_accept", "mac_result_valid", "mac_result_ready"),
                                     ("pp_accept", "pp_valid", "pp_ready"),
                                     ("commit_accept", "commit_valid", "commit_ready")):
            assert r[accept] == (r[valid] and r[ready]), (accept, r)
        if r["mac_accept"] and r["group"] == 0:
            assert not pending or "last" in pending[-1]
            pending.append({"first": r["cycle"]})
        if r["mac_accept"] and r["mac_last"]:
            assert pending and "last" not in pending[-1]
            pending[-1]["last"] = r["cycle"]
        if r["mac_result_accept"]:
            task = pending.popleft()
            last_to_pop.append(r["cycle"] - task["last"])
            first_to_pop.append(r["cycle"] - task["first"])
        if r["pp_accept"]:
            assert r["pp_mask"] in ((7,) if r["layer"] else (1, 2, 4))
            for lane in range(3):
                if r["pp_mask"] & (1 << lane):
                    key = (r["layer"], r["pp_position"], r["pp_channel"] + lane)
                    assert 0 <= key[1] < 16 and 0 <= key[2] < (24 if key[0] else 16)
                    assert key not in accepted_tags, key
                    accepted_tags[key] = r["cycle"]
        if r["commit_accept"]:
            tag = r["commit_tag"]
            assert 0 <= tag <= 65535 and tag & 63 == 0
            key = (tag >> 15, (tag >> 11) & 15, (tag >> 6) & 31)
            batch_to_commit.append(r["cycle"] - accepted_tags.pop(key))
        for key, limit in (("mac_reserved", 4), ("mac_queued", 4), ("ingress", 2), ("retire", 8), ("meta", 8)):
            assert 0 <= r[key] <= limit, (key, r)
    assert not pending and not accepted_tags
    assert len(firsts) == events["mac_result_accept"] == 128
    scalar_count = 384 if data[0]["layer"] else 256
    assert events["mac_accept"] == (256 if data[0]["layer"] else 384)
    assert events["pp_accept"] == (128 if data[0]["layer"] else 256)
    assert all(events[key] == scalar_count for key in
               ("pre_accept", "silu_accept", "post_accept", "post_complete", "commit_accept"))
    assert reasons["send_guard_wait"] == 0
    return {"cycles": len(data), "states": dict(states), "exclusive_scheduler_class": dict(reasons),
            "events": dict(events), "first_gap_histogram": histogram(b-a for a, b in zip(firsts, firsts[1:])),
            "event_gap_histograms": {key: histogram(b-a for a, b in zip(times, times[1:]))
                for key in ("pre_accept", "silu_accept", "post_accept", "post_complete", "commit_accept")
                for times in [[r["cycle"] for r in data if r[key]]]},
            "last_to_result_pop": histogram(last_to_pop), "first_to_result_pop": histogram(first_to_pop),
            "batch_accept_to_scalar_commit": histogram(batch_to_commit),
            "occupancy": {key: histogram(r[key] for r in data) for key in
                          ("mac_reserved", "mac_queued", "ingress", "retire", "meta")},
            "stage_activity_mask_histogram": dict(sorted(activity.items())),
            "stage_union_cycles": sum(value for key, value in activity.items() if key),
            "stage_overlap_cycles": sum(value for key, value in activity.items() if key.bit_count() >= 2),
            # This is an overlap opportunity, not a subtraction from endpoint cycles.
            "commit_backpressure_cycles": sum(r["commit_valid"] and not r["commit_ready"] for r in data),
            "serialized_state_mac_ready_cycles": sum(r["mac_ready"] and r["state"] in (3, 9) for r in data)}


def analyze(work):
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["all_passed"]
    output = {"simulation": str(work), "dut_changed": False, "sets": {}}
    for name in receipt["results"]:
        traces = rows(work / (name + "_trace.csv"))
        summary = rows(work / (name + ".csv"))
        windows = rows(work / (name + "_windows.csv"))
        assert len(summary) == len(windows) == 10
        cases = {}
        for old, window in zip(summary, windows):
            assert old["case"] == window["case"]
            data = [r for r in traces if r["case"] == old["case"]]
            assert [r["cycle"] for r in data] == list(range(1, old["endpoint"] + 1))
            assert all(len(r) == 42 for r in data)
            assert [r["layer"] for r in data] == sorted(r["layer"] for r in data)
            boundary = next(i for i, r in enumerate(data) if r["layer"] == 1)
            assert data[boundary-1]["state"] == 4 and data[boundary]["state"] == 1
            assert data[boundary-1]["dw_writes"] == data[boundary]["dw_writes"] == 256
            assert all(data[index][key] == 0 for index in (boundary-1, boundary)
                       for key in ("mac_reserved", "mac_queued", "ingress", "retire", "meta"))
            assert data[-1]["state"] == 6 and data[-1]["pw_writes"] == 384
            assert all(data[-1][key] == 0 for key in ("mac_reserved", "mac_queued", "ingress", "retire", "meta"))
            profiles = {label: layer_profile([r for r in data if r["layer"] == layer])
                        for layer, label in enumerate(("dw", "pw"))}
            assert profiles["dw"]["cycles"] == old["dw_endpoint"]
            assert profiles["pw"]["cycles"] == old["pw_endpoint"]
            assert sum(p["cycles"] for p in profiles.values()) == window["core"] == old["endpoint"]
            assert window["table_accepted"] == 1024 and window["load_accepted"] == 1948
            assert window["export_accepted"] == 384 and window["export_span"] == old["export_cycles"]
            if old["case"] in (0, 1, 2, 6, 7, 9):
                assert (old["dw_endpoint"], old["pw_endpoint"], old["endpoint"]) == (2015, 592, 2607)
            cases[str(old["case"])] = {**profiles, "windows": window}
        output["sets"][name] = cases
    path = ROOT / "analysis.json"
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    sample = [r for r in rows(work / "fixed_original_trace.csv") if r["case"] == 0 and r["cycle"] <= 36]
    signals = [{"name": "clock", "wave": "p" + "." * (len(sample)-1)}]
    for name in ("mac_accept", "mac_last", "mac_result_accept", "pp_accept", "pre_accept", "silu_accept", "commit_accept"):
        signals.append({"name": name, "wave": "".join(str(r[name]) for r in sample)})
    (ROOT / "tests/dw_frozen_first_tasks.wave.json").write_text(json.dumps({
        "signal": signals, "head": {"text": "Frozen DW cycles 1 to 36 before NBA", "tick": 1},
        "config": {"hscale": 1}}, indent=2), encoding="utf-8")
    base = output["sets"]["fixed_original"]["0"]
    print(json.dumps({"cases_verified": 40, "baseline": base}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    work = Path(sys.argv[1]).resolve()
    work.relative_to(ROOT)
    analyze(work)
