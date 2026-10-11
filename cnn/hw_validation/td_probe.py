"""Prepare isolated component TD runs only after strict RTL delivery approval.

This is a component mapping/timing probe, never a full-CNN acceptance claim.
The explicit local Anlogic route is user-approved; no programming command exists.
"""
import argparse
import json
import re
from pathlib import Path

from baseline import ROOT, digest, save_json, verify


def require_gate(gate):
    required = ("compile", "ast", "readability", "comment", "naming", "profile")
    passed = all(gate.get("checks", {}).get(key, {}).get("status") == "passed"
                 for key in required)
    if (gate.get("strict") is not True or not gate.get("delivery_ready") or
            gate.get("errors") != 0 or gate.get("strict_warnings") != 0 or not passed):
        raise ValueError("Strict RTL gate failed: TD run remains blocked; no waiver applied")


def rom_inputs():
    paths = [ROOT / "rom/road_yolo_numeric_rom_group.v",
             ROOT / "rom/road_yolo_numeric_rom_probe.v"]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    return paths


def require_binding(gate_root, binding, original_hashes, staged_hashes):
    if Path(binding.get("gate_root", "")).resolve() != gate_root:
        raise ValueError("Gate root and source binding disagree")
    if binding.get("sources") != original_hashes or staged_hashes != original_hashes:
        raise ValueError("Approved source closure changed or contains unexpected RTL")


def write_project(build, name, top, sources):
    # TD's native file has required run/configuration nodes and literal '&'.
    # Reuse the proven baseline envelope instead of inventing a partial schema.
    template = ROOT / "baseline/hw_video_baseline.al"
    text = template.read_text(encoding="utf-8")
    entries = "\n".join(
        f'<File Path="{path.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/>'
        '<Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/>'
        f'<Attr Name="CompileOrder" Val="{index}"/></FileInfo></File>'
        for index, path in enumerate(sources, 1))
    text = re.sub(r'<Source_Files>.*?</Source_Files>',
                  '<Source_Files><Verilog>' + entries + '</Verilog></Source_Files>',
                  text, count=1, flags=re.S)
    text = text.replace((ROOT / "baseline").as_posix(), build.as_posix())
    text = text.replace('<Name>hw_video_baseline</Name>', f'<Name>{name}</Name>')
    text = text.replace('design_top_wrapper', top)
    if re.findall(r'<File Path="([^"]+)"', text) != [path.as_posix() for path in sources]:
        raise ValueError("Native project source closure does not match approved RTL")
    (build / (name + '.al')).write_text(text, encoding="utf-8")


