"""运行小球Python工程：demo、摄像头或本地视频都进入同一处理通路。"""

import argparse
import csv
import json
from pathlib import Path
import time

import cv2
import numpy as np

from pipeline import COLORS, NAMES, Pipeline, text
from scenes import demo_frame


def save_png(path, rgb):
    ok, encoded = cv2.imencode('.png', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    if not ok:
        raise RuntimeError('PNG编码失败')
    encoded.tofile(str(path))


def components_image(engine, stats):
    cfg = engine.cfg
    image = np.full((cfg.height, cfg.width, 3), (15, 23, 35), np.uint8)
    cells = engine.components.banks[1-engine.components.write_bank] >> 5
    palette = np.array([(15, 23, 35), COLORS[1], COLORS[2], COLORS[3]], np.uint8)
    painted = np.repeat(np.repeat(palette[cells], 4, axis=0), 4, axis=1)
    ox, oy = engine.components.origin
    h, w = min(painted.shape[0], cfg.height-oy), min(painted.shape[1], cfg.width-ox)
    image[oy:oy+h, ox:ox+w] = painted[:h, :w]
    text(image, '4x4 COLOR SUPPORT -> SAME-COLOR 2D REGIONS', (24, 28), scale=0.65)
    for candidate in stats.candidates:
        left, top, right, bottom = candidate.box
        cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 255), 1)
    return image


def save_stages(folder, source, stats, output, engine):
    folder.mkdir(parents=True, exist_ok=True)
    palette = np.array([(12, 18, 25), COLORS[1], COLORS[2], COLORS[3]], np.uint8)
    mask_rgb = palette[stats.mask]
    for name, image in (('01_input.png', source), ('02_mask.png', mask_rgb),
                        ('03_components.png', components_image(engine, stats)), ('04_hdmi_output.png', output)):
        save_png(folder/name, image)
    panels = []
    for title, image in (('ACTUAL INPUT RGB', source), ('COLOR MASK FROM PIXELS', mask_rgb),
                         ('2D COLOR REGIONS / CANDIDATES', components_image(engine, stats)),
                         ('BUFFERED DISPLAY OUTPUT', output)):
        panel = np.full((360, 640, 3), (8, 15, 24), np.uint8)
        scale = min(640/image.shape[1], 324/image.shape[0])
        resized = cv2.resize(image, (round(image.shape[1]*scale), round(image.shape[0]*scale)))
        top, left = 36+(324-resized.shape[0])//2, (640-resized.shape[1])//2
        panel[top:top+resized.shape[0], left:left+resized.shape[1]] = resized
        text(panel, title, (16, 24), scale=0.48)
        panels.append(panel)
    save_png(folder/'pipeline_overview.png', np.vstack((np.hstack(panels[:2]), np.hstack(panels[2:]))))


