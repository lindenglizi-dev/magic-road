"""Narrow source audit; RTL simulations remain the semantic authority."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT.parent / "v7_minimal_chain_20261006" / "inputs"
OLD = BASELINE / "road_mac_probe.v"
NEW = ROOT / "candidate" / "road_mac_probe.v"
ORIGINAL = ROOT.parents[2] / "mac" / "road_mac_probe.v"


def compact(text):
    return re.sub(r"\s+", "", re.sub(r"//[^\n]*", "", text))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    old, new = OLD.read_text(encoding="utf-8"), NEW.read_text(encoding="utf-8")
    old_code, new_code = compact(old), compact(new)
    assert sha(OLD) == "5df97da6910c5673f35807207cc06260fc6ed6edc7d9313aa2fac9ec7b3016be"
    assert sha(ORIGINAL) == sha(OLD), "Original kernel was overwritten"
    assert old_code.split(");", 1)[0] == new_code.split(");", 1)[0], "External ports changed"
    widened = ["reg_base_product", "reg_base_pair", "reg_base_quad", "reg_base_dot",
               "reg_publish_data", "reg_accumulator"]
    for name in widened:
        assert f"reg[98:0]{name}=99'd0;" in new_code, name
        assert f"{name}<=99'd0;" in new_code, name + " reset"
    for lane, field in [("alpha", "32:0"), ("beta", "65:33"), ("gamma", "98:66")]:
        assert f"wiresigned[32:0]base_{lane};" in new_code
        assert f"assignbase_{lane}=reg_base_dot[{field}];" in new_code
        assert f"wiresigned[32:0]dot_{lane}_wide;" in new_code
        assert f"wiresigned[33:0]candidate_{lane}_sum;" in new_code
        assert f"assigncandidate_{lane}_sum=base_{lane}+dot_{lane}_wide;" in new_code
        for suffix in ("", "_hold", "_final"):
            assert f"regsigned[33:0]reg_candidate_{lane}{suffix}=34'sd0;" in new_code
        assert f"reg_candidate_{lane}<=candidate_{lane}_sum;" in new_code
    assert ("reg_base_product<=flag_first_front?{reg_bias_front[95],reg_bias_front[95:64],"
            "reg_bias_front[63],reg_bias_front[63:32],reg_bias_front[31],reg_bias_front[31:0]}"
            ":reg_accumulator;") in new_code
    for destination, source in [("reg_base_pair", "reg_base_product"),
                                ("reg_base_quad", "reg_base_pair"),
                                ("reg_base_dot", "reg_base_quad")]:
        assert f"{destination}<={source};" in new_code
    assert ("reg_publish_data<={reg_candidate_gamma_final[32:0],"
            "reg_candidate_beta_final[32:0],reg_candidate_alpha_final[32:0]};") in new_code
    assert "reg_accumulator<=reg_publish_data;" in new_code
    # These must remain bit-for-bit identical; this audit does not infer their cycle meaning.
    preserved = ["input_ready_o", "flag_stage_valid", "reg_last_pipe", "flag_last",
                 "flag_publish_event", "flag_commit_event", "flag_release_no_output",
                 "flag_release", "flag_output_accept", "result_valid_o", "result_data_o"]
    for name in preserved:
        pattern = rf"(?<![A-Za-z0-9_]){name}<=[^;]+;"
        assert re.findall(pattern, old_code) == re.findall(pattern, new_code), name
    contract = ROOT.parents[1] / "deployment_contract.json"
    frozen_contract = BASELINE / "deployment_contract.json"
    assert sha(contract) == sha(frozen_contract), "Deployment contract was changed"
    proof = json.loads((ROOT / "coordinator" / "range_proof.json").read_text())
    assert proof["status"] == "PROVED_FOR_FROZEN_GRAPH_LEGAL_REDUCTIONS"
    report = {"status": "SOURCE_AUDIT_PASS", "widened_banks": widened,
              "unchanged_control_assignments": preserved, "external_ports_unchanged": True,
              "deployment_contract_unchanged": True,
              "source_sha256": {str(path): sha(path) for path in (OLD, ORIGINAL, NEW, contract)},
              "scope": "Source wiring/width/control guard, not semantic or physical signoff"}
    (ROOT / "coordinator" / "source_audit.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    check()
