"""Freeze production inputs and prepare an isolated, volatile-only H0 build."""
import argparse
import hashlib
import json
import shutil
import tempfile
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inventory(project):
    files = list((project / "user_source").rglob("*"))
    files += [project / "td_project" / name for name in
              ("camera_to_dsi_display.al", "camera_to_dsi_display.sdc")]
    files += [project / "cnn" / name for name in
              ("model.py", "loss.py", "integer.py", "contract.json")]
    files += list((project / "cnn" / "template").glob("*.v"))
    files += [project / "cnn/template/output/cnn_video_template.al"]
    return {str(path.relative_to(project)).replace("\\", "/"): digest(path)
            for path in sorted(set(files)) if path.is_file()}


def changes(before, after):
    return {name: {"before": before.get(name), "after": after.get(name)}
            for name in sorted(before.keys() | after.keys())
            if before.get(name) != after.get(name)}


def save_json(path, value, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def capture():
    receipt = ROOT / "reports/production_before.json"
    if receipt.exists():
        return verify()
    save_json(receipt, {"utc": datetime.now(timezone.utc).isoformat(),
                       "project": str(PROJECT), "files": inventory(PROJECT)}, True)
    print("Production input hashes frozen; no production files written.")


def verify():
    receipt = json.loads((ROOT / "reports/production_before.json").read_text(encoding="utf-8"))
    diff = changes(receipt["files"], inventory(PROJECT))
    save_json(ROOT / "reports/production_after.json",
              {"utc": datetime.now(timezone.utc).isoformat(),
               "unchanged": not diff, "differences": diff})
    print(json.dumps({"production_unchanged": not diff, "differences": diff}))
    if diff:
        raise SystemExit("Production input drift detected: inspect before building.")


def prepare():
    capture()
    build = ROOT / "baseline"
    build.mkdir(exist_ok=True)
    project_file = build / "hw_video_baseline.al"
    if project_file.exists():
        raise SystemExit("Baseline already prepared; preserving existing build inputs.")
    source = PROJECT / "cnn/template"
    shutil.copy2(source / "design_top_wrapper.v", build / "design_top_wrapper.v")
    # TD emits literal ampersands (UsedInP&R): preserve its native syntax.
    project_text = (source / "output/cnn_video_template.al").read_text(encoding="utf-8")
    project_text = project_text.replace((source / "output").as_posix(), build.as_posix())
    project_text = project_text.replace("<Name>cnn_video_template</Name>",
                                        "<Name>hw_video_baseline</Name>")
    project_text = project_text.replace((source / "design_top_wrapper.v").as_posix(),
                                        (build / "design_top_wrapper.v").as_posix())
    for filename in re.findall(r'<File Path="([^"]+)"', project_text):
        if not Path(filename).is_file():
            raise FileNotFoundError(filename)
    project_file.write_text(project_text, encoding="utf-8")
    script = (source / "run_template.tcl").read_text(encoding="utf-8")
    script = script.replace("cnn_video_template.al", "hw_video_baseline.al")
    script = script.replace("../../../", PROJECT.as_posix() + "/")
    script += "\n# JTAG recovery artifact only; no programmer or Flash operation here.\n"
    script += "bitgen -bit hw_video_baseline.bit\n"
    (build / "build.tcl").write_text(script, encoding="utf-8")
    defaults = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator/config/defaults.json")
    settings = json.loads(defaults.read_text(encoding="utf-8"))
    settings["paths"]["skill_root"] = str(defaults.parents[1])
    settings["paths"]["reports_dir"] = str(ROOT / "reports")
    settings["policy"].update(allow_implicit_local_external_validation=True,
                              prefer_remote_for_external_validation=False,
                              block_when_remote_unconfigured=False)
    settings["skill_dependencies"]["state_path"] = str(ROOT / "reports/dependency-state.json")
    settings["fpga_developer_routing"]["state_path"] = str(ROOT / "reports/dependency-state.json")
    save_json(ROOT / "settings.json", settings, True)
    save_json(build / "inputs.json", {"project": digest(project_file),
              "top": digest(build / "design_top_wrapper.v"),
              "script": digest(build / "build.tcl"),
              "external_sources": "read-only existing sources; no shared IP edits",
              "hardware": "PH1P35MDG324 speed -3; physical board identity unverified"}, True)
    print("Independent baseline prepared: " + str(build))


def self_check():
    assert changes({"a": "1"}, {"a": "1"}) == {}
    assert set(changes({"a": "1", "b": "2"}, {"a": "3", "c": "4"})) == {"a", "b", "c"}
    with tempfile.TemporaryDirectory(prefix="roadyolo_hash_") as directory:
        path = Path(directory) / "one.bin"
        path.write_bytes(b"abc")
        assert digest(path) == hashlib.sha256(b"abc").hexdigest()
        save_json(Path(directory) / "receipt.json", {"ok": True}, True)
        try:
            save_json(Path(directory) / "receipt.json", {}, True)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Must not overwrite baseline receipt")
    print("PASS: hashing, change/add/delete detection, exclusive receipt preservation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("capture", "verify", "prepare", "self-check"))
    args = parser.parse_args()
    {"capture": capture, "verify": verify, "prepare": prepare,
     "self-check": self_check}[args.action]()
