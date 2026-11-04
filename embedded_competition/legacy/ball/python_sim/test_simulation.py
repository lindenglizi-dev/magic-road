"""无额外测试框架；从RGB像素验证模块逻辑及完整软件通路。"""

from dataclasses import replace
import json
from pathlib import Path
import time

import numpy as np

from pipeline import Config, Pipeline, segment
from scenes import draw_ball
from video_io import DDRFrameBuffer, FourPixelInput, RGB96Packer, pack_frame


CFG = Config(width=160, height=96, roi=(0, 0, 160, 96), gate=(56, 0, 104, 96),
             line=80, hysteresis=4, min_area=16, min_size=3, max_size=64, max_move=12)


def frame(balls=(), cfg=CFG):
    rgb = np.full((cfg.height, cfg.width, 3), 24, np.uint8)
    for x, y, color, radius in balls:
        draw_ball(rgb, x, y, color, radius)
    return rgb


def feed(engine, balls=(), repeat=1):
    for _ in range(repeat):
        stats = engine.analyse(frame(balls, engine.cfg))
        assert engine.accept(stats)
    return engine.snapshot


def ready(engine):
    feed(engine, repeat=3)
    assert engine.counter.state == 'READY'


def pass_ball(engine, color):
    feed(engine, ((65, 48, color, 8),), 2)
    assert engine.counter.state == 'ARMED'
    feed(engine, ((87, 48, color, 8),))
    assert engine.counter.state == 'HOLD'


def test_classifier_and_roi():
    cfg = replace(CFG, roi=(3, 2, 157, 94), gate=(56, 2, 104, 94))
    rgb = frame(cfg=cfg)
    colors = ((255, 0, 0), (255, 255, 0), (0, 255, 0), (255, 255, 255),
              (128, 128, 128), (0, 0, 255), (120, 0, 0), (0, 0, 0))
    for index, color in enumerate(colors):
        rgb[10, 8+index*4:12+index*4] = color
    rgb[10, 0:3] = (255, 0, 0)
    mask = segment(rgb, cfg)
    assert mask[10, 8:40:4].tolist() == [1, 2, 3, 0, 0, 0, 1, 0]
    assert not mask[:, :3].any() and not mask[:, 157:].any()
    assert segment(rgb, replace(cfg, strict=True))[10, 32] == 0


def test_component_banks_and_tail():
    cfg = replace(CFG, min_area=4, min_size=1)
    engine = Pipeline(cfg)
    rgb = frame(((28, 38, 1, 8), (82, 52, 1, 9)), cfg)
    rgb[28:40, 148:160] = (0, 255, 0)
    stats = engine.analyse(rgb)
    assert len(stats.candidates) == 3
    reds = sorted((d for d in stats.candidates if d.color == 1), key=lambda d: d.center)
    assert len(reds) == 2
    # 单元边界有最多3像素量化，中心仍应落在此范围。
    assert max(abs(a-b) for a, b in zip(reds[0].center, (28, 38))) <= 3
    assert max(abs(a-b) for a, b in zip(reds[1].center, (82, 52))) <= 3
    assert next(d for d in stats.candidates if d.color == 3).box[2] == 159
    # 用逐像素直方图核对实际存储字，不调用捕获器的批量公式。
    bank = engine.components.banks[0]
    for y in range(bank.shape[0]):
        for x in range(bank.shape[1]):
            labels = stats.mask[y*4:y*4+4, x*4:x*4+4]
            counts = [sum(int(value) == color for value in labels.flat) for color in (1, 2, 3)]
            area = max(counts)
            expected = ((counts.index(area)+1) << 5) | area if area >= 4 and area*4 >= sum(counts)*3 else 0
            assert int(bank[y, x]) == expected
    empty_stats = engine.analyse(frame(cfg=cfg))
    assert not empty_stats.candidates
    assert engine.components.tags == [(0, 0), (1, 0)]


