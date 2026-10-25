"""核验已保存的CSP3/CSP4回归并发布交接；不重新仿真、综合或训练。"""
import argparse
import copy
import re
from pathlib import Path

from run import CORES, MODEL, PRIOR, ROOT, VENDOR, digest, read, save


COUNT_KEYS = ("outputs", "tasks", "groups", "reads", "parameters")
LOG_NAMES = ("vlib.log", "compile.log", "simulation.log")


def fields(marker):
    return {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", marker)}


def verify_hashes(mapping, allowed_mismatches=()):
    """拒绝空/占位哈希，并只允许调用方明确列出的已知差异。"""
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


def expected_counts(family_contract, tb_contract, family):
    reference = family_contract["families"][f"csp{family}"]["stages"]
    assert [stage["stage"] for stage in reference] == list(range(7))
    expected = dict(
        outputs=[stage["logical_output_elements"] for stage in reference],
        tasks=[stage["task_count"] for stage in reference],
        groups=[stage["accepted_core_groups"] for stage in reference],
        reads=[stage["expected_read_requests"] for stage in reference],
        parameters=[stage["expected_parameter_requests"] for stage in reference],
    )
    tb = tb_contract["family_counts"][str(family)]
    for key in COUNT_KEYS:
        assert tb[f"stage_{key}"] == expected[key]
    assert tb["outputs"] == sum(expected["outputs"])
    assert tb["tasks"] == sum(expected["tasks"])
    assert tb["groups"] == sum(expected["groups"])
    assert tb["barriers"] == 7
    return expected


def validate_run(run, stages, states, expected, family, case):
    assert len(stages) == 7 and sorted(row["stage"] for row in stages) == list(range(7))
    assert len(states) == 17 and sorted(row["state"] for row in states) == list(range(17))
    assert run["family"] == family and run["case"] == case and run["cycles"] > 0
    for stage in stages:
        index = stage["stage"]
        assert stage["family"] == family and stage["case"] == case and stage["run"] == run["run"]
        assert all(stage[key] == expected[key][index] for key in COUNT_KEYS)
        assert stage["barriers"] == 1 and stage["cycles"] >= 0
    for state in states:
        assert state["family"] == family and state["case"] == case and state["run"] == run["run"]
        assert state["cycles"] >= 0
    assert all(run[key] == sum(expected[key]) for key in COUNT_KEYS)
    assert all(run[key] == sum(expected["outputs"]) for key in ("acc", "pre", "silu", "post"))
    assert run["barriers"] == 7
    assert sum(row["cycles"] for row in stages) == run["cycles"]
    assert sum(row["cycles"] for row in states) == run["cycles"] == run["accounted"]


def self_check():
    expected = {key: [index + offset for index in range(7)]
                for offset, key in enumerate(COUNT_KEYS, start=1)}
    stages = [dict(family=3, case=0, run=1, stage=index, cycles=1, barriers=1,
                   **{key: expected[key][index] for key in COUNT_KEYS}) for index in range(7)]
    states = [dict(family=3, case=0, run=1, state=index, cycles=int(index < 7))
              for index in range(17)]
    run = {key: sum(values) for key, values in expected.items()}
    run.update(family=3, case=0, run=1, cycles=7, accounted=7, barriers=7,
               acc=sum(expected["outputs"]), pre=sum(expected["outputs"]),
               silu=sum(expected["outputs"]), post=sum(expected["outputs"]))
    validate_run(run, stages, states, expected, 3, 0)
    mutated = copy.deepcopy(stages)
    mutated[0]["reads"] += 1
    try:
        validate_run(run, mutated, states, expected, 3, 0)
    except AssertionError:
        return
    raise AssertionError("finalizer failed to reject mutated read count")


def case_folder(target, family, case, kind=0):
    suffix = f"_kind{kind}" if case == 5 else ""
    return target / f"family{family}_case{case}{suffix}"


def contract_entry(tb_contract, case, kind):
    entries = [entry for entry in tb_contract["runner_cases"] if entry["case"] == case and
               (case != 5 or f"+FAULT_KIND={kind}" in entry.get("plusargs", []))]
    assert len(entries) == 1
    return entries[0]


def validate_case(target, family, case, kind, expected, tb_contract):
    folder = case_folder(target, family, case, kind)
    negative = case == 99
    status = read(folder / "status.json")
    assert status["status"] == ("PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE")
    assert status["family"] == family and status["case"] == case
    commands = read(folder / "commands.json")
    assert len(commands) == 3
    for command, filename in zip(commands, LOG_NAMES, strict=True):
        assert re.fullmatch(r"[0-9a-fA-F]{64}", command.get("log_sha256", ""))
        assert digest(folder / filename).lower() == command["log_sha256"].lower()
        assert Path(command["cwd"]).resolve() == folder.resolve()
    assert commands[0]["argv"] == [str(MODEL / "vlib.exe"), "work"]
    sources = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
    sources += [target / "reused" / f"{module}.v" for module in CORES]
    sources += [target / "rtl/road_csp_family_client.v", target / "tests/tb_csp_family_client.v"]
    assert commands[1]["argv"] == [str(MODEL / "vlog.exe"), "-work", "work", *map(str, sources)]
    assert all(command["native_returncode"] == command["validated_returncode"] == 0
               for command in commands[:2])
    compilation = (folder / "compile.log").read_text(encoding="utf-8")
    simulation = (folder / "simulation.log").read_text(encoding="utf-8")
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compilation)
    assert summaries and summaries[-1] == ("0", "0")
    assert len(re.findall(r"(?m)^# \*\* Warning:", simulation)) == 12
    argv = commands[-1]["argv"]
    assert "tb_csp_family_client" in argv and f"-gC_FAMILY={family}" in argv
    assert f"+CASE={0 if negative else case}" in argv
    assert any(value.endswith(f"/reference/csp{family}") for value in argv)
    entry = contract_entry(tb_contract, case, kind)
    for plusarg in entry.get("plusargs", []):
        assert plusarg in argv
    if negative:
        assert commands[-1]["validated_returncode"] != 0
        assert "NEGATIVE_ACC injected acc mismatch" in simulation
        assert "CSP_FAMILY_PASS" not in simulation and "+NEGATIVE_ACC=1" in argv
        files = ("commands.json", "status.json", *LOG_NAMES)
        return [], {str((folder / name).relative_to(ROOT)): digest(folder / name) for name in files}

    assert commands[-1]["validated_returncode"] == 0
    assert not re.search(r"\*\* (?:Error|Fatal):", simulation)
    receipt = read(folder / "receipt.json")
    assert receipt["stage_ledger"] == re.findall(r"CSP_FAMILY_STAGE [^\r\n]*", simulation)
    assert receipt["state_ledger"] == re.findall(r"CSP_FAMILY_STATE [^\r\n]*", simulation)
    assert receipt["measured_runs"] == re.findall(r"CSP_FAMILY_RUN [^\r\n]*", simulation)
    markers = re.findall(r"CSP_FAMILY_(?:PASS|EXPECTED_FAULT) [^\r\n]*", simulation)
    assert markers == [receipt["marker"]] and receipt["marker"].startswith(entry["marker"])
    assert receipt["fields"] == fields(receipt["marker"])
    assert receipt["fields"]["family"] == family and receipt["fields"]["case"] == case
    wanted = entry.get("expected_fields_by_family", {}).get(str(family), entry.get("expected_fields", {}))
    assert all(receipt["fields"].get(key) == value for key, value in wanted.items())

    runs = []
    if case in (0, 1, 2):
        assert len(receipt["measured_runs"]) == 1 and receipt["fields"]["runs"] == 1
        parsed_stages = list(map(fields, receipt["stage_ledger"]))
        parsed_states = list(map(fields, receipt["state_ledger"]))
        run = fields(receipt["measured_runs"][0])
        assert all(receipt["fields"][key] == value for key, value in run.items() if key != "run")
        stages = [row for row in parsed_stages if row["run"] == run["run"]]
        states = [row for row in parsed_states if row["run"] == run["run"]]
        validate_run(run, stages, states, expected, family, case)
        counters = {row["state"]: row["cycles"] for row in states}
        categories = dict(
            input_prefetch=sum(counters[index] for index in (2, 3, 4)),
            parameter_prefetch=counters[5] + counters[6],
            task_tile_setup=counters[1] + counters[7],
            local_operand_assembly=counters[8] + counters[9],
            accepted_core_groups=run["groups"],
            core_admission_wait=counters[10] - run["groups"],
            arithmetic_pipeline_and_output_retirement=counters[11],
            registered_retire_and_advance=counters[12] + counters[13],
            layer_visibility_barrier=counters[14],
            other_control=counters[0] + counters[15] + counters[16],
        )
        assert all(value >= 0 for value in categories.values())
        assert sum(categories.values()) == run["cycles"]
        runs.append(dict(family=family, case=case, run=run["run"], endpoint=run,
                         stages=stages, states=states, exclusive_cycles=categories,
                         retirement_window_is_not_pure_idle=True))
    else:
        assert not receipt["measured_runs"] and not receipt["stage_ledger"] and not receipt["state_ledger"]
    files = ("commands.json", "status.json", "receipt.json", *LOG_NAMES)
    evidence = {str((folder / name).relative_to(ROOT)): digest(folder / name) for name in files}
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in evidence.values())
    return runs, evidence


