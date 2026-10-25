"""核验已有物理工作仓证据并封存；不运行仿真、综合或修改冻结源。"""

import argparse
import copy
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import run as runner

ROOT, PRIOR, SELECTED = runner.ROOT, runner.PRIOR, runner.SELECTED
digest, read, save = runner.digest, runner.read, runner.save
COUNT_KEYS = ("outputs", "tasks", "groups", "reads", "parameters")
NUMERIC_KEYS = ("acc", "pre", "silu", "post")
LOG_NAMES = ("vlib.log", "compile.log", "simulation.log")
PUBLIC_GATES = {"compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"}
REQUIRED = [("workstore", case) for case in (0, 1, 99)]
REQUIRED += [("csp", case) for case in (0, 1, 2, 3, 4, 5, 99)]
REQUIRED += [("sppf", case) for case in (0, 1, 2, 3, 99)]
TOPS = dict(workstore="tb_feature_workstore", csp="tb_feature_blocks_client", sppf="tb_feature_sppf_client")
NEGATIVES = dict(workstore="NEGATIVE_WORKSTORE", csp="NEGATIVE_ACC", sppf="NEGATIVE_POOL")
PREFIXES = dict(workstore="FEATURE_WORKSTORE", csp="FEATURE_BLOCKS", sppf="FEATURE_SPPF")


def fields(marker):
    """复用旧finalizer整数marker规则，同时拒绝重复字段。"""
    pairs = re.findall(r"(\w+)=(\d+)", marker)
    assert pairs and len({key for key, _ in pairs}) == len(pairs), marker
    return {key: int(value) for key, value in pairs}


def verify_hashes(mapping):
    """严格重算每个绑定文件；本批不允许静默哈希例外。"""
    assert mapping
    for raw_path, expected in mapping.items():
        path = Path(raw_path)
        assert re.fullmatch(r"[0-9a-fA-F]{64}", expected or ""), raw_path
        assert path.is_file() and digest(path).lower() == expected.lower(), raw_path


def evidence(paths):
    return {str(path): digest(path) for path in paths}


def check_bindings(target, storage):
    """旧绑定递归验证由已有runner负责；明确区分旧草案与准确WIF1。"""
    result = {}
    for candidate, storage_only in ((storage, True), (target, False)):
        binding = runner.check_binding(candidate)
        assert binding["storage_only"] is storage_only
        assert binding["actual_DDR"] is False and binding["synthesis"] is False
        live_doc, staged_doc = ROOT / "workstore_interface.txt", candidate / "workstore_interface.txt"
        assert str(staged_doc) in binding["staged_sha256"]
        if storage_only:
            assert str(live_doc) not in binding["original_sha256"]
            assert digest(staged_doc) == "1d826729b5191f6586fae14892bb33fb0645074e28f909c1be87f07ef29e73dd"
        else:
            assert binding["original_sha256"][str(live_doc)] == digest(staged_doc) == digest(live_doc)
        result[candidate.name] = dict(input_binding_sha256=digest(candidate / "input_binding.json"),
            original_files=len(binding["original_sha256"]), staged_files=len(binding["staged_sha256"]),
            live_WIF1_bound=not storage_only, staged_WIF1_sha256=digest(staged_doc))
    return result


def expected_counts(target):
    """计数继承旧CSP/SPPF封存合同；不从本次日志反推期望。"""
    contracts = read(target / "tb_contract.json")["modes"]
    old = dict(csp=read(PRIOR / "frozen_attempt2/tb_contract.json"),
               sppf=read(SELECTED / "tb_contract.json"))
    expected = {}
    for mode in ("csp", "sppf"):
        contract = contracts[mode]
        assert contract["raw_states"] == list(range(28))
        assert contract["sequence_counts"] == old[mode]["sequence_counts"]
        assert contract["block_counts"] == old[mode]["block_counts"]
        assert contract["runner_cases"] == old[mode]["runner_cases"]
        assert contract["marker_fields"] == old[mode]["marker_fields"]
        assert contract["cycle_contract"]["clean_budget_cycles_exclusive"] is None
        expected[mode] = {}
        for block, row in contract["block_counts"].items():
            counts = {key: row["stage_" + key] for key in COUNT_KEYS}
            counts["numeric"] = row.get("stage_numeric", counts["outputs"])
            assert all(len(values) == (5 if int(block) in (2, 5) else 7) for values in counts.values())
            assert all(row[key] == sum(counts[key]) for key in COUNT_KEYS)
            assert row["barriers"] == len(counts["outputs"])
            expected[mode][int(block)] = counts
    assert expected["csp"][2]["outputs"] == [110592] * 4 + [221184]
    assert expected["sppf"][5]["numeric"] == [13824, 0, 0, 0, 55296]
    assert expected["sppf"][5]["reads"] == [3456, 3060, 3060, 3060, 4608]
    return contracts, expected


