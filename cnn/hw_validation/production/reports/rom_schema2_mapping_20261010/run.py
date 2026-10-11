"""schema2 ROM 独立诊断：复用原ROM、工具助手和已核查的厂商源。"""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
HW = ROOT.parents[2]
ROM = HW / "rom"
PACKAGE = ROOT.parents[1] / "numeric_artifacts"
PRIOR = ROOT.parent / "mac_ce_fanout_local_20261010"
CHECKER = ROOT.parent / "checker_fact_closure_20261009"
TOP = "road_yolo_numeric_rom_probe"
MSIM = Path("D:/modeltech64_2020.4/win64")
spec = importlib.util.spec_from_file_location("existing_tools", ROOT.parent / "runtime_layer_integration_20261009/run_candidate.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
digest = tools.digest


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def frozen():
    path = ROOT / "frozen.json"
    if not path.exists():
        sources = [p for base in (ROM, PACKAGE, PRIOR / "rtl", PRIOR / "physical", CHECKER / "checker_overlay",
                    tools.SKILL / "scripts", tools.SKILL / "config", tools.SKILL / "assets")
            for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts
            and "work" not in p.parts and (base in (ROM, PACKAGE) or p.suffix in (".v", ".py", ".json", ".sdc", ".adc", ".tcl"))]
        sources += [Path(tools.__file__), tools.TD, MSIM / "vlib.exe", MSIM / "vlog.exe", MSIM / "vsim.exe",
            HW / "interfaces/ph1p_eram_interface_complete.v", HW / "interfaces/complete_provenance.json"]
        source_receipt = json.loads((ROOT.parent / "mac_task_stream_20261009/candidate_attempt4/receipt.json").read_text(encoding="utf-8"))
        sources += [Path(name) for name in source_receipt["sources"] if "sim_release" in name]
        save(path, {str(p): digest(p) for p in sources})
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = [name for name, sha in records.items() if digest(Path(name)) != sha]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def prepare():
    assert not (ROOT / "rtl").exists()
    for name in ("baseline", "rtl", "tests", "interfaces"):
        (ROOT / name).mkdir()
    for path in (ROM / "road_yolo_numeric_rom_group.v", ROM / (TOP + ".v")):
        for target in ("baseline", "rtl"):
            shutil.copyfile(path, ROOT / target / path.name)
    shutil.copyfile(ROM / ("tb_" + TOP + ".v"), ROOT / "tests" / ("tb_" + TOP + ".v"))
    shutil.copytree(ROM / "spec", ROOT / "spec")
    shutil.copyfile(HW / "interfaces/ph1p_eram_interface_complete.v", ROOT / "interfaces/ph1p_eram_interface_complete.v")
    shutil.copytree(PACKAGE, ROOT / "artifacts")
    package_check()
    work = tools.fresh("preflight")
    output = tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings", tools.SKILL / "config/defaults.json"],
        work, "dependencies", allowed=(0, 1))
    dependency = json.loads(output[output.index("{"):])
    assert dependency["required_ok"]
    save(ROOT / "status.json", {"stage": "prepared_schema2_test", "deployment_release": False})


def package_check():
    manifest = json.loads((ROOT / "artifacts/manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 2 and manifest["payload_bytes"] == 140522
    payload = (ROOT / "artifacts/numeric_test.bin").read_bytes()
    physical = (ROOT / "artifacts/numeric_test_padded.bin").read_bytes()
    assert digest(ROOT / "artifacts/numeric_test.bin") == manifest["payload_sha256"]
    assert digest(ROOT / "artifacts/numeric_test_padded.bin") == manifest["physical_sha256"]
    import zlib
    assert f"{zlib.crc32(physical):08x}" == manifest["physical_crc32"] == "1bbd0dce"
    words = [int(line, 16).to_bytes(20, "little") for line in (ROOT / "artifacts/words.dath").read_text().splitlines()]
    assert len(words) == 7168 and b"".join(words) == physical
    for group in range(14):
        lanes = [[int(line, 16).to_bytes(5, "little") for line in
            (ROOT / f"artifacts/group_{group:02d}_lane_{lane}.dath").read_text().splitlines()] for lane in range(4)]
        assert all(len(lane) == 512 for lane in lanes)
        assert all(b"".join(lane[index] for lane in lanes) == words[group * 512 + index] for index in range(512))
    assert physical[:len(payload)] == payload and physical[len(payload):] == bytes(2838)
    save(ROOT / "package_check.json", {"schema": 2, "payload_bytes": len(payload), "physical_bytes": len(physical),
        "crc32": "1bbd0dce", "payload_sha256": manifest["payload_sha256"], "all_lanes_reconstructed": True,
        "status": "TEST_NOT_QAT", "manifest_sha256": digest(ROOT / "artifacts/manifest.json")})


def gate(label):
    work = tools.fresh("gate_" + label)
    overlay = CHECKER / "checker_overlay" if label != "original" else ROOT.parents[1] / "checker_overlay"
    target = ROOT / ("baseline" if label in ("baseline", "original") else "tests" if label == "testbench" else "rtl")
    entry = (f"import sys;sys.path[:0]=[{str(overlay)!r},{str(tools.SKILL)!r}];"
        "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    args = [sys.executable, "-B", "-X", "utf8", "-c", entry, target,
        "--external-interface-source", ROOT / "interfaces/ph1p_eram_interface_complete.v",
        "--json", work / "gate.json", "--markdown", work / "gate.md"]
    if label == "testbench":
        args.append("--include-testbench")
    tools.command(args, work, "gate", timeout=600, allowed=(0, 1))
    result = json.loads((work / "gate.json").read_text(encoding="utf-8"))
    save(ROOT / ("gate_" + label + "_current.json"), {"work": str(work)})
    print("GATE", label, result["errors"], result["strict_warnings"], result["delivery_ready"], flush=True)
    assert result["checks"]["compile"]["status"] == "passed"
    assert result["checks"]["compile"]["parse_errors"] == 0


def review():
    for source in (ROOT / "baseline").glob("*.v"):
        work = tools.fresh("review_" + source.stem)
        entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
            "from scripts.python.workflow.cli import main;raise SystemExit(main())")
        tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target", source,
            "--report-json", work / "review.json"], work, "review", allowed=(0, 1, 2))
        assert (work / "review.json").exists()
    for label in ("original", "baseline"):
        gate(label)


