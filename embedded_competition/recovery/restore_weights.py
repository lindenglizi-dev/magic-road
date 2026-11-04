"""Verify checkpoints without loading pickle; optionally restore original relative paths."""
import argparse
import csv
import hashlib
from pathlib import Path
import shutil

BASE=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore-to',type=Path,help='Restore under this directory; conflicting files are never overwritten')
    args=parser.parse_args()
    rows=list(csv.DictReader((BASE/'weights_manifest.csv').open(encoding='utf-8')))
    target=args.restore_to.resolve() if args.restore_to else None
    seen=set()
    for row in rows:
        original=Path(row['original_path']);relative=Path(row['object_path'])
        if original.is_absolute() or relative.is_absolute() or '..' in original.parts or '..' in relative.parts:
            raise ValueError('Invalid manifest path')
        obj=(BASE/relative).resolve()
        if not obj.is_relative_to(BASE) or original.as_posix() in seen:
            raise ValueError('Escaping or duplicate manifest path')
        seen.add(original.as_posix())
        if obj.stat().st_size!=int(row['bytes']) or sha(obj)!=row['sha256']:
            raise ValueError('Checkpoint checksum mismatch: '+row['original_path'])
        if target:
            dest=(target/original).resolve()
            if not dest.is_relative_to(target):raise ValueError('Restore path escapes destination')
            if dest.exists() and (not dest.is_file() or sha(dest)!=row['sha256']):
                raise ValueError('Conflicting destination: '+str(dest))
    if target:
        for row in rows:
            dest=target/row['original_path']
            if not dest.exists():
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(BASE/row['object_path'],dest)
                if sha(dest)!=row['sha256']:raise ValueError('Restored file checksum mismatch')
    print(f'PASS: {len(rows)} checkpoint paths verified'+('; restored' if target else '; no files restored'))


if __name__=='__main__':main()
