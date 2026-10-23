#!/usr/bin/env python3
import numpy as np
from pathlib import Path
from gen_vectors import ROOT,scale_for_dim,softmax_fixed

def read_signed(path, bits, shape):
    a=np.array([int(x,16) for x in path.read_text().split()],dtype=np.uint64)
    signs=(a&(1<<(bits-1)))!=0
    a=a.astype(np.int64)
    a[signs]-=1<<bits
    return a.reshape(shape)

def run():
    count=0
    for name in ("demo","edge_5x7","random_00","sat_1x1"):
        path=ROOT/"vectors"/name
        z=np.load(path/"reference.npz")
        L,D=z["X"].shape
        F,ats,hs,w1b,w2b=map(int,(path/"ffn_config.txt").read_text().split())
        shifts=list(map(int,(path/'config.txt').read_text().split()))[2:5]
        raw=z["X"].astype(np.int32)@z["W"].astype(np.int32)
        qkv=np.stack([np.clip(raw[i]>>shifts[i],-128,127) for i in range(3)])
        np.testing.assert_array_equal(raw,z['raw'])
        np.testing.assert_array_equal(qkv,z['out'])
        np.testing.assert_array_equal(read_signed(path/'raw.hex',32,(3,L,D)),raw)
        np.testing.assert_array_equal(read_signed(path/'out.hex',8,(3,L,D)),qkv)
        count+=raw.size+qkv.size
        score=qkv[0]@qkv[1].T
        p=np.minimum(127,(np.array([softmax_fixed(row,scale_for_dim(D)) for row in score])+1)//2)
        o=p@qkv[2]
        act=np.clip(o>>ats,-128,127).astype(np.int8)
        rng=np.random.default_rng(8000+L*100+D)
        w1=rng.integers(-3,4,size=(D,F),dtype=np.int8)
        w2=rng.integers(-3,4,size=(F,D),dtype=np.int8)
        h=np.clip(np.maximum(0,(act.astype(np.int32)@w1.astype(np.int32))>>hs),0,127).astype(np.int8)
        y=h.astype(np.int32)@w2.astype(np.int32)
        for stem,bits,shape,expected in [('score',32,(L,L),score),('pv',32,(L,D),o),('act',8,(L,D),act),('hidden',8,(L,F),h),('final',32,(L,D),y)]:
            np.testing.assert_array_equal(read_signed(path/(stem+'.hex'),bits,shape),expected)
            count+=expected.size
        print(f'PASS {name}: L={L},D={D},F={F}, checked output arrays')
    rtl=(ROOT/'rtl'/'transformer_block_top.sv').read_text()
    assert rtl.count('u_gemm (')==1
    assert all(s in rtl for s in ('PH_FFN1=5','PH_FFN2=6','act_wr_en','hidden_wr_en','y_wr_en'))
    print('PASS Python end-to-end, signed quantization, bank layout, one GEMM:',count,'values')
if __name__=='__main__':run()
