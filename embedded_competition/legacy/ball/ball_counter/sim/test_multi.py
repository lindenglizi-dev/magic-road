"""候选顺序扰动、四球同帧、掉检、反向、容量、故障与饱和的独立模型向量。"""
from pathlib import Path
import random
import sys

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from multi_model import MultiCounter,Track,box,check


def pack(model):
    valid=sum(int(t.active)<<i for i,t in enumerate(model.tracks))
    colors=sum((0 if not t.active or t.misses else t.color)<<(i*2) for i,t in enumerate(model.tracks))
    bounds=[0,0,0,0]
    for i,t in enumerate(model.tracks):
        if not t.active:continue
        l=t.x-(t.w-1)//2;top=t.y-(t.h-1)//2
        for k,v in enumerate([l,l+t.w-1,top,top+t.h-1]):bounds[k]|=v<<(12*i)
    first=next((t for t in model.tracks if t.active),None)
    values=[(model.counts[1],32),(model.counts[3],32),(model.counts[2],32),
            (model.reason,3),(model.state,3),(valid.bit_count(),3),(valid,4),(colors,8)]
    values += [(v,48) for v in bounds]
    values += [(first.x if first else 0,12),(first.y if first else 0,12)]
    result=0
    for v,w in values:result=(result<<w)|v
    return result


def main():
    check()
    model=MultiCounter();rng=random.Random(20);frames=[];expected=[]
    def frame(obs=(),fault=0,overflow=0,clear=0):
        obs=list(obs);rng.shuffle(obs)
        if clear:
            model.tracks=[Track() for _ in range(4)];model.reason=0;model.state=0
            if clear==2:model.counts=[0,0,0,0]
        else:model.step(obs,fault=bool(fault),overflow=bool(overflow))
        frames.append((obs,fault,overflow,clear));expected.append(pack(model))
    frame()
    for x in [560,580,620,660,680]:frame([box(1,x,y) for y in [200,300,400,500]])
    for _ in range(20):frame([box(1,680,y) for y in [200,300,400,500]])
    frame();frame();frame([box(1,680,y) for y in [200,300,400,500]])
    for x in list(range(640,559,-40))+list(range(600,681,40)):
        frame([box(1,x,y) for y in [200,300,400,500]])
    frame(clear=1)
    for x in [560,580,620,660]:frame([box(c,x,y) for c,y in [(1,200),(2,300),(3,400),(1,500)]])
    for _ in range(8):frame()
    for x in [560,580,660]:frame([box(1,x,300)])
    frame(clear=1)
    for x in [560,580]:frame([box(2,x,y) for y in [200,300,400,500]])
    frame([box(2,660,y) for y in [200,300,400,500]],fault=3)
    frame([box(2,660,y) for y in [200,300,400,500]],fault=2)
    frame([box(2,660,y) for y in [200,300,400,500]],overflow=1)
    frame([box(2,660,y) for y in [200,300,400,500]])
    frame([box(1,560,y) for y in [180,260,340,420,500]])
    frame(clear=1)
    # 四个旧槽位仍保留时，新目标不可覆盖；缺失计数继续老化，八帧后可分配。
    frame([box(1,200,y) for y in [200,300,400,500]])
    for _ in range(9):frame([box(2,560,300)])
    frame([box(2,580,300)]);frame([box(2,660,300)])
    frame(clear=2)
    for x in [740,700,660,620,580,620,660]:frame([box(3,x,300)])
    assert model.counts==[0,0,0,0],model.counts
    frame(clear=2)
    for step in range(30):frame([box(1,x+step*20,300) for x in [100,230,360,490]])
    assert model.counts==[0,4,0,0],model.counts
    with (root/'sim/multi_inputs.txt').open('w') as out:
        for obs,fault,overflow,clear in frames:
            out.write(f'{len(obs)} {fault} {overflow} {clear}\n')
            for c,l,r,t,b in obs:out.write(f'{c} {l} {r} {t} {b}\n')
    (root/'sim/multi_expected.hex').write_text(''.join(f'{v:084x}\n' for v in expected))
    print(f'PASS model vectors:{len(frames)} frames',flush=True)


if __name__=='__main__':main()
