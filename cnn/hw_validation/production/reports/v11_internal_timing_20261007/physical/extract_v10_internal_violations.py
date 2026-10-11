"""Extract the seven non-I/O setup failures from the frozen v10 STA report."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V10 = ROOT.parents[1] / "v10_postprocess_overlap_20261007" / "physical"
SOURCE = V10 / "coverage_100000_violations.timing"


def value(block, label):
    match = re.search(rf"^{re.escape(label)}\s+:\s+(.+)$", block, re.MULTILINE)
    if not match:
        raise ValueError(f"missing {label}")
    return match.group(1).strip()


def point(block, label):
    return value(block, label).split(" (", 1)[0]


def cone(block):
    data = block.split("clk2q", 1)[1].split("Arrival", 1)[0]
    cells = []
    nets = []
    sources = []
    for line in data.splitlines():
        cell = re.match(r"^([A-Z][A-Z0-9]*(?: \(reg\))?)\s+\S+.*?pin:\s+(\S+)", line)
        if cell:
            cells.append({"type": cell.group(1), "pin": cell.group(2)})
        net = re.search(r"net:\s+([^,]+),\s+(.+\.v\(\d+\)|NOFILE\(0\))", line)
        if net:
            nets.append({"name": net.group(1).strip(), "source": net.group(2).strip()})
            if net.group(2) != "NOFILE(0)" and net.group(2) not in sources:
                sources.append(net.group(2))
    return {"cells": cells, "nets": nets, "sources": sources}


def main():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    starts = [match.start() for match in re.finditer(r"^Slack\s+:\s+", text, re.MULTILINE)]
    starts.append(len(text))
    paths = []
    for index in range(len(starts) - 1):
        block = text[starts[index]:starts[index + 1]]
        if value(block, "Check Type") != "setup":
            continue
        end = point(block, "End Point")
        if end.startswith("o_"):
            continue
        paths.append({
            "rank": len(paths) + 1,
            "slack_ns": float(value(block, "Slack").removesuffix("ns")),
            "begin": point(block, "Begin Point"),
            "end": end,
            "process": value(block, "Process"),
            "budget": value(block, "Budget"),
            "data_path_delay": value(block, "Data Path Delay"),
            "clock_skew": value(block, "Clock Skew"),
            "logic_level": value(block, "Logic Level"),
            "max_fanout": int(value(block, "Max Fanout")),
            "cone": cone(block),
        })
    if len(paths) != 7:
        raise SystemExit(f"expected 7 internal setup paths, found {len(paths)}")

    payload = {
        "schema": "v11-v10-internal-setup-extraction-1",
        "source": str(SOURCE),
        "classification": "global setup violations excluding top-level output endpoints",
        "count": len(paths),
        "paths": paths,
    }
    (ROOT / "v10_internal_setup_paths.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Frozen v10 internal setup failures",
        "",
        "Extracted from `coverage_100000_violations.timing`; top-level output endpoints are excluded.",
        "",
        "| Rank | Slack | Begin | End | Data path | Logic |",
        "|---:|---:|---|---|---|---|",
    ]
    for item in paths:
        lines.append(
            f"| {item['rank']} | {item['slack_ns']:.3f} ns | `{item['begin']}` | "
            f"`{item['end']}` | {item['data_path_delay']} | {item['logic_level']} |"
        )
    for item in paths:
        lines.extend(["", f"## Path {item['rank']}: {item['slack_ns']:.3f} ns", "",
                      f"- Begin: `{item['begin']}`", f"- End: `{item['end']}`",
                      f"- Corner: `{item['process']}`", f"- Budget: {item['budget']}",
                      f"- Data delay: {item['data_path_delay']}",
                      f"- Clock skew: {item['clock_skew']}",
                      f"- Logic: {item['logic_level']}",
                      f"- Max fanout: {item['max_fanout']}",
                      "- Source cone:"])
        for source in item["cone"]["sources"]:
            lines.append(f"  - `{source}`")
        lines.append("- Routed cell sequence:")
        for cell in item["cone"]["cells"]:
            lines.append(f"  - `{cell['type']}` → `{cell['pin']}`")
    (ROOT / "v10_internal_setup_paths.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS extracted 7 internal setup paths")


if __name__ == "__main__":
    main()
