"""只核验已有七个case证据并发布交接；不仿真，不修改冻结源。"""

import argparse
import copy
from pathlib import Path
import re

from run import CORES, CSP2, MODEL, PAYLOAD, PRIOR, PROJECT, ROOT, SKILL, VENDOR, digest, read, save


COUNT_KEYS = ("outputs", "tasks", "groups", "reads", "parameters")
LOG_NAMES = ("vlib.log", "compile.log", "simulation.log")
PUBLIC_GATES = {"compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"}
SEQUENCE_COUNTS = dict(blocks=3, runs=3, outputs=1327104, acc=1327104, pre=1327104,
                       silu=1327104, post=1327104, groups=1612800, tasks=520704,
                       reads=190858, parameters=193920, barriers=19)


def fields(marker):
    """沿前批finalize的整数marker解析，额外拒绝重复字段。"""
    pairs = re.findall(r"(\w+)=(\d+)", marker)
    assert pairs and len({key for key, _ in pairs}) == len(pairs)
    return {key: int(value) for key, value in pairs}


def verify_hashes(mapping, allowed_mismatches=()):
    """复用前批stdlib哈希合同：仅允许明确列出的全部差异。"""
    allowed = {str(Path(path)) for path in allowed_mismatches}
    mismatches = []
    assert mapping
    for raw_path, expected in mapping.items():
        assert re.fullmatch(r"[0-9a-fA-F]{64}", expected or "")
        path = Path(raw_path)
        if not path.is_file() or digest(path).lower() != expected.lower():
            mismatches.append(str(path))
    assert set(mismatches) == allowed, (mismatches, sorted(allowed))
    return mismatches


def expected_counts(target, tb_contract):
    family = read(target / "reference/family_receipt/family_contract.json")
    assert family["schema"] == "csp_family_layer_reference_v2_residual_bypass_corrected"
    expected = {}
    for block in (2, 3, 4):
        contract = tb_contract["block_counts"][str(block)]
        rows = {key: contract["stage_" + key] for key in COUNT_KEYS}
        assert all(len(value) == (5 if block == 2 else 7) for value in rows.values())
        assert all(contract[key] == sum(rows[key]) for key in COUNT_KEYS)
        assert contract["barriers"] == len(rows["outputs"])
        if block in (3, 4):
            reference = family["families"][f"csp{block}"]["stages"]
            keys = dict(outputs="logical_output_elements", tasks="task_count", groups="accepted_core_groups",
                        reads="expected_read_requests", parameters="expected_parameter_requests")
            assert [row["stage"] for row in reference] == list(range(7))
            assert all(rows[key] == [row[field] for row in reference] for key, field in keys.items())
        else:
            # 前批CSP2 finalize.EXPECTED的封存计数，与本批TB合同交叉核对。
            prior = dict(outputs=[110592]*4+[221184], tasks=[55296,36864,55296,36864,73728],
                         groups=[110592,73728,110592,73728,221184],
                         reads=[30210,20736,16748,13824,27648],
                         parameters=[27648,4608,27648,4608,13824])
            assert rows == prior
        expected[block] = rows
    assert tb_contract["sequence_counts"] == SEQUENCE_COUNTS
    assert all(sum(sum(expected[b][key]) for b in expected) == SEQUENCE_COUNTS[key] for key in COUNT_KEYS)
    assert tb_contract["raw_states"] == list(range(17))
    return expected


def validate_run(run, stages, states, expected, block, case, number):
    size = len(expected["outputs"])
    assert (run["block"], run["case"], run["run"]) == (block, case, number)
    assert len(stages) == size and sorted(row["stage"] for row in stages) == list(range(size))
    assert len(states) == 17 and sorted(row["state"] for row in states) == list(range(17))
    for row in [*stages, *states]:
        assert (row["block"], row["case"], row["run"]) == (block, case, number)
        assert row["cycles"] >= 0
    for row in stages:
        assert all(row[key] == expected[key][row["stage"]] for key in COUNT_KEYS)
        assert row["barriers"] == 1
    assert all(run[key] == sum(expected[key]) for key in COUNT_KEYS)
    assert all(run[key] == run["outputs"] for key in ("acc", "pre", "silu", "post"))
    assert run["barriers"] == size
    assert sum(row["cycles"] for row in stages) == sum(row["cycles"] for row in states)
    assert sum(row["cycles"] for row in stages) == run["cycles"] == run["accounted"] > 0


