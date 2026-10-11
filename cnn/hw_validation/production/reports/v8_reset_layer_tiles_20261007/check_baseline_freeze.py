"""Freeze prior evidence in place; never write inside the previous baseline."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    baseline = root.parent / "v7_low_io_physical_20261006"
    chain = root.parent / "v7_onchip_chain_20261006"
    closure = json.loads((baseline / "frozen_inputs.json").read_text(encoding="utf-8"))["sha256"]
    prior = json.loads((chain / "final_manifest.json").read_text(encoding="utf-8"))["sha256"]
    for name, expected in prior.items():
        path = chain / name
        assert digest(path) == expected, f"Prior chain mismatch: {path}"
        closure[str(path)] = expected
    for name, expected in closure.items():
        assert digest(Path(name)) == expected, f"Frozen source mismatch: {name}"
    paths = set(baseline.rglob("*"))
    paths.update(Path(name) for name in closure)
    paths.add(root.parent.parent / "graph_artifacts" / "graph.json")
    actual = {str(path): {"bytes": path.stat().st_size, "sha256": digest(path)}
              for path in sorted(paths) if path.is_file()}
    manifest = root / "baseline_full_manifest.json"
    if args.freeze:
        assert not manifest.exists(), "Baseline manifest already exists; cannot replace it"
        payload = {"scope": "Complete previous low-IO tree, failed reports/databases, frozen dependency closure and graph; retained in place",
                   "baseline": {"dsp": 26, "slice": 4068, "core_cycles": 436},
                   "files": actual}
        with manifest.open("x", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    else:
        expected = json.loads(manifest.read_text(encoding="utf-8"))["files"]
        assert actual == expected, "Previous baseline added/removed/changed; compare manifest before continuing"
    print(json.dumps({"status": "BASELINE_FREEZE_PASS", "files": len(actual),
                      "bytes": sum(item["bytes"] for item in actual.values()),
                      "manifest_sha256": digest(manifest)}))


if __name__ == "__main__":
    main()