def validate_stage_counts(stages, expected):
    assert sorted(row["stage"] for row in stages) == list(range(len(expected["outputs"])))
    for row in stages:
        assert all(row[key] == expected[key][row["stage"]] for key in COUNT_KEYS), row
        assert row["barriers"] == 1


def exclusive_cycles(run, states):
    """28态互斥账本；所有native请求与响应等待均在原端点窗口内。"""
    counters = {row["state"]: row["cycles"] for row in states}
    pools = run.get("pools", 0)
    categories = dict(input_prefetch=sum(counters[index] for index in (2, 3, 4)),
        parameter_prefetch=counters[5] + counters[6], task_tile_setup=counters[1] + counters[7],
        local_operand_request=counters[8] + counters[9], accepted_core_groups=run["groups"],
        core_admission_wait=counters[10] - run["groups"], arithmetic_and_output_retirement=counters[11],
        registered_retire_and_advance=counters[12] + counters[13], layer_visibility_barrier=counters[14],
        other_control=counters[0] + counters[15] + counters[16], pool_byte_request=counters[17],
        pool_signed_compare=counters[18], pool_accepted_write=pools,
        pool_write_backpressure=counters[19] - pools, byte_prefetch_commit_wait=counters[20],
        weight_write_request=counters[21], weight_write_commit_wait=counters[22],
        activation_read_response_wait=counters[23], bypass_read_response_wait=counters[24],
        pool_read_response_wait=counters[25], weight_read_request=counters[26],
        weight_read_response_wait=counters[27])
    assert all(value >= 0 for value in categories.values())
    assert sum(categories.values()) == run["cycles"]
    return categories


def validate_run(run, stages, states, expected, block, case, number):
    assert (run["block"], run["case"], run["run"]) == (block, case, number)
    assert len(states) == 28 and sorted(row["state"] for row in states) == list(range(28))
    validate_stage_counts(stages, expected)
    for row in [*stages, *states]:
        assert (row["block"], row["case"], row["run"]) == (block, case, number)
        assert row["cycles"] >= 0
    assert all(run[key] == sum(expected[key]) for key in COUNT_KEYS)
    assert all(run[key] == sum(expected["numeric"]) for key in NUMERIC_KEYS)
    assert run["barriers"] == len(expected["outputs"])
    assert sum(row["cycles"] for row in stages) == sum(row["cycles"] for row in states)
    assert sum(row["cycles"] for row in states) == run["cycles"] == run["accounted"] > 0
    pools = 41472 if block == 5 else 0
    if "pools" in run:
        assert run["pools"] == pools and run["concat_values"] == (1769472 if block == 5 else 0)
    counter = {row["state"]: row["cycles"] for row in states}
    assert counter[18] == 25 * pools and counter[17] >= 25 * pools and counter[25] >= 25 * pools
    if block != 5:
        assert counter[17] == counter[18] == counter[19] == counter[25] == 0
    assert counter[21] >= run["parameters"] and counter[22] >= run["parameters"]
    assert counter[26] >= run["groups"] and counter[27] >= run["groups"]
    return exclusive_cycles(run, states)


def command_logs(folder, expected_argv=None):
    commands = read(folder / "commands.json")
    assert len(commands) == (3 if expected_argv is not None else 1)
    texts = []
    names = LOG_NAMES if expected_argv is not None else ("simulation.log",)
    for index, (record, filename) in enumerate(zip(commands, names, strict=True)):
        verify_hashes({str(folder / filename): record["log_sha256"]})
        assert Path(record["cwd"]).resolve() == folder.resolve()
        if expected_argv is not None:
            assert record["argv"] == list(map(str, expected_argv[index])), record["argv"]
        text = (folder / filename).read_text(encoding="utf-8")
        effective = record["native_returncode"] or int(bool(re.search(r"\*\* (?:Error|Fatal):", text)))
        assert record["validated_returncode"] == effective
        texts.append(text)
    return commands, texts


