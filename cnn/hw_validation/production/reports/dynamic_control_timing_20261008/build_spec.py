"""Publish exact narrow-shell contract with the installed WaveDrom runtime."""
import json
import os
import subprocess
import sys
from prepare import HERE, OLD

def main():
    contract=json.loads((OLD/'road_dynamic_postprocess.contract.json').read_text(encoding='utf-8'))
    module=contract['modules'][0]
    module['name']='road_dynamic_low_io_top'; module['feature']='dynamic_low_io'
    module['rtl_path']='road_dynamic_low_io_top.v'
    module['description']='38-bit runtime-loaded diagnostic shell for frozen dynamic serial postprocessing.'
    ports=[('i_clk',1,'input'),('i_rstn',1,'input'),('i_rx_valid',1,'input'),('i_rx_data',16,'input'),
           ('o_rx_ready',1,'output'),('o_tx_valid',1,'output'),('o_tx_data',16,'output'),('i_tx_ready',1,'input')]
    module['interfaces']['ports']=[dict(name=n,width=w,direction=d,role=n,description=n,clock_domain='i_clk') for n,w,d in ports]
    assert sum(w for _,w,_ in ports)==38
    module['interfaces']['streams']=[dict(id='rx',valid='i_rx_valid',ready='o_rx_ready',payload=['i_rx_data']),
                                      dict(id='tx',valid='o_tx_valid',ready='i_tx_ready',payload=['o_tx_data'])]
    # Legacy contract key is handshakes rather than streams in some versions.
    for key in ('handshakes','ready_valid'):
        if key in module['interfaces']:
            module['interfaces'][key]=module['interfaces']['streams']
    module['reset']['values']='Immediate assertion cancels all work, two rising edges release, reload table addresses 0..1023 before compute.'
    module['behavior']=[
        'A000 followed by 1024 signed16 words loads the table sequentially.',
        'B000 followed by 19 least-significant-first 16-bit words loads one 304-bit packet; only then submit.',
        'Packet bits: accumulator95:0 pre191:96 shifts209:192 post241:210 shift247:242 activate248 mask251:249 tags299:252 fault300 padding303:301.',
        'Each result transmits tag, signed16 data and flags (bit1 INT16, bit0 fault) in three accepted words; all hold under stall.',
        'C000 transmits input count, output count, table/fault flags. D000 transmits counted SUBMIT/WAIT clocks low/high and flags.',
        'Cycle counter excludes packet/table preload and TX clocks: diagnostic window, not full core latency or FPS.',
        'No new MAC, DDR, board protocol or timing exception.']
    module['constraints']=['100MHz PH1P35MDG324 -3 diagnostic only, automatic pins and zero I/O delays.',
                           'Parameters are runtime data, not constant coefficients. Existing round, SiLU and fault semantics retained.',
                           'Strict failures and external/removal timing failures remain unclosed.']
    module['corner_cases']=['Partial packet/table reset, running reset, random TX stall, counter wrap after 65535 batches.']
    module['verification_cases']=['330 batches/604 outputs, partial load and running reset, payload hold, counts.']
    module['timing_diagrams']=[dict(id='narrow_transfer',title='Partial packet cannot submit',scenario='packet',
        description='Compressed illustrative timeline; variable compute and stall durations, not cycle-exact core latency.',
        wavejson={'signal':[{'name':'i_clk','wave':'p.........'},
          {'name':'i_rx_valid','wave':'01..0.....'}, {'name':'o_rx_ready','wave':'1...0....1'},
          {'name':'phase','wave':'23..4..5.2','data':['idle','19 words','submit/compute','tag/data/status','idle']},
          {'name':'o_tx_valid','wave':'0......1.0'}, {'name':'i_tx_ready','wave':'0.......10'}]})]
    (HERE/'shell.contract.json').write_text(json.dumps(contract,indent=2),encoding='utf-8')
    env={**os.environ,'PYTHONPATH':'C:/Users/lenovo/.codex/skills/readable-verilog-generator'}
    with (HERE/'spec.log').open('w',encoding='utf-8') as stream:
        code=subprocess.run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
            '--spec',str(HERE/'shell.contract.json'),'--out-dir',str(HERE),
            '--source',str(HERE/'road_dynamic_low_io_top.v'),'--language','zh'],cwd=HERE,env=env,
            stdout=stream,stderr=subprocess.STDOUT).returncode
    assert code==0,code
    print('SPEC_PASS ports=8 bits=38')
    candidate=json.loads((OLD/'road_dynamic_postprocess.contract.json').read_text(encoding='utf-8'))
    candidate['modules'][0]['behavior'].append('Capture pre operands and tag in the existing SELECT edge; prepare post operands in the existing accepted SiLU-return edge. No added state, edge, II or external port change.')
    candidate['modules'][0]['verification_cases'].append('Compare all 330 individual batch cycle windows and 604 output triples to frozen serial baseline.')
    path=HERE/'candidate/chain.contract.json'
    path.write_text(json.dumps(candidate,indent=2),encoding='utf-8')
    with (HERE/'candidate/spec.log').open('w',encoding='utf-8') as stream:
        code=subprocess.run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
            '--spec',str(path),'--out-dir',str(HERE/'candidate'),
            '--source',str(HERE/'candidate/rtl/road_dynamic_postprocess.v'),'--language','zh'],
            cwd=HERE,env=env,stdout=stream,stderr=subprocess.STDOUT).returncode
    assert code==0,code
    print('CANDIDATE_SPEC_PASS ports=24')

if __name__=='__main__': main()
