"""只读解析本次证据，写入本目录；不改RTL、门禁或任何旧报告。"""
from collections import Counter
import csv
import json
from pathlib import Path
import re

from run import ROOT, COMPUTE, ROM, check, digest, save


def current(label):
    path = Path(json.loads((ROOT / (label + "_current.json")).read_text(encoding="utf-8"))["work"])
    path.resolve().relative_to(ROOT)
    return path


def timing(path):
    pattern = re.compile(r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
                         r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)\s+Process\s+:\s+(\w+)")
    rows = [{"slack_ns": float(slack), "begin": begin.split()[0], "end": end.split()[0],
             "kind": kind, "corner": corner, "external": begin.startswith("i_") or end.startswith("o_")}
            for slack, begin, end, kind, corner in pattern.findall(path.read_text(encoding="utf-8", errors="replace"))]
    result = {}
    for scope in ("internal", "external"):
        result[scope] = {}
        for kind in ("setup", "hold", "recovery", "removal"):
            selected = [row for row in rows if row["kind"] == kind and row["external"] == (scope == "external")]
            failed = [row for row in selected if row["slack_ns"] < 0]
            result[scope][kind] = {"records": len(selected), "worst": min(selected, key=lambda row: row["slack_ns"]) if selected else None,
                "negative_records": len(failed), "unique_failed_endpoints": len({row["end"] for row in failed}),
                "corners": sorted({row["corner"] for row in selected})}
    return {"summary": result, "negative": [row for row in rows if row["slack_ns"] < 0]}


def rom_initialization(path):
    # Reuse frozen ROM collector's physical INIT extraction; exclude the separate SiLU RAM.
    rows = re.findall(r"PH1P_PHY_ERAM_V2\s*#\((.*?)\)\s*\\(\S+)\s*\((.*?)\);", path.read_text(), re.S)
    result = {}
    for parameters, name, _ in rows:
        if "road_yolo_numeric_rom_group_Inst_" not in name:
            continue
        key = "/".join(name.split("/")[-2:])
        values = dict(re.findall(r"\.(INIT(?:P)?_[0-9A-F]{2})\(256'h([0-9A-F]+)\)", parameters))
        assert len(values) == 80 and key not in result
        result[key] = values
    assert len(result) == 56, (path, len(result))
    return result