def validate_storage(marker, contract, case):
    entry, = [row for row in contract["runner_cases"] if row["case"] == case]
    assert set(marker) == set(contract["marker_fields"][entry["marker"]])
    assert marker["case"] == case
    assert all(marker[key] == value for key, value in entry["expected_fields"].items())
    for channel in ("byte", "weight"):
        assert marker["accepted_" + channel] == marker["retired_" + channel] + marker["aborted_" + channel]
        assert marker["held_" + channel] > 0 and marker[channel + "_replace"] == 1
    assert marker["simultaneous"] > 0 and marker["cycles"] > 0
    if case == 1:
        assert marker["held_byte"] >= 256 and marker["held_weight"] >= 256


def validate_sequence(marker, runs, aborted, mode, case, contract):
    assert all(marker[key] == value for key, value in contract["sequence_counts"].items())
    keys = (*COUNT_KEYS, *NUMERIC_KEYS, "barriers")
    if mode == "sppf":
        keys += ("pools", "concat_values")
    assert all(marker[key] == sum(row[key] for row in runs) for key in keys)
    assert marker["cycles"] == marker["accounted"] == sum(row["cycles"] for row in runs)
    assert marker["sequence_cycles"] == marker["cycles"] + marker["overhead_cycles"] + marker["aborted_cycles"]
    assert marker["overhead_cycles"] >= 0 and marker["table_loads"] == (2 if case == 2 else 1)
    assert marker["aborted_runs"] == len(aborted) == int(case == 2)
    if case == 2:
        abort, = aborted
        assert abort["case"] == 2 and abort["cycles"] > 0
        minimum, maximum, block = (221184 + 13824 + 13824 + 128, 331776, 5) if mode == "sppf" else (2 * 110592 + 128, 663552, 2)
        assert abort["block"] == block and minimum <= abort["outputs"] < maximum
        assert marker["aborted_cycles"] == abort["cycles"] and marker["aborted_outputs"] == abort["outputs"]
    else:
        assert marker["aborted_cycles"] == marker["aborted_outputs"] == 0
    if mode == "sppf":
        assert marker["busy_id_perturb_cycles"] > 0 and marker["busy_start_cycles"] > 0
        assert marker["long_pool_stalls"] == (64 if case == 3 else 0)


