"""汇总同周期循环取指与实际物理证据；不生成中间位流。"""
import json
import re
import run


def read(path):
    return json.loads((run.ROOT / path).read_text(encoding='utf-8'))


def main():
    root = run.ROOT
    run.check()
    closure = read('physical/source_hashes.json')
    assert all(run.sha(p) == value for p, value in closure.items())
    constraint = read('constraint_recheck/receipt.json')
    assert constraint['passed'] and constraint['database_sha256'] == run.sha(root / 'physical/pr.db')
    assert constraint['timing'] == run.timing(root / 'physical/all_endpoints.timing')
    functional = read('functional_comparison.json')
    assert functional['passed'] and functional['integrated_cycles_identical']
    payload = run.timing(root / 'physical/bounded_payload.timing')
    assert not payload['violations']
    synchronizers = {n: run.timing(root / 'physical' / f'{n}.timing') for n in ('reg_request_meta', 'reg_ack_meta')}
    assert all(not value['violations'] for value in synchronizers.values())
    area = (root / 'physical/route.area').read_text(encoding='utf-8')
    resources = {n: int(re.search(r'^#' + n + r'\s+(\d+)', area, re.M)[1]) for n in ('slice', 'dsp', 'eram', 'plb', 'pll', 'IO')}
    coverage = float(re.search(r'STA coverage\s*:\s*([\d.]+)', (root / 'physical/final_timing.rpt').read_text(encoding='utf-8'))[1])
    direct = read('sequence_verification/receipts/manifest.json')
    child = root / 'rtl/road_frontend_load_sequence.v'
    assert str(child) in direct['compile_command']
    integrated = read('integrated_simulation/receipt.json')
    assert integrated['source_hashes'][str(child)] == run.sha(child)
    run.save(root / 'direct_manifest_supplement.json', {'direct_manifest_sha256': run.sha(root / 'sequence_verification/receipts/manifest.json'),
        'omitted_from_old_hash_dictionary_only': str(child), 'sha256': run.sha(child),
        'actual_compile_command_contains_child': True, 'independent_integrated_hash_matches': True,
        'explanation': '原编译命令已包含loader；脚本哈希字典现已补齐，旧成功收据保留并通过本补充绑定。'})
    summary = {'stage': 'CONTROL_LOOP_IMPLEMENTATION_PASS', 'formal_acceptance': False,
        'board_baseline': read('board_baseline.json'), 'functional': functional, 'reference': read('loop_reference.json'),
        'resources_including_ddr_hdmi_shell': resources, 'all_endpoints': constraint['timing'],
        'sta_coverage_percent': coverage, 'constraint_check': constraint, 'display_payload': payload,
        'display_synchronizers': synchronizers, 'source_hashes': closure,
        'strict_gate_pass': False, 'strict_gate_directory': 'gate_attempt2',
        'new_bitstream': False, 'board_run_this_candidate': False,
        'next': '../frontend_ddr_full_20261015: complete RGB/Stem/PW DDR tensor traversal',
        'limits': ['TEST_ONLY four-tile parameters', 'external IO timing not signed off', 'thin margins',
                   'ROM logical size reduction is not ERAM reduction', 'complete CNN and FPS not established']}
    run.save(root / 'comparison.json', summary)
    run.save(root / 'status.json', {'stage': summary['stage'], 'comparison': str(root / 'comparison.json'),
                                  'strict_gate_pass': False, 'new_bitstream': False, 'full_tensor_next': summary['next']})
    run.check()
    print(json.dumps({'resources': resources, 'coverage': coverage, 'worst': {k: v['slack_ns'] for k, v in constraint['timing']['worst'].items()}}), flush=True)


if __name__ == '__main__':
    main()
