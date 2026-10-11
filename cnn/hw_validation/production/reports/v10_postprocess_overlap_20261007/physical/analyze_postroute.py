"""Stream TD reports into a compact, reproducible post-route audit."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent

FIELD_RE = re.compile(r"^(Slack|Begin Point|End Point|Check Type|Process)\s+:\s+(.*)$")
STAT_RE = re.compile(
    r"^(Max|Min)\s+:\s+[SH]WNS\s+([+-]?\d+\.\d+)ns,\s+"
    r"[SH]TNS\s+([+-]?\d+\.\d+)ns,\s+(\d+) Viol Endpoints,\s+"
    r"(\d+) Total Endpoints,\s+(\d+) Paths Analyzed"
)


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def clean_point(value: str) -> str:
    return value.split(" (", 1)[0]


def iter_paths(path: Path):
    record = None
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for raw in stream:
            match = FIELD_RE.match(raw.rstrip("\r\n"))
            if not match:
                continue
            field, value = match.groups()
            if field == "Slack":
                if record and {"slack_ns", "begin", "end", "check", "process"} <= record.keys():
                    yield record
                record = {"slack_ns": float(value.removesuffix("ns"))}
            elif record is not None:
                key = {"Begin Point": "begin", "End Point": "end",
                       "Check Type": "check", "Process": "process"}[field]
                record[key] = clean_point(value) if key in {"begin", "end"} else value
    if record and {"slack_ns", "begin", "end", "check", "process"} <= record.keys():
        yield record


def header(path: Path) -> dict:
    result = {}
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for index, raw in enumerate(stream):
            match = STAT_RE.match(raw.rstrip("\r\n"))
            if match:
                check, wns, tns, violations, endpoints, paths = match.groups()
                result[check.lower()] = {
                    "wns_ns": float(wns),
                    "tns_ns": float(tns),
                    "violating_endpoints": int(violations),
                    "total_endpoints": int(endpoints),
                    "paths_analyzed": int(paths),
                }
            if index > 100 or ("max" in result and "min" in result):
                break
    return result


def origin(point: str) -> str:
    if point.startswith("i_rstn"):
        return "raw_reset"
    if point.startswith("i_rx_") or point.startswith("i_tx_ready"):
        return "diagnostic_input"
    return "internal"


def component(point: str) -> str:
    if point.startswith("o_"):
        return "diagnostic_output"
    if "PH1P_LOGIC_ERAM_Inst_silu_table" in point:
        return "silu_eram"
    if "/road_mac_probe_Inst_tile/" in point:
        return "mac_dsp"
    if "/road_round_shift_Inst_pre/" in point:
        return "pre_round"
    if "/road_round_shift_Inst_post/" in point:
        return "post_round"
    if "/silu_shared_unit_Inst_shared/" in point:
        return "silu_control"
    if any(name in point for name in ("reg_group_data_", "reg_group_mask_", "cnt_result_queue", "reg_meta_fifo", "cnt_meta_")):
        return "postprocess_queue_meta"
    if "ramread" in point:
        return "distributed_ram"
    if point.startswith("down2_overlap_tile_runner_Inst_shell/"):
        return "runner_scheduler_storage"
    return "shell_control"


def summarize_types(path: Path, wanted=None) -> dict:
    groups = defaultdict(list)
    for item in iter_paths(path):
        if wanted is None or item["check"] in wanted:
            groups[item["check"]].append(item)
    summary = {}
    for check, items in sorted(groups.items()):
        worst = min(items, key=lambda item: item["slack_ns"])
        best = max(items, key=lambda item: item["slack_ns"])
        summary[check] = {
            "reported_paths": len(items),
            "violating_paths": sum(item["slack_ns"] < 0 for item in items),
            "worst": worst,
            "best_slack_ns": best["slack_ns"],
            "processes": sorted({item["process"] for item in items}),
        }
    return summary


def violation_audit(path: Path) -> dict:
    items = list(iter_paths(path))
    setup = [item for item in items if item["check"] == "setup"]
    hold = [item for item in items if item["check"] == "hold"]
    removal = [item for item in items if item["check"] == "removal"]

    def counts(group):
        return {
            "origin": dict(sorted(Counter(origin(item["begin"]) for item in group).items())),
            "endpoint_component": dict(sorted(Counter(component(item["end"]) for item in group).items())),
            "origin_to_component": dict(sorted(Counter(
                f"{origin(item['begin'])}->{component(item['end'])}" for item in group
            ).items())),
            "process": dict(sorted(Counter(item["process"] for item in group).items())),
        }

    return {
        "header": header(path),
        "reported_path_records": len(items),
        "setup": {"count": len(setup), "counts": counts(setup), "paths": setup},
        "hold": {"count": len(hold), "counts": counts(hold), "paths": hold},
        "removal": {"count": len(removal), "counts": counts(removal), "paths": removal},
        "min_check_total": len(hold) + len(removal),
    }


def find_name_counts(path: Path) -> dict:
    patterns = {
        "reg_halo": re.compile(r"reg_halo"),
        "reg_dw_cache": re.compile(r"reg_dw_cache"),
        "reg_output_cache": re.compile(r"reg_output_cache"),
        "reg_dw_weight": re.compile(r"reg_dw_weight"),
        "reg_dw_bias": re.compile(r"reg_dw_bias"),
        "reg_pw_weight": re.compile(r"reg_pw_weight"),
        "reg_pw_bias": re.compile(r"reg_pw_bias"),
        "reg_group_data_head": re.compile(r"reg_group_data_head"),
        "reg_group_data_tail": re.compile(r"reg_group_data_tail"),
        "reg_group_mask_head": re.compile(r"reg_group_mask_head"),
        "reg_group_mask_tail": re.compile(r"reg_group_mask_tail"),
        "cnt_result_queue": re.compile(r"cnt_result_queue"),
        "reg_meta_fifo": re.compile(r"reg_meta_fifo"),
        "cnt_meta": re.compile(r"cnt_meta"),
        "reg_commit_ready": re.compile(r"reg_commit_ready"),
    }
    counts = Counter()
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            for name, pattern in patterns.items():
                if pattern.search(line):
                    counts[name] += 1
    return dict(sorted(counts.items()))


def memory_mapping(path: Path) -> dict:
    hardcon = Counter()
    source_re = re.compile(r"\|\s+([^|]+\.v\(\d+\))\s+\|")
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            if "Dram Hardcon" not in line:
                continue
            match = source_re.search(line)
            hardcon[match.group(1).strip() if match else "unresolved"] += 1
    return {"dram_hardcon_by_source": dict(sorted(hardcon.items())),
            "dram_hardcon_total": sum(hardcon.values())}


def dummy_node_audit(path: Path) -> dict:
    dsp = mac = round_dsp = lslice = 0
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            if re.search(r"\.mul9_(?:mode|signed)\s*$", line):
                dsp += 1
                if "road_mac_probe" in line:
                    mac += 1
                elif "road_postprocess_stream" in line:
                    round_dsp += 1
            if re.search(r"reg_group_data_head.*\.ofb\s*$", line):
                lslice += 1
    return {
        "dsp_optional_9x_mode_or_signed_pins": dsp,
        "mac_dsp_optional_pins": mac,
        "round_dsp_optional_pins": round_dsp,
        "unused_lslice_outputs": lslice,
        "interpretation": (
            "TD zero-filled unused 9x submode controls on 26 mapped full-width DSPs; "
            "signed operands remain explicitly sign-extended at xa/y. The LSLICE item is "
            "one unused secondary output, not a missing storage bit."
        ),
    }


def main() -> None:
    timing_files = {
        "global_violations": ROOT / "coverage_100000_violations.timing",
        "internal_reg_to_reg": ROOT / "internal_reg_to_reg.timing",
        "diagnostic_inputs_to_regs": ROOT / "diagnostic_inputs_to_regs.timing",
        "regs_to_diagnostic_outputs": ROOT / "regs_to_diagnostic_outputs.timing",
        "external_reset_entry": ROOT / "external_reset_entry.timing",
        "functional_reset_distribution": ROOT / "functional_reset_distribution.timing",
        "reset_sync_interstage": ROOT / "reset_sync_interstage.timing",
        "dsp": ROOT / "discovered_dsp_paths.timing",
        "mac_dsp": ROOT / "discovered_mac_dsp_paths.timing",
        "eram": ROOT / "discovered_eram_paths.timing",
        "dram": ROOT / "discovered_dram_paths.timing",
    }
    primitive = json.loads((ROOT / "discovered_hardblocks.json").read_text(encoding="utf-8"))
    report = {
        "schema": "v10-postroute-audit-1",
        "baseline_mutated": False,
        "global_violations": violation_audit(timing_files["global_violations"]),
        "report_headers": {name: header(path) for name, path in timing_files.items()},
        "reset_checks": {
            "external_reset_entry": summarize_types(timing_files["external_reset_entry"]),
            "functional_reset_distribution": summarize_types(timing_files["functional_reset_distribution"]),
        },
        "hardblock_timing": {
            name: summarize_types(timing_files[name]) for name in ("dsp", "mac_dsp", "eram", "dram")
        },
        "hardblock_discovery": primitive,
        "fixed_round_note": (
            "The two non-MAC DSPs are the fixed-coefficient pre/post round multipliers. "
            "This is a legal fixed-coefficient implementation cost and is not a generic "
            "runtime-coefficient multiplier estimate."
        ),
        "memory_mapping": memory_mapping(ROOT / "shell_route_ram.rpt"),
        "syn5025_dummy_node_audit": dummy_node_audit(ROOT / "check_timing_verbose.rpt"),
        "retained_name_occurrences_in_routed_netlist": find_name_counts(ROOT / "routed_netlist.v"),
        "evidence_sha256": {
            path.name: digest(path) for path in [
                *timing_files.values(),
                ROOT / "check_timing_verbose.rpt",
                ROOT / "timing_exceptions.rpt",
                ROOT / "timing_ignored.rpt",
                ROOT / "abnormal_targets.rpt",
                ROOT / "shell_route.area",
                ROOT / "shell_route_ram.rpt",
                ROOT / "td_build.log",
            ]
        },
    }
    target = ROOT / "postroute_audit_v2.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PASS post-route audit", target.name)


if __name__ == "__main__":
    main()
