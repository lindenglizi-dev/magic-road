"""复核旧只读绑定并原样封存 CSP 数据；一次写入，不重算网络。"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
PRODUCTION = PROJECT / "cnn/hw_validation/production"
PAYLOAD = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert not (ROOT / "csp_manifest.json").exists(), "CSP bundle already frozen"
    sources = {}
    checks = []
    artifacts = {}
    package = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
    bundles = [(PRODUCTION / "csp2_layer_scheduled_20261015/frozen/vectors", "csp2"),
               (PRODUCTION / "csp_family_layer_scheduled_20261015/frozen_attempt3/reference", "family"),
               (PRODUCTION / "csp2_complete_20261015/reference/road_input", None)]
    copies = []
    for base, target in bundles:
        manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["payload_sha256"] == PAYLOAD
        sources.update(manifest.get("source_sha256", {}))
        for name, expected in manifest.get("package_sha256", {}).items():
            sources[(package / name).relative_to(PROJECT).as_posix()] = expected
        for name, expected in manifest["artifacts"].items():
            original = base / name
            assert sha(original) == expected, str(original)
            sources[original.relative_to(PROJECT).as_posix()] = expected
            if target == "csp2":
                copies.append((original, ROOT / "csp2" / name))
            elif target == "family" and name.startswith(("csp3/", "csp4/")):
                copies.append((original, ROOT / name))
            elif target == "family":
                copies.append((original, ROOT / "family_receipt" / name))
        manifest_name = (base / "manifest.json").relative_to(PROJECT).as_posix()
        sources[manifest_name] = sha(base / "manifest.json")
        if target:
            copies.append((base / "manifest.json", ROOT / "source_receipts" / f"{target}_manifest.json"))
        checks.append({"manifest": manifest_name, "artifacts_checked": len(manifest["artifacts"]),
                       "source_bindings_checked": len(manifest.get("source_sha256", {})),
                       "payload_sha256": manifest["payload_sha256"], "status": "PASS"})
    for relative, expected in sources.items():
        assert sha(PROJECT / relative) == expected, relative
    before = dict(sources)
    for original, destination in copies:
        assert not destination.exists(), str(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, destination)
        assert sha(destination) == sha(original)
        artifacts[destination.relative_to(ROOT).as_posix()] = sha(destination)
    for relative, expected in before.items():
        assert sha(PROJECT / relative) == expected, f"source changed: {relative}"
    sample = copies[0][1].read_bytes()
    mutation = bytes([sample[0] ^ 1]) + sample[1:]
    assert hashlib.sha256(mutation).hexdigest() != sha(copies[0][1])
    report = {"status": "PASS", "old_manifest_checks": checks, "source_before_after_equal": True,
              "source_files_checked": len(sources), "copied_files": len(copies),
              "real_negative": {"mutation": "first artifact first byte xor1", "hash_rejected": True},
              "csp_recomputed": False, "cuda_imported": False, "training": False,
              "boundary": "Frozen CPU sources include down3/down4; these are separate CSP block fixtures, not a continuous RTL backbone."}
    (ROOT / "csp_binding_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("freeze_csp_reference.py", "selector_reference.py", "control_contract.json",
                 "selector_report.json", "csp_binding_report.json"):
        artifacts[name] = sha(ROOT / name)
    manifest = {"schema": 1, "status": "FROZEN_CPU_REFERENCE_NOT_RTL_PREFIX",
                "payload_sha256": PAYLOAD, "source_sha256": sources,
                "artifacts": artifacts, "artifact_count": len(artifacts),
                "immutable_after_generation": True, "eram_mapping": "UNPROVEN"}
    (ROOT / "csp_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(sources)} sources unchanged; {len(copies)} exact copies; {len(artifacts)} frozen artifacts")


if __name__ == "__main__":
    main()
