"""冻结三种PW缓存形状的独立验证；不扩大算术接口或装载协议。"""
import argparse
from collections import Counter
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "pw48_parameter_banks_20261015"
GOLDEN = ROOT.parent / "pw48_tile_20261015"
spec = importlib.util.spec_from_file_location("deep_pw_existing_tools", GOLDEN / "run.py")
tools = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tools
spec.loader.exec_module(tools)
tools.ROOT = ROOT
tools.helpers.ROOT = ROOT
sha, save, fresh, command = tools.sha, tools.save, tools.fresh, tools.command


def setup():
    assert not (ROOT / "frozen.json").exists()
    paths = [*BASE.joinpath("rtl").glob("*.v"), *BASE.joinpath("tests").glob("*.v"),
             *GOLDEN.glob("*.hex"), BASE / "artifact_manifest.json", BASE / "status.json",
             BASE / "physical/pr.db", BASE / "physical/physical_summary.json",
             BASE / "simulation_attempt2/receipt.json", GOLDEN / "run.py",
             *[tools.CORE / name for name in tools.CORE_NAMES],
             tools.REPO / "cnn/hw_validation/production/graph_artifacts/graph.json",
             tools.REPO / "cnn/hw_validation/production/deployment_contract.json",
             tools.REPO / "user_source/hdl_source/design_top_wrapper.v"]
    save(ROOT / "frozen.json", {str(p): sha(p) for p in paths})
    for folder in ("rtl", "tests"):
        (ROOT / folder).mkdir(exist_ok=True)
        for p in (BASE / folder).glob("*.v"):
            shutil.copyfile(p, ROOT / folder / p.name)
    save(ROOT / "status.json", {"status": "FROZEN_REFERENCE_PENDING", "baseline_commit": "9661d2ae",
         "scope": "fixed PW96->24 and eight PW192->12 output slabs", "production_delivery_ready": False})
    tools.check()


def review():
    work = fresh("review")
    for name in ("road_pw_tile_scheduler", "road_pw_validation_top"):
        command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"),
                 "review", "--target", BASE / "rtl" / (name + ".v"), "--report-json", work / (name + ".json")],
                work, name, allowed=(0, 1, 2))
    tools.check()


