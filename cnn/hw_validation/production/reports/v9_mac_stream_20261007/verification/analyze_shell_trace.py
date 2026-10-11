"""Measure mutually exclusive shell core-cycle buckets from the v9 trace."""
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRACE = ROOT / "shell_cycle_trace.csv"
OLD_SUMMARY = ROOT.parent.parent / "v7_low_io_physical_20261006/shell/shell_cycle_summary.json"
BUCKET_BY_STATE = {
    0: "mac",
    1: "pre_requant",
    2: "pre_requant",
    3: "pre_requant",
    4: "silu",
    5: "silu",
    6: "post_requant",
    7: "post_requant",
    8: "commit",
    9: "commit",
    10: "commit",
    11: "fault",
}
BUCKETS = ("mac", "pre_requant", "silu", "post_requant", "commit", "fault")


def main():
    old = json.loads(OLD_SUMMARY.read_text(encoding="utf-8"))
    with TRACE.open(encoding="utf-8", newline="") as stream:
        rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(stream)]

    runs = []
    cancelled = []
    start = None
    for index, row in enumerate(rows):
        if not row["rstn"]:
            if start is not None:
                cancelled.append({
                    "start_cycle": rows[start]["cycle"],
                    "reset_cycle": row["cycle"],
                    "status": "cancelled_by_reset",
                })
            start = None
            continue
        if start is None and row["core_input"]:
            start = index
        completes = (
            start is not None
            and row["shell_state"] == 6
            and index + 1 < len(rows)
            and rows[index + 1]["shell_state"] == 7
        )
        if not completes:
            continue
        buckets = dict.fromkeys(BUCKETS, 0)
        for sample in rows[start:index]:
            buckets[BUCKET_BY_STATE[sample["chain_state"]]] += 1
        core_cycles = row["cycle"] - rows[start]["cycle"]
        assert sum(buckets.values()) == core_cycles
        old_run = old["runs"][len(runs)]
        runs.append({
            "name": old_run["name"],
            "start_cycle": rows[start]["cycle"],
            "end_cycle": row["cycle"],
            "core_cycles": core_cycles,
            "exclusive_stage_cycles": buckets,
            "old_core_cycles": old_run["endpoint_delta_cycles"],
            "old_exclusive_stage_cycles": old_run["exclusive_stage_cycles"],
            "delta_vs_old": core_cycles - old_run["endpoint_delta_cycles"],
        })
        start = None

    assert len(runs) == len(old["runs"]) == 11
    assert len(cancelled) == len(old["cancelled_runs"]) == 1
    result = {
        "status": "SHELL_TRACE_ACCOUNTING_PASS",
        "trace_rows": len(rows),
        "accounting": "Every half-open core interval cycle belongs to exactly one chain-state bucket.",
        "completed_runs": runs,
        "cancelled_runs": cancelled,
    }
    (ROOT / "shell_measured_cycles.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        "completed_runs": len(runs),
        "cancelled_runs": len(cancelled),
        "core_cycles": [run["core_cycles"] for run in runs],
        "mac_cycles": [run["exclusive_stage_cycles"]["mac"] for run in runs],
    }))


if __name__ == "__main__":
    main()
