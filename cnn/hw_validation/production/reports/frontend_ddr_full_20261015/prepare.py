"""复制完整层所需核、板壳、参数，保留两代已验证基线。"""
import json
import shutil
import run


def main():
    root, base = run.ROOT, run.BASE
    assert not (root / 'frozen.json').exists()
    frozen = json.loads((base / 'frozen.json').read_text(encoding='utf-8'))
    for folder in ('reused', 'build'):
        (root / folder).mkdir(exist_ok=True)
        for path in (base / folder).iterdir():
            if path.is_file() and path.suffix in ('.v', '.tcl'):
                frozen[str(path)] = run.sha(path)
                shutil.copyfile(path, root / folder / path.name)
    (root / 'rtl').mkdir(exist_ok=True)
    (root / 'tests').mkdir(exist_ok=True)
    for name in ('road_paxi_mailbox.v', 'road_stem_ddr_board_top.v', 'road_frontend_load_sequence.v'):
        path = base / 'rtl' / name
        frozen[str(path)] = run.sha(path)
        target = name.replace('load_sequence', 'layer_sequence')
        shutil.copyfile(path, root / 'rtl' / target)
    for name in ('loop_table.hex', 'loop_parameters.hex'):
        for folder in ('rtl', 'vectors'):
            (root / folder).mkdir(exist_ok=True)
            shutil.copyfile(base / 'vectors' / name, root / folder / name)
        frozen[str(base / 'vectors' / name)] = run.sha(base / 'vectors' / name)
    for name in ('shared_core_interface.v', 'new_interfaces.v'):
        shutil.copyfile(base / name, root / name)
    run.save(root / 'frozen.json', frozen)
    run.save(root / 'reused_sources.json', {str(p): run.sha(p) for p in (root / 'reused').glob('*.v')})
    run.check()
    print('FULL_FRONTEND_BASE_PREPARED', flush=True)


if __name__ == '__main__':
    main()