def scope():
    records = {}
    for source in (ROOT / "rtl").glob("*.v"):
        assert source.read_bytes() == (ROOT / "baseline" / source.name).read_bytes()
        assert source.read_bytes() == (ROM / source.name).read_bytes()
        records[str(source)] = digest(source)
    assert len(records) == 2
    save(ROOT / "scope_check.json", {"rtl_byte_identical": True, "sources": records,
        "only_binding_change": "artifacts resolves to frozen schema2 package in each new workdir",
        "old_package_and_sources_unchanged": True, "io_bits": 35, "new_timing_exceptions": False})


def work_artifacts(work):
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    assert digest(work / "artifacts/manifest.json") == digest(PACKAGE / "manifest.json")


def simulate(mapped=False):
    scope()
    package_check()
    work = tools.fresh("mapped_simulation" if mapped else "vendor_simulation")
    work_artifacts(work)
    source_receipt = json.loads((ROOT.parent / "mac_task_stream_20261009/candidate_attempt4/receipt.json").read_text(encoding="utf-8"))
    sources = [Path(name) for name in source_receipt["sources"] if "sim_release" in name]
    if mapped:
        syn = Path(json.loads((ROOT / "synthesis_current.json").read_text())["work"])
        sources.append(syn / "gate_netlist.v")
    else:
        sources += sorted((ROOT / "rtl").glob("*.v"))
    sources.append(ROOT / "tests" / ("tb_" + TOP + ".v"))
    save(work / "input_manifest.json", {str(p): digest(p) for p in sources})
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    log = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_" + TOP,
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "vsim", timeout=1200)
    assert "PASS: 7168 words / 143360 bytes checked, CRC32=1bbd0dce" in log
    assert "Fatal:" not in log and "** Error:" not in log
    observed = [int(line, 16).to_bytes(20, "little") for line in (work / "observed_words.dath").read_text().splitlines()]
    actual = b"".join(observed)
    expected = (ROOT / "artifacts/numeric_test_padded.bin").read_bytes()
    assert len(observed) == 7168 and actual == expected
    manifest = json.loads((ROOT / "artifacts/manifest.json").read_text(encoding="utf-8"))
    field_key = "segments" if "segments" in manifest else "fields"
    fields = manifest[field_key]
    assert len(fields) == 393
    for field in fields:
        start = field["offset"]
        length = field.get("length", field.get("bytes"))
        assert actual[start:start + length] == expected[start:start + length]
    assert "RESET_RESTART_PASS" in log
    save(work / "receipt.json", {"all_passed": True, "vendor_model": True, "standin_used": False,
        "words": 7168, "bytes": len(actual), "fields": len(fields), "crc32": "1bbd0dce",
        "reset_restart_checked": "RESET_RESTART_PASS" in log, "mapped_netlist": mapped,
        "sdf_used": False, "sources": {str(p): digest(p) for p in sources},
        "package_sha256": digest(work / "artifacts/manifest.json"), "deployment_release": False})
    save(ROOT / ("mapped_simulation_current.json" if mapped else "simulation_current.json"), {"work": str(work)})
    print("VENDOR_ROM_PASS", len(observed), len(fields), flush=True)


