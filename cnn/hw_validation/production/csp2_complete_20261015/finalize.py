"""封存CSP2功能证据；不改旧失败状态，不运行仿真、TD、训练或板卡。"""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[3]
FROZEN=ROOT/"frozen_attempt2"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def check(hashes):
    for path,value in hashes.items():
        assert sha(Path(path))==value,path


def fields(line):
    return {key:int(value) for key,value in re.findall(r"(\w+)=(\d+)",line)}


def ledgers(content):
    runs=[fields(line) for line in re.findall(r"CSP_COMPLETE_RUN [^\r\n]*",content)]
    stages=[fields(line) for line in re.findall(r"CSP_COMPLETE_STAGE [^\r\n]*",content)]
    states=[fields(line) for line in re.findall(r"CSP_COMPLETE_STATE [^\r\n]*",content)]
    for run in runs:
        selected=[s for s in stages if s["run"]==run["run"]]
        ledger=[s for s in states if s["run"]==run["run"]]
        assert len(selected)==5 and {s["stage"] for s in selected}==set(range(5))
        assert len(ledger)==15 and {s["state"] for s in ledger}==set(range(15))
        assert sum(s["cycles"] for s in selected)==run["cycles"]
        assert sum(s["cycles"] for s in ledger)==run["cycles"]
        for name in ("groups","tasks","outputs","reads"):
            assert sum(s[name] for s in selected)==run[name],name
    return dict(runs=runs,stages=stages,states=states)


