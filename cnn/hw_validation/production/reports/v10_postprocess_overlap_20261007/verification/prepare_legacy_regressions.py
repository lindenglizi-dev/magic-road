"""Copy frozen legacy regressions into isolated v10 working directories."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_exact(source: Path, target: Path) -> dict[str, object]:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    if sha256(source) != sha256(target):
        raise RuntimeError(f"copy mismatch: {source}")
    return {
        "source": str(source),
        "copy": str(target),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "transformation": "none",
    }


def copy_tb_with_paths(
    source: Path, target: Path, replacements: dict[str, str]
) -> dict[str, object]:
    original = source.read_text(encoding="utf-8")
    changed = original
    counts: dict[str, int] = {}
    for old, new in replacements.items():
        counts[old] = changed.count(old)
        if counts[old] == 0:
            raise RuntimeError(f"path not found in {source}: {old}")
        changed = changed.replace(old, new)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(changed, encoding="utf-8", newline="\n")
    return {
        "source": str(source),
        "copy": str(target),
        "bytes": target.stat().st_size,
        "source_sha256": sha256(source),
        "sha256": sha256(target),
        "transformation": "path-only",
        "replacements": counts,
    }


def prepare_shell() -> list[dict[str, object]]:
    target = ROOT / "regression_v9_shell"
    v7_inputs = REPORTS / "v7_onchip_chain_20261006" / "inputs"
    low_io = REPORTS / "v7_low_io_physical_20261006" / "shell"
    v8_reset = REPORTS / "v8_reset_layer_tiles_20261007" / "reset"
    v9 = REPORTS / "v9_mac_stream_20261007"
    records = []
    for source, relative in [
        (v7_inputs / "ph1p_logic_eram.v", "ph1p_logic_eram.v"),
        (v7_inputs / "ph1p_phy_gsr.v", "ph1p_phy_gsr.v"),
        (v9 / "core" / "road_mac_probe.v", "road_mac_probe.v"),
        (v7_inputs / "road_round_shift.v", "road_round_shift.v"),
        (v7_inputs / "silu_shared_unit.v", "silu_shared_unit.v"),
        (REPORTS / "v7_onchip_chain_20261006" / "road_onchip_chain.v",
         "road_onchip_chain.v"),
        (low_io / "road_low_io_physical_shell.v", "road_low_io_physical_shell.v"),
        (v8_reset / "road_low_io_reset_shell.v", "road_low_io_reset_shell.v"),
    ]:
        records.append(copy_exact(source, target / relative))
    for source in sorted((low_io / "inputs").iterdir()):
        if source.is_file():
            records.append(copy_exact(source, target / "inputs" / source.name))
    replacements = {
        "../../v7_low_io_physical_20261006/shell/inputs/": "inputs/"
    }
    tb_dir = v9 / "verification" / "shell_v9_tb"
    for name in (
        "tb_road_low_io_reset_shell_regression_v9.v",
        "tb_road_low_io_reset_shell_v9.v",
    ):
        records.append(copy_tb_with_paths(tb_dir / name, target / name, replacements))
    return records


def prepare_round() -> list[dict[str, object]]:
    source = REPORTS / "v3_round_stall_20261005"
    target = ROOT / "regression_round_7042"
    return [
        copy_exact(source / name, target / name)
        for name in ("road_round_shift.v", "tb_road_round_shift_stall.v", "vectors.dath")
    ]


def prepare_silu() -> list[dict[str, object]]:
    source = REPORTS / "v4_silu_regression_20261005"
    target = ROOT / "regression_silu_65536"
    records = []
    for old, relative in [
        (source / "vendor_sources" / "ph1p_logic_eram.v", "ph1p_logic_eram.v"),
        (source / "vendor_sources" / "ph1p_phy_gsr.v", "ph1p_phy_gsr.v"),
        (source / "candidate" / "silu_shared_unit.v", "silu_shared_unit.v"),
        (source / "frozen_data" / "silu_table.hex", "frozen_data/silu_table.hex"),
        (source / "frozen_data" / "silu_expected.hex", "frozen_data/silu_expected.hex"),
    ]:
        records.append(copy_exact(old, target / relative))
    records.append(copy_tb_with_paths(
        source / "tb_silu_shared_unit.v",
        target / "tb_silu_shared_unit.v",
        {"../../silu/generated/": "frozen_data/"},
    ))
    return records


def main() -> None:
    manifest = {
        "status": "COPIED_FROZEN_INPUTS_HASH_MATCH",
        "note": "Only copied testbench file paths were changed; checks are unchanged.",
        "v9_shell_14_plus_reset6": prepare_shell(),
        "round_7042": prepare_round(),
        "silu_65536": prepare_silu(),
    }
    output = ROOT / "legacy_inputs_manifest.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: len(value) for key, value in manifest.items()
                      if isinstance(value, list)}, sort_keys=True))


if __name__ == "__main__":
    main()
