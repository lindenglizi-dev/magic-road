"""只读取冻结 TD 文本报告，分类实际路径；不修改 RTL 或约束。"""
import hashlib
import json
from pathlib import Path
import re


def paths(text):
    records = []
    for match in re.finditer(r"^Slack\s+: ([+-]?[\d.]+)ns\s*$", text, re.M):
        block = text[match.start():]
        end = re.search(r"^Slack\s+: ", block[1:], re.M)
        if end:
            block = block[:end.start() + 1]
        record = {"slack_ns": float(match[1])}
        for label, key in [("Begin Point", "begin"), ("End Point", "end"),
                           ("Check Type", "check"), ("Process", "corner"),
                           ("Data Path Delay", "data_delay"),
                           ("Clock Skew", "clock_skew"), ("Logic Level", "logic_level"),
                           ("Max Fanout", "max_fanout")]:
            value = re.search(r"^" + label + r"\s+: (.+)$", block, re.M)
            record[key] = value[1].strip() if value else None
        if not record["check"]:
            continue
        record["dut_touched"] = "silu_shared_unit_Inst_stage/" in block
        records.append(record)
    return records


def self_check():
    sample = "Slack : 0.054ns\nBegin Point : a.clk\nEnd Point : b.d\nCheck Type : hold\nProcess : fast_m40c\n"
    assert paths(sample)[0]["check"] == "hold"
    assert len(paths(sample + sample.replace("0.054", "-0.010"))) == 2
    assert min(r["slack_ns"] for r in paths(sample + sample.replace("0.054", "-0.010"))) == -0.010
    assert paths("STA coverage : 99.92%") == []


if __name__ == "__main__":
    self_check()
    root = Path(__file__).resolve().parent
    td = root.parent / "physical" / "td"
    output = {"scope": "existing routed reports only; no new implementation", "reports": {}}
    production = root.parents[2]
    frozen = production / "reports" / "v3_silu_stall_candidate_20261005" / "silu_shared_unit.v"
    digest = hashlib.sha256(frozen.read_bytes()).hexdigest()
    assert digest == "5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938"
    assert hashlib.sha256((td / "pr.db").read_bytes()).hexdigest() == "e92f620dfb966141bb04ce95dd6318655311b4053fec1200cf42111acb2067ef"
    output["frozen_dut_sha256"] = digest
    for name in ["all_paths_full.timing", "internal_reg_to_reg_full.timing", "reset_to_regs_full.timing"]:
        source = td / name
        data = source.read_bytes()
        records = paths(data.decode("utf-8", errors="replace"))
        assert records, f"No detailed paths in {name}"
        by_check = {}
        for check in sorted({r["check"] for r in records}):
            selected = [r for r in records if r["check"] == check]
            touched = [r for r in selected if r["dut_touched"]]
            by_check[check] = {"reported_paths": len(selected),
                               "worst": min(selected, key=lambda r: r["slack_ns"]),
                               "dut_touched_worst": min(touched, key=lambda r: r["slack_ns"]) if touched else None}
        output["reports"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "checks": by_check}
    assert output["reports"]["all_paths_full.timing"]["checks"]["setup"]["worst"]["end"].startswith("o_result_count")
    (root / "path_audit.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inputs = [frozen, td / "pr.db", td / "probe.sdc", Path(__file__).resolve()]
    mac = production.parent / "mac"
    inputs.extend(mac / name for name in ["road_mac_probe.v", "road_mac_stream_probe.v", "tb_road_mac_stream_probe.v", "mac_vectors.txt", "test_mac_reference.py", "test_mac_stream_reference.py"])
    inputs.extend(td / name for name in output["reports"])
    manifest = {"date": "2026-10-06 Asia/Shanghai", "files": [
        {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in inputs]}
    (root / "input_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))
