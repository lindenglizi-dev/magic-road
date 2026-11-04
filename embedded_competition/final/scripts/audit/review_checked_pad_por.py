
from bisect import bisect_right
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import re
import os

A = Path(__file__).resolve().parent
ROOT=Path(__file__).resolve().parents[2]
RUN = ROOT / "build/route"
LOG = A / "checked_clock_audit.log"
read = lambda path: Path(path).read_text(encoding="utf-8-sig")
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
norm = lambda value: re.sub(r"\s+", "", value).replace("\\", "")


def one(values):
    assert len(values) == 1, values
    return values[0]


def timing_rows(path):
    text = read(path)
    rows = []
    starts = list(re.finditer(r"(?m)^Slack\s+: (-?[\d.]+)ns\s*$", text))
    for index, match in enumerate(starts):
        block = text[match.end():starts[index + 1].start() if index + 1 < len(starts) else len(text)]
        row = {"slack_ns": float(match[1])}
        for label, key in [("Begin Point", "begin"), ("End Point", "end"), ("Check Type", "check"), ("Process", "process")]:
            row[key] = re.search(r"(?m)^" + label + r"\s+: (\S+)", block)[1]
        row["budget_ns"] = float(re.search(r"(?m)^Budget\s+: (-?[\d.]+)ns", block)[1])
        row["logic_levels"] = int(re.search(r"(?m)^Logic Level\s+: (\d+)", block)[1])
        rows.append(row)
    assert rows, path
    return rows


