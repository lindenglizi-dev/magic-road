"""Derive narrow-load, core, and export endpoint deltas from the final trace."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
TRACE = HERE / "shell_cycle_trace.csv"
OUTPUT = HERE / "shell_phase_cycles.csv"
RUN_NAMES = [
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
]


def main() -> None:
    """Write reproducible endpoint deltas without mixing narrow I/O into core time."""
    with TRACE.open(newline="", encoding="utf-8") as stream:
        rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(stream)]

    completed: list[dict[str, object]] = []
    cancelled: list[dict[str, object]] = []
    table_start: int | None = None
    run_command: int | None = None
    core_start: int | None = None
    export_start: int | None = None

    for index, row in enumerate(rows[:-1]):
        next_row = rows[index + 1]
        cycle = row["cycle"]

        if row["rstn"] == 0:
            if core_start is not None:
                cancelled.append(
                    {
                        "name": "cancelled_core_reset",
                        "preload_cycles": (run_command - table_start) if table_start is not None and run_command is not None else "",
                        "core_cycles": cycle - core_start,
                        "export_cycles": "",
                        "completion": "cancelled_by_reset",
                    }
                )
            if export_start is not None and completed:
                completed[-1]["export_cycles"] = ""
                completed[-1]["completion"] = "export_cancelled_by_reset"
            table_start = None
            run_command = None
            core_start = None
            export_start = None
            continue

        if row["shell_state"] == 0 and row["rx_transfer"] and next_row["shell_state"] == 1:
            table_start = cycle
        if row["shell_state"] == 0 and row["rx_transfer"] and next_row["shell_state"] == 5:
            run_command = cycle
        if row["core_input"] and core_start is None:
            core_start = cycle

        if row["shell_state"] == 6 and next_row["shell_state"] == 7 and core_start is not None:
            run_index = len(completed)
            completed.append(
                {
                    "name": RUN_NAMES[run_index],
                    "preload_cycles": (run_command - table_start) if table_start is not None and run_command is not None else "",
                    "core_cycles": cycle - core_start,
                    "export_cycles": "",
                    "completion": "core_complete_export_not_started",
                }
            )
            core_start = None

        if row["shell_state"] == 0 and row["rx_transfer"] and next_row["shell_state"] == 8:
            export_start = cycle
        if row["shell_state"] == 10 and row["tx_transfer"] and next_row["shell_state"] == 11:
            if export_start is None or not completed:
                raise AssertionError("completed export has no matching command or core run")
            completed[-1]["export_cycles"] = cycle - export_start
            completed[-1]["completion"] = "core_and_export_complete"
            export_start = None

    if len(completed) != len(RUN_NAMES):
        raise AssertionError(f"expected {len(RUN_NAMES)} completed runs, observed {len(completed)}")

    records = sorted(completed + cancelled, key=lambda item: RUN_NAMES.index(item["name"]) if item["name"] in RUN_NAMES else 8.5)
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["name", "preload_cycles", "core_cycles", "export_cycles", "completion"],
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"PHASE_CSV_PASS completed={len(completed)} cancelled={len(cancelled)}")


if __name__ == "__main__":
    main()
