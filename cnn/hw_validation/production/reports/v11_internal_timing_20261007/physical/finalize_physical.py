"""Seal the single v11 implementation into compact status and review reports."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIELD_RE = re.compile(r"^(Slack|Begin Point|End Point|Check Type|Process)\s+:\s+(.*)$")


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def iter_paths(path: Path):
    record = None
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            match = FIELD_RE.match(raw.rstrip("\r\n"))
            if not match:
                continue
            field, value = match.groups()
            if field == "Slack":
                if record and {"slack_ns", "begin", "end", "check", "process"} <= record.keys():
                    yield record
                record = {"slack_ns": float(value.removesuffix("ns"))}
                continue
            if record is None:
                continue
            key = {"Begin Point": "begin", "End Point": "end",
                   "Check Type": "check", "Process": "process"}[field]
            record[key] = value.split(" (", 1)[0] if key in {"begin", "end"} else value
    if record and {"slack_ns", "begin", "end", "check", "process"} <= record.keys():
        yield record


def signature(end: str) -> str | None:
    match = re.search(r"road_round_shift_Inst_pre/reg_absolute_reg\[(29|31|33|34|35)\]", end)
    if match:
        return f"pre_round_absolute[{match.group(1)}]"
    if "cnt_output_reg[2]" in end:
        return "runner_cnt_output[2]"
    if "mult17_syn_57.xa[1]" in end:
        return "mac_mult17_xa[1]"
    return None


def full_coverage_old_seven(audit: dict) -> list[dict]:
    best: dict[str, dict] = {}
    for item in iter_paths(ROOT / "coverage_100000_all_paths.timing"):
        if item["check"] != "setup":
            continue
        name = signature(item["end"])
        if name is not None and (name not in best or item["slack_ns"] < best[name]["slack_ns"]):
            best[name] = item

    mapped = []
    for old in audit["baseline_internal_endpoint_map"]:
        current = best.get(old["signature"])
        mapped.append({
            "baseline_rank": old["baseline_rank"],
            "signature": old["signature"],
            "baseline_slack_ns": old["baseline_slack_ns"],
            "candidate": current,
            "status": ("PASS" if current and current["slack_ns"] >= 0 else
                       "FAIL" if current else "UNMAPPED"),
            "mapping_basis": "worst setup path in complete 100000-endpoint-cap all-path report for the same logical endpoint family",
        })
    return mapped


def source_hashes() -> dict[str, str]:
    paths = [
        "road_postprocess_low_io_top.v",
        "../rtl/down2_overlap_tile_runner.v",
        "../rtl/road_postprocess_stream.v",
        "../../v9_mac_stream_20261007/core/road_mac_probe.v",
        "../../v7_onchip_chain_20261006/inputs/road_round_shift.v",
        "../../v7_onchip_chain_20261006/inputs/silu_shared_unit.v",
    ]
    return {name: sha256((ROOT / name).resolve()) for name in paths}


def table(rows: list[list[object]], headings: list[str]) -> str:
    lines = ["| " + " | ".join(headings) + " |",
             "| " + " | ".join("---" for _ in headings) + " |"]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def main() -> None:
    original = json.loads((ROOT / "postroute_audit.json").read_text(encoding="utf-8"))
    audit = json.loads(json.dumps(original))
    audit["schema"] = "v11-postroute-audit-2"
    audit["supersedes_without_overwriting"] = "postroute_audit.json"
    audit["baseline_internal_endpoint_map"] = full_coverage_old_seven(audit)
    audit["syn5025_dummy_node_audit"]["interpretation"] = (
        "TD reports 52 unused optional mul9_mode/mul9_signed pins across the 26 full-width DSPs; "
        "24 MAC DSPs account for 48 and two fixed-round DSPs account for four. Signed operands "
        "remain explicitly sign-extended at xa/y. The named-storage unused-LSLICE count is zero."
    )
    audit["syn5025_dummy_node_audit"]["raw_other_dummy_node"] = (
        "PH1P_PHY_LSLICE _al_n1_syn_556.ofb is retained in raw check_timing output; it is anonymous "
        "and is not attributed to a queue, metadata, cache, or weight storage bit."
    )
    audit["evidence_sha256"]["coverage_100000_all_paths.timing"] = sha256(
        ROOT / "coverage_100000_all_paths.timing"
    )
    (ROOT / "postroute_audit_v2.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8"
    )

    setup = audit["global_violations"]["setup"]["paths"]
    internal_setup = [item for item in setup if not item["end"].startswith("o_")]
    external_setup = [item for item in setup if item["end"].startswith("o_")]
    old7_pass = all(item["status"] == "PASS" for item in audit["baseline_internal_endpoint_map"])
    status = {
        "schema": "v11-physical-status-1",
        "status": "FAIL_INTERNAL_SETUP_AND_DIAGNOSTIC_IO_TIMING",
        "build": {
            "tool": "Anlogic TD 6.2.1 Engineer 6.2.168.116",
            "device": "PH1P35MDG324",
            "speed_grade": "-3",
            "clock_mhz": 100,
            "single_place_route_seed": True,
            "bitstream_generated": False,
        },
        "functional_candidate": {
            "status": "PASS",
            "runner_no_stall_cycles": 5433,
            "standalone_latency_cycles": [24, 25],
            "cut_payload_hold_assertion": "PASS",
        },
        "resources": {
            "io": 38, "lut6": 8032, "registers": 6567, "slices": 8733,
            "logic_slices": 7509, "ram_slices": 1224, "dram_luts": 1160,
            "shifter_luts": 64, "eram": 1, "dsp": 26,
            "mac_dsp": 24, "fixed_round_dsp": 2,
        },
        "coverage": audit["report_headers"]["global_violations"],
        "timing": {
            "global_setup": audit["report_headers"]["global_violations"]["max"],
            "global_hold": audit["report_headers"]["global_violations"]["min"],
            "internal_reg_to_reg": audit["report_headers"]["internal_reg_to_reg"],
            "internal_setup_violations": internal_setup,
            "diagnostic_output_setup_violations": external_setup,
            "global_hold_classification": audit["global_violations"]["hold"]["counts"],
            "global_removal_violations": audit["global_violations"]["removal"],
            "global_recovery_violations": 0,
            "functional_reset_distribution": audit["reset_checks"]["functional_reset_distribution"],
            "hardblocks": audit["hardblock_timing"],
        },
        "old_v10_internal_seven": {
            "all_same_logical_endpoint_families_positive": old7_pass,
            "paths": audit["baseline_internal_endpoint_map"],
        },
        "constraints": {
            "false_paths": 0, "multicycle_paths": 0, "ignored_paths": 0,
            "diagnostic_io_max_min_ns": 0.0,
            "diagnostic_io_is_external_signoff": False,
        },
        "hardblock_discovery": audit["hardblock_discovery"],
        "syn5025": audit["syn5025_dummy_node_audit"],
        "retained_storage_names": audit["retained_name_occurrences_in_routed_netlist"],
        "source_sha256": source_hashes(),
        "functional_evidence_sha256": {
            "vsim_runner.log": "387ab48c84f3cd4029b06b375da04caecf148296fea337ee48748c4d98989282",
            "vsim_postprocess_attempt3.log": "161d4deb0add10818b50b5bbabbbba70b677e2980eb1589859e712baebf60989",
            "verification_summary.json": "1ed92924c024234c6bd235e5a49aaf7f19b1b96e6c95e0122433f5ffac2afadf",
        },
        "audit_sha256": sha256(ROOT / "postroute_audit_v2.json"),
    }
    (ROOT / "physical_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )

    old_rows = []
    for item in status["old_v10_internal_seven"]["paths"]:
        current = item["candidate"]
        old_rows.append([
            item["baseline_rank"], item["signature"], f"{item['baseline_slack_ns']:+.3f}",
            f"{current['slack_ns']:+.3f}" if current else "unmapped", item["status"],
        ])
    internal_rows = [[f"{p['slack_ns']:+.3f}", p["begin"], p["end"]] for p in internal_setup]
    report = f"""# v11 Internal-Timing Physical Validation