def validate_case(target, mode, case, contract, expected):
    folder = target / f"{mode}_case{case}"
    entry, = [row for row in contract["runner_cases"] if row["case"] == case]
    sources = [runner.VENDOR / "ph1p_logic_eram.v", runner.VENDOR / "ph1p_phy_gsr.v"]
    if mode != "workstore":
        sources += [target / "reused" / (module + ".v") for module in runner.CORES]
        sources.append(target / "rtl/road_feature_blocks_client.v")
    sources += [target / "rtl/road_feature_workstore.v", target / "tests" / (TOPS[mode] + ".v")]
    arguments = [f"+CASE={0 if case == 99 else case}", f"+VECTORS_ROOT={(target / 'vectors').as_posix()}"]
    if case == 99:
        arguments.append("+" + NEGATIVES[mode] + "=1")
    argv = [[runner.MODEL / "vlib.exe", "work"],
            [runner.MODEL / "vlog.exe", "-work", "work", *sources],
            [runner.MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", TOPS[mode],
             *arguments, "-do", "run -all; quit -code 0"]]
    commands, texts = command_logs(folder, argv)
    assert all(row["native_returncode"] == row["validated_returncode"] == 0 for row in commands[:2])
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", texts[1])
    assert summaries and all(pair == ("0", "0") for pair in summaries)
    simulation, status, receipt = texts[2], read(folder / "status.json"), read(folder / "receipt.json")
    runner.prior.check_vector_loading(simulation)
    assert status["mode"] == mode and status["case"] == case
    assert status["status"] == ("PASS_REAL_CHECKER_NEGATIVE" if case == 99 else "PASS_FUNCTION_CASE")
    assert status["actual_DDR"] is False and status["physical_resource_mapping"] is False
    prefix = "FEAT_BLOCK" if mode == "csp" else "FEAT_SPPF"
    parsed = {key: list(map(fields, re.findall(prefix + "_" + suffix + r" [^\r\n]*", simulation)))
              for key, suffix in (("stages", "STAGE"), ("states", "STATE"), ("runs", "RUN"))}
    result = dict(mode=mode, case=case, runs=[], excluded_negative_prelude_runs=[],
        native_returncode=commands[2]["native_returncode"], validated_returncode=commands[2]["validated_returncode"],
        elaboration_warning_lines=re.findall(r"(?m)^# \*\* Warning:[^\r\n]*", simulation))
    if case == 99:
        assert commands[2]["validated_returncode"] != 0
        assert entry["marker"] in simulation and "** Fatal: " + entry["marker"] in simulation
        fatals = re.findall(r"\*\* Fatal: ([^\r\n]*)", simulation)
        assert len(fatals) == 1 and fatals[0].startswith(entry["marker"])
        assert "** Error:" not in simulation
        assert PREFIXES[mode] + "_PASS" not in simulation and PREFIXES[mode] + "_EXPECTED_FAULT" not in simulation
        assert receipt == dict(actual_checker_negative=True, forbidden_success_marker_absent=True)
        if mode == "sppf":
            assert len(parsed["runs"]) == 1
            run, = parsed["runs"]
            validate_run(run, parsed["stages"], parsed["states"], expected[4], 4, 0, 1)
            result["excluded_negative_prelude_runs"] = [run]
        else:
            assert not any(parsed.values())
        result["actual_numeric_checker_negative_rejected"] = True
    else:
        assert commands[2]["validated_returncode"] == 0 and not re.search(r"\*\* (?:Error|Fatal):", simulation)
        markers = re.findall(PREFIXES[mode] + r"_(?:PASS|EXPECTED_FAULT) [^\r\n]*", simulation)
        assert markers == [receipt["marker"]] and markers[0].startswith(entry["marker"] + " ")
        marker = fields(markers[0])
        assert receipt["fields"] == marker and marker["case"] == case
        assert set(marker) == set(contract["marker_fields"][entry["marker"]])
        assert all(marker.get(key) == value for key, value in entry["expected_fields"].items())
        result["endpoint"] = marker
        if mode == "workstore":
            validate_storage(marker, contract, case)
        else:
            for key, suffix in (("stage_ledger", "STAGE"), ("state_ledger", "STATE"), ("measured_runs", "RUN")):
                assert receipt[key] == re.findall(prefix + "_" + suffix + r" [^\r\n]*", simulation)
            aborted = list(map(fields, re.findall(prefix + r"_ABORT [^\r\n]*", simulation)))
            if mode == "sppf" or case in (0, 1, 2):
                blocks = (4, 5) if mode == "sppf" else (2, 3, 4)
                assert len(parsed["runs"]) == len(blocks)
                assert len(parsed["stages"]) == sum(len(expected[block]["outputs"]) for block in blocks)
                assert len(parsed["states"]) == 28 * len(blocks)
                for number, (block, run) in enumerate(zip(blocks, parsed["runs"], strict=True), start=1):
                    stages = [row for row in parsed["stages"] if row["run"] == number]
                    states = [row for row in parsed["states"] if row["run"] == number]
                    exclusive = validate_run(run, stages, states, expected[block], block, case, number)
                    result["runs"].append(dict(mode=mode, case=case, block=block, endpoint=run,
                        stages=stages, states=states, exclusive_cycles=exclusive))
                validate_sequence(marker, parsed["runs"], aborted, mode, case, contract)
                if mode == "sppf" and case == 3:
                    assert result["runs"][1]["exclusive_cycles"]["pool_write_backpressure"] >= 64
                result["aborted_prefix_excluded_from_clean"] = aborted
            else:
                assert not any(parsed.values()) and not aborted
    result["evidence"] = evidence([folder / name for name in ("commands.json", "status.json", "receipt.json", *LOG_NAMES)])
    return result


