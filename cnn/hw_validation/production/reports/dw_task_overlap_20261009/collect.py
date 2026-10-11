"""收集本候选的实际资源与路径；外部路径不混入内部签核。"""
from collections import Counter
import json
from math import ceil
from pathlib import Path
import re
from run import ROOT, MAC, tools, frozen, save

PATH = re.compile(r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
                  r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)\s+Process\s+:\s+(\w+)")


def paths(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    return [{"slack_ns": float(slack), "begin": begin.split()[0], "end": end.split()[0],
             "kind": kind, "corner": corner,
             "external": begin.startswith("i_") or end.startswith("o_")}
            for slack, begin, end, kind, corner in PATH.findall(text)]


def summarize(path):
    records = paths(path)
    groups = {}
    for scope in ("internal", "external"):
        selected = [p for p in records if p["external"] == (scope == "external")]
        groups[scope] = {"paths": len(selected), "negative": dict(Counter(
            p["kind"] for p in selected if p["slack_ns"] < 0)), "checks": {}}
        for kind in sorted({p["kind"] for p in selected}):
            group = [p for p in selected if p["kind"] == kind]
            groups[scope]["checks"][kind] = {"count": len(group),
                "worst": min(group, key=lambda p: p["slack_ns"]),
                "corners": sorted({p["corner"] for p in group})}
    return groups


def main():
    physical = Path(json.loads((ROOT / "physical_current.json").read_text(encoding="utf-8"))["work"])
    manifest = json.loads((physical / "input_manifest.json").read_text(encoding="utf-8"))
    assert all(tools.digest(Path(name)) == sha for name, sha in manifest.items())
    area = (physical / "shell_route.area").read_text(encoding="utf-8")
    resource = {key: int(re.search(r"^#" + key + r"\s+(\d+)", area, re.M).group(1))
                for key in ("IO", "slice", "reg", "lut6", "dsp", "eram")}
    report_names = ("coverage_100000_all_paths", "coverage_100000_violations", "internal_reg_to_reg",
        "external_reset_entry", "reset_sync_interstage", "functional_reset_distribution",
        "dsp_all", "eram_all", "dsp_inputs_all", "eram_inputs_all")
    reports = {name: summarize(physical / (name + ".timing")) for name in report_names}
    all_text = (physical / "coverage_100000_all_paths.timing").read_text(encoding="utf-8")
    assert "Routed" in all_text and "Both (Slow and Fast)" in all_text
    coverage = re.search(r"STA coverage\s+:\s+([\d.]+)%", all_text).group(1)
    negative = [p for p in paths(physical / "coverage_100000_violations.timing") if p["slack_ns"] < 0]
    result = {"physical": str(physical), "resources_including_shell": resource,
        "sta_reported_coverage_percent": float(coverage), "reports": reports,
        "negative_paths": negative, "internal_negative_count": sum(not p["external"] for p in negative),
        "external_contract_signed_off": False, "production_delivery": False,
        "constraint_sha256": tools.digest(physical / "shell.sdc"),
        "sdc_unchanged": tools.digest(physical / "shell.sdc") == tools.digest(MAC / "physical_opt/shell.sdc"),
        "source_manifest": manifest}
    assert result["sdc_unchanged"]
    save(ROOT / "physical_analysis.json", result)
    old = json.loads((MAC / "layer_budget.json").read_text(encoding="utf-8"))
    graph_path = Path(old["graph"])
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    assert tools.digest(graph_path) == old["graph_sha256"]
    analysis = json.loads((ROOT / "analysis.json").read_text(encoding="utf-8"))
    measured = analysis["comparison"]["candidate"]
    rows = []
    for row in old["rows"]:
        row = dict(row)
        row["measurement_scope"] = "UNMEASURED_KEEP_PREVIOUS_OPTIMISTIC_FLOOR"
        if row["layer"] in ("down2.dw.conv", "down2.pw.conv"):
            node = next(n for n in graph["nodes"] if n["name"] == row["layer"])
            height, width, _ = node["output_shape_hwc"]
            tiles = ceil(height / 4) * ceil(width / 4)
            row.update(measurement_scope="MEASURED_4x4_TILE_TEST_PARAMETERS_PROJECTION",
                tile_count=tiles, measured_tile_cycles=measured[row["kind"]],
                projected_core_cycles=tiles * measured[row["kind"]])
        rows.append(row)
    assert len(rows) == 67 and sum("measured_tile_cycles" in row for row in rows) == 2
    save(ROOT / "layer_budget.json", {"graph": str(graph_path), "graph_sha256": tools.digest(graph_path),
        "rows": rows, "previous_optimistic_floor_sum_unchanged": old["sum"],
        "measured_down2": measured, "budget_5fps_cycles": 20000000,
        "not_full_network_cycle_simulation": True,
        "exclusions": ["DDR/ROM traffic and waiting", "non-convolution operators and full graph scheduling",
            "real QAT parameters and activation-dependent faults", "cross-tile reuse or overlap not implemented"],
        "interpretation": "Do not sum two measured tile projections with65 optimistic floors and call it measured FPS."})
    print(json.dumps({"resources": resource, "internal_negative": result["internal_negative_count"],
        "negative_checks": dict(Counter(p["kind"] for p in negative)), "coverage": coverage}))


if __name__ == "__main__":
    frozen()
    try:
        main()
    finally:
        frozen()