def exclusive_cycles(run, states):
    counters = {row["state"]: row["cycles"] for row in states}
    categories = dict(input_prefetch=sum(counters[index] for index in (2, 3, 4)),
        parameter_prefetch=counters[5]+counters[6], task_tile_setup=counters[1]+counters[7],
        local_operand_assembly=counters[8]+counters[9], accepted_core_groups=run["groups"],
        core_admission_wait=counters[10]-run["groups"],
        arithmetic_pipeline_and_output_retirement=counters[11],
        registered_retire_and_advance=counters[12]+counters[13],
        layer_visibility_barrier=counters[14], other_control=counters[0]+counters[15]+counters[16])
    assert all(value >= 0 for value in categories.values())
    assert sum(categories.values()) == run["cycles"]
    return categories


def validate_sequence(marker, runs, aborted, case):
    assert all(marker[key] == value for key, value in SEQUENCE_COUNTS.items())
    assert marker["case"] == case and len(runs) == 3
    assert [(row["block"], row["run"]) for row in runs] == [(2, 1), (3, 2), (4, 3)]
    assert all(marker[key] == sum(row[key] for row in runs)
               for key in (*COUNT_KEYS, "acc", "pre", "silu", "post", "barriers"))
    assert marker["cycles"] == marker["accounted"] == sum(row["cycles"] for row in runs)
    assert marker["sequence_cycles"] == marker["cycles"] + marker["overhead_cycles"] + marker["aborted_cycles"]
    assert marker["cycles"] < 100000000 and marker["overhead_cycles"] >= 0
    assert marker["table_loads"] == (2 if case == 2 else 1)
    assert marker["aborted_runs"] == len(aborted) == int(case == 2)
    if case == 2:
        abort = aborted[0]
        assert abort["case"] == 2 and abort["block"] == 2 and abort["cycles"] > 0
        assert 2*110592+128 <= abort["outputs"] < 663552
        assert marker["aborted_cycles"] == abort["cycles"]
        assert marker["aborted_outputs"] == abort["outputs"]
    else:
        assert marker["aborted_cycles"] == marker["aborted_outputs"] == 0


def self_check():
    expected = {key: [index + offset for index in range(5)]
                for offset, key in enumerate(COUNT_KEYS, start=1)}
    stages = [dict(block=2, case=0, run=1, stage=index, cycles=1, barriers=1,
                   **{key: values[index] for key, values in expected.items()}) for index in range(5)]
    states = [dict(block=2, case=0, run=1, state=index, cycles=int(index < 5)) for index in range(17)]
    run = {key: sum(values) for key, values in expected.items()}
    run.update(block=2, case=0, run=1, cycles=5, accounted=5, barriers=5,
               **{key: sum(expected["outputs"]) for key in ("acc", "pre", "silu", "post")})
    validate_run(run, stages, states, expected, 2, 0, 1)
    mutated = copy.deepcopy(stages)
    mutated[0]["reads"] += 1
    try:
        validate_run(run, mutated, states, expected, 2, 0, 1)
    except AssertionError:
        return
    raise AssertionError("mutated stage read count escaped finalizer")