def prepare(gate_path, binding_path, component="rom"):
    verify()
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    require_gate(gate)
    sources = rom_inputs() if component == "rom" else [
        ROOT / "mac/road_mac_probe.v", ROOT / "mac/road_mac_stream_probe.v"]
    gate_root = Path(gate["root"]).resolve()
    # Gate only the two production modules; testbenches are checked separately.
    # The approved staging copy and original RTL must both match the receipt.
    if not gate_root.is_dir() or not gate_root.is_relative_to(ROOT.resolve()):
        raise ValueError("Gate must cover an isolated production closure in this workspace")
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    original_hashes = {path.name: digest(path) for path in sources}
    staged_hashes = {path.name: digest(path) for path in gate_root.rglob("*.v")}
    require_binding(gate_root, binding, original_hashes, staged_hashes)
    if any(path.stat().st_mtime_ns > gate_path.stat().st_mtime_ns
           for path in gate_root.rglob("*.v")):
        raise ValueError("Staged RTL was modified after its gate report")
    # Validate all initialization paths before publishing any build input.
    initializers = []
    if component == "rom":
        manifest = json.loads((ROOT / "rom/artifacts/manifest.json").read_text(encoding="utf-8"))
        if not manifest:
            raise ValueError("ROM package manifest is absent")
        initializers = re.findall(r'"(artifacts/[^"\r\n]+\.dath)"', sources[1].read_text(encoding="utf-8"))
        if len(set(initializers)) != 56:
            raise ValueError("Expected 56 distinct relative lane initialization files")
    for relative in initializers:
        if not (ROOT / "rom" / relative).is_file():
            raise FileNotFoundError(relative)
    build = ROOT / "td" / component
    build.mkdir(parents=True, exist_ok=True)
    name = "rom_storage_probe" if component == "rom" else "mac_compute_probe"
    top = "road_yolo_numeric_rom_probe" if component == "rom" else "road_mac_stream_probe"
    project_path = build / (name + ".al")
    if project_path.exists():
        raise FileExistsError("Preserving previous TD run; use its frozen inputs")
    write_project(build, name, top, sources)
    # The ROM INIT_FILE paths must resolve without rewriting approved RTL.
    (build / "probe.adc").write_text(
        "set_pin_assignment { i_clk } { LOCATION = C4; IOSTANDARD = LVCMOS33; PULLTYPE = PULLUP; }\n"
        "set_pin_assignment { i_rstn } { LOCATION = R10; IOSTANDARD = LVCMOS33; PULLTYPE = PULLUP; }\n",
        encoding="utf-8")
    inputs = "i_rstn" if component == "rom" else "i_rstn i_command_valid i_command_opcode[*] i_command_index[*] i_command_data[*] i_result_ready"
    outputs = "o_done o_checksum[*]" if component == "rom" else "o_command_ready o_result_valid o_result_data[*] o_fault"
    (build / "probe.sdc").write_text(
        "create_clock -name {probe_clk} -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]\n"
        f"set_input_delay -clock [get_clocks {{probe_clk}}] -max 0.000 [get_ports {{{inputs}}}]\n"
        f"set_input_delay -clock [get_clocks {{probe_clk}}] -min 0.000 [get_ports {{{inputs}}}]\n"
        f"set_output_delay -clock [get_clocks {{probe_clk}}] -max 0.000 [get_ports {{{outputs}}}]\n"
        f"set_output_delay -clock [get_clocks {{probe_clk}}] -min 0.000 [get_ports {{{outputs}}}]\n",
        encoding="utf-8")
    (build / "build.tcl").write_text(
        "import_device ph1_35p.db -package PH1P35MDG324 -speed 3\n"
        f"open_project {name}.al -single_run\n"
        f"elaborate -top {top}\nread_adc probe.adc\nread_sdc probe.sdc\n"
        "optimize_rtl\nreport_area -file probe_rtl.area\noptimize_gate\n"
        "legalize_phy_inst\nupdate_timing\nplace\nroute\n"
        "report_area -io_info -file probe_route.area\nupdate_timing -mode final\n"
        "report_timing_status -file probe_route.ts\nreport_timing_summary -file probe_route.timing\n",
        encoding="utf-8")
    frozen = {str(path.relative_to(ROOT)): digest(path) for path in sources}
    frozen.update({"rom/" + relative: digest(ROOT / "rom" / relative) for relative in initializers})
    save_json(build / "inputs.json", {"gate": str(gate_path), "gate_sha256": digest(gate_path),
              "source_binding": str(binding_path), "source_binding_sha256": digest(binding_path),
              "source_and_init_sha256": frozen, "constraint_period_ns": 10,
              "artifact_kind": component + " component only, not full CNN",
              "need_artifacts_junction": str(ROOT / "rom/artifacts") if initializers else None,
              "board_download_allowed": False,
              "timing_boundary": "100MHz offline target, no board clock or external IO timing acceptance"}, True)
    print("Prepared " + str(build) + ("; create artifacts junction before TD" if initializers else ""))