def run(args, mode):
    output_dir = Path(args.output)/mode
    output_dir.mkdir(parents=True, exist_ok=True)
    engine = Pipeline(mode=mode)
    cfg = engine.cfg
    capture = None
    frames = args.frames or (240 if mode == 'track' else 360)
    if args.source != 'demo':
        source = int(args.source) if args.source.isdecimal() else args.source
        capture = cv2.VideoCapture(source)
        if not capture.isOpened():
            raise RuntimeError(f'不能打开输入源：{args.source}')
    writer = None
    if args.record or args.headless:
        writer = cv2.VideoWriter(str(output_dir/'simulation.mp4'), cv2.VideoWriter_fourcc(*'mp4v'),
                                 24, (cfg.width, cfg.height))
        if not writer.isOpened():
            if capture is not None:
                capture.release()
            raise RuntimeError('视频编码器未能打开')
    log_file = (output_dir/'frame_trace.csv').open('w', newline='', encoding='utf-8-sig')
    log = csv.writer(log_file)
    log.writerow(('input_frame', 'config_epoch', 'mode', 'candidate_count', 'candidate_centers',
                  'tracker_state', 'gate_state', 'empty_frames', 'red', 'green', 'yellow', 'total',
                  'count_event', 'reason', 'display_input_frame', 'display_result_frame', 'ddr_words'))
    start = time.perf_counter()
    events = []
    max_candidates = processed = 0
    mask_view = paused = False
    last_output = None
    window = 'Ball vision - Python functional engineering simulation'
    if not args.headless:
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window, 1280, 720)
    try:
        while processed < frames or (not args.headless and args.frames == 0):
            tick = time.perf_counter()
            if not paused:
                if capture is None:
                    rgb = demo_frame(engine.mode, processed if args.headless else processed % (240 if engine.mode == 'track' else 360))
                else:
                    ok, bgr = capture.read()
                    if not ok:
                        break
                    rgb = cv2.cvtColor(cv2.resize(bgr, (cfg.width, cfg.height)), cv2.COLOR_BGR2RGB)
                last_output, stats, snapshot, shown, words = engine.process(rgb, mask_view)
                counts = dict(zip((1, 2, 3), snapshot.counts))
                if snapshot.event:
                    events.append({'frame': snapshot.frame_id, 'color': NAMES[snapshot.event], 'total': sum(snapshot.counts)})
                max_candidates = max(max_candidates, len(stats.candidates))
                log.writerow((stats.frame_id, stats.epoch, engine.mode, len(stats.candidates),
                              json.dumps([d.center for d in stats.candidates]), snapshot.tracker_state,
                              snapshot.gate_state, snapshot.empty, counts[1], counts[3], counts[2],
                              sum(snapshot.counts), NAMES[snapshot.event] if snapshot.event else '', snapshot.reason,
                              shown[0] if shown else '', shown[1].frame_id if shown and shown[1] else '', words))
                if processed == (110 if mode == 'count' else 120):
                    save_stages(output_dir, rgb, stats, last_output, engine)
                if writer is not None:
                    writer.write(cv2.cvtColor(last_output, cv2.COLOR_RGB2BGR))
                processed += 1
                if args.headless and processed % 80 == 0:
                    print(f'{mode}: frame {processed}/{frames}, counts={counts}, gate={snapshot.gate_state}', flush=True)
            if not args.headless:
                if last_output is not None:
                    cv2.imshow(window, cv2.cvtColor(last_output, cv2.COLOR_RGB2BGR))
                delay = max(1, round(1000/24-(time.perf_counter()-tick)*1000))
                key = cv2.waitKey(delay) & 255
                if key in (27, ord('q')) or cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
                    break
                if key == ord(' '):
                    paused = not paused
                elif key == ord('m'):
                    mask_view = not mask_view
                elif key == ord('t'):
                    engine.configure(strict=not engine.cfg.strict)
                elif key == ord('c'):
                    engine.configure(clear=True)
                elif key in (ord('1'), ord('2')):
                    engine.configure(mode='track' if key == ord('1') else 'count')
            elif processed >= frames:
                break
    finally:
        log_file.close()
        if writer is not None:
            writer.release()
        if capture is not None:
            capture.release()
        if not args.headless:
            cv2.destroyAllWindows()
    if processed == 0:
        raise RuntimeError('输入源未提供任何有效帧')
    save_png(output_dir/'last_frame.png', last_output)
    summary = {'model': 'frame-functional; not RTL cycle/timing simulation', 'source': args.source,
               'mode': mode, 'frames': processed, 'elapsed_seconds': round(time.perf_counter()-start, 3),
               'max_simultaneous_candidates': max_candidates,
               'counts': {NAMES[c]: n for c, n in engine.counter.counts.items()},
               'total': sum(engine.counter.counts.values()), 'events': events,
               'rgb96_groups_per_frame': cfg.width*cfg.height//4,
               'ddr128_words_per_frame': cfg.width*cfg.height*3//16,
               'algorithm_result_delay_frames': 1, 'framebuffer_delay_frames': 1,
               'detector': '4x4 same-color four-connected regions',
               'hardware_dense_scene_extra_frame_possible': True}
    if args.source == 'demo' and mode == 'count' and args.headless and processed == 360:
        if summary['counts'] != {'RED': 2, 'YELLOW': 2, 'GREEN': 2}:
            raise AssertionError(f'流水线演示计数与输入真值不一致：{summary}')
        if max_candidates < 2:
            raise AssertionError('未验证多球同时入镜')
        summary['expected_demo_counts_match'] = True
    (output_dir/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='demo', help='demo、摄像头编号（如0）或本地视频路径')
    parser.add_argument('--mode', choices=('track', 'count', 'both'), default='count')
    parser.add_argument('--headless', action='store_true', help='不打开窗口，执行有限帧并保存结果')
    parser.add_argument('--frames', type=int, default=0, help='0使用内置场景默认长度')
    parser.add_argument('--record', action='store_true', help='交互模式也录制输出')
    parser.add_argument('--output', default=str(Path(__file__).parent/'output'))
    args = parser.parse_args()
    if args.frames < 0:
        parser.error('frames不能为负')
    if args.mode == 'both' and (not args.headless or args.source != 'demo'):
        parser.error('both仅用于headless demo批量仿真')
    for mode in ('track', 'count') if args.mode == 'both' else (args.mode,):
        run(args, mode)


if __name__ == '__main__':
    main()
