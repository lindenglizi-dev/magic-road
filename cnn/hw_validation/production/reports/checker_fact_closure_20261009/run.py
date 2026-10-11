"""同一冻结 RTL 的原/改检查器对比；全部新输出限定在本目录。"""
from collections import Counter
import argparse
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parents[1]
PREVIOUS = ROOT.parent / "mac_task_stream_20261009"
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
OVERLAYS = {"original": PRODUCTION / "checker_overlay", "fixed": ROOT / "checker_overlay"}
ORIGINS = ("vg_instance_rules", "vg_value_facts", "vg_structure_rules", "vg_contract_liveness")


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def freeze():
    manifest = ROOT / "frozen.json"
    if not manifest.exists():
        records = json.loads((PREVIOUS / "frozen.json").read_text(encoding="utf-8"))
        records.update({str(PREVIOUS / name): value for name, value in json.loads(
            (PREVIOUS / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
        for base in (OVERLAYS["original"], SKILL / "scripts", SKILL / "assets", SKILL / "config"):
            records.update({str(path): digest(path) for path in base.rglob("*")
                            if path.is_file() and path.suffix in (".py", ".json")})
        save(manifest, records)
    records = json.loads(manifest.read_text(encoding="utf-8"))
    changed = [name for name, expected in records.items() if digest(Path(name)) != expected]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def prepare():
    target = ROOT / "inputs/rtl"
    target.mkdir(parents=True, exist_ok=False)
    source = PREVIOUS / "checker_replay_final/inputs/candidate"
    for path in sorted(source.glob("*.v")):
        shutil.copy2(path, target / path.name)
    assert len(list(target.glob("*.v"))) == 8
    external = PREVIOUS / "checker_replay_final/interfaces/ph1p_eram_interface_complete.v"
    destination = ROOT / "inputs/interfaces" / external.name
    destination.parent.mkdir(parents=True)
    shutil.copy2(external, destination)
    save(ROOT / "inputs/manifest.json", {str(path.relative_to(ROOT)): digest(path)
         for path in (ROOT / "inputs").rglob("*.v")})
    save(ROOT / "status.json", {"stage": "frozen_inputs_ready", "rtl_changed": False,
         "deployment_release": False, "scope": "VG097/VG153/VG136 checker facts only"})


def command(arguments, work, label, allowed=(0,)):
    work.resolve().relative_to(ROOT)
    work.mkdir(parents=True, exist_ok=True)
    with (work / (label + ".log")).open("w", encoding="utf-8") as output:
        completed = subprocess.run([str(arg) for arg in arguments], cwd=work, stdout=output,
                                   stderr=subprocess.STDOUT, timeout=300)
    save(work / (label + ".command.json"), {"command": [str(arg) for arg in arguments],
         "cwd": str(work), "returncode": completed.returncode,
         "log_sha256": digest(work / (label + ".log"))})
    assert completed.returncode in allowed, (label, completed.returncode, work)


def gate(mode):
    work = ROOT / "gates" / mode
    assert not work.exists(), "Preserve prior attempts; select a fresh output for reruns."
    bootstrap = (f"import sys;sys.path[:0]=[{str(OVERLAYS[mode])!r},{str(SKILL)!r}];"
                 "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", bootstrap, ROOT / "inputs/rtl",
             "--external-interface-source", ROOT / "inputs/interfaces/ph1p_eram_interface_complete.v",
             "--json", work / "gate.json", "--markdown", work / "gate.md"], work, "gate", (0, 1))
    report = json.loads((work / "gate.json").read_text(encoding="utf-8"))
    print(mode, report["errors"], report["strict_warnings"], report["delivery_ready"], flush=True)


def regression_worker(mode, output):
    output.resolve().relative_to(ROOT)
    sys.path[:0] = [str(OVERLAYS[mode]), str(SKILL)]
    spec = importlib.util.spec_from_file_location("existing_project_gate", PRODUCTION / "run_project_gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = module.regress(output)
    origins = {}
    for name in ORIGINS:
        imported = __import__("scripts.python.quality." + name, fromlist=["*"])
        path = Path(imported.__file__).resolve()
        origins[name] = {"path": str(path), "sha256": digest(path)}
    save(output / "receipt.json", {"cases": results, "origins": origins,
         "all_passed": all(case["passed"] for case in results.values())})
    assert all(case["passed"] for case in results.values()), results


def regress(mode):
    work = ROOT / "existing_regression" / mode
    assert not work.exists()
    command([sys.executable, "-B", "-X", "utf8", Path(__file__), "regression_worker",
             "--mode", mode, "--output", work], work, "regression")
    print("EXISTING_REGRESSION_PASS", mode, flush=True)


def summary():
    reports = {mode: json.loads((ROOT / "gates" / mode / "gate.json").read_text(encoding="utf-8"))
               for mode in OVERLAYS}
    first, second = [report["delivery_issues_by_rule"] for report in reports.values()]
    delta = {rule: second.get(rule, 0)-first.get(rule, 0) for rule in sorted(set(first) | set(second))
             if first.get(rule, 0) != second.get(rule, 0)}
    assert reports["original"]["errors"] == 4975, "Original checker/input drift must be explained."
    changed_rules = {"VG097", "VG136", "VG153"}
    assert set(delta) <= changed_rules, delta
    unaffected = [Counter(json.dumps(issue, ensure_ascii=False, sort_keys=True)
                          for issue in report["issues"] if issue.get("code") not in changed_rules)
                  for report in reports.values()]
    assert unaffected[0] == unaffected[1], "Unrelated diagnostic facts changed."
    regressions = {mode: json.loads((ROOT / "existing_regression" / mode / "receipt.json").read_text(encoding="utf-8"))
                   for mode in OVERLAYS}
    assert all(value["all_passed"] for value in regressions.values())
    targeted = {}
    for name in ("analysis/array_width_results_v2.json", "tests/array_driver_results_v2.json",
                 "analysis/loop_feedback_test_v3.json"):
        result = json.loads((ROOT / name).read_text(encoding="utf-8"))
        assert result["all_passed"], name
        targeted[name] = {"sha256": digest(ROOT / name), "all_passed": True}
    python_sources = [ROOT / "run.py", *sorted((ROOT / "tests").glob("*.py")),
                      *sorted(OVERLAYS["fixed"].rglob("*.py"))]
    for path in python_sources:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    source_manifest = json.loads((ROOT / "inputs/manifest.json").read_text(encoding="utf-8"))
    assert all(digest(ROOT / name) == expected for name, expected in source_manifest.items())
    groups = {
        "width_range_review": {"VG085", "VG097", "VG122", "VG137"},
        "literal_coding_contract": {"VG125", "VG138"},
        "driver_feedback": {"VG136", "VG141", "VG153"}, "state_contract": {"VG144"},
        "source_operation_budget": {"VG145", "VG146", "VG147"},
        "format_comment_naming": {"VG004", "VG007", "VG009", "VG013", "VG014", "VG015", "VG020",
            "VG021", "VG023", "VG024", "VG025", "VG030", "VG031", "VG040", "VG041", "VG042",
            "VG054", "VG060", "VG061", "VG062", "VG063", "VG064", "VG065", "VG066", "VG067",
            "VG068", "VG070", "VG156", "VG157", "COMMENT_COMMENT_PLACEMENT", "FORMATTER_TEMPLATE_MISMATCH"},
    }
    categories = Counter()
    for rule, count in second.items():
        categories[next((name for name, rules in groups.items() if rule in rules), "other_semantics_or_unresolved")] += count
    patch = []
    for path in sorted(OVERLAYS["fixed"].rglob("*.py")):
        relative = path.relative_to(OVERLAYS["fixed"])
        original = OVERLAYS["original"] / relative
        if not original.exists():
            original = SKILL / relative
        old = original.read_text(encoding="utf-8").splitlines(True) if original.exists() else []
        patch.extend(difflib.unified_diff(old, path.read_text(encoding="utf-8").splitlines(True),
                     fromfile="original/" + relative.as_posix(), tofile="fixed/" + relative.as_posix()))
    (ROOT / "checker.patch").write_text("".join(patch), encoding="utf-8")
    save(ROOT / "comparison.json", {"errors": [report["errors"] for report in reports.values()],
         "strict_warnings": [report["strict_warnings"] for report in reports.values()], "delta_by_rule": delta,
         "category_count_scope": "delivery_issues_by_rule includes strict warnings; not unique functional bugs",
         "fixed_categories": dict(categories), "rtl_unchanged": True, "deployment_release": False,
         "fixed_eight_gates": reports["fixed"]["checks"], "source_sha256": source_manifest,
         "checker_sha256": {str(path.relative_to(ROOT)): digest(path) for path in OVERLAYS["fixed"].rglob("*.py")},
         "existing_regression": regressions, "targeted_regression": targeted,
         "unaffected_issue_multiset_equal": True, "unaffected_issue_count": sum(unaffected[0].values()),
         "python_syntax_checked_files": len(python_sources), "patch_sha256": digest(ROOT / "checker.patch")})
    save(ROOT / "status.json", {"stage": "checker_comparison_complete_strict_not_closed",
         "original_errors": reports["original"]["errors"], "fixed_errors": reports["fixed"]["errors"],
         "delta_by_rule": delta, "rtl_changed": False, "deployment_release": False,
         "physical_rebuilt": False, "training_started": False})
    save(ROOT / "evidence_hashes.json", {str(path.relative_to(ROOT)): digest(path)
         for path in sorted(ROOT.rglob("*")) if path.is_file()
         and path.name != "evidence_hashes.json" and "__pycache__" not in path.parts})
    print(json.dumps({"delta": delta, "categories": categories}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "gate", "regress", "regression_worker", "summary"))
    parser.add_argument("--mode", choices=tuple(OVERLAYS))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    freeze()
    try:
        if args.stage == "prepare": prepare()
        elif args.stage == "gate": gate(args.mode)
        elif args.stage == "regress": regress(args.mode)
        elif args.stage == "regression_worker": regression_worker(args.mode, args.output)
        else: summary()
    finally:
        freeze()
