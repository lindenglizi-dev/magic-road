from pathlib import Path
import hashlib
import html
import json
import re
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root):
    release = json.loads((root / 'docs/基准位流.json').read_text(encoding='utf-8-sig'))
    bit = root / release['bit_file']
    if bit.stat().st_size != release['size'] or sha(bit) != release['sha256']:
        raise ValueError('位流校验失败')
    for line in (root / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        expected, name = line.split('  ', 1)
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or sha(root / relative) != expected:
            raise ValueError('文件校验失败：' + name)
    project = root / 'td_project/ball_face.al'
    for entry in re.findall(r'<File\s+Path="([^"]+)"', project.read_text(encoding='utf-8-sig')):
        path = html.unescape(entry)
        if path and not (project.parent / path).is_file():
            raise ValueError('工程引用缺失：' + path)
    if release['database_included']:
        if sha(root / 'implementation/checked.db') != release['checked_db_sha256']:
            raise ValueError('数据库校验失败')
    print('通过：逐文件完整性、工程引用、位流及所附数据库检查')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    verify(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