def simulate():
    tools.check()
    receipt = json.loads((ROOT / "reference_receipt.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS"
    assert sha(ROOT / "reference.py") == receipt["sources"]["reference.py"]
    assert sha(ROOT / "reference_contract.json") == receipt["sources"]["reference_contract.json"]
    for name in ("package_manifest", "package_payload"):
        record = receipt["sources"][name]
        assert sha(tools.REPO / record["path"]) == record["sha256"]
    for case in receipt["cases"]:
        for record in case["files"].values():
            assert sha(ROOT / record["name"]) == record["sha256"]
    table = receipt["common_files"]["silu_table"]
    assert sha(ROOT / table["name"]) == table["sha256"]
    work = fresh("simulation")
    snapshots = work / "sources"
    snapshots.mkdir()
    for p in [*ROOT.joinpath("rtl").glob("*.v"), *ROOT.joinpath("tests").glob("*.v")]:
        shutil.copyfile(p, snapshots / p.name)
    sources = [*sorted(snapshots.glob("*.v")), *[tools.CORE / name for name in tools.CORE_NAMES]]
    args = json.loads((GOLDEN / "simulation_attempt3/vlog.command.json").read_text(encoding="utf-8"))["command"]
    vendor = [a for a in args if "sim_release" in str(a)]
    hashes = {str(p): sha(p) for p in [*sources, *ROOT.glob("*.hex"), *GOLDEN.glob("*.hex"), ROOT / "reference_receipt.json"]}
    save(work / "input_manifest.json", hashes)
    command([tools.helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([tools.helpers.MSIM / "vlog.exe", "-work", "work", *vendor, *sources], work, "vlog")
    cases = [("tb_pw_tile", GOLDEN), ("tb_pw_narrow", GOLDEN), ("tb_pw_deep96", ROOT), ("tb_pw_deep192", ROOT)]
    if (ROOT / "tests/tb_pw_deep_narrow.v").exists():
        cases.append(("tb_pw_deep_narrow", ROOT))
    results = {}
    for name, vectors in cases:
        output = command([tools.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", name,
            "+VECTORS=" + vectors.as_posix(), "+REPORT=" + (work / (name + ".csv")).as_posix(),
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, name)
        assert "Failed to open readmem" not in output, (name, "test vector path missing")
        assert "TB_PASS_" in output, (name, str(work / (name + ".log")))
        results[name] = [line for line in output.splitlines() if "TB_PASS_" in line]
    assert all(sha(Path(p)) == value for p, value in hashes.items())
    save(work / "receipt.json", {"status": "PASS", "results": results,
         "input_manifest_sha256": sha(work / "input_manifest.json"), "arithmetic_core_unchanged": True})
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_PHYSICAL_PENDING", "production_delivery_ready": False})
    tools.check()


def specifications():
    work = fresh("specifications")
    for name in ("road_pw_tile_scheduler", "road_pw_validation_top"):
        data = json.loads((BASE / "specifications_attempt2" / (name + ".json")).read_text(encoding="utf-8"))
        module = data["modules"][0]
        module["description"] = "冻结三种形状：PROFILE0=48→48兼容，1=96→24，2=192→12输出分片；同一算术核和窄口协议。"
        module["parameters"] = [{"name": "PROFILE", "type": "integer", "default": 0 if name.endswith("scheduler") else 2,
                                 "description": "只支持0/1/2三个冻结编译形状；不是运行时任意卷积配置。"}]
        module["constraints"] = ["12位逻辑装载地址不变；每片权重2304，输入768/1536/3072，输出768/384/192。",
                                  "192→96按8个12输出通道分片；当前外部图级遍历和全局写址尚未实现。",
                                  "算术核signed33末组INT32、RNE、SiLU、II、反压和复位行为不变。"]
        module["behavior"] = ["PROFILE0保留原回归；PROFILE1/2分别12/24组×8输入，未超过192有效乘积。",
            "输入bank=ic%8,row=position*(Cin/8)+ic//8；权重bank=(local_oc%3)*8+ic%8,row=(local_oc//3)*(Cin/8)+ic//8。",
            "bias/pre三浅bank不变；装载地址0重启，完整性与合法性检查按冻结片形状展开。",
            "每片输出local tag=position*Cout+local_oc；局部输出真实缓存逐项导出。全局OC合并由参考检查，不声称图执行器已实现。",
            "表1024项重装、first/last、长反压、故障禁止发布、复位即时取消与既有接口保持。"]
        module["corner_cases"] = ["输入1535/1536、3071/3072，权重2303/2304，24/12参数边界，末24组及输出分片拼接。"]
        module["verification_cases"] = ["PROFILE0同CSV回归；96及192八片真实参数逐级黄金值、随机/长反压、复位取消。"]
        for port in module["interfaces"]["ports"]:
            if port["name"] == "i_load_addr":
                port["description"] = "12位地址不变；输入0..16Cin-1、权重0..2303、通道参数0..Cout-1。"
            if port["name"] == "o_output_index":
                port["description"] = "片内HWC索引0..16Cout-1，握手推进；不冒充整图全局写地址。"
        module["timing_diagrams"] = [{"id": "slab", "scenario": "slab", "title": "输出分片逐段归约",
            "description": "装载→PREPARE→12或24组接受→MAC等待→下一任务，所有输出提交才done，再导出。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p........"}, {"name": "load_complete", "wave": "01......."},
                {"name": "mac_valid", "wave": "0.1...0.."}, {"name": "group", "wave": "x.====x..", "data": ["0", "1", "...", "11/23"]},
                {"name": "result_accept", "wave": "0......10"}, {"name": "next_task", "wave": "0.......1"}]}}]
        path = work / (name + ".json")
        save(path, data)
        command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"), "write-spec",
                 "--spec", path, "--source", ROOT / "rtl" / (name + ".v"), "--out-dir", work, "--no-state"],
                ROOT, str(work.relative_to(ROOT) / name))
        bundle = work / "spec/pw_fixed_tile"
        shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "rtl" / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    tools.check()