def synth():
    scope()
    receipt = json.loads((Path(json.loads((ROOT / "simulation_current.json").read_text())["work"]) / "receipt.json").read_text())
    assert receipt["all_passed"] and receipt["vendor_model"]
    work = tools.fresh("synthesis")
    work_artifacts(work)
    # TD resolves INIT_FILE against the RTL directory; ModelSim uses its workdir.
    local_package = ROOT / "rtl/artifacts"
    if not local_package.exists():
        shutil.copytree(ROOT / "artifacts", local_package)
    assert all(digest(local_package / p.name) == digest(p) for p in (ROOT / "artifacts").iterdir() if p.is_file())
    sources = sorted((ROOT / "rtl").glob("*.v"))
    name = tools.project(work, "layer_shell", sources)
    content = (work / name).read_text(encoding="utf-8")
    for tag in ("LABEL", "MODULE"):
        content = content.replace(f"<{tag}>road_dynamic_overlap_low_io_top</{tag}>", f"<{tag}>{TOP}</{tag}>")
    (work / name).write_text(content, encoding="utf-8")
    shutil.copyfile(ROOT / "synth.tcl", work / "synth.tcl")
    shutil.copyfile(ROOT / "rom.sdc", work / "rom.sdc")
    save(work / "input_manifest.json", {str(p): digest(p) for p in sources})
    log = tools.command([tools.TD, "synth.tcl"], work, "td", timeout=1200)
    assert "ROM_SYNTH_DONE" in log and "ERROR:" not in log
    assert "ROM_ERAM_COUNT 56" in log
    area = (work / "rom_gate.area").read_text()
    assert re.search(r"^#eram\s+56\s", area, re.M) and re.search(r"^#dsp\s+0\s", area, re.M)
    save(ROOT / "synthesis_current.json", {"work": str(work)})
    print("ROM_SYNTHESIS_COLLECT_NEXT", work, flush=True)


def physical():
    scope()
    mapped = Path(json.loads((ROOT / "mapped_readback_current.json").read_text())["work"])
    assert json.loads((mapped / "receipt.json").read_text())["all_passed"]
    syn = Path(json.loads((ROOT / "synthesis_current.json").read_text())["work"])
    log = (syn / "td.log").read_text(encoding="utf-8")
    assert "ROM_ERAM_COUNT 56" in log and "UNDRIVEN_RECORD" not in log
    work = tools.fresh("physical")
    for name in ("gate.db", "road_dynamic_overlap_low_io_top.al"):
        shutil.copyfile(syn / name, work / name)
    for name in ("rom.sdc", "physical.tcl"):
        shutil.copyfile(ROOT / name, work / name)
    save(work / "input_manifest.json", {str(p): digest(p) for p in
        [syn / "gate.db", ROOT / "rom.sdc", ROOT / "physical.tcl", syn / "gate_netlist.v"]})
    log = tools.command([tools.TD, "physical.tcl"], work, "td", timeout=1800)
    assert "ROM_PHYSICAL_DONE" in log and "ERROR:" not in log
    assert "ROM_IMPORTED_CLOCK probe_clk" in log
    assert "STA coverage        : 100.00%" in (work / "final_timing.rpt").read_text()
    save(ROOT / "physical_current.json", {"work": str(work)})
    print("ROM_PHYSICAL_COLLECT_NEXT", work, flush=True)


def continuous():
    scope()
    work = tools.fresh("continuous_physical")
    work_artifacts(work)
    name = tools.project(work, "layer_shell", sorted((ROOT / "rtl").glob("*.v")))
    content = (work / name).read_text()
    for tag in ("LABEL", "MODULE"):
        content = content.replace(f"<{tag}>road_dynamic_overlap_low_io_top</{tag}>", f"<{tag}>{TOP}</{tag}>")
    (work / name).write_text(content, encoding="utf-8")
    shutil.copyfile(ROOT / "rom.sdc", work / "rom.sdc")
    synthesis = (ROOT / "synth.tcl").read_text().replace("close_project", "")
    implementation = "\n".join(line for line in (ROOT / "physical.tcl").read_text().splitlines()
        if not line.startswith(("import_device ", "import_db ")))
    (work / "build.tcl").write_text(synthesis + "\n" + implementation, encoding="utf-8")
    save(work / "input_manifest.json", {str(p): digest(p) for p in [*sorted((ROOT / "rtl").glob("*.v")),
        ROOT / "rom.sdc", work / "build.tcl", work / name, ROOT / "run.py"]})
    log = tools.command([tools.TD, "build.tcl"], work, "td", timeout=1800)
    assert "ROM_SYNTH_DONE" in log and "ROM_PHYSICAL_DONE" in log and "ERROR:" not in log
    assert "ROM_ERAM_COUNT 56" in log and "ROM_IMPORTED_CLOCK probe_clk" in log
    assert "STA coverage        : 100.00%" in (work / "final_timing.rpt").read_text()
    save(ROOT / "continuous_current.json", {"work": str(work)})
    print("CONTINUOUS_ROM_COLLECT_NEXT", work, flush=True)