def prepare_mac_synthesis():
    """Measure the approved core first, without pretending its wide IO can route."""
    verify()
    source = ROOT / "mac/road_mac_probe.v"
    status_path = ROOT / "mac/status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    if digest(source) != status.get("artifact_sha256", {}).get(source.name):
        raise ValueError("MAC core differs from its numeric/static validation receipt")
    gate_path = ROOT / "mac" / status["strict_gate_report"]
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    require_gate(gate)
    if Path(gate["root"]).resolve() != source.resolve():
        raise ValueError("MAC gate does not cover the requested core")
    if not status.get("numeric_evidence", {}).get("iverilog_result", "").startswith(
            "VERILOG-GEN-RESULT PASS cases=1031 errors=0"):
        raise ValueError("MAC numeric test has not passed")
    build = ROOT / "td/mac_core_synthesis_v2"
    build.mkdir(parents=True, exist_ok=True)
    project_path = build / "mac_core_synthesis.al"
    if project_path.exists():
        raise FileExistsError("Preserving previous MAC synthesis inputs")
    write_project(build, "mac_core_synthesis", "road_mac_probe", [source])
    (build / "build.tcl").write_text(
        "import_device ph1_35p.db -package PH1P35MDG324 -speed 3\n"
        "open_project mac_core_synthesis.al -single_run\n"
        "elaborate -top road_mac_probe\noptimize_rtl\n"
        "report_area -file mac_core_rtl.area\noptimize_gate\n"
        "report_area -file mac_core_gate.area\n", encoding="utf-8")
    save_json(build / "inputs.json", {
        "gate": str(gate_path), "gate_sha256": digest(gate_path),
        "status_sha256": digest(status_path), "source_sha256": digest(source),
        "artifact_kind": "MAC core synthesis only; no placement, timing or bitstream",
        "reason": "Wide parallel core IO exceeds package pins; dynamic wrapper routes separately",
        "board_download_allowed": False}, True)
    print("Prepared " + str(build))


def prepare_round(hold_fix=False):
    """Route the numerically checked rounding primitive, not the whole CNN."""
    verify()
    source = ROOT / "production/round/road_round_shift.v"
    gate_path = source.parent / "gate_group_pass.json"
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    require_gate(gate)
    if (Path(gate["root"]).resolve() != source.resolve() or
            source.stat().st_mtime_ns > gate_path.stat().st_mtime_ns):
        raise ValueError("Rounding source is not covered by its current strict gate")
    report = json.loads((ROOT / "production/latest_report.json").read_text(encoding="utf-8"))
    numeric = json.loads(Path(report["report"]).read_text(encoding="utf-8"))
    if (not numeric["checks"]["round_sim"]["passed"] or
            numeric["source_sha256"].get("round/road_round_shift.v") != digest(source)):
        raise ValueError("Current rounding RTL lacks successful numeric simulation")
    build = ROOT / ("td/round_shift_hold_20261004" if hold_fix else "td/round_shift_20261004")
    build.mkdir(parents=True, exist_ok=True)
    if (build / "round_shift_probe.al").exists():
        raise FileExistsError("Preserving previous rounding TD inputs")
    write_project(build, "round_shift_probe", "road_round_shift", [source])
    (build / "probe.adc").write_text(
        "set_pin_assignment { i_clk } { LOCATION = C4; IOSTANDARD = LVCMOS33; PULLTYPE = PULLUP; }\n"
        "set_pin_assignment { i_rstn } { LOCATION = R10; IOSTANDARD = LVCMOS33; PULLTYPE = PULLUP; }\n",
        encoding="utf-8")
    inputs = "i_rstn i_advance i_input_valid i_product[*] i_shift[*] i_tag[*]"
    outputs = "o_result_valid o_result_data[*] o_result_tag[*] o_fault"
    (build / "probe.sdc").write_text(
        "create_clock -name {probe_clk} -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]\n"
        f"set_input_delay -clock [get_clocks {{probe_clk}}] -max 0.000 [get_ports {{{inputs}}}]\n"
        f"set_input_delay -clock [get_clocks {{probe_clk}}] -min 0.000 [get_ports {{{inputs}}}]\n"
        f"set_output_delay -clock [get_clocks {{probe_clk}}] -max 0.000 [get_ports {{{outputs}}}]\n"
        f"set_output_delay -clock [get_clocks {{probe_clk}}] -min 0.000 [get_ports {{{outputs}}}]\n",
        encoding="utf-8")
    (build / "build.tcl").write_text(
        "import_device ph1_35p.db -package PH1P35MDG324 -speed 3\n"
        "open_project round_shift_probe.al -single_run\nelaborate -top road_round_shift\n"
        "read_adc probe.adc\nread_sdc probe.sdc\noptimize_rtl\n"
        "report_area -file probe_rtl.area\noptimize_gate\nlegalize_phy_inst\n"
        "update_timing\nplace\nroute\n" + ("fix_hold\n" if hold_fix else "") +
        "report_area -io_info -file probe_route.area\n"
        "update_timing -mode final\nreport_timing_status -file probe_route.ts\n"
        "report_timing_summary -file probe_route.timing\n", encoding="utf-8")
    save_json(build / "inputs.json", {
        "source": str(source), "source_sha256": digest(source),
        "gate": str(gate_path), "gate_sha256": digest(gate_path),
        "numeric_report": report["report"], "numeric_report_sha256": digest(Path(report["report"])),
        "generated_inputs_sha256": {name: digest(build / name) for name in
                                   ("round_shift_probe.al", "probe.adc", "probe.sdc", "build.tcl")},
        "artifact_kind": "standalone rounding only; no multiplier, full CNN or video integration",
        "native_hold_repair": hold_fix,
        "timing_boundary": "100 MHz offline; zero external IO delays are a component fixture, not board acceptance",
        "board_download_allowed": False}, True)
    print("Prepared " + str(build))