## Result

**FAIL at 100 MHz.** The authorized product-cut repaired all seven v10 logical endpoint families, but this same single routed build exposes five new internal setup failures. The worst internal path is `{internal_setup[0]['slack_ns']:+.3f} ns` from `{internal_setup[0]['begin']}` to `{internal_setup[0]['end']}`. No second seed, timing exception, bitstream, or arithmetic-core change was used.

The global worst setup is `{status['timing']['global_setup']['wns_ns']:+.3f} ns`; 15 of 20 setup failures terminate at the deliberately 0 ns diagnostic outputs. Those diagnostic paths are evidence only and are not external-interface signoff. Internal register hold is positive at `+0.054 ns`; global hold failures are diagnostic-input/raw-reset paths. Four raw-reset removal failures remain at the shell release synchronizer, while recovery has no violation and functional reset distribution is positive.

## Frozen candidate and functional evidence

- Stream SHA-256: `{status['source_sha256']['../rtl/road_postprocess_stream.v']}`
- Runner SHA-256: `{status['source_sha256']['../rtl/down2_overlap_tile_runner.v']}`
- Runner regression: four cases, all 640 stage/writebacks, no-stall 5433 cycles.
- Standalone regression: latency 24/25 cycles, reset ages 1..25, pressure cases, and explicit full-cut payload-hold assertion PASS.

