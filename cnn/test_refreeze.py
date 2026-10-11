"""Frozen-copy integrity, duplicate refusal and tamper rejection."""
import json
from pathlib import Path
import tempfile

from .archive_oct5 import copy_frozen, sha


def main():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "source"
        source.mkdir()
        (source / "weights").write_bytes(b"original frozen weights")
        (source / "release.json").write_text(json.dumps({
            "files": {"weights": sha(source / "weights")}}), encoding="utf-8")
        receipt = copy_frozen(source, root / "copy")
        assert receipt["files_verified"] == 1
        assert sha(source / "weights") == sha(root / "copy/weights")
        try:
            copy_frozen(source, root / "copy")
        except FileExistsError:
            pass
        else:
            raise AssertionError("duplicate freeze accepted")
        (source / "weights").write_bytes(b"tampered")
        try:
            copy_frozen(source, root / "tampered-copy")
        except ValueError:
            assert not (root / "tampered-copy").exists()
        else:
            raise AssertionError("tampered freeze accepted")
        (source / "release.json").write_text(json.dumps({
            "files": {str(source / "weights"): sha(source / "weights")}}), encoding="utf-8")
        try:
            copy_frozen(source, root / "unsafe-copy")
        except ValueError:
            assert not (root / "unsafe-copy").exists()
        else:
            raise AssertionError("absolute inventory path accepted")
    print("PASS frozen copy integrity/duplicate/tamper")


if __name__ == "__main__":
    main()
