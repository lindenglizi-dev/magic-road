"""Independent once-only Stem/DDR/down2 diagnostic; preserve old closures."""
import argparse
import ast
import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[4]
PREVIOUS=ROOT.parent/'ddr_extended_board_20261013'
SOURCE=ROOT.parent/'weight_address_stem_write_20261013'
CORE=ROOT.parent/'board_selftest_20261010/core'
MSIM=Path('D:/modeltech64_2020.4/win64')
SKILL=Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def save(path,value):
    path=Path(path)
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def fresh(name):
    folder=ROOT/name
    index=1
    while folder.exists():
        index+=1
        folder=ROOT/f'{name}_attempt{index}'
    folder.mkdir()
    return folder


def command(args,work,name,allowed=(0,)):
    work.resolve().relative_to(ROOT)
    began=time.monotonic()
    log=work/f'{name}.log'
    assert not log.exists()
    with log.open('w',encoding='utf-8') as stream:
        result=subprocess.run(list(map(str,args)),cwd=work,stdout=stream,stderr=subprocess.STDOUT,timeout=1800)
    save(work/f'{name}.command.json',{'argv':list(map(str,args)),'cwd':str(work),
         'returncode':result.returncode,'seconds':time.monotonic()-began})
    assert result.returncode in allowed,log
    return log.read_text(encoding='utf-8',errors='replace')


def check():
    frozen=json.loads((ROOT/'frozen.json').read_text(encoding='utf-8'))
    changed=[p for p,h in frozen.items() if sha(p)!=h]
    save(ROOT/'frozen_check.json',{'checked':len(frozen),'changed':changed})
    assert not changed,changed
    reused=json.loads((ROOT/'reused_sources.json').read_text(encoding='utf-8'))
    assert all(sha(p)==h for p,h in reused.items())


