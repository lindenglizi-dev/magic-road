"""首残差固定任务顺序验证；不重复实现算术包装或DDR接口。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "qat_g10_csp_first_data_20261015_v2"
BASE = ROOT.parent / "qat_g10_csp_first_checks_20261015_v2"
DEEP = ROOT.parent / "pw_deep_slices_20261015"
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MSIM = Path("D:/modeltech64_2020.4/win64")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command(argv, cwd, name, allowed=(0,)):
    args = [str(a) for a in argv]
    result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding="utf-8", errors="replace")
    (cwd / (name + ".log")).write_text(result.stdout, encoding="utf-8")
    save(cwd / (name + ".command.json"), {"argv": args, "cwd": str(cwd),
         "executable_sha256": sha(args[0]), "exit_code": result.returncode})
    assert result.returncode in allowed, (name, result.stdout[-5000:])
    return result.stdout


def fresh(name):
    for attempt in range(1, 100):
        path = ROOT / (name if attempt == 1 else f"{name}_attempt{attempt}")
        if not path.exists():
            path.mkdir()
            return path
    raise RuntimeError("验证目录数量异常，禁止覆盖旧结果")


def entry(module):
    return f"import sys;sys.path.insert(0,{str(SKILL)!r});from {module} import main;raise SystemExit(main())"


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [p for p, digest in frozen.items() if sha(p) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed


def setup():
    assert not (ROOT / "frozen.json").exists(), "旧冻结清单不可覆盖"
    inputs = [DATA / name for name in ("contract.json", "mac_tasks.json", "identity.json", "verification_receipt.json")]
    inputs += [BASE / name for name in ("status.json", "case_receipts.json", "input_binding.json")]
    inputs += list(BASE.joinpath("rtl").glob("*.v")) + list(BASE.joinpath("reused").glob("*.v"))
    inputs += [DEEP / name for name in ("status.json", "artifact_manifest.json", "physical/pr.db")]
    save(ROOT / "frozen.json", {str(p): sha(p) for p in inputs})
    save(ROOT / "requirements.json", {"classification": "generate, validate", "baseline_commit": "709d98a4",
         "scope": "fixed first CSP residual tile descriptor sequencer only",
         "shape": {"DW": [4, 4, 12], "PW": [4, 4, 12]}, "tasks": 160, "groups": 320,
         "completion": "last valid result accepted by local storage adapter, NOT DDR visibility",
         "reset": "common asynchronous assertion; release supplied by existing top, reload 1024 table entries before start",
         "unchanged": ["arithmetic", "numerics", "MAC II", "core interface", "production", "external protocol"],
         "missing": ["halo address/data adapter", "DW intermediate cache", "PW operand adapter", "DDR commit", "physical timing"],
         "codegen_plan": ["bind frozen tasks", "Python independent enumeration", "render interface specification",
                          "fixed counter FSM RTL", "random stalls/reset/fault regression", "strict gates"],
         "public_gates": ["compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"]})
    check()


def dependency():
    work = fresh("dependency")
    paths = [MSIM / name for name in ("vlib.exe", "vlog.exe", "vsim.exe")]
    paths += [SKILL / "SKILL.md", Path("C:/Users/lenovo/.codex/skills/erie-remote-ssh/SKILL.md")]
    assert all(p.is_file() for p in paths)
    save(work / "paths.json", {str(p): sha(p) for p in paths})
    command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.toolchain.wavedrom_runtime"),
             "check"], work, "renderer")
    check()


def specs():
    work = fresh("specifications")
    ports = [("i_clk", "input", 1, "100MHz同域时钟"), ("i_rstn", "input", 1, "共同低有效异步取消，释放由现顶层保证"),
             ("i_start", "input", 1, "与start_ready握手启动，忙时不接受"),
             ("i_table_loaded", "input", 1, "来自冻结核，复位后重装1024项才允许启动"),
             ("i_group_ready", "input", 1, "操作数适配器和核共同接受本组"),
             ("i_task_done", "input", 1, "末路本地接收事件；一段高电平只消费一次，回低后重武装"),
             ("i_core_fault", "input", 1, "共同核故障，优先取消，恢复必须共同复位"),
             ("o_start_ready", "output", 1, "空闲且表已满且健康时允许启动"),
             ("o_group_valid", "output", 1, "当前组描述符有效，背压保持"),
             ("o_first", "output", 1, "两组中的首组"), ("o_last", "output", 1, "两组中的末组"),
             ("o_pw", "output", 1, "0 DW，1 PW"), ("o_y", "output", 2, "输出tile行0至3"),
             ("o_x", "output", 2, "DW三点起点0或3；PW单位置0至3"),
             ("o_channel", "output", 4, "DW同一通道0至11；PW输出起点0/3/6/9"),
             ("o_output_mask", "output", 3, "DW尾空间点001，其余111"),
             ("o_input_mask", "output", 8, "DW并集15/9，PW输入12，末组显式mask"),
             ("o_task_index", "output", 8, "固定任务序号0至159"),
             ("o_busy", "output", 1, "当前tile尚未完整结束"),
             ("o_done", "output", 1, "160个任务全部本地提交后单周期完成"),
             ("o_fault", "output", 1, "早到完成或核故障粘滞，禁止发布")]
    timing = {"id": "task", "scenario": "task", "title": "双组及完整结果提交后推进",
              "description": "两次group握手后等待task_done；背压不改变当前描述符。",
              "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
                  {"name": "group_valid", "wave": "01..0.1."}, {"name": "group_ready", "wave": "01.10..."},
                  {"name": "group", "wave": "x=..=x=.", "data": ["first", "last", "next first"]},
                  {"name": "task_done", "wave": "0....10."}]}}
    module = {"name": "road_csp_tile_schedule", "feature": "csp_schedule", "rtl_path": "road_csp_tile_schedule.v",
              "description": "固定左上首残差4×4×12任务计数器；无数据通路或通用微码",
              "interfaces": {"protocol": "discrete", "ports": [{"name": n, "direction": d, "width": w,
                  "role": "native", "description": desc, "clock_domain": "i_clk"} for n, d, w, desc in ports]},
              "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
              "reset": {"name": "i_rstn", "active": "low", "synchronous": False}, "parameters": [],
              "behavior": ["DW y/channel/x0或3，96任务；PW y/x/channel0或3或6或9，64任务。",
                           "每任务两组；仅valid与ready推进组，WAIT收到最后结果提交才推进任务。",
                           "未装满表拒绝启动；忙时start忽略；未消费的提前task_done故障；已消费高电平尾部不报错或重复推进；reset立即取消旧描述符。",
                           "最终done周期允许start_ready，同时握手可立即启动下一tile；fault在reset期间强制低。"],
              "constraints": ["仅本固定tile，不生成全局DDR地址，不证明写可见性，不改变冻结核II或接口。"],
              "corner_cases": ["DW末点、阶段切换、最终PW、任意反压、WAIT复位、早到done。"],
              "verification_cases": ["320组逐项同冻结mac_tasks；随机ready/完成延迟、长反压、逐状态复位、故障。"],
              "timing_diagrams": [timing]}
    for name, data, source in [("rtl", module, True), ("tb", {
        "name": "tb_csp_tile_schedule", "feature": "csp_schedule_test", "rtl_path": "tb_csp_tile_schedule.v",
        "description": "固定调度顺序及握手自检，不执行算术或DDR",
        "interfaces": {"protocol": "discrete", "ports": [{"name": "o_test_done", "direction": "output", "width": 1,
            "role": "test_complete", "description": "全部自检通过后置位", "clock_domain": "clk"}]},
        "clock": {"name": "clk", "edge": "posedge", "frequency_hz": 100000000, "internal": True},
        "reset": {"name": "rstn", "active": "low", "synchronous": False, "internal": True}, "parameters": [],
        "behavior": ["逐组与Python冻结描述符比较；故障和复位不得泄漏旧任务。"],
        "constraints": ["仅仿真，不替代算术回归或物理检查。"], "corner_cases": module["corner_cases"],
        "verification_cases": module["verification_cases"], "timing_diagrams": [timing]}, False)]:
        spec = work / (name + ".json")
        save(spec, {"modules": [data]})
        args = [sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.workflow.cli"),
                "write-spec", "--spec", spec, "--out-dir", work / name, "--no-state"]
        if source and (ROOT / "rtl/road_csp_tile_schedule.v").exists():
            args += ["--source", ROOT / "rtl/road_csp_tile_schedule.v"]
        command(args, ROOT, str(work.relative_to(ROOT) / name))
        bundle = work / name / "spec" / data["feature"]
        target = ROOT / ("rtl" if source else "tests")
        target.mkdir(exist_ok=True)
        shutil.copyfile(bundle / (data["name"] + "_spec.md"), target / (data["name"] + "_spec.md"))
        shutil.copytree(bundle / "waveforms", target / "waveforms", dirs_exist_ok=True)
    check()


def simulate():
    check()
    receipt = json.loads((ROOT / "reference/receipt.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS"
    assert sha(ROOT / "reference.py") == receipt["reference_sha256"]
    assert all(sha(p) == digest for p, digest in receipt["input_sha256"].items())
    assert all(sha(ROOT / "reference" / p) == digest for p, digest in receipt["output_sha256"].items())
    work = fresh("simulation")
    snapshots = work / "sources"
    snapshots.mkdir()
    sources = [ROOT / "rtl/road_csp_tile_schedule.v", ROOT / "tests/tb_csp_tile_schedule.v"]
    vectors = list(ROOT.joinpath("reference").glob("*.hex"))
    manifest = {str(p): sha(p) for p in [*sources, *vectors, ROOT / "reference.py", ROOT / "reference/receipt.json"]}
    save(work / "input_manifest.json", manifest)
    for p in sources:
        shutil.copyfile(p, snapshots / p.name)
    command([MSIM / "vlib.exe", "work"], work, "vlib")
    output = command([MSIM / "vlog.exe", "-work", "work", *sorted(snapshots.glob("*.v"))], work, "vlog")
    assert "Errors: 0, Warnings: 0" in output, output
    output = command([MSIM / "vsim.exe", "-c", "-lib", "work", "tb_csp_tile_schedule",
         "+VECTORS=" + (ROOT / "reference").as_posix(), "-do",
         "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "vsim")
    assert "TB_PASS_CSP_TILE_SCHEDULE" in output, output[-5000:]
    cases = re.findall(r"CSP_SCHEDULE_CASE=(\d+) groups=(\d+) tasks=(\d+) cycles=(\d+) send=(\d+) group_stall=(\d+) local_commit_wait=(\d+)", output)
    assert len(cases) == 7 and {int(c[0]) for c in cases} == set(range(7)), cases
    assert all(int(c[1]) == 320 and int(c[2]) == 160 and int(c[3]) == sum(map(int, c[4:])) for c in cases)
    assert all(sha(p) == digest for p, digest in manifest.items())
    save(work / "receipt.json", {"status": "PASS", "results": [line for line in output.splitlines() if "CSP_" in line],
         "cases": [{key: int(value) for key, value in zip(("case", "groups", "tasks", "cycles", "send", "group_stall", "local_commit_wait"), c)} for c in cases],
         "input_manifest_sha256": sha(work / "input_manifest.json"), "arithmetic_executed": False})
    check()


def gate():
    work = fresh("gate")
    for name, path in [("rtl", ROOT / "rtl"), ("tb", ROOT / "tests")]:
        command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.validation.generated_deliverable_gate"),
                 path, "--json", work / (name + ".json"), "--markdown", work / (name + ".md")],
                work, name, allowed=(0, 1))
    closure = work / "closure"
    for folder in ("rtl", "tests"):
        (closure / folder).mkdir(parents=True)
        for path in (ROOT / folder).glob("*.v"):
            shutil.copyfile(path, closure / folder / path.name)
    command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.validation.generated_deliverable_gate"),
             closure, "--include-testbench", "--json", work / "full.json", "--markdown", work / "full.md"],
            work, "full", allowed=(0, 1))
    check()


def finalize():
    check()
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1]
    runs = json.loads(simulation.read_text(encoding="utf-8"))["cases"]
    gate_dir = sorted(ROOT.glob("gate*/full.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    gates = {}
    for name in ("rtl", "tb", "full"):
        record = json.loads((gate_dir / (name + ".json")).read_text(encoding="utf-8"))
        gates[name] = {"errors": record["errors"], "strict_warnings": record["strict_warnings"],
                       "delivery_ready": record["delivery_ready"], "checks": record["checks"]}
    save(ROOT / "strict_summary.json", gates)
    save(ROOT / "status.json", {"status": "DESCRIPTOR_SCHEDULE_FUNCTIONAL_PASS_NOT_INTEGRATED",
         "reference": "reference/receipt.json", "simulation": str(simulation.relative_to(ROOT)),
         "tasks_per_run": 160, "groups_per_run": 320, "complete_runs": 7,
         "cycles": {"synthetic_one_cycle_completion": runs[0]["cycles"], "random_stalls_and_completion": runs[1]["cycles"],
                    "initial_512_backpressure_plus_random": runs[2]["cycles"]},
         "cycle_warning": "simulation completion is a test stimulus, NOT arithmetic latency, no speedup claim",
         "arithmetic_executed": False, "DDR_executed": False, "synthesis_run": False,
         "internal_numeric_interface_ii_changed": False, "production_delivery_ready": False,
         "remaining": ["operand/halo adapter", "DW intermediate store", "real last-output completion binding",
                       "wrapper strict closure", "actual integrated timing and cycles", "full graph and DDR"]})
    paths = [p for p in ROOT.rglob("*") if p.is_file() and "work" not in p.parts
             and p.name != "artifact_manifest.json" and "__pycache__" not in p.parts]
    save(ROOT / "artifact_manifest.json", {str(p.relative_to(ROOT)): sha(p) for p in paths})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "dependency", "specs", "simulate", "gate", "finalize"))
    globals()[parser.parse_args().action]()
