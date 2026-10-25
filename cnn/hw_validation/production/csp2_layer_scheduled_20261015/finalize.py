"""只核验已保存的完整回归并发布交接；不重新仿真、训练、综合或改冻结文件。"""
import argparse
import copy
import re

from run import CORES, OLD, ROOT, digest, read, save, verify

EXPECTED = dict(outputs=[110592]*4+[221184], tasks=[55296,36864,55296,36864,73728],
                groups=[110592,73728,110592,73728,221184],
                reads=[30210,20736,16748,13824,27648],
                parameters=[27648,4608,27648,4608,13824])


def fields(marker):
    return {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", marker)}


def validate_run(run, stages, states):
    """各层源读/驻留参数和任务数量均独立于TB的PASS标记核验。"""
    assert len(stages) == 5 and sorted(row["stage"] for row in stages) == list(range(5))
    assert len(states) == 17 and sorted(row["state"] for row in states) == list(range(17))
    for stage in stages:
        index = stage["stage"]
        assert all(stage[key] == expected[index] for key, expected in EXPECTED.items())
        assert stage["barriers"] == 1
    assert all(run[key] == sum(expected) for key, expected in EXPECTED.items())
    assert all(run[key] == 663552 for key in ("acc", "pre", "silu", "post"))
    assert run["barriers"] == 5
    assert sum(row["cycles"] for row in stages) == run["cycles"]
    assert sum(row["cycles"] for row in states) == run["cycles"] == run["accounted"]


def self_check():
    run = {key: sum(value) for key, value in EXPECTED.items()}
    run.update(acc=663552, pre=663552, silu=663552, post=663552, barriers=5, cycles=5, accounted=5)
    stages = [dict(stage=index, cycles=1, barriers=1,
                   **{key: value[index] for key, value in EXPECTED.items()}) for index in range(5)]
    states = [dict(state=index, cycles=int(index < 5)) for index in range(17)]
    validate_run(run, stages, states)
    bad = copy.deepcopy(stages)
    bad[0]["reads"] += 1
    try:
        validate_run(run, bad, states)
    except AssertionError:
        return
    raise AssertionError("finalizer failed to reject mutated read count")


def finalize(name):
    self_check()
    target = ROOT / name
    binding = read(target / "input_binding.json")
    verify(binding["original_sha256"])
    verify(binding["staged_sha256"])
    paths = ["verification_case0", "verification_case1", "verification_case2",
             "verification_case3", "verification_case4", "verification_case5_kind0",
             "verification_case5_kind1", "verification_case99"]
    evidence = {}
    complete_runs = []
    for relative in paths:
        folder = target / relative
        status = read(folder / "status.json")
        negative = relative == "verification_case99"
        assert status["status"] == ("PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE")
        commands = read(folder / "commands.json")
        assert len(commands) == 3
        for command, filename in zip(commands, ("vlib.log", "compile.log", "simulation.log"), strict=True):
            verify({str(folder / filename): command["log_sha256"]})
        simulation = (folder / "simulation.log").read_text(encoding="utf-8")
        compilation = (folder / "compile.log").read_text(encoding="utf-8")
        assert re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compilation)[-1] == ("0", "0")
        if negative:
            assert commands[-1]["validated_returncode"] != 0
            assert "NEGATIVE_ACC injected acc mismatch" in simulation and "CSP_LAYER_PASS" not in simulation
        else:
            assert commands[-1]["validated_returncode"] == 0
            assert not re.search(r"\*\* (?:Error|Fatal):", simulation)
            receipt = read(folder / "receipt.json")
            assert receipt["stage_ledger"] == re.findall(r"CSP_LAYER_STAGE [^\r\n]*", simulation)
            assert receipt["state_ledger"] == re.findall(r"CSP_LAYER_STATE [^\r\n]*", simulation)
            assert receipt["measured_runs"] == re.findall(r"CSP_LAYER_RUN [^\r\n]*", simulation)
            assert receipt["marker"] in simulation and receipt["fields"] == fields(receipt["marker"])
            parsed_stages = list(map(fields, receipt["stage_ledger"]))
            parsed_states = list(map(fields, receipt["state_ledger"]))
            for marker in receipt["measured_runs"]:
                run = fields(marker)
                stages = [row for row in parsed_stages if row["run"] == run["run"]]
                states = [row for row in parsed_states if row["run"] == run["run"]]
                validate_run(run, stages, states)
                counters = {row["state"]: row["cycles"] for row in states}
                categories = dict(input_prefetch=sum(counters[index] for index in (2,3,4)),
                    parameter_prefetch=counters[5]+counters[6],
                    task_tile_setup=counters[1]+counters[7],
                    local_operand_assembly=counters[8]+counters[9],
                    accepted_core_groups=run["groups"],
                    core_admission_wait=counters[10]-run["groups"],
                    arithmetic_pipeline_and_output_retirement=counters[11],
                    registered_retire_and_advance=counters[12]+counters[13],
                    layer_visibility_barrier=counters[14],
                    other_control=counters[0]+counters[15]+counters[16])
                assert all(value >= 0 for value in categories.values())
                assert sum(categories.values()) == run["cycles"]
                complete_runs.append(dict(case=run["case"], run=run["run"], endpoint=run,
                    stages=stages, exclusive_cycles=categories,
                    retirement_window_is_not_pure_idle=True))
        evidence[relative] = {str(p.relative_to(ROOT)): digest(p) for p in folder.iterdir()
                              if p.is_file() and p.name in ("commands.json", "status.json", "receipt.json", "compile.log", "simulation.log")}
    assert len(complete_runs) == 4
    normal = complete_runs[0]["endpoint"]["cycles"]
    random_cycles = next(row["endpoint"]["cycles"] for row in complete_runs if row["case"] == 1 and row["run"] == 2)
    gate = read(target / "static_gate/gate.json")
    old_cycles = 59619664
    ledger = dict(scope="real-road full72x128 CSP2 only; not full CNN/video/DDR/FPS",
        clock_hz=100000000, LUT_preload_excluded=True, runs=complete_runs,
        normal_cycles=normal, random_cycles=random_cycles, management_target_cycles=8000000,
        management_target_met=normal <= 8000000, excess_cycles=max(0,normal-8000000),
        old_tile_route_conditional_projection=old_cycles,
        projection_not_full_frame_measurement=True,
        fraction_of_system_2FPS_budget=normal/50000000,
        fraction_of_system_1FPS_alternative_budget=normal/100000000,
        system_2FPS_budget=50000000, system_1FPS_alternative_budget=100000000,
        result_expiry_ms=500, whole_system_FPS_qualified=False,
        waits_include_controlled_endpoint_not_real_DDR=True)
    save(ROOT / "cycle_ledger.json", ledger)
    sources = {str(p.relative_to(ROOT)): digest(p) for p in (target / "reused").glob("*.v")}
    sources[str((target / "rtl/road_csp_layer_client.v").relative_to(ROOT))] = digest(target / "rtl/road_csp_layer_client.v")
    assert len(sources) == 7
    for module in CORES:
        assert digest(target / "reused" / (module+".v")) == digest(OLD / "frozen_attempt2/reused" / (module+".v"))
    save(ROOT / "integration_sources.json", dict(functional_sources=sources,
        client_MAC_instances=0, testbench_one_arithmetic_owner=True,
        physical_top_selected=False, real_DDR_connected=False))
    summary = dict(status="FULL_FRAME_CSP2_FUNCTION_PASS_8M_BUDGET_NOT_MET_NOT_DEPLOYMENT",
        selected_candidate=name, functional_cases=7, completed_full_frame_runs=4,
        values_per_full_run=663552, checker_negative_pass=True,
        finalizer_positive_and_mutated_read_negative=True,
        normal_cycles=normal, random_cycles=random_cycles, CSP2_8M_target_met=normal <= 8000000,
        source_binding_original_files=len(binding["original_sha256"]),
        source_binding_staged_files=len(binding["staged_sha256"]),
        payload_sha256=binding["payload_sha256"], image_sha256=binding["image_sha256"],
        client_sha256=digest(target / "rtl/road_csp_layer_client.v"),
        tb_sha256=digest(target / "tests/tb_csp_layer_client.v"),
        original_and_staged_inputs_rechecked=True, arithmetic_changed=False,
        actual_ModelSim_compile_errors=0, actual_ModelSim_compile_warnings=0,
        preserved_elaboration_warnings=12,
        strict_public_matrix={key: value["status"] for key, value in gate["checks"].items()}, strict_errors=gate["errors"],
        strict_warnings=gate["strict_warnings"], strict_delivery_ready=gate["delivery_ready"],
        actual_DDR=False, ROM_reader_connected=False, unique_owner_integrated=False,
        full_CSP2_frame_RTL=True, full_graph=False, training_updates=0,
        synthesis=False, place_route=False, bitstream=False, board=False,
        accuracy_evaluation=False, FPS_qualification=False, expiry_ms=500,
        deployment_delivery_ready=False, evidence=evidence)
    save(ROOT / "final_checks.json", summary)
    save(ROOT / "status.json", summary)
    print("SEALED_FULL_FRAME_CSP2_FUNCTION_ONLY_8M_NOT_MET", normal, random_cycles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("FINALIZER_POSITIVE_AND_MUTATED_READ_NEGATIVE_PASS")
    else:
        finalize(args.name)
