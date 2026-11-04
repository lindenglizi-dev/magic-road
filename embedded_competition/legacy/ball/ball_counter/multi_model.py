"""COUNT四轨迹语义模型；输入来自检测结果，不读取球场景身份。"""
from dataclasses import dataclass,replace
from pathlib import Path
import json


@dataclass
class Track:
    active: bool=False
    color: int=0
    x: int=0
    y: int=0
    w: int=0
    h: int=0
    vx: int=0
    vy: int=0
    misses: int=0
    upstream: int=0
    armed: bool=False
    counted: bool=False
    blocked: bool=False


class MultiCounter:
    def __init__(self,move=64,line=640,hyst=16):
        self.tracks=[Track() for _ in range(4)]
        self.counts=[0,0,0,0]
        self.move,self.line,self.hyst=move,line,hyst
        self.reason=0
        self.state=0

    def step(self,candidates,fault=False,overflow=False):
        # 候选为(color,left,right,top,bottom)，候选顺序允许逐帧变化。
        if fault or overflow or len(candidates)>4:
            self.reason=5 if fault else 1 if overflow else 2
            self.state=4
            return
        obs=[(c,(l+r)//2,(t+b)//2,r-l+1,b-t+1) for c,l,r,t,b in candidates]
        work=[replace(t) for t in self.tracks]
        used_t,used_c=set(),set()
        matches={}
        for _ in range(4):
            pairs=[]
            for i,t in enumerate(work):
                for j,(c,x,y,w,h) in enumerate(obs):
                    dx,dy=abs(x-t.x-t.vx),abs(y-t.y-t.vy)
                    limit=self.move*(2 if t.misses else 1)
                    if t.active and i not in used_t and j not in used_c and c==t.color and \
                       w<=2*t.w and t.w<=2*w and h<=2*t.h and t.h<=2*h and dx<=limit and dy<=limit:
                        pairs.append((dx+dy,i,j))
            if not pairs:break
            _,i,j=min(pairs);used_t.add(i);used_c.add(j);matches[i]=j
        for i,t in enumerate(work):
            if t.active and i not in used_t:
                t.misses+=1
                if not t.armed:t.upstream=0
                if t.misses>=8:t.active=False
        if sum(not t.active for t in work)<len(obs)-len(used_c):
            self.tracks=work
            self.reason=2
            self.state=4
            return
        for j,obs_item in enumerate(obs):
            if j in used_c:continue
            free=next((i for i,t in enumerate(work) if not t.active),None)
            if free is None:
                self.reason=2
                return
            work[free]=Track(active=True,color=obs_item[0])
            matches[free]=j;used_c.add(j)
        delta=[0,0,0,0];reason=0
        for i,j in matches.items():
            t=work[i];c,x,y,w,h=obs[j]
            if t.w and not t.misses:
                t.vx=max(-2*self.move,min(2*self.move,x-t.x))
                t.vy=max(-2*self.move,min(2*self.move,y-t.y))
            t.x,t.y,t.w,t.h,t.misses=x,y,w,h,0
            if not t.counted and not t.blocked:
                if x<=self.line-self.hyst:
                    t.upstream=min(2,t.upstream+1)
                    if t.upstream>=2:t.armed=True
                elif not t.armed:
                    t.blocked=True;reason=3
                elif x>=self.line+self.hyst:
                    t.counted=True;delta[c]+=1
        self.tracks=work
        for c in [1,2,3]:
            value=self.counts[c]+delta[c]
            if value>0xffffffff:reason=6
            self.counts[c]=min(value,0xffffffff)
        self.reason=reason
        self.state=2 if any(t.active and t.armed and not t.counted for t in work) else 3 if any(t.active and t.counted for t in work) else 1


def shape_ok(width,height,area,cells,perimeter,min_size=24,max_size=384):
    return area>=128 and min_size<=width<=max_size and min_size<=height<=max_size and \
        2*width<=3*height and 2*height<=3*width and area*4>=width*height and \
        cells*256<=width*height*15 and perimeter*perimeter<=27*cells


def box(color,x,y,size=40):return color,x-size//2,x+size//2-1,y-size//2,y+size//2-1


def check():
    m=MultiCounter()
    for x in [560,580,620,660,680]:m.step([box(1,x,y) for y in [200,300,400,500]])
    assert m.counts==[0,4,0,0]
    for _ in range(20):m.step([box(1,680,y) for y in [200,300,400,500]])
    assert m.counts[1]==4
    for _ in range(2):m.step([])
    m.step([box(1,680,y) for y in [200,300,400,500]])
    assert m.counts[1]==4
    for _ in range(8):m.step([])
    for x in [560,580,660]:m.step([box(2,x,300)])
    assert m.counts[2]==1
    counts=m.counts[:]
    m.step([box(1,560,y) for y in [180,260,340,420,500]])
    assert m.reason==2 and m.counts==counts
    assert shape_ok(80,80,4800,320,80)
    assert not shape_ok(80,80,6400,400,80) # 实心方块。
    assert not shape_ok(80,80,3200,200,80) # 三角形/低紧致度。
    assert not shape_ok(120,40,3800,240,80)
    Path('reports/model_checks.json').write_text(json.dumps({'passed':True,'counts':m.counts,'tracks':4,'miss_retention':8}),encoding='utf-8')
    print('PASS model:four simultaneous same-color counts, hold/dropout dedup, next color, capacity and shape examples')


if __name__=='__main__':check()