def route_metrics(area, timing_status, timing):
    """Missing resource/timing evidence must never turn into a zero value."""
    resources = {}
    for name in ("slice", "dsp", "eram"):
        match = re.search(r"^#" + name + r"\s+(\d+)\s+out of\s+(\d+)", area, re.M)
        if not match:
            raise ValueError("Missing routed resource count: " + name)
        resources[name] = int(match[1])
    values = {}
    for name in ("SWNS", "STNS", "HWNS", "HTNS"):
        match = re.search(name + r":\s*([-+]?\d+\.\d+)ns", timing_status)
        if not match:
            raise ValueError("Missing routed timing value: " + name)
        values[name] = float(match[1])
    coverage = re.search(r"STA coverage\s*:\s*(\d+\.\d+)%", timing)
    if not coverage or "Confidence          : Routed" not in timing:
        raise ValueError("Missing final routed timing coverage")
    return {"resources": resources, "timing_ns": values,
            "sta_coverage_percent": float(coverage[1]),
            "setup_passed": values["SWNS"] >= 0 and values["STNS"] == 0,
            "hold_passed": values["HWNS"] >= 0 and values["HTNS"] == 0}


def report_round():
    """Keep both failed runs, bound to their unchanged RTL and constraints."""
    runs = []
    for name in ("round_shift_20261004", "round_shift_hold_20261004"):
        build = ROOT / "td" / name
        inputs = json.loads((build / "inputs.json").read_text(encoding="utf-8"))
        if (digest(Path(inputs["source"])) != inputs["source_sha256"] or
                digest(Path(inputs["gate"])) != inputs["gate_sha256"] or
                any(digest(build / file) != expected for file, expected in
                    inputs["generated_inputs_sha256"].items())):
            raise ValueError("TD input evidence changed: " + name)
        metrics = route_metrics((build / "probe_route.area").read_text(encoding="utf-8"),
                                (build / "probe_route.ts").read_text(encoding="utf-8"),
                                (build / "probe_route.timing").read_text(encoding="utf-8"))
        logs = list(build.glob("td_*.log"))
        if len(logs) != 1:
            raise ValueError("Expected exactly one frozen TD run log")
        log = logs[0].read_text(encoding="utf-8")
        native_hold_repair = inputs.get("native_hold_repair", False)
        if native_hold_repair and 'start command "fix_hold"' not in log:
            raise ValueError("Requested native hold repair did not execute")
        runs.append({"directory": str(build), **metrics,
                     "source_sha256": inputs["source_sha256"],
                     "sdc_sha256": digest(build / "probe.sdc"),
                     "native_hold_repair": native_hold_repair,
                     "board_safe": False,
                     "unassigned_io_warning": "has no user assigned specific location constraint" in log,
                     "evidence_sha256": {file.name: digest(file) for file in
                                          [build / "inputs.json", build / "probe_route.area",
                                           build / "probe_route.ts", build / "probe_route.timing", logs[0]]}})
    if len({run["sdc_sha256"] for run in runs}) != 1:
        raise ValueError("Hold comparison changed constraints")
    save_json(ROOT / "production/reports/round_td_20261004.json", {
        "status": "timing_failed" if any(not run["setup_passed"] or not run["hold_passed"]
                                         for run in runs) else "component_timing_passed",
        "scope": "standalone rounding only; no full CNN, video integration, safe board image or bitstream",
        "runs": runs,
        "remaining": "Verify real registered upstream/downstream and synchronized reset release; no timing waiver."}, True)
    print(json.dumps(runs, ensure_ascii=False, indent=2))