def finalize(name):
    self_check()
    target = ROOT / name
    assert target.is_dir()
    family_contract = read(target / "reference/family_contract.json")
    tb_contract = read(target / "tb_contract.json")
    reference_status = read(target / "reference/status.json")
    assert family_contract["schema"] == "csp_family_layer_reference_v2_residual_bypass_corrected"
    assert reference_status["old_wrong_dw_post_bypass_rejected_for_all_six_real_residuals"] is True
    residual_negatives = []
    for family in (3, 4):
        rows = reference_status["graph_nonconv_named_input_checks"][f"csp{family}"]["real_road_old_wrong_bypass_negative"]
        assert [row["stage"] for row in rows] == [1, 3, 5]
        assert all(row["old_wrong_rejected"] and row["mismatch_values"] > 0 and
                   row["graph_bypass"] != row["old_wrong_bypass"] for row in rows)
        residual_negatives.extend(dict(family=family, **row) for row in rows)
    assert len(residual_negatives) == 6

    binding = read(target / "input_binding.json")
    verify_hashes(binding["original_sha256"])
    verify_hashes(binding["staged_sha256"])
    prior_binding = read(PRIOR / "frozen/input_binding.json")
    assert binding["prior_CSP2_original_sha256"] == prior_binding["original_sha256"]
    assert binding["prior_CSP2_staged_sha256"] == prior_binding["staged_sha256"]
    verify_hashes(binding["prior_CSP2_original_sha256"])
    verify_hashes(binding["prior_CSP2_staged_sha256"])

    attempt1 = ROOT / "frozen"
    attempt1_binding = read(attempt1 / "input_binding.json")
    root_run = ROOT / "run.py"
    mismatch = verify_hashes(attempt1_binding["original_sha256"], (root_run,))
    verify_hashes(attempt1_binding["staged_sha256"])
    attempt1_expected_run = attempt1_binding["original_sha256"][str(root_run)]
    assert mismatch == [str(root_run)]
    assert digest(attempt1 / "run.py") == attempt1_expected_run
    attempt1_reference_count = sum("reference" in Path(path).parts
                                   for path in attempt1_binding["staged_sha256"])
    assert attempt1_reference_count > 0

    expected_by_family = {family: expected_counts(family_contract, tb_contract, family)
                          for family in (3, 4)}
    runs, evidence = [], {}
    cases = ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (99, 0))
    for family in (3, 4):
        for case, kind in cases:
            measured, case_evidence = validate_case(target, family, case, kind,
                                                     expected_by_family[family], tb_contract)
            runs.extend(measured)
            evidence.update(case_evidence)
    assert len(runs) == 6
    assert sorted((row["family"], row["case"]) for row in runs) == [
        (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2)]

    original_gate = read(ROOT / "frozen/static_gate/gate.json")
    corrected_gate = read(target / "static_gate/gate.json")
    for gate in (original_gate, corrected_gate):
        assert gate["delivery_ready"] is False and gate["errors"] == 3363 and gate["strict_warnings"] == 5
    original_matrix = {key: value["status"] for key, value in original_gate["checks"].items()}
    corrected_matrix = {key: value["status"] for key, value in corrected_gate["checks"].items()}
    assert corrected_matrix == original_matrix
    for gate_root in (ROOT / "frozen/static_gate", target / "static_gate"):
        gate_command = read(gate_root / "command.json")
        verify_hashes({str(gate_root / "run.log"): gate_command["log_sha256"]})
        assert gate_command["returncode"] == 1
        for filename in ("gate.json", "gate.md", "command.json", "run.log"):
            evidence[str((gate_root / filename).relative_to(ROOT))] = digest(gate_root / filename)

    by_family = {}
    for family in (3, 4):
        selected = {row["case"]: row["endpoint"]["cycles"] for row in runs if row["family"] == family}
        assert set(selected) == {0, 1, 2}
        by_family[str(family)] = dict(normal_cycles=selected[0], random_cycles=selected[1],
                                      reset_restart_cycles=selected[2],
                                      normal_within_system_1FPS_budget=selected[0] <= 100000000)
    ledger = dict(scope="CSP3/CSP4 seven-stage ModelSim function only; not full graph, DDR, synthesis, board or FPS qualification",
                  clock_hz=100000000, LUT_preload_excluded=True, runs=runs, families=by_family,
                  system_1FPS_budget_cycles=100000000, result_expiry_ms=500,
                  budget_comparison_is_not_whole_system_FPS_qualification=True,
                  whole_system_FPS_qualified=False, waits_include_controlled_endpoint_not_real_DDR=True)

    sources = {str(path.relative_to(ROOT)): digest(path) for path in (target / "reused").glob("*.v")}
    client = target / "rtl/road_csp_family_client.v"
    sources[str(client.relative_to(ROOT))] = digest(client)
    assert len(CORES) == 6 and len(sources) == 7
    for module in CORES:
        assert digest(target / "reused" / f"{module}.v") == digest(PRIOR / "frozen/reused" / f"{module}.v")
    tb_text = (target / "tests/tb_csp_family_client.v").read_text(encoding="utf-8")
    client_text = client.read_text(encoding="utf-8")
    assert len(re.findall(r"\broad_csp_first_probe\s+arithmetic_Inst\s*\(", tb_text)) == 1
    assert not re.search(r"\b(?:road_csp_first_probe|road_mac_probe|road_dynamic_postprocess)\s+\w+\s*\(", client_text)
    integration = dict(functional_sources=sources, reused_arithmetic_files=6, client_MAC_instances=0,
                       testbench_one_arithmetic_owner=True, physical_shared_cache_integrated=False,
                       actual_DDR_connected=False, full_graph_integrated=False)

    run_exception = dict(path=str(root_run), expected_attempt1_sha256=attempt1_expected_run,
                         actual_corrected_sha256=digest(root_run), only_original_binding_exception=True,
                         reason="root runner intentionally selects corrected reference_attempt2",
                         staged_attempt1_run_unchanged=True,
                         staged_attempt1_run_sha256=digest(attempt1 / "run.py"))
    summary = dict(status="CSP3_CSP4_FUNCTION_PASS_NOT_DEPLOYMENT", selected_candidate=name,
                   validated_case_directories=16, positive_or_expected_fault_cases=14,
                   checker_negative_cases=2, completed_full_frame_runs=6,
                   family_output_values_per_full_run={str(f): sum(expected_by_family[f]["outputs"]) for f in (3, 4)},
                   finalizer_positive_and_mutated_read_negative=True,
                   corrected_real_residual_negatives=residual_negatives,
                   all_six_old_wrong_residual_bypasses_rejected=True,
                   source_binding_original_files=len(binding["original_sha256"]),
                   source_binding_staged_files=len(binding["staged_sha256"]),
                   prior_CSP2_binding_rechecked=True, old_reference_artifacts_unchanged=True,
                   preserved_attempt1_root_run_exception=run_exception,
                   payload_sha256=binding["payload_sha256"], image_sha256=binding["image_sha256"],
                   client_sha256=digest(client), tb_sha256=digest(target / "tests/tb_csp_family_client.v"),
                   arithmetic_changed=False, actual_ModelSim_compile_errors=0,
                   actual_ModelSim_compile_warnings=0,
                   actual_ModelSim_elaboration_warnings_per_case=12,
                   preserved_diagnostic_port_warnings=9, preserved_vendor_INIT_warnings=2,
                   preserved_port_connection_count_warning=1,
                   strict_gate_comparison_preserved=dict(original_errors=3363, original_warnings=5,
                       corrected_errors=3363, corrected_warnings=5, public_matrix_unchanged=True,
                       delivery_ready=False, checks=corrected_matrix),
                   actual_DDR=False, physical_shared_cache_integrated=False, full_graph=False,
                   synthesis=False, place_route=False, bitstream=False, board=False,
                   accuracy_evaluation=False, FPS_qualification=False, expiry_ms=500,
                   training_updates=0, production_delivery_ready=False, evidence=evidence)
    summary["finalizer_sha256"] = digest(Path(__file__))
    summary["input_binding_sha256"] = digest(target / "input_binding.json")
    summary["reference_manifest_sha256"] = digest(target / "reference/manifest.json")
    summary["preserved_failed_attempts"] = {
        "first_reference_mismatch_status_sha256": digest(ROOT / "frozen/family3_case0/status.json"),
        "sandbox_launch_failure_status_sha256": digest(ROOT / "frozen_attempt2/family3_case0/status.json"),
    }
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in evidence.values())
    save(ROOT / "cycle_ledger.json", ledger)
    save(ROOT / "integration_sources.json", integration)
    save(ROOT / "final_checks.json", summary)
    save(ROOT / "status.json", summary)
    published = {str(ROOT / filename): digest(ROOT / filename) for filename in (
        "cycle_ledger.json", "integration_sources.json", "final_checks.json", "status.json",
        "PAN依赖与缓存交接.txt", "交接_CSP3_CSP4全幅回归_20261015.txt")}
    verify_hashes(published)
    save(ROOT / "delivery_manifest.json", dict(status=summary["status"],
        selected_candidate=name, artifacts_sha256=published,
        finalizer_sha256=digest(Path(__file__)), input_binding_sha256=digest(target / "input_binding.json"),
        payload_sha256=binding["payload_sha256"], production_delivery_ready=False))
    print("SEALED_CSP3_CSP4_FUNCTION_ONLY_NOT_DEPLOYMENT",
          by_family["3"]["normal_cycles"], by_family["4"]["normal_cycles"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="frozen_attempt3")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("FINALIZER_POSITIVE_AND_MUTATED_READ_NEGATIVE_PASS")
    else:
        finalize(args.name)
