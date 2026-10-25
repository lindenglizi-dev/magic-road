"""Four real Stem tiles and one top-left down2 tile, frozen test parameters."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
BASE = ROOT.parent/'stem_down2_handoff_20261011/vectors'
sys.path.insert(0,str(PROJECT))
from cnn import integer


def words(name,bits):
    raw = np.array([int(v,16) for v in (BASE/name).read_text().split()],dtype=np.int64)
    return np.where(raw >= 1<<(bits-1),raw-(1<<bits),raw)


def generate():
    out = ROOT/'vectors'
    out.mkdir(exist_ok=True)
    rgb = words('rgb.hex',8).astype(np.uint8).reshape(288,512,3)
    sw = words('stem_weights.hex',8).reshape(16,3,3,3).astype(np.int8)
    sb = words('stem_biases.hex',32)
    sm = words('stem_multipliers.hex',32)
    ss = words('stem_shifts.hex',32)
    sp = words('stem_post.hex',32)
    dw = words('dw_weights.hex',8).reshape(16,1,3,3).astype(np.int8)
    db = words('dw_biases.hex',32)
    pw = words('pw_weights.hex',8).reshape(24,16,1,1).astype(np.int8)
    pb = words('pw_biases.hex',32)
    multipliers,controls = words('multipliers.hex',32),words('controls.hex',32)
    source = (rgb[:16,:16].astype(np.int16)-128).astype(np.int8)
    stem_acc = integer.conv2d(source,sw,sb,stride=2,padding=1)
    stem_pre = integer.requantize(stem_acc,sm,ss,-32768,32767)
    stem_act = integer.silu(stem_pre)
    stem = integer.requantize(stem_act.astype(np.int32),int(sp[0]),int(sp[1])).astype(np.int8)
    assert stem.shape == (8,8,16)
    assert np.array_equal(stem,np.load(BASE/'expected_stem_hwc.npy')[:8,:8])
    halo = np.pad(stem,((1,0),(1,0),(0,0)))
    acc_dw = integer.conv2d(halo,dw,db,stride=2,padding=0,groups=16)
    pre_dw = integer.requantize(acc_dw,multipliers[:16],controls[:16],-32768,32767)
    act_dw = integer.silu(pre_dw)
    result_dw = integer.requantize(act_dw.astype(np.int32),int(controls[40]),int(controls[42])).astype(np.int8)
    acc_pw = integer.conv2d(result_dw,pw,pb,stride=1,padding=0)
    pre_pw = integer.requantize(acc_pw,multipliers[16:],controls[16:40],-32768,32767)
    act_pw = integer.silu(pre_pw)
    result_pw = integer.requantize(act_pw.astype(np.int32),int(controls[41]),int(controls[43])).astype(np.int8)
    assert result_pw.shape == (4,4,24)
    assert np.array_equal(result_pw,np.load(BASE/'expected_pw_hwc.npy')[:4,:4])
    program = []
    def record(op,address=0,kind=0,value=0):
        assert 0<=op<8 and 0<=address<2048 and 0<=kind<8
        program.append(op<<60 | address<<49 | kind<<46 | int(value)&0xffffffff)
    def load(kind,values):
        for address,value in enumerate(np.asarray(values).ravel()):
            record(1,address,kind,int(value))
    for address,value in enumerate(words('silu.hex',16)):
        record(0,address,value=int(value))
    load(2,sw);load(3,sb);load(4,sm);load(5,ss);load(6,sp)
    golden,addresses = [],[]
    for ty,tx in [(0,0),(0,1),(1,0),(1,1)]:
        for hy in range(9):
            for hx in range(9):
                gy,gx = ty*8+hy-1,tx*8+hx-1
                padding = gy<0 or gx<0
                for channel in range(3):
                    record(1,(hy*9+hx)*3+channel,int(padding),0 if padding else int(rgb[gy,gx,channel]))
        record(2);record(3)
        for ly in range(4):
            for lx in range(4):
                pixel = stem[ty*4+ly,tx*4+lx].view(np.uint8).tobytes()
                golden.append(int.from_bytes(pixel,'little'))
                addresses.append((0x03500000+((ty*64+tx)*16+ly*4+lx)*16)//2)
    record(4,value=1)
    load(2,dw);load(3,pw);load(4,db);load(5,pb);load(6,multipliers);load(7,controls)
    record(5);record(2);record(6);record(7)
    assert len(program)<=4096 and len(golden)==len(set(addresses))==64
    assert all(0x03400000<=a*2<=0x03fffff0 and a%8==0 for a in addresses)
    mapping = []
    for y in range(9):
        for x in range(9):
            if y==0 or x==0:
                mapping.append(0x80)
            else:
                gy,gx=y-1,x-1
                mapping.append(((gy//4)*2+gx//4)*16+(gy%4)*4+gx%4)
    assert sum(v==0x80 for v in mapping)==17
    assert sorted(v for v in mapping if v!=0x80)==list(range(64))
    reconstructed = np.zeros((9,9,16),dtype=np.uint8)
    for pos,index in enumerate(mapping):
        if index!=0x80:
            reconstructed.reshape(81,16)[pos]=np.frombuffer(golden[index].to_bytes(16,'little'),dtype=np.uint8)
    assert np.array_equal(reconstructed.view(np.int8),halo)
    def emit(name,values,bits,depth=None):
        values=list(map(int,values))
        if depth:
            values += [0]*(depth-len(values))
        (out/name).write_text(''.join(f'{v&((1<<bits)-1):0{bits//4}x}\n' for v in values),encoding='ascii')
    emit('program.hex',program,64,4096)
    emit('stem_golden.hex',golden,128)
    emit('stem_addresses.hex',addresses,32)
    emit('halo_map.hex',mapping,8,128)
    emit('pw_golden.hex',result_pw.view(np.uint8).ravel(),8,512)
    emit('stem_acc.hex',np.concatenate([stem_acc[y:y+4,x:x+4].ravel() for y,x in [(0,0),(0,4),(4,0),(4,4)]]),32)
    emit('dw_acc.hex',acc_dw.ravel(),32)
    emit('pw_acc.hex',acc_pw.ravel(),32)
    (out/'once_constants.vh').write_text(f'localparam PROGRAM_LENGTH = 13\'d{len(program)};\n',encoding='ascii')
    inputs = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir()
              if p.is_file() and p.name in {'rgb.hex','stem_weights.hex','stem_biases.hex','stem_multipliers.hex',
                  'stem_shifts.hex','stem_post.hex','dw_weights.hex','dw_biases.hex','pw_weights.hex',
                  'pw_biases.hex','multipliers.hex','controls.hex','silu.hex','expected_stem_hwc.npy','expected_pw_hwc.npy'}}
    receipt = {'passed':True,'parameters':'FROZEN_TEST_ONLY','program_length':len(program),'stem_tiles':4,
               'stem_bytes':1024,'writes':64,'reads':64,'padding_pixels':17,'halo_bytes':1296,'pw_bytes':384,
               'layout':'frozen tile4x4_hwc; tile IDs 0/1/64/65; native=byte>>1',
               'input_hashes':inputs,'output_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}}
    (ROOT/'reference.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print('ONCE_REFERENCE_PASS',len(program),'commands 64W/64R 1024Stem/384PW bytes')
    return receipt


if __name__=='__main__':
    generate()
