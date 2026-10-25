"""固定发令器真实ModelSim检查；受控完成端点不是实际计算。"""

from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOOLS = Path("D:/modeltech64_2020.4/win64")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = HERE / "reports" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    snapshot = report / "inputs"
    snapshot.mkdir(parents=True)
    sources = [ROOT / "rtl/road_standard_layer_sequence.v", HERE / "tb_standard_layer_sequence.v",
               ROOT / "jobs22.hex", ROOT / "reference.py", ROOT / "requirements.json", ROOT / "codegen_plan.txt", Path(__file__)]
    original = {}
    for source in sources:
        original[str(source)] = sha(source)
        shutil.copy2(source, snapshot / source.name)
    closure = {p.name: sha(p) for p in snapshot.iterdir() if p.is_file()}
    tools = {name: {"path": str(TOOLS / (name + ".exe")), "sha256": sha(TOOLS / (name + ".exe"))} for name in ("vlib", "vlog", "vsim")}
    receipt = {"status": "STARTED", "snapshot": str(snapshot), "original_sha256": original,
               "snapshot_sha256": closure, "tools": tools, "commands": [], "boundary": "controlled tile retirement only; no convolution, DDR, physical mapping or whole-network execution"}
    summary = report / "summary.json"
    for name, args in (("vlib", ["work"]), ("vlog", ["-work", "work", "road_standard_layer_sequence.v", "tb_standard_layer_sequence.v"]),
                       ("vsim", ["-c", "-lib", "work", "tb_standard_layer_sequence", "+JOBS=jobs22.hex", "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"])):
        command = [tools[name]["path"], *args]
        result = subprocess.run(command, cwd=snapshot, capture_output=True, text=True, timeout=90)
        output = result.stdout + result.stderr
        log = report / (name + ".log")
        log.write_text(output, encoding="utf-8")
        receipt["commands"].append({"argv": command, "cwd": str(snapshot), "returncode": result.returncode, "log_sha256": sha(log)})
        if result.returncode != 0 or "** Error:" in output or "** Fatal:" in output:
            receipt["status"] = "FAILED"
            break
        if name == "vsim":
            receipt["status"] = "PASS" if "SEQUENCE_PASS " in output else "FAILED_NO_MARKER"
            receipt["metrics"] = [line for line in output.splitlines() if "SEQUENCE_" in line]
    receipt["snapshot_unchanged"] = all(sha(snapshot / name) == value for name, value in closure.items())
    receipt["current_sources_unchanged"] = all(sha(Path(name)) == value for name, value in original.items())
    summary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(summary)
    print(receipt["status"])
    if receipt["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
