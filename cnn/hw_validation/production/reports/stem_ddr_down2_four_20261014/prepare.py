"""Clone a frozen diagnostic, change only outer tile scheduling widths."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'stem_ddr_down2_once_20261014'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def replace(text,old,new):
    assert old in text,old
    return text.replace(old,new)


def generate():
    assert not (ROOT/'frozen.json').exists()
    frozen=json.loads((BASE/'frozen.json').read_text(encoding='utf-8'))
    frozen.update(json.loads((BASE/'artifact_hashes.json').read_text(encoding='utf-8')))
    assert all(sha(p)==h for p,h in frozen.items())
    (ROOT/'frozen.json').write_text(json.dumps(frozen,indent=2),encoding='utf-8')
    for name in ('rtl','tests','build','vectors','reused','mailbox_verification'):
        (ROOT/name).mkdir(exist_ok=True)
    for path in (BASE/'reused').glob('*.v'):
        shutil.copyfile(path,ROOT/'reused'/path.name)
    reused={str(p):sha(p) for p in (ROOT/'reused').glob('*.v')}
    (ROOT/'reused_sources.json').write_text(json.dumps(reused,indent=2),encoding='utf-8')
    for name in ('shared_core_interface.v','new_interfaces.v'):
        shutil.copyfile(BASE/name,ROOT/name)
    shutil.copyfile(BASE/'mailbox_verification/road_paxi_mailbox_spec.json',ROOT/'mailbox_verification/road_paxi_mailbox_spec.json')
    shutil.copyfile(BASE/'rtl/road_paxi_mailbox.v',ROOT/'rtl/road_paxi_mailbox.v')
    text=(BASE/'rtl/road_stem_ddr_sequence.v').read_text(encoding='utf-8')
    changes=[('[6:0]o_writes','[8:0]o_writes'),('[6:0]o_reads','[8:0]o_reads'),
        ('[8:0]o_output_bytes','[10:0]o_output_bytes'),('[0:4095]','[0:8191]'),
        ('[0:63]','[0:255]'),('reg [7:0]reg_halo_map[0:127]','reg [15:0]reg_halo_map[0:511]'),
        ('reg [7:0]reg_map','reg [15:0]reg_map'),('reg_output_golden[0:511]','reg_output_golden[0:2047]'),
        ('[11:0]cnt_program','[12:0]cnt_program'),('[5:0]reg_golden_index','[7:0]reg_golden_index'),
        ('[6:0]cnt_writes_o','[8:0]cnt_writes_o'),('[6:0]cnt_reads_o','[8:0]cnt_reads_o'),
        ('[8:0]cnt_output_bytes_o','[10:0]cnt_output_bytes_o'),
        ("cnt_writes_o == 7'd64 && cnt_reads_o == 7'd64","cnt_writes_o == 9'd256 && cnt_reads_o == 9'd289"),
        ("cnt_output_bytes_o == 9'd384","cnt_output_bytes_o == 11'd1536 && cnt_down2_tile == 3'd4"),
        ('reg_halo_map[cnt_halo_pixel]','reg_halo_map[{cnt_down2_tile[1:0],cnt_halo_pixel}]'),
        ('reg_map[7]','reg_map[8]'),('reg_map[5:0]','reg_map[7:0]'),
        ("cnt_output_bytes_o == 9'd383","cnt_tile_output == 9'd383"),
        ("cnt_program <= 12'd0","cnt_program <= 13'd0"),
        ("reg_golden_index <= 6'd0","reg_golden_index <= 8'd0"),
        ("cnt_writes_o <= 7'd0","cnt_writes_o <= 9'd0"),
        ("cnt_reads_o <= 7'd0","cnt_reads_o <= 9'd0"),
        ("cnt_output_bytes_o <= 9'd0","cnt_output_bytes_o <= 11'd0"),
        ("cnt_writes_o + 7'd1","cnt_writes_o + 9'd1"),
        ("reg_golden_index != 6'd63","reg_golden_index != 8'd255"),
        ("reg_golden_index + 6'd1","reg_golden_index + 8'd1"),
        ("cnt_reads_o + 7'd1","cnt_reads_o + 9'd1"),
        ("cnt_output_bytes_o + 9'd1","cnt_output_bytes_o + 11'd1"),
        ('core_output_index != cnt_output_bytes_o','core_output_index != cnt_tile_output'),
        ("cnt_program + 12'd1","cnt_program + 13'd1"),
        ("{1'b0,cnt_program}+13'd1","{1'b0,cnt_program}+14'd1")]
    for old,new in changes:
        text=replace(text,old,new)
    text=replace(text,'reg [8:0]cnt_export;',
        'reg [2:0]cnt_down2_tile; // 四个消费者，最终值四\n\treg [8:0]cnt_tile_output; // 当前tile的384字节输出游标\n\treg [8:0]cnt_export;')
    text=replace(text,"cnt_export <= 9'd0;\n", "cnt_export <= 9'd0;\n\t\t\tcnt_down2_tile <= 3'd0;\n\t\t\tcnt_tile_output <= 9'd0;\n")
    text=replace(text,"if(reg_command[63:60] == 4'd5)begin", "if(reg_command[63:60] == 4'd6)begin cnt_tile_output <= 9'd0; end\n\t\t\t\t\tif(reg_command[63:60] == 4'd5)begin")
    text=replace(text,"cnt_output_bytes_o <= cnt_output_bytes_o + 11'd1;", "cnt_output_bytes_o <= cnt_output_bytes_o + 11'd1;\n\t\t\t\t\t\tcnt_tile_output <= cnt_tile_output + 9'd1;\n\t\t\t\t\t\tif(cnt_tile_output == 9'd383)begin cnt_down2_tile <= cnt_down2_tile + 3'd1; end")
    text=replace(text,'Four computed Stem tiles are read back from DDR before down2.','Sixteen Stem tiles feed four down2 consumers through real DDR.')
    text=replace(text,'tile零、一、六十四、六十五的16字地址','十六个实际tile的256个字地址，保留层行跨度')
    text=replace(text,'最高位表示top/left补零，其余为黄金字索引','位八表示top/left补零，低八位为黄金字索引')
    text=replace(text,'384项有效PW输出与零填充','1536项有效PW输出与零填充')
    text=replace(text,'4096项ROM索引','8192项ROM索引')
    (ROOT/'rtl/road_stem_ddr_sequence.v').write_text(text,encoding='utf-8')
    # Mechanical generation keeps the established clock/IP shell unchanged.
    for name in ('run.py','make_board.py','prepare_build.py','render_spec.py'):
        text=(BASE/name).read_text(encoding='utf-8')
        if name=='run.py':
            text=text.replace("work=ROOT/'physical_reports_attempt3'","work=ROOT/'physical'")
            text=text.replace("cdc_work=ROOT/'physical_reports_attempt2'","cdc_work=ROOT/'physical'")
            text=text.replace("original=ROOT/'physical_attempt2'","original=ROOT/'physical'")
            text=text.replace("report=ROOT/'physical_reports_attempt3'","report=ROOT/'physical'")
            text=text.replace("for directory in (work,cdc_work):\n        receipt=json.loads((directory/'recovery_receipt.json').read_text(encoding='utf-8'))\n        assert receipt['same_database_sha256']==database_sha",'assert cdc_work==work')
            text=text.replace('HX1P35A_C7_STEM_DDR_DOWN2.bit','HX1P35A_C7_STEM_DDR_DOWN2_FOUR.bit')
        elif name=='make_board.py':
            text=text.replace('wire [6:0] writes,reads','wire [8:0] writes,reads').replace('wire [8:0] output_bytes','wire [10:0] output_bytes')
            text=text.replace("cycles,60'h535444445232","cycles,54'h535444445234")
        elif name=='prepare_build.py':
            text=text.replace('$bit < 188','$bit < 182').replace('0x535444445232','0x535444445234')
            text=text.replace('HX1P35A_C7_STEM_DDR_DOWN2.bit','HX1P35A_C7_STEM_DDR_DOWN2_FOUR.bit')
        elif name=='render_spec.py':
            text=text.replace('stem_ddr_down2_once','stem_ddr_down2_four')
            text=text.replace('四个实际Stem tile','十六个实际Stem tile').replace('384字节','1536字节')
            text=text.replace('3143条固定命令，4个Stem tile、64个唯一写字、64个真实读字、17像素补零、384输出字节。',
                '固定程序，16个Stem tile、256个唯一写字、289个真实读字、35次补零像素、1536输出字节。')
        (ROOT/name).write_text(text,encoding='utf-8')
    assert sha(ROOT/'rtl/road_paxi_mailbox.v')==sha(BASE/'rtl/road_paxi_mailbox.v')
    print('PREPARED: old baseline frozen; only outer sequence widths and tile metadata changed')


if __name__=='__main__':
    generate()
