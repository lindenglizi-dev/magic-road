#!/usr/bin/env python3
"""Run the isolated byte-addressed 32x32 ROI reader verification."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT / "evaluation/ddr_architecture/ddr_roi_bytes_20261002_v1"
IVERILOG = PROJECT.parents[1] / ".tools/iverilog/bin/iverilog.exe"
VVP = PROJECT.parents[1] / ".tools/iverilog/bin/vvp.exe"

OWNED_SOURCES = [
    Path("tools/ddr_roi_byte_reference.py"),
    Path("tools/ddr_roi_bytes_trial.py"),
    Path("tests/experimental_ddr_ccl/ddr_roi_byte_reader.v"),
    Path("tests/experimental_ddr_ccl/ddr_roi_byte_reader_spec.md"),
    Path("tests/tb_ddr_roi_bytes.v"),
    Path("tests/tb_ddr_roi_bytes_spec.md"),
]

FACT_SOURCES = [
    Path("user_source/hdl_source/mc_to_user_interface.v"),
    Path("user_source/hdl_source/design_top_wrapper.v"),
    Path("user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v"),
    Path("user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v"),
    Path("user_source/hdl_source/ph1p35_ddr/ddr2/Design.xml"),
    Path("user_source/hdl_source/ph1p35_ddr/ddr2/ph1p_ddrmc_wrapper_63f4ac254419.v"),
    Path("user_source/hdl_source/ph1p35_ddr/ddr2/src/rtl/init/ph1p_ddrphy_dram_init_ddr2.v"),
    Path("user_source/hdl_source/video_in.v"),
    Path("user_source/hdl_source/video_out.v"),
    Path("user_source/hdl_source/data_96bit_to_128bit.v"),
    Path("user_source/hdl_source/isp/awb/awb.v"),
    Path("user_source/hdl_source/isp/isp_top.v"),
]

SCENARIOS = [
    {"scenario": 0, "task": 0x101, "frame": 0x201, "base": 0x00100000,
     "box": (0, 0, 1280, 720), "expected_requests": 1024},
    {"scenario": 1, "task": 0x102, "frame": 0x202, "base": 0x00400000,
     "box": (5, 0, 6, 1), "expected_requests": 2048},
    {"scenario": 2, "task": 0x103, "frame": 0x203, "base": 0x00700000,
     "box": (1279, 719, 1280, 720), "expected_requests": 1},
    {"scenario": 3, "task": 0x104, "frame": 0x204, "base": 0x00A00000,
     "box": (10, 719, 11, 720), "expected_requests": 2048},
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_hashes() -> dict[str, str]:
    fixed = [
        Path("CURRENT_ARCHITECTURE.md"),
        Path("REAL_DATA_WORKFLOW.md"),
        Path("DDR_ROAD_VISION_ARCHITECTURE_PLAN.md"),
        Path("evaluation/status.json"),
        Path("evaluation/criteria.pending.json"),
    ]
    files = [PROJECT / path for path in fixed]
    files += sorted((PROJECT / "user_source").rglob("*.v"))
    return {path.relative_to(PROJECT).as_posix(): digest(path)
            for path in files if path.is_file()}


def run_command(command: list[str], log: Path) -> None:
    completed = subprocess.run(command, cwd=PROJECT, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")


def source_facts() -> list[dict]:
    return [
        {"status": "proven", "fact": "user interface is 25-bit address and 128-bit data",
         "evidence": ["user_source/hdl_source/mc_to_user_interface.v:13-17"]},
        {"status": "proven", "fact": "read valid/data pass through without a user return-ready signal",
         "evidence": ["user_source/hdl_source/mc_to_user_interface.v:31-33",
                      "user_source/hdl_source/mc_to_user_interface.v:66-68"]},
        {"status": "proven", "fact": "active wrapper uses PAXI and permanently asserts paxi_rready",
         "evidence": ["user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v:51-58",
                      "user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v:69-74"]},
        {"status": "proven", "fact": "PAXI exposes no arlen/arsize/arburst; those fields occur only in the conditional full-AXI interface",
         "evidence": ["user_source/hdl_source/ph1p35_ddr/ddr2/ph1p_ddrmc_wrapper_63f4ac254419.v:88-126",
                      "user_source/hdl_source/ph1p35_ddr/ddr2/ph1p_ddrmc_wrapper_63f4ac254419.v:127-146"]},
        {"status": "proven", "fact": "generated controller is 128-bit, DDR2 is x16, and physical initialization selects BL8",
         "evidence": ["user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v:93-102",
                      "user_source/hdl_source/ph1p35_ddr/ddr2/Design.xml:44-46",
                      "user_source/hdl_source/ph1p35_ddr/ddr2/Design.xml:69-75",
                      "user_source/hdl_source/ph1p35_ddr/ddr2/src/rtl/init/ph1p_ddrphy_dram_init_ddr2.v:31"]},
        {"status": "candidate", "fact": "existing video logic advances address by 8 per 128-bit transfer; with x16 this supports 16-bit-word addressing and byte_addr>>1 adaptation",
         "evidence": ["user_source/hdl_source/video_in.v:202-203",
                      "user_source/hdl_source/video_out.v:127-128",
                      "user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v:69"]},
        {"status": "proven", "fact": "RGB888 is tightly packed and the lowest byte address of a beat maps to bits 127:120",
         "evidence": ["user_source/hdl_source/isp/awb/awb.v:478-482",
                      "user_source/hdl_source/data_96bit_to_128bit.v:48-61",
                      "user_source/hdl_source/video_out.v:174-193"]},
        {"status": "unresolved", "fact": "one accepted user read producing exactly one attributable 128-bit return is not frozen at the board boundary; paxi_rlast is not propagated to the user bridge and O_mc_app_rd_data_end has no assignment",
         "evidence": ["user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v:15-17",
                      "user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v:72-75",
                      "user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v:96-102",
                      "user_source/hdl_source/mc_to_user_interface.v:31-33"]},
    ]


def load_reference_module():
    sys.path.insert(0, str(PROJECT / "tools"))
    import ddr_roi_byte_reference as reference
    return reference


def parse_and_check(events_path: Path) -> dict:
    reference = load_reference_module()
    events = list(csv.reader(events_path.open(encoding="utf-8", newline="")))
    roi_by_tag: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
    jobs = {}
    accepts = []
    returns = []
    no_return = None
    late_cancel = None
    summary = None
    for row in events:
        if not row:
            continue
        if row[0] == "ROI":
            key = (int(row[1]), int(row[2]))
            roi_by_tag.setdefault(key, []).append(tuple(map(int, row[3:6])))
        elif row[0] == "JOB_DONE":
            jobs[int(row[1])] = tuple(map(int, row[2:4]))
        elif row[0] == "ACCEPT":
            accepts.append(tuple(map(int, row[1:4])))
        elif row[0] == "RETURN":
            returns.append(int(row[1]))
        elif row[0] == "NO_RETURN_HELD":
            no_return = tuple(map(int, row[1:5]))
        elif row[0] == "LATE_CANCEL_DONE":
            late_cancel = int(row[1])
        elif row[0] == "SUMMARY":
            summary = tuple(map(int, row[1:]))

    if summary != (4096, 5123, 5123, 1024, 2048, 1, 2048, 0):
        raise AssertionError(f"unexpected summary: {summary}")
    if no_return != (20, 1, 0, 1):
        raise AssertionError(f"reservation was not retained: {no_return}")
    if late_cancel is None:
        raise AssertionError("late cancel completion missing")
    if len(accepts) != len(returns) or any(address & 15 for _, _, address in accepts):
        raise AssertionError("accepted/returned count or alignment mismatch")

    vector_hashes = {}
    for item in SCENARIOS:
        expected = reference.roi_reference(item["base"], item["box"])
        actual = roi_by_tag.get((item["task"], item["frame"]), [])
        golden = [(entry["u"], entry["v"], entry["gray"]) for entry in expected]
        if actual != golden:
            raise AssertionError(f"ROI mismatch in scenario {item['scenario']}")
        if jobs.get(item["scenario"]) != (1024, item["expected_requests"]):
            raise AssertionError(f"request count mismatch in scenario {item['scenario']}")
        encoded = json.dumps(golden, separators=(",", ":")).encode()
        vector_hashes[str(item["scenario"])] = hashlib.sha256(encoded).hexdigest()

    return {
        "status": "PASS",
        "roi_pixels_compared": 4096,
        "accepted_requests": len(accepts),
        "returned_beats": len(returns),
        "requests_by_scenario": [jobs[index][1] for index in range(4)],
        "no_return_hold_cycles": no_return[0],
        "late_cancel_drain_cycles": late_cancel,
        "cancel_roi_outputs": summary[-1],
        "golden_vector_sha256": vector_hashes,
    }


def snapshot_sources(output: Path, sources: list[Path]) -> None:
    root = output / "runtime_sources"
    for relative in sources:
        source = PROJECT / relative
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def report_text(summary: dict) -> str:
    return f"""# DDR ROI 字节读取隔离验证

