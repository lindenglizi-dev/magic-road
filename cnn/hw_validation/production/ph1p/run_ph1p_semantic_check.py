"""Run the governed PH1P interface-only semantic check.

This adapter deliberately models only the public PH1P_LOGIC_ERAM interface.
The encrypted implementation is never interpreted, and every output remains an
opaque hierarchy boundary until vendor timing behaviour is independently proven.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


MODULE_NAME = "PH1P_LOGIC_ERAM"
INSTANCE_NAME = "PH1P_LOGIC_ERAM_Inst_silu_table"
PROTECT_MARKER = b"`pragma protect begin_protected"
EXPECTED_HEADER_SHA256 = "9e1c7a39b4f0d8ecbe78301a737674beac63b53237d1970b0003439822cb1627"
EXPECTED_FULL_SHA256 = "70d89b70bdd51812ad86b91e88526b4604ebb117516efda5af976fcddb2e69af"

PORT_ORDER = (
    "dia", "addra", "cea", "ocea", "clka", "wea", "rsta", "bea",
    "dib", "addrb", "ceb", "oceb", "clkb", "web", "rstb", "beb",
    "ecc_sbiterrinj", "ecc_dbiterrinj", "doa", "dob", "ecc_sbiterr",
    "ecc_dbiterr",
)

SUPPORTED_PARAMETERS: dict[str, str] = {
    "DATA_WIDTH_A": "20",
    "DATA_WIDTH_B": "20",
    "ADDR_WIDTH_A": "10",
    "ADDR_WIDTH_B": "10",
    "DATA_DEPTH_A": "1024",
    "DATA_DEPTH_B": "1024",
    "BYTE_ENABLE": "0",
    "BYTE_A": "1",
    "BYTE_B": "1",
    "MODE": '"SP"',
    "REGMODE_A": '"NOREG"',
    "REGMODE_B": '"NOREG"',
    "WRITEMODE_A": '"NORMAL"',
    "WRITEMODE_B": '"NORMAL"',
    "RESETMODE_A": '"ASYNC"',
    "RESETMODE_B": '"ASYNC"',
    "OREGSET_A": '"RESET"',
    "OREGSET_B": '"RESET"',
    "SSROVERCE": '"DISABLE"',
    "ECC_DECODE": '"DISABLE"',
    "ECC_ENCODE": '"DISABLE"',
    "ASYNC_RESET_RELEASE_A": '"ASYNC"',
    "ASYNC_RESET_RELEASE_B": '"ASYNC"',
    "CLKMODE": '"ASYNC"',
    "DEBUGGABLE": '"NO"',
    "PACKABLE": '"NO"',
    "FORCE_KEEP": '"ON"',
    "INIT_FILE": '"NONE"',
    "FILL_ALL": '"NONE"',
    "IMPLEMENT": '"20K"',
}

HEADER_DEFAULTS: dict[str, str] = {
    "DATA_WIDTH_A": "20",
    "DATA_WIDTH_B": "DATA_WIDTH_A",
    "ADDR_WIDTH_A": "10",
    "ADDR_WIDTH_B": "ADDR_WIDTH_A",
    "DATA_DEPTH_A": "2**ADDR_WIDTH_A",
    "DATA_DEPTH_B": "2**ADDR_WIDTH_B",
    "BYTE_ENABLE": "0",
    "BYTE_A": "BYTE_ENABLE==0?1:DATA_WIDTH_A/BYTE_ENABLE",
    "BYTE_B": "BYTE_ENABLE==0?1:DATA_WIDTH_B/BYTE_ENABLE",
    "MODE": '"DP"',
    "REGMODE_A": '"NOREG"',
    "REGMODE_B": '"NOREG"',
    "WRITEMODE_A": '"NORMAL"',
    "WRITEMODE_B": '"NORMAL"',
    "RESETMODE_A": '"ASYNC"',
    "RESETMODE_B": '"ASYNC"',
    "OREGSET_A": '"SET"',
    "OREGSET_B": '"SET"',
    "SSROVERCE": '"ENABLE"',
    "ECC_DECODE": '"DISABLE"',
    "ECC_ENCODE": '"DISABLE"',
    "ASYNC_RESET_RELEASE_A": '"SYNC"',
    "ASYNC_RESET_RELEASE_B": '"SYNC"',
    "CLKMODE": '"ASYNC"',
    "DEBUGGABLE": '"NO"',
    "PACKABLE": '"NO"',
    "FORCE_KEEP": '"OFF"',
    "INIT_FILE": '"NONE"',
    "FILL_ALL": '"NONE"',
    "IMPLEMENT": '"20K"',
}


def _compact(text: str) -> str:
    """Remove whitespace without changing quoted literal content used here."""

    return re.sub(r"\s+", "", text)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _parse_named_associations(block: str, *, literals_only: bool) -> list[tuple[str, str]]:
    """Parse and fully consume named associations, rejecting duplicates."""

    clean = re.sub(r"//[^\r\n]*", "", block)
    associations: list[tuple[str, str]] = []
    names: set[str] = set()
    position = 0
    while position < len(clean):
        separator = re.match(r"\s*(?:,\s*)?", clean[position:])
        position += separator.end() if separator else 0
        if position == len(clean):
            break
        opening = re.match(r"\.([A-Za-z_]\w*)\s*\(", clean[position:])
        if opening is None:
            raise ValueError(f"unparsed named-association text: {clean[position:position + 40]!r}")
        name = opening.group(1)
        if name in names:
            raise ValueError(f"duplicate named association: {name}")
        names.add(name)
        value_start = position + opening.end()
        cursor = value_start
        depth = 1
        quoted = False
        while cursor < len(clean) and depth:
            character = clean[cursor]
            if character == '"':
                quoted = not quoted
            elif not quoted and character == "(":
                depth += 1
            elif not quoted and character == ")":
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError(f"unterminated named association: {name}")
        value = clean[value_start:cursor - 1].strip()
        if literals_only and re.fullmatch(r'"[^"\r\n]*"|[0-9]+', value) is None:
            raise ValueError(f"non-literal parameter association: {name}={value}")
        associations.append((name, _compact(value)))
        position = cursor
        trailer = re.match(r"\s*", clean[position:])
        position += trailer.end() if trailer else 0
        if position < len(clean) and clean[position] != ",":
            raise ValueError(f"unexpected association trailer: {clean[position:position + 40]!r}")
    return associations


def read_and_validate_header(source: Path) -> dict[str, Any]:
    """Validate the exact public header and never consume protected semantics."""

    raw = source.read_bytes()
    marker_offset = raw.find(PROTECT_MARKER)
    if marker_offset < 0:
        raise ValueError("protected marker missing")
    header_bytes = raw[:marker_offset]
    header_sha256 = _sha256(header_bytes)
    if header_sha256 != EXPECTED_HEADER_SHA256:
        raise ValueError(f"public header SHA mismatch: {header_sha256}")
    header = header_bytes.decode("ascii")

    module_match = re.search(
        rf"module\s+{MODULE_NAME}\s*\((.*?)\);",
        header,
        flags=re.DOTALL,
    )
    if module_match is None:
        raise ValueError("public module declaration missing")
    parsed_ports = tuple(
        token for token in re.split(r"[\s,]+", module_match.group(1).strip()) if token
    )
    if parsed_ports != PORT_ORDER:
        raise ValueError(f"public port order mismatch: {parsed_ports}")

    parsed_defaults = {
        name: _compact(value)
        for name, value in re.findall(
            r"\bparameter\s+([A-Za-z_]\w*)\s*=\s*([^;]+);",
            header,
        )
    }
    if parsed_defaults != HEADER_DEFAULTS:
        raise ValueError("public parameter defaults differ from the pinned contract")
    if not re.search(r"\binput\s+clka\s*;.*?Clock A signal", header):
        raise ValueError("clka public clock role missing")
    if not re.search(r"\binput\s+clkb\s*;.*?Clock B signal", header):
        raise ValueError("clkb public clock role missing")

    return {
        "source": str(source.resolve()),
        "marker_offset": marker_offset,
        "public_header_sha256": header_sha256,
        "expected_public_header_sha256": EXPECTED_HEADER_SHA256,
        "full_file_sha256_observed": _sha256(raw),
        "full_file_sha256_reference": EXPECTED_FULL_SHA256,
        "port_order": list(parsed_ports),
        "parameter_defaults": parsed_defaults,
        "protected_payload_interpreted": False,
        "status": "passed",
    }


def extract_instance_binding(rtl: Path) -> dict[str, Any]:
    """Extract the one named SiLU PH1P instance with conservative syntax."""

    text = rtl.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"\b{MODULE_NAME}\s*#\s*\((.*?)\)\s*{INSTANCE_NAME}\s*\((.*?)\)\s*;",
        flags=re.DOTALL,
    )
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"expected one {INSTANCE_NAME} instance, found {len(matches)}")
    parameter_block, port_block = matches[0]
    parameter_associations = _parse_named_associations(parameter_block, literals_only=True)
    parameters = dict(parameter_associations)
    if parameters != SUPPORTED_PARAMETERS:
        missing = sorted(set(SUPPORTED_PARAMETERS) - set(parameters))
        extra = sorted(set(parameters) - set(SUPPORTED_PARAMETERS))
        changed = {
            key: {"expected": value, "observed": parameters.get(key)}
            for key, value in SUPPORTED_PARAMETERS.items()
            if parameters.get(key) != value
        }
        raise ValueError(
            f"unsupported parameter binding: missing={missing}, extra={extra}, changed={changed}"
        )
    port_names = tuple(name for name, _value in _parse_named_associations(port_block, literals_only=False))
    if port_names != PORT_ORDER:
        raise ValueError(f"instance port order/set mismatch: {port_names}")
    return {
        "rtl": str(rtl.resolve()),
        "rtl_sha256": _sha256(rtl.read_bytes()),
        "instance": INSTANCE_NAME,
        "parameters": parameters,
        "ports": list(port_names),
        "status": "passed",
    }


def build_profile(parameters: dict[str, str]) -> dict[str, Any]:
    """Build only the single audited 20x1024 profile; reject all variants."""

    if parameters != SUPPORTED_PARAMETERS:
        raise ValueError("only the audited SiLU 20x1024 PH1P configuration is supported")
    widths = {
        "dia": 20, "addra": 10, "cea": 1, "ocea": 1, "clka": 1,
        "wea": 1, "rsta": 1, "bea": 1, "dib": 20, "addrb": 10,
        "ceb": 1, "oceb": 1, "clkb": 1, "web": 1, "rstb": 1,
        "beb": 1, "ecc_sbiterrinj": 1, "ecc_dbiterrinj": 1,
        "doa": 20, "dob": 20, "ecc_sbiterr": 1, "ecc_dbiterr": 1,
    }
    outputs = {name for name in ("doa", "dob", "ecc_sbiterr", "ecc_dbiterr")}
    roles = {
        "clka": ["clock_input"],
        "clkb": ["clock_input"],
        "cea": ["clock_enable"],
        "ocea": ["clock_enable"],
        "ceb": ["clock_enable"],
        "oceb": ["clock_enable"],
        "rsta": ["reset_control"],
        "rstb": ["reset_control"],
    }
    ports: dict[str, dict[str, Any]] = {}
    for name in PORT_ORDER:
        ports[name] = {
            "direction": "output" if name in outputs else "input",
            "width": widths[name],
            "roles": roles.get(name, ["data"]),
        }
    profile = {
        "name": MODULE_NAME,
        "module_name": MODULE_NAME,
        "profile_id": "ANLOGIC::PH1P_LOGIC_ERAM::silu_20x1024_header_only",
        "library": "ANLOGIC",
        "family": "embedded_ram",
        "support_level": "P2_BOUNDARY",
        "clock_capable": True,
        "ports": ports,
        "outputs": {name: "opaque" for name in outputs},
        "authority": {
            "public_header_sha256": EXPECTED_HEADER_SHA256,
            "configuration": copy.deepcopy(SUPPORTED_PARAMETERS),
            "behaviour_proven": False,
        },
    }
    validate_profile(profile)
    return profile


def validate_profile(profile: dict[str, Any]) -> None:
    """Reject broadened identity, widths, clock roles, or output semantics."""

    if profile.get("module_name") != MODULE_NAME:
        raise ValueError("profile module identity mismatch")
    if tuple(profile.get("ports", {})) != PORT_ORDER:
        raise ValueError("profile port order mismatch")
    expected_widths = build_expected_widths()
    observed_widths = {
        name: int(details.get("width", 0))
        for name, details in profile["ports"].items()
    }
    if observed_widths != expected_widths:
        raise ValueError("profile width mismatch")
    output_names = {"doa", "dob", "ecc_sbiterr", "ecc_dbiterr"}
    expected_directions = {
        name: "output" if name in output_names else "input" for name in PORT_ORDER
    }
    observed_directions = {
        name: str(details.get("direction") or "")
        for name, details in profile["ports"].items()
    }
    if observed_directions != expected_directions:
        raise ValueError("profile direction mismatch")
    clock_role_names = {"clock_input", "clock_output", "clock_feedback", "clock_capable"}
    clock_ports = {
        name
        for name, details in profile["ports"].items()
        if set(details.get("roles", [])) & clock_role_names
    }
    if clock_ports != {"clka", "clkb"}:
        raise ValueError(f"profile clock roles invalid: {sorted(clock_ports)}")
    if profile["ports"]["clka"].get("roles") != ["clock_input"]:
        raise ValueError("clka role set is not exact")
    if profile["ports"]["clkb"].get("roles") != ["clock_input"]:
        raise ValueError("clkb role set is not exact")
    expected_outputs = {name: "opaque" for name in ("doa", "dob", "ecc_sbiterr", "ecc_dbiterr")}
    if profile.get("outputs") != expected_outputs:
        raise ValueError("all PH1P outputs must remain opaque")


def build_expected_widths() -> dict[str, int]:
    widths = {name: 1 for name in PORT_ORDER}
    widths.update({"dia": 20, "dib": 20, "doa": 20, "dob": 20, "addra": 10, "addrb": 10})
    return widths


def run_self_checks(profile: dict[str, Any], skill_root: Path) -> list[dict[str, Any]]:
    """Exercise required fail-closed boundaries without modifying the skill."""

    sys.path.insert(0, str(skill_root))
    from scripts.python.quality.vg_primitive_facts import (  # pylint: disable=import-outside-toplevel
        coerce_primitive_catalog,
        primitive_port_is_clock_role,
        resolve_primitive_profile,
    )

    results: list[dict[str, Any]] = []

    unknown = resolve_primitive_profile("PH1P_LOGIC_ERAM_UNKNOWN")
    results.append({
        "name": "unknown_module_rejected",
        "passed": unknown.get("status") == "inconclusive" and unknown.get("profile") is None,
        "observed": unknown,
    })

    bad_parameters = copy.deepcopy(SUPPORTED_PARAMETERS)
    bad_parameters["DATA_WIDTH_A"] = "16"
    try:
        build_profile(bad_parameters)
        rejected_bad_parameters = False
    except ValueError:
        rejected_bad_parameters = True
    results.append({
        "name": "bad_parameter_rejected",
        "passed": rejected_bad_parameters,
        "mutation": {"DATA_WIDTH_A": "16"},
    })

    try:
        _parse_named_associations(".DATA_WIDTH_A(SOME_EXPR)", literals_only=True)
        rejected_unknown_parameter_value = False
    except ValueError:
        rejected_unknown_parameter_value = True
    results.append({
        "name": "nonliteral_parameter_rejected",
        "passed": rejected_unknown_parameter_value,
        "mutation": {"DATA_WIDTH_A": "SOME_EXPR"},
    })

    try:
        _parse_named_associations(
            ".DATA_WIDTH_A(20), .DATA_WIDTH_A(20)",
            literals_only=True,
        )
        rejected_duplicate_parameter = False
    except ValueError:
        rejected_duplicate_parameter = True
    results.append({
        "name": "duplicate_parameter_rejected",
        "passed": rejected_duplicate_parameter,
        "mutation": {"DATA_WIDTH_A": "duplicated"},
    })

    bad_width_profile = copy.deepcopy(profile)
    bad_width_profile["ports"]["dia"]["width"] = 16
    try:
        validate_profile(bad_width_profile)
        rejected_bad_width = False
    except ValueError:
        rejected_bad_width = True
    results.append({
        "name": "bad_port_width_rejected",
        "passed": rejected_bad_width,
        "mutation": {"dia.width": 16},
    })

    bad_role_profile = copy.deepcopy(profile)
    bad_role_profile["ports"]["dia"]["roles"] = ["data", "clock_input"]
    try:
        validate_profile(bad_role_profile)
        rejected_bad_role = False
    except ValueError:
        rejected_bad_role = True
    catalog = coerce_primitive_catalog(profile)
    role_api_passed = (
        primitive_port_is_clock_role(catalog, MODULE_NAME, "clka")
        and primitive_port_is_clock_role(catalog, MODULE_NAME, "clkb")
        and not primitive_port_is_clock_role(catalog, MODULE_NAME, "dia")
        and not primitive_port_is_clock_role(catalog, MODULE_NAME, "cea")
        and not primitive_port_is_clock_role(catalog, MODULE_NAME, "rsta")
    )
    results.append({
        "name": "ordinary_data_not_clock",
        "passed": rejected_bad_role and role_api_passed,
        "clock_ports": ["clka", "clkb"],
        "explicit_non_clock_ports_checked": ["dia", "cea", "rsta"],
    })

    if not all(item["passed"] for item in results):
        raise RuntimeError("one or more PH1P fail-closed self-checks failed")
    return results


def write_markdown(report: dict[str, Any], destination: Path) -> None:
    semantic = report.get("semantic_gate", {})
    delivery_issues = semantic.get("delivery_issues_by_rule", {})
    status_counts = semantic.get("vg_rule_summary", {}).get("status_counts", {})
    lines = [
        "# PH1P interface-only semantic check",
        "",
        f"- Interface support ready: `{str(report['interface_support_ready']).lower()}`",
        f"- Eight-gate delivery claimed: `false`",
        f"- Existing strict gate modified: `false`",
        f"- Public header SHA-256: `{report['authority']['public_header_sha256']}`",
        f"- SiLU RTL SHA-256: `{report['binding']['rtl_sha256']}`",
        f"- Semantic delivery ready: `{str(semantic.get('delivery_ready', False)).lower()}`",
        f"- Semantic rule status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        f"- Semantic delivery issues: `{json.dumps(delivery_issues, sort_keys=True)}`",
        "",
        "## Scope boundary",
        "",
        "Only the exact current 20x1024 SiLU instance is admitted. The encrypted vendor body was not interpreted. REGMODE=NOREG timing is not treated as proven, so doa, dob, ecc_sbiterr, and ecc_dbiterr remain opaque; no state_cut is asserted.",
        "",
        "## Required negative checks",
        "",
    ]
    lines.extend(
        f"- {item['name']}: `{'PASS' if item['passed'] else 'FAIL'}`"
        for item in report["self_checks"]
    )
    lines.extend([
        "",
        "## Remaining boundary",
        "",
        "This is a standalone semantic API report, not the high-level eight-gate quality report. It supplies exact interface widths and clock roles only. Vendor read latency, output-register behaviour, collision semantics, reset release behaviour, synthesis mapping, timing closure, and board behaviour remain unproven. TD was not run.",
        "",
    ])
    destination.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rtl", type=Path, required=True)
    parser.add_argument("--vendor-source", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report: dict[str, Any] = {
        "schema": "ph1p-interface-semantic-check-v1",
        "interface_support_ready": False,
        "eight_gate_delivery_claimed": False,
        "existing_gate_modified": False,
        "td_run": False,
    }
    try:
        report["authority"] = read_and_validate_header(args.vendor_source)
        report["binding"] = extract_instance_binding(args.rtl)
        profile = build_profile(report["binding"]["parameters"])
        report["primitive_profile"] = profile
        report["self_checks"] = run_self_checks(profile, args.skill_root.resolve())

        from scripts.python.quality.vg_semantic_engine import (  # pylint: disable=import-outside-toplevel
            run_vg_semantic_gate,
        )

        report["semantic_gate"] = run_vg_semantic_gate(
            args.rtl.resolve(),
            strict=True,
            include_testbench=False,
            primitive_profile=profile,
        )
        report["interface_support_ready"] = True
        exit_code = 0
    except Exception as error:  # fail closed and preserve diagnostic evidence
        report["fatal_error"] = f"{type(error).__name__}: {error}"
        exit_code = 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(report, args.output.with_suffix(".md")) if report.get("authority") and report.get("binding") else None
    print(json.dumps({
        "interface_support_ready": report["interface_support_ready"],
        "semantic_delivery_ready": report.get("semantic_gate", {}).get("delivery_ready", False),
        "fatal_error": report.get("fatal_error"),
        "output": str(args.output.resolve()),
    }, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
