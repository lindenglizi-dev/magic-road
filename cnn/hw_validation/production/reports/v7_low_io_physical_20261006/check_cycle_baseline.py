"""Independent half-open-window audit of the unchanged 482-cycle baseline."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    path = root / "review" / "review_cycle_trace.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    start, end = int(rows[0]["cycle"]), int(rows[-1]["cycle"])
    assert end - start == 482 and len(rows) == 483
    assert [int(row["cycle"]) for row in rows] == list(range(start, end + 1))
    counts = Counter(int(row["state"]) for row in rows[:-1])
    expected = {0: 134, 1: 12, 2: 12, 3: 108, 4: 12, 5: 72,
                6: 12, 7: 108, 8: 4, 9: 4, 10: 4}
    assert dict(counts) == expected
    assert sum(int(row["cache_response"]) for row in rows) == 12
    result = {"status": "PASS_CSV_AUDIT_ONLY", "start": start, "end": end,
              "interval": "[start,end)", "total_cycles": 482,
              "state_occupancy": dict(counts), "cache_responses": 12,
              "trace_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "scope": "Independent numerical audit of reviewer simulation; no separate main RTL run"}
    (root / "cycle_baseline_audit.json").write_text(json.dumps(result, indent=2) + "\n",
                                                   encoding="utf-8")
    print(json.dumps({"status": result["status"], "cycles": 482}))


if __name__ == "__main__":
    main()
