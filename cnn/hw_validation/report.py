"""Record reproducible software checks and honest first-batch evidence boundaries."""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from baseline import PROJECT, ROOT, digest, save_json, verify

SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")


def check(name, command, cwd):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    log = ROOT / "reports" / (name + ".log")
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    return {"command": command, "cwd": str(cwd), "exit_code": result.returncode,
            "log": str(log.relative_to(ROOT)), "sha256": digest(log)}


def baseline_result():
    build = ROOT / "baseline"
    area = build / "template_route.area"
    timing = build / "template_route.timing"
    bit = build / "hw_video_baseline.bit"
    result = {"routed_report_present": area.exists() and timing.exists(),
              "bitstream_present": bit.exists(), "board_10min": "not_measured",
              "jtag_recovery": "not_measured", "physical_board_identity": "unverified",
              "board_available": False,
              "board_blocker": "User confirmed board is not currently in their possession",
              "usb_inventory_scope": "Computer connected-device list only, not board memory readback"}
    logs = sorted(build.glob("td_*.log"))
    if logs:
        log = logs[-1]
        content = log.read_text(encoding="utf-8", errors="replace")
        result["tool_log"] = str(log.relative_to(ROOT))
        result["tool_log_sha256"] = digest(log)
        result["bitgen_completed_in_log"] = 'finish command "bitgen -bit hw_video_baseline.bit"' in content
        result["tool_error_lines"] = [line for line in content.splitlines()
                                      if re.search(r"\bERROR\b|invalid command name|couldn't", line, re.I)]
    if area.exists():
        text = area.read_text(encoding="utf-8", errors="replace")
        result["resources"] = {key: int(re.search(r"^#" + name + r"\s+(\d+)",
                                                   text, re.M).group(1))
                               for key, name in (("slice", "slice"), ("dsp", "dsp"),
                                                 ("eram", "eram"))}
        result["area_sha256"] = digest(area)
    if timing.exists():
        text = timing.read_text(encoding="utf-8", errors="replace")
        result["timing_ns"] = {key: float(re.search(key + r":\s*([-\d.]+)ns", text).group(1))
                               for key in ("SWNS", "STNS", "HWNS", "HTNS")}
        result["sta_coverage_percent"] = float(re.search(r"STA coverage\s*:\s*([\d.]+)%", text).group(1))
        result["timing_sha256"] = digest(timing)
    if bit.exists():
        result["bitstream_bytes"] = bit.stat().st_size
        result["bitstream_sha256"] = digest(bit)
    return result


def probe_result(name):
    directory = ROOT / name
    sources = {path.name: digest(path) for path in directory.glob("*.v")}
    gates = sorted(list(directory.rglob("*gate*.json")) + list(directory.rglob("final_readiness.json")),
                   key=lambda path: path.stat().st_mtime)
    result = {"source_hashes": sources, "physical_board_test": "not_measured",
              "gate_binding": "Work-in-progress snapshot; old gate results do not automatically validate later source edits"}
    if gates:
        latest = gates[-1]
        gate = json.loads(latest.read_text(encoding="utf-8"))
        result.update(gate_report=str(latest.relative_to(ROOT)),
                      gate_report_sha256=digest(latest),
                      gate_scope=gate.get("root"),
                      delivery_ready=gate.get("delivery_ready"),
                      errors=gate.get("errors"),
                      public_gates={key: value.get("status")
                                    for key, value in gate.get("checks", {}).items()})
    else:
        result["strict_gate"] = "no_report_yet"
    return result


def component_td_result(directory):
    """Keep elaboration, physical mapping and bit generation distinct."""
    result = {"directory": str(directory.relative_to(ROOT)),
              "scope": "isolated component, never full CNN or board acceptance"}
    logs = sorted(directory.glob("td_*.log"))
    if not logs:
        return dict(result, status="not_run")
    log = logs[-1]
    text = log.read_text(encoding="utf-8", errors="replace")
    errors = [line for line in text.splitlines()
              if re.search(r"\bERROR\b|Oops!|invalid command name|couldn't", line, re.I)]
    result.update(log=str(log.relative_to(ROOT)), log_sha256=digest(log), errors=errors)
    areas = sorted(directory.glob("*.area"))
    result["area_reports"] = {path.name: digest(path) for path in areas}
    route = directory / "probe_route.area"
    timing = directory / "probe_route.timing"
    result["routed"] = route.exists() and timing.exists() and not errors
    if route.exists():
        area_text = route.read_text(encoding="utf-8", errors="replace")
        result["physical_resources"] = {}
        for resource in ("slice", "dsp", "eram"):
            match = re.search(r"^#" + resource + r"\s+(\d+)", area_text, re.M | re.I)
            result["physical_resources"][resource] = int(match.group(1)) if match else None
    if timing.exists():
        timing_text = timing.read_text(encoding="utf-8", errors="replace")
        result["timing_ns"] = {}
        for key in ("SWNS", "STNS", "HWNS", "HTNS"):
            match = re.search(key + r":\s*([-\d.]+)ns", timing_text)
            result["timing_ns"][key] = float(match.group(1)) if match else None
        match = re.search(r"STA coverage\s*:\s*([\d.]+)%", timing_text)
        result["sta_coverage_percent"] = float(match.group(1)) if match else None
    result["bitstreams"] = {path.name: digest(path) for path in directory.glob("*.bit")}
    result["status"] = "tool_failed" if errors else "routed" if result["routed"] else "partial"
    return result


