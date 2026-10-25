"""窄口资源诊断：只读复用冻结核，封存后运行独立仿真。"""
import argparse
import importlib.util
import os
from pathlib import Path
import re
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "workstore_feature_20261016"
module_spec = importlib.util.spec_from_file_location("native_workstore_helpers", OLD / "run.py")
old = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(old)
digest, read, save, verify = old.digest, old.read, old.save, old.verify


def check_old():
    old.check_binding(OLD / "frozen")
    old.check_binding(OLD / "storage_frozen")
    verify(read(OLD / "latest_delivery_manifest.json")["artifacts_sha256"])


def prepare(name):
    if not re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?", name):
        raise ValueError("unsafe candidate name")
    check_old()
    target = ROOT / name
    target.mkdir(exist_ok=False)
    files = [ROOT / filename for filename in ("run.py", "interface_contract.json", "reference.py",
             "synthesize.py", "build.tcl", "diagnostic_clock.sdc")]
    files += [path for folder in ("rtl", "tests", "spec")
              for path in (ROOT / folder).rglob("*")
              if path.is_file() and "__pycache__" not in path.parts]
    assert any(path.suffix == ".v" and path.parent.name == "rtl" for path in files)
    assert any(path.suffix == ".v" and path.parent.name == "tests" for path in files)
    original = {str(path): digest(path) for path in files}
    for path in files:
        destination = target / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    for folder in ("rtl", "reused", "vectors"):
        for path in (OLD / "frozen" / folder).rglob("*"):
            if path.is_file():
                destination = target / ("core" if folder == "rtl" else folder) / path.relative_to(OLD / "frozen" / folder)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
                original[str(path)] = digest(path)
    plan = ROOT.parent.parent / "plans/resource_budget_20261015"
    for path in (plan / "第八批任务_R256零训练与资源诊断_20261016.txt",
                 plan / "r256_candidate_contract_20261016.json",
                 OLD / "latest_delivery_manifest.json"):
        original[str(path)] = digest(path)
    for path in [*(old.MODEL / (tool + ".exe") for tool in ("vlib", "vlog", "vsim")),
                 *(old.VENDOR / (tool + ".v") for tool in ("ph1p_logic_eram", "ph1p_phy_gsr"))]:
        original[str(path)] = digest(path)
    staged = {str(path): digest(path) for path in target.rglob("*") if path.is_file()}
    verify(original)
    verify(staged)
    save(target / "input_binding.json", dict(original_sha256=original, staged_sha256=staged,
         old_binding_sha256=digest(OLD / "frozen/input_binding.json"),
         actual_model_ROM=False, full_graph=False, actual_DDR=False))
    print("FROZEN_NARROW_FEATURE", name, len(staged), flush=True)


def check(name):
    check_old()
    target = ROOT / name
    binding = read(target / "input_binding.json")
    verify(binding["original_sha256"])
    verify(binding["staged_sha256"])
    assert binding["old_binding_sha256"] == digest(OLD / "frozen/input_binding.json")
    return target


def preflight():
    folder = ROOT / "preflight"
    folder.mkdir(exist_ok=False)
    temporary = ROOT / "runtime_tmp"
    temporary.mkdir(exist_ok=True)
    environment = dict(os.environ, TMP=str(temporary), TEMP=str(temporary))
    commands = dict(dependencies=["scripts.python.toolchain.manage_skill_dependencies", "check", "--settings", "config/defaults.json"],
        renderer=["scripts.python.toolchain.wavedrom_runtime", "--settings", "config/defaults.json", "check"],
        readiness=["scripts.python.toolchain.preflight_verilog_toolchain", "--settings", "config/defaults.json", "--readiness", "execute"])
    for name, arguments in commands.items():
        records = []
        _, code = old.command([sys.executable, "-B", "-m", *arguments], folder, name + ".log", records,
                             timeout=60, cwd=old.SKILL, env=environment)
        save(folder / (name + "_command.json"), records[-1])
        print("PREFLIGHT", name, code, flush=True)


def execute(name, mode, case):
    target = check(name)
    folder = target / (mode + "_case" + str(case))
    folder.mkdir(exist_ok=False)
    records, started = [], time.monotonic()
    top = "tb_narrow_feature_" + mode
    try:
        _, code = old.command([old.MODEL / "vlib.exe", "work"], folder, "vlib.log", records)
        assert code == 0
        sources = [old.VENDOR / (module + ".v") for module in ("ph1p_logic_eram", "ph1p_phy_gsr")]
        sources += list((target / "reused").glob("*.v")) + list((target / "core").glob("*.v"))
        sources += list((target / "rtl").glob("*.v")) + list((target / "tests").glob("*.v"))
        output, code = old.command([old.MODEL / "vlog.exe", "-work", "work", "+incdir+" + str(target / "tests"), *sources], folder, "compile.log", records)
        counts = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", output)
        assert code == 0 and counts and all(row == ("0", "0") for row in counts), "compile failed or warned"
        arguments = [f"+CASE={0 if case == 99 else case}", f"+VECTORS_ROOT={(target / 'vectors').as_posix()}"]
        if case == 99:
            arguments.append("+NEGATIVE_ACC=1" if mode == "csp" else "+NEGATIVE_POOL=1")
        output, code = old.command([old.MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", top,
            *arguments, "-do", "run -all; quit -code 0"], folder, "simulation.log", records, timeout=7200)
        old.prior.check_vector_loading(output)
        negative = "NEGATIVE_ACC" if mode == "csp" else "NEGATIVE_POOL"
        marker = {"csp": "FEATURE_BLOCKS", "sppf": "FEATURE_SPPF", "protocol": "NARROW_PROTOCOL"}[mode]
        if case == 99:
            assert code != 0 and negative + " injected" in output and marker + "_PASS" not in output
        else:
            assert code == 0 and len(re.findall(marker + r"_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)) == 1
        check(name)
        save(folder / "receipt.json", dict(actual_negative=case == 99,
             markers=re.findall(r"(?:FEATURE_|FEAT_|NARROW_)[^\r\n]*", output),
             seconds=time.monotonic() - started))
        save(folder / "status.json", dict(status="PASS_REAL_CHECKER_NEGATIVE" if case == 99 else "PASS_FUNCTION_CASE",
             case=case, mode=mode, physical_mapping=False, actual_DDR=False, production_delivery_ready=False))
        print("PASS_NARROW_FEATURE", mode, case, flush=True)
    except BaseException as error:
        save(folder / "status.json", dict(status="FAILED_PRESERVED", error=repr(error), mode=mode, case=case))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "check", "execute", "preflight"))
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--mode", choices=("csp", "sppf", "protocol"), default="csp")
    parser.add_argument("--case", type=int, default=0)
    args = parser.parse_args()
    if args.action == "preflight":
        preflight()
    elif args.action == "prepare":
        prepare(args.name)
    elif args.action == "check":
        check(args.name)
        print("PASS_INPUT_BINDING")
    else:
        execute(args.name, args.mode, args.case)