## 结果

- Python 整数参考自检：PASS。
- RTL/测试台：PASS；逐像素对拍 {summary['roi_pixels_compared']} 个灰度输出。
- 四个成功任务的读请求数：{summary['requests_by_scenario']}，分别覆盖全帧缩放、offset=15 跨拍重复采样、右下角末像素、offset=14 跨拍重复采样。
- 总请求/返回：{summary['accepted_requests']}/{summary['returned_beats']}；全部请求 16-byte 对齐。
- 迟取消在已接受返回到达后才完成排空；故意阻止返回 {summary['no_return_hold_cycles']} 周期时保持 busy=1、drained=0、reserved=1。
- 取消任务产生 ROI 输出：{summary['cancel_roi_outputs']}。

## 已证明的局部合同

测试对象使用字节地址，接受请求时固定 task/frame tag；接收深度为一拍，任何时刻 occupied+reserved<=1。取消会停止新请求，但不会清除已经接受的返回预留。返回没有 ready，测试台按一次接受对应一次 128-bit 返回拍的隔离合同驱动，并保证返回至少晚于接受一拍；同拍零延迟返回不在合同内。32x32 采样使用半开候选框中心最近邻坐标，RGB888 跨 16-byte 拍提取后按 `(R>>2)+(G>>1)+(B>>2)` 计算灰度。