def validate_case(target, case, expected, tb_contract):
    folder = target / f"case{case}"
    negative = case == 99
    status = read(folder / "status.json")
    assert status["case"] == case
    assert status["status"] == ("PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE")
    commands = read(folder / "commands.json")
    assert len(commands) == 3
    texts = []
    for record, filename in zip(commands, LOG_NAMES, strict=True):
        verify_hashes({str(folder / filename): record["log_sha256"]})
        assert Path(record["cwd"]).resolve() == folder.resolve()
        text = (folder / filename).read_text(encoding="utf-8")
        effective = record["native_returncode"] or int(bool(re.search(r"\*\* (?:Error|Fatal):", text)))
        assert record["validated_returncode"] == effective
        texts.append(text)
    sources = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
    sources += [target / "reused" / f"{module}.v" for module in CORES]
    sources += [target / "rtl/road_feature_blocks_client.v", target / "tests/tb_feature_blocks_client.v"]
    assert commands[0]["argv"] == [str(MODEL / "vlib.exe"), "work"]
    assert commands[1]["argv"] == [str(MODEL / "vlog.exe"), "-work", "work", *map(str, sources)]
    assert all(row["native_returncode"] == row["validated_returncode"] == 0 for row in commands[:2])
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", texts[1])
    assert summaries and all(row == ("0", "0") for row in summaries)
    entry, = [row for row in tb_contract["runner_cases"] if row["case"] == case]
    argv = [str(MODEL / "vsim.exe"), "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_feature_blocks_client",
            f"+CASE={0 if negative else case}", f"+VECTORS_ROOT={(target / 'reference').as_posix()}",
            *(["+NEGATIVE_ACC=1"] if negative else entry.get("plusargs", [])),
            "-do", "run -all; quit -code 0"]
    assert commands[2]["argv"] == argv
    simulation = texts[2]
    files = ["commands.json", "status.json", *LOG_NAMES]
    result = dict(case=case, native_simulation_returncode=commands[2]["native_returncode"],
                  validated_simulation_returncode=commands[2]["validated_returncode"],
                  compile_errors=0, compile_warnings=0,
                  elaboration_warning_lines=re.findall(r"(?m)^# \*\* Warning:[^\r\n]*", simulation),
                  runs=[], aborted=[])
    if negative:
        assert commands[2]["validated_returncode"] != 0
        assert "NEGATIVE_ACC injected acc mismatch" in simulation
        assert not re.search(r"FEATURE_BLOCKS_(?:PASS|EXPECTED_FAULT) |FEAT_BLOCK_RUN ", simulation)
        result["real_acc_checker_negative_rejected"] = True
    else:
        assert commands[2]["validated_returncode"] == 0
        assert not re.search(r"\*\* (?:Error|Fatal):", simulation)
        receipt = read(folder / "receipt.json")
        files.append("receipt.json")
        for key, prefix in (("stage_ledger", "FEAT_BLOCK_STAGE"), ("state_ledger", "FEAT_BLOCK_STATE"),
                            ("measured_runs", "FEAT_BLOCK_RUN")):
            assert receipt[key] == re.findall(prefix + r" [^\r\n]*", simulation)
        markers = re.findall(r"FEATURE_BLOCKS_(?:PASS|EXPECTED_FAULT) [^\r\n]*", simulation)
        assert markers == [receipt["marker"]] and markers[0].startswith(entry["marker"])
        marker = fields(markers[0])
        assert receipt["fields"] == marker and marker["case"] == case
        assert all(marker.get(key) == value for key, value in entry.get("expected_fields", {}).items())
        assert set(marker) == set(tb_contract["marker_fields"][entry["marker"]])
        result["endpoint"] = marker
        parsed_stages = list(map(fields, receipt["stage_ledger"]))
        parsed_states = list(map(fields, receipt["state_ledger"]))
        aborts = list(map(fields, re.findall(r"FEAT_BLOCK_ABORT [^\r\n]*", simulation)))
        if case in (0, 1, 2):
            parsed_runs = list(map(fields, receipt["measured_runs"]))
            assert len(parsed_stages) == 19 and len(parsed_states) == 51 and len(parsed_runs) == 3
            for number, run in enumerate(parsed_runs, start=1):
                block = number + 1
                stages = [row for row in parsed_stages if row["run"] == number]
                states = [row for row in parsed_states if row["run"] == number]
                validate_run(run, stages, states, expected[block], block, case, number)
                result["runs"].append(dict(block=block, case=case, run=number, endpoint=run,
                    stages=stages, states=states, exclusive_cycles=exclusive_cycles(run, states),
                    retirement_window_is_not_pure_idle=True))
            validate_sequence(marker, parsed_runs, aborts, case)
            result["aborted"] = aborts
        else:
            assert not receipt["measured_runs"] and not parsed_stages and not parsed_states and not aborts
    result["evidence"] = {str((folder / filename).relative_to(ROOT)): digest(folder / filename) for filename in files}
    return result


