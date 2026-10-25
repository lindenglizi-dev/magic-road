"""核验保存的CSP4→SPPF增量及旧CSP回归；不重新仿真或修改冻结资产。"""

import argparse
import copy
import importlib.util
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
sys.path.insert(0, str(PARENT))

import run_sppf as runner

_spec = importlib.util.spec_from_file_location("phase1_finalizer_helpers", PARENT / "finalize.py")
phase1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase1)
digest, read, save = runner.digest, runner.read, runner.save
fields, verify_hashes = phase1.fields, phase1.verify_hashes
COUNT_KEYS, LOG_NAMES = phase1.COUNT_KEYS, phase1.LOG_NAMES
CLIENT_SHA256 = "9311eceda255a4206b6d78955689114f243dd8bc8af4d63520f6d5cdb5ec0d72"
CHAIN = dict(blocks=2, runs=2, outputs=331776, acc=290304, pre=290304, silu=290304,
             post=290304, groups=746496, tasks=110592, reads=41832, parameters=69120,
             barriers=12, pools=41472, concat_values=1769472, negative_pool_outputs=1628)


def expected_counts(target, contract):
    regression = read(target / "regression_contract.json")
    prior = phase1.expected_counts(PARENT / "frozen_attempt2", regression)
    assert contract["raw_states"] == list(range(20)) and contract["sequence_counts"] == CHAIN
    expected = {}
    for block in (4, 5):
        row = contract["block_counts"][str(block)]
        counts = {key: row["stage_" + key] for key in COUNT_KEYS}
        counts["numeric"] = row.get("stage_numeric", row["stage_outputs"])
        size = 7 if block == 4 else 5
        assert all(len(values) == size for values in counts.values())
        assert all(row[key] == sum(counts[key]) for key in COUNT_KEYS)
        assert row["barriers"] == size
        if block == 4:
            assert {key: counts[key] for key in COUNT_KEYS} == prior[4]
        else:
            assert counts["outputs"] == [13824]*4+[55296]
            assert counts["numeric"] == [13824, 0, 0, 0, 55296]
            assert counts["tasks"] == [4608, 0, 0, 0, 18432]
            assert counts["groups"] == [55296, 0, 0, 0, 221184]
            assert counts["parameters"] == [3840, 0, 0, 0, 15360]
            assert row["pools"] == sum(counts["outputs"][1:4]) == 41472
            assert row["concat_values"] == 576*32*96 == 1769472
        expected[block] = counts
    schedule = read(target / "schedule_report.json")
    assert schedule["status"] == "PASS_FIXED_SPPF_READ_SCHEDULE"
    assert schedule["script_sha256"] == digest(target / "reference_schedule.py") == digest(ROOT / "reference_schedule.py")
    graph_path = runner.PROJECT / "cnn/hw_validation/production/graph_artifacts/graph.json"
    assert schedule["graph_sha256"] == digest(graph_path)
    graph = read(graph_path)
    nodes = {node["name"]: node for node in graph["nodes"]}
    spec = importlib.util.spec_from_file_location("sealed_sppf_schedule", target / "reference_schedule.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    names = ["csp4.out.conv", "sppf.squeeze.conv", "pool.00", "pool.01", "pool.02"]
    sources = [[nodes[name]["storage"]["base"]] for name in names[:4]]
    sources.append([nodes[name]["storage"]["base"] for name in names[1:]])
    independently_counted = [model.read_count(stage, bases) for stage, bases in enumerate(sources)]
    assert independently_counted == schedule["stage_reads"] == expected[5]["reads"] == [3456, 3060, 3060, 3060, 4608]
    assert contract["read_contract"]["SPPF_exact_stage_reads"] == independently_counted
    assert all(CHAIN[key] == sum(sum(expected[block][key]) for block in (4, 5)) for key in COUNT_KEYS)
    assert CHAIN["acc"] == sum(sum(expected[block]["numeric"]) for block in (4, 5))
    return expected, prior


def validate_run(run, stages, states, expected, block, case, number):
    size = len(expected["outputs"])
    assert (run["block"], run["case"], run["run"]) == (block, case, number)
    assert len(stages) == size and sorted(row["stage"] for row in stages) == list(range(size))
    assert len(states) == 20 and sorted(row["state"] for row in states) == list(range(20))
    for row in [*stages, *states]:
        assert (row["block"], row["case"], row["run"]) == (block, case, number)
        assert row["cycles"] >= 0
    for row in stages:
        assert all(row[key] == expected[key][row["stage"]] for key in COUNT_KEYS)
        assert row["barriers"] == 1
    assert all(run[key] == sum(expected[key]) for key in COUNT_KEYS)
    assert all(run[key] == sum(expected["numeric"]) for key in ("acc", "pre", "silu", "post"))
    assert run["barriers"] == size
    assert run["pools"] == (41472 if block == 5 else 0)
    assert run["concat_values"] == (1769472 if block == 5 else 0)
    assert sum(row["cycles"] for row in stages) == sum(row["cycles"] for row in states)
    assert sum(row["cycles"] for row in states) == run["cycles"] == run["accounted"] > 0
    counter = {row["state"]: row["cycles"] for row in states}
    assert counter[17] == counter[18] == 25*run["pools"]
    assert counter[19] >= run["pools"]
    if block == 4:
        assert counter[19] == 0


def exclusive_cycles(run, states):
    counters = {row["state"]: row["cycles"] for row in states}
    categories = dict(input_prefetch=sum(counters[index] for index in (2, 3, 4)),
        parameter_prefetch=counters[5]+counters[6], task_tile_setup=counters[1]+counters[7],
        local_operand_assembly=counters[8]+counters[9], accepted_core_groups=run["groups"],
        core_admission_wait=counters[10]-run["groups"],
        arithmetic_pipeline_and_output_retirement=counters[11],
        registered_retire_and_advance=counters[12]+counters[13], layer_visibility_barrier=counters[14],
        other_control=counters[0]+counters[15]+counters[16], pool_byte_read=counters[17],
        pool_signed_compare=counters[18], pool_accepted_write=run["pools"],
        pool_write_backpressure=counters[19]-run["pools"])
    assert all(value >= 0 for value in categories.values()) and sum(categories.values()) == run["cycles"]
    return categories


def self_check():
    row = read(ROOT / "tb_contract.json")["block_counts"]["5"]
    expected = {key: row["stage_"+key] for key in COUNT_KEYS}
    expected["numeric"] = row["stage_numeric"]
    stages = [dict(block=5, case=0, run=2, stage=index, barriers=1,
                   cycles=(expected["groups"][index]+int(index == 0) if index in (0, 4) else 51*13824),
                   **{key: expected[key][index] for key in COUNT_KEYS}) for index in range(5)]
    states = [dict(block=5, case=0, run=2, state=index, cycles=0) for index in range(20)]
    for state, value in ((0, 1), (10, sum(expected["groups"])), (17, 25*41472), (18, 25*41472), (19, 41472)):
        states[state]["cycles"] = value
    run = {key: sum(expected[key]) for key in COUNT_KEYS}
    run.update(block=5, case=0, run=2, barriers=5, pools=41472, concat_values=1769472,
               cycles=sum(stage["cycles"] for stage in stages), accounted=sum(stage["cycles"] for stage in stages),
               **{key: 69120 for key in ("acc", "pre", "silu", "post")})
    validate_run(run, stages, states, expected, 5, 0, 2)
    exclusive_cycles(run, states)
    mutated = copy.deepcopy(stages)
    mutated[1]["reads"] += 1
    try:
        validate_run(run, mutated, states, expected, 5, 0, 2)
    except AssertionError:
        return
    raise AssertionError("mutated pool read count escaped finalizer")


def case_logs(target, case, regression=False):
    folder = target / (f"regression_case{case}" if regression else f"case{case}")
    commands = read(folder / "commands.json")
    assert len(commands) == 3
    texts = []
    for command, name in zip(commands, LOG_NAMES, strict=True):
        verify_hashes({str(folder/name): command["log_sha256"]})
        assert Path(command["cwd"]).resolve() == folder.resolve()
        text = (folder/name).read_text(encoding="utf-8")
        effective = command["native_returncode"] or int(bool(re.search(r"\*\* (?:Error|Fatal):", text)))
        assert command["validated_returncode"] == effective
        texts.append(text)
    sources = [runner.VENDOR/"ph1p_logic_eram.v", runner.VENDOR/"ph1p_phy_gsr.v"]
    sources += [target/"reused"/(module+".v") for module in runner.CORES]
    sources += [target/"rtl/road_feature_blocks_client.v", target/"tests/tb_feature_sppf_client.v", target/"tests/tb_feature_blocks_client.v"]
    assert commands[0]["argv"] == [str(runner.MODEL/"vlib.exe"), "work"]
    assert commands[1]["argv"] == [str(runner.MODEL/"vlog.exe"), "-work", "work", *map(str, sources)]
    assert all(command["native_returncode"] == command["validated_returncode"] == 0 for command in commands[:2])
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", texts[1])
    assert summaries and all(pair == ("0", "0") for pair in summaries)
    contract = read(target/("regression_contract.json" if regression else "tb_contract.json"))
    entry, = [row for row in contract["runner_cases"] if row["case"] == case]
    top = "tb_feature_blocks_client" if regression else "tb_feature_sppf_client"
    token = "NEGATIVE_ACC" if regression else "NEGATIVE_POOL"
    argv = [str(runner.MODEL/"vsim.exe"), "-c", "-lib", "work", "PH1P_PHY_GSR", top,
            f"+CASE={0 if case == 99 else case}", f"+VECTORS_ROOT={(target/'reference').as_posix()}",
            *([f"+{token}=1"] if case == 99 else entry.get("plusargs", [])), "-do", "run -all; quit -code 0"]
    assert commands[2]["argv"] == argv
    return folder, commands, texts[2], contract, entry


def parsed_ledgers(simulation, prefix):
    return {key: list(map(fields, re.findall(prefix+"_"+suffix+r" [^\r\n]*", simulation)))
            for key, suffix in (("stages", "STAGE"), ("states", "STATE"), ("runs", "RUN"))}


def validate_case(target, case, expected, prior, regression=False):
    folder, commands, simulation, contract, entry = case_logs(target, case, regression)
    runner.check_vector_loading(simulation)
    status = read(folder/"status.json")
    assert status["case"] == case and status["regression"] is regression
    assert status["status"] == ("PASS_REAL_CHECKER_NEGATIVE" if case == 99 else "PASS_FUNCTION_CASE")
    result = dict(case=case, regression=regression, runs=[], excluded_negative_prelude_runs=[],
                  native_returncode=commands[2]["native_returncode"], validated_returncode=commands[2]["validated_returncode"],
                  compile_errors=0, compile_warnings=0,
                  elaboration_warning_lines=re.findall(r"(?m)^# \*\* Warning:[^\r\n]*", simulation))
    files = ["commands.json", "status.json", *LOG_NAMES]
    prefix = "FEAT_BLOCK" if regression else "FEAT_SPPF"
    parsed = parsed_ledgers(simulation, prefix)
    if case == 99:
        assert not regression and commands[2]["validated_returncode"] != 0
        assert "NEGATIVE_POOL injected pool mismatch" in simulation and "FEATURE_SPPF_PASS" not in simulation
        # 负例先完整计算CSP4，但它不是一个正常链case，也不进入11个clean完整块统计。
        assert len(parsed["runs"]) == 1
        prelude = parsed["runs"][0]
        validate_run(prelude, parsed["stages"], parsed["states"], expected[4], 4, 0, 1)
        result["excluded_negative_prelude_runs"] = [prelude]
        result["real_pool_checker_negative_rejected"] = True
    else:
        assert commands[2]["validated_returncode"] == 0 and not re.search(r"\*\* (?:Error|Fatal):", simulation)
        receipt = read(folder/"receipt.json")
        files.append("receipt.json")
        for key, suffix in (("stage_ledger", "STAGE"), ("state_ledger", "STATE"), ("measured_runs", "RUN")):
            assert receipt[key] == re.findall(prefix+"_"+suffix+r" [^\r\n]*", simulation)
        marker_prefix = "FEATURE_BLOCKS" if regression else "FEATURE_SPPF"
        markers = re.findall(marker_prefix+r"_(?:PASS|EXPECTED_FAULT) [^\r\n]*", simulation)
        assert markers == [receipt["marker"]] and markers[0].startswith(entry["marker"])
        marker = fields(markers[0])
        assert receipt["fields"] == marker and marker["case"] == case
        assert set(marker) == set(contract["marker_fields"][entry["marker"]])
        assert all(marker.get(key) == value for key, value in entry.get("expected_fields", {}).items())
        result["endpoint"] = marker
        if regression:
            assert case == 0 and len(parsed["runs"]) == 3 and len(parsed["stages"]) == 19 and len(parsed["states"]) == 51
            for number, run in enumerate(parsed["runs"], start=1):
                block = number+1
                stages = [row for row in parsed["stages"] if row["run"] == number]
                states = [row for row in parsed["states"] if row["run"] == number]
                phase1.validate_run(run, stages, states, prior[block], block, 0, number)
                result["runs"].append(dict(block=block, case=0, regression=True, endpoint=run,
                    stages=stages, states=states, exclusive_cycles=phase1.exclusive_cycles(run, states)))
            phase1.validate_sequence(marker, parsed["runs"], [], 0)
        else:
            assert case in (0, 1, 2, 3) and len(parsed["runs"]) == 2
            assert len(parsed["stages"]) == 12 and len(parsed["states"]) == 40
            for number, run in enumerate(parsed["runs"], start=1):
                block = number+3
                stages = [row for row in parsed["stages"] if row["run"] == number]
                states = [row for row in parsed["states"] if row["run"] == number]
                validate_run(run, stages, states, expected[block], block, case, number)
                result["runs"].append(dict(block=block, case=case, regression=False, endpoint=run,
                    stages=stages, states=states, exclusive_cycles=exclusive_cycles(run, states)))
            assert all(marker[key] == value for key, value in CHAIN.items())
            assert all(marker[key] == sum(run[key] for run in parsed["runs"])
                       for key in (*COUNT_KEYS, "acc", "pre", "silu", "post", "barriers", "pools", "concat_values"))
            assert marker["cycles"] == marker["accounted"] == sum(run["cycles"] for run in parsed["runs"])
            assert marker["cycles"] < 100000000
            assert marker["sequence_cycles"] == marker["cycles"]+marker["overhead_cycles"]+marker["aborted_cycles"]
            assert marker["busy_id_perturb_cycles"] > 0 and marker["busy_start_cycles"] > 0
            assert marker["table_loads"] == (2 if case == 2 else 1)
            assert marker["long_pool_stalls"] == (64 if case == 3 else 0)
            if case == 3:
                assert result["runs"][1]["exclusive_cycles"]["pool_write_backpressure"] >= 64
            aborted = list(map(fields, re.findall(r"FEAT_SPPF_ABORT [^\r\n]*", simulation)))
            assert len(aborted) == marker["aborted_runs"] == int(case == 2)
            if case == 2:
                abort = aborted[0]
                assert (abort["block"], abort["case"]) == (5, 2) and abort["cycles"] > 0
                assert 221184+13824+13824+128 <= abort["outputs"] < 331776
                assert marker["aborted_cycles"] == abort["cycles"] and marker["aborted_outputs"] == abort["outputs"]
            else:
                assert marker["aborted_cycles"] == marker["aborted_outputs"] == 0
            result["aborted_prefix_includes_CSP4_and_partial_SPPF"] = aborted
    result["evidence"] = {str(folder/name): digest(folder/name) for name in files}
    return result


def check_bindings(target):
    binding = read(target/"input_binding.json")
    verify_hashes(binding["original_sha256"])
    verify_hashes(binding["staged_sha256"])
    prior = read(PARENT/"frozen_attempt2/input_binding.json")
    assert binding["prior_binding"] == prior
    for item in [prior, *prior["old_bindings"]]:
        verify_hashes(item["original_sha256"])
        verify_hashes(item["staged_sha256"])
    seal_path = PARENT/"delivery_manifest.json"
    seal = read(seal_path)
    assert seal["selected_candidate"] == "frozen_attempt2"
    verify_hashes(seal["artifacts_sha256"])
    assert seal["input_binding_sha256"] == digest(PARENT/"frozen_attempt2/input_binding.json")
    baseline = ROOT/"frozen"
    original = read(baseline/"input_binding.json")
    assert original["prior_binding"] == prior
    changed = [PARENT/"run_sppf.py", ROOT/"tests/tb_feature_sppf_client.v"]
    verify_hashes(original["original_sha256"], changed)
    verify_hashes(original["staged_sha256"])
    assert digest(baseline/"run_sppf.py") == original["original_sha256"][str(changed[0])]
    assert digest(baseline/"tests/tb_feature_sppf_client.v") == original["original_sha256"][str(changed[1])]
    old_tb = (baseline/"tests/tb_feature_sppf_client.v").read_text(encoding="utf-8")
    new_tb = changed[1].read_text(encoding="utf-8")
    assert "/pool.%02d.hex" in old_tb and "/pool.%02d.hex" not in new_tb
    assert all(f"/pool.{index:02d}.hex" in new_tb for index in range(3))
    assert "$fopen(stage_path" in new_tb and "VECTOR_FILE_OPEN_REJECTED" in new_tb and "$fclose(vector_handle)" in new_tb
    for candidate in (baseline, target):
        assert digest(candidate/"rtl/road_feature_blocks_client.v") == CLIENT_SHA256
        assert digest(candidate/"tests/tb_feature_blocks_client.v") == digest(PARENT/"frozen_attempt2/tests/tb_feature_blocks_client.v")
        assert digest(candidate/"regression_contract.json") == digest(PARENT/"frozen_attempt2/tb_contract.json")
    assert digest(ROOT/"rtl/road_feature_blocks_client.v") == CLIENT_SHA256
    exceptions = [{"path": str(path), "baseline_sha256": original["original_sha256"][str(path)],
                   "corrected_sha256": digest(path)} for path in changed]
    return binding, dict(baseline_original_only_exceptions=exceptions, baseline_staged_all_verified=True,
                         RTL_changed_between_failed_and_corrected_attempt=False,
                         parent_phase1_delivery_manifest_sha256=digest(seal_path))


def failed_loader_evidence():
    baseline = ROOT/"frozen"
    folder, commands, simulation, _, _ = case_logs(baseline, 0)
    status = read(folder/"status.json")
    assert status["status"] == "FAILED_PRESERVED" and commands[2]["validated_returncode"] != 0
    missing = re.findall(r"Failed to open readmem file[^\r\n]*pool\. ([012])\.hex", simulation)
    assert missing == ["0", "1", "2"] and "FEATURE_SPPF_PASS" not in simulation
    try:
        runner.check_vector_loading(simulation)
    except ValueError:
        rejected = True
    else:
        raise AssertionError("real original failed vector-loading log escaped fail-closed checker")
    match = re.search(r"write mismatch block=5 stage=1 index=0 data=([0-9a-fA-F]+) sum=(-?\d+)", simulation)
    assert match
    observed = int(match.group(1), 16)
    golden = int((PARENT/"reference/sppf/pool.00.hex").read_text(encoding="ascii").splitlines()[0], 16)
    assert observed == golden and int(match.group(2)) == (golden if golden < 128 else golden-256)
    return dict(status="FAILED_PRESERVED_VECTOR_LOADER_NOT_COMPUTE_ACCEPTANCE",
                missing_pool_paths=missing, actual_failed_log_rejected_by_new_runner=rejected,
                first_pool_actual_byte=observed, first_pool_CPU_golden_byte=golden,
                first_pool_value_equal_does_not_qualify_failed_run=True,
                native_returncode=commands[2]["native_returncode"], validated_returncode=commands[2]["validated_returncode"],
                evidence={str(folder/name): digest(folder/name) for name in ("commands.json", "status.json", *LOG_NAMES)})


def finalize(name):
    self_check()
    assert name == "frozen_attempt2"
    target = ROOT/name
    binding, exceptions = check_bindings(target)
    assert binding["payload_sha256"] == runner.PAYLOAD
    contract = read(target/"tb_contract.json")
    expected, prior = expected_counts(target, contract)
    cases = [validate_case(target, case, expected, prior) for case in (0, 1, 2, 3, 99)]
    regression = validate_case(target, 0, expected, prior, regression=True)
    runs = [run for case in [*cases, regression] for run in case["runs"]]
    assert len(runs) == 11 and sum(not run["regression"] for run in runs) == 8
    failed = failed_loader_evidence()
    gates = dict(original=phase1.check_gate(ROOT/"frozen"), corrected=phase1.check_gate(target))
    reference = phase1.check_reference()
    integration = phase1.integration_sources(target)
    sppf_tb = (target/"tests/tb_feature_sppf_client.v").read_text(encoding="utf-8")
    assert len(re.findall(r"\broad_feature_blocks_client\s+client\s*\(", sppf_tb)) == 1
    assert len(re.findall(r"\broad_csp_first_probe\s+arithmetic_Inst\s*\(", sppf_tb)) == 1
    integration["functional_sources"] = {str(PARENT/path): value for path, value in integration["functional_sources"].items()}
    integration.update(CSP4_to_SPPF_actual_logical_memory_dependency=True,
                       SPPF_RTL_in_selected_candidate=True, PAN_RTL_in_selected_candidate=False,
                       cache_port_organization="exclusive PREFETCH write / CACHE_ACTIVATION read / CACHE_BYPASS read / POOL_READ read states",
                       both_testbench_tops_individually_one_client_one_owner=True,
                       upstream_down3_down4_CPU_only=True, physical_shared_cache_mapped=False)
    evidence = {path: value for case in [*cases, regression] for path, value in case["evidence"].items()}
    evidence.update(failed["evidence"])
    for gate in gates.values():
        evidence.update({str(PARENT/path): value for path, value in gate["evidence"].items()})
    evidence.update({str(PARENT/path): value for path, value in reference["evidence"].items()})
    for path in (target/"input_binding.json", ROOT/"frozen/input_binding.json", PARENT/"delivery_manifest.json",
                 PARENT/"finalize.py", PARENT/"run_sppf.py", ROOT/"reference_schedule.py", ROOT/"schedule_report.json"):
        evidence[str(path)] = digest(path)
    handoff = ROOT/"handoff.txt"
    assert handoff.is_file(), "Root phase2 handoff text required before publication"
    evidence[str(handoff)] = digest(handoff)
    assert check_bindings(target) == (binding, exceptions)
    assert phase1.check_reference() == reference
    verify_hashes(evidence)
    ledger = dict(scope="Real same-client CSP4→SPPF logical-memory chain plus original CSP2/3/4 regression",
        clock_hz=100000000, complete_normal_block_runs=11, chain_block_runs=8, original_CSP_regression_block_runs=3,
        runs=runs, sequences=[case for case in cases if case["case"] in (0, 1, 2, 3)],
        checker_negative_prelude_runs_excluded=[run for case in cases for run in case["excluded_negative_prelude_runs"]],
        abort_prefix_and_reset_reload_excluded_from_clean=True,
        endpoint="Accepted start through entering DONE, inclusive; sum stages=sum20 raw states=clean block cycles. Regression retains17-state original TB ledger.",
        system_target_cycles=100000000, whole_system_FPS_qualified=False, controlled_logical_memory_not_real_DDR=True)
    summary = dict(status="CSP4_SPPF_LOGICAL_MEMORY_CHAIN_FUNCTION_PASS_NOT_DEPLOYMENT", selected_candidate=name,
        validated_case_directories=6, chain_cases=4, pool_checker_negative_cases=1, original_CSP_regression_cases=1,
        completed_normal_block_runs=11, completed_chain_block_runs=8, completed_original_CSP_regression_block_runs=3,
        negative_prelude_completed_CSP4_excluded_from_clean=True,
        finalizer_positive_and_mutated_pool_read_negative=True,
        source_binding_original_files=len(binding["original_sha256"]), source_binding_staged_files=len(binding["staged_sha256"]),
        new_parent_old_bindings_and_reference_closures_rechecked_before_after=True,
        preserved_original_binding_exceptions=exceptions, preserved_failed_loader=failed,
        vector_loading_fail_closed=True, CPU_reference=reference,
        independent_SPPF_stage_reads=expected[5]["reads"],
        actual_ModelSim_compile_errors=0, actual_ModelSim_compile_warnings=0,
        simulation_exit_evidence=[{key: case[key] for key in ("case", "regression", "native_returncode", "validated_returncode", "elaboration_warning_lines")} for case in [*cases, regression]],
        strict_gate_comparison=dict(**gates, public_matrix_equal=gates["original"]["checks"] == gates["corrected"]["checks"]),
        payload_sha256=runner.PAYLOAD, image_sha256=binding["image_sha256"],
        CPU_package_qualification="TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED",
        client_sha256=CLIENT_SHA256, tb_sha256=digest(target/"tests/tb_feature_sppf_client.v"),
        finalizer_sha256=digest(Path(__file__)), input_binding_sha256=digest(target/"input_binding.json"),
        CSP4_to_SPPF_actual_logical_memory_dependency_pass=True, SPPF_RTL_in_selected_candidate=True,
        PAN_RTL_in_selected_candidate=False, one_runtime_client=True, one_arithmetic_owner=True,
        arithmetic_changed=False,
        upstream_down3_down4_CPU_only=True, actual_DDR=False, physical_shared_cache_mapped=False,
        full_graph=False, synthesis=False, place_route=False, bitstream=False, board=False,
        accuracy_evaluation=False, FPS_qualification=False, training_updates=0,
        production_delivery_ready=False, evidence=evidence)
    for filename, value in (("cycle_ledger.json", ledger), ("integration_sources.json", integration),
                            ("final_checks.json", summary), ("status.json", summary)):
        save(ROOT/filename, value)
    published = {str(ROOT/name): digest(ROOT/name) for name in (
        "cycle_ledger.json", "integration_sources.json", "final_checks.json", "status.json", "handoff.txt")}
    verify_hashes(published)
    save(ROOT/"delivery_manifest.json", dict(status=summary["status"], selected_candidate=name,
        artifacts_sha256=published, finalizer_sha256=digest(Path(__file__)),
        input_binding_sha256=digest(target/"input_binding.json"), payload_sha256=runner.PAYLOAD,
        production_delivery_ready=False))
    print("SEALED_CSP4_SPPF_LOGICAL_MEMORY_CHAIN_FUNCTION_ONLY", len(runs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="frozen_attempt2")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("SPPF_FINALIZER_POSITIVE_AND_MUTATED_POOL_READ_NEGATIVE_PASS")
    else:
        finalize(args.name)