def test_tracker_lost_and_reacquire():
    engine = Pipeline(CFG, 'track')
    assert feed(engine, ((30, 40, 1, 8),)).tracker_state == 'CONFIRM'
    assert feed(engine, ((35, 43, 1, 8),)).tracker_state == 'TRACK'
    assert feed(engine).tracker_state == 'LOST'
    assert feed(engine).tracker_state == 'LOST'
    assert feed(engine, ((42, 44, 1, 8),)).tracker_state == 'TRACK'
    assert feed(engine, repeat=3).tracker_state == 'SEARCH'
    assert feed(engine, ((110, 40, 3, 8),), 2).tracker_state == 'TRACK'


def test_pause_dropout_same_color_and_totals():
    engine = Pipeline(CFG)
    ready(engine)
    feed(engine, ((65, 48, 1, 8),), 100)
    assert sum(engine.counter.counts.values()) == 0
    feed(engine, repeat=2)
    assert engine.counter.state == 'ARMED'
    feed(engine, ((87, 48, 1, 8),))
    assert engine.counter.counts[1] == 1
    feed(engine, ((87, 48, 1, 8),), 100)
    feed(engine, repeat=2)
    feed(engine, ((87, 48, 1, 8),), 10)
    assert engine.counter.counts[1] == 1
    ready(engine)
    pass_ball(engine, 1)
    ready(engine)
    pass_ball(engine, 3)
    ready(engine)
    pass_ball(engine, 2)
    assert engine.counter.counts == {1: 2, 2: 1, 3: 1}
    assert sum(engine.counter.counts.values()) == 4


def test_simultaneous_same_color():
    engine = Pipeline(CFG)
    ready(engine)
    feed(engine, ((65, 48, 1, 8), (20, 48, 1, 8)), 2)
    assert len(engine.snapshot.candidates) == 2
    feed(engine, ((87, 48, 1, 8), (20, 48, 1, 8)))
    # 全画面仍有红球；只有计数门清空，必须允许下一颗。
    feed(engine, ((20, 48, 1, 8),), 3)
    assert engine.counter.state == 'READY'
    feed(engine, ((135, 48, 1, 8), (65, 48, 1, 8)), 2)
    feed(engine, ((135, 48, 1, 8), (87, 48, 1, 8)))
    assert engine.counter.counts[1] == 2


def test_downstream_reverse_jitter_and_clear():
    engine = Pipeline(CFG)
    ready(engine)
    feed(engine, ((87, 48, 1, 8),), 2)
    assert engine.counter.state == 'BLOCKED' and sum(engine.counter.counts.values()) == 0
    feed(engine, ((65, 48, 1, 8),), 2)
    assert sum(engine.counter.counts.values()) == 0
    ready(engine)
    feed(engine, ((65, 48, 1, 8),), 2)
    for x in (77, 81, 79, 83, 78):
        feed(engine, ((x, 48, 1, 8),))
    assert sum(engine.counter.counts.values()) == 0
    feed(engine, ((87, 48, 1, 8),))
    assert engine.counter.counts[1] == 1
    engine.configure(clear=True)
    feed(engine, ((87, 48, 1, 8),), 4)
    assert engine.counter.state == 'WAIT_CLEAR' and engine.counter.counts[1] == 0
    ready(engine)
    pass_ball(engine, 1)
    assert engine.counter.counts[1] == 1


def test_short_gap_multi_ball_and_overflow():
    engine = Pipeline(CFG)
    ready(engine)
    pass_ball(engine, 1)
    feed(engine, repeat=2)
    feed(engine, ((65, 48, 1, 8),), 2)
    assert engine.counter.state == 'BLOCKED' and engine.counter.counts[1] == 1
    ready(engine)
    feed(engine, ((63, 48, 1, 6), (97, 48, 3, 6)))
    assert engine.counter.state == 'BLOCKED' and 'MULTIPLE' in engine.counter.reason
    wide = Config(width=320, height=96, roi=(0, 0, 320, 96), gate=(136, 0, 184, 96),
                  line=160, hysteresis=4, min_area=8, min_size=2, max_size=40)
    other = Pipeline(wide)
    stats = other.analyse(frame(tuple((16+i*32, 48, 1, 5) for i in range(9)), wide))
    assert stats.overflow and len(stats.candidates) == 8
    other.accept(stats)
    assert other.counter.state == 'BLOCKED'


