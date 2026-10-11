"""Copy the frozen v10 candidate fixtures and the v11 RTL into this run area."""
from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
V11 = HERE.parent
V10_VERIFY = V11.parent / "v10_postprocess_overlap_20261007" / "verification"
SOURCE = V10_VERIFY / "regression_candidate"
DEST = HERE / "regression_candidate"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copy2(source, destination)


def main() -> None:
    copy_file(SOURCE / "tb_road_postprocess_stream.v", DEST / "tb_road_postprocess_stream.v")
    copy_file(SOURCE / "tb_down2_overlap_tile_runner.v", DEST / "tb_down2_overlap_tile_runner.v")
    for source in sorted((SOURCE / "vectors").iterdir()):
        if source.is_file():
            copy_file(source, DEST / "vectors" / source.name)
    for name in ("road_round_shift.v", "silu_shared_unit.v", "road_mac_probe.v",
                 "ph1p_logic_eram.v", "ph1p_phy_gsr.v"):
        copy_file(SOURCE / name, DEST / name)
    copy_file(V11 / "rtl" / "road_postprocess_stream.v", DEST / "road_postprocess_stream.v")
    copy_file(V11 / "rtl" / "down2_overlap_tile_runner.v", DEST / "down2_overlap_tile_runner.v")
    print("PREPARE_CANDIDATE_PASS")


if __name__ == "__main__":
    main()