def native_observation(storage):
    """重解析实际300拍记录，并再次运行真实timing篡改负例。"""
    import observe_native
    folder = ROOT / "native_endpoint_observation_attempt3"
    commands, texts = command_logs(folder)
    expected = [str(runner.MODEL / "vsim.exe"), "-c", "-voptargs=+acc", "-lib", "work",
                "PH1P_PHY_GSR", "tb_feature_workstore", "+CASE=0", "-do", "observe.tcl"]
    assert commands[0]["argv"] == expected and commands[0]["validated_returncode"] == 0
    receipt = read(folder / "receipt.json")
    assert receipt["status"] == "PASS_ACTUAL_NATIVE_ENDPOINT_OBSERVATION"
    verify_hashes({str(ROOT / "observe_native.py"): receipt["script_sha256"],
        str(folder / "observe.tcl"): receipt["tcl_sha256"],
        str(storage / "input_binding.json"): receipt["input_binding_sha256"],
        str(folder / "simulation.log"): receipt["log_sha256"]})
    assert receipt["same_frozen_TB"] is True and receipt["complete_case_pass"] is False
    assert receipt["synthesis"] is False and receipt["mutated_timing_negative_rejected"] is True
    assert receipt["sample_period_ns"] == 10 and receipt["sample_offset_after_rising_edge_ns"] == 2
    rows = list(map(fields, re.findall(r"NATIVE_ENDPOINT sample=\d+ [^\r\n]*", texts[0])))
    assert [row["sample"] for row in rows] == list(range(300))
    measured = observe_native.measure(rows)
    assert receipt["byte_request_to_response_valid_cycles"] == sorted(set(measured["byte"])) == [2]
    assert receipt["weight_request_to_response_valid_cycles"] == sorted(set(measured["weight"])) == [4]
    assert receipt["byte_observed_responses"] == len(measured["byte"]) == 8
    assert receipt["weight_observed_responses"] == len(measured["weight"]) == 42
    mutated = copy.deepcopy(rows)
    mutated[next(index for index, row in enumerate(mutated) if row["bvalid"])]["sample"] += 1
    must_reject(lambda: observe_native.measure(mutated))
    preserved = []
    paths = [folder / name for name in ("receipt.json", "commands.json", "simulation.log", "observe.tcl")]
    for name, cause in (("native_endpoint_observation", "Unknown option '-radix'"),
                        ("native_endpoint_observation_attempt2", "Error loading design")):
        failed = ROOT / name
        records, logs = command_logs(failed)
        assert records[0]["validated_returncode"] != 0 and cause in logs[0]
        assert "NATIVE_ENDPOINT sample=0 " not in logs[0] and "FEATURE_WORKSTORE_PASS" not in logs[0]
        assert records[0]["argv"][0] == str(runner.MODEL / "vsim.exe")
        assert records[0]["argv"][records[0]["argv"].index("-lib") + 1] == str(storage / "workstore_case0/work")
        preserved.append(dict(path=str(failed), native_returncode=records[0]["native_returncode"],
                              validated_returncode=records[0]["validated_returncode"], cause=cause))
        paths += [failed / "commands.json", failed / "simulation.log"]
        if (failed / "observe.tcl").is_file():
            paths.append(failed / "observe.tcl")
    return dict(receipt=receipt, preserved_failed_commands=preserved, evidence=evidence(paths))


def source_organization(target):
    """源码组织证据只计实例和owner，不把primitive数量当综合映射。"""
    def text(path):
        return re.sub(r"/\*.*?\*/|//[^\r\n]*", "", path.read_text(encoding="utf-8"), flags=re.S)
    def instances(source, module):
        return len(re.findall(r"\b" + module + r"\s+(?:#\s*\([^;]+?\)\s*)?\w+\s*\(", source))
    client_path, store_path, top_path = [target / "rtl" / (name + ".v") for name in
        ("road_feature_blocks_client", "road_feature_workstore", "road_feature_workstore_top")]
    client, store, top = map(text, (client_path, store_path, top_path))
    arrays = r"\b(?:reg|wire)\s+(?:signed\s+)?(?:\[[^\]]+\]\s*)?\w+\s*\[[^\]]+\]\s*;"
    assert not re.search(arrays, client) and not re.search(arrays, store) and not re.search(arrays, top)
    assert "reg_tile_cache" not in client and "reg_weight_bank" not in client
    assert len(re.findall(r"\breg\s+\[191:0\]\s*reg_weight\s*;", client)) == 1
    assert len(re.findall(r"\breg\s+\[4:0\]\s*state_current\s*;", client)) == 1
    assert len(re.findall(r"\bPH1P_LOGIC_ERAM\s*#\s*\(", store)) == 4
    for module in ("road_feature_workstore", "road_csp_first_probe", "road_mac_probe", "road_dynamic_postprocess"):
        assert instances(client, module) == 0
    for module in ("road_feature_blocks_client", "road_feature_workstore", "road_csp_first_probe"):
        assert instances(top, module) == 1
    paths = [client_path, store_path, top_path]
    for mode in ("csp", "sppf"):
        path = target / "tests" / (TOPS[mode] + ".v")
        source = text(path)
        for module in ("road_feature_blocks_client", "road_feature_workstore", "road_csp_first_probe"):
            assert instances(source, module) == 1
        paths.append(path)
        if mode == "sppf":
            assignments = re.findall(r"live_memory\[[^\]]+\]\s*=\s*([^;]+);", source)
            assert assignments == ["write_data", "8'ha5^(poison_index&8'hff)"]
            assert not re.search(r"\$readmemh\([^;]*,\s*live_memory", source)
            assert source.count('"/vectors/source.hex"') == 1
            loader = source[source.index("if(requested_block==4)begin"):]
            assert loader.index('"/vectors/source.hex"') < loader.index("end else begin")
    for module in runner.CORES:
        path = target / "reused" / (module + ".v")
        assert digest(path) == digest(SELECTED / "reused" / path.name)
        paths.append(path)
    return dict(client_large_arrays=0, client_current_weight_bits=192, workstore_instances_per_top=1,
        arithmetic_owner_instances_per_top=1, vendor_primitive_instances_in_workstore_source=4,
        source_organization_only=True, physical_ERAM_mapping_proven=False,
        CSP4_to_SPPF_CPU_prefill=False, upstream_down3_down4_CPU_only=True, evidence=evidence(paths))