def self_check():
    good = {"strict": True, "delivery_ready": True, "errors": 0, "strict_warnings": 0,
            "checks": {key: {"status": "passed"} for key in
                       ("compile", "ast", "readability", "comment", "naming", "profile")}}
    require_gate(good)
    for field, value in (("strict", False), ("delivery_ready", False), ("errors", 1),
                         ("errors", None), ("strict_warnings", 1), ("strict_warnings", None)):
        bad = dict(good, **{field: value})
        try:
            require_gate(bad)
        except ValueError:
            continue
        raise AssertionError("Fail-closed gate rejected invalid input incorrectly")
    try:
        require_gate({"delivery_ready": True})
    except ValueError:
        pass
    else:
        raise AssertionError("Missing public evidence must not release TD")
    hashes = {"probe.v": "frozen-sha"}
    binding = {"gate_root": str(ROOT), "sources": hashes}
    require_binding(ROOT.resolve(), binding, hashes, hashes)
    for staged in ({"probe.v": "changed"}, {}, dict(hashes, unexpected="extra")):
        try:
            require_binding(ROOT.resolve(), binding, hashes, staged)
        except ValueError:
            continue
        raise AssertionError("Modified or incomplete source closure must not release TD")
    area = "#slice 867 out of 21216\n#dsp 0 out of 40\n#eram 0 out of 108\n"
    status = "SWNS: 1.419ns, STNS: 0.000ns.\nHWNS: -1.742ns, HTNS: -175.425ns."
    timing = "STA coverage : 100.00%\nConfidence          : Routed"
    measured = route_metrics(area, status, timing)
    assert measured["setup_passed"] and not measured["hold_passed"]
    for args in (("", status, timing), (area, "", timing), (area, status, "")):
        try:
            route_metrics(*args)
        except ValueError:
            continue
        raise AssertionError("Missing routed evidence must fail closed")
    print("PASS: failed/warned/missing gate and changed/incomplete source closure cannot release TD")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=Path)
    parser.add_argument("--binding", type=Path)
    parser.add_argument("--component", choices=("rom", "mac"), default="rom")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--mac-synthesis", action="store_true")
    parser.add_argument("--round", action="store_true")
    parser.add_argument("--round-hold-fix", action="store_true")
    parser.add_argument("--round-report", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
    elif args.mac_synthesis:
        prepare_mac_synthesis()
    elif args.round:
        prepare_round()
    elif args.round_hold_fix:
        prepare_round(hold_fix=True)
    elif args.round_report:
        report_round()
    elif args.gate and args.binding:
        prepare(args.gate.resolve(), args.binding.resolve(), args.component)
    else:
        parser.error("Specify --self-check or --gate with --binding")
