"""Replay the existing two-clock mailbox tests with verified real QAT vectors."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

from run_qat_front3_rtl import BASE, OLD, check_hashes, digest, self_test

PRIOR = BASE / "qat_g10_front3_rtl_20261015_v2"
OUT = BASE / "qat_g10_front3_paxi_20261015_v1"
ORIGINAL_RUN = OLD / "integrated_simulation_attempt2"


def save(name: str, value: dict) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def command(name: str) -> list[str]:
    original = json.loads((OUT / "original_commands" / name).read_text())["argv"]
    return [arg.replace(str(OLD), str(OUT)).replace(str(OLD).replace("\\", "/"), OUT.as_posix())
            for arg in original]


def prepare() -> None:
    prior_binding = json.loads((PRIOR / "input_binding.json").read_text())
    hashes = {**prior_binding["original_sha256"], **prior_binding["staged_sha256"]}
    prior_receipt = json.loads((PRIOR / "verification_receipt.json").read_text())
    check_hashes({str(PRIOR / name): sha for name, sha in prior_receipt["sha256"].items()})
    if json.loads((PRIOR / "status.json").read_text())["status"] != "PASS_REAL_QAT_FRONT3_13_OF_13":
        raise ValueError("direct QAT regression prerequisite did not pass")
    sources = [*sorted((PRIOR / "reused").glob("*.v")), PRIOR / "rtl/road_stem_ddr_sequence.v",
               PRIOR / "rtl/once_constants.vh", OLD / "rtl/road_paxi_mailbox.v",
               OLD / "tests/tb_stem_ddr_mailbox.v"]
    templates = [ORIGINAL_RUN / name for name in ("vlog.command.json", "mode_0.command.json", "mode_1.command.json")]
    hashes.update({str(path): digest(path) for path in [*sources, *templates, Path(__file__),
                   Path(__file__).with_name("run_qat_front3_rtl.py"), PRIOR / "verification_receipt.json"]})
    # Bind vendor simulation models and executable identities before and after execution too.
    for path in templates:
        argv = json.loads(path.read_text())["argv"]
        for arg in argv:
            if arg.endswith((".v", ".exe")):
                hashes[arg] = digest(Path(arg))
    check_hashes(hashes)
    OUT.mkdir(exist_ok=False)
    for path in sources:
        source_root = PRIOR if path.is_relative_to(PRIOR) else OLD
        target = OUT / path.relative_to(source_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    shutil.copytree(PRIOR / "vectors", OUT / "vectors")
    for path in templates:
        target = OUT / "original_commands" / path.name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(path, target)
    shutil.copy2(__file__, OUT / "launcher_snapshot.py")
    shutil.copy2(PRIOR / "status.json", OUT / "prior_direct_status.json")
    (OUT / "run").mkdir()
    for path in (OUT / "vectors").glob("*.hex"):
        shutil.copy2(path, OUT / "run" / path.name)
    staged = {str(path): digest(path) for path in OUT.rglob("*") if path.is_file()}
    save("input_binding.json", {"original_sha256": hashes, "staged_sha256": staged,
                               "payload_sha256": prior_binding["payload_sha256"],
                               "checkpoint_sha256": prior_binding["checkpoint_sha256"],
                               "policy": "explicit existing local ModelSim backend, unchanged RTL/TB and PAXI protocol"})
    save("status.json", {"status": "PREPARED_NOT_SIMULATED", "formal_acceptance": False})
    print("PREPARED", OUT, flush=True)


def execute() -> None:
    binding = json.loads((OUT / "input_binding.json").read_text())
    check_hashes(binding["original_sha256"])
    check_hashes(binding["staged_sha256"])
    with (OUT / "execution_started.json").open("x", encoding="utf-8") as stream:
        json.dump({"started_at": datetime.now().astimezone().isoformat()}, stream)
    started = time.monotonic()
    commands = []

    def run(argv: list[str], name: str) -> str:
        commands.append({"argv": argv, "cwd": str(OUT / "run"), "executable_sha256": digest(Path(argv[0]))})
        save("commands.json", {"commands": commands})
        print("RUN", name, flush=True)
        result = subprocess.run(argv, cwd=OUT / "run", text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", timeout=180)
        (OUT / "run" / name).write_text(result.stdout, encoding="utf-8")
        commands[-1]["exit_code"] = result.returncode
        save("commands.json", {"commands": commands})
        if result.returncode:
            raise RuntimeError(f"command failed {result.returncode}: {name}")
        return result.stdout

    save("status.json", {"status": "MODELSIM_RUNNING", "formal_acceptance": False})
    try:
        vlog = command("vlog.command.json")
        run([str(Path(vlog[0]).with_name("vlib.exe")), "work"], "vlib.log")
        compile_log = run(vlog, "compile.log")
        summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_log)
        if not summaries or tuple(map(int, summaries[-1])) != (0, 0):
            raise ValueError("compile did not finish with 0 errors /0 warnings")
        modes = []
        for mode in (0, 1):
            output = run(command(f"mode_{mode}.command.json"), f"mode_{mode}.log")
            match = re.search(rf"STEM_DDR_MAILBOX_PASS mode={mode} cycles=(\d+) W=256 R=289 PW=1536", output)
            bins = re.findall(rf"INTEGRATED_BIN mode={mode} bin=(\d+) cycles=(\d+)", output)
            if not match or [int(i) for i, _ in bins] != list(range(10)) or sum(int(n) for _, n in bins) != int(match[1]):
                raise ValueError(f"mode {mode} PASS or exclusive-cycle coverage missing")
            if re.search(r"\*\* (?:Fatal|Error):", output):
                raise ValueError(f"mode {mode} simulator reported an error")
            modes.append({"mode": mode, "cycles": int(match[1]), "writes": 256, "reads": 289,
                          "pw_bytes": 1536, "exclusive_cycle_bins": [int(n) for _, n in bins]})
        check_hashes(binding["original_sha256"])
        check_hashes(binding["staged_sha256"])
        save("status.json", {"status": "PASS_REAL_QAT_FRONT3_PAXI_2_OF_2", "as_of": datetime.now().astimezone().isoformat(),
                             "seconds": time.monotonic()-started, "modes": modes,
                             "input_and_source_hashes_unchanged": True, "payload_sha256": binding["payload_sha256"],
                             "checkpoint_sha256": binding["checkpoint_sha256"], "compile_errors": 0, "compile_warnings": 0,
                             "clock_mhz": [100, 133.33333333333334], "ddr_clock_phase_ns": 1.7,
                             "scope": "unchanged synthetic RGB, real QAT first3 window, actual mailbox with controlled PAXI endpoint",
                             "training_updates": 0, "RTL_changed": False, "full_network_RTL_compared": False,
                             "real_DDR_or_physical_or_board_run": False, "formal_acceptance": False})
        print("PASS_REAL_QAT_FRONT3_PAXI_2_OF_2", modes, flush=True)
    except BaseException as error:
        save("status.json", {"status": "FAILED_NO_RETRY", "error": repr(error),
                             "seconds": time.monotonic()-started, "formal_acceptance": False})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("self-test", "prepare", "execute"))
    action = parser.parse_args().action
    {"self-test": self_test, "prepare": prepare, "execute": execute}[action]()
