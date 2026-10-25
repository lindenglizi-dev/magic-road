"""冻结BANKS通过版本；仅复制必要源码和向量，不覆盖旧候选。"""
import json
import shutil
import run


def main():
    root, base = run.ROOT, run.BASE
    assert not (root / 'frozen.json').exists()
    frozen = json.loads((base / 'frozen.json').read_text(encoding='utf-8'))
    frozen.update(json.loads((base / 'physical/source_hashes.json').read_text(encoding='utf-8')))
    for folder in ('rtl', 'reused', 'vectors', 'tests', 'build'):
        (root / folder).mkdir(exist_ok=True)
        for path in (base / folder).iterdir():
            if path.is_file() and path.suffix in ('.v', '.vh', '.hex', '.tcl'):
                frozen[str(path)] = run.sha(path)
                if path.name not in ('tb_program_banks.v', 'tb_netlist_rom.v'):
                    shutil.copyfile(path, root / folder / path.name)
    for name in ('comparison.json', 'status.json', 'reference.json', 'requirements.txt', 'run.py',
                 'diagnostic_bitgen/receipt.json', 'physical/pr.db',
                 'diagnostic_bitgen/HX1P35A_C7_STEM_DDR_DOWN2_BANKS.bit'):
        frozen[str(base / name)] = run.sha(base / name)
    assert all(run.sha(p) == h for p, h in frozen.items())
    run.save(root / 'frozen.json', frozen)
    for name in ('reference.json', 'shared_core_interface.v', 'new_interfaces.v'):
        shutil.copyfile(base / name, root / name)
    (root / 'sequence_verification').mkdir()
    shutil.copyfile(base / 'sequence_verification/run_verify.py', root / 'sequence_verification/run_verify.py')
    (root / 'mailbox_verification').mkdir()
    shutil.copyfile(base / 'mailbox_verification/road_paxi_mailbox_spec.json', root / 'mailbox_verification/road_paxi_mailbox_spec.json')
    run.save(root / 'reused_sources.json', {str(p): run.sha(p) for p in (root / 'reused').glob('*.v')})
    receipt = json.loads((base / 'diagnostic_bitgen/receipt.json').read_text(encoding='utf-8'))
    run.save(root / 'board_baseline.json', {'status': 'FOUR_TILE_BOARD_SELFTEST_PASS_USER_REPORTED',
        'reported_on': '2026-10-15', 'source': 'User in this chat: 三次复位恢复绿色、保持10分钟稳定正常',
        'reset_recoveries': 3, 'stable_minutes': 10, 'bitstream': receipt,
        'scope': 'Four-tile TEST_ONLY diagnostic; observations supplied by user, no agent board access'})
    run.check()
    print('BANKS_FROZEN_AND_USER_BOARD_RESULT_RECORDED', flush=True)


if __name__ == '__main__':
    main()
