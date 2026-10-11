"""Narrow actual simulator/TD checks; never writes earlier evidence."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from prepare import HERE, V19, sha, check

IVERILOG = Path('E:/project/qiansai/.tools/iverilog/bin/iverilog.exe')
VVP = IVERILOG.with_name('vvp.exe')
TD = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe')

def execute(args, cwd, log, text=None):
    with (cwd / log).open('w', encoding='utf-8') as stream:
        process = subprocess.run([str(x) for x in args], cwd=cwd, stdout=stream,
                                 stderr=subprocess.STDOUT, input=text, text=True)
    assert process.returncode == 0, (args, process.returncode, log)

def simulate(which):
    directory = HERE / which
    core = [directory / 'rtl' / name for name in ('road_dynamic_postprocess.v',
            'road_dynamic_requant.v', 'road_round_shift.v', 'silu_shared_unit.v',
            'ph1p_logic_eram_runtime_model.v')]
    for top, tb, extra in [('tb_road_dynamic_postprocess', directory / 'tb_road_dynamic_postprocess.v', []),
                           ('tb_low_io', HERE / 'tb_low_io.v', [HERE / 'road_dynamic_low_io_top.v'])]:
        execute([IVERILOG, '-g2001', '-Wall', '-I', directory, '-s', top,
                 '-o', directory / (top + '.vvp'), tb, *extra, *core], directory, top + '_compile.log')
        execute([VVP, directory / (top + '.vvp')], directory, top + '.log')
        log = (directory / (top + '.log')).read_text(encoding='utf-8')
        assert 'PASS' in log and 'FATAL' not in log, log
        print(which, log.strip())
    assert (directory / 'results.csv').read_bytes() == (HERE.parent / 'fixed_graph_function_20261008/results.csv').read_bytes()
    check()

def physical(which):
    directory = HERE / which / 'physical'
    shutil.copy2(HERE / 'road_dynamic_low_io_top.v', directory / 'road_dynamic_low_io_top.v')
    # TD's .al dialect contains literal UsedInP&R, not well-formed XML.
    source = (V19 / 'physical/road_postprocess_low_io_top.al').read_text(encoding='utf-8')
    root = ET.fromstring(source.replace('UsedInP&R', 'UsedInP&amp;R'))
    root.set('Path', directory.as_posix())
    root.find('Name').text = 'road_dynamic_low_io_top'
    verilog = root.find('Source_Files/Verilog'); verilog.clear()
    names = ['road_dynamic_low_io_top.v'] + ['../rtl/' + name for name in
            ('road_dynamic_postprocess.v', 'road_dynamic_requant.v', 'road_round_shift.v', 'silu_shared_unit.v')]
    for index, name in enumerate(names, 1):
        info = ET.SubElement(ET.SubElement(verilog, 'File', Path=name), 'FileInfo')
        for key, value in [('UsedInSyn', 'true'), ('UsedInP&R', 'true'), ('BelongTo', 'design_1'), ('CompileOrder', str(index))]:
            ET.SubElement(info, 'Attr', Name=key, Val=value)
    root.find('TOP_MODULE/LABEL').text = 'road_dynamic_low_io_top'
    root.find('TOP_MODULE/MODULE').text = 'road_dynamic_low_io_top'
    project = ET.tostring(root, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R')
    (directory / 'road_dynamic_low_io_top.al').write_text(project, encoding='utf-8')
    script = (V19 / 'physical/build.tcl').read_text(encoding='utf-8').replace('road_postprocess_low_io_top', 'road_dynamic_low_io_top')
    (directory / 'build.tcl').write_text(script, encoding='utf-8')
    manifest = {p.relative_to(HERE / which).as_posix(): sha(p) for p in
                [directory / 'road_dynamic_low_io_top.v', directory / 'shell.sdc', directory / 'shell.adc'] +
                [HERE / which / 'rtl' / name for name in ('road_dynamic_postprocess.v', 'road_dynamic_requant.v', 'road_round_shift.v', 'silu_shared_unit.v')]}
    (directory / 'input_hashes.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    execute([TD], directory, 'td_actual.log', 'source build.tcl\nexit\n')
    assert (directory / 'pr.db').exists(), 'No routed database'
    assert (directory / 'coverage_100000_all_paths.timing').exists(), 'No coverage'
    check()

if __name__ == '__main__':
    check()
    (physical if '--physical' in sys.argv else simulate)(sys.argv[1])
