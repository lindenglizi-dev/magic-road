
from pathlib import Path
from bisect import bisect_right
import hashlib
import json
import re
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
ART = OUT.parent
ROOT=Path(__file__).resolve().parents[2]
RUN = ROOT / 'build/route'
read = lambda p: Path(p).read_text(encoding='utf-8-sig')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
norm = lambda s: re.sub(r'\s+', '', s).replace('\\', '')


def one(items):
    assert len(items) == 1, items
    return items[0]


def main():
    log = read(OUT / 'checked_clock_audit.log')
    assert 'CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED' in log
    text = re.sub(r'//[^\n]*', '', read(OUT / 'actual_checked.v'))
    line_offsets = [m.start() for m in re.finditer('\n', text)]
    cells = {}
    for m in re.finditer(r'\b(PH1P_PHY_\w+)\s*(?:#\((.*?)\)\s*)?(\\?\S+)\s+\((.*?)\);', text, re.S):
        typ, attrs, name, ports = m.groups()
        cells[name.lstrip('\\')] = dict(type=typ, line=bisect_right(line_offsets, m.start())+1,
            ports={k:norm(v) for k,v in re.findall(r'\.(\w+)\(\s*([^)]*?)\s*\)', ports)})
    feedback = {}
    for label in ('main', 'ethernet', 'ddr_user'):
        block = log.split('BEGIN_CHECKED_PLL_FEEDBACK '+label, 1)[1].split('END_CHECKED_PLL_FEEDBACK '+label, 1)[0]
        row = re.search(r'PLL_FEEDBACK_CONNECTION label=\S+ clock=(\S+) sink=(\S+) bufg=(\S+) net=(\S+)', block)
        assert row, label
        clock, sink, bufg, net = row.groups()
        pll = cells[sink.removesuffix('.fbclk')]
        assert pll['type'].startswith('PH1P_PHY_PLL') and pll['ports']['fbclk'] == net
        sclk_name, sclk = one([(n,c) for n,c in cells.items() if c['type'].startswith('PH1P_PHY_SCLK') and c['ports'].get('clkout') == net])
        gclk = cells[bufg]
        assert gclk['type'] == 'PH1P_PHY_GCLK' and gclk['ports']['clkout'] == sclk['ports']['clkin']
        assert pll['ports']['clkc'].strip('{}').split(',')[-1] in gclk['ports']['clkin'].strip('{}').split(',')
        for actual in (net, sclk['ports']['clkin']):
            net_block = block.split('RUN-1001 : Net: '+actual+'\n', 1)[1]
            net_block = net_block.split('RUN-1002 : start command', 1)[0]
            assert re.search(r'Route Type\s*\|\s*global', net_block), actual
        tree = ET.parse(OUT / f'checked_clock_{label}_tree.rpt').getroot()
        assert any(p.get('name') == sclk_name+'.clkin' and p.get('route') == 'global' for p in tree.iter('pin')), sclk_name
        feedback[label] = dict(clock=clock, sink=sink, net=net, pll=pll, sclk_name=sclk_name, sclk=sclk, gclk_name=bufg, gclk=gclk,
                               native_route_type='global', own_pll_output_feedback_verified=True)
    tree = ET.parse(OUT / 'checked_clock_main_tree.rpt').getroot()
    local = [p for p in tree.iter('pin') if p.get('route') == 'local']
                                                                                      
    pad_name, pad = one([(n,c) for n,c in cells.items() if c['ports'].get('opad') == 'O_cam_24m'])
    input_pad_name, input_pad = one([(n,c) for n,c in cells.items() if c['ports'].get('ipad') == 'I_sys_clk'])
    camera = one([p for p in local if p.get('inst') == pad_name and any(q.get('name') == 'O_cam_24m' for q in p.iter('pin'))])
    input_leaf = one([p for p in local if p.get('inst') == input_pad_name and p.get('name') == input_pad_name+'.ipad'])
    assert len(local) == 2 and {p.get('name') for p in local} == {camera.get('name'), input_leaf.get('name')}
    parent = {child:node for node in tree.iter() for child in node}
    ancestors = []
    current = camera
    while current in parent:
        current = parent[current]
        ancestors.append(current)
    camera_sclk = one([p for p in ancestors if p.tag == 'pin' and p.get('name','').endswith('.clkout')
                      and cells.get(p.get('inst'),{}).get('type','').startswith('PH1P_PHY_SCLK')])
    evidence = [OUT/'checked_clock_audit.log', OUT/'actual_checked.v', OUT/'actual_checked.sdc', OUT/'actual_checked.adc',
                OUT/'checked_clock_summary.timing', OUT/'checked_clock_checks.rpt', OUT/'checked_clock_groups.rpt',
                OUT/'checked_clock_utilization.rpt', RUN/'checked.db', ART/'route_auto_native.log', ART/'qualification_native.log']
    evidence += [OUT/f'checked_clock_{s}_tree.rpt' for s in feedback]
    diagnostics = {}
    for p in (ART/'route_auto_native.log', ART/'qualification_native.log', OUT/'checked_clock_audit.log'):
        s = read(p)
        assert not re.search(r'(?m)^USR-6135\b', s), p
        diagnostics[str(p)] = [line for line in s.splitlines() if re.match(r'(?:PHY-5079|PHY-5088|USR-\d+).*',line)]
    summary = read(OUT/'checked_clock_summary.timing')
    timing = {k:float(re.search(k+r':\s*(-?[0-9.]+)ns',summary)[1]) for k in ('SWNS','STNS','HWNS','HTNS')}
    assert min(timing.values()) >= 0
    out = dict(status='EXTRACTED_REQUIRES_REVIEW', feedback_branches=feedback,
               local_tree_pins=[p.attrib for p in local], camera_pad_name=pad_name, camera_pad=pad,
               system_input_pad_name=input_pad_name, system_input_pad=input_pad,
               camera_sclk_ancestor=camera_sclk.attrib,
               camera_pad_latency=[p.attrib for p in camera.iter('latency')], native_diagnostics=diagnostics,
               global_timing_ns=timing, evidence_sha256={str(p):sha(p) for p in evidence})
    (OUT/'clock_graph_evidence.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('EXTRACTED_CURRENT_CLOCK_GRAPH_REQUIRES_REVIEW')


if __name__ == '__main__':
    main()