def check_bindings(target):
    binding = read(target / "input_binding.json")
    verify_hashes(binding["original_sha256"])
    verify_hashes(binding["staged_sha256"])
    previous = [read(CSP2 / "frozen/input_binding.json"), read(PRIOR / "frozen_attempt3/input_binding.json")]
    assert binding["old_bindings"] == previous
    for old in previous:
        verify_hashes(old["original_sha256"])
        verify_hashes(old["staged_sha256"])
    baseline = ROOT / "frozen"
    baseline_binding = read(baseline / "input_binding.json")
    assert baseline_binding["old_bindings"] == previous
    changed_tb = ROOT / "tests/tb_feature_blocks_client.v"
    verify_hashes(baseline_binding["original_sha256"], (changed_tb,))
    verify_hashes(baseline_binding["staged_sha256"])
    original_tb = baseline / "tests/tb_feature_blocks_client.v"
    assert digest(original_tb) == baseline_binding["original_sha256"][str(changed_tb)]

    def tokens(path):
        text = re.sub(r"/\*.*?\*/|//[^\r\n]*", "", path.read_text(encoding="utf-8"), flags=re.S)
        return re.sub(r"\s+", "", text)

    old_text, new_text = tokens(original_tb), tokens(changed_tb)
    anchor = "wait(layer==2&&busy&&stage_outputs[2]>=128);@(negedgeclk);"
    assert old_text.count(anchor) == 1
    assert new_text == old_text.replace(anchor, anchor + "rstn=0;", 1)
    return binding, dict(path=str(changed_tb), baseline_sha256=digest(original_tb),
        corrected_sha256=digest(changed_tb), only_baseline_original_exception=True,
        reason="CASE2 asserts common reset at the same negedge as the aborted-cycle endpoint",
        baseline_staged_hash_unchanged=True, baseline_staged_all_verified=True)


def check_gate(candidate):
    folder = candidate / "static_gate"
    command = read(folder / "command.json")
    verify_hashes({str(folder / "run.log"): command["log_sha256"]})
    expected = [command["argv"][0], "-B", "-m", "scripts.python.validation.generated_deliverable_gate",
                str(candidate), "--include-testbench", "--spec", str(candidate / "spec_contract.json"),
                "--json", str(folder / "gate.json"), "--markdown", str(folder / "gate.md")]
    assert command["argv"] == expected and Path(command["cwd"]).resolve() == SKILL.resolve()
    report = read(folder / "gate.json")
    assert report["version"] == 3 and report["strict"] is True
    assert Path(report["root"]).resolve() == candidate.resolve()
    assert set(report["checks"]) == PUBLIC_GATES
    assert command["returncode"] == (0 if report["delivery_ready"] else 1)
    evidence = {str((folder / name).relative_to(ROOT)): digest(folder / name)
                for name in ("gate.json", "gate.md", "command.json", "run.log")}
    return dict(errors=report["errors"], strict_warnings=report["strict_warnings"],
                delivery_ready=report["delivery_ready"],
                checks={key: row["status"] for key, row in report["checks"].items()}, evidence=evidence)


def check_reference():
    reference = ROOT / "reference"
    csp = read(reference / "csp_manifest.json")
    sppf = read(reference / "sppf_manifest.json")
    evidence = {}
    for filename, manifest in (("csp_manifest.json", csp), ("sppf_manifest.json", sppf)):
        assert manifest["payload_sha256"] == PAYLOAD
        verify_hashes({str(PROJECT / path): value for path, value in manifest["source_sha256"].items()})
        verify_hashes({str(reference / path): value for path, value in manifest["artifacts"].items()})
        assert len(manifest["artifacts"]) == manifest["artifact_count"]
        evidence[str((reference / filename).relative_to(ROOT))] = digest(reference / filename)
    assert csp["artifact_count"] == 335
    assert read(reference / "selector_report.json")["status"] == "PASS"
    report = read(reference / "sppf/report.json")
    assert report["status"] == "PASS_CPU_SPPF_REFERENCE" and report["source_before_after_equal"]
    assert report["cuda_initialized"] is False and report["cpu_only"] is True
    assert report["conv_full_scalar_checked"] == 2 and len(report["pool_checks"]) == 3
    assert all(row["full_scalar_values"] == 13824 for row in report["pool_checks"])
    assert all(row["wrong_rejected"] and row["mismatches"] > 0 for row in report["true_numerical_negative_checks"])
    assert read(reference / "sppf/pan_dependency_spec.json")["status"] == "SPEC_ONLY_NO_PAN_GOLDEN_NO_RTL"
    return dict(CSP_reference_artifacts=335, SPPF_CPU_reference_pass=True, SPPF_RTL_in_selected_CSP_candidate=False,
                PAN_CPU_dependency_spec_pass=True, PAN_CPU_golden_implemented=False,
                PAN_RTL_in_selected_CSP_candidate=False, CUDA_initialized=False, evidence=evidence)