def main():
    native = read(LOG)
    assert "CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED" in native
    assert "I_a_checked_rgmii_rx_ctl" not in native and "O_a_checked_rgmii_tx_ctl" not in native
    assert sha(RUN / "checked.db") == json.loads((A.parent/"checked_binding.json").read_text())["checked_db_sha256"]
    required = [LOG, A / "actual_checked.v", A / "actual_checked.adc", A / "actual_checked.sdc",
                A / "checked_completion_ref.timing", A / "checked_completion_ddr.timing", A / "checked_init8.timing"]
    required += [A / f"checked_rgmii_{direction}_{corner}.timing" for direction in ["rx", "tx"] for corner in ["slow", "fast"]]
    for path in required[1:]:
        assert path.is_file() and path.stat().st_size > 0
        assert (RUN / "checked.db").stat().st_mtime <= path.stat().st_mtime <= LOG.stat().st_mtime
    text = read(A / "actual_checked.v")
    offsets = [match.start() for match in re.finditer("\n", text)]
    cells = []
    for match in re.finditer(r"\b(PH1P_PHY_\w+)\s*#\((.*?)\)\s+(\\?\S+)\s+\((.*?)\);", text, re.S):
        typ, attrs, name, ports = match.groups()
        cells.append({"type": typ, "name": name.lstrip("\\"), "line": bisect_right(offsets, match.start()) + 1,
                      "attrs": dict(re.findall(r"\.(\w+)\(\s*([^)]*?)\s*\)", re.sub(r"//[^\n]*", "", attrs))),
                      "ports": {key: norm(value) for key, value in re.findall(r"\.(\w+)\(\s*([^)]*?)\s*\)", ports)}})
    byname = {cell["name"]: cell for cell in cells}
    assert len(byname) == len(cells)

    def same_clock(first, second):
        if first == second:
            return True
                                                                          
                                                                               
        left = one([c for c in cells if c['type'] == 'PH1P_PHY_SCLK_V2' and c['ports'].get('clkout') == first])
        right = one([c for c in cells if c['type'] == 'PH1P_PHY_SCLK_V2' and c['ports'].get('clkout') == second])
        return left['attrs'] == right['attrs'] and {k:v for k,v in left['ports'].items() if k != 'clkout'} == {k:v for k,v in right['ports'].items() if k != 'clkout'}

    def qendpoint(net):
        return one([(cell, pin) for cell in cells for pin in ["oqa", "oqb"] if cell["ports"].get(pin) == net])

    def bank_of(pin):
        return "A" if pin == "oqa" else "B"

    def initialized_ff(cell, pin, asynchronous):
        attrs = cell["attrs"]
        bank = bank_of(pin)
        for key, value in {"LATCHMODE": "DFF", "CLKMUX": "SIG", "OQ" + bank + "MUX": "Q" + bank,
                           "REG" + bank + "_REGSET_ASYNC": "RESET", "REG" + bank + "_REGSET_SYNC": "RESET"}.items():
            assert attrs[key] == '"' + value + '"', (cell["name"], key)
        assert attrs.get("GSR", '"ENABLE"') == '"ENABLE"'
        assert attrs["ASRMUX"] == ('"INV"' if asynchronous else '"0"') and attrs["SSRMUX"] == '"0"'

    def lut_inputs(cell, bank):
        ports, attrs = cell["ports"], cell["attrs"]
        if bank == "A":
            names = ["ia", "ib", "ima" if attrs.get("LUT5A_SD0", '"IC"') == '"IMA"' else "ic", "id",
                     "imf" if attrs.get("LUT5A_SD1", '"IE"') == '"IMF"' else "ie"]
        else:
            names = ["ia", "ib", "ic", "imb" if attrs.get("LUT5B_SD2", '"ID"') == '"IMB"' else "id", "ie"]
        return [ports.get(name, "1'b1") for name in names]

    def consistent_lut_rows(cell, bank):
        pins = lut_inputs(cell, bank)
        bits = int(cell["attrs"]["INIT_LUT5" + bank].split("'b")[1], 2)
        for address in range(32):
            known = {}
            valid = True
            for bit, net in enumerate(pins):
                value = (address >> bit) & 1
                if net in ["1'b0", "1'b1"] and value != int(net[-1]):
                    valid = False
                if net in known and known[net] != value:
                    valid = False
                known[net] = value
            if valid:
                yield known, (bits >> address) & 1

    def bank_for_output(cell, pin):
        assert cell["type"] == "PH1P_PHY_LSLICE"
        if pin == "ofa":
            assert cell["attrs"].get("OFA_SD", '"LUT5A"') == '"LUT5A"'
            return "A"
        assert pin == "ofb" and cell["attrs"].get("OFB_SD", '"LUTX"') == '"LUTX"'
        assert cell["attrs"]["LUTMODE"] == '"DLUT5"'
        return "B"

    original, private = "u_power_on_reset/startup_complete", "u_power_on_reset/O_ref_startup_complete"
    mainpll = byname["u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL"]
    lock = mainpll["ports"]["lock"]
    orig, orig_pin = qendpoint(original)
    priv, priv_pin = qendpoint(private)
    assert (orig["name"], orig_pin) != (priv["name"], priv_pin)
    initialized_ff(orig, orig_pin, False)
    initialized_ff(priv, priv_pin, False)
    assert same_clock(orig["ports"]["clk"], priv["ports"]["clk"])
    release = {}
    for prefix, source in [("S_ref_reset_release", private), ("S_ddr_reset_release", original)]:
        stages = []
        for stage in [0, 1]:
            cell, pin = qendpoint(f"{prefix}[{stage}]")
            initialized_ff(cell, pin, True)
            bank = bank_of(pin)
            assert cell["attrs"]["REG" + bank + "_SD"] == ('"IMA"' if bank == "A" else '"IMB"')
            assert cell["attrs"]["CE" + bank + "MUX"] == '"1"'
            assert cell["ports"]["ima" if bank == "A" else "imb"] == (source if stage == 0 else prefix + "[0]")
            assert cell["ports"]["asr"] == lock
            stages.append({"net": f"{prefix}[{stage}]", "bank": bank, "cell": cell})
        assert stages[0]["cell"]["ports"]["clk"] == stages[1]["cell"]["ports"]["clk"]
        release[prefix] = stages
    assert release["S_ref_reset_release"][0]["cell"]["ports"]["clk"] != release["S_ddr_reset_release"][0]["cell"]["ports"]["clk"]
    counters = []
    for bit in range(16):
        cell, pin = qendpoint(f"u_power_on_reset/startup_count[{bit}]")
        initialized_ff(cell, pin, False)
        assert same_clock(cell["ports"]["clk"], orig["ports"]["clk"])
        counters.append({"bit": bit, "cell": cell["name"], "bank": bank_of(pin), "line": cell["line"]})
    lib = Path(os.environ['TD_EXEC']).resolve().parents[1]/'sim_release/ph1p/ph1p_phy_lslice.v'
    assert 'parameter GSR = "ENABLE"' in read(lib) and "tri1 ia,ib,ic,id,ie,imf,ima,imb;" in read(lib)

    comb = {net: (cell, pin) for cell in cells for pin, net in cell["ports"].items() if pin in ["ofa", "ofb"]}
    private_data_pin = "ima" if bank_of(priv_pin) == "A" else "imb"
    assert priv["attrs"]["REG" + bank_of(priv_pin) + "_SD"] == '"' + private_data_pin.upper() + '"'
    private_d = priv["ports"][private_data_pin]
    private_lut, private_output = comb[private_d]
    private_bank = bank_for_output(private_lut, private_output)
    assert private_lut["attrs"]["LUTMODE"] == '"DLUT5"'
    original_enable = orig["ports"]["imf"]
    enable_lut, enable_output = comb[original_enable]
    enable_bank = bank_for_output(enable_lut, enable_output)
    terminal = one(list((set(lut_inputs(private_lut, private_bank)) & set(lut_inputs(enable_lut, enable_bank))) - {original, private, "1'b0", "1'b1"}))
    private_rows = list(consistent_lut_rows(private_lut, private_bank))
    for known, value in private_rows:
        assert value == (known[private] | (known[terminal] & (1 - known[original])))
    enable_rows = list(consistent_lut_rows(enable_lut, enable_bank))
    for known, value in enable_rows:
        assert value == 1 - (known[original] | known[terminal])
    for known, value in consistent_lut_rows(orig, bank_of(orig_pin)):
        assert value == 1 - known[original_enable]
    reset_driver, reset_output = comb[mainpll["ports"]["pllreset"]]
    reset_bank = bank_for_output(reset_driver, reset_output)
    assert reset_driver["attrs"]["LUTMODE"] == '"DLUT5"'
    for known, value in consistent_lut_rows(reset_driver, reset_bank):
        assert value == 1 - known[original]

    @lru_cache(None)
    def lut_bits(name, bank):
        return int(byname[name]["attrs"]["INIT_LUT5" + bank].split("'b")[1], 2)

    @lru_cache(None)
    def lut_support(name, bank):
        bits = lut_bits(name, bank)
        return tuple(bit for bit in range(5) if any(
            ((bits >> address) & 1) != ((bits >> (address ^ (1 << bit))) & 1)
            for address in range(32)))

    terminal_cells = set()
    def eval_net(net, values, cache):
        if net in values:
            return values[net]
        if net in ["1'b0", "1'b1"]:
            return int(net[-1])
        if net in cache:
            return cache[net]
        cell, port = comb[net]
        assert cell["type"] == "PH1P_PHY_LSLICE"
        terminal_cells.add(cell["name"])
        if port == "ofa":
            bank = "A"
        else:
            assert cell["attrs"].get("OFB_SD", '"LUTX"') == '"LUTX"'
            bank = "B" if cell["attrs"]["LUTMODE"] == '"DLUT5"' or eval_net(cell["ports"].get("imf", "1'b1"), values, cache) else "A"
        pins = lut_inputs(cell, bank)
                                                                              
                                                                            
        address = sum(eval_net(pins[bit], values, cache) << bit for bit in lut_support(cell["name"], bank))
        cache[net] = (lut_bits(cell["name"], bank) >> address) & 1
        return cache[net]
    for value in range(65536):
        inputs = {f"u_power_on_reset/startup_count[{bit}]": (value >> bit) & 1 for bit in range(16)}
        assert eval_net(terminal, inputs, {}) == (value == 65535)

    completion = {}
    for name, cell, stages, budget in [("ref", priv, release["S_ref_reset_release"], 2.0),
                                        ("ddr", orig, release["S_ddr_reset_release"], 2.5)]:
        path = A / f"checked_completion_{name}.timing"
        input_pin = ".ima" if stages[0]["bank"] == "A" else ".imb"
        rows = [row for row in timing_rows(path) if row["begin"] == cell["name"] + ".clk" and row["end"] == stages[0]["cell"]["name"] + input_pin]
        assert len(rows) == 2 and Counter(row["check"] for row in rows) == {"setup": 1, "hold": 1}
        for row in rows:
            assert row["slack_ns"] >= 0 and row["logic_levels"] == 0
            assert row["budget_ns"] == (budget if row["check"] == "setup" else 0.0)
        completion[name] = rows
    init8 = timing_rows(A / "checked_init8.timing")
    assert len(init8) == 16 and Counter(row["check"] for row in init8) == {"setup": 8, "hold": 8}
    for row in init8:
        assert row["slack_ns"] >= 0 and row["budget_ns"] == (2.5 if row["check"] == "setup" else 0.0)
    assert {row["end"] for row in init8 if row["check"] == "setup"} == {row["end"] for row in init8 if row["check"] == "hold"}

    area = read(RUN / "candidate_final.area")
    actual_pins = {}
    for line in area.splitlines():
        fields = line.split()
        if len(fields) == 8 and fields[1] in ["INPUT", "OUTPUT", "INOUT"]:
            actual_pins[fields[0]] = dict(zip(["direction", "location", "standard", "type", "drive", "pull", "mode"], fields[1:]))
    pin_checks = {}
    for port, body in re.findall(r"set_pin_assignment\s*\{\s*([^}]+?)\s*\}\s*\{([^}]+)\}", read(ROOT / "user_source/constraints_source/pin.adc")):
        config = dict(re.findall(r"(\w+)\s*=\s*([^;]+?)\s*;", body))
        for name, field in [("LOCATION", "location"), ("IOSTANDARD", "standard"), ("DRIVESTRENGTH", "drive"), ("PULLTYPE", "pull")]:
            if name in config:
                assert config[name] == actual_pins[port][field], (port, name)
        pin_checks[port] = actual_pins[port]
    rxports = {f"I_a_rgmii_rxd[{bit}]" for bit in range(4)} | {"I_a_rgmii_rx_ctl"}
    txports = {f"O_a_rgmii_txd[{bit}]" for bit in range(4)} | {"O_a_rgmii_tx_ctl"}
    for port in rxports:
        cell = byname[port + "_syn_2"]
        assert cell["attrs"]["IDDRMODE"] == '"DDRX1_OPPOSITE"' and cell["attrs"]["IDLYEN"] == '"ENABLE"'
        assert cell["ports"]["dly"] == "5'b01000" and cell["attrs"]["IOTYPE"] == '"LVCMOS33"'
    tx_clocks = set()
    for port in txports | {"O_a_rgmii_txc"}:
        cell = byname[port + "_syn_2"]
        assert cell["attrs"]["ODDRMODE"] == '"DDRX1"' and cell["attrs"]["OTYPE"] == '"DDRSDR"' and cell["attrs"]["IOTYPE"] == '"LVCMOS33"'
        tx_clocks.add(cell["ports"]["osclk"])
    assert len(tx_clocks) == 1 and byname["O_a_rgmii_txc_syn_2"]["ports"]["doq"] == "2'b01"
    sdc = read(A / "actual_checked.sdc")
    assert "-edge_shift {2.000 2.000 2.000} [get_ports O_a_rgmii_txc]" in sdc
    for line in [line for line in read(ROOT / "td_project/camera_to_dsi_display.sdc").splitlines() if line.startswith(("set_input_delay", "set_output_delay"))]:
        assert line in sdc, line
    rgmii = {}
    for direction, ports in [("rx", rxports), ("tx", txports)]:
        for corner in ["slow", "fast"]:
            path = A / f"checked_rgmii_{direction}_{corner}.timing"
            rows = re.findall(r"Slack\s+: (-?[\d.]+)ns\nBegin Point\s+: (.*?) \((rising|falling) edge.*?\nEnd Point\s+: (.*?) \((rising|falling) edge.*?\nCheck Type\s+: (\w+)\nProcess\s+: (\w+)", read(path), re.S)
            assert len(rows) == 40
            observed = {}
            for slack, start, launch, end, capture, check, process in rows:
                port = start if direction == "rx" else end
                assert port in ports and float(slack) >= 0 and process.startswith(corner + "_")
                observed.setdefault(port, []).append({"check": check, "launch": launch, "capture": capture, "process": process, "slack_ns": float(slack)})
            assert set(observed) == ports
            for port_rows in observed.values():
                assert len(port_rows) == 8
                for check in ["setup", "hold"]:
                    assert {(row["launch"], row["capture"]) for row in port_rows if row["check"] == check} == set(product(["rising", "falling"], repeat=2))
            rgmii[direction + "_" + corner] = {"rows": 40, "all_five_ports": observed,
                "min_setup_ns": min(float(row[0]) for row in rows if row[5] == "setup"),
                "min_hold_ns": min(float(row[0]) for row in rows if row[5] == "hold")}
    evidence = {str(path): sha(path) for path in required + [lib, Path(__file__), A.parent / "checked_binding.json", RUN / "checked.db", RUN / "candidate_final.area", ROOT / "rtl/board_power_on_reset.v", ROOT / "user_source/constraints_source/pin.adc", ROOT / "td_project/camera_to_dsi_display.sdc"]}
    report = {"result": "PASS_PAD_AND_POR_CURRENT_CHECKED_EVIDENCE", "checked_utc": datetime.now(timezone.utc).isoformat(),
              "checked_db_sha256": sha(RUN / "checked.db"), "unresolved_findings": [], "evidence_sha256": evidence,
              "reviewer": "本地引脚与复位检查",
              "reviewer_adaptations": [
                  {"original_assumption": "Private completion LUT output must be ofa/bankA.",
                   "actual_current_carrier": private_lut["name"], "actual_output": private_output, "actual_bank": private_bank,
                   "change": "Resolve LUT bank from the current physical output port and actual DLUT5/OFB_SD attributes; retain exhaustive reachable-row equality to private | (terminal & !original)."},
                  {"original_assumption": "Fixed A bank for enable, B bank for PLL reset and ima for release-stage input.",
                   "actual_enable_bank": enable_bank, "actual_reset_bank": reset_bank,
                   "change": "Derive bank and ima/imb from current physical ports and DFF bank mapping; setup/hold budgets, count, zero-logic and truth-function assertions remain unchanged."},
                  {"original_assumption": "Recursively evaluate every pin of every packed LUT.",
                   "change": "Determine Boolean support from all32 INIT rows; skip a pin only if both cofactors are equal for all16 assignments. This avoids falsely treating unrelated packed pins as POR dependencies; all65536 counter cases still must equal the original terminal function."}],
              "pad": "PASS", "por": "PASS", "unresolved": [], "pad_details": {"result": "PASS", "explicit_pin_matches": len(pin_checks), "pins": pin_checks, "rgmii": rgmii,
                      "physical_RX": "All five actual opposite-edge IDDRs, enabled input delay tap8, LVCMOS33.",
                      "physical_TX": "Five data/control ODDRs plus forwarded clock ODDR use same actual osclk; clock doq=01; LVCMOS33 and requested16mA retained.",
                      "external_assumptions": "Original real forwarded PHY_TX_CAPTURE2ns phase and input1.5/2.5/output+/-1.35ns assumptions retained; no PHY readback/link test claim."},
              "por_details": {"result": "PASS", "release_four_physical_DFF_banks": release, "private_completion": priv, "private_bank": bank_of(priv_pin),
                      "original_completion": orig, "original_bank": bank_of(orig_pin), "counter16_zero_init_banks": counters,
                      "initialization": "Actual DFF banks explicitly RESET async/sync, with GSR ENABLE per current vendor library; no raw configuration-bit decode or board readback claimed.",
                      "private_next_state": "private | (terminal & !original)", "private_reachable_LUT_rows_checked": len(private_rows),
                      "original_next_state": "original | terminal, via NOT original_enable", "enable_reachable_LUT_rows_checked": len(enable_rows),
                      "terminal_net": terminal, "terminal_exhaustive_count_cases": 65536, "terminal_function": "AND of all actual16 startup_count Q bits", "terminal_cone_cells": sorted(terminal_cells),
                      "PLL_reset": "NOT original startup_complete; all reachable actual packedLUT rows checked", "PLL_reset_driver": reset_driver,
                      "completion_timing": completion, "init8": {"result": "PASS", "setup_endpoints": 8, "hold_endpoints": 8,
                          "min_setup_ns": min(row["slack_ns"] for row in init8 if row["check"] == "setup"), "min_hold_ns": min(row["slack_ns"] for row in init8 if row["check"] == "hold")},
                      "native_collection_note": "Native get_regs reference-release wildcard also returned private completion alias; actual direct privateQ->refstage0 rows were selected by current physical endpoints, and all extra self-paths remain in native report."},
              "limits": ["Pad/POR scope only; no source_freeze/DRC/clock/coverage overall approval or independent_audit.receipt generated.",
                         "Actual cell packing and aliases were derived from this checked export; no old physical cell numbers or prior passing reports reused as current evidence.",
                         "Inherited failed strict RTL gates are not reclassified by this physical review."]}
    (A / "checked_pad_por_review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report["result"])
    print("Pad160paths/4cornerviews, originalpinfields, fourreleaseFFbanks+twoindependentcompletionFFs+counter16zero-init and terminal65536cases checked")


if __name__ == "__main__":
    main()