def check_gate(target):
    folder = target / "static_gate_full"
    command, = read(folder / "commands.json")
    verify_hashes({str(folder / "gate.log"): command["log_sha256"]})
    assert Path(command["cwd"]).resolve() == runner.SKILL.resolve()
    assert command["argv"] == [command["argv"][0], "-B", "-m", "scripts.python.validation.generated_deliverable_gate",
        str(target), "--include-testbench", "--json", str(folder / "gate.json"), "--markdown", str(folder / "gate.md")]
    report = read(folder / "gate.json")
    assert report["version"] == 3 and report["strict"] is True
    assert Path(report["root"]).resolve() == target.resolve() and set(report["checks"]) == PUBLIC_GATES
    assert command["native_returncode"] == command["validated_returncode"] == int(not report["delivery_ready"])
    assert command["native_returncode"] in (0, 1)
    return dict(delivery_ready=report["delivery_ready"], errors=report["errors"], strict_warnings=report["strict_warnings"],
        checks={key: row["status"] for key, row in report["checks"].items()},
        evidence=evidence([folder / name for name in ("commands.json", "gate.log", "gate.json", "gate.md")]))


def check_review(target, organization):
    path = ROOT / "semantic_review.json"
    review = read(path)
    assert review["candidate"] == target.name
    assert review["unexplained_high_confidence_semantic_risks"] == []
    verify_hashes(review["reviewed_sha256"])
    required = [*organization["evidence"], str(ROOT / "workstore_interface.txt")]
    required += [str(path) for folder in ("rtl", "reused", "tests") for path in (target / folder).rglob("*.v")]
    assert all(review["reviewed_sha256"].get(raw_path) == digest(Path(raw_path)) for raw_path in required)
    assert (ROOT / "handoff.txt").is_file()
    return dict(path=str(path), sha256=digest(path), reviewed_sha256=review["reviewed_sha256"],
        unexplained_high_confidence_semantic_risks=[], evidence=evidence([path, ROOT / "handoff.txt"]))


def diagnostic_elaboration(target):
    """诊断顶层仅展开1ns，绑定真实源码；不计入15个功能case。"""
    folder = ROOT / "diagnostic_elaboration"
    sources = [runner.VENDOR / "ph1p_logic_eram.v", runner.VENDOR / "ph1p_phy_gsr.v"]
    sources += [target / "reused" / (module + ".v") for module in runner.CORES]
    sources += [target / "rtl" / (module + ".v") for module in
                ("road_feature_blocks_client", "road_feature_workstore", "road_feature_workstore_top")]
    expected = [[str(runner.MODEL / "vlib.exe"), "work"],
        [str(runner.MODEL / "vlog.exe"), "-work", "work", *map(str, sources)],
        [str(runner.MODEL / "vsim.exe"), "-c", "-lib", "work", "PH1P_PHY_GSR",
         "road_feature_workstore_top", "-do", "run 1 ns; quit -code 0"]]
    commands = read(folder / "commands.json")
    assert len(commands) == 3
    names = ("vlib.log", "compile.log", "elaboration.log")
    texts = []
    for record, argv, filename in zip(commands, expected, names, strict=True):
        assert record["argv"] == argv and Path(record["cwd"]).resolve() == folder.resolve()
        assert record["native_returncode"] == record["validated_returncode"] == 0
        verify_hashes({str(folder / filename): record["log_sha256"]})
        text = (folder / filename).read_text(encoding="utf-8")
        assert not re.search(r"\*\* (?:Error|Fatal):", text)
        texts.append(text)
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", texts[1])
    assert summaries and all(pair == ("0", "0") for pair in summaries)
    status = read(folder / "status.json")
    assert status["status"] == "PASS_ACTUAL_DIAGNOSTIC_TOP_ELABORATION_ONLY"
    assert status["functional_test"] is False and status["synthesis"] is False
    assert status["source_binding_sha256"] == digest(target / "input_binding.json")
    assert status["elaboration_log_sha256"] == digest(folder / "elaboration.log")
    return dict(functional_test=False, synthesis=False, elaborated_ns=1,
        elaboration_warning_lines=re.findall(r"(?m)^# \*\* Warning:[^\r\n]*", texts[2]),
        evidence=evidence([folder / name for name in ("commands.json", "status.json", *names)]))