def integration_sources(target):
    client = target / "rtl/road_feature_blocks_client.v"
    tb = target / "tests/tb_feature_blocks_client.v"
    text, test = client.read_text(encoding="utf-8"), tb.read_text(encoding="utf-8")
    assert len(re.findall(r"\breg\s+\[4:0\]\s*state_current\s*;", text)) == 1
    assert len(re.findall(r"\breg\s+\[7:0\]\s*reg_tile_cache\s*\[0:3071\]\s*;", text)) == 1
    assert len(re.findall(r"\breg\s+\[191:0\]\s*reg_weight_bank\s*\[0:23\]\s*;", text)) == 1
    assert len(re.findall(r"\broad_feature_blocks_client\s+client\s*\(", test)) == 1
    assert len(re.findall(r"\broad_csp_first_probe\s+arithmetic_Inst\s*\(", test)) == 1
    assert not re.search(r"\b(?:road_csp_first_probe|road_mac_probe|road_dynamic_postprocess)\s+\w+\s*\(", text)
    sources = {str(client.relative_to(ROOT)): digest(client)}
    assert len(CORES) == 6
    for module in CORES:
        path = target / "reused" / f"{module}.v"
        assert digest(path) == digest(PRIOR / "frozen_attempt3/reused" / path.name)
        sources[str(path.relative_to(ROOT))] = digest(path)
    return dict(functional_sources=sources, client_MAC_instances=0, client_FSM_count=1,
                runtime_client_instances_in_TB=1, arithmetic_owner_instances_in_TB=1,
                work_cache_arrays=1, work_cache_bytes=3072, weight_banks=1, weight_bank_slots=24,
                weight_bank_bits_per_slot=192, total_reserved_data_bytes=3695,
                cache_port_organization="exclusive PREFETCH write / CACHE_ACTIVATION read / CACHE_BYPASS read states",
                source_storage_organization_only=True, physical_shared_cache_mapped=False,
                actual_DDR_connected=False, continuous_backbone_integrated=False, full_graph_integrated=False)


