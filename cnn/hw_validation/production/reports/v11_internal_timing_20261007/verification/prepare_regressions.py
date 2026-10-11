"""Copy only frozen source and vector inputs for fresh v11 regressions."""
from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
V10 = HERE.parent.parent / "v10_postprocess_overlap_20261007" / "verification"
SUITES = (
    "regression_v9_mac",
    "regression_v9_serial_layers",
    "regression_v8_layers",
    "regression_v9_shell",
    "regression_round_7042",
    "regression_silu_65536",
)
DATA_DIRS = {"vectors", "inputs", "frozen_data"}
TOP_SUFFIXES = {".v", ".txt", ".csv", ".dath", ".hex"}


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copy2(source, destination)


def main() -> None:
    for suite in SUITES:
        source_root = V10 / suite
        destination_root = HERE / suite
        for source in sorted(source_root.rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(source_root)
            if relative.parent == Path(".") and source.suffix.lower() in TOP_SUFFIXES:
                copy(source, destination_root / relative)
            elif relative.parts and relative.parts[0] in DATA_DIRS:
                copy(source, destination_root / relative)
    print("PREPARE_REGRESSIONS_PASS")


if __name__ == "__main__":
    main()