def tb_specifications():
    work = fresh("test_specifications")
    template = json.loads((BASE / "test_specifications/tb_pw_tile.json").read_text(encoding="utf-8"))
    for name in ("tb_pw_tile", "tb_pw_narrow", "tb_pw_deep", "tb_pw_deep96", "tb_pw_deep192", "tb_pw_deep_narrow"):
        data = json.loads(json.dumps(template))
        module = data["modules"][0]
        source = "tb_pw_deep.v" if name in ("tb_pw_deep96", "tb_pw_deep192") else name + ".v"
        module.update(name=name, rtl_path=source, description="PW固定形状逐级对拍与独立周期窗口；o_test_done只在完整自检通过时置位。")
        module["behavior"] = ["旧PROFILE0沿冻结四套向量；新96/192先正常窗口，再压力、故障和复位。",
            "acc/pre/SiLU/post/提交/真实导出逐项比较；192八片重组不代替图级全局地址执行。",
            "prepare/send/mac_wait/drain/advance互斥周期和等于core；raw PP busy有重叠，不相加。"]
        module["verification_cases"] = ["ModelSim实际日志PASS且0 errors；源码/参数快照另存。"]
        module["parameters"] = [{"name": "PROFILE", "type": "integer", "default": 1,
                                  "description": "仅1=96→24或2=192→12"}] if name == "tb_pw_deep" else []
        path = work / (name + ".json")
        save(path, data)
        module_out = work / name
        # task输入误识别仍保留原失败；这里只渲染已确认的真实完成端口，不冒充源码解析通过。
        command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"), "write-spec",
                 "--spec", path, "--out-dir", module_out, "--no-state"], ROOT, str(work.relative_to(ROOT) / name))
        bundle = module_out / "spec/pw_testbench"
        shutil.copyfile(bundle / (Path(source).stem + "_spec.md"), ROOT / "tests" / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms", dirs_exist_ok=True)
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


def finalize():
    tools.check()
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    assert json.loads((simulation / "receipt.json").read_text(encoding="utf-8"))["status"] == "PASS"
    for path, value in json.loads((simulation / "input_manifest.json").read_text(encoding="utf-8")).items():
        assert sha(Path(path)) == value, path
        for folder in ("rtl", "tests"):
            candidate = ROOT / folder / Path(path).name
            if candidate.exists() and candidate.suffix == ".v":
                assert sha(candidate) == value, str(candidate)
    for name in ("tb_pw_tile.csv", "tb_pw_narrow.csv"):
        old = list(csv.DictReader((BASE / "simulation_attempt2" / name).open(encoding="utf-8")))
        new = list(csv.DictReader((simulation / name).open(encoding="utf-8")))
        assert old == new, name
    deep = {}
    partition = ("prepare", "send_accept", "send_stall", "mac_wait_accept", "mac_wait", "drain", "advance")
    for name in ("tb_pw_deep96", "tb_pw_deep192"):
        rows = [{k: int(v) for k, v in row.items()} for row in csv.DictReader((simulation / (name + ".csv")).open(encoding="utf-8"))]
        assert all(sum(row[k] for k in partition) == row["core_cycles"] for row in rows)
        deep[name] = rows
    normal96 = [r for r in deep["tb_pw_deep96"] if r["stall_mode"] == 0]
    normal192 = [r for r in deep["tb_pw_deep192"] if r["stall_mode"] == 0]
    assert len(normal96) == 1 and len(normal192) == 8
    assert [r["slab"] for r in normal192] == list(range(8))
    cycles96 = normal96[0]["core_cycles"]
    cycles192 = normal192[0]["core_cycles"]
    assert all(r["core_cycles"] == cycles192 for r in normal192)
    narrow = list(csv.DictReader((simulation / "tb_pw_deep_narrow.csv").open(encoding="utf-8")))
    assert int(narrow[0]["core_cycles"]) == cycles192
    save(ROOT / "cycle_summary.json", {"profiles": deep, "normal96": cycles96, "normal192_slab": cycles192,
         "normal192_eight_slabs_core_sum": sum(r["core_cycles"] for r in normal192),
         "partition": partition, "raw_pp_busy_not_additive": True, "narrow": narrow,
         "compatibility_all_csv_fields_identical": True,
         "limits": "Eight independently driven slabs; no graph-level traversal/global DDR writer or full-frame measurement"})
    physical = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    current = json.loads((physical / "physical_summary.json").read_text(encoding="utf-8"))
    assert json.loads((physical / "input_check_after.json").read_text(encoding="utf-8"))["same"]
    for path, value in json.loads((physical / "input_manifest.json").read_text(encoding="utf-8")).items():
        assert sha(Path(path)) == value, path
    parser = tools.load("deep_pw_timing_parser", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    failed = {}
    for name in current["reports"]:
        _, records = parser.read_timing(physical / (name + ".timing"), keep_negative=True)
        for record in records:
            key = (record["check"], record["end"])
            if key not in failed or record["slack_ns"] < failed[key]["slack_ns"]:
                failed[key] = record
    internal = [r for r in failed.values() if r["scope"] == "internal"]
    current.update(internal_failed_endpoints=internal, internal_timing_pass=not internal)
    save(physical / "physical_summary.json", current)
    save(physical / "failed_endpoint_inventory_union.json", list(failed.values()))
    resources = current["resources"]
    assert resources["io"]["used"] == 42
    assert resources["dsp"]["used"] <= 40 and resources["eram"]["used"] <= 108 and resources["slice"]["used"] <= 21216
    assert all(resources["hierarchy_rows"][name] == 1 for name in
               ("road_mac_probe", "road_dynamic_postprocess", "silu_shared_unit"))
    gate = sorted(ROOT.glob("gate*/rtl.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    gates = {}
    for name in ("rtl", "tests"):
        value = json.loads((gate / (name + ".json")).read_text(encoding="utf-8"))
        gates[name] = {k: value[k] for k in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}
    save(ROOT / "strict_summary.json", {"objects": gates, "delivery_ready": False,
         "actual_modelsim": "PASS", "actual_td_internal": not internal})
    graph = json.loads((tools.REPO / "cnn/hw_validation/production/graph_artifacts/graph.json").read_text(encoding="utf-8"))
    ledger = json.loads((GOLDEN / "layer_cycle_ledger.json").read_text(encoding="utf-8"))
    projections = []
    for node in graph["nodes"]:
        if node["op"] != "conv" or node["groups"] != 1 or node["kernel"] != [1, 1]:
            continue
        cin = node["input_shape_hwc"][2]
        if cin not in (96, 192):
            continue
        height, width, cout = node["output_shape_hwc"]
        chunk = 24 if cin == 96 else 12
        assert cout % chunk == 0 and node["dtype"] == "int8"
        tiles = ((height + 3) // 4) * ((width + 3) // 4)
        slab_cycles = cycles96 if cin == 96 else cycles192
        row = {"name": node["name"], "shape_hwc": node["output_shape_hwc"], "cin": cin, "chunk": chunk,
               "chunks": cout // chunk, "tiles_including_partial_bottom": tiles, "measured_slab_core": slab_cycles,
               "conditional_layer_core": tiles * (cout // chunk) * slab_cycles,
               "own_parameters_checked_as_tile": node["name"] in ("sppf.squeeze.conv", "fuse4_bu.reduce.conv"),
               "full_tensor_rtl_verified": False}
        projections.append(row)
        target = next(item for item in ledger["layers"] if item["name"] == node["name"])
        target.update(measurement_kind="measured_shape_output_slab_projection", **{k: v for k, v in row.items() if k != "name"})
    total = ledger["conditional_5layer_core"] + sum(row["conditional_layer_core"] for row in projections)
    ledger.update(deep_pw_projections=projections, additional_fixed_tile_shapes=4,
                  deep_tile_layers_with_own_parameters=2, budgeted_layer_shapes=13, conditional_13layer_core=total,
                  remaining_54conv_and_other_budget=20000000-total,
                  limits="3 full-tensor test-parameter layers; all other entries are tile/shape projections. DDR/ROM, graph traversal, partial-tile cropping, nonconv/NMS not included.")
    save(ROOT / "layer_cycle_ledger.json", ledger)
    external = dict(Counter(r["scope"] + ":" + r["check"] for r in failed.values() if r["scope"] != "internal"))
    checks = current["reports"]["internal_all_checks"]["checks"]
    query = sorted(ROOT.glob("memory_query*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    assert json.loads((query / "receipt.json").read_text(encoding="utf-8"))["database_sha256"] == current["database_sha256"]
    save(ROOT / "status.json", {"status": "DEEP_PW_NUMERIC_CYCLE_INTERNAL_PASS" if not internal else "DEEP_PW_NUMERIC_PASS_INTERNAL_TIMING_FAILED",
         "baseline_commit": "9661d2ae", "normal96_core": cycles96, "normal192_slab_core": cycles192,
         "eight_slabs_core_sum": cycles192*8, "physical_resources_profile2": resources,
         "internal_min_slack_ns": {k: v["worst_slack_ns"] for k, v in checks.items()},
         "internal_failed_endpoints": len(internal), "external_failed_endpoints": external,
         "conditional_13layer_core": total, "remaining_54conv_and_other_budget": 20000000-total,
         "production_delivery_ready": False, "whole_network_verified": False})
    text = f"""RoadYOLO深通道PW：执行、总体位置与下一步（2026-10-15）

尚未通过：外部I/O/原始复位时序、严格交付门、67层图执行、真实DDR可见性、整网精度及5FPS。
当前位于B/C扩展收口、D固定图执行的前段；本次不是训练或整机部署。

1. 本轮实际完成
冻结9661d2ae参数浅bank基线及59项依赖，未覆盖旧核/旧报告。新代码位于本目录rtl/。
三种编译形状：PROFILE0原48→48；PROFILE1真实sppf.squeeze.conv的96→24；PROFILE2真实fuse4_bu.reduce.conv按8个192→12片执行。
每片权重2304B不变、24权重bank仍96深，输入bank变为192/384深，参数3浅bank，输出只保留当前片。
12位装载地址、16位窄口、42位I/O、算术接口/II/数值/复位契约不变。未加新算术核、FIFO或外设协议。
三种PROFILE仅用于独立测量，部署不能复制三套MAC；最终仍应一套24MAC/PP由固定图调度器复用。

2. 参数与数值
复用另一条线已保存的QAT-G10硬件联调包；原manifest标记TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED保持不改。
这代表已有训练参数的硬件联调资产，不是完整QAT/精度合格证明。输入为固定种子随机中间激活，不是整网真实图像。
96→24及192→96的全部acc/pre/SiLU/post参考通过；192八片四阶段重组完全一致。
192全层294912逐乘积prefix、36864分组prefix通过；普适上界2^31+192*128*128=2150629376<2^32，最终INT32另作实际检查。
concat.10固定通道顺序[down4_bu.pw.conv,sppf.out.conv]，不互相交错。
最终ModelSim五顶层均PASS；全部阶段/地址/真实缓存导出比较，旧48的两份CSV每列完全不变。
新测试含正常、随机及512拍满队列、部分装载/表、末组/PP复位和末MAC故障禁止发布。192窄口5414包、1024表项和192真实输出通过。

3. 实测周期，分清范围
96→24：正常core={cycles96}；128任务×12组，384输出。互斥分桶={dict((k, normal96[0][k]) for k in partition)}。
192→12：每片正常core={cycles192}，8片均相同；每片64任务×24组，192输出。互斥分桶={dict((k, normal192[0][k]) for k in partition)}。
192→96八片core算术合计={cycles192*8}。这是8次片内运行之和，不含片间图级调度、参数搬运和全局DDR写址。
原48→48保持3874拍。三者每片恰好36864 MAC，不能只看2146<3874就称整网加速；输出数分别192/384/768，归约长度不同。
正常96装载3915、导出385；192首片装载5415、后续5416、导出193；重装检查额外1拍来自TB启动校验，不是核变慢。
窄口端点记录={narrow}。raw pre/SiLU/post busy有重叠，不能相加代替core；数据搬运和主机节拍也不当DDR带宽。

4. 实际PH1P35MDG324-3、100MHz实现
本轮实际顶层PROFILE2：{resources['slice']['used']} Slice、{resources['dsp']['used']} DSP、{resources['eram']['used']} ERAM、42 I/O，含参数/特征缓存与窄口壳。
不含完整权重ROM、DDR、摄像头或HDMI。资源仅对应192→12分片，不是三种PROFILE同时集成或整个CNN。
全报告负端点并集内部失败={len(internal)}；寄存边界slack(ns)={dict((k, v['worst_slack_ns']) for k, v in checks.items())}。
外部及raw-reset仍有违例：{external}；没有新增例外或编造板级延迟。
全量报告含ignored/DSP/ERAM，四角点与覆盖={current['reports']['all_endpoints_include_ignored']['processes']}/{current['reports']['all_endpoints_include_ignored']['coverage']}。
actual RAM归属见memory_query/ram.rpt；相对旧48候选的10 ERAM不能不分形状直接称再省1块，输出缓存容量已改变。
实查ERAM为输入2、权重6、SiLU1；192字节片内输出映射为分布式RAM，distributed RAM LUT共400。
最紧内部max检查是recovery：reg_release_done→u_mac/add3.asr，扇出1635、net占94%，余量0.172ns。
最紧setup：reg_release_done→u_post/u_round/reg_quotient_compare[40].cea，扇出701，余量1.234ns。
这不表示旧48候选的0.017ns路径被通用修复；两者编译形状不同，最终共享图顶层必须再测。
严格RTL={gates['rtl']['errors']}、TB={gates['tests']['errors']}条，八项状态见strict_summary.json。原AST控制解析与格式/注释项保留，真实ModelSim/TD不替代严格门。
SYN-5025及dummy控制端诊断原样保存，未做完整逐pin生产签核。

5. 整网预算更新
把本次实测形状用于冻结图8个96/192输入PW的条件投影；18×32按40个4×4 tile计算（包含底部不足4行的片），不按36个整tile漏算。
上述8层条件core合计={sum(row['conditional_layer_core'] for row in projections)}；加原5层条件9042624，13层累计={total}。
100MHz/5FPS每帧20M拍，剩余{20000000-total}需容纳54卷积、DDR/ROM等待、非卷积和NMS。
只有前3层是旧测试参数完整张量RTL证据，其余均为小块/形状投影；未实现全图遍历、边缘裁写或全帧时序，因此这不是整网速度上下界或通过结论。

6. 与其他线的交接和下一步
本聊天已补深通道PW，不再自己开发另一套CSP/stride1 DW黄金值。
下一步承接qat_g10_csp_first_data_20261015_v1的12通道split/DW/PW/residual参考，按现有算术核最小适配，形成首个完整CSP残差块。
同时跟踪旧855使能与本轮1635复位分发的高扇出路径；不能通过复制核、随机反复布局或新增例外逃避资源/时序问题。
图级联调应接同一真实参数包、同一共享核和明确全局地址；板/DDR线另闭合写完成/读可见性，当前受控端点不能代替真实DDR。
需要改变算术核、II、数值、真实外设协议或例外时先提出单独决定；未训练、不改生产、不生成位流、不上板、不写Flash。

结论：本轮实际补齐了深通道PW的数值、周期和实际顶层证据，而非再扩校验探针。失败经过见失败记录.txt，旧版本可回退。
"""
    (ROOT / "阶段报告与下一步.txt").write_text(text, encoding="utf-8")
    files = [p for p in ROOT.rglob("*") if p.is_file() and "work" not in p.relative_to(ROOT).parts and "__pycache__" not in p.parts]
    save(ROOT / "artifact_manifest.json", {str(p.relative_to(ROOT)): sha(p) for p in files if p.name != "artifact_manifest.json"})


if __name__ == "__main__":
    actions = {"setup": setup, "review": review, "simulate": simulate, "specifications": specifications,
               "tb_specifications": tb_specifications, "memory": memory, "finalize": finalize}
    actions.update({name: getattr(tools, name) for name in ("check", "dependency", "gate", "physical")})
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=actions)
    action = parser.parse_args().action
    try:
        actions[action]()
    except Exception as error:
        failure = fresh("failure")
        previous = json.loads((ROOT / "status.json").read_text(encoding="utf-8")) if (ROOT / "status.json").exists() else {}
        save(failure / "receipt.json", {"action": action, "error": repr(error), "previous_status": previous})
        save(ROOT / "status.json", {"status": "ACTION_FAILED", "action": action, "error": repr(error),
             "failure_record": str(failure), "production_delivery_ready": False})
        raise
