"""生成逐时钟跟踪向量；独立断言先约束运动、干扰、失联和边界语义。"""
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python' if (ROOT/'python').is_dir() else ROOT/'python_sim'))
from pipeline import Config, Detection, TargetTracker


def ball(x, y=350, color=1, width=40, height=40, area=900):
    return Detection((x-width//2, y-height//2, x+(width-1)//2, y+(height-1)//2), color, area)


def main():
    cfg = Config()
    tracker = TargetTracker(cfg)
    rows = []
    frames = 0

    def row(inputs):
        target = tracker.target
        outputs = [int(target is not None), ['SEARCH', 'CONFIRM', 'TRACK', 'LOST'].index(tracker.state)]
        outputs += [target.color, *target.box, *target.center] if target else [0]*7
        rows.append(' '.join(map(str, [*inputs, *outputs])))

    def run(candidates=(), clear=False, overflow=False):
        nonlocal frames
        if clear:
            tracker.reset()
            row([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for detection in candidates:
            x0, y0, x1, y1 = detection.box
            row([0, 0, 1, 0, 0, detection.color, detection.area, x0, x1, y0, y1])
        if overflow:
            tracker.reset()
        else:
            tracker.update(candidates)
        row([0, 0, 0, 1, int(overflow), 0, 0, 0, 0, 0, 0])
        row([0]*11)
        frames += 1

    # 每帧80像素已超过旧64像素关联窗，确认后应持续跟随。
    for index, x in enumerate((200, 280, 360, 440, 520)):
        run([ball(x)], clear=index == 0)
        assert tracker.state == ('CONFIRM' if index == 0 else 'TRACK')
        assert tracker.target.center[0] == x-1+(80 if index else 0)
    # 异色近邻、同色巨框即使更大且更近，也不能抢走轨迹；顺序不得影响结果。
    for x, reverse in ((600, False), (680, True)):
        candidates = [ball(x-80, area=5000), ball(x, color=3, area=20000),
                      ball(x, width=140, height=140, area=15000), ball(x)]
        run(list(reversed(candidates)) if reverse else candidates)
        assert tracker.observed == ball(x) and tracker.state == 'TRACK'
    frozen = tracker.target
    run([])
    assert tracker.state == 'LOST' and tracker.target == frozen
    run([])
    assert tracker.state == 'LOST' and tracker.target == frozen
    run([ball(920)])
    assert tracker.state == 'TRACK' and tracker.velocity == (80, 0)
    run([ball(1000)])
    assert tracker.target.center[0] == 1079
    # 停球后清除速度；4像素量化抖动不应产生预测位移。
    run([ball(1000)])
    assert tracker.velocity == (0, 0) and tracker.target.center[0] == 999
    run([ball(1004)])
    assert tracker.velocity == (0, 0)
    run([], overflow=True)
    assert tracker.state == 'SEARCH' and tracker.velocity == (0, 0)
    # 两轴负速度、ROI四侧平移限幅保持框的宽高。
    for x, y in ((300, 350), (220, 290), (140, 230), (84, 180)):
        run([ball(x, y)], clear=(x == 300))
    assert tracker.target.box[0] == 64 and tracker.target.box[1] == 160
    assert tracker.target.box[2]-tracker.target.box[0]+1 == 40
    for x, y in ((1000, 500), (1080, 560), (1160, 620)):
        run([ball(x, y)], clear=(x == 1000))
    assert tracker.target.box[2] == 1215 and tracker.target.box[3] == 639
    # 只有异色时不能改色续接；第三帧失联回搜索，随后可重新锁定绿球。
    run([ball(1160, 620, color=3)])
    assert tracker.state == 'LOST' and tracker.color == 1
    run([])
    run([])
    assert tracker.state == 'SEARCH'
    run([ball(500, color=3)])
    run([ball(510, color=3)])
    assert tracker.state == 'TRACK' and tracker.color == 3
    # 固定随机种子，覆盖方向变化、尺寸变化、空帧、候选顺序和重置。
    rng = random.Random(20261019)
    x, y = 500, 350
    for index in range(180):
        x = max(100, min(1150, x+rng.randint(-95, 95)))
        y = max(190, min(610, y+rng.randint(-35, 35)))
        candidate = ball(x, y, width=rng.choice((32, 40, 48)), height=40)
        candidates = [ball(x, y, color=2), candidate]
        rng.shuffle(candidates)
        run([] if index % 17 == 0 else candidates, clear=index % 53 == 0)
    (ROOT/'sim/motion_vectors.txt').write_text('\n'.join(rows)+'\n', encoding='ascii')
    result = {'frames': frames, 'cycles': len(rows), 'model_assertions': 'passed',
              'scope': 'association, one-frame display forecast, dropout freeze, ROI clamp, overflow/clear'}
    (ROOT/'reports/motion_model.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
