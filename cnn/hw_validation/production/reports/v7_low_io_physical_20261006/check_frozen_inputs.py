"""Check frozen internal source closure without modifying any internal module."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    reports = root.parent
    chain = reports / "v7_onchip_chain_20261006"
    manifest = json.loads((chain / "final_manifest.json").read_text(encoding="utf-8"))
    mismatch = [name for name, digest in manifest["sha256"].items()
                if hashlib.sha256((chain / name).read_bytes()).hexdigest() != digest]
    assert not mismatch, mismatch
    files = [chain / "road_onchip_chain.v", chain / "road_onchip_chain.contract.json",
             chain / "strict_gate.json", chain / "final_manifest.json"]
    files.extend(chain / "inputs" / name for name in (
        "road_mac_probe.v", "road_round_shift.v", "silu_shared_unit.v", "silu_table.hex",
        "ph1p_logic_eram.v", "ph1p_phy_gsr.v", "stage_vectors.json", "test_parameters.json"))
    production = reports.parent
    files.extend((production / "deployment_contract.json",
                  production.parent / "mac" / "road_mac_probe.v"))
    closure = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    target = root / "frozen_inputs.json"
    if target.exists():
        previous = json.loads(target.read_text(encoding="utf-8"))
        assert previous["sha256"] == closure, "Frozen closure changed"
    else:
        target.write_text(json.dumps({"sha256": closure, "chain_manifest_entries": 30,
                                     "scope": "Frozen inputs; does not include future shell or TD outputs"},
                                    indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "FROZEN_INPUTS_PASS", "files": len(closure),
                      "chain_manifest_entries": len(manifest["sha256"])}))


if __name__ == "__main__":
    main()
