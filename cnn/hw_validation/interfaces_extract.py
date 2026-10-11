"""Recover complete public ERAM declarations; never extract protected behavior."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from baseline import ROOT, digest, save_json

VENDOR = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_eram.v")
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")


def public_manifest(text):
    public = text.split("`pragma protect begin_protected", 1)[0]
    public = re.sub(r"//[^\n]*", "", public)
    header = re.search(r"module\s+(\w+)\s*\((.*?)\)\s*;", public, re.S)
    if not header:
        raise ValueError("Expected the vendor's public non-ANSI module header")
    parameters = [{"name": name, "value": value.strip()} for name, value in
                  re.findall(r"\bparameter\s+(\w+)\s*=\s*([^;]+);", public)]
    ports = {}
    for direction, width, names in re.findall(
            r"\b(input|output|inout)\s*(\[[^\]]+\])?\s*([^;]+);", public):
        for name in names.split(","):
            name = name.strip()
            if not re.fullmatch(r"[A-Za-z_]\w*", name) or name in ports:
                raise ValueError("Ambiguous public port declaration")
            ports[name] = {"name": name, "direction": direction,
                           "width": width[1:-1].strip() if width else ""}
    order = [name.strip() for name in header[2].split(",")]
    if len(order) != len(ports) or set(order) != set(ports):
        raise ValueError("Public header and port declarations disagree")
    if len(parameters) != len({item["name"] for item in parameters}):
        raise ValueError("Duplicate vendor parameter declaration")
    return {"modules": [{"name": header[1], "parameters": parameters,
                         "ports": [ports[name] for name in order]}]}


def extract():
    manifest = public_manifest(VENDOR.read_text(encoding="utf-8"))
    module = manifest["modules"][0]
    if module["name"] != "PH1P_LOGIC_ERAM" or len(module["parameters"]) != 30:
        raise ValueError("Unexpected vendor interface revision; review before using")
    interface_dir = ROOT / "interfaces"
    manifest.update(source=str(VENDOR), source_sha256=digest(VENDOR),
                    boundary="Exact public declarations only; no behavior or clock-boundary proof")
    manifest_path = interface_dir / "ph1p_eram_manifest.json"
    save_json(manifest_path, manifest)
    # The canonical manifest renderer rejects the official BYTE_A/B ternary.
    # Its extractor supports that expression, but only parameters before ports.
    # Reorder declarations mechanically, preserving every value and port width.
    ordered = "module PH1P_LOGIC_ERAM(" + ",".join(port["name"] for port in module["ports"]) + ");\n"
    ordered += "\n".join("parameter " + item["name"] + " = " + item["value"] + ";"
                         for item in module["parameters"]) + "\n"
    ordered += "\n".join(port["direction"] + " " +
                         ("[" + port["width"] + "] " if port["width"] else "") +
                         port["name"] + ";" for port in module["ports"]) + "\nendmodule\n"
    if public_manifest(ordered)["modules"][0] != module:
        raise ValueError("Declaration reordering changed public interface facts")
    ordered_path = interface_dir / "ph1p_eram_declaration_order.v"
    ordered_path.write_text(ordered, encoding="utf-8")
    output = interface_dir / "ph1p_eram_interface_complete.v"
    subprocess.run([sys.executable, "-B", "-X", "utf8", "-m",
                    "scripts.python.quality.external_interface_stubs", "extract",
                    "--source", str(ordered_path), "--module", "PH1P_LOGIC_ERAM", "--output", str(output)],
                   cwd=SKILL, check=True, timeout=30)
    if public_manifest(output.read_text(encoding="utf-8"))["modules"][0] != module:
        raise ValueError("Canonical extraction changed public interface facts")
    save_json(interface_dir / "complete_provenance.json", {
        "source": str(VENDOR), "source_sha256": digest(VENDOR),
        "manifest_sha256": digest(manifest_path), "interface_sha256": digest(output),
        "extractor_sha256": digest(Path(__file__)), "parameter_count": 30,
        "ordered_declarations_sha256": digest(ordered_path),
        "canonical_renderer": "scripts.python.quality.external_interface_stubs extract",
        "use": "Static interface facts only; prohibited in simulation/synthesis"})
    print("PASS: all 30 official parameters preserved; protected body excluded")


def self_check():
    text = '''module example(a,z);
parameter WIDTH=9;
input [WIDTH-1:0] a;
output z;
parameter MODE="SP";
`pragma protect begin_protected
parameter NOT_PUBLIC=1;
'''
    module = public_manifest(text)["modules"][0]
    assert module["parameters"] == [{"name": "WIDTH", "value": "9"},
                                    {"name": "MODE", "value": '"SP"'}]
    assert module["ports"][0]["width"] == "WIDTH-1:0"
    assert [port["name"] for port in module["ports"]] == ["a", "z"]
    for bad in (text.replace("a,z", "a,b"), text.replace("output z;", "output z; output z;")):
        try:
            public_manifest(bad)
        except ValueError:
            continue
        raise AssertionError("Conflicting public declarations must fail closed")
    print("PASS: trailing parameters, port order, protected body and conflict checks")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    self_check() if args.self_check else extract()
