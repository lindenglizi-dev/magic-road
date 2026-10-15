"""PW48参数浅bank候选：复用原工具，只在本目录输出。"""
import argparse
from collections import Counter
import csv
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "pw48_tile_20261015"
spec = importlib.util.spec_from_file_location("pw48_frozen_tools", BASE / "run.py")
tools = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tools
spec.loader.exec_module(tools)
tools.ROOT = ROOT
tools.helpers.ROOT = ROOT
sha, save, fresh, command = tools.sha, tools.save, tools.fresh, tools.command


def setup():
    assert not (ROOT / "frozen.json").exists()
    paths = [*BASE.joinpath("rtl").glob("*.v"), *BASE.joinpath("tests").glob("*.v"),
             *BASE.glob("*.hex"), BASE / "run.py", BASE / "artifact_manifest.json",
             BASE / "status.json", BASE / "physical_attempt2/pr.db",
             BASE / "physical_attempt2/physical_summary.json", BASE / "simulation_attempt3/receipt.json",
             *[tools.CORE / name for name in tools.CORE_NAMES],
             tools.REPO / "user_source/hdl_source/design_top_wrapper.v"]
    save(ROOT / "frozen.json", {str(p): sha(p) for p in paths})
    for folder in ("rtl", "tests"):
        (ROOT / folder).mkdir(exist_ok=True)
        for p in (BASE / folder).glob("*.v"):
            shutil.copyfile(p, ROOT / folder / p.name)
    for p in [*BASE.glob("*.hex"), BASE / "reference_receipt.json"]:
        shutil.copyfile(p, ROOT / p.name)
    save(ROOT / "status.json", {"status": "FROZEN_REVIEW_PENDING", "baseline_commit": "2be925d5",
         "scope": "bias/pre_multiplier three 16-deep banks only", "production_delivery_ready": False})
    tools.check()


def review():
    work = fresh("review")
    command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"),
             "review", "--target", BASE / "rtl/road_pw_tile_scheduler.v", "--report-json", work / "review.json"],
            work, "review", allowed=(0, 1, 2))
    tools.check()


def memory():
    source = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    work = fresh("memory_query")
    shutil.copyfile(source / "pr.db", work / "source.db")
    project = (source / "road_pw_validation_top.al").read_text(encoding="utf-8").replace(source.as_posix(), work.as_posix())
    (work / "road_pw_validation_top.al").write_text(project, encoding="utf-8")
    (work / "query.tcl").write_text("""import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_pw_validation_top.al -single_run
import_db source.db
report_ram_utilization -file ram.rpt
puts "MEMORY_QUERY_DONE"
close_project
exit
""", encoding="utf-8")
    digest = sha(source / "pr.db")
    output = command([tools.TD, "query.tcl"], work, "td_launcher")
    assert "MEMORY_QUERY_DONE" in output and sha(source / "pr.db") == digest
    save(work / "receipt.json", {"status": "PASS", "database_sha256": digest})
    tools.check()