def setup():
    assert not (ROOT/'frozen.json').exists()
    frozen=json.loads((PREVIOUS/'artifact_hashes.json').read_text(encoding='utf-8'))
    frozen.update(json.loads((PREVIOUS/'frozen.json').read_text(encoding='utf-8')))
    paths=[*CORE.glob('*.v'),*(SOURCE/'rtl').glob('*.v'),PROJECT/'cnn/integer.py',
           PROJECT/'cnn/hw_validation/production/graph_artifacts/graph.json']
    frozen.update({str(p):sha(p) for p in paths})
    save(ROOT/'frozen.json',frozen)
    reused={}
    (ROOT/'reused').mkdir(exist_ok=True)
    names=('road_stem_tile_scheduler.v','road_down2_tile_scheduler.v','road_frontend_shared_core.v')
    for p in [*(SOURCE/'rtl'/name for name in names),*(CORE/name for name in
              ('road_mac_probe.v','road_dynamic_postprocess.v','road_dynamic_requant.v','road_round_shift.v','silu_shared_unit.v'))]:
        target=ROOT/'reused'/p.name
        shutil.copyfile(p,target)
        reused[str(target)]=sha(target)
    save(ROOT/'reused_sources.json',reused)
    for name in ('rtl','tests','build'):
        (ROOT/name).mkdir(exist_ok=True)
    check()
    sys.path.insert(0,str(SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    result=check_dependencies(json.loads((SKILL/'config/defaults.json').read_text(encoding='utf-8')),state_path=ROOT/'dependency_state.json')
    save(ROOT/'dependency_preflight.json',result)
    assert result['required_ok']


def reference():
    check()
    spec=importlib.util.spec_from_file_location('once_reference',ROOT/'reference.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.generate()
    for path in (ROOT/'vectors').glob('*.hex'):
        shutil.copyfile(path,ROOT/'rtl'/path.name)
    shutil.copyfile(ROOT/'vectors/once_constants.vh',ROOT/'rtl/once_constants.vh')
    check()


def gate():
    check()
    work=fresh('gate')
    entry=f'import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())'
    sources={str(p):sha(p) for folder in ('rtl','reused','tests') for p in (ROOT/folder).glob('*.v')}
    save(work/'source_hashes.json',sources)
    for name in ('rtl','tests'):
        external=[]
        for path in (ROOT/'shared_core_interface.v',ROOT/'new_interfaces.v',PROJECT/'user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v',
                     ROOT.parent/'board_selftest_20261010/rtl/road_selftest_display.v'):
            external += ['--external-interface-source',path]
        command([sys.executable,'-B','-X','utf8','-c',entry,ROOT/name,*external,
                 *(['--include-testbench'] if name=='tests' else []),
                 '--json',work/f'{name}.json','--markdown',work/f'{name}.md'],work,name,allowed=(0,1,2))
        assert (work/f'{name}.json').exists()
    assert all(sha(p)==h for p,h in sources.items())
    check()


def integrated():
    check()
    work=fresh('integrated_simulation')
    for path in (ROOT/'vectors').glob('*.hex'):
        shutil.copyfile(path,work/path.name)
    vendor=Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p')
    paths=[vendor/'ph1p_logic_eram.v',vendor/'ph1p_phy_gsr.v',*sorted((ROOT/'reused').glob('*.v')),
           ROOT/'rtl/road_stem_ddr_sequence.v',ROOT/'rtl/road_paxi_mailbox.v',ROOT/'tests/tb_stem_ddr_mailbox.v']
    hashes={str(p):sha(p) for p in paths}
    command([MSIM/'vlib.exe','work'],work,'vlib')
    command([MSIM/'vlog.exe','-work','work','+incdir+'+str(ROOT/'rtl'),*paths],work,'vlog')
    results=[]
    for mode in (0,1):
        output=command([MSIM/'vsim.exe','-c','-lib','work','PH1P_PHY_GSR','tb_stem_ddr_mailbox',
                        f'+MODE={mode}','+VECTORS='+str(ROOT/'vectors'),'-do',
                        'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],work,f'mode_{mode}',allowed=(0,1,2))
        assert f'STEM_DDR_MAILBOX_PASS mode={mode} ' in output,work
        results.append({'mode':mode,'passed':True,'lines':[s for s in output.splitlines() if 'INTEGRATED_BIN' in s or 'STEM_DDR_MAILBOX_PASS' in s]})
        save(work/'receipt.json',{'results':results,'source_hashes':hashes,'scope':'Actual frozen arithmetic and CDC, controlled PAXI memory endpoint'})
        print('\n'.join(results[-1]['lines']),flush=True)
    assert all(sha(p)==h for p,h in hashes.items())
    check()


def physical():
    check()
    work=fresh('physical')
    # Large text timing reports compress transparently without changing bytes.
    command(['compact.exe','/C','/I',work],work,'compress_directory')
    prior=PREVIOUS/'physical_attempt2'
    for name in ('official','ddr2'):
        shutil.copytree(prior/name,work/name)
    for name in ('board.adc','board.sdc'):
        shutil.copyfile(prior/name,work/name)
    tree=ET.fromstring((prior/'road_ddr_selftest_top.al').read_text(encoding='utf-8').replace('UsedInP&R','UsedInP&amp;R'))
    tree.set('Path',work.as_posix())
    tree.find('Name').text='road_stem_ddr_board_top'
    for node in ('LABEL','MODULE'):
        tree.find(f'TOP_MODULE/{node}').text='road_stem_ddr_board_top'
    sources=tree.find('Source_Files')
    sources.clear()
    verilog=ET.SubElement(sources,'Verilog')
    ips=ET.SubElement(sources,'IP_FILE')
    paths=[*sorted((ROOT/'reused').glob('*.v')),*sorted((ROOT/'rtl').glob('*.v')),
           ROOT.parent/'board_selftest_20261010/rtl/road_selftest_display.v',
           *sorted((work/'official').glob('*.v')),work/'official/PLL/PLL.xml',work/'ddr2/ddr2.xml']
    for order,path in enumerate(paths):
        node=ET.SubElement(ips if path.suffix=='.xml' else verilog,'File',{'Path':path.as_posix()})
        info=ET.SubElement(node,'FileInfo')
        for key,value in [('UsedInSyn','true'),('UsedInP&R','true'),('BelongTo','design_1'),('CompileOrder',str(order+1))]:
            ET.SubElement(info,'Attr',{'Name':key,'Val':value})
    (work/'road_stem_ddr_board_top.al').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(tree,encoding='unicode').replace('UsedInP&amp;R','UsedInP&R'),encoding='utf-8')
    for path in (ROOT/'vectors').iterdir():
        if path.is_file():
            shutil.copyfile(path,work/path.name)
    shutil.copyfile(ROOT/'build/build.tcl',work/'build.tcl')
    closure=[*paths,*[p for folder in ('rtl','build','vectors') for p in (ROOT/folder).rglob('*') if p.is_file()]]
    closure += [p for folder in ('ddr2','official') for p in (work/folder).rglob('*') if p.is_file()]
    save(work/'source_hashes.json',{str(p):sha(p) for p in closure})
    output=command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe','build.tcl'],work,'td',allowed=(0,1,2))
    assert 'ONCE_PHYSICAL_COMPLETE' in output,work/'td.log'
    assert all(sha(p)==h for p,h in json.loads((work/'source_hashes.json').read_text(encoding='utf-8')).items())
    check()


def timing(path):
    spec=importlib.util.spec_from_file_location('frozen_cdc_parser',ROOT.parent/'ddr_display_cdc_20261013/run_cdc.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.timing(path)


def recover_reports():
    check()
    original=ROOT/'physical_attempt2'
    assert 'ONCE_PHYSICAL_COMPLETE' in (original/'td.log').read_text(encoding='utf-8')
    work=fresh('physical_reports')
    command(['compact.exe','/C','/I',work],work,'compress_directory')
    name='road_stem_ddr_board_top.al'
    # TD rewrites .al at close; disk-full also truncated that metadata file.
    tree=ET.fromstring((PREVIOUS/'physical_attempt2/road_ddr_selftest_top.al').read_text(encoding='utf-8').replace('UsedInP&R','UsedInP&amp;R'))
    tree.set('Path',work.as_posix())
    tree.find('Name').text='road_stem_ddr_board_top'
    for node in ('LABEL','MODULE'):
        tree.find(f'TOP_MODULE/{node}').text='road_stem_ddr_board_top'
    sources=tree.find('Source_Files')
    sources.clear()
    verilog=ET.SubElement(sources,'Verilog')
    ips=ET.SubElement(sources,'IP_FILE')
    paths=[*sorted((ROOT/'reused').glob('*.v')),*sorted((ROOT/'rtl').glob('*.v')),
           ROOT.parent/'board_selftest_20261010/rtl/road_selftest_display.v',
           *sorted((original/'official').glob('*.v')),original/'official/PLL/PLL.xml',original/'ddr2/ddr2.xml']
    for order,path in enumerate(paths):
        node=ET.SubElement(ips if path.suffix=='.xml' else verilog,'File',{'Path':path.as_posix()})
        info=ET.SubElement(node,'FileInfo')
        for key,value in [('UsedInSyn','true'),('UsedInP&R','true'),('BelongTo','design_1'),('CompileOrder',str(order+1))]:
            ET.SubElement(info,'Attr',{'Name':key,'Val':value})
    (work/name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(tree,encoding='unicode').replace('UsedInP&amp;R','UsedInP&R'),encoding='utf-8')
    shutil.copyfile(original/'pr.db',work/'pr.db')
    shutil.copyfile(original/'source_hashes.json',work/'source_hashes.json')
    script=(ROOT/'build/build.tcl').read_text(encoding='utf-8')
    tail=script[script.index('write_verilog routed_netlist.v'):].replace('export_db pr.db','')
    # Keep one exhaustive report. Other views sample worst paths; duplicating
    # the exhaustive body is redundant and previously exhausted the disk.
    lines=[]
    for line in tail.splitlines():
        if ' -file include_ignored.timing' in line:
            line=line.replace('-ep_num 100000','-ep_num 64')
        if ' -file internal_reg_to_reg.timing' in line or ' -file arithmetic_all.timing' in line:
            line=line.replace('-ep_num 100000','-ep_num 256')
        lines.append(line)
    tail='\n'.join(lines)+'\n'
    head='import_device ph1_35p.db -package PH1P35MDG324 -speed 3\nopen_project road_stem_ddr_board_top.al -single_run\nimport_db pr.db\nupdate_timing -mode final\nsource ../build/display_cdc.tcl\n'
    (work/'report.tcl').write_text(head+tail,encoding='utf-8')
    output=command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe','report.tcl'],work,'td',allowed=(0,1,2))
    assert 'ONCE_PHYSICAL_COMPLETE' in output
    assert sha(work/'pr.db')==sha(original/'pr.db')
    save(work/'recovery_receipt.json',{'original_physical':str(original),'same_database_sha256':sha(work/'pr.db'),
         'source':'Final actual P&R; reports re-exported after disk-full truncation; no RTL/constraint changes'})
    check()


def collect():
    check()
    # Three report exports describe the same routed DB, not three designs.
    work=ROOT/'physical_reports_attempt3'
    cdc_work=ROOT/'physical_reports_attempt2'
    check_work=ROOT/'constraint_recheck'
    database_sha=sha(work/'pr.db')
    assert sha(cdc_work/'pr.db')==database_sha
    for directory in (work,cdc_work):
        receipt=json.loads((directory/'recovery_receipt.json').read_text(encoding='utf-8'))
        assert receipt['same_database_sha256']==database_sha
    assert 'ONCE_PHYSICAL_COMPLETE' in (work/'td.log').read_text(encoding='utf-8')
    all_paths=timing(work/'all_endpoints.timing')
    assert set(all_paths['worst'])=={'setup','hold','recovery','removal'}
    payload=timing(cdc_work/'bounded_payload.timing')
    rows=list(csv.DictReader((cdc_work/'display_cdc_mapping.tsv').open(encoding='utf-8'),delimiter='\t'))
    unique={(r['source_q'],r['destination_d']) for r in rows if r['kind']=='payload'}
    assert payload['records']=={'setup':len(unique)}
    sync={name:timing(cdc_work/f'{name}.timing') for name in ('reg_request_meta','reg_ack_meta')}
    assert all(v['records']=={'setup':1,'hold':1} for v in sync.values())
    area=(work/'route.area').read_text(encoding='utf-8')
    resources={name:int(re.search(r'^#'+name+r'\s+(\d+)',area,re.M)[1]) for name in ('slice','eram','dsp','pll','IO')}
    with (work/'all_endpoints.timing').open(encoding='utf-8') as stream:
        header=''.join(next(stream) for _ in range(35))
    coverage=float(re.search(r'STA coverage\s*:\s*([\d.]+)%',header)[1])
    check_receipt=json.loads((check_work/'receipt.json').read_text(encoding='utf-8'))
    assert check_receipt['passed'] and check_receipt['database_sha256']==sha(work/'pr.db')
    assert all(sha(p)==h for p,h in check_receipt['constraints'].items())
    checks=(check_work/'check_timing.rpt').read_text(encoding='utf-8')
    assert 'checking invalid constraint(0)' in checks and 'checking combinational loops(0)' in checks
    sources=json.loads((work/'source_hashes.json').read_text(encoding='utf-8'))
    assert all(sha(p)==h for p,h in sources.items())
    rom=json.loads((work/'program_audit.json').read_text(encoding='utf-8'))
    assert rom['passed'] and rom['netlist_sha256']==sha(work/'routed_netlist.v') and rom['expected_sha256']==sha(ROOT/'vectors/program.hex')
    direct=json.loads((ROOT/'sequence_verification/receipts/manifest.json').read_text(encoding='utf-8'))
    assert direct['result']=='PASS_13_OF_13' and direct['tb_sha256'].lower()==sha(ROOT/'tests/tb_stem_ddr_sequence.v')
    assert direct['dut_sha256'].lower()==sha(ROOT/'rtl/road_stem_ddr_sequence.v')
    assert direct['program_sha256'].lower()==sha(ROOT/'vectors/program.hex')
    integrated=max((p for p in ROOT.glob('integrated_simulation*') if (p/'receipt.json').exists()),key=lambda p:p.stat().st_mtime)
    combined=json.loads((integrated/'receipt.json').read_text(encoding='utf-8'))
    assert len(combined['results'])==2 and all(v['passed'] for v in combined['results'])
    assert all(sha(p)==h for p,h in combined['source_hashes'].items())
    gate=max((p for p in ROOT.glob('gate*') if (p/'tests.json').exists()),key=lambda p:p.stat().st_mtime)
    hashes=json.loads((gate/'source_hashes.json').read_text(encoding='utf-8'))
    assert all(sha(p)==h for p,h in hashes.items())
    strict={}
    for name in ('rtl','tests'):
        result=json.loads((gate/f'{name}.json').read_text(encoding='utf-8'))
        strict[name]={k:result[k] for k in ('errors','strict_warnings','checks','delivery_ready')}
    clean=not all_paths['violations'] and not payload['violations'] and all(not v['violations'] for v in sync.values())
    assert resources['slice']<=21216 and resources['eram']<=108 and resources['dsp']<=40
    summary={'physical_directory':str(work),'cdc_report_directory':str(cdc_work),'all_endpoints':all_paths,'display_payload':payload,
             'display_synchronizers':sync,'resources_including_entire_diagnostic':resources,
             'sta_coverage_percent':coverage,'program_initialization':rom,'source_hashes':sources,
             'constraint_check_directory':str(check_work),'constraint_check':check_receipt,
             'strict':strict,'gate_directory':str(gate),'direct_regression':direct,'integrated':combined,
             'bitstream':'NOT_GENERATED','board_status':'NOT_RUN','whole_system_signoff':False}
    save(ROOT/'comparison.json',summary)
    save(ROOT/'status.json',{'status':'ONCE_FUNCTIONAL_TIMING_PASS' if clean else 'PHYSICAL_TIMING_FAILED',
         'physical_directory':str(work),'strict_delivery_ready':False,'parameters':'FROZEN_TEST_ONLY',
         'production_modified':False,'core_modified':False,'board_status':'NOT_RUN','bitstream':'NOT_GENERATED'})
    print(json.dumps({'worst':{k:v['slack_ns'] for k,v in all_paths['worst'].items()},
                      'violations':len(all_paths['violations']),'resources':resources,'coverage':coverage}),flush=True)
    check()


def check_constraints():
    check()
    original=ROOT/'physical_attempt2'
    report=ROOT/'physical_reports_attempt3'
    work=fresh('constraint_recheck')
    shutil.copyfile(report/'road_stem_ddr_board_top.al',work/'road_stem_ddr_board_top.al')
    shutil.copyfile(original/'pr.db',work/'pr.db')
    constraints=[original/'board.sdc',original/'ddr2/src/sdc/ddr2.sdc',original/'resolved_display.sdc']
    script='''import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_stem_ddr_board_top.al -single_run
import_db pr.db
'''
    script+=f'read_sdc {{{constraints[0].as_posix()}}}\nread_sdc -ip ddr2 {{{constraints[1].as_posix()}}}\nread_sdc {{{constraints[2].as_posix()}}}\n'
    script+='''update_timing -mode final
report_timing_status -file route.ts
report_timing_summary -ep_num 100 -path_num 1 -file verification.timing
check_timing -verbose -file check_timing.rpt
report_timing_exception -ep_num 1000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 1000 -path_num 1 -file ignored.rpt
report_clock_summary -clocks [get_clocks -include_generated_clocks *] -expand_buckets -debug -file clocks.rpt
puts "ONCE_CONSTRAINT_CHECK_COMPLETE"
close_project
'''
    (work/'check.tcl').write_text(script,encoding='utf-8')
    output=command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe','check.tcl'],work,'td',allowed=(0,1,2))
    assert 'ONCE_CONSTRAINT_CHECK_COMPLETE' in output
    checks=(work/'check_timing.rpt').read_text(encoding='utf-8')
    assert 'checking invalid constraint(0)' in checks and 'checking combinational loops(0)' in checks
    paths=timing(work/'verification.timing')
    assert not paths['violations']
    save(work/'receipt.json',{'passed':True,'database_sha256':sha(work/'pr.db'),
         'constraints':{str(p):sha(p) for p in constraints},'timing':paths,
         'scope':'Reload same original constraints; no new exception or relaxed bound'})
    print('CONSTRAINT_RECHECK_PASS',flush=True)
    check()


def bitgen():
    check()
    summary=json.loads((ROOT/'comparison.json').read_text(encoding='utf-8'))
    assert not summary['all_endpoints']['violations'] and not summary['display_payload']['violations']
    physical=Path(summary['physical_directory'])
    assert all(sha(p)==h for p,h in summary['source_hashes'].items())
    work=fresh('diagnostic_bitgen')
    command(['compact.exe','/C','/I',work],work,'compress_directory')
    name='road_stem_ddr_board_top.al'
    tree=ET.fromstring((physical/name).read_text(encoding='utf-8').replace('UsedInP&R','UsedInP&amp;R'))
    tree.set('Path',work.as_posix())
    (work/name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(tree,encoding='unicode').replace('UsedInP&amp;R','UsedInP&R'),encoding='utf-8')
    shutil.copyfile(physical/'pr.db',work/'pr.db')
    script=(ROOT/'build/bitgen.tcl').read_text(encoding='utf-8')
    constraints=list(summary['constraint_check']['constraints'])
    assert all(sha(p)==h for p,h in summary['constraint_check']['constraints'].items())
    reads=f'read_sdc {{{Path(constraints[0]).as_posix()}}}\nread_sdc -ip ddr2 {{{Path(constraints[1]).as_posix()}}}\nread_sdc {{{Path(constraints[2]).as_posix()}}}\n'
    script=script.replace('import_db pr.db\n','import_db pr.db\n'+reads)
    # The exhaustive pre-bitgen report remains in the physical closure.
    script=script.replace('report_timing_summary -ep_num 100000','report_timing_summary -ep_num 100')
    (work/'bitgen.tcl').write_text(script,encoding='utf-8')
    output=command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe','bitgen.tcl'],work,'td',allowed=(0,1,2))
    assert 'DDR_DIAGNOSTIC_BITGEN_COMPLETE' in output and 'DDR_PAXI_CONNECTIVITY_COMPLETE count=256' in output
    imported=timing(work/'imported.timing')
    assert sha(work/'pr.db')==sha(physical/'pr.db')
    assert not imported['violations'] and set(imported['worst'])=={'setup','hold','recovery','removal'}
    bit=work/'HX1P35A_C7_STEM_DDR_DOWN2.bit'
    assert bit.stat().st_size>0
    receipt={'bitstream':str(bit),'sha256':sha(bit),'bytes':bit.stat().st_size,'database_sha256':sha(physical/'pr.db'),
             'program_sha256':sha(ROOT/'vectors/program.hex'),'board_status':'NOT_RUN',
             'scope':'Temporary SRAM diagnostic, actual arithmetic and DDR handoff with frozen TEST_ONLY coefficients'}
    save(work/'receipt.json',receipt)
    summary['bitstream']=receipt
    save(ROOT/'comparison.json',summary)
    status=json.loads((ROOT/'status.json').read_text(encoding='utf-8'))
    status['bitstream']=receipt
    save(ROOT/'status.json',status)
    print(json.dumps(receipt),flush=True)
    check()


def finalize():
    check()
    summary=json.loads((ROOT/'comparison.json').read_text(encoding='utf-8'))
    bit=summary['bitstream']
    assert sha(bit['bitstream'])==bit['sha256']
    assert summary['board_status']=='NOT_RUN' and not summary['whole_system_signoff']
    assert all(sha(p)==h for p,h in summary['source_hashes'].items())
    paths=[*ROOT.glob('*.py'),ROOT/'阶段报告.txt',ROOT/'上板操作.txt',ROOT/'comparison.json',
           ROOT/'frozen_check.json',ROOT/'diagnostic_bitgen/receipt.json']
    paths += [p for folder in ('rtl','reused','vectors','tests','build') for p in (ROOT/folder).rglob('*') if p.is_file()]
    save(ROOT/'artifact_hashes.json',{str(p):sha(p) for p in paths})
    save(ROOT/'status.json',{'status':'AWAITING_USER_BOARD_TEST','board_status':'NOT_RUN',
         'parameters':'FROZEN_TEST_ONLY','strict_delivery_ready':False,
         'production_modified':False,'core_modified':False,'bitstream':bit})
    print('FINAL_CLOSURE_PASS; awaiting user temporary SRAM board test',flush=True)


if __name__=='__main__':
    ast.parse(Path(__file__).read_text(encoding='utf-8'))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('setup','check','reference','gate','physical','integrated','recover_reports','collect','bitgen','check_constraints','finalize'))
    globals()[parser.parse_args().action]()
