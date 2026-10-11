#!/usr/bin/env python3
"""Verify blind-reserve bytes/hashes without decoding videos or parsing labels."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha512(path: Path) -> str:
    hasher = hashlib.sha512()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify(root: Path, request: dict) -> dict:
    results = []
    for expected in request["files"]:
        path = root / expected["relative_path"]
        present = path.is_file()
        size = path.stat().st_size if present else None
        actual_hash = sha512(path) if present and size == expected["bytes"] else None
        results.append({
            "relative_path": expected["relative_path"],
            "present": present,
            "bytes": size,
            "size_pass": size == expected["bytes"],
            "sha512_pass": actual_hash == expected["sha512"],
        })
    passed = all(row["present"] and row["size_pass"] and row["sha512_pass"] for row in results)
    return {
        "status": "pass_hash_only_no_content_inspection" if passed else "fail",
        "root": str(root.resolve()),
        "file_count": len(results),
        "files": results,
        "content_inspected": False,
        "note": "This receipt verifies only byte count and SHA-512; it preserves the blind-test boundary.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    result = verify(args.root, request)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "pass_hash_only_no_content_inspection":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
