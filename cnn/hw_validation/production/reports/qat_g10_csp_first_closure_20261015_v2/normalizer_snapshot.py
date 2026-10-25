"""Use the installed governed formatter on the new CSP wrapper only."""
import difflib
import json
import os
from pathlib import Path

from scripts.python.quality.formatter_config import create_formatter_backend
from scripts.python.workflow.spec_document import extract_verilog_interfaces

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "csp_first_probe/rtl/road_csp_first_probe.v"
TARGET = ROOT / "csp_first_closure/rtl/road_csp_first_probe.v"


def main():
    engine = create_formatter_backend(overrides={"formatter": {"auto_fix_prefix": False},
        "header": {"company_en": "RoadYOLO", "company_cn": "RoadYOLO",
            "engineer_en": "Codex", "engineer_cn": "Codex",
            "copyright_owner_en": "RoadYOLO", "copyright_owner_cn": "RoadYOLO",
            "developer_en": "Codex", "developer_cn": "Codex",
            "reviser_en": "Codex", "reviser_cn": "Codex"}})
    source = TARGET.read_text(encoding="utf-8")
    # Pure interfaces were extracted by the governed tool from the actual cores.
    # Bound lookup to those interfaces; never normalize the frozen implementations.
    os.chdir(ROOT / "reports/csp_first_closure_static_20261015_v1")
    candidate = engine.format_text(source)
    second = engine.format_text(candidate)
    if second != candidate:
        Path("formatter_pass_one.txt").write_text(candidate, encoding="utf-8")
        Path("formatter_pass_two.txt").write_text(second, encoding="utf-8")
        Path("formatter_instability.diff").write_text("".join(difflib.unified_diff(
            candidate.splitlines(True), second.splitlines(True))), encoding="utf-8")
        raise ValueError("formatter candidate is not stable on second pass")
    if extract_verilog_interfaces(source) != extract_verilog_interfaces(candidate):
        raise ValueError("formatter changed the wrapper interface")
    target_root = TARGET.parents[1]
    (target_root / "formatter_candidate.diff").write_text("".join(difflib.unified_diff(
        source.splitlines(True), candidate.splitlines(True), fromfile=str(TARGET), tofile="formatter_candidate")), encoding="utf-8")
    (target_root / "formatter_review.json").write_text(json.dumps(dict(
        source=str(TARGET), baseline=str(SOURCE), target=str(TARGET), stable_second_pass=True, interface_names_unchanged=True,
        scope="new wrapper only; not frozen arithmetic cores",
        risk="formatter splits nonblocking target processes, normalizes expressions and adds declaration zero initializers; requires numerical/handshake regression before use",
        production_or_timing_approval=False), indent=2)+"\n", encoding="utf-8")
    TARGET.write_text(candidate, encoding="utf-8")
    print("FORMATTER_CANDIDATE_WRITTEN_REQUIRES_SIMULATION")


if __name__ == "__main__":
    main()
