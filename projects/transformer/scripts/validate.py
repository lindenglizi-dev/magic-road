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
        vectors=REPORTS/'gemm_unit_vectors'
        result['checks']['gemm_vectors']=run_case('gemm_vectors',[sys.executable,str(BASE/'validation/gen_gemm_unit_vectors.py'),'--out-dir',str(vectors)],PROJECT,'PASS GEMM_VECTORS')
        if result['checks']['gemm_vectors']['status']=='PASS':
            executable=REPORTS/'tb_tiled_gemm.out'
            result['checks']['gemm_compile']=run_case('gemm_compile',['iverilog','-g2012','-s','tb_tiled_gemm','-o',str(executable),str(PROJECT/'rtl/mac_array_4x4.sv'),str(PROJECT/'rtl/tiled_gemm_4x4_banked_compact.sv'),str(BASE/'validation/tb_tiled_gemm.sv')],PROJECT)
            if result['checks']['gemm_compile']['status']=='PASS':
                result['checks']['gemm_rtl']=run_case('gemm_rtl',['vvp',str(executable),f'+VECTORS={vectors}'],PROJECT,'PASS GEMM_UNIT')
        result['checks']['softmax_vectors']=run_case('softmax_vectors',[sys.executable,str(BASE/'validation/gen_softmax_vectors.py')],PROJECT,'PASS SOFTMAX_VECTORS')
        if result['checks']['softmax_vectors']['status']=='PASS':
            executable=REPORTS/'tb_softmax_row.out'
            result['checks']['softmax_compile']=run_case('softmax_compile',['iverilog','-g2012','-s','tb_softmax_row','-o',str(executable),str(PROJECT/'rtl/softmax_row_int32.sv'),str(BASE/'validation/tb_softmax_row.sv')],PROJECT)
            if result['checks']['softmax_compile']['status']=='PASS':
                result['checks']['softmax_rtl']=run_case('softmax_rtl',['vvp',str(executable),f'+VECTORS={REPORTS/"softmax_unit_vectors/cases.txt"}'],PROJECT,'PASS SOFTMAX_ROW')
        result['checks']['requant_vectors']=run_case('requant_vectors',[sys.executable,str(BASE/'validation/gen_requant_vectors.py')],PROJECT,'PASS REQUANT_VECTORS')
        if result['checks']['requant_vectors']['status']=='PASS':
            executable=REPORTS/'tb_requant.out'
            result['checks']['requant_compile']=run_case('requant_compile',['iverilog','-g2012','-s','tb_requant','-o',str(executable),str(PROJECT/'rtl/requant_shift_sat.sv'),str(PROJECT/'rtl/ffn_relu_requant.sv'),str(BASE/'validation/tb_requant.sv')],PROJECT)
            if result['checks']['requant_compile']['status']=='PASS':
                result['checks']['requant_rtl']=run_case('requant_rtl',['vvp',str(executable),f'+VECTORS={REPORTS/"requant_unit_vectors/cases.txt"}'],PROJECT,'PASS REQUANT_UNIT')
        executable=REPORTS/'tb_probability_writer.out'
        result['checks']['probability_compile']=run_case('probability_compile',['iverilog','-g2012','-s','tb_probability_writer','-o',str(executable),str(PROJECT/'rtl/probability_writer.sv'),str(BASE/'validation/tb_probability_writer.sv')],PROJECT)
        if result['checks']['probability_compile']['status']=='PASS':
            result['checks']['probability_rtl']=run_case('probability_rtl',['vvp',str(executable)],PROJECT,'PASS PROBABILITY_WRITER')
        executable=REPORTS/'tb_transformer.out'
        compile_cmd=['iverilog','-g2012','-s','tb_transformer_block','-o',str(executable)] + rtl_sources + [str(PROJECT/'tb/tb_transformer_block.sv')]
        result['checks']['top_compile']=run_case('top_compile',compile_cmd,PROJECT)
        if result['checks']['top_compile']['status']=='PASS':
            for case in CASES:
                result['checks'][f'rtl_{case}']=run_case(f'rtl_{case}',['vvp',str(executable),f'+CASE=vectors/{case}'],PROJECT,f'PASS TRANSFORMER BLOCK case=vectors/{case}')
    statuses=[c.get('status') for c in result['checks'].values() if isinstance(c,dict)]
    required=('mac_rtl','gemm_rtl','softmax_rtl','requant_rtl','probability_rtl') + tuple(f'rtl_{case}' for case in CASES)
    rtl_pass=all(result['checks'].get(name,{}).get('status')=='PASS' for name in required)
    result['gate']='FAIL' if 'FAIL' in statuses else ('RTL_PASS' if rtl_pass else 'RTL_UNVERIFIED')
    (REPORTS/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print('\nFINAL GATE:',result['gate'],'(see reports/summary.json)')
    return 1 if result['gate']=='FAIL' or (args.strict and result['gate']!='RTL_PASS') else 0
if __name__=='__main__':raise SystemExit(main())
