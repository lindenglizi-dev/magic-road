"""Independently check the frozen minimal-chain trace, not physical sign-off."""
import csv
import hashlib
import json
from pathlib import Path


def signed(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def main():
    root = Path(__file__).resolve().parents[2] / "v7_onchip_chain_20261006"
    trace = list(csv.DictReader((root / "cycle_trace.csv").open(encoding="utf-8")))
    first_reset = next(i for i, row in enumerate(trace) if row["event"] == "reset_assert")
    numeric = trace[:first_reset]
    stages = []
    features = []
    used = [root / "cycle_trace.csv", root / "modelsim_chain_run_final.log"]
    for suffix in ("16", "13", "saturation"):
        stage_path = root / "inputs" / f"expected_stages_{suffix}.hex"
        feature_path = root / "inputs" / f"expected_features_{suffix}.hex"
        used.extend((stage_path, feature_path))
        stages.extend(int(line, 16) for line in stage_path.read_text().splitlines())
        features.extend(signed(int(line, 16), 8) for line in feature_path.read_text().splitlines())
    assert len(stages) == len(features) == 27
    # Packed stages are acc32/preprod64/pre16/SiLU16/postprod64/post16/feature8.
    for event, offset, bits in (("pre_round", 104, 16), ("silu_output", 88, 16),
                                ("post_round", 8, 16)):
        actual = [int(row["value"]) for row in numeric if row["event"] == event]
        expected = [signed((word >> offset) & ((1 << bits) - 1), bits) for word in stages]
        assert actual == expected, event
    actual_features = [int(row["value"]) for row in numeric if row["event"] == "cache_consume"]
    assert actual_features == features, "actual cache read responses"
    terminals = [int(row["value"]) for row in numeric if row["event"] == "mac_terminal"]
    assert terminals == [signed(word >> 184, 32) for word in stages[::3]]
    assert sum(row["event"] == "position_commit" for row in numeric) == 9
    log = (root / "modelsim_chain_run_final.log").read_text(encoding="utf-8")
    assert "TB_PASS_CHAIN mac=9 pre=27 silu=27 post=27 read=27 atomic_hidden=18 reset=6 directed=1 errors=0" in log
    assert "Errors: 0, Warnings: 2" in log
    receipt = {
        "status": "PASS_TRACE_ONLY", "checked_outputs": 27,
        "checked_stage_events": 81, "checked_mac_terminals": 9,
        "scope": "Independent CSV/golden check; not independent RTL rerun or TD/board sign-off",
        "vendor_model_warnings": 2,
        "sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in used},
    }
    output = Path(__file__).with_name("chain_trace_receipt.json")
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "outputs": 27, "stage_events": 81}))


if __name__ == "__main__":
    main()
