"""Check the archived source bytes and explicit Anlogic project references."""
import csv
import hashlib
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(__file__).resolve().parent


def main():
    seen = set()
    projects = []
    with (BASE/'source_manifest.csv').open(encoding='utf-8') as handle:
        for item in csv.DictReader(handle):
            relative = Path(item['path'])
            if relative.is_absolute() or '..' in relative.parts or item['path'] in seen:
                raise ValueError('Invalid or duplicate manifest path: '+item['path'])
            path = (ROOT/relative).resolve()
            if not path.is_relative_to(BASE):
                raise ValueError('Manifest path outside archive: '+item['path'])
            if path.stat().st_size != int(item['bytes']) or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError('Source integrity mismatch: '+item['path'])
            seen.add(item['path'])
            if path.suffix == '.al':
                projects.append(path)
    for project in projects:
        for value in re.findall(r'<File\s+Path="([^"]+)"',project.read_text(encoding='utf-8-sig')):
            dependency = (project.parent/html.unescape(value).replace('\\','/')).resolve()
            if not dependency.is_relative_to(BASE) or not dependency.is_file():
                raise ValueError('Missing or external project dependency: '+value)
            if dependency.relative_to(ROOT).as_posix() not in seen:
                raise ValueError('Project dependency is not in the manifest: '+value)
    if not seen or len(projects) != 6:
        raise ValueError('Unexpected source/project inventory')
    print(f'PASS: {len(seen)} source files; {len(projects)} TD projects; all explicit dependencies included')


if __name__ == '__main__':
    main()
