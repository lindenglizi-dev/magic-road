"""Check independently rerun MAC trace against the frozen signed33 vectors."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERIFY = ROOT.parent / "verification"


def check():
    vectors = json.loads((VERIFY / "signed33_vectors.json").read_text())["vectors"]
    rows = list(csv.DictReader((ROOT / "independent_trace.csv").open(newline="")))
    accepts = [row for row in rows if row["event"] == "accept"]
    terminals = [row for row in rows if row["event"] == "result_valid"]
    assert len(accepts) == len(vectors) == 84
    intervals = []
    by_key = {}
    for index, (row, vector) in enumerate(zip(accepts, vectors)):
        key = (int(row["case"]), int(row["beat"]))
        assert key == (vector["case_id"], vector["beat_id"])
        by_key[key] = (row, vector)
        if index:
            interval = int(row["cycle"]) - int(accepts[index - 1]["cycle"])
            previous = vectors[index - 1]
            expected = 13 + previous["stall_cycles"] if previous["emit"] else 11
            assert interval == expected, (key, interval, expected)
            intervals.append(interval)
    assert len(terminals) == sum(vector["emit"] for vector in vectors) == 12
    faults = 0
    for row in terminals:
        accepted, vector = by_key[(int(row["case"]), int(row["beat"]))]
        assert vector["emit"] and int(row["cycle"]) - int(accepted["cycle"]) == 9
        assert int(row["fault"]) == vector["fault"]
        expected = sum((value & 0xffffffff) << (32 * lane)
                       for lane, value in enumerate(vector["expected_data"]))
        assert int(row["data"], 16) == expected
        faults += int(row["fault"])
    assert faults == 8
    assert sum(row["event"] == "reset_assert" for row in rows) == 10
    assert sum(row["event"] == "ready_high_result" for row in rows) == 1
    paths = [ROOT.parent / "candidate" / "road_mac_probe.v",
             VERIFY / "tb_road_mac_signed_accumulator.v", VERIFY / "signed33_vectors.json",
             VERIFY / "signed33_vectors.txt", ROOT / "independent.vvp",
             ROOT / "independent_trace.csv", Path(__file__).resolve()]
    report = {"status": "INDEPENDENT_TRACE_PASS", "vectors": 84, "terminals": 12,
              "atomic_faults": faults, "reset_points": 10, "ready_high_cases": 1,
              "terminal_latency_cycles": 9, "nonlast_accept_interval_cycles": 11,
              "terminal_stall3_next_accept_interval_cycles": 16,
              "terminal_stall12_next_accept_interval_cycles": 25,
              "observed_intervals": sorted(set(intervals)),
              "sha256": {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
              "scope": "MAC only; no integrated-chain throughput or TD timing evidence"}
    (ROOT / "independent_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    check()
