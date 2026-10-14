"""只核对已观察到的目标LUT换脚和一个复位副本合并，不是通用HDL解析器。"""
import re


def fields(text, port, net):
    assert text.count(f".{port}({net})") == 1, "Require exactly one named output driver"
    position = text.index(f".{port}({net})")
    start = text.rfind("  PH1P_PHY_LSLICE #(", 0, position)
    assert start >= 0
    end = text.index(");", position)
    # Same bounded literal field extraction as existing check_replication.py.
    return dict(re.findall(r"^\s*\.(\w+)\(([^()\n]*)\)\)?[,\s]*$", text[start:end], re.M))


def verify(work, connections, after_name="after_place.v"):
    old, new = connections
    assert len(old) == len(new) == 41
    changed = {pin: [old[pin], new[pin]] for pin in old if old[pin] != new[pin]}
    assert set(changed) == {"id", "ie", "asr"}, changed
    assert old["id"] == new["ie"] and old["ie"] == new["id"]
    texts = [(work / name).read_text(encoding="utf-8") for name in ("before_place.v", after_name)]
    target_net = "\\" + old["ofb"] + " "
    target = [fields(text, "ofb", target_net) for text in texts]
    assert all(item["LUTMODE"] == '"DLUT5"' and item["OFB_SD"] == '"LUTX"' for item in target)
    assert target[0]["LUT5B_SD2"] == target[1]["LUT5B_SD2"] == '"ID"'
    tables = [int(item["INIT_LUT5B"].split("'b")[1], 2) for item in target]
    for index in range(32):
        swapped = (index & 7) | ((index & 8) << 1) | ((index & 16) >> 1)
        assert (tables[0] >> index) & 1 == (tables[1] >> swapped) & 1
    register_keys = ("ASRMUX", "CEAMUX", "CEBMUX", "CLKMUX", "LATCHMODE", "OQAMUX", "OQBMUX",
        "REGA_REGSET_ASYNC", "REGA_REGSET_SYNC", "REGA_SD", "REGB_REGSET_ASYNC",
        "REGB_REGSET_SYNC", "REGB_SD", "SSRMUX", "SSROVERCE", "ima", "imb", "clk", "oqa", "oqb")
    assert all(target[0].get(key) == target[1].get(key) for key in register_keys)
    # Two old release-done FFs and the retained FF have identical D/clock/reset/enable.
    release = [fields(texts[0], "oqa", f"reg_release_done_dup_{index}") for index in (1, 2)]
    release.append(fields(texts[1], "oqa", "reg_release_done_dup_1"))
    release = [{key: value for key, value in item.items() if key != "oqa"} for item in release]
    assert release[0] == release[1] == release[2]
    reset = [fields(text, "ofb", pins["asr"]) for text, pins in zip(texts, connections)]
    for item in reset:
        assert item["LUTMODE"] == '"DLUT5"'
        assert item["LUT5B_SD2"] == '"IMB"' and item["OFB_SD"] == '"LUTX"'
        assert {item["ie"], item["imb"]} in (
            {"i_rstn_dup_1", "reg_release_done_dup_1"}, {"i_rstn_dup_1", "reg_release_done_dup_2"})
        table = int(item["INIT_LUT5B"].split("'b")[1], 2)
        assert all(((table >> index) & 1) == bool(index & 8 and index & 16) for index in range(32))
    return {"status": "PASS_TARGET_PIN_SWAP_AND_RESET_REPLICA_EQUIVALENCE", "pins": 41,
        "literal_pin_identity": False, "changed": changed, "before": old, "after": new,
        "target_lut_truth_table_cases": 32, "reset_lut_cases_each": 32,
        "release_registers_identical_except_output": True,
        "scope": "One packed cell and reset driver/FF merge only; not whole-design formal or gate simulation"}
