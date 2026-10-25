"""Run the frozen thirteen-case ModelSim test with retained QAT-G10 vectors.

No RTL edits, training, physical implementation, or board operations. Each new
output directory can execute once; failed attempts are retained, not retried.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent / "reports"
DATA = BASE / "qat_g10_front3_data_20261014_v1"
OLD = BASE / "stem_ddr_down2_four_20261014"
OUT = BASE / "qat_g10_front3_rtl_20261015_v1"
RECEIPT_HASH = "e959ab3d8cfe5c3c2f4efbe539c6467a11b04982817742ca6d09a3e6a2175e73"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes(hashes: dict[str, str]) -> None:
    for name, expected in hashes.items():
        if digest(Path(name)) != expected.lower():
            raise ValueError(f"changed input: {name}")


def save(name: str, value: dict) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def prepare() -> None:
    check_hashes({str(DATA / "verification_receipt.json"): RECEIPT_HASH})
    receipt = json.loads((DATA / "verification_receipt.json").read_text())
    identity = json.loads((DATA / "identity.json").read_text())
    if not receipt["scalar_generator_and_independent_oracle_exact"] or receipt["stage_values"] != 26624:
        raise ValueError("data-only prerequisite not verified")
    hashes = {**identity["fixed_inputs"], **identity["sources"]}
    hashes.update({str(DATA / name): sha for name, sha in receipt["artifact_sha256"].items()})
    hashes.update({str(DATA / name): digest(DATA / name)
                   for name in ("verification_receipt.json", "identity.json", "reference.json", "status.json")})
    source_paths = [*sorted((OLD / "reused").glob("*.v")),
                    OLD / "rtl/road_stem_ddr_sequence.v", OLD / "rtl/once_constants.vh",
                    OLD / "tests/tb_stem_ddr_sequence.v", OLD / "sequence_verification/run_verify.py"]
    if len(source_paths) != 12:
        raise ValueError("unexpected frozen source closure")
    hashes.update({str(path): digest(path) for path in source_paths})
    hashes[str(Path(__file__).resolve())] = digest(Path(__file__))
    check_hashes(hashes)
    OUT.mkdir(exist_ok=False)
    for path in source_paths:
        target = OUT / path.relative_to(OLD)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for path in sorted((DATA / "vectors").iterdir()):
        target = OUT / "vectors" / path.name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(path, target)
    if digest(OUT / "rtl/once_constants.vh") != digest(OUT / "vectors/once_constants.vh"):
        raise ValueError("RTL program constants differ from QAT data")
    shutil.copy2(DATA / "reference.json", OUT / "reference.json")
    for name in ("verification_receipt.json", "identity.json", "status.json"):
        target = OUT / "data_evidence" / name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(DATA / name, target)
    shutil.copy2(__file__, OUT / "launcher_snapshot.py")
    staged = {str(path): digest(path) for path in OUT.rglob("*") if path.is_file()}
    save("input_binding.json", {"original_sha256": hashes, "staged_sha256": staged,
                               "payload_sha256": receipt["payload_sha256"],
                               "checkpoint_sha256": identity["checkpoint_sha256"],
                               "policy": "explicit reuse of existing project-local ModelSim flow; not remote gate"})
    save("status.json", {"status": "PREPARED_NOT_SIMULATED", "formal_acceptance": False})
    print("PREPARED", OUT, flush=True)


def execute() -> None:
    binding = json.loads((OUT / "input_binding.json").read_text())
    check_hashes(binding["original_sha256"])
    check_hashes(binding["staged_sha256"])
    # Exclusive marker prevents accidental reruns and preserves every failed attempt.
    with (OUT / "execution_started.json").open("x", encoding="utf-8") as stream:
        json.dump({"started_at": datetime.now().astimezone().isoformat()}, stream)
    spec = importlib.util.spec_from_file_location("frozen_front3_verify", OUT / "sequence_verification/run_verify.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    commands = []
    started = time.monotonic()

    def bounded_run(command: list[str], log: Path) -> str:
        commands.append({"argv": command, "cwd": str(runner.RUN),
                         "executable_sha256": digest(Path(command[0])), "timeout_seconds": 180})
        save("commands.json", {"commands": commands})
        print("RUN", log.name, flush=True)
        try:
            result = subprocess.run(command, cwd=runner.RUN, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", timeout=180)
        except subprocess.TimeoutExpired as error:
            output = error.stdout or b""
            log.write_bytes(output if isinstance(output, bytes) else output.encode("utf-8"))
            raise
        log.write_text(result.stdout, encoding="utf-8")
        commands[-1]["exit_code"] = result.returncode
        save("commands.json", {"commands": commands})
        if result.returncode:
            raise RuntimeError(f"external command failed: {result.returncode}; {log}")
        return result.stdout

    runner.run = bounded_run
    save("status.json", {"status": "MODELSIM_RUNNING", "formal_acceptance": False})
    try:
        runner.main()
        cases = [json.loads((runner.RECEIPTS / f"case{i:02d}.json").read_text()) for i in range(13)]
        for i, case in enumerate(cases):
            if case["case"] != i or (case["status"], case["error"]) != runner.EXPECTED[i][:2]:
                raise ValueError(f"bad terminal receipt {i}")
            if i not in (3, 4, 11):
                if (case["stem_acc_pre_silu_post"] != [4096]*4 or
                        case["dw_acc_pre_silu_post"] != [1024]*4 or
                        case["pw_acc_pre_silu_post"] != [1536]*4 or
                        (case["writes"], case["reads"], case["pw"]) != (256, 289, 1536)):
                    raise ValueError(f"incomplete arithmetic/transfer coverage {i}")
        check_hashes(binding["original_sha256"])
        check_hashes(binding["staged_sha256"])
        manifest = runner.RECEIPTS / "manifest.json"
        save("status.json", {"status": "PASS_REAL_QAT_FRONT3_13_OF_13", "as_of": datetime.now().astimezone().isoformat(),
                             "seconds": time.monotonic()-started, "cases": cases,
                             "original_and_staged_inputs_unchanged": True,
                             "payload_sha256": binding["payload_sha256"],
                             "checkpoint_sha256": binding["checkpoint_sha256"],
                             "legacy_manifest_sha256": digest(manifest),
                             "legacy_date_note": "frozen runner literal 2026-10-14 is not execution date; use this as_of",
                             "scope": "real QAT parameters, synthetic RGB, top-left 3-layer window, direct simulated DDR endpoint",
                             "RTL_changed": False, "training_updates": 0, "formal_acceptance": False,
                             "full_network_RTL_compared": False, "physical_or_board_run": False})
        print("PASS_REAL_QAT_FRONT3_13_OF_13", flush=True)
    except BaseException as error:
        save("status.json", {"status": "FAILED_NO_RETRY", "error": repr(error),
                             "seconds": time.monotonic()-started, "formal_acceptance": False})
        raise


def self_test() -> None:
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "input"
        path.write_bytes(b"original")
        hashes = {str(path): digest(path)}
        check_hashes(hashes)
        path.write_bytes(b"changed")
        try:
            check_hashes(hashes)
        except ValueError:
            pass
        else:
            raise AssertionError("tampered input accepted")
    print("PASS_HASH_POSITIVE_AND_TAMPER_NEGATIVE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("self-test", "prepare", "execute"))
    action = parser.parse_args().action
    # Existing runner owns tool-path arguments; defaults remain frozen.
    sys.argv = [sys.argv[0]]
    {"self-test": self_test, "prepare": prepare, "execute": execute}[action]()
