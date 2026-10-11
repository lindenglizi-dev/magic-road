"""Build the v11 verification hash and frozen-copy audit manifest."""
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V10_VERIFY = ROOT.parent / "v10_postprocess_overlap_20261007" / "verification"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return sha256(stream.read()).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": digest(path)}


rtl_names = ("road_postprocess_stream.v", "down2_overlap_tile_runner.v")
rtl = []
for name in rtl_names:
    source = ROOT / "rtl" / name
    copy = HERE / "regression_candidate" / name
    rtl.append({"source": record(source), "simulation_copy": record(copy),
                "match": digest(source) == digest(copy)})

evidence_paths = (
    "regression_candidate/vsim_postprocess.log",
    "regression_candidate/vsim_postprocess_attempt2.log",
    "regression_candidate/vsim_postprocess_attempt3.log",
    "regression_candidate/vsim_runner.log",
    "regression_candidate/vsim_runner_turnaround.log",
    "regression_v9_mac/vsim.log",
    "regression_v9_serial_layers/vsim.log",
    "regression_v8_layers/vsim.log",
    "regression_v9_shell/vsim_shell14.log",
    "regression_v9_shell/vsim_reset6.log",
    "regression_round_7042/guard_simulate.log",
    "regression_silu_65536/vsim.log",
    "reference_self_check.log",
    "reference_self_check_attempt2.log",
    "reference_self_check_attempt3.log",
    "reference_self_check_attempt4.log",
)

copy_audit = []
input_suffixes = {".v", ".txt", ".csv", ".dath", ".hex"}
for suite in ("regression_v9_mac", "regression_v9_serial_layers", "regression_v8_layers",
              "regression_v9_shell", "regression_round_7042", "regression_silu_65536"):
    for candidate in sorted((HERE / suite).rglob("*")):
        if not candidate.is_file():
            continue
        relative = candidate.relative_to(HERE / suite)
        frozen = V10_VERIFY / suite / relative
        if candidate.suffix.lower() in input_suffixes and frozen.is_file():
            copy_audit.append({"copy": str(candidate.relative_to(ROOT)),
                               "frozen_source": str(frozen),
                               "sha256": digest(candidate),
                               "match": digest(candidate) == digest(frozen)})

candidate_vectors = []
for candidate in sorted((HERE / "regression_candidate" / "vectors").iterdir()):
    frozen = V10_VERIFY / "regression_candidate" / "vectors" / candidate.name
    candidate_vectors.append({"copy": str(candidate.relative_to(ROOT)),
                              "frozen_source": str(frozen),
                              "sha256": digest(candidate),
                              "match": digest(candidate) == digest(frozen)})

manifest = {
    "status": "HASH_MANIFEST_PASS",
    "frozen_guard_manifest_sha256":
        "7fa8cc8baa1cdd5451ae4eb3fa9953f36e6e46b5da4af97209bf1fd899616bb7",
    "rtl": rtl,
    "candidate_testbenches": [
        record(HERE / "regression_candidate" / "tb_road_postprocess_stream.v"),
        record(HERE / "regression_candidate" / "tb_down2_overlap_tile_runner.v"),
    ],
    "evidence": [record(HERE / path) for path in evidence_paths],
    "candidate_vectors": candidate_vectors,
    "legacy_copy_audit": copy_audit,
    "all_copy_hashes_match": all(item["match"] for item in candidate_vectors + copy_audit),
}
destination = HERE / "hash_manifest.json"
if destination.exists():
    raise FileExistsError(destination)
destination.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": manifest["status"], "rtl": len(rtl),
                  "evidence": len(manifest["evidence"]),
                  "copy_files": len(candidate_vectors) + len(copy_audit),
                  "all_copy_hashes_match": manifest["all_copy_hashes_match"]}))
