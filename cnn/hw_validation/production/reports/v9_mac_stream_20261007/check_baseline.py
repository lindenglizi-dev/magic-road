"""Freeze/check the completed reset-and-tile evidence, without touching old files."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    previous = root.parent / "v8_reset_layer_tiles_20261007"
    entries = [{"path": str(path.relative_to(previous)).replace("\\", "/"),
                "bytes": path.stat().st_size, "sha256": digest(path)}
               for path in sorted(previous.rglob("*")) if path.is_file()]
    manifest = root / "previous_stage_manifest.json"
    if args.freeze:
        with manifest.open("x", encoding="utf-8") as stream:
            json.dump({"source": str(previous), "files": entries}, stream, indent=2)
            stream.write("\n")
    else:
        assert entries == json.loads(manifest.read_text(encoding="utf-8"))["files"]
    legacy = json.loads((previous / "baseline_full_manifest.json").read_text(encoding="utf-8"))
    for name, entry in legacy["files"].items():
        path = Path(name)
        assert path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"], path
    print(json.dumps({"status": "BASELINES_UNCHANGED", "previous_stage_files": len(entries),
                      "previous_stage_bytes": sum(item["bytes"] for item in entries),
                      "legacy_files": len(legacy["files"]), "manifest_sha256": digest(manifest)}))


if __name__ == "__main__":
    main()
