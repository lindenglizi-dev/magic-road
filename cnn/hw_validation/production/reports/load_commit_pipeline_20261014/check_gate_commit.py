"""仅核查本候选综合网表两个已知写口，确认写资格被寄存边界切断。"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def check():
    text = (ROOT / "physical/gate_netlist.v").read_text(encoding="utf-8")
    pattern = r"^  (AL_MAP_LUT[1-6]|AL_MAP_SEQ_GSR|PH1P_PHY_DRAMHARDCON)\s*#\((.*?)\)\s*(\\\S+|[A-Za-z_]\w*)\s*\((.*?)\);"
    instances = []
    drivers = {}
    for kind, parameters, name, ports in re.findall(pattern, text, re.M | re.S):
        name = name.lstrip("\\")
        pins = {p: value.strip() for p, value in re.findall(r"\.(\w+)\(([^()\n]*)\)", ports)}
        item = {"kind": kind, "name": name, "pins": pins, "parameters": parameters}
        instances.append(item)
        if kind.startswith("AL_MAP_LUT"):
            assert pins["o"] not in drivers
            drivers[pins["o"]] = item
    results = {}
    for owner, pending, address, prefix in (
        ("u_stem", "flag_weight_write_pending", "reg_weight_write_address", "reg_weight_n_syn_"),
        ("u_down2", "flag_halo_write_pending", "reg_halo_write_address", "reg_halo_n_syn_")):
        net = "\\u_compute/" + owner + "/" + pending
        ff = [item for item in instances if item["kind"] == "AL_MAP_SEQ_GSR" and item["pins"].get("q") == net]
        assert len(ff) == 1 and ff[0]["pins"]["sr"] == "domain_rstn"
        assert '.SRMODE("ASYNC")' in ff[0]["parameters"]
        leaves = set()

        def depth(value):
            if value == net or value == "domain_rstn" or value.startswith("\\u_compute/" + owner + "/" + address + " "):
                leaves.add(value)
                return 0
            assert value in drivers, (owner, "unexpected upstream dependency", value)
            item = drivers[value]
            inputs = [v for p, v in item["pins"].items() if p in "abcdef"]
            assert inputs
            return 1 + max(depth(v) for v in inputs)

        targets = [item for item in instances if item["kind"] == "PH1P_PHY_DRAMHARDCON" and
                   item["name"].startswith("u_compute/" + owner + "/") and
                   item["pins"].get("we", "").startswith("\\u_compute/" + owner + "/" + prefix)]
        assert targets, owner
        depths = {item["name"]: depth(item["pins"]["we"]) for item in targets}
        assert net in leaves and max(depths.values()) <= 2, (owner, depths)
        results[owner] = {"registered_valid": ff[0]["name"], "distributed_ram_write_endpoints": len(targets),
                          "max_write_enable_lut_depth_after_register": max(depths.values()),
                          "write_enable_leaves": sorted(leaves)}
    assert text.count(".wea(\\u_compute/u_stem/flag_weight_write_pending )") == 3
    result = {"status": "PASS", "targets": results,
              "stem_eram_write_enables_direct_from_pending": 3,
              "scope": "Known gate-level write-enable cones only; physical timing and full equivalence are separate"}
    (ROOT / "physical/gate_commit_check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    check()
