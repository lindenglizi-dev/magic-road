"""Bounded metadata/admission/saturation regression of the independent CSP probe."""
import argparse
import json
from pathlib import Path
import re

import run_csp_first_probe as base

SOURCE = Path(__file__).resolve().parent / "csp_first_closure"
OUT = base.BASE / "qat_g10_csp_first_closure_20261015_v2"
ORIGINAL_VECTORS = base.vectors


def vectors(root):
    ORIGINAL_VECTORS(root)
    # Same frozen SiLU and arithmetic; only synthetic bypasses vary at boundaries.
    biases = [(256, -256, 0)[i % 3] for i in range(16)]
    lut = base.readhex(root / "silu.hex")
    silu = [lut[512+bias//4] for bias in biases]
    silu = [value-65536 if value >= 32768 else value for value in silu]
    post = [max(-128, min(127, value*4)) for value in silu]
    wanted = [127, -129, -128, 128, -256, -127, 254, -128, 0,
              126, -128, 127, 127, -129, -128, 128]
    bypass = [value-actual for value, actual in zip(wanted, post, strict=True)]
    if not all(-128 <= value <= 127 for value in bypass):
        raise ValueError("synthetic boundary cannot be encoded as signed8 bypass")
    output = [max(-128, min(127, value)) for value in wanted]
    base.emit(root, "sat_sum", wanted, 16)
    base.emit(root, "sat_output", output, 8)
    base.emit(root, "sat_word", [base.pack(output, 8)], 128)
    base.emit(root, "sat_task_bypass", [base.pack(bypass[start:start+3], 8)
        for start in range(0, 16, 3)], 24)
    assert {127, 128, -129, -128, 254, -256}.issubset(wanted)


def validate_receipt(case, text):
    if case < 10:
        return base.validate_receipt(case, text)
    markers = re.findall(r"CSP_FIRST_(?:PASS|EXPECTED_FAULT) [^\r\n]*", text)
    if len(markers) != 1:
        raise ValueError("followup terminal receipt count")
    marker = markers[0]
    fields = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", marker)}
    fault_case = case in (12, 13)
    if fault_case:
        expected = dict(case=case, outputs=0)
    else:
        count = 16 if case == 15 else 384
        expected = dict(case=case, generation=2 if case in (11, 14) else 1,
            groups=12 if case == 15 else 320, tasks=6 if case == 15 else 160,
            outputs=count, acc=count, pre=count, silu=count, post=count,
            sums=16 if case == 15 else 192)
    prefix = "CSP_FIRST_EXPECTED_FAULT " if fault_case else "CSP_FIRST_PASS "
    if not marker.startswith(prefix) or any(fields.get(key) != value for key, value in expected.items()):
        raise ValueError(f"case{case} incomplete: {marker}")
    if not fault_case and fields.get("cycles", 0) <= 0:
        raise ValueError("followup missing cycles")
    if case in (10, 11, 14):
        coverage = re.findall(rf"CSP_FIRST_COVERAGE case={case}\b[^\r\n]*", text)
        wanted = {10: (320, 0, 0), 11: (0, 4, 0), 14: (0, 1, 257)}[case]
        if len(coverage) != 1:
            raise ValueError("missing adversarial coverage receipt")
        observed = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", coverage[0])}
        if tuple(observed.get(key) for key in ("metadata_poison", "admission_blocks", "partial_entries")) != wanted:
            raise ValueError("incomplete adversarial coverage")
    if case == 16:
        coverage = re.findall(r"CSP_FIRST_ARBITRATION case=16\b[^\r\n]*", text)
        if len(coverage) != 1:
            raise ValueError("missing table/task arbitration receipt")
        observed = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", coverage[0])}
        if observed.get("table_priority") != 1 or observed.get("owned_progress") != 1:
            raise ValueError("incomplete table/task arbitration")
    return marker


def specs():
    base.SOURCE = SOURCE
    base.specs()
    path = SOURCE / "spec_contract.json"
    spec = json.loads(path.read_text(encoding="utf-8"))
    for module in spec["modules"]:
        module["description"] = "首残差独立数据通路与有界对抗回归；不代表完整CNN或可部署实现。"
        module["verification_cases"] += ["首组后元数据毒化仍保持黄金结果", "未装表、非法first顺序和占有时改表均不接受",
            "零mask、重复tag故障且不发布输出", "部分装表复位必须完整重载", "127/128/-129/-128残差临界点",
            "空闲装表与首组同拍时只收装表；已有归约不被未获准的装表请求阻断"]
        module["constraints"] += ["first/last必须由上游按任务顺序驱动；错序持续背压，没有自动重试或本地超时"]
        if module["name"] == "road_csp_first_probe":
            module["behavior"] += ["空闲且i_table_valid为1时首组ready为0，装表优先；已拥有归约时装表请求不阻断合法后续组"]
    base.save(path, spec)
    base.save(SOURCE / "wrapper_contract.json", dict(name="csp_first_closure", modules=[spec["modules"][0]]))


def prepare():
    base.SOURCE = SOURCE
    base.OUT = OUT
    base.vectors = vectors
    audit = base.BASE / "csp_first_closure_static_20261015_v1"
    base.prepare(extra_sources=(Path(__file__).resolve(), SOURCE / "wrapper_contract.json",
        *[p for p in audit.iterdir() if p.is_file()]))


def selftest():
    base.selftest()
    good = "CSP_FIRST_PASS case=10 generation=1 groups=320 tasks=160 outputs=384 acc=384 pre=384 silu=384 post=384 sums=192 cycles=1"
    coverage = "\nCSP_FIRST_COVERAGE case=10 metadata_poison=320 admission_blocks=0 partial_entries=0"
    assert validate_receipt(10, good+coverage) == good
    for case, text in ((11, good), (10, good.replace("pre=384", "pre=383")),
                       (12, good.replace("case=10", "case=12")), (10, good),
                       (10, good+coverage.replace("metadata_poison=320", "metadata_poison=319"))):
        try:
            validate_receipt(case, text)
        except ValueError:
            continue
        raise AssertionError("followup accepted bad receipt")
    print("FOLLOWUP_RECEIPT_PASS positive1 negative5")
    for bits in range(16):
        owned, closed, first, table_valid = [bool(bits & (1 << lane)) for lane in range(4)]
        prior = (not closed and not first) if owned else first
        fixed = (not closed and not first) if owned else (first and not table_valid)
        assert not (not owned and fixed and table_valid)
        if owned or not table_valid:
            assert prior == fixed
        if not owned and first and table_valid:
            assert prior and not fixed
    print("ARBITRATION_TRUTH_TABLE_16_OF_16")
    terminal = good.replace("case=10", "case=16")
    arbitration = "\nCSP_FIRST_ARBITRATION case=16 table_priority=1 owned_progress=1"
    assert validate_receipt(16, terminal+arbitration) == terminal
    for bad in (terminal, terminal+arbitration.replace("owned_progress=1", "owned_progress=0")):
        try:
            validate_receipt(16, bad)
        except ValueError:
            continue
        raise AssertionError("bad arbitration receipt accepted")
    for a in range(-128, 128):
        for b in range(-128, 128):
            value = a+b
            upper, lower = 0x07f, 0x180-512
            result = 0x7f if value > upper else 0x80-256 if value < lower else value
            assert result == max(-128, min(127, value))
    print("ARBITRATION_RECEIPT_POSITIVE1_NEGATIVE2 SAT_LITERAL_PAIRS65536")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("spec", "prepare", "execute", "selftest"))
    action = parser.parse_args().action
    if action == "execute":
        base.OUT = OUT
        base.execute(range(17), validate_receipt)
    else:
        {"spec": specs, "prepare": prepare, "selftest": selftest}[action]()
