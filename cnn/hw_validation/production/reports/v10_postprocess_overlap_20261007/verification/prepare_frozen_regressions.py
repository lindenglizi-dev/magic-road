"""Copy the exact frozen v9 MAC and v8 layer regression inputs locally."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parents[1]
V10 = ROOT.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_set(destination: Path, sources: list[tuple[Path, Path]]) -> list[dict[str, object]]:
    records = []
    for source, relative in sources:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if sha256(source) != sha256(target):
            raise RuntimeError(f"copy mismatch: {source}")
        records.append({"source": str(source), "copy": str(target),
                        "bytes": target.stat().st_size, "sha256": sha256(target)})
    return records


def main() -> None:
    v9 = REPORTS / "v9_mac_stream_20261007"
    v9_sources = [
        (v9 / "core" / "road_mac_probe.v", Path("road_mac_probe.v")),
        (v9 / "verification" / "tb_road_mac_stream.v", Path("tb_road_mac_stream.v")),
        (v9 / "verification" / "stream_vectors.txt", Path("stream_vectors.txt")),
    ]

    v8 = REPORTS / "v8_reset_layer_tiles_20261007" / "layers"
    v7 = REPORTS / "v7_onchip_chain_20261006" / "inputs"
    v8_sources = [
        (v7 / name, Path(name)) for name in (
            "ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_mac_probe.v",
            "road_round_shift.v", "silu_shared_unit.v")
    ]
    v8_sources.extend((v8 / name, Path(name)) for name in
                      ("down2_tile_runner.v", "tb_down2_tile_runner.v"))
    v8_sources.extend((path, Path("vectors") / path.name)
                      for path in sorted((v8 / "vectors").glob("*.hex")))
    v9_serial_sources = [
        (v9 / "core" / "road_mac_probe.v", Path("road_mac_probe.v"))
        if relative == Path("road_mac_probe.v") else (source, relative)
        for source, relative in v8_sources
    ]
    candidate_sources = [
        (source, Path("tb_down2_overlap_tile_runner.v")
         if relative == Path("tb_down2_tile_runner.v") else relative)
        for source, relative in v9_serial_sources
        if relative != Path("down2_tile_runner.v")
    ]
    candidate_sources.extend((V10 / "rtl" / name, Path(name)) for name in
                             ("road_postprocess_stream.v", "down2_overlap_tile_runner.v"))

    manifest = {
        "status": "COPIED_INPUTS_HASH_MATCH",
        "v9_mac_123": copy_set(ROOT / "regression_v9_mac", v9_sources),
        "v8_four_layer_cases": copy_set(ROOT / "regression_v8_layers", v8_sources),
        "v9_mac_serial_four_layer_cases":
            copy_set(ROOT / "regression_v9_serial_layers", v9_serial_sources),
        "candidate_four_layer_cases":
            copy_set(ROOT / "regression_candidate", candidate_sources),
    }
    (ROOT / "copied_inputs_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"],
                      "v9_files": len(manifest["v9_mac_123"]),
                      "v8_files": len(manifest["v8_four_layer_cases"]),
                      "v9_serial_files": len(manifest["v9_mac_serial_four_layer_cases"])},
                     
                     sort_keys=True))


if __name__ == "__main__":
    main()
