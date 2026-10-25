"""Exercise actual mapped ROM primitives, not a second behavioral ROM."""
import shutil
import re
from pathlib import Path
import run


def main():
    run.check()
    work = run.fresh('netlist_rom')
    vendor = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release')
    netlist = run.ROOT / 'physical/gate_netlist.v'
    text = netlist.read_text(encoding='utf-8')
    # ponytail: retain the actual sequence cone, not unrelated DDR/PLL simulation;
    # full netlist/SDF simulation belongs to a separate controller verification.
    starts = list(re.finditer(r'^  (?:AL_MAP_\w+|PH1P_\w+|buf)\b', text, re.M))
    assert starts
    blocks = []
    for start in starts:
        end = text.index(');', start.start()) + 2
        block = text[start.start():end]
        names = re.findall(r'(\\u_sequence/[^\s]+)\s+\(', block)
        if names and '/u_core/' not in names[0]:
            blocks.append(block)
    assert len(blocks) > 100
    cone = work / 'mapped_sequence.v'
    cone.write_text(text[:starts[0].start()] + '\n'.join(blocks) + '\nendmodule\n', encoding='utf-8')
    sources = [*sorted((vendor / 'common').glob('*.v')), *sorted((vendor / 'ph1p').glob('*.v')), cone,
               run.ROOT / 'tests/tb_netlist_rom.v']
    shutil.copyfile(run.ROOT / 'vectors/program.hex', work / 'program.hex')
    run.command([run.MSIM / 'vlib.exe', 'work'], work, 'vlib')
    run.command([run.MSIM / 'vlog.exe', '-work', 'work', *sources], work, 'vlog')
    output = run.command([run.MSIM / 'vsim.exe', '-c', '-voptargs=+acc', '-lib', 'work', 'glbl', 'PH1P_PHY_GSR', 'tb_netlist_rom',
        '-do', 'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'], work, 'vsim', allowed=(0, 1, 2))
    assert 'MAPPED_ROM_PASS words=8192 hold_checks=16384' in output, work / 'vsim.log'
    run.save(work / 'receipt.json', {'passed': True, 'words': 8192, 'hold_checks': 16384,
        'source_hashes': {str(p): run.sha(p) for p in sources},
        'original_netlist_sha256': run.sha(netlist), 'retained_sequence_instances': len(blocks),
        'scope': 'Unmodified sequence instances extracted from actual gate netlist plus vendor primitives; forced PC/fetch clock/enable only, no DDR model or SDF'})
    run.check()


if __name__ == '__main__':
    main()