def test_epoch_and_repeated_result():
    engine = Pipeline(CFG)
    ready(engine)
    old_stats = engine.analyse(frame(((65, 48, 1, 8),)))
    engine.configure(strict=True)
    assert not engine.accept(old_stats)
    assert engine.counter.state == 'WAIT_CLEAR'
    assert engine.counter.empty == 0
    stats = engine.analyse(frame())
    assert engine.accept(stats) and not engine.accept(stats)
    assert engine.counter.empty == 1


def test_packer_valid_gaps_and_markers():
    width, height = 32, 4
    rgb = np.arange(width*height*3, dtype=np.uint16).astype(np.uint8).reshape(height, width, 3)
    source, packer = FourPixelInput(width, height), RGB96Packer()
    assert source.step(early=True) is None
    assert source.step() is None
    words, eols, eofs, starts = [], 0, 0, 0
    groups = rgb.reshape(-1, 12)
    for index, group in enumerate(groups):
        if index % 3 == 1:
            x, y = source.x, source.y
            assert source.step() is None and (x, y) == (source.x, source.y)
            assert packer.step() is None
        data, x, y, sof, eol, eof = source.step(group.tobytes())
        assert (x, y) == ((index % (width//4))*4, index//(width//4))
        starts += int(sof)
        result = packer.step(data, sof, eol, eof)
        if result is not None:
            word, last, done = result
            words.append(word)
            eols += int(last)
            eofs += int(done)
    assert b''.join(words) == rgb.tobytes()
    assert starts == 1 and eols == height and eofs == 1
    assert not source.active and not packer.pending
    assert pack_frame(rgb).tobytes() == b''.join(words)
    first = int.from_bytes(groups[0].tobytes(), 'big')
    assert (first >> 72).to_bytes(3, 'big') == rgb[0, 0].tobytes()


def test_full_frame_ddr_and_invalid_input():
    rng = np.random.default_rng(7)
    rgb = rng.integers(0, 256, (720, 1280, 3), np.uint8)
    words = pack_frame(rgb)
    assert words.shape == (172800, 16)
    assert np.array_equal(words.reshape(rgb.shape), rgb)
    buffer = DDRFrameBuffer()
    first, meta, count = buffer.exchange(rgb, 'frame0')
    assert not first.any() and meta is None and count == 172800
    second, meta, _ = buffer.exchange(np.zeros_like(rgb), 'frame1')
    assert np.array_equal(second, rgb) and meta == 'frame0'
    engine = Pipeline(CFG)
    try:
        engine.analyse(np.zeros((95, 160, 3), np.uint8))
    except ValueError:
        pass
    else:
        raise AssertionError('不完整输入帧未被拒绝')
    assert engine.frame_id == -1 and engine.counter.empty == 0


def test_saturation_and_sum():
    engine = Pipeline(CFG)
    engine.counter.counts = {1: (1 << 32)-1, 2: (1 << 32)-1, 3: (1 << 32)-1}
    ready(engine)
    pass_ball(engine, 1)
    assert engine.counter.counts[1] == (1 << 32)-1
    assert sum(engine.counter.counts.values()) == 3*((1 << 32)-1)
    assert engine.counter.reason == 'COUNTER SATURATED'


def main():
    start = time.perf_counter()
    results = []
    for name, check in sorted(globals().copy().items()):
        if name.startswith('test_') and callable(check):
            check()
            results.append(name)
            print(f'PASS {name}', flush=True)
    report = {'passed': len(results), 'failed': 0, 'checks': results,
              'elapsed_seconds': round(time.perf_counter()-start, 3),
              'scope': 'Python functional model only; no RTL simulation or hardware timing evidence'}
    folder = Path(__file__).parent/'output'
    folder.mkdir(exist_ok=True)
    (folder/'test_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
