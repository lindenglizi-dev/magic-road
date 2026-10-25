"""封存第七批收据与R256只读输入；再次执行只核对，不覆盖冻结记录。"""
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
PRODUCTION = HERE.parent
PLAN = PROJECT / 'cnn/hw_validation/plans/resource_budget_20261015'
OLD = PRODUCTION / 'frame_ready_dispatch_20261016'
PACKAGE = PROJECT / 'cnn/reports/qat_frozen_stem_g10_20261014_v1/package'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def check_or_write(path, value):
    if path.exists():
        assert read(path) == value, f'冻结内容发生变化：{path}'
    else:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run():
    frozen = HERE / 'frozen'
    frozen.mkdir(exist_ok=True)
    receipt_path = OLD / 'verification/final_verification_receipt.json'
    receipt = read(receipt_path)
    assert receipt['protocol_scenarios'] == 18 and receipt['joint_counts'] == [7, 0]
    assert receipt['all_bound_inputs_unchanged'] is True
    assert sha(OLD / 'rtl/road_frame_ready_dispatch.v') == receipt['accepted_latest_dispatcher_sha256']
    retained = [receipt_path, OLD / 'verification/acceptance_coverage.json', OLD / 'handoff.txt',
                OLD / 'gates/dispatcher_unique.json', OLD / 'verification/verification_handoff.txt',
                OLD / 'verification/runs/20261016_011729_746_4b7ddac1/summary.json']
    copies = []
    for source in retained:
        target = frozen / source.relative_to(OLD)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copies.append({'source': str(source), 'copy': str(target), 'sha256': sha(source)})
    check_or_write(frozen / 'dispatcher_receipt_closure.json', copies)
    inputs = retained + [
        PLAN / '第八批任务_R256零训练与资源诊断_20261016.txt',
        PLAN / 'r256_candidate_contract_20261016.json',
        PRODUCTION / 'graph_artifacts/graph.json', PRODUCTION / 'graph.py',
        PRODUCTION / 'deployment_contract.json',
        PRODUCTION / 'model_handoff_20261015/artifacts/layer_parameter_index.json',
        PRODUCTION / 'postprocess_golden_2fps_20261015/golden.py',
        PRODUCTION / 'postprocess_golden_2fps_20261015/artifacts/receipt.json',
        PACKAGE / 'manifest.json', PACKAGE / 'numeric_test.bin', PACKAGE / 'numeric_test_padded.bin',
        PROJECT / 'cnn/integer.py', PROJECT / 'cnn/model.py', PROJECT / 'cnn/contract.json',
    ]
    inputs.extend(sorted((OLD / 'rtl').glob('*.v')))
    # 只绑定已批准的既有厂商闭包，不复制第二份权重ROM。
    inputs.extend(path for path in sorted((OLD / 'vendor_rom').rglob('*')) if path.is_file())
    for item in read(OLD / 'frozen_dependencies.json')['files']:
        inputs.append(Path(item['source']))
    records = [{'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}
               for path in sorted(set(inputs))]
    assert sha(PACKAGE / 'numeric_test.bin') == 'b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145'
    binding = {'status': 'FROZEN_READ_ONLY_INPUTS', 'files': records,
               'python_executable': sys.executable, 'python_executable_sha256': sha(Path(sys.executable))}
    check_or_write(HERE / 'input_closure.json', binding)
    print(json.dumps({'status': 'PASS_INPUTS_UNCHANGED', 'files': len(records),
                      'dispatcher_scenarios': 18, 'joint_counts': [7, 0]}))


if __name__ == '__main__':
    run()
