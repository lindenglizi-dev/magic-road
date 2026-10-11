"""Pin the approved candidate and independently compare frozen module ports."""
import hashlib
import json
import re
from pathlib import Path


def ports(path):
    source = re.sub(r"//[^\n]*", "", path.read_text(encoding="utf-8"))
    header = source[source.index("module road_mac_probe"):].split(");", 1)[0]
    return re.findall(r"\b(input|output)\s*(\[[^\]]+\])?\s*(\w+)", header)


def main():
    root = Path(__file__).resolve().parent
    candidate = root / "core/road_mac_probe.v"
    original = root.parent / "v7_onchip_chain_20261006/inputs/road_mac_probe.v"
    sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
    assert sha == "04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51"
    assert ports(candidate) == ports(original)
    assert len(ports(candidate)) == 14
    assert sum(int(high) - int(low) + 1 for _, width, _ in ports(candidate)
               for high, low in [width.strip("[]").split(":") if width else ("0", "0")]) == 465
    result = {"status": "FROZEN_MAC_INTERFACE_PASS", "sha256": sha,
              "ports": ports(candidate), "expanded_mac_io_bits": 465,
              "scope": "Internal MAC interface, not the external 38-bit shell"}
    (root / "frozen_contract_audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "ports"}))


if __name__ == "__main__":
    main()