def specifications():
    tools.specifications()
    work = sorted(ROOT.glob("specifications*"), key=lambda p: p.stat().st_mtime)[-1]
    path = work / "road_pw_tile_scheduler.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    module = data["modules"][0]
    module["behavior"].append("bias/pre_multiplier各三路16×32浅bank；通道c存bank=c%3,row=c//3，PREPARE读三bank的output_group。")
    module["behavior"].append("两类装载lane/row独立，地址0重启；非法记录不写不推进，reset只清游标/完整性，不清数组。")
    module["timing_diagrams"].append({"id": "parameter_bank", "scenario": "parameter_bank", "title": "三浅bank连续装载",
        "description": "逻辑地址按0..47连续接受；三bank轮转，row每三项推进，addr0重启。计算读地址无需除3。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p......"}, {"name": "load_accept", "wave": "01....0"},
            {"name": "logical_address", "wave": "x=====x", "data": ["0", "1", "2", "3", "4"]},
            {"name": "write_bank", "wave": "x=====x", "data": ["0", "1", "2", "0", "1"]},
            {"name": "write_row", "wave": "x=..=.x", "data": ["0", "1"]}]}})
    save(path, data)
    command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"), "write-spec",
             "--spec", path, "--source", ROOT / "rtl/road_pw_tile_scheduler.v", "--out-dir", work, "--no-state"],
            ROOT, str(work.relative_to(ROOT) / "bank_spec"))
    shutil.copyfile(work / "spec/pw_fixed_tile/road_pw_tile_scheduler_spec.md", ROOT / "rtl/road_pw_tile_scheduler_spec.md")
    shutil.copytree(work / "spec/pw_fixed_tile/waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)


def compare():
    tools.check()
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    assert json.loads((simulation / "receipt.json").read_text(encoding="utf-8"))["status"] == "PASS"
    assert "TB_PASS_PARAMETER_BANKS" in (simulation / "tb_pw_tile.log").read_text(encoding="utf-8")
    assert sha(ROOT / "rtl/road_pw_validation_top.v") == sha(BASE / "rtl/road_pw_validation_top.v")
    for manifest in (simulation / "input_manifest.json",):
        for path, value in json.loads(manifest.read_text(encoding="utf-8")).items():
            assert sha(Path(path)) == value
            for folder in ("rtl", "tests"):
                if Path(path).name.endswith(".v") and (ROOT / folder / Path(path).name).exists():
                    assert sha(ROOT / folder / Path(path).name) == value, str(ROOT / folder / Path(path).name)
    comparisons = {}
    for name in ("tb_pw_tile.csv", "tb_pw_narrow.csv"):
        old = list(csv.DictReader((BASE / "simulation_attempt3" / name).open(encoding="utf-8")))
        new = list(csv.DictReader((simulation / name).open(encoding="utf-8")))
        assert old == new, (name, old, new)
        comparisons[name] = {"same_all_fields": True, "rows": new}
    save(ROOT / "cycle_comparison.json", comparisons)
    physical = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    current = json.loads((physical / "physical_summary.json").read_text(encoding="utf-8"))
    old = json.loads((BASE / "physical_attempt2/physical_summary.json").read_text(encoding="utf-8"))
    assert json.loads((physical / "input_check_after.json").read_text(encoding="utf-8"))["same"]
    assert all(sha(Path(path)) == value for path, value in
               json.loads((physical / "input_manifest.json").read_text(encoding="utf-8")).items())
    parser = tools.load("parameter_bank_timing_parser", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    failed = {}
    for name in current["reports"]:
        _, records = parser.read_timing(physical / (name + ".timing"), keep_negative=True)
        for record in records:
            key = (record["check"], record["end"])
            if key not in failed or record["slack_ns"] < failed[key]["slack_ns"]:
                failed[key] = record
    current["internal_failed_endpoints"] = [r for r in failed.values() if r["scope"] == "internal"]
    current["internal_timing_pass"] = not current["internal_failed_endpoints"]
    save(physical / "physical_summary.json", current)
    save(physical / "failed_endpoint_inventory_union.json", list(failed.values()))
    save(ROOT / "resource_comparison.json", {"baseline": old["resources"], "candidate": current["resources"],
         "internal_timing_pass": current["internal_timing_pass"], "scope": current["scope"],
         "not_whole_network_or_board": True})
    gate = sorted(ROOT.glob("gate*/rtl.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    summary = {}
    for folder in ("rtl", "tests"):
        data = json.loads((gate / (folder + ".json")).read_text(encoding="utf-8"))
        summary[folder] = {k: data.get(k) for k in ("errors", "strict_warnings", "checks", "delivery_ready", "delivery_issues_by_rule")}
    save(ROOT / "strict_summary.json", summary)
    query = sorted(ROOT.glob("memory_query*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    assert json.loads((query / "receipt.json").read_text(encoding="utf-8"))["database_sha256"] == current["database_sha256"]
    ram = (query / "ram.rpt").read_text(encoding="utf-8")
    eram = ram.split("ERAM20K Usage", 1)[1].split("Distributed RAM Usage", 1)[0]
    records = re.findall(r"^\s*(\S+)\s*\|\s*(\S+\.v\((\d+)\))", eram, re.M)
    assert len(records) == current["resources"]["eram"]["used"]
    source_lines = (ROOT / "rtl/road_pw_tile_scheduler.v").read_text(encoding="utf-8").splitlines()
    save(ROOT / "ram_allocation.json", {"observed_eram": len(records), "records": [
        {"name": name, "source": source, "rtl_line": source_lines[int(line) - 1] if "scheduler.v" in source else "shared SiLU"}
        for name, source, line in records], "ram_report_sha256": sha(query / "ram.rpt")})
    before, after = old["resources"], current["resources"]
    assert all(after["hierarchy_rows"][name] == 1 for name in
               ("road_mac_probe", "road_dynamic_postprocess", "silu_shared_unit"))
    assert after["dsp"]["used"] <= 40 and after["eram"]["used"] <= 108 and after["slice"]["used"] <= 21216
    checks = current["reports"]["internal_all_checks"]["checks"]
    external = dict(Counter(r["scope"] + ":" + r["check"] for r in failed.values() if r["scope"] != "internal"))
    gate_before = json.loads((BASE / "strict_summary.json").read_text(encoding="utf-8"))["objects"]
    text = f"""RoadYOLO PW48参数浅bank：实测对比与下一步（2026-10-15）

尚未通过：外部窄口/原始复位接口时序、严格交付门、完整图/DDR/视频集成及真实量化模型验收。
内部时序是否通过：{current['internal_timing_pass']}；全报告并集内部失败端点{len(current['internal_failed_endpoints'])}。
当前较差：内部setup余量只有0.017ns（旧1.287ns），hold0.021ns（旧0.020ns）；不能称为稳健裕量。

一、本次只改什么
基线work/roadyolo @2be925d5，旧目录pw48_tile_20261015未覆盖，冻结依赖见frozen.json/frozen_check.json。
新rtl/road_pw_tile_scheduler.v：bias及pre_multiplier各从48×32三读数组改为三路16×32一读bank。
逻辑通道c→bank=c%3,row=c//3；计算直接用output_group读三个bank。
装载两类使用独立lane/row游标，地址0重启，不在计算路径加入除法。47→bank2,row15后归零。
未改shift、激活/权重/输出缓存、算术核、wrapper、调度FSM、接口、II、数值和复位契约。

二、功能与周期证据
Python映射参考131072条交错/重启记录通过；旧四套黄金向量按原哈希复用。
ModelSim原五个计时窗口、MAC/pre/SiLU/post/提交/实际导出全部通过；两个TB各0 errors、2个厂商INIT_FILE警告。
新增交错bias/premul48项、两类地址0重启、47边界、非法记录不推进/不改写、装载中复位均通过。
tb_pw_tile.csv五行和tb_pw_narrow.csv所有字段与基线完全一致，不只比较最终done。
正常核心3874拍；随机3875；512拍满队列4375。预装载/导出窗口也未变化。
正常互斥分解：PREPARE256 + MAC有效送入1536 + MAC结果接受256 + MAC等待1536 + DRAIN34 + ADVANCE256 = 3874。
pre/SiLU/post活动3328/2048/3328有重叠，不能相加。此次是存储优化，不是吞吐加速。

三、真实PH1P35MDG324-3、100MHz布局布线（含42位验证壳，不含完整ROM/视频/DDR）
资源          基线       新候选       变化
ERAM          {before['eram']['used']}          {after['eram']['used']}          {after['eram']['used']-before['eram']['used']:+d}
DSP           {before['dsp']['used']}          {after['dsp']['used']}          {after['dsp']['used']-before['dsp']['used']:+d}
Slice         {before['slice']['used']}        {after['slice']['used']}        {after['slice']['used']-before['slice']['used']:+d}
register      {before['registers']}        {after['registers']}        {after['registers']-before['registers']:+d}
I/O           {before['io']['used']}          {after['io']['used']}          {after['io']['used']-before['io']['used']:+d}
RAM逐项归属见ram_allocation.json与memory_query/ram.rpt，不能凭源码数组数推断物理数量。
ERAM减少6块的同时，distributed RAM LUT由272增至368，Slice多250、register多325；不是所有资源同时下降。
MAC/dynamic_PP/SiLU实际层级各保留1，动态输入和参数不替换为常量；完整源码/工具输入及数据库哈希已记录。

四、时序与证据边界
内部最差slack(ns)：{dict((k, v['worst_slack_ns']) for k, v in checks.items())}。
全部报告（含ignored、DSP、ERAM）负端点按check/end取最差并集，外部未签核：{external}。
角点与覆盖：{current['reports']['all_endpoints_include_ignored']['processes']}；{current['reports']['all_endpoints_include_ignored']['coverage']}。
自动引脚、0ns诊断I/O延迟只供隔离比较，不代表真实外设满足。未新增时序例外，未生成位流。
新候选内部通过不能替代外部接口、整机和生产签核；正hold余量仍需在融合顶层重测。
最差setup：壳state_current[2]→PP ingress/inflight控制→u_pre/u_round CE；slow_m40c，4级逻辑，扇出855。
数据延迟9.737ns，其中net8.777ns（91%）；末段i_advance网4.923ns。这是现有停顿使能分发的布线瓶颈，不是乘积位宽变长。
算术核源码未改；资源映射改变后布局敏感。保留旧版本作较宽setup裕量的对照，不宣布新候选可直接融合上板。
raw_reset仍有66个removal、32个hold负端点；不能笼统当成不重要接口问题，更不能未经对象证明添加例外。
check_timing的2类DSP dummy控制端与SYN-5025置零通用警告保留；日志未给出完整逐pin清单，本轮不宣称原语全pin签核。

五、严格门禁与失败解释
RTL诊断{gate_before['rtl']['errors']}→{summary['rtl']['errors']}；TB{gate_before['tests']['errors']}→{summary['tests']['errors']}。
两份RTL仍有control parser strict failure，0解析模块，后续部分诊断为级联；其余缩进/注释/命名未本轮重写。
诊断数变化随新增声明和测试注释项增长，不等于新增同数量硬件错误；仍明确不通过，不豁免。
八项完整矩阵见strict_summary.json。真实ModelSim编译运行和TD实现证据另存，不能替代严格门。
最初默认运行Python打印运行时定位提示但已执行setup/review；重试setup由冻结文件存在保护拒绝，未覆盖基线。
两次review和第一次规格输出均保留；后续规格补齐实际bank行为及周期图，没有删除失败记录。
最终哈希检查还发现初次仿真快照的premul非法地址测试用负数据，而最终TB改成合法正数据以隔离地址错误；功能RTL未变。
因此重跑仿真及门禁，最终报告只接受与当前源码逐字节绑定的最新收据；旧仿真/失败原因保留见失败记录.txt。

六、对全局预算的影响和下一步
条件式简单拼接：旧40视频+56ROM+16本壳=112；当前40+56+{after['eram']['used']}={96+after['eram']['used']}。
这只说明当前存储冲突改善程度，不是融合综合通过：共享缓存、控制、DDR、NMS等尚未完整计入。
本次周期不变，沿用上一阶段三完整前层4579776 + 两个S4 PW48形状投影4462848 = 9042624。
剩余10957376拍需容纳其余62卷积和DDR/非卷积/NMS，整网5FPS尚未证明；测试系数不代表真实QAT。
下一单变量：复用当前核和bank方案，验证冻结图中96/192输入PW的真实形状/尾组，及stride1 DW的小块周期。
在下一个实际顶层同步核对该高扇出使能路径，不围绕本壳17ps重复随机布局；需要改内部使能寄存/核接口时先提出单独决定。
先对拍并更新逐层预算；不同时改变MAC任务间重叠或缩网。只有实测完整预算仍不满足再决定唯一H24备选。

结论：用实际映射检验浅bank是否省RAM，保持原数值与全部周期窗口。当前仍是局部算子阶段，不是已部署完整CNN。
"""
    (ROOT / "阶段报告与下一步.txt").write_text(text, encoding="utf-8")
    save(ROOT / "status.json", {"status": "MEASURED_INTERNAL_PASS_EXTERNAL_STRICT_OPEN" if current["internal_timing_pass"] else "INTERNAL_TIMING_FAILED",
         "baseline_commit": "2be925d5", "functional_pass": True, "cycles_identical": True,
         "normal_core_cycles": 3874, "physical_resources": after,
         "internal_min_slack_ns": {k: v["worst_slack_ns"] for k, v in checks.items()},
         "external_failed_endpoints": external,
         "production_delivery_ready": False, "whole_network_verified": False})
    files = [p for p in ROOT.rglob("*") if p.is_file() and "work" not in p.relative_to(ROOT).parts and "__pycache__" not in p.parts]
    save(ROOT / "artifact_manifest.json", {str(p.relative_to(ROOT)): sha(p) for p in files if p.name != "artifact_manifest.json"})


if __name__ == "__main__":
    actions = {"setup": setup, "review": review, "memory": memory, "compare": compare, "specifications": specifications}
    actions.update({name: getattr(tools, name) for name in
                   ("check", "dependency", "tb_specifications", "gate", "simulate", "physical")})
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=actions)
    actions[parser.parse_args().action]()
