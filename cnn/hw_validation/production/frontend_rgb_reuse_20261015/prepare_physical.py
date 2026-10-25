"""Stage the actual S1 top and unchanged constraints; do not invoke TD."""
import shutil
import xml.etree.ElementTree as ET
import run


def main():
    run.check()
    root, base = run.ROOT, run.BASE / 'physical'
    work = root / 'implementation'
    assert not work.exists()
    work.mkdir()
    for name in ('official', 'ddr2'):
        shutil.copytree(base / name, work / name)
    for name in ('board.adc', 'board.sdc'):
        shutil.copyfile(base / name, work / name)
    shutil.copyfile(root / 'build/build.tcl', work / 'build.tcl')
    for name in ('loop_table.hex', 'loop_parameters.hex', 'rgb_pattern_words.hex', 'combined_golden.hex'):
        shutil.copyfile(root / 'vectors' / name, work / name)
    tree = ET.fromstring((base / 'road_stem_ddr_board_top.al').read_text(encoding='utf-8').replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    sources = tree.find('Source_Files')
    sources.clear()
    verilog = ET.SubElement(sources, 'Verilog')
    ips = ET.SubElement(sources, 'IP_FILE')
    paths = [*sorted((root / 'reused').glob('*.v')), *sorted((root / 'rtl').glob('*.v')),
        run.PROJECT / 'cnn/hw_validation/production/reports/board_selftest_20261010/rtl/road_selftest_display.v',
        *sorted((work / 'official').glob('*.v')), work / 'official/PLL/PLL.xml', work / 'ddr2/ddr2.xml']
    assert all(path.is_file() for path in paths)
    for index, path in enumerate(paths):
        node = ET.SubElement(ips if path.suffix == '.xml' else verilog, 'File', {'Path': path.as_posix()})
        info = ET.SubElement(node, 'FileInfo')
        for key, value in [('UsedInSyn', 'true'), ('UsedInP&R', 'true'), ('BelongTo', 'design_1'), ('CompileOrder', str(index + 1))]:
            ET.SubElement(info, 'Attr', {'Name': key, 'Val': value})
    (work / 'road_stem_ddr_board_top.al').write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R'), encoding='utf-8')
    closure = [*paths, *[p for folder in ('rtl', 'build') for p in (root / folder).rglob('*') if p.is_file()],
               *[p for p in work.rglob('*') if p.is_file()]]
    run.save(work / 'source_hashes.json', {str(path): run.sha(path) for path in closure})
    run.save(root / 'physical_preparation.json', {'prepared': True, 'td_started': False,
        'top': 'road_stem_ddr_board_top', 'work_directory': str(work),
        'command_when_coordinator_schedules': 'D:/Python313/python.exe -B -X utf8 run.py physical',
        'scope': 'Actual S1 sequence + frozen 8 cores + mailbox + DDR/HDMI diagnostic shell',
        'constraints': 'Original board.sdc and DDR IP SDC; original display_cdc.tcl bounds resolved after placement',
        'unchanged_vs_baseline': ['device PH1P35MDG324 speed3', 'CNN100MHz', 'PAXI', 'reset', 'timing exception rules']})
    run.check()
    print('S1_PHYSICAL_CLOSURE_PREPARED_NOT_RUN', flush=True)


if __name__ == '__main__':
    main()
