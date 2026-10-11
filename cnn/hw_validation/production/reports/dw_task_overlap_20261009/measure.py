"""复用冻结测量器，比较相同 DW/PW 端点，不累加重叠忙周期。"""
import importlib.util
import json
from pathlib import Path
from run import ROOT, BASE, tools, frozen, save

spec = importlib.util.spec_from_file_location("frozen_measure", BASE / "analyze.py")
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)


def main(work):
    work.resolve().relative_to(ROOT)
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["all_passed"]
    assert all(tools.digest(Path(name)) == sha for name, sha in receipt["sources"].items())
    result = {"simulation": str(work), "sets": {}, "parameter_origin": "TEST_NOT_QAT"}
    for name in receipt["results"]:
        trace = measure.rows(work / (name + "_trace.csv"))
        summary = measure.rows(work / (name + ".csv"))
        assert [r["case"] for r in summary] == list(range(16))
        windows = {r["case"]: r for r in measure.rows(work / (name + "_windows.csv"))}
        cases = {}
        for row in summary:
            data = [r for r in trace if r["case"] == row["case"]]
            assert [r["cycle"] for r in data] == list(range(1, row["endpoint"] + 1))
            boundary = next(i for i, r in enumerate(data) if r["layer"])
            assert data[boundary-1]["state"] == 4 and data[boundary]["state"] == 1
            assert all(data[i][key] == 0 for i in (boundary-1, boundary) for key in
                       ("mac_reserved", "mac_queued", "ingress", "retire", "meta", "active_valid", "task_meta_count"))
            assert data[boundary]["dw_writes"] == 256 and data[-1]["pw_writes"] == 384
            assert all(r["mac_reserved"] == r["task_meta_count"] for r in data)
            layers = {key: measure.layer_profile([r for r in data if r["layer"] == flag])
                      for flag, key in enumerate(("dw", "pw"))}
            assert layers["dw"]["cycles"] + layers["pw"]["cycles"] == row["endpoint"]
            if row["case"] < 3:
                assert layers["dw"]["cycles"] < 2015 and layers["pw"]["cycles"] == 592
            cases[str(row["case"])] = {**layers, "windows": windows[row["case"]],
                "dw_active_cycles": sum(r["active_valid"] for r in data if not r["layer"]),
                "dw_issue_and_retire_same_cycle": sum(r["mac_accept"] and r["pp_accept"]
                                                      for r in data if not r["layer"])}
        result["sets"][name] = cases
    base = result["sets"]["fixed_original"]["0"]
    result["comparison"] = {"baseline": {"dw": 2015, "pw": 592, "total": 2607},
        "candidate": {"dw": base["dw"]["cycles"], "pw": base["pw"]["cycles"], "total": base["windows"]["core"]}}
    save(ROOT / "analysis.json", result)
    sample = [r for r in measure.rows(work / "fixed_original_trace.csv") if r["case"] == 0 and r["cycle"] <= 36]
    wave = [{"name": "clk", "wave": "p" + "." * 35}]
    for field in ("mac_accept", "mac_last", "mac_result_accept", "pp_accept", "active_valid", "commit_accept"):
        wave.append({"name": field, "wave": "".join(str(r[field]) for r in sample)})
    save(ROOT / "dw_task_overlap.wave.json", {"signal": wave, "head": {"tick": 1,
        "text": "Observed DW overlap cycles 1 to 36 before NBA"}})
    print(json.dumps({"cases_verified": sum(len(v) for v in result["sets"].values()),
                      "comparison": result["comparison"]}, ensure_ascii=False))


if __name__ == "__main__":
    import sys
    frozen()
    try:
        main(Path(sys.argv[1]).resolve())
    finally:
        frozen()
