#!/usr/bin/env python3
"""Lesson15 reproducible gate. No source modifications; SKIP means not tested."""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys
BASE=pathlib.Path(__file__).resolve().parents[1]
PROJECT=BASE/'lesson14_transformer_full'
REPORTS=BASE/'reports'; REPORTS.mkdir(exist_ok=True)
CASES=('demo','edge_5x7','random_00','sat_1x1')

def run_case(name,argv,cwd,expected=None):
    print(f'\n== {name} ==')
    try:
        proc=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        data=proc.stdout or ''
        (REPORTS/(name.replace('/','_')+'.log')).write_text(data,encoding='utf-8')
        tail='\n'.join(data.splitlines()[-8:]); print(tail or '(empty output)')
        ok=proc.returncode==0 and (expected is None or expected in data)
        return {'status':'PASS' if ok else 'FAIL','returncode':proc.returncode,'command':argv,'log':name.replace('/','_')+'.log'}
    except (OSError,subprocess.TimeoutExpired) as e:
        return {'status':'FAIL','error':str(e),'command':argv}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model-only',action='store_true',help='skip RTL; result is NOT a hardware pass')
    ap.add_argument('--strict',action='store_true',help='fail exit code if RTL is not available')
    args=ap.parse_args()
    files=sorted(p for p in (PROJECT/'rtl').glob('*.sv'))
    manifest={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (REPORTS/'rtl_sha256.json').write_text(json.dumps(manifest,indent=2))
    result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'sources':str(PROJECT.name),'tool_iverilog':shutil.which('iverilog'),
            'tool_vvp':shutil.which('vvp'),'tool_yosys':shutil.which('yosys'),
            'checks':{}}
    result['checks']['reference']=run_case('reference',[sys.executable,str(PROJECT/'reference/verify_full_block.py')],PROJECT,'PASS Python end-to-end')
    result['checks']['contracts']=run_case('contracts',[sys.executable,str(PROJECT/'reference/static_contracts.py')],PROJECT,'PASS source-level')
    result['checks']['check_contracts']=run_case('check_contracts',[sys.executable,str(PROJECT/'reference/check_contracts.py')],PROJECT,None)
    rtl_sources=[str(p) for p in files]
    if args.model_only:
        result['checks']['rtl']='SKIP (explicit --model-only)'
    elif not shutil.which('iverilog') or not shutil.which('vvp'):
        result['checks']['rtl']='SKIP (no iverilog/vvp available)'
        print('\nRTL SKIPPED: install Icarus or use ModelSim; Python is not RTL verification.')
    else:
        executable=REPORTS/'tb_mac.out'
        result['checks']['mac_compile']=run_case('mac_compile',['iverilog','-g2012','-s','tb_mac_smoke','-o',str(executable),str(PROJECT/'rtl/mac_array_4x4.sv'),str(BASE/'validation/tb_mac_smoke.sv')],PROJECT)
        if result['checks']['mac_compile']['status']=='PASS':
            result['checks']['mac_rtl']=run_case('mac_rtl',['vvp',str(executable)],PROJECT,'PASS MAC_SMOKE')
        executable=REPORTS/'tb_transformer.out'
        compile_cmd=['iverilog','-g2012','-s','tb_transformer_block','-o',str(executable)] + rtl_sources + [str(PROJECT/'tb/tb_transformer_block.sv')]
        result['checks']['top_compile']=run_case('top_compile',compile_cmd,PROJECT)
        if result['checks']['top_compile']['status']=='PASS':
            for case in CASES:
                result['checks'][f'rtl_{case}']=run_case(f'rtl_{case}',['vvp',str(executable),f'+CASE=vectors/{case}'],PROJECT,f'PASS TRANSFORMER BLOCK case=vectors/{case}')
    statuses=[c.get('status') for c in result['checks'].values() if isinstance(c,dict)]
    result['gate']='FAIL' if 'FAIL' in statuses else ('RTL_UNVERIFIED' if not any(k.startswith('rtl_demo') for k in result['checks']) else 'RTL_PASS')
    (REPORTS/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print('\nFINAL GATE:',result['gate'],'(see reports/summary.json)')
    return 1 if result['gate']=='FAIL' or (args.strict and result['gate']!='RTL_PASS') else 0
if __name__=='__main__':raise SystemExit(main())
