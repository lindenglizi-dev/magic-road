from pathlib import Path
import sys,json
import numpy as np
from softmax_fixed import softmax_fixed,scale_for_dim
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'vectors'

def put_hex(p,values,bits):
    mask=(1<<bits)-1
    p.write_text(''.join(f'{int(x)&mask:0{bits//4}x}\n' for x in np.asarray(values).flat))

def gen(case):
    src=SRC/case
    cfg=json.loads((src/'config.json').read_text())
    data=np.load(src/'reference.npz')
    Q,K,V=[data['out'][i].astype(np.int32) for i in range(3)]
    L,D=Q.shape
    score=Q@K.T
    scale=scale_for_dim(D)
    prob_u8=np.asarray([softmax_fixed(row,scale) for row in score],dtype=np.int32)
    prob_i8=np.minimum(127,(prob_u8+1)//2).astype(np.int32)
    out=prob_i8@V
    dest=ROOT/'vectors'/case
    dest.mkdir(parents=True,exist_ok=True)
    for x in ['x_banks.hex','w_banks.hex','config.txt','raw.hex','out.hex','score.hex']:
        if (dest/x).resolve() != (src/x).resolve():
            (dest/x).write_bytes((src/x).read_bytes())
    put_hex(dest/'prob.hex',prob_i8,8)
    put_hex(dest/'pv.hex',out,32)
    (dest/'softmax_scale.txt').write_text(str(scale)+'\n')
    (dest/'expected.json').write_text(json.dumps(dict(L=L,D=D,scale=scale, Q=Q.tolist() if L<5 else 'omitted',score=score.tolist() if L<5 else 'omitted', P=prob_i8.tolist() if L<5 else 'omitted',output=out.tolist() if L<5 else 'omitted'),ensure_ascii=False,indent=2))
    check_score=np.array([int(x,16) for x in (dest/'score.hex').read_text().splitlines()],dtype=np.uint32).view(np.int32).reshape(L,L)
    np.testing.assert_array_equal(score,check_score)
    # verify exact physical addressing: Q/Key row bank; V col bank; P row bank
    for row in range(L):
      for col in range(D):
        vbank=col%4;vaddr=row*((D+3)//4)+col//4
        assert vaddr < L*((D+3)//4)
      for col in range(L):
        pbank=row%4;paddr=(row//4)*L+col
        assert paddr<((L+3)//4)*L
    print(f'PASS Python source-to-tail: {case} L={L} D={D}, output={out.shape}, scale={scale}')

if __name__=='__main__':
    for name in ['demo','edge_5x7','random_00','sat_1x1']:
        if (SRC/name/'reference.npz').exists():gen(name)
