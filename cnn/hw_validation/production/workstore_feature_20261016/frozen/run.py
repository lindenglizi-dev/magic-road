"""物理工作仓的隔离封存与真实厂商模型回归；不触碰旧交付。"""
import argparse
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / "feature_blocks_shared_20261015"
SELECTED = PRIOR / "sppf_candidate/frozen_attempt2"
spec = importlib.util.spec_from_file_location("readonly_sppf_helpers", PRIOR / "run_sppf.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
digest, read, save, verify = prior.digest, prior.read, prior.save, prior.verify
PROJECT, MODEL, VENDOR, SKILL, CORES = prior.PROJECT, prior.MODEL, prior.VENDOR, prior.SKILL, prior.CORES


def check_old():
    seal = read(PRIOR / "sppf_candidate/delivery_manifest.json")
    verify(seal["artifacts_sha256"])
    binding = read(SELECTED / "input_binding.json")
    for item in [binding, binding["prior_binding"], *binding["prior_binding"]["old_bindings"]]:
        verify(item["original_sha256"])
        verify(item["staged_sha256"])
    assert binding["payload_sha256"] == prior.PAYLOAD
    return binding


def prepare(name, storage_only):
    assert re.fullmatch(r"(?:storage_)?frozen(?:_attempt[1-9][0-9]*)?", name)
    target = ROOT/name
    if target.exists():
        raise ValueError("existing candidate must be retained")
    old = check_old()
    folders = ("rtl", "tests", "reference", "spec")
    if storage_only:
        files = [ROOT/"rtl/road_feature_workstore.v", ROOT/"tests/tb_feature_workstore.v"]
        files += list((ROOT/"reference").glob("workstore*"))
        files += list((ROOT/"rtl").glob("road_feature_workstore*json"))
        files += list((ROOT/"rtl").glob("road_feature_workstore*md"))
        files += list((ROOT/"tests").glob("tb_feature_workstore*md"))
    else:
        files = [path for folder in folders for path in (ROOT/folder).rglob("*")
                 if path.is_file() and "__pycache__" not in path.parts]
        assert (ROOT/"rtl/road_feature_blocks_client.v") in files
    files += [ROOT/"workstore_interface.txt", Path(__file__)]
    if (ROOT/"tb_contract.json").is_file():
        files.append(ROOT/"tb_contract.json")
    assert all(path.is_file() for path in files)
    original = {str(path): digest(path) for path in files
                if not storage_only or path != ROOT/"workstore_interface.txt"}
    for tool in ("vlib", "vlog", "vsim"):
        path = MODEL/(tool+".exe")
        original[str(path)] = digest(path)
    for module in ("ph1p_logic_eram", "ph1p_phy_gsr"):
        path = VENDOR/(module+".v")
        original[str(path)] = digest(path)
    target.mkdir()
    for path in files:
        destination = target/path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    if not storage_only:
        shutil.copytree(SELECTED/"reference", target/"vectors")
        shutil.copytree(SELECTED/"reused", target/"reused")
        for folder in ("vectors", "reused"):
            for path in (SELECTED/("reference" if folder == "vectors" else folder)).rglob("*"):
                if path.is_file():
                    original[str(path)] = digest(path)
    staged = {str(path): digest(path) for path in target.rglob("*") if path.is_file()}
    verify(original)
    verify(staged)
    save(target/"input_binding.json", dict(original_sha256=original, staged_sha256=staged,
         prior_binding=old, storage_only=storage_only, payload_sha256=prior.PAYLOAD,
         actual_DDR=False, synthesis=False, production_delivery_ready=False))
    print("FROZEN_NATIVE_WORKSTORE", name, len(staged), flush=True)


def check_binding(target):
    binding = read(target/"input_binding.json")
    verify(binding["original_sha256"])
    verify(binding["staged_sha256"])
    assert check_old() == binding["prior_binding"]
    return binding


def command(argv, folder, filename, records, timeout=2400, cwd=None, env=None):
    result = subprocess.run(list(map(str, argv)), cwd=cwd or folder, env=env,
         capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    output = result.stdout+result.stderr
    path = folder/filename
    path.write_text(output, encoding="utf-8")
    code = result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):", output)))
    records.append(dict(argv=list(map(str, argv)), cwd=str(cwd or folder),
         native_returncode=result.returncode, validated_returncode=code, log_sha256=digest(path)))
    save(folder/"commands.json", records)
    return output, code


def execute(name, mode, case):
    target = ROOT/name
    binding = check_binding(target)
    assert not binding["storage_only"] or mode == "workstore"
    folder = target/(mode+"_case"+str(case))
    folder.mkdir(exist_ok=False)
    records, started = [], time.monotonic()
    tops = dict(workstore="tb_feature_workstore", csp="tb_feature_blocks_client", sppf="tb_feature_sppf_client")
    markers = dict(workstore="FEATURE_WORKSTORE_PASS", csp="FEATURE_BLOCKS_PASS", sppf="FEATURE_SPPF_PASS")
    negative = dict(workstore="NEGATIVE_WORKSTORE", csp="NEGATIVE_ACC", sppf="NEGATIVE_POOL")
    try:
        _, code = command([MODEL/"vlib.exe", "work"], folder, "vlib.log", records)
        assert code == 0, "vlib failed"
        sources = [VENDOR/"ph1p_logic_eram.v", VENDOR/"ph1p_phy_gsr.v"]
        if mode != "workstore":
            sources += [target/"reused"/(module+".v") for module in CORES]
            sources.append(target/"rtl/road_feature_blocks_client.v")
        sources += [target/"rtl/road_feature_workstore.v", target/"tests"/(tops[mode]+".v")]
        output, code = command([MODEL/"vlog.exe", "-work", "work", *sources], folder, "compile.log", records)
        summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", output)
        assert code == 0 and summaries and all(row == ("0", "0") for row in summaries), "compile failed or warned"
        arguments = [f"+CASE={0 if case == 99 else case}", f"+VECTORS_ROOT={(target/'vectors').as_posix()}"]
        if case == 99:
            arguments.append("+"+negative[mode]+"=1")
        print("RUN_NATIVE_WORKSTORE", name, mode, case, flush=True)
        output, code = command([MODEL/"vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", tops[mode],
                 *arguments, "-do", "run -all; quit -code 0"], folder, "simulation.log", records)
        prior.check_vector_loading(output)
        if case == 99:
            assert code != 0 and negative[mode]+" injected" in output and markers[mode] not in output
            receipt = dict(actual_checker_negative=True, forbidden_success_marker_absent=True)
        else:
            assert code == 0, "real simulation failure retained"
            prefix = markers[mode].removesuffix("_PASS")
            found = re.findall(prefix+r"_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)
            assert len(found) == 1, "unique complete receipt absent"
            fields = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", found[0])}
            assert fields.get("case") == case
            receipt = dict(marker=found[0], fields=fields)
            if mode != "workstore":
                ledger = "FEAT_BLOCK" if mode == "csp" else "FEAT_SPPF"
                receipt.update(stage_ledger=re.findall(ledger+r"_STAGE [^\r\n]*", output),
                      state_ledger=re.findall(ledger+r"_STATE [^\r\n]*", output),
                      measured_runs=re.findall(ledger+r"_RUN [^\r\n]*", output))
        check_binding(target)
        save(folder/"receipt.json", receipt)
        save(folder/"status.json", dict(status="PASS_REAL_CHECKER_NEGATIVE" if case == 99 else "PASS_FUNCTION_CASE",
             mode=mode, case=case, seconds=time.monotonic()-started, actual_DDR=False,
             physical_resource_mapping=False, production_delivery_ready=False))
        print("PASS_NATIVE_WORKSTORE", mode, case, round(time.monotonic()-started, 2), flush=True)
    except BaseException as error:
        save(folder/"status.json", dict(status="FAILED_PRESERVED", mode=mode, case=case, error=repr(error)))
        raise


def preflight():
    folder = ROOT/"dependency"
    folder.mkdir(exist_ok=False)
    temporary = ROOT/"runtime_tmp"
    temporary.mkdir(exist_ok=True)
    environment = dict(os.environ, TMP=str(temporary), TEMP=str(temporary))
    commands = dict(dependencies=["scripts.python.toolchain.manage_skill_dependencies", "check", "--settings", "config/defaults.json"],
        renderer=["scripts.python.toolchain.wavedrom_runtime", "--settings", "config/defaults.json", "check"],
        readiness=["scripts.python.toolchain.preflight_verilog_toolchain", "--settings", "config/defaults.json", "--readiness", "execute"])
    for name, arguments in commands.items():
        records = []
        output, code = command([sys.executable, "-B", "-m", *arguments], folder, name+".log", records,
                               timeout=60, cwd=SKILL, env=environment)
        save(folder/(name+"_command.json"), records[0])
        print("PREFLIGHT", name, code, flush=True)


def gate(name):
    target = ROOT/name
    folder = target/"static_gate"
    folder.mkdir(exist_ok=False)
    records = []
    output, code = command([sys.executable, "-B", "-m", "scripts.python.validation.generated_deliverable_gate",
        str(target/"rtl"), "--json", str(folder/"gate.json"), "--markdown", str(folder/"gate.md")],
        folder, "gate.log", records, timeout=240, cwd=SKILL)
    assert records[-1]["native_returncode"] in (0, 1) and (folder/"gate.json").is_file()
    report = read(folder/"gate.json")
    print("STRICT_GATE", report["delivery_ready"], report["errors"], report["strict_warnings"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "execute", "gate", "preflight", "self-check"))
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--storage-only", action="store_true")
    parser.add_argument("--mode", choices=("workstore", "csp", "sppf"), default="workstore")
    parser.add_argument("--case", type=int, default=0)
    args = parser.parse_args()
    if args.action == "prepare":
        prepare(args.name, args.storage_only)
    elif args.action == "execute":
        execute(args.name, args.mode, args.case)
    elif args.action == "gate":
        gate(args.name)
    elif args.action == "preflight":
        preflight()
    else:
        prior.check_vector_loading("WORKSTORE_PASS case=0")
        try:
            prior.check_vector_loading("Failed to open readmem file pool. 0.hex")
        except ValueError:
            print("PASS_VECTOR_LOADING_NEGATIVE")
        else:
            raise AssertionError("missing vector escaped")