def cycle_comparison(cases):
    result, paths = [], []
    for mode, prior_path in (("csp", PRIOR / "cycle_ledger.json"),
                             ("sppf", PRIOR / "sppf_candidate/cycle_ledger.json")):
        seal_path = prior_path.parent / "delivery_manifest.json"
        seal = read(seal_path)
        assert seal["selected_candidate"] == "frozen_attempt2"
        verify_hashes(seal["artifacts_sha256"])
        assert seal["artifacts_sha256"][str(prior_path)] == digest(prior_path)
        old = read(prior_path)
        paths += [prior_path, seal_path]
        prior_cases = {row["case"]: row for row in old["sequences"]}
        for case in cases:
            if case["mode"] != mode or not case["runs"]:
                continue
            before, after = prior_cases[case["case"]]["endpoint"], case["endpoint"]
            result.append(dict(mode=mode, case=case["case"], old_clean_cycles=before["cycles"],
                new_clean_cycles=after["cycles"], added_clean_cycles=after["cycles"] - before["cycles"],
                old_sequence_cycles=before["sequence_cycles"], new_sequence_cycles=after["sequence_cycles"],
                added_sequence_cycles=after["sequence_cycles"] - before["sequence_cycles"],
                new_partial_chain_over_100M=after["cycles"] > 100000000, whole_network_FPS_qualified=False,
                blocks=[dict(block=run["block"], old_cycles=next(row["endpoint"]["cycles"] for row in old["runs"]
                    if row["block"] == run["block"] and row["case"] == case["case"] and
                    (mode == "csp" or not row.get("regression", False))), new_cycles=run["endpoint"]["cycles"])
                    for run in case["runs"]]))
    return dict(scope="同一启动到DONE端点；仅CSP夹具或CSP4至SPPF部分链，非整网预算验收",
                cases=result, evidence=evidence(paths))


def must_reject(check):
    try:
        check()
    except (AssertionError, ValueError):
        return
    raise AssertionError("mutated real evidence escaped finalizer")


def self_check():
    """不发布：真实storage案例、实际封存stage计数及其篡改负例。"""
    storage = ROOT / "storage_frozen"
    contract = read(storage / "tb_contract.json")["modes"]["workstore"]
    cases = [validate_case(storage, "workstore", case, contract, {}) for case in (0, 1, 99)]
    mutated = copy.deepcopy(cases[0]["endpoint"])
    mutated["accepted_byte"] += 1
    must_reject(lambda: validate_storage(mutated, contract, 0))
    old_contract = read(SELECTED / "tb_contract.json")["block_counts"]["5"]
    expected = {key: old_contract["stage_" + key] for key in COUNT_KEYS}
    receipt = read(SELECTED / "case0/receipt.json")
    stages = [row for row in map(fields, receipt["stage_ledger"]) if row["block"] == 5]
    validate_stage_counts(stages, expected)
    mutated_stages = copy.deepcopy(stages)
    mutated_stages[1]["reads"] += 1
    must_reject(lambda: validate_stage_counts(mutated_stages, expected))
    run = fields(next(row for row in receipt["measured_runs"] if fields(row)["block"] == 5))
    states = [row for row in map(fields, receipt["state_ledger"]) if row["block"] == 5]
    states += [dict(block=5, case=0, run=2, state=index, cycles=0) for index in range(20, 28)]
    expected["numeric"] = old_contract["stage_numeric"]
    for state, value in ((21, run["parameters"]), (22, run["parameters"]), (25, 25 * run["pools"]),
                         (26, run["groups"]), (27, run["groups"])):
        states[state]["cycles"] += value
        stages[0]["cycles"] += value
        run["cycles"] += value
        run["accounted"] += value
    validate_run(run, stages, states, expected, 5, 0, 2)
    mutated_states = copy.deepcopy(states)
    mutated_states[27]["cycles"] += 1
    must_reject(lambda: validate_run(run, stages, mutated_states, expected, 5, 0, 2))
    observed = native_observation(storage)
    current_checked = False
    if (ROOT / "frozen/csp_case0/receipt.json").is_file():
        contracts, counts = expected_counts(ROOT / "frozen")
        current = validate_case(ROOT / "frozen", "csp", 0, contracts["csp"], counts["csp"])
        mutated = copy.deepcopy(current["runs"][0]["stages"])
        mutated[0]["reads"] += 1
        must_reject(lambda: validate_stage_counts(mutated, counts["csp"][2]))
        current_checked = True
    return dict(storage_actual_cases_checked=3, actual_storage_count_mutation_rejected=True,
        actual_old_pool_stage_read_mutation_rejected=True, constructed_28state_ledger_mutation_rejected=True,
        actual_current_CSP0_stage_read_mutation_rejected=current_checked,
        native_observation_reparsed=True, native_timing_mutation_rejected=True,
        observed_byte_cycles=observed["receipt"]["byte_request_to_response_valid_cycles"],
        observed_weight_cycles=observed["receipt"]["weight_request_to_response_valid_cycles"], published=False)