def main():
    assert fields("case=4 outputs=1632 cycles=104966")==dict(case=4,outputs=1632,cycles=104966)
    binding=read(FROZEN/"input_binding.json")
    original={key:value for key,value in binding["original_sha256"].items() if key!=str(ROOT/"run.py")}
    check(original)
    check(binding["staged_sha256"])
    assert sha(ROOT/"rtl/road_csp_complete_client.v")==sha(FROZEN/"rtl/road_csp_complete_client.v")
    assert sha(ROOT/"tests/tb_csp_complete_client.v")==sha(FROZEN/"tests/tb_csp_complete_client.v")
    normal=read(FROZEN/"verification/case_receipts.json")
    contract=read(FROZEN/"tb_contract.json")["runner_cases"]
    assert len(normal)==len(contract)==28
    numeric_runs=[]
    for number,(receipt,expected) in enumerate(zip(normal,contract,strict=True)):
        assert receipt["case"]==expected
        assert receipt["receipt"].startswith(expected["marker"])
        assert all(receipt["fields"].get(key)==value for key,value in expected["expected_fields"].items())
        content=(FROZEN/"verification"/f"case_{number}.log").read_text(encoding="utf-8")
        assert not re.search(r"\*\* (?:Error|Fatal):",content)
        assert len(re.findall(r"CSP_COMPLETE_(?:PASS|EXPECTED_FAULT) [^\r\n]*",content))==1
        if expected["marker"]=="CSP_COMPLETE_PASS":
            numeric_runs.extend(ledgers(content)["runs"])
    exit_receipt=read(FROZEN/"verification_exit_attempt3/receipt.json")
    assert exit_receipt["status"]=="PASS_EXIT_TRANSLATION_POSITIVE_AND_REAL_NEGATIVE"
    assert sha(FROZEN/"verification_exit_attempt3/launcher_snapshot.py")==exit_receipt["corrected_launcher_sha256"]
    assert [r["validated_returncode"] for r in exit_receipt["commands"]]==[0,1]
    assert [r["returncode"] for r in exit_receipt["commands"]]==[0,0]
    for record in exit_receipt["commands"]:
        path=FROZEN/"verification_exit_attempt3"/("negative.log" if record["negative"] else "positive.log")
        assert sha(path)==record["log_sha256"]
    road=read(FROZEN/"verification_road/input_binding.json")
    check(road["original_sha256"])
    check(road["staged_sha256"])
    assert sha(FROZEN/"verification_road/launcher_snapshot.py")==road["launcher_sha256"]==sha(ROOT/"run.py")
    assert read(FROZEN/"verification_road/status.json")["cases"]==9
    road_cases=read(FROZEN/"verification_road/case_receipts.json")
    assert len(road_cases)==9
    road_runs=[]
    for number,receipt in enumerate(road_cases):
        content=(FROZEN/"verification_road"/f"case_{number}.log").read_text(encoding="utf-8")
        assert not re.search(r"\*\* (?:Error|Fatal):",content)
        assert all(receipt["fields"].get(key)==value for key,value in contract[number]["expected_fields"].items())
        road_runs.extend(ledgers(content)["runs"])
    assert len(road_runs)==9
    compile_log=(FROZEN/"verification/compile.log").read_text(encoding="utf-8")
    assert re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)",compile_log)[-1]==("0","0")
    gate=read(FROZEN/"static_gate/gate.json")
    assert gate["delivery_ready"] is False
    expected_status={name:gate["checks"][name]["status"] for name in
                     ("compile","ast","readability","comment","naming","profile","testbench","toolchain")}
    assert all(expected_status[name]=="failed" for name in expected_status if name!="toolchain")
    assert expected_status["toolchain"]=="not_requested"
    selected=ledgers((FROZEN/"verification_road/case_4.log").read_text(encoding="utf-8"))
    save(ROOT/"cycle_ledger.json",dict(scope="complete CSP2 operator for individual 4x4 target tiles; no full-frame RTL traversal/FPS",
        clock_hz=100000000,table_preload_excluded=True,
        synthetic_cases=[r["fields"] for r in normal],synthetic_complete_runs=numeric_runs,
        real_road_runs=road_runs,real_road_interior=selected,
        memory_endpoint="single logical byte, two-cycle response-delay counter; not actual PAXI/DRAM",
        full_frame_cycles_measured=False,full_frame_FPS_measured=False))
    rtl_sources=[FROZEN/"rtl/road_csp_complete_client.v",*sorted((FROZEN/"reused").glob("*.v"))]
    save(ROOT/"integration_sources.json",dict(
        replacement="fixed first-residual scheduling/cache part only; keep original arithmetic/writeback or equivalent approved shared-owner packaging",
        synth_client=str(rtl_sources[0]),client_private_MAC_instances=0,
        simulation_single_arithmetic_sources=[dict(path=str(p),sha256=sha(p)) for p in rtl_sources[1:]],
        sources=[dict(path=str(p),sha256=sha(p)) for p in rtl_sources],
        testbench=dict(path=str(FROZEN/"tests/tb_csp_complete_client.v"),sha256=sha(FROZEN/"tests/tb_csp_complete_client.v")),
        selected_model_payload=road["payload_sha256"],parameter_source="same existing package; testbench field service, not a new ROM reader",
        new_TD_executed=False,production_source_list_modified=False,
        physical_top_selected=False,physical_command="C7 must attach the client to its unique owner and C8 service before a representative implementation; do not synthesize the testbench or claim standalone client omits no compute"))
    report=dict(status="COMPLETE_CSP2_TILE_FUNCTION_HANDOFF_READY_NOT_DEPLOYMENT",
        selected_candidate="frozen_attempt2",numeric_protocol_cases=28,real_road_tiles=9,
        checker_positive_negative=True,native_ModelSim_fatal_returncode=0,validated_fatal_returncode=1,
        original_numeric_RTL_inputs_rechecked=len(original),staged_inputs_rechecked=len(binding["staged_sha256"]),
        road_original_inputs_rechecked=len(road["original_sha256"]),road_staged_inputs_rechecked=len(road["staged_sha256"]),
        launcher_revision_explicit=True,launcher_sha256=sha(ROOT/"run.py"),
        client_sha256=sha(rtl_sources[0]),testbench_sha256=sha(FROZEN/"tests/tb_csp_complete_client.v"),
        payload_sha256=road["payload_sha256"],road_image_sha256=road["image_sha256"],
        five_convolutions=True,two_residuals=True,concat_final_fusion=True,
        private_MAC_instances_in_client=0,actual_ModelSim_compile_errors=0,actual_ModelSim_compile_warnings=0,
        original_elaboration_warnings=12,elaboration_warning_boundary="nine unused diagnostic outputs plus group warning in frozen wrapper; two vendor INIT_FILE bounds warnings; not suppressed or repaired",
        strict_public_matrix=expected_status,strict_errors=gate["errors"],strict_warnings=gate["strict_warnings"],
        deployment_delivery_ready=False,actual_DDR=False,ROM_reader_connected=False,unique_owner_integrated=False,
        full_CSP2_frame_RTL=False,full_graph=False,training_updates=0,
        synthesis=False,place_route=False,bitstream=False,board=False,accuracy_evaluation=False,
        current_week_target_FPS=2,whole_system_cycle_budget=50000000,result_expiry_ms=500,
        FPS_qualification=False,old_failures_preserved=True)
    save(ROOT/"final_checks.json",report)
    save(ROOT/"status.json",report)
    print("SEALED_COMPLETE_CSP2_TILE_28_CASES_AND_9_REAL_TILES_NOT_DEPLOYMENT")


if __name__=="__main__":
    main()
