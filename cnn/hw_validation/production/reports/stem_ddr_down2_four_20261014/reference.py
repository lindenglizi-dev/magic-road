"""Sixteen actual Stem tiles, four overlapping down2 halos, frozen test data."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[4]
BASE=ROOT.parent/'stem_down2_handoff_20261011/vectors'
sys.path.insert(0,str(PROJECT))
from cnn import integer


def words(name,bits):
    raw=np.array([int(v,16) for v in (BASE/name).read_text().split()],dtype=np.int64)
    return np.where(raw>=1<<(bits-1),raw-(1<<bits),raw)


def generate():
    out=ROOT/'vectors'
    out.mkdir(exist_ok=True)
    rgb=words('rgb.hex',8).astype(np.uint8).reshape(288,512,3)
    sw=words('stem_weights.hex',8).reshape(16,3,3,3).astype(np.int8)
    sb,sm,ss,sp=(words(n,32) for n in ('stem_biases.hex','stem_multipliers.hex','stem_shifts.hex','stem_post.hex'))
    dw=words('dw_weights.hex',8).reshape(16,1,3,3).astype(np.int8)
    db=words('dw_biases.hex',32)
    pw=words('pw_weights.hex',8).reshape(24,16,1,1).astype(np.int8)
    pb=words('pw_biases.hex',32)
    multipliers,controls=words('multipliers.hex',32),words('controls.hex',32)
    stem_acc=integer.conv2d((rgb[:32,:32].astype(np.int16)-128).astype(np.int8),sw,sb,stride=2,padding=1)
    stem_pre=integer.requantize(stem_acc,sm,ss,-32768,32767)
    stem_act=integer.silu(stem_pre)
    stem=integer.requantize(stem_act.astype(np.int32),int(sp[0]),int(sp[1])).astype(np.int8)
    assert stem.shape==(16,16,16)
    assert np.array_equal(stem,np.load(BASE/'expected_stem_hwc.npy')[:16,:16])
    halo=np.pad(stem,((1,0),(1,0),(0,0)))
    acc_dw=integer.conv2d(halo,dw,db,stride=2,padding=0,groups=16)
    pre_dw=integer.requantize(acc_dw,multipliers[:16],controls[:16],-32768,32767)
    act_dw=integer.silu(pre_dw)
    result_dw=integer.requantize(act_dw.astype(np.int32),int(controls[40]),int(controls[42])).astype(np.int8)
    acc_pw=integer.conv2d(result_dw,pw,pb,stride=1,padding=0)
    pre_pw=integer.requantize(acc_pw,multipliers[16:],controls[16:40],-32768,32767)
    act_pw=integer.silu(pre_pw)
    result_pw=integer.requantize(act_pw.astype(np.int32),int(controls[41]),int(controls[43])).astype(np.int8)
    assert result_pw.shape==(8,8,24)
    assert np.array_equal(result_pw,np.load(BASE/'expected_pw_hwc.npy')[:8,:8])
    program=[]
    def record(op,address=0,kind=0,value=0):
        assert 0<=op<8 and 0<=address<2048 and 0<=kind<8
        program.append(op<<60 | address<<49 | kind<<46 | int(value)&0xffffffff)
    def load(kind,values):
        for address,value in enumerate(np.asarray(values).ravel()):
            record(1,address,kind,int(value))
    for address,value in enumerate(words('silu.hex',16)):
        record(0,address,value=int(value))
    load(2,sw);load(3,sb);load(4,sm);load(5,ss);load(6,sp)
    golden,addresses=[],[]
    stem_tiles=[(y,x) for y in range(4) for x in range(4)]
    output_tiles=[(0,0),(0,1),(1,0),(1,1)]
    for ty,tx in stem_tiles:
        for hy in range(9):
            for hx in range(9):
                gy,gx=ty*8+hy-1,tx*8+hx-1
                padding=gy<0 or gx<0
                for channel in range(3):
                    record(1,(hy*9+hx)*3+channel,int(padding),0 if padding else int(rgb[gy,gx,channel]))
        record(2);record(3)
        for ly in range(4):
            for lx in range(4):
                pixel=stem[ty*4+ly,tx*4+lx].view(np.uint8).tobytes()
                golden.append(int.from_bytes(pixel,'little'))
                addresses.append((0x03500000+((ty*64+tx)*16+ly*4+lx)*16)//2)
    record(4,value=1)
    load(2,dw);load(3,db);load(4,pw);load(5,pb);load(6,multipliers);load(7,controls)
    for _ in output_tiles:
        record(5);record(2);record(6)
    record(7)
    assert len(program)<=8192 and len(golden)==len(set(addresses))==256
    selected=False
    lengths=({0:243,1:243,2:432,3:16,4:16,5:16,6:2},
             {0:1296,1:256,2:144,3:16,4:384,5:24,6:40,7:44})
    for instruction in program:
        opcode=instruction>>60
        if opcode==4:
            selected=bool(instruction&1)
        elif opcode==1:
            kind=(instruction>>46)&7
            address=(instruction>>49)&2047
            assert kind in lengths[selected] and address<lengths[selected][kind],(selected,kind,address)
    assert all(0x03400000<=a*2<=0x03fffff0 and a%8==0 for a in addresses)
    mapping,read_indices,padding_counts=[],[],[]
    for ty,tx in output_tiles:
        tile_map=[]
        for y in range(9):
            for x in range(9):
                gy,gx=ty*8+y-1,tx*8+x-1
                index=256 if gy<0 or gx<0 else ((gy//4)*4+gx//4)*16+(gy%4)*4+gx%4
                tile_map.append(index)
        assert len(set(i for i in tile_map if i!=256))==sum(i!=256 for i in tile_map)
        padding_counts.append(tile_map.count(256))
        reconstructed=np.zeros((81,16),dtype=np.uint8)
        for pos,index in enumerate(tile_map):
            if index!=256:
                read_indices.append(index)
                reconstructed[pos]=np.frombuffer(golden[index].to_bytes(16,'little'),dtype=np.uint8)
        assert np.array_equal(reconstructed.reshape(9,9,16).view(np.int8),halo[ty*8:ty*8+9,tx*8:tx*8+9])
        mapping+=tile_map+[256]*47
    assert padding_counts==[17,9,9,0] and len(read_indices)==289
    assert len(set(read_indices))==256
    def tiled(tensor,tiles):
        return np.concatenate([tensor[y*4:y*4+4,x*4:x*4+4].ravel() for y,x in tiles])
    def emit(name,values,bits,depth=None):
        values=list(map(int,values))
        if depth:
            assert len(values)<=depth
            values += [0]*(depth-len(values))
        (out/name).write_text(''.join(f'{v&((1<<bits)-1):0{bits//4}x}\n' for v in values),encoding='ascii')
    emit('program.hex',program,64,8192)
    emit('stem_golden.hex',golden,128)
    emit('stem_addresses.hex',addresses,32)
    emit('halo_map.hex',mapping,16,512)
    emit('read_indices.hex',read_indices,16)
    emit('pw_golden.hex',tiled(result_pw,output_tiles).view(np.uint8),8,2048)
    for prefix,tensors,tiles in [('stem',(stem_acc,stem_pre,stem_act,stem),stem_tiles),
                                  ('dw',(acc_dw,pre_dw,act_dw,result_dw),output_tiles),
                                  ('pw',(acc_pw,pre_pw,act_pw,result_pw),output_tiles)]:
        for suffix,tensor,bits in zip(('acc','pre','silu','post'),tensors,(32,16,16,8)):
            emit(f'{prefix}_{suffix}.hex',tiled(tensor,tiles),bits)
    (out/'once_constants.vh').write_text(f"localparam PROGRAM_LENGTH = 14'd{len(program)};\n",encoding='ascii')
    inputs={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir()
            if p.is_file() and p.suffix in ('.hex','.npy')}
    receipt={'passed':True,'parameters':'FROZEN_TEST_ONLY','program_length':len(program),
        'stem_tiles':16,'stem_bytes':4096,'writes':256,'reads':289,'down2_tiles':4,
        'padding_pixels':padding_counts,'halo_bytes_per_tile':1296,'pw_bytes':1536,
        'read_indices':read_indices,'stem_tile_ids':[y*64+x for y,x in stem_tiles],
        'down2_tile_ids':[0,1,32,33],'layout':'frozen tile4x4_hwc; native=byte>>1',
        'input_hashes':inputs,'output_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}}
    (ROOT/'reference.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print('FOUR_REFERENCE_PASS',len(program),'commands 256W/289R 4096Stem/1536PW bytes')
    return receipt


if __name__=='__main__':
    generate()
