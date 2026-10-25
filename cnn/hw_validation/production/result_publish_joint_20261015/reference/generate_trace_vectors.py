"""Pack the frozen Python trace into one deterministic full-port RTL vector file."""

import hashlib
import json
import sys
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent
    parent = directory.parent
    sys.path.insert(0, str(parent))
    from reference import DEFAULTS

    trace_path = directory / "cycle_trace.json"
    spec_path = parent / "publisher_spec.json"
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    ports = json.loads(spec_path.read_text(encoding="utf-8"))["modules"][0]["interfaces"]["ports"]
    inputs = [port for port in ports if port["direction"] == "input" and port["name"] != "i_clk"]
    outputs = [port for port in ports if port["direction"] == "output"]
    states = {"IDLE": 0, "RUN": 1, "META": 2, "WAIT_ACK": 3, "ABORT": 4}
    width = 1 + sum(port["width"] for port in inputs + outputs) + 3 + 7
    lines = []
    previous_case = None
    cases = []
    for index, cycle in enumerate(trace):
        new_case = cycle["case"] != previous_case
        if new_case:
            assert cycle["state_before"] == "IDLE"
            cases.append({"case": cycle["case"], "first_cycle": index})
        values = DEFAULTS | cycle["inputs"]
        packed = int(new_case)
        for port in inputs + outputs:
            value = values[port["name"]] if port in inputs else cycle["outputs"][port["name"]]
            assert 0 <= value < (1 << port["width"])
            packed = (packed << port["width"]) | value
        packed = (packed << 3) | states[cycle["state_after"]]
        packed = (packed << 7) | cycle["accepted_after"]
        lines.append(f"{packed:0{(width + 3) // 4}x}")
        previous_case = cycle["case"]
    assert len(lines) == 500 and len(cases) == 33
    vector_path = directory / "publisher_trace.hex"
    vector_path.write_text("\n".join(lines) + "\n", encoding="ascii")
    receipt = {
        "status": "PASS", "cycles": len(lines), "case_count": len(cases),
        "vector_bits": width, "input_order": inputs, "output_order": outputs,
        "layout": "new_case, ordered inputs except i_clk, ordered outputs, state_after[2:0], accepted_after[6:0]",
        "cases": cases,
        "sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in (trace_path, spec_path, parent / "reference.py", vector_path, Path(__file__))},
    }
    (directory / "trace_vector_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in ("status", "cycles", "case_count", "vector_bits", "sha256")}))


if __name__ == "__main__":
    main()
