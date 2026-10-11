"""Produce mutually exclusive core-stage occupancy from the shell cycle trace."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TRACE = HERE / "shell_cycle_trace.csv"
OUTPUT = HERE / "shell_cycle_summary.json"
RUN_NAMES = (
    "base16",
    "tail13",
    "saturation",
    "atomic_fault",
    "positive_recovery",
    "negative_recovery",
    "maximum_192_legal",
    "maximum_192_fault",
    "maximum_96_packets",
    "held_export_setup",
    "reset_recovery_run",
)


def stage_name(chain_state: int) -> str:
    """Map each frozen chain state into one non-overlapping accounting bucket."""
    if chain_state == 0:
        return "mac"
    if chain_state in (1, 2, 3):
        return "pre_requant"
    if chain_state in (4, 5):
        return "silu"
    if chain_state in (6, 7):
        return "post_requant"
    if chain_state in (8, 9, 10):
        return "commit"
    return "fault"


def main() -> None:
    """Find each RUN window from first parallel accept to shell completion."""
    with TRACE.open(newline="", encoding="utf-8") as stream:
        rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(stream)]
    runs = []
    cancelled_runs = []
    start_index = None
    for index, row in enumerate(rows):
        if row["rstn"] == 0:
            if start_index is not None:
                cancelled_runs.append({
                    "start_cycle": rows[start_index]["cycle"],
                    "reset_cycle": row["cycle"],
                    "status": "cancelled_by_reset",
                })
            start_index = None
            continue
        if start_index is None and row["core_input"]:
            start_index = index
        if start_index is None:
            continue
        next_shell = rows[index + 1]["shell_state"] if index + 1 < len(rows) else row["shell_state"]
        if row["shell_state"] == 6 and next_shell == 7:
            start = rows[start_index]["cycle"]
            end = row["cycle"]
            window = rows[start_index:index]
            buckets = {name: 0 for name in ("mac", "pre_requant", "silu", "post_requant", "commit", "fault")}
            for sample in window:
                buckets[stage_name(sample["chain_state"])] += 1
            runs.append({
                "name": RUN_NAMES[len(runs)] if len(runs) < len(RUN_NAMES) else f"run_{len(runs)}",
                "start_cycle": start,
                "end_cycle": end,
                "endpoint_delta_cycles": end - start,
                "sampled_half_open_cycles": sum(buckets.values()),
                "exclusive_stage_cycles": buckets,
            })
            start_index = None
    result = {
        "status": "TRACE_PASS" if runs else "TRACE_EMPTY",
        "accounting": "Each sampled core cycle belongs to exactly one frozen chain-state bucket; endpoint delta excludes the start endpoint and matches the shell counter contract.",
        "runs": runs,
        "cancelled_runs": cancelled_runs,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not runs or any(sum(run["exclusive_stage_cycles"].values()) != run["endpoint_delta_cycles"] for run in runs):
        raise SystemExit("trace accounting failed")
    print(f"TRACE_PASS runs={len(runs)} base_delta={runs[0]['endpoint_delta_cycles']}")


if __name__ == "__main__":
    main()
