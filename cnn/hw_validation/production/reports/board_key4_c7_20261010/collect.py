"""TD保存工程会重写.al；只允许该容器变化，逐项核对实际源列表与器件。"""
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
import run


if __name__ == "__main__":
    inputs = json.loads((run.ROOT / "inputs.json").read_text(encoding="utf-8"))
    changed = [p for p, sha in inputs.items() if run.digest(p) != sha]
    project_path = run.WORK / "road_board_selftest_top.al"
    assert changed == [str(project_path)], changed
    parse = lambda path: ET.fromstring(path.read_text(encoding="utf-8").replace("UsedInP&R", "UsedInP&amp;R"))
    actual = parse(project_path)
    old = parse(run.OLD / "physical_attempt2/road_board_selftest_top.al")
    def sources(tree, directory):
        result = []
        for entry in tree.findall(".//Source_Files//File"):
            path = run.Path(entry.attrib["Path"])
            path = path if path.is_absolute() else directory / path
            result.append((str(path.resolve()), sorted((a.attrib["Name"], a.attrib["Val"]) for a in entry.findall(".//Attr"))))
        return result
    assert sources(actual, run.WORK) == sources(old, run.OLD / "physical_attempt2")
    for field in ("Name", "HardWare/Family", "HardWare/Device", "HardWare/Speed", "TOP_MODULE/LABEL", "TOP_MODULE/MODULE"):
        assert actual.findtext(field) == old.findtext(field), field
    run.save("project_rewrite_check.json", {"changed_input": changed, "unchanged_other_inputs": len(inputs) - 1, "effective_sources_attributes_device_and_top_match": True, "reason": "TD close_project重写工程容器；原始输入哈希未覆盖，所有源与约束哈希保持一致", "current_project_sha256": run.digest(project_path)})
    sys.path.insert(0, str(run.OLD))
    spec = importlib.util.spec_from_file_location("frozen_evidence", run.OLD / "evidence.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = ("all_endpoints.timing", "internal_reg_to_reg.timing", "compute_reset_sync.timing", "pixel_reset_sync.timing", "compute_reset_distribution.timing", "hdmi_reset_distribution.timing", "dsp_inputs.timing", "dsp_outputs.timing", "eram_inputs.timing", "eram_outputs.timing")
    result = {name: module.paths(run.WORK / name) for name in names}
    assert set(result["all_endpoints.timing"]["worst"]) == {"setup", "hold", "recovery", "removal"}
    run.save("timing_checks.json", result)
    netlist = (run.WORK / "gate_netlist.v").read_text(encoding="utf-8")
    run.save("primitives.json", {"dsp": len(re.findall(r"^  PH1P_PHY_DSPSIOU_V2\s", netlist, re.M)), "eram": len(re.findall(r"^  PH1P_PHY_ERAM_V2\s", netlist, re.M))})
    run.check_old("old_final")
    run.save("outputs.json", {str(p): run.digest(p) for p in run.WORK.iterdir() if p.is_file()})
    print(json.dumps({"worst": {k: v["slack_ns"] for k, v in result["all_endpoints.timing"]["worst"].items()}, "checks": result["all_endpoints.timing"]["reported_checks"]}, ensure_ascii=False))