## Old seven endpoint-family mapping

{table(old_rows, ['Rank', 'Logical endpoint family', 'v10 slack ns', 'v11 worst setup ns', 'Status'])}

The five pre-round families now launch through the registered product cut. `cnt_output[2]` and `mult17.xa[1]` are mapped from the complete 100,000-endpoint-cap all-path report, not inferred from absence in the violation report.

## New internal setup failures

{table(internal_rows, ['Slack ns', 'Begin', 'End'])}

All five launch from the shell `state_current[3]` decode and terminate in one MAC-weight storage data pin or four `cnt_output[0]` logic pins. This is a new shell scheduling/ack cone, not the repaired mask-to-fixed-round cone. The next candidate must be separately frozen and functionally proven; this baseline is sealed without further RTL changes.

## Coverage and constraints

- Complete report: 17,578 endpoints and 140,328 analyzed paths; cap 100,000 did not truncate endpoints.
- Global setup: 20 endpoints, WNS `{status['timing']['global_setup']['wns_ns']:+.3f} ns`, TNS `{status['timing']['global_setup']['tns_ns']:+.3f} ns`.
- Global min: 411 endpoints, WNS `{status['timing']['global_hold']['wns_ns']:+.3f} ns`, TNS `{status['timing']['global_hold']['tns_ns']:+.3f} ns`; 407 hold plus four removal records.
- No false path, multicycle path, ignored path, invalid constraint, or combinational loop is present.
- Clock report: one 100 MHz `probe_clk`, 6,273 clock endpoints. The 0 ns narrow-I/O constraints are diagnostic only.

## Hard blocks and memory

- 26 routed DSPs: 24 dynamic MAC DSPs plus two actual fixed-coefficient round DSPs. The latter are legal implementation cost, not a generic runtime-coefficient multiplier estimate.
- One SiLU ERAM and 145 distributed-RAM hard connections were discovered from this routed netlist.
- DSP timing: setup `+0.994 ns`, hold `+0.133 ns`; MAC-only setup `+1.784 ns`.
- DRAM timing: setup `+0.627 ns`, hold `+0.043 ns`.
- ERAM setup is `+3.454 ns`; its `-1.449 ns` hold failure is from the 0 ns diagnostic table-load input.
- Routed retained-name evidence includes metadata FIFO, result queue count, group head/tail data and masks, commit-ready control, halo, DW/PW weights and biases, DW cache, and output cache.

## Area

- 8,733 slices (41.16%): 7,509 logic and 1,224 RAM slices.
- 8,032 LUT6, 6,567 registers, 1,160 DRAM LUTs, 64 shifter LUTs.
- 1 ERAM, 26 DSPs, 38 I/O pins.

## SYN5025 / dummy-node audit

TD lists 52 unused optional `mul9_mode`/`mul9_signed` pins: 48 on the 24 MAC DSPs and four on the two fixed-round DSPs. These are disabled 9x submode controls on full-width multipliers; signed operands remain sign-extended at `xa/y`. The named-storage unused-LSLICE count is zero. Raw `check_timing` also retains one anonymous `_al_n1_syn_556.ofb` dummy output; it is not attributed to a queue, metadata, cache, or weight-storage bit.

## Evidence preservation

The initial `postroute_audit.json` and all three dynamic-export attempts remain unchanged. Corrected classification is in `postroute_audit_v2.json`; compact machine status is `physical_status.json`. `gate.db`, `pr.db`, routed netlist, all raw timing reports, failed logs, and guard receipts are retained. The frozen v10/prior guard remained unchanged before and after every guarded action.
"""
    (ROOT / "PHYSICAL_VALIDATION_REPORT.md").write_text(report, encoding="utf-8")

    manifest_paths = [
        "physical_status.json", "PHYSICAL_VALIDATION_REPORT.md", "postroute_audit.json",
        "postroute_audit_v2.json", "discovered_hardblocks.json", "gate.db", "pr.db",
        "routed_netlist.v", "coverage_100000_all_paths.timing",
        "coverage_100000_violations.timing", "check_timing_verbose.rpt",
        "timing_exceptions.rpt", "timing_ignored.rpt", "td_build.log",
    ]
    manifest = {
        "schema": "v11-physical-final-manifest-1",
        "status": status["status"],
        "files": {name: sha256(ROOT / name) for name in manifest_paths},
    }
    (ROOT / "physical_final_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("PASS V11_PHYSICAL_EVIDENCE_SEALED")
    print(f"old7_pass={old7_pass} internal_setup_failures={len(internal_setup)}")
    print(f"global_setup_wns_ns={status['timing']['global_setup']['wns_ns']}")


if __name__ == "__main__":
    main()
