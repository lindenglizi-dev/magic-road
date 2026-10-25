"""绑定完整数值参考，仅把小型图案和分类golden复制到综合源目录。"""
import json
import shutil
import run


def main():
    root = run.ROOT
    contract = json.loads((root / 'reference/contract.json').read_text(encoding='utf-8'))
    assert contract['status'] == 'PASS_TEST_ONLY_NOT_DEPLOYMENT_MODEL'
    assert all(run.sha(root / 'vectors' / name) == value for name, value in contract['hashes']['vectors'].items())
    for name in ('rgb_pattern_words.hex', 'combined_golden.hex'):
        shutil.copyfile(root / 'vectors' / name, root / 'rtl' / name)
    frozen = json.loads((root / 'frozen.json').read_text(encoding='utf-8'))
    for path in [root / 'reference/generate.py', root / 'reference/contract.json',
                 *[root / 'vectors' / name for name in contract['hashes']['vectors']]]:
        frozen[str(path)] = run.sha(path)
    run.save(root / 'frozen.json', frozen)
    run.save(root / 'status.json', {'stage': 'FULL_FRONTEND_IMPLEMENTED_REFERENCE_PASS_SIMULATION_PENDING',
        'tensor_bytes': [442368, 589824, 221184], 'stem_tiles': 2304, 'down2_tiles': 576,
        'board_run': False, 'physical_run': False, 'new_bitstream': False, 'formal_acceptance': False})
    run.check()
    print('FULL_REFERENCE_BOUND_SMALL_ROMS_STAGED', flush=True)


if __name__ == '__main__':
    main()
