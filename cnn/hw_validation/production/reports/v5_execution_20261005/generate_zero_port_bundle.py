"""通过原规范与受治理渲染入口生成零端口文档，保留所有暂存证据。"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
sys.path[:0] = [str(ROOT / 'checker_overlay'), str(SKILL)]
from scripts.python.workflow import spec_document as document
from scripts.python.workflow.config import load_settings


def main():
    assert not (HERE / 'zero_port_bundle').exists(), 'Do not overwrite a prior bundle'
    retained_stages = []
    cleanup = document._cleanup_stage
    # 按用户禁止批量删除的要求，保留该次生成器自己的暂存文件；不改变验证或渲染。
    document._cleanup_stage = lambda path: retained_stages.append(str(path))
    try:
        report = document.write_spec_bundle(
            HERE / 'zero_port_spec.json', HERE / 'zero_port_bundle',
            source_paths=[HERE / 'tb_zero_port_parentheses.v'],
            runtime_settings=load_settings(SKILL / 'config/defaults.json'))
    finally:
        document._cleanup_stage = cleanup
    report['retained_stages'] = retained_stages
    report['temporary_retention_only'] = True
    report['rtl_quality_release'] = False
    (HERE / 'zero_port_bundle_result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    assert report['ok']
    for module in report['modules']:
        assert Path(module['spec']).is_file()
        for waveform in module['waveforms']:
            assert Path(waveform['svg']).read_text(encoding='utf-8').lstrip().startswith('<')
    print(json.dumps({'canonical_bundle_generated': True, 'modules': len(report['modules']),
                      'retained_stages': retained_stages}, ensure_ascii=False))


if __name__ == '__main__':
    main()
