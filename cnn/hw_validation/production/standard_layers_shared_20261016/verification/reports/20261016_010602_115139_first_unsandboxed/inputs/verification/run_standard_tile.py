"""独立冻结四标准层代表tile与行为WIF1端点，保留每个失败尝试。"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT.parent
PROJECT = PACKAGE.parents[3]
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
MODEL = Path('D:/modeltech64_2020.4/win64')
VENDOR = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p')
REUSED = PACKAGE.parent / 'feature_blocks_shared_20261015/frozen_attempt2/reused'
TABLE = REUSED.parent / 'reference/csp3/parameters/silu.hex'
CORES = ('road_csp_first_probe','road_mac_probe','road_dynamic_postprocess','road_dynamic_requant','road_round_shift','silu_shared_unit')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label',default='local')
    parser.add_argument('--only',type=int)
    parser.add_argument('--mode',type=int,default=0)
    parser.add_argument('--negative',action='store_true')
    parser.add_argument('--random',type=int,default=1)
    parser.add_argument('--gates',action='store_true')
    parser.add_argument('--timeout',type=int,default=180)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_]+',args.label):
        raise ValueError('safe attempt label required')
    report = ROOT / 'reports' / (datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'_'+args.label)
    report.mkdir(parents=True)
    snapshot = report / 'inputs'
    snapshot.mkdir()
    reference = PACKAGE / 'reference'
    original = {}
    def include(source, destination):
        original[str(source)] = sha(source)
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,destination)
    manifest = read(reference / 'artifact_manifest.json')
    for relative,digest in manifest.items():
        if sha(reference / relative) != digest:
            raise ValueError('reference manifest mismatch: '+relative)
        include(reference / relative,snapshot / 'reference' / relative)
    include(reference / 'artifact_manifest.json',snapshot / 'reference/artifact_manifest.json')
    for path,digest in read(reference / 'input_binding.json')['source_sha256'].items():
        if sha(Path(path)) != digest:
            raise ValueError('original reference input changed: '+path)
        original[path] = digest
    for name in ('requirements.json','codegen_plan.txt','ports.json'):
        include(PACKAGE / name,snapshot / name)
    for path in (PACKAGE / 'rtl').glob('*.v'):
        include(path,snapshot / 'rtl' / path.name)
    for name in CORES:
        include(REUSED / (name+'.v'),snapshot / 'reused' / (name+'.v'))
    for name in ('ph1p_logic_eram.v','ph1p_phy_gsr.v'):
        include(VENDOR / name,snapshot / 'vendor' / name)
    include(TABLE,snapshot / 'silu.hex')
    for name in ('tb_standard_tile_client.v','run_standard_tile.py'):
        include(ROOT / name,snapshot / 'verification' / name)
    tools = {name:dict(path=str(MODEL / (name+'.exe')),sha256=sha(MODEL / (name+'.exe'))) for name in ('vlib','vlog','vsim')}
    descriptor = read(snapshot / 'reference/tasks.json')
    param_count = len(read(snapshot / 'reference/parameter_responses.json'))
    base_by_layer = {12:56975360,13:57196544,26:57708544,27:57819136}
    cases = []
    for layer in descriptor['layers']:
        for case in layer['cases']:
            case_root = snapshot / 'reference' / case['directory']
            transactions = list(csv.DictReader((case_root / 'wif1_transactions.csv').open(encoding='utf-8')))
            byte_rows = [r for r in transactions if r['channel']=='byte']
            weight_rows = [r for r in transactions if r['channel']=='weight']
            for rows,name,width,shift in ((byte_rows,'byte_trace29.hex',8,16),(weight_rows,'weight_trace390.hex',192,384)):
                packed=[]
                for row in rows:
                    address=int(row['address_or_group']); write=int(row['write'])
                    request=int(row['request_hex'],16); response=int(row['response_hex'],16)
                    word=(((write << (12 if width==8 else 5))|address)<<shift)|(request<<width)|response
                    packed.append(f'{word:0{(shift+(13 if width==8 else 6)+3)//4}x}\n')
                (case_root / name).write_text(''.join(packed),encoding='ascii')
            task_rows=read(case_root / 'tasks.json')
            (case_root / 'task_quant248.hex').write_text(''.join(f'{r["quant248"]:062x}\n' for r in task_rows),encoding='ascii')
            h,w,c=layer['input_shape_hwc']
            outputs=sum(int(r['mask']).bit_count() for r in task_rows)
            cfg=[layer['layer_id'],case['tile_y'],case['tile_x'],h,w,c,base_by_layer[layer['layer_id']],case['groups'],case['tasks'],outputs,param_count,len(byte_rows),len(weight_rows),h*w*c,0,0]
            (case_root / 'cfg.hex').write_text(''.join(f'{n:08x}\n' for n in cfg),encoding='ascii')
            cases.append(dict(layer=layer,case=case,root=case_root,cfg=cfg))
    closure={p.relative_to(snapshot).as_posix():sha(p) for p in snapshot.rglob('*') if p.is_file()}
    receipt=dict(status='STARTED',original_sha256=original,snapshot_sha256=closure,tools=tools,
                 python=dict(path=sys.executable,sha256=sha(Path(sys.executable))),commands=[],tests=[],
                 boundaries=['Behavioral WIF1 only; arrays are testbench endpoint state, not physical4ERAM',
                             'Actual sole arithmetic owner and five frozen arithmetic source files',
                             'Representative tiles from CPU tensors; no actual preceding hardware producer',
                             'No full ROM7168 rerun, synthesis, DDR, board, whole network, accuracy or FPS claim'])
    def persist(): save(report / 'summary.json',receipt)
    def command(name,argv,cwd=snapshot,timeout=None):
        temporary = report / 'runtime_tmp'
        temporary.mkdir(exist_ok=True)
        try:
            result=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',
                                  timeout=timeout or args.timeout,env=dict(os.environ,PYTHONPATH=str(SKILL),TEMP=str(temporary),TMP=str(temporary)))
            native_code=result.returncode
            content=result.stdout+result.stderr
        except (OSError, subprocess.TimeoutExpired) as error:
            native_code=-998
            content=repr(error)
        log=report / (name+'.log'); log.write_text(content,encoding='utf-8')
        effective=native_code or int(bool(re.search(r'\*\* (?:Error|Fatal):',content)))
        receipt['commands'].append(dict(name=name,argv=list(map(str,argv)),cwd=str(cwd),returncode=native_code,
                                        effective_returncode=effective,log_sha256=sha(log)))
        persist(); return effective,content
    persist()
    for name,arguments in dict(dependencies=['scripts.python.toolchain.manage_skill_dependencies','check','--settings','config/defaults.json'],
                               renderer=['scripts.python.toolchain.wavedrom_runtime','--settings','config/defaults.json','check'],
                               readiness=['scripts.python.toolchain.preflight_verilog_toolchain','--settings','config/defaults.json','--readiness','execute']).items():
        command(name,[sys.executable,'-B','-m',*arguments],SKILL,60)
    if args.gates:
        command('strict_gate',[sys.executable,'-B','-m','scripts.python.validation.generated_deliverable_gate',snapshot,'--include-testbench',
                              '--json',report / 'gate.json','--markdown',report / 'gate.md'],SKILL,300)
    code,_=command('vlib',[MODEL / 'vlib.exe','work'])
    if code: raise RuntimeError('vlib failed: '+str(report))
    sources=[*sorted((snapshot / 'vendor').glob('*.v')),*[snapshot / 'reused' / (n+'.v') for n in CORES],snapshot / 'rtl/road_standard_tile_client.v',snapshot / 'verification/tb_standard_tile_client.v']
    code,content=command('compile',[MODEL / 'vlog.exe','-work','work',*sources])
    if code:
        receipt['status']='COMPILE_FAILED';persist();print(report);return 1
    chosen=cases if args.only is None else [cases[args.only]]
    for number,item in enumerate(chosen):
        trace=report / f'trace_{number}.csv'
        layer_root=snapshot / 'reference' / item['layer']['name']
        argv=[MODEL / 'vsim.exe','-c','-lib','work','PH1P_PHY_GSR','tb_standard_tile_client',
              '+VECTOR_ROOT='+(snapshot / 'reference').as_posix(),'+LAYER_ROOT='+layer_root.as_posix(),
              '+CASE_ROOT='+item['root'].as_posix(),'+TABLE='+(snapshot / 'silu.hex').as_posix(),'+TRACE='+trace.as_posix(),
              f'+MODE={args.mode}',f'+NEGATIVE={int(args.negative)}',f'+RANDOM={args.random}',
              '-do','onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0']
        code,content=command('simulation_'+str(number),argv)
        marker='STANDARD_TILE_PROTOCOL_PASS' if args.mode else 'STANDARD_TILE_PASS'
        passed=(bool(code) and 'ACC_MISMATCH task=0 negative=1' in content and marker not in content) if args.negative else code==0 and content.count(marker)==1
        receipt['tests'].append(dict(layer=item['layer']['layer_id'],case=item['case']['case'],mode=args.mode,negative=args.negative,
                                     status='PASS_REAL_CHECKER_NEGATIVE' if passed and args.negative else 'PASS' if passed else 'FAILED',
                                     metrics=[line for line in content.splitlines() if 'STANDARD_TILE_' in line],trace_sha256=sha(trace) if trace.exists() else None))
        persist();print(item['layer']['layer_id'],item['case']['case'],receipt['tests'][-1]['status'],flush=True)
        if not passed: break
    receipt['snapshot_unchanged']=all(sha(snapshot / p)==d for p,d in closure.items())
    receipt['original_unchanged']=all(sha(Path(p))==d for p,d in original.items())
    receipt['status']='PASS' if receipt['snapshot_unchanged'] and receipt['original_unchanged'] and all(t['status'].startswith('PASS') for t in receipt['tests']) else 'FAILED_PRESERVED'
    persist();print(report);return 0 if receipt['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
