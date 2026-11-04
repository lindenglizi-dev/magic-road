"""复现背景碎片导致ERR2无法恢复，并生成真实二维区域→计数器逐帧期望。"""
import json
from pathlib import Path
import sys

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python' if (ROOT/'python').exists() else ROOT/'python_sim'))
from pipeline import ComponentRAM, Config, GateCounter


def main():
    cfg = Config(width=320,height=128,roi=(0,0,320,128),gate=(136,0,184,128),line=160,hysteresis=4)
    store, counter = ComponentRAM(cfg), GateCounter(cfg)
    masks, headers, trace = [], [], []
    def scene(kind, color=1):
        mask=np.zeros((128,320),np.uint8)
        if kind == 'noise':
            for y in (8,24,40,56):
                for x in (140,164):
                    mask[y:y+4,x:x+4]=1
        if kind == 'up': mask[80:92,144:156]=color
        if kind == 'down': mask[80:92,164:176]=color
        if kind == 'multi':
            mask[80:92,140:152]=1;mask[80:92,168:180]=2
        if kind == 'rejected': mask[40:44,136:184]=color
        if kind == 'overflow':
            mask[80:92,164:176]=color
            for x in (0,32,64,96,208,240,272,304): mask[16:28,x:x+12]=1
        return mask
    def run(kind,color=1,expected=None):
        index=len(masks);mask=scene(kind,color)
        stats=store.scan(store.capture(mask,index,0),mask)
        # 这些向量由完整4x4块构成，逐像素OpenCV连通域是独立的占用判据。
        occupied=False
        for c in (1,2,3):
            count,labels,regions,_=cv2.connectedComponentsWithStats((mask==c).astype(np.uint8),connectivity=4)
            for x,y,w,h,area in regions[1:]:
                occupied |= bool(area>=cfg.min_area and x<184 and x+w>136)
        assert stats.gate_region_occupied == occupied,(index,kind)
        counter.update(stats)
        if expected: assert counter.state==expected,(index,kind,counter.state,expected)
        reason={'':0,'MULTIPLE BALLS IN GATE':2,'COLOR MISMATCH OR REVERSE MOTION':4,'CANDIDATE OVERFLOW':1}.get(counter.reason,0)
        headers.append(f'{stats.raw_gate_pixels} {int(occupied)} {len(stats.candidates)} {int(stats.overflow)} '
                       f'{["WAIT_CLEAR","READY","ARMED","HOLD","BLOCKED"].index(counter.state)} {reason} '
                       f'{counter.counts[1]} {counter.counts[3]} {counter.counts[2]}')
        masks.append(mask)
        trace.append(dict(frame=index,scene=kind,color=color,raw=stats.raw_gate_pixels,occupied=occupied,
                          candidates=len(stats.candidates),state=counter.state,reason=counter.reason,counts=counter.counts.copy()))
    for _ in range(3):run('empty')
    assert counter.state=='READY'
    run('multi',expected='BLOCKED')
    for _ in range(3):run('noise')
    assert counter.state=='READY'
    run('up');run('up',expected='ARMED')
    for _ in range(3):run('rejected',expected='ARMED')
    run('down',expected='HOLD')
    for _ in range(5):run('down',expected='HOLD')
    assert counter.counts[1]==1
    run('empty',expected='HOLD');run('empty',expected='HOLD');run('down',expected='HOLD')
    assert counter.counts[1]==1
    for _ in range(3):run('noise')
    run('up');run('up',expected='ARMED');run('down',expected='HOLD')
    assert counter.counts[1]==2
    for _ in range(3):run('noise')
    run('up',3);run('up',3,expected='ARMED');run('down',2,expected='BLOCKED')
    assert counter.counts[3]==0 and counter.counts[2]==0
    for _ in range(3):run('noise')
    run('up',3);run('up',3,expected='ARMED');run('overflow',3,expected='BLOCKED')
    assert counter.counts[3]==0
    for _ in range(3):run('noise')
    run('up',3);run('up',3,expected='ARMED');run('down',3,expected='HOLD')
    assert counter.counts=={1:2,2:0,3:1}
    with (ROOT/'sim/gate_recovery_frames.hex').open('w',encoding='ascii') as output:
        for mask in masks:
            words=(mask.reshape(-1,4).astype(np.uint16)*np.array([1,4,16,64])).sum(axis=1)
            output.writelines(f'{int(word):02x}\n' for word in words)
    (ROOT/'sim/gate_recovery_headers.txt').write_text('\n'.join(headers)+'\n',encoding='ascii')
    report={'frames':len(masks),'input_words':len(masks)*10240,'passed':True,'counts':counter.counts,'trace':trace}
    (ROOT/'reports/gate_recovery_model.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS gate recovery model:',len(masks),'frames; sparse128px releases, rejected192px holds, red2/green1/yellow0')


if __name__ == '__main__':main()