def main():
    (ROOT / "reports").mkdir(exist_ok=True)
    python = [sys.executable, "-B", "-X", "utf8"]
    checks = {
        "baseline_self_check": check("baseline_self_check", python + [str(ROOT / "baseline.py"), "self-check"], PROJECT),
        "integer_contract": check("integer_contract", python + ["-m", "unittest", "cnn.test_integer"], PROJECT),
        "numeric_scalar": check("numeric_scalar", python + [str(ROOT / "numeric_selfcheck.py")], PROJECT),
        "interface_extractor": check("interface_extractor", python + [str(ROOT / "interfaces_extract.py"), "--self-check"], PROJECT),
        "mac_stream_numeric": check("mac_stream_numeric", python + [str(ROOT / "mac/run_mac_stream_probe.py")], PROJECT),
        "local_preflight": check("local_preflight", python + ["-m", "scripts.python.toolchain.preflight_verilog_toolchain",
                                "--settings", str(ROOT / "settings.json"), "--readiness", "execute"], SKILL),
        "dependencies": check("dependencies", python + ["-m", "scripts.python.toolchain.manage_skill_dependencies",
                              "check", "--settings", str(ROOT / "settings.json")], SKILL),
        "usb_inventory": check("usb_inventory", ["pnputil.exe", "/enum-devices", "/connected", "/class", "USB"], PROJECT),
    }
    dependency_info = json.loads((ROOT / "reports/dependencies.log").read_text(encoding="utf-8"))
    verify()
    interface_source = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_eram.v")
    interface_bundle = ROOT / "interfaces/ph1p_eram_interface.v"
    if interface_bundle.exists():
        save_json(ROOT / "interfaces/provenance.json", {
            "source": str(interface_source), "source_sha256": digest(interface_source),
            "interface": str(interface_bundle), "interface_sha256": digest(interface_bundle),
            "module_whitelist": ["PH1P_LOGIC_ERAM"],
            "extractor": "scripts.python.quality.external_interface_stubs extract",
            "boundary": "Only static parameter/port declarations, not simulation/synthesis/behavior evidence"})
    summary = {"utc": datetime.now(timezone.utc).isoformat(),
               "scope": "H0/H1 and small H2 probes; software/static evidence is not board acceptance",
               "checks": checks, "h0": baseline_result(),
               "required_dependencies_ok": dependency_info.get("required_ok"),
               "missing_required_tools": dependency_info.get("missing_required_tools"),
               "missing_recommended": dependency_info.get("missing_recommended"),
               "production_unchanged": True,
               "h1_a": "See rom evidence; physical mapping and board checksum separately required",
               "h1_b": "Controlled endpoint only; vendor commit/fence and physical DDR unproven",
               "h2": "Small MAC only; requant/SiLU/tile/whole-layer/5FPS not accepted",
               "probe_snapshot": {name: probe_result(name) for name in ("rom", "ddr", "mac")},
               "mac_core_receipt": json.loads((ROOT / "mac/status.json").read_text(encoding="utf-8")),
               "complete_vendor_interface": json.loads((ROOT / "interfaces/complete_provenance.json").read_text(encoding="utf-8")),
               "component_td": {directory.name: component_td_result(directory)
                                for directory in (ROOT / "td").iterdir() if directory.is_dir()},
               "h3_h4": "not_started",
               "full_cnn_deployment": {"ready": False, "full_67_layer_rtl": False,
                                       "cnn_bitstream_present": False, "fps_verified": False},
               "legacy_gate": "Historical template has strict style failures; TD evidence is separate",
               "no_flash_no_training": True}
    save_json(ROOT / "reports/first_batch.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