def main():
    images = list((ROOT / "artifacts").glob("group_*_lane_*.dath"))
    assert len(images) == 56
    image_hashes = {}
    for image in images:
        value = digest(image)
        assert value == digest(ROOT / "rtl/artifacts" / image.name) == digest(ROM / "artifacts" / image.name)
        image_hashes[image.name] = value
    receipts = {}
    for label in ("simulation", "regression", "reader", "prefetch"):
        directory = current(label)
        receipt = json.loads((directory / "receipt.json").read_text(encoding="utf-8"))
        assert receipt["all_passed"]
        assert all(digest(Path(source)) == value for source, value in receipt["sources"].items())
        receipts[label] = str(directory.relative_to(ROOT))
    cycles = list(csv.DictReader((current("simulation") / "cycles.csv").open(encoding="utf-8")))
    bins = ("commit_stall", "capacity_stall", "commit", "mac_issue", "issue_wait", "drain_other")
    assert all(sum(int(row[key]) for key in bins) == int(row["core"]) for row in cycles)
    copied = [row for row in json.loads((ROOT / "checkpoint_manifest.json").read_text(encoding="utf-8"))["files"]
              if Path(row["source"]).parent == COMPUTE / "rtl" and Path(row["source"]).suffix == ".v"]
    assert all(digest(ROOT / "rtl" / Path(row["source"]).name) == row["sha256"] for row in copied)
    gates = {}
    for label in ("full", "testbench"):
        data = json.loads((current("gate") / (label + ".json")).read_text(encoding="utf-8"))
        gates[label] = {"errors": data["errors"], "strict_warnings": data["strict_warnings"],
            "checks": {key: {field: value.get(field) for field in ("ready", "status", "errors", "parse_errors")}
                       for key, value in data["checks"].items()},
            "diagnostic_records_by_rule": dict(Counter(row.get("rule") for row in data["issues"])),
            "diagnostic_records_by_file": dict(Counter(re.sub(r":\d+$", "", str(row.get("path", ""))) for row in data["issues"]))}
    result = {"receipts": receipts, "same_frozen_compute_files": len(copied), "cycles": cycles,
        "rom_image_sha256_same_in_frozen_simulation_and_td": image_hashes,
        "strict_gates": gates, "physical": None, "trained_parameters": False,
        "crc_probe_in_joint_top": False, "external_signed_off": False, "full_network_fps_proven": False,
        "production_modified": False, "bitstream_generated": False, "board_or_flash": False}
    if (ROOT / "physical_current.json").exists():
        directory = current("physical")
        manifest = json.loads((directory / "input_manifest.json").read_text(encoding="utf-8"))
        assert all(digest(Path(source)) == value for source, value in manifest.items() if Path(source).suffix != ".al")
        projects = {}
        expected_sources = sorted(str(Path(source).resolve()) for source in manifest if Path(source).suffix == ".v")
        for source, before_hash in manifest.items():
            project = Path(source)
            if project.suffix != ".al":
                continue
            text = project.read_text(encoding="utf-8")
            actual_sources = sorted(str((project.parent / name).resolve()) for name in re.findall(r'<File Path="([^"]+)">', text))
            assert actual_sources == expected_sources
            assert '<MODULE>road_rom_down2_top</MODULE>' in text
            assert '<Device>PH1P35MDG324</Device>' in text and '<Speed>-3</Speed>' in text
            projects[source] = {"input_sha256": before_hash, "td_saved_sha256": digest(project),
                "same_11_source_bindings_top_and_device": True,
                "note": "TD重存工程文件并将绝对源码路径改写为相对路径；不是源码或约束哈希改变。"}
        area = (directory / "joint_route.area").read_text(encoding="utf-8")
        resources = {key: int(re.search(r"^#" + key + r"\s+(\d+)", area, re.M).group(1))
                     for key in ("IO", "slice", "reg", "lut6", "dsp", "eram")}
        reports = {name: timing(directory / (name + ".timing")) for name in
            ("all_paths", "internal", "external_reset", "eram_outputs", "eram_inputs", "dsp_outputs", "dsp_inputs")}
        full = (directory / "final_timing.rpt").read_text(encoding="utf-8")
        coverage = float(re.search(r"STA coverage\s+:\s+([\d.]+)%", full).group(1))
        assert "Routed" in full and "Both (Slow and Fast)" in full and coverage == 100.0
        netlist = (directory / "routed_netlist.v").read_text(encoding="utf-8", errors="replace")
        assert "crc" not in netlist.lower()
        init_values = rom_initialization(directory / "routed_netlist.v")
        assert init_values == rom_initialization(directory / "gate_netlist.v")
        assert init_values == rom_initialization(ROM / "continuous_physical/routed_netlist.v")
        log = (directory / "td.log").read_text(encoding="utf-8", errors="replace")
        result["physical"] = {"work": str(directory.relative_to(ROOT)), "resources_including_shell": resources,
            "sta_reported_coverage_percent": coverage, "reports": reports,
            "rom_init_parameters_same_as_validated_frozen_rom": 56 * 80,
            "synthesis_zeroing_warnings": [line for line in log.splitlines() if "SYN-5025" in line],
            "corner_boundary": "TD选择每条路径最差slow/fast角点；不等于每个角点独立全量签核",
            "input_manifest": manifest, "td_project_reserialization": projects,
            "routed_db_sha256": digest(directory / "pr.db")}
    save(ROOT / "result.json", result)
    print(json.dumps({"frozen_files": len(copied), "receipts": receipts, "resources":
        result["physical"]["resources_including_shell"] if result["physical"] else None}, ensure_ascii=False))


if __name__ == "__main__":
    check()
    try:
        main()
    finally:
        check()