def mapped_readback():
    scope()
    syn = Path(json.loads((ROOT / "synthesis_current.json").read_text())["work"])
    netlist = syn / "gate_netlist.v"
    work = tools.fresh("mapped_readback")
    work_artifacts(work)
    source = (ROOT / "rtl" / (TOP + ".v")).read_text()
    groups = {name: int(re.search(r"group_(\d+)_lane_0", params)[1]) for params, name in
        re.findall(r"road_yolo_numeric_rom_group\s*#\((.*?)\)\s*(\w+)\s*\(", source, re.S)}
    assert len(groups) == 14
    instances = re.findall(r"PH1P_PHY_ERAM_V2\s*#\((.*?)\)\s*\\(\S+)\s*\((.*?)\);",
        netlist.read_text(), re.S)
    assert len(instances) == 56
    parts, binding = [], []
    for params, name, ports in instances:
        group, primitive = name.split("/")
        lane_name = re.fullmatch(r"PH1P_LOGIC_ERAM_Inst_(alpha|beta|gamma|delta)_syn_1", primitive)[1]
        index = groups[group] * 4 + ("alpha", "beta", "gamma", "delta").index(lane_name)
        assert len(re.findall(r"\.INIT(?:P)?_[0-9A-F]{2}\(256'h[0-9A-F]+\)", params)) == 80
        assert set(re.findall(r"\.(\w+)\(", ports)) == {"addra", "addrb", "clka", "clkb", "dia", "dib",
            "dia_extra", "dib_extra", "doa", "dob", "doa_extra", "dob_extra"}
        original_ports = ports
        ports = re.sub(r"\\(\S+)/lane_(\w+)_data\s+", lambda m: f"lane_{index} ", ports)
        assert "lane_" in ports and "/lane_" not in ports
        parts.append(f"wire [39:0] lane_{index};\nassign observed[{index * 40} +: 40] = lane_{index};\n"
            f"PH1P_PHY_ERAM_V2 #( {params} ) \\{name} ( {ports} );\n")
        binding.append({"instance": name, "lane_index": index, "parameters": params, "original_ports": original_ports})
    assert sorted(row["lane_index"] for row in binding) == list(range(56))
    # Generated test harness only, not a replacement DUT or synthesis source.
    (work / "native_instances.vh").write_text("\n".join(parts), encoding="utf-8")
    save(work / "extraction.json", {"source": str(netlist), "sha256": digest(netlist), "instances": binding,
        "parameter_blocks_unchanged": True, "scope": "physical memory contents and read ports; excludes CRC/mux controller"})
    source_receipt = json.loads((ROOT.parent / "mac_task_stream_20261009/candidate_attempt4/receipt.json").read_text())
    sources = [Path(name) for name in source_receipt["sources"] if "sim_release" in name]
    sources.append(ROOT / "tests/tb_mapped_rom_readback.v")
    save(work / "input_manifest.json", {str(p): digest(p) for p in sources + [netlist, work / "native_instances.vh"]})
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    log = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_mapped_rom_readback",
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "vsim", timeout=300)
    assert "NATIVE_ROM_PASS" in log and "Fatal:" not in log and "** Error:" not in log
    records = {}
    for line in (work / "native_readback.txt").read_text().splitlines():
        lane, addr, value = line.split()
        key = int(lane), int(addr)
        assert key not in records
        records[key] = int(value, 16).to_bytes(5, "little")
    assert len(records) == 56 * 512
    actual = b"".join(records[group * 4 + lane, addr] for group in range(14) for addr in range(512) for lane in range(4))
    assert actual == (ROOT / "artifacts/numeric_test_padded.bin").read_bytes()
    save(work / "receipt.json", {"all_passed": True, "erams": 56, "addresses_each": 512, "bytes": len(actual),
        "vendor_model": True, "physical_parameters_from_td": True, "whole_mapped_control_regression": False,
        "sdf_used": False, "netlist_sha256": digest(netlist)})
    save(ROOT / "mapped_readback_current.json", {"work": str(work)})
    print("NATIVE_ROM_READBACK_PASS", len(actual), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "scope", "gate_candidate", "gate_testbench", "simulate", "mapped_sim", "mapped_readback", "synth", "physical", "continuous"))
    stage = parser.parse_args().stage
    frozen()
    try:
        if stage.startswith("gate_"):
            gate(stage[5:])
        elif stage == "mapped_sim":
            simulate(mapped=True)
        else:
            globals()[stage]()
    except Exception as error:
        work = tools.fresh(stage + "_failure")
        save(work / "receipt.json", {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        frozen()
