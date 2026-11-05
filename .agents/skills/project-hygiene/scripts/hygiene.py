"""Standard-library-only storage report and Git-index gate. No deletion mode."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import time

GIB = 1024**3


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args],
                          capture_output=True, check=True).stdout


def linked(path):
    s = path.lstat()
    return stat.S_ISLNK(s.st_mode) or bool(getattr(s, 'st_file_attributes', 0) & 0x400)


def measure(root):
    result = {'path': str(root), 'bytes': 0, 'files': 0, 'errors': [], 'links': []}
    if not root.exists():
        result['missing'] = True
        return result
    stack = [root]
    while stack:
        folder = stack.pop()
        try:
            if linked(folder):
                result['links'].append(str(folder))
                continue
            with os.scandir(folder) as entries:
                for e in entries:
                    try:
                        s = e.stat(follow_symlinks=False)
                        if stat.S_ISLNK(s.st_mode) or getattr(s, 'st_file_attributes', 0) & 0x400:
                            result['links'].append(e.path)
                        elif e.is_dir(follow_symlinks=False):
                            stack.append(Path(e.path))
                        elif e.is_file(follow_symlinks=False):
                            result['bytes'] += s.st_size
                            result['files'] += 1
                    except OSError as exc:
                        result['errors'].append(str(exc))
        except OSError as exc:
            result['errors'].append(str(exc))
    return result


def run_candidates(artifacts, now=None):
    now = time.time() if now is None else now
    records = []
    if not artifacts.exists() or linked(artifacts):
        return records
    for folder in artifacts.iterdir():
        if not folder.is_dir() or linked(folder) or folder.name == 'hygiene':
            continue
        marker = folder / 'run.json'
        record = {'path': str(folder), 'candidate': False, 'reason': 'unowned or invalid marker'}
        records.append(record)
        try:
            if linked(marker):
                continue
            if marker.stat().st_size > 65536:
                continue
            m = json.loads(marker.read_text(encoding='utf-8'))
            if not isinstance(m, dict) or type(m.get('project_hygiene')) is not int or m['project_hygiene'] != 1:
                continue
            if m.get('status') not in ('success', 'failed', 'running') or type(m.get('pinned')) is not bool:
                continue
            if m['pinned'] or m['status'] == 'running':
                record['reason'] = 'pinned or running'
                continue
            finished = dt.datetime.fromisoformat(m['finished_at'])
            if finished.tzinfo is None:
                continue
            record.update(status=m['status'], finished=finished.timestamp(), reason='retained completed run')
        except (OSError, ValueError, KeyError, TypeError):
            continue
    for status, keep in [('success', 2), ('failed', 1)]:
        completed = sorted((r for r in records if r.get('status') == status),
                           key=lambda r: r['finished'], reverse=True)
        for r in completed[keep:]:
            if now-r['finished'] >= 7*86400:
                size = measure(Path(r['path']))
                r['bytes'] = size['bytes']
                if not size['errors'] and not size['links']:
                    r.update(candidate=True, reason='superseded completed run older than seven days; approval required')
                else:
                    r['reason'] = 'scan error or link; retain'
    return records


def staged(repo, max_bytes=50*1024**2):
    names = git(repo, 'diff', '--cached', '--name-only', '-z', '--diff-filter=ACMRT').split(b'\0')
    names = [n.decode('utf-8', errors='surrogateescape') for n in names if n]
    findings = []
    for name in names:
        parts = Path(name).parts
        base = parts[-1].casefold()
        if (parts[0] == 'artifacts' or any(p in ('.venv', 'node_modules', '__pycache__') for p in parts)):
            findings.append({'path': name, 'reason': 'generated output or dependency directory'})
        if (base in ('auth.json', '.env', 'credentials.json') or
                (base.startswith('.env.') and base not in ('.env.example', '.env.template')) or
                Path(base).suffix in ('.pem', '.key', '.pfx', '.p12', '.lic')):
            findings.append({'path': name, 'reason': 'credential or private-license filename; inspect'})
        size = int(git(repo, 'cat-file', '-s', ':'+name))
        if size > max_bytes:
            findings.append({'path': name, 'reason': 'staged blob exceeds 50 MiB review threshold', 'bytes': size})
    return {'passed': not findings, 'staged_files': len(names), 'findings': findings}


def scan(repo, report_dir):
    artifacts = repo / 'artifacts'
    home = Path.home()
    local = Path(os.environ.get('LOCALAPPDATA', str(home/'AppData/Local')))
    roots = [artifacts, home/'.codex', home/'.cache/codex-runtimes',
             local/'OpenAI', home/'AppData/Roaming/Codex', local/'pip/cache',
             local/'npm-cache', home/'AppData/Roaming/Code/CachedExtensionVSIXs']
    for name in ('PIP_CACHE_DIR', 'NPM_CONFIG_CACHE'):
        if os.environ.get(name):
            roots.append(Path(os.environ[name]))
    roots = list(dict.fromkeys(roots))
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir/'latest.json'
    previous = {}
    if report_file.is_file():
        try:
            old = json.loads(report_file.read_text(encoding='utf-8'))
            if old.get('repo') == str(repo):
                previous = {r['path']: r for r in old['directories']}
        except (ValueError, KeyError, TypeError):
            pass
    sizes = [measure(p) for p in roots]
    for r in sizes:
        old = previous.get(r['path'])
        r['delta_bytes'] = (r['bytes']-old['bytes']) if old and not any(
            r.get(k) or old.get(k) for k in ('errors', 'links', 'missing')) else None
    warnings = []
    disks = {}
    for drive in dict.fromkeys([repo.anchor, 'C:\\' if os.name == 'nt' else '/']):
        u = shutil.disk_usage(drive)
        disks[drive] = {'total': u.total, 'free': u.free}
        if u.free < 30*GIB:
            warnings.append(drive+' has less than 30 GiB free')
    if sizes[0]['bytes'] > 30*GIB:
        warnings.append('Project artifacts exceed 30 GiB; review before further large generation')
    try:
        behind, ahead = map(int, git(repo, 'rev-list', '--left-right', '--count', '@{upstream}...HEAD').split())
        sync = {'ahead': ahead, 'behind': behind, 'remote_freshly_checked': False}
    except subprocess.CalledProcessError:
        sync = {'upstream': None, 'remote_freshly_checked': False}
    result = {'repo': str(repo), 'measured_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'branch': git(repo, 'branch', '--show-current').decode().strip(),
              'git_sync': sync,
              'directories': sizes, 'disks': disks, 'warnings': warnings,
              'runs': run_candidates(artifacts), 'files_deleted': 0,
              'note': 'Logical file sizes; hardlinks/compression can affect actual allocation. Unknown or active state is not disposable.'}
    report_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'report': str(report_file), 'warnings': warnings,
            'cleanup_candidates': sum(r['candidate'] for r in result['runs']), 'files_deleted': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['scan', 'staged'])
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--report-dir', type=Path)
    args = parser.parse_args()
    repo = Path(git(args.repo, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    result = staged(repo) if args.mode == 'staged' else scan(repo, args.report_dir or repo/'artifacts/hygiene')
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(1 if result.get('passed') is False else 0)
