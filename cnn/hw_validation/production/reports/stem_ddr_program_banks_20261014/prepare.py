"""Freeze the parent and split only command storage, never arithmetic."""
import json
from pathlib import Path
import shutil

import run

ROOT,BASE=run.ROOT,run.BASE


def replace(text,old,new):
    assert text.count(old)==1,old
    return text.replace(old,new)


def prepare():
    assert not (ROOT/'frozen.json').exists()
    frozen=json.loads((BASE/'frozen.json').read_text(encoding='utf-8'))
    frozen.update(json.loads((BASE/'artifact_hashes.json').read_text(encoding='utf-8')))
    assert all(run.sha(path)==value for path,value in frozen.items())
    run.save(ROOT/'frozen.json',frozen)
    for folder in ('rtl','reused','vectors','tests','build'):
        (ROOT/folder).mkdir(exist_ok=True)
        for path in (BASE/folder).iterdir():
            if path.is_file() and path.suffix in ('.v','.vh','.hex','.tcl','.py'):
                shutil.copyfile(path,ROOT/folder/path.name)
    for name in ('reference.json','shared_core_interface.v','new_interfaces.v'):
        shutil.copyfile(BASE/name,ROOT/name)
    (ROOT/'sequence_verification').mkdir()
    shutil.copyfile(BASE/'sequence_verification/run_verify.py',ROOT/'sequence_verification/run_verify.py')
    (ROOT/'mailbox_verification').mkdir()
    shutil.copyfile(BASE/'mailbox_verification/road_paxi_mailbox_spec.json',ROOT/'mailbox_verification/road_paxi_mailbox_spec.json')
    run.save(ROOT/'reused_sources.json',{str(path):run.sha(path) for path in (ROOT/'reused').glob('*.v')})
    # Python semantic check precedes RTL generation.
    words=(ROOT/'vectors/program.hex').read_text(encoding='ascii').splitlines()
    assert len(words)==8192
    banks=[words[:4096],words[4096:]]
    assert banks[0]+banks[1]==words
    assert banks[0][-1]==words[4095] and banks[1][0]==words[4096]
    for name,values in zip(('program_low.hex','program_high.hex'),banks):
        for folder in ('rtl','vectors'):
            (ROOT/folder/name).write_text('\n'.join(values)+'\n',encoding='ascii')
    path=ROOT/'rtl/road_stem_ddr_sequence.v'
    text=path.read_text(encoding='utf-8')
    text=replace(text,'reg [63:0]reg_commands[0:8191]; // 固定程序，无运行时修改或跳转',
        'reg [63:0]reg_commands_low[0:4095]; // 命令地址零至四千零九十五\n\treg [63:0]reg_commands_high[0:4095]; // 命令地址四千零九十六至八千一百九十一')
    text=replace(text,'reg [63:0]reg_command; // 同步ROM返回，整个命令执行时保持',
        '(* syn_keep = 1 *) reg [63:0]reg_command_low; // 低bank同步返回，仅FETCH更新\n\t(* syn_keep = 1 *) reg [63:0]reg_command_high; // 高bank同步返回，与低bank同沿\n\t(* syn_keep = 1 *) reg flag_command_bank; // 与两个返回同拍锁存的选择位\n\twire [63:0]reg_command; // 稳定的原接口命令字，不增加取指拍')
    text=replace(text,'assign flag_halo_load = state_current == ST_HALO_BYTE;',
        'assign reg_command = flag_command_bank ? reg_command_high : reg_command_low;\n\tassign flag_halo_load = state_current == ST_HALO_BYTE;')
    text=replace(text,'$readmemh("program.hex",reg_commands);',
        '$readmemh("program_low.hex",reg_commands_low);\n\t\t$readmemh("program_high.hex",reg_commands_high);')
    text=replace(text,'reg_command <= reg_commands[cnt_program];',
        'reg_command_low <= reg_commands_low[cnt_program[11:0]];\n\t\t\treg_command_high <= reg_commands_high[cnt_program[11:0]];\n\t\t\tflag_command_bank <= cnt_program[12];')
    path.write_text(text,encoding='utf-8')
    assert run.sha(ROOT/'rtl/road_paxi_mailbox.v')==run.sha(BASE/'rtl/road_paxi_mailbox.v')
    assert run.sha(ROOT/'rtl/road_stem_ddr_board_top.v')==run.sha(BASE/'rtl/road_stem_ddr_board_top.v')
    run.save(ROOT/'reference_banks.json',{'passed':True,'words':8192,'banks':2,'words_per_bank':4096,
        'latency_change':0,'original_program_sha256':run.sha(ROOT/'vectors/program.hex'),
        'boundary':{'4095':words[4095],'4096':words[4096]},
        'bank_sha256':{n:run.sha(ROOT/'vectors'/n) for n in ('program_low.hex','program_high.hex')},
        'unchanged_build':{p.name:run.sha(p) for p in (ROOT/'build').glob('*.tcl')}})
    run.check()
    print('BANK_REFERENCE_PASS words=8192 boundary4095/4096 identical; old candidate frozen')


if __name__=='__main__':
    prepare()
