"""只读取冻结 RTL，展开现有 formatter 的异常链，不修改技能。"""
import hashlib
from pathlib import Path
import traceback

from scripts.python.quality.formatter_config import create_formatter_backend

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / 'dynamic_postprocess_function_20261008/road_dynamic_postprocess.v'


def main():
    engine = create_formatter_backend()
    candidate = ROOT / 'rtl/road_dynamic_postprocess.v'
    source = candidate if candidate.exists() else ORIGINAL
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    try:
        module, parameters, ports, body = engine._parse_module(source.read_text(encoding='utf-8'))
        parsed = engine._parse_body(body)
        print('PARSER_PASS', module, len(ports), list(parsed))
    except Exception as error:
        traceback.print_exception(error)
        raise SystemExit(1)
    finally:
        assert hashlib.sha256(source.read_bytes()).hexdigest() == before


if __name__ == '__main__':
    main()