def finalize(name):
    self_check()
    assert name == "frozen_attempt2", "Only the explicitly corrected candidate is selected"
    target = ROOT / name
    binding, exception = check_bindings(target)
    assert binding["payload_sha256"] == PAYLOAD
    tb_contract = read(target / "tb_contract.json")
    expected = expected_counts(target, tb_contract)
    cases = [validate_case(target, case, expected, tb_contract) for case in (0, 1, 2, 3, 4, 5, 99)]
    runs = [run for case in cases for run in case["runs"]]
    assert len(runs) == 9 and sorted((row["case"], row["block"]) for row in runs) == [
        (case, block) for case in (0, 1, 2) for block in (2, 3, 4)]
    baseline_gate, corrected_gate = check_gate(ROOT / "frozen"), check_gate(target)
    reference = check_reference()
    integration = integration_sources(target)
    evidence = {path: value for case in cases for path, value in case["evidence"].items()}
    for gate in (baseline_gate, corrected_gate):
        evidence.update(gate["evidence"])
    evidence.update(reference["evidence"])
    # 两次失败规格调用仍保留，成功规格报告与真实命令一起绑定。
    spec_calls = []
    for stem in ("spec_attempt1", "spec_attempt2", "road_feature_blocks_client_spec", "tb_feature_blocks_client_spec"):
        command_path = ROOT / (stem + "_command.json")
        log_path = ROOT / (stem + "_render.log")
        command = read(command_path)
        verify_hashes({str(log_path): command["log_sha256"]})
        evidence[str(command_path.relative_to(ROOT))] = digest(command_path)
        evidence[str(log_path.relative_to(ROOT))] = digest(log_path)
        spec_calls.append(dict(command_file=str(command_path.relative_to(ROOT)), returncode=command["returncode"]))
    assert all(row["returncode"] == 0 for row in spec_calls[2:])
    handoff = [ROOT / "handoff.txt", ROOT / "PAN_存储交接.txt"]
    assert all(path.is_file() for path in handoff), "Root handoff texts required before publication"
    evidence.update({str(path.relative_to(ROOT)): digest(path) for path in handoff})
    before = dict(evidence)
    assert check_bindings(target) == (binding, exception)
    assert check_reference() == reference
    verify_hashes({str(ROOT / path): value for path, value in before.items()})
    ledger = dict(scope="Same-DUT CSP2/3/4 fixtures; CPU down3/down4 bridge, not continuous RTL CNN",
                  clock_hz=100000000, runs=runs, sequences=[case for case in cases if case["case"] in (0, 1, 2)],
                  endpoint="Accepted start through edge entering DONE, inclusive; 17 raw states and per-stage totals independently equal clean block cycles",
                  initial_LUT_load_excluded=True, aborted_partial_runs_excluded_from_clean=True,
                  reset_LUT_reload_and_idle_only_in_sequence_overhead=True,
                  system_target_cycles=100000000, whole_system_FPS_qualified=False,
                  controlled_memory_service_not_real_DDR=True)
    summary = dict(status="FIXED_CSP2_CSP3_CSP4_FUNCTION_PASS_NOT_DEPLOYMENT", selected_candidate=name,
        validated_case_directories=7, positive_sequence_cases=3, expected_fault_cases=3,
        real_acc_checker_negative_cases=1, completed_full_block_runs=9,
        original_staged_and_old_bindings_rechecked_before_after=True,
        baseline_original_measurement_exception=exception,
        source_binding_original_files=len(binding["original_sha256"]), source_binding_staged_files=len(binding["staged_sha256"]),
        payload_sha256=PAYLOAD, image_sha256=binding["image_sha256"],
        client_sha256=digest(target / "rtl/road_feature_blocks_client.v"),
        tb_sha256=digest(target / "tests/tb_feature_blocks_client.v"),
        finalizer_sha256=digest(Path(__file__)), input_binding_sha256=digest(target / "input_binding.json"),
        actual_ModelSim_compile_errors=0, actual_ModelSim_compile_warnings=0,
        simulation_exit_evidence=[{key: case[key] for key in ("case", "native_simulation_returncode", "validated_simulation_returncode", "elaboration_warning_lines")} for case in cases],
        finalizer_positive_and_mutated_read_negative=True,
        strict_gate_comparison=dict(original=baseline_gate, corrected=corrected_gate,
            public_matrix_equal=baseline_gate["checks"] == corrected_gate["checks"]),
        CPU_reference=reference, specification_calls=spec_calls, arithmetic_changed=False,
        one_runtime_client=True, physical_shared_cache_mapped=False, actual_DDR=False,
        continuous_backbone=False, full_graph=False, synthesis=False, place_route=False,
        bitstream=False, board=False, accuracy_evaluation=False, FPS_qualification=False,
        training_updates=0, production_delivery_ready=False, evidence=evidence)
    for filename, content in (("cycle_ledger.json", ledger), ("integration_sources.json", integration),
                              ("final_checks.json", summary), ("status.json", summary)):
        save(ROOT / filename, content)
    published = {str(ROOT / filename): digest(ROOT / filename) for filename in (
        "cycle_ledger.json", "integration_sources.json", "final_checks.json", "status.json", "handoff.txt", "PAN_存储交接.txt")}
    verify_hashes(published)
    save(ROOT / "delivery_manifest.json", dict(status=summary["status"], selected_candidate=name,
        artifacts_sha256=published, finalizer_sha256=digest(Path(__file__)),
        input_binding_sha256=digest(target / "input_binding.json"), payload_sha256=PAYLOAD,
        production_delivery_ready=False))
    print("SEALED_FIXED_CSP_BLOCKS_FUNCTION_ONLY_NOT_DEPLOYMENT", len(runs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="frozen_attempt2")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("FINALIZER_POSITIVE_AND_MUTATED_READ_NEGATIVE_PASS")
    else:
        finalize(args.name)
