"""Fail-closed identity and functional gate for the single v11 TD build."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "prebuild_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_hashes(items: list[dict[str, str]], label: str) -> None:
    for item in items:
        path = (ROOT / item["path"]).resolve()
        actual = sha256(path)
        expected = item["sha256"].lower()
        if actual != expected:
            raise SystemExit(
                f"FAIL {label} hash {item['path']}: expected {expected}, got {actual}"
            )


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "FROZEN_FOR_SINGLE_PHYSICAL_BUILD":
        raise SystemExit("FAIL manifest is not frozen for the single physical build")
    if manifest.get("single_build_only") is not True:
        raise SystemExit("FAIL single-build policy is not asserted")
    if manifest.get("bitstream_requested") is not False:
        raise SystemExit("FAIL bitstream policy is not disabled")
    constraints = manifest.get("constraints", {})
    if constraints.get("exceptions_added") is not False:
        raise SystemExit("FAIL timing exceptions are present")
    if constraints.get("report_endpoint_limit") != 100000:
        raise SystemExit("FAIL report endpoint limit is not 100000")

    check_hashes(manifest["source_read_order"], "source")
    check_hashes(
        [
            {"path": name, "sha256": digest}
            for name, digest in manifest["flow_sha256"].items()
            if name != "road_postprocess_low_io_top.al_prebuild"
        ],
        "flow",
    )
    project_expected = manifest["flow_sha256"]["road_postprocess_low_io_top.al_prebuild"]
    project_actual = sha256(ROOT / "road_postprocess_low_io_top.al")
    if project_actual != project_expected:
        raise SystemExit(
            f"FAIL project hash: expected {project_expected}, got {project_actual}"
        )
    check_hashes(
        [
            {"path": name, "sha256": digest}
            for name, digest in manifest["functional_evidence_sha256"].items()
        ],
        "functional evidence",
    )

    runner = (ROOT / "../verification/regression_candidate/vsim_runner.log").read_text(
        encoding="utf-8", errors="replace"
    )
    standalone = (
        ROOT / "../verification/regression_candidate/vsim_postprocess_attempt3.log"
    ).read_text(encoding="utf-8", errors="replace")
    required = (
        (runner, "TB_PASS_DOWN2_TILE cases=4", "runner PASS"),
        (runner, "Errors: 0", "runner zero errors"),
        (standalone, "TB_PASS_POSTPROCESS", "standalone PASS"),
        (standalone, "Errors: 0", "standalone zero errors"),
    )
    for text, marker, label in required:
        if marker not in text:
            raise SystemExit(f"FAIL missing {label}: {marker}")

    print("PASS PREBUILD_IDENTITY_AND_FUNCTIONAL_GATE")
    print(f"stream={manifest['source_read_order'][2]['sha256']}")
    print(f"runner={manifest['source_read_order'][1]['sha256']}")
    print("single_td_build_authorized=1")


if __name__ == "__main__":
    main()