def finalize(name):
    assert re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?", name)
    target, storage = ROOT / name, ROOT / "storage_frozen"
    assert not (ROOT / "functional_ready.json").exists(), "retain the existing published receipt"
    check = self_check()
    bindings = check_bindings(target, storage)
    contracts, expected = expected_counts(target)
    cases = [validate_case(storage if mode == "workstore" else target, mode, case,
             contracts[mode], expected.get(mode, {})) for mode, case in REQUIRED]
    assert len(cases) == 15
    organization = source_organization(target)
    observed, gate = native_observation(storage), check_gate(target)
    elaboration = diagnostic_elaboration(target)
    review, comparison = check_review(target, organization), cycle_comparison(cases)
    runs = [run for case in cases for run in case["runs"]]
    assert len(runs) == 17
    closure = {}
    for item in [*cases, organization, observed, gate, review, comparison, elaboration]:
        closure.update(item["evidence"])
    closure.update(evidence([Path(__file__), ROOT / "run.py", target / "input_binding.json",
                            storage / "input_binding.json", target / "tb_contract.json"]))
    verify_hashes(closure)
    assert check_bindings(target, storage) == bindings
    ledger = dict(clock_hz=100000000, runs=runs, cases=cases, cycle_comparison=comparison,
        completed_clean_block_runs=17, exclusive_28state_and_stage_sums_equal_endpoints=True,
        aborted_prefix_and_reset_reload_excluded_from_clean=True, system_target_cycles=100000000,
        system_target_used_as_functional_pass_threshold=False, whole_network_FPS_qualified=False)
    ready = dict(status="NATIVE_WORKSTORE_COMPONENT_FUNCTION_PASS_DIAGNOSTIC_SYNTHESIS_NOT_RUN",
        candidate=name, all_required_cases_passed=True, validated_case_directories=15,
        storage_case_directories=3, full_case_directories=12, completed_clean_block_runs=17,
        unexplained_high_confidence_semantic_risks=[], semantic_review=review,
        source_organization=organization, input_binding_sha256=digest(target / "input_binding.json"),
        storage_input_binding_sha256=digest(storage / "input_binding.json"), source_bindings=bindings,
        finalizer_sha256=digest(Path(__file__)), checker_self_check=check, native_endpoint=observed,
        diagnostic_top_elaboration_only=elaboration,
        strict_gate=gate, cycle_comparison=comparison, actual_DDR=False,
        physical_ERAM_mapping_proven=False, synthesis=False, place_route=False, bitstream=False, board=False,
        full_graph=False, FPS_qualification=False, accuracy_evaluation=False, training_updates=0,
        production_delivery_ready=False, evidence=closure)
    for filename, value in (("cycle_ledger.json", ledger), ("integration_sources.json", organization),
                            ("final_checks.json", ready), ("status.json", ready)):
        save(ROOT / filename, value)
    published = evidence([ROOT / filename for filename in ("cycle_ledger.json", "integration_sources.json",
                         "final_checks.json", "status.json", "handoff.txt")])
    verify_hashes(published)
    save(ROOT / "delivery_manifest.json", dict(status=ready["status"], selected_candidate=name,
        artifacts_sha256=published, finalizer_sha256=digest(Path(__file__)),
        input_binding_sha256=ready["input_binding_sha256"], payload_sha256=runner.prior.PAYLOAD,
        production_delivery_ready=False))
    ready["delivery_manifest_sha256"] = digest(ROOT / "delivery_manifest.json")
    save(ROOT / "functional_ready.json", ready)
    print("SEALED_NATIVE_WORKSTORE_COMPONENT_FUNCTION_ONLY", len(cases), len(runs), flush=True)


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("evidence assertions require Python without -O")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        print("PASS_FINALIZER_SELF_CHECK", self_check(), flush=True)
    else:
        finalize(args.name)