`roi_valid` 没有 ready，下游必须保证每个有效输出都写入 ROI RAM。最近拍缓存以 frame ID 和帧基址识别内容；它们必须唯一对应尚未覆盖的同一帧，复用 ID/基址或覆盖帧区前需要显式失效缓存。

源码证据支持紧密 RGB888 及最高位优先 lane：最低字节地址对应 `beat[127:120]`。现有视频读写每个 128-bit 传输将 25-bit 用户地址加 8；结合 DDR2 x16，这支持适配层采用 `byte_addr>>1`，但这里仍将其列为接入候选合同。

## 证据边界

这不是实际板载 DDR 或已综合行缓存测试。PAXI 接口没有 `arlen/arsize/arburst`；生成配置为 128-bit、DDR2 x16、BL8。虽然物理突发宽度与 128 bit 相符，现有 wrapper 没有把 `paxi_rlast` 传到用户桥，`O_mc_app_rd_data_end` 也没有赋值。因此，一次用户读命令恰好产生一个可归属的 128-bit 返回拍，仍需用真实 IP 仿真或板上监测确认后才能冻结。

异步复位会清除本模块的 pending 状态，但不证明外部 DDR 已排空；正式接入需协调复位并排空或丢弃旧返回。本测试证明的是取消路径保留预留，不包含异步复位在途返回。坐标与字节地址乘法仅是功能参考写法，没有综合资源证据。

当前实现是单在途、单像素请求并只复用最近拍；本验证没有证明 15 Hz 或 DDR 带宽目标。没有修改生产 RTL、模型、验收配置或架构计划。
"""


def self_check() -> dict:
    reference = load_reference_module()
    result = reference.self_check()
    required = [PROJECT / path for path in OWNED_SOURCES + FACT_SOURCES]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    if not IVERILOG.is_file() or not VVP.is_file():
        raise FileNotFoundError("local Icarus toolchain missing")
    return {"status": "PASS", "reference": result, "sources_checked": len(required)}


def run(output: Path) -> dict:
    output = output.resolve()
    expected_root = (PROJECT / "evaluation/ddr_architecture").resolve()
    if not output.is_relative_to(expected_root):
        raise ValueError("output must stay inside evaluation/ddr_architecture")
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    protected_before = protected_hashes()
    output.mkdir(parents=True)

    commands = {
        "reference": [sys.executable, "-B", "tools/ddr_roi_byte_reference.py"],
        "compile": [str(IVERILOG), "-g2012", "-Wall", "-s", "tb_ddr_roi_bytes",
                    "-o", str(output / "simulation.vvp"),
                    "tests/tb_ddr_roi_bytes.v",
                    "tests/experimental_ddr_ccl/ddr_roi_byte_reader.v"],
        "simulate": [str(VVP), str(output / "simulation.vvp"),
                     f"+LOG={output / 'events.csv'}"],
    }
    run_command(commands["reference"], output / "reference.log")
    run_command(commands["compile"], output / "compile.log")
    run_command(commands["simulate"], output / "simulation.log")
    summary = parse_and_check(output / "events.csv")
    summary["reference_self_check"] = json.loads((output / "reference.log").read_text(encoding="utf-8"))
    dump(output / "summary.json", summary)
    dump(output / "commands.json", commands)
    dump(output / "source_facts.json", source_facts())
    (output / "report.md").write_text(report_text(summary), encoding="utf-8")

    sources = OWNED_SOURCES + FACT_SOURCES
    snapshot_sources(output, sources)
    protected_after = protected_hashes()
    if protected_after != protected_before:
        raise AssertionError("protected source changed during trial")

    source_hashes = {path.as_posix(): digest(PROJECT / path) for path in sources}
    artifacts = {path.relative_to(output).as_posix(): digest(path)
                 for path in sorted(output.rglob("*"))
                 if path.is_file() and path.name != "receipt.json"}
    receipt = {
        "status": "PASS",
        "command": [sys.executable, *sys.argv],
        "runtime": {"python": sys.version},
        "toolchain": {"iverilog": str(IVERILOG), "vvp": str(VVP)},
        "commands": commands,
        "source_hashes": source_hashes,
        "runtime_source_hashes": {
            path.as_posix(): digest(output / "runtime_sources" / path) for path in sources
        },
        "protected_sources_unchanged": protected_after,
        "artifact_hashes": artifacts,
        "evidence_boundary": "isolated one-request/one-128-bit-response model; real board/IP response ownership and byte-to-user address conversion remain unqualified",
    }
    if receipt["source_hashes"] != receipt["runtime_source_hashes"]:
        raise AssertionError("runtime source snapshot mismatch")
    dump(output / "receipt.json", receipt)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    result = self_check() if arguments.self_check else run(arguments.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
