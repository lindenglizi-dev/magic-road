"""Integer Haar model. Bulk NumPy evaluates the same scalar windows, not RTL clocks."""
from pathlib import Path
import hashlib
import json
import math
import xml.etree.ElementTree as ET

import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'python_face'
if not BASE.is_dir():
    BASE = Path('E:/project/ball/python_face')
XML = BASE/'assets/haarcascade_frontalface_default.xml'
C = json.loads((ROOT/'contract.json').read_text(encoding='utf-8'))
SCHEDULE = C['cycle_schedule']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quantize(values, fraction, bits):
    values = np.asarray(values, np.float64)
    result = (np.sign(values)*np.floor(np.abs(values)*(1 << fraction)+0.5)).astype(np.int64)
    if np.any(result < -(1 << (bits-1))) or np.any(result >= 1 << (bits-1)):
        raise ValueError(f'Parameter exceeds signed {bits}-bit Q{fraction}')
    return result


def float_model():
    if sha(XML) != C['source_model_sha256']:
        raise ValueError('Source model differs from the frozen classifier')
    cascade = ET.parse(XML).getroot().find('cascade')
    if (cascade.findtext('featureType') != 'HAAR' or cascade.findtext('width') != '24'
            or cascade.findtext('height') != '24'):
        raise ValueError('Only the frozen 24x24 upright Haar stump model is supported')
    features = []
    for node in cascade.find('features'):
        rects = [list(map(float, r.text.split())) for r in node.find('rects')]
        if int(node.findtext('tilted', '0')):
            raise ValueError('Tilted Haar feature is unsupported')
        features.append(rects)
    rects, modes, thresholds, leaves, counts, stages = [], [], [], [], [], []
    for stage in cascade.find('stages'):
        weak = list(stage.find('weakClassifiers'))
        counts.append(len(weak))
        stages.append(np.float32(np.float32(stage.findtext('stageThreshold'))-np.float32(1e-5)))
        for node in weak:
            values = list(map(float, node.findtext('internalNodes').split()))
            if len(values) != 4 or values[:2] != [0, -1] or int(values[2]) != len(rects):
                raise ValueError('Unexpected tree structure or feature order')
            feature = features[int(values[2])]
            weights = [int(r[4]) for r in feature] + [0]*(3-len(feature))
            mode = C['rect_weight_modes'].index(weights)
            packed = [list(map(int, r[:4])) for r in feature]+[[0]*4]*(3-len(feature))
            if any(x < 0 or y < 0 or x+w > 24 or y+h > 24 for x, y, w, h in packed):
                raise ValueError('Invalid feature rectangle')
            rects.append(packed)
            modes.append(mode)
            thresholds.append(np.float32(values[3]))
            leaves.append(list(map(np.float32, node.findtext('leafValues').split())))
    if len(rects) != 2913 or len(counts) != 25 or len(features) != 2913:
        raise ValueError('Model inventory differs from the frozen design')
    return {'rects': np.array(rects, np.int64), 'modes': np.array(modes, np.int64),
            'nodes': np.array(thresholds, np.float32), 'leaves': np.array(leaves, np.float32),
            'counts': np.array(counts, np.int64), 'stages': np.array(stages, np.float32)}


def export_rom():
    model = float_model()
    folder = ROOT/'rom'
    folder.mkdir(exist_ok=True)
    nodes = quantize(model['nodes'], 14, 16)
    leaves = quantize(model['leaves'], 12, 18)
    stages = quantize(model['stages'], 12, 18)
    words = []
    for i, rects in enumerate(model['rects']):
        word = 0
        for r, rect in enumerate(rects):
            for field, value in enumerate(rect):
                word |= int(value) << (r*20+field*5)
        word |= int(model['modes'][i]) << 60
        word |= (int(nodes[i]) & 0xffff) << 62
        word |= (int(leaves[i, 0]) & 0x3ffff) << 78
        word |= (int(leaves[i, 1]) & 0x3ffff) << 96
        words.append(f'{word:030x}')
    (folder/'stumps.mem').write_text('\n'.join(words)+'\n', encoding='ascii')
    (folder/'stages.mem').write_text(''.join(f'{int(count) | ((int(q)&0x3ffff)<<8):010x}\n'
                                            for count, q in zip(model['counts'], stages)), encoding='ascii')
    xml_text = XML.read_text(encoding='utf-8')
    (folder/'LICENSE_OpenCV.txt').write_text(xml_text.split('<!--', 1)[1].split('-->', 1)[0], encoding='utf-8')
    manifest = {'source_xml': str(XML), 'source_sha256': sha(XML), 'contract_sha256': sha(ROOT/'contract.json'),
                'stumps': 2913, 'stages': 25, 'rectangles': 6383,
                'stump_rom_sha256': sha(folder/'stumps.mem'), 'stage_rom_sha256': sha(folder/'stages.mem'),
                'parameter_error_max': {
                    'node': float(np.max(np.abs(model['nodes'].astype(float)-nodes/16384))),
                    'leaf': float(np.max(np.abs(model['leaves'].astype(float)-leaves/4096))),
                    'stage': float(np.max(np.abs(model['stages'].astype(float)-stages/4096)))}}
    (folder/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


def signed(value, bits):
    return value-(1 << bits) if value & (1 << (bits-1)) else value


def load_rom():
    folder = ROOT/'rom'
    manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if (sha(ROOT/'contract.json') != manifest['contract_sha256'] or
        sha(folder/'stumps.mem') != manifest['stump_rom_sha256'] or
        sha(folder/'stages.mem') != manifest['stage_rom_sha256']):
        raise ValueError('Contract or ROM hash mismatch; explicitly regenerate the ROM')
    rects, modes, nodes, leaves = [], [], [], []
    for line in (folder/'stumps.mem').read_text(encoding='ascii').splitlines():
        word = int(line, 16)
        if word >> 114 or ((word >> 60) & 3) == 3:
            raise ValueError('Invalid reserved bits or rectangle mode')
        rects.append([[(word >> (r*20+f*5)) & 31 for f in range(4)] for r in range(3)])
        modes.append((word >> 60) & 3)
        nodes.append(signed((word >> 62) & 65535, 16))
        leaves.append([signed((word >> 78) & 262143, 18), signed((word >> 96) & 262143, 18)])
    counts, stages = [], []
    for line in (folder/'stages.mem').read_text(encoding='ascii').splitlines():
        word = int(line, 16)
        if word >> 26 or not 1 <= (word & 255) <= 211:
            raise ValueError('Invalid stage word')
        counts.append(word & 255)
        stages.append(signed((word >> 8) & 262143, 18))
    if len(rects) != 2913 or len(stages) != 25 or sum(counts) != 2913:
        raise ValueError('Invalid ROM dimensions')
    return {name: np.array(values, np.int64) for name, values in
            (('rects', rects), ('modes', modes), ('nodes', nodes), ('leaves', leaves), ('counts', counts), ('stages', stages))}


def gray_roi(rgb):
    if rgb.dtype != np.uint8 or rgb.shape != (720, 1280, 3):
        raise ValueError('Expected 1280x720 uint8 RGB')
    blocks = rgb[232:488, 512:768].astype(np.int64).reshape(64, 4, 64, 4, 3).sum(axis=(1, 3))
    return ((blocks @ np.array((77, 150, 29)) + 2048) >> 12).astype(np.uint8)


def resize_gray(gray, size):
    if gray.shape != (64, 64) or gray.dtype != np.uint8 or size not in C['pyramid_sizes']:
        raise ValueError('Unexpected pyramid input')
    if size == 64:
        return gray.copy()
    coord = np.clip(((2*np.arange(size)+1)*64*128)//size-128, 0, 63*256)
    low, frac = coord >> 8, coord & 255
    high = np.minimum(low+1, 63)
    source = gray.astype(np.int64)
    upper = source[low[:, None], low]*(256-frac)+source[low[:, None], high]*frac
    lower = source[high[:, None], low]*(256-frac)+source[high[:, None], high]*frac
    return ((upper*(256-frac[:, None])+lower*frac[:, None]+32768) >> 16).astype(np.uint8)


def integral(gray):
    result = np.zeros((gray.shape[0]+1, gray.shape[1]+1), np.int64)
    result[1:, 1:] = gray.cumsum(0, dtype=np.int64).cumsum(1, dtype=np.int64)
    if result.max() >= 1 << 20:
        raise OverflowError('Integral image exceeds 20 bits')
    return result


def rectangle(sat, x, y, rect):
    rx, ry, width, height = rect
    left, top = x+rx, y+ry
    return sat[top, left]+sat[top+height, left+width]-sat[top, left+width]-sat[top+height, left]


def floor_sqrt(value):
    if value < 0 or value >= 1 << 34:
        raise OverflowError('Variance input exceeds 34 bits')
    root = remainder = 0
    for shift in range(32, -1, -2):
        remainder = (remainder << 2) | ((value >> shift) & 3)
        trial = (root << 2) | 1
        root <<= 1
        if remainder >= trial:
            remainder -= trial
            root |= 1
    return root


def mapped_box(x, y, size):
    # Half-open x,y,w,h. Positive half ties round up, including scale mapping.
    return ((2*x*256+size)//(2*size), (2*y*256+size)//(2*size),
            (2*24*256+size)//(2*size), (2*24*256+size)//(2*size))


def group_boxes(boxes):
    if len(boxes) > C['raw_candidate_capacity']:
        return (), True, 0
    parent = list(range(len(boxes)))
    cycles = 0

    def find(i):
        nonlocal cycles
        while parent[i] != i:
            i = parent[i]
            cycles += SCHEDULE['group_find_parent_hop']
        return i

    for i, a in enumerate(boxes):
        for j in range(i):
            b = boxes[j]
            delta = min(a[2], b[2])+min(a[3], b[3])
            cycles += SCHEDULE['group_pair']
            if all(10*abs(p-q) <= delta for p, q in zip(
                    (a[0], a[1], a[0]+a[2], a[1]+a[3]),
                    (b[0], b[1], b[0]+b[2], b[1]+b[3]))):
                p, q = find(i), find(j)
                if p != q:
                    parent[max(p, q)] = min(p, q)
                    cycles += SCHEDULE['group_union']
    groups = {}
    for i, box in enumerate(boxes):
        groups.setdefault(find(i), []).append(box)
        cycles += SCHEDULE['group_accumulate_candidate']
    merged = []
    for members in groups.values():
        count = len(members)
        averaged = tuple((sum(b[k] for b in members)+count//2)//count for k in range(4))
        merged.append((averaged, count))
        cycles += 4*SCHEDULE['group_mean_field']
    output = []
    for a, support in merged:
        if support <= 5:
            continue
        nested = False
        for b, other_support in merged:
            if b == a or other_support <= 5:
                continue
            cycles += SCHEDULE['group_nested_pair']
            dx, dy = (b[2]+2)//5, (b[3]+2)//5
            if (a[0] >= b[0]-dx and a[1] >= b[1]-dy and a[0]+a[2] <= b[0]+b[2]+dx
                    and a[1]+a[3] <= b[1]+b[3]+dy and other_support > max(3, support)):
                nested = True
                break
        if not nested:
            output.append((*a, support))
    return tuple(sorted(output)), False, cycles+SCHEDULE['group_finalize']


def scan_level(gray, model, floating=False, keep_trace=False):
    size = len(gray)
    yy, xx = np.mgrid[:size-23, :size-23]
    x, y = xx.ravel(), yy.ravel()
    sat = integral(gray)
    # Host vectorization of repeated 22x22 serial reads, NOT a square-integral RAM.
    windows = np.lib.stride_tricks.sliding_window_view(gray, (22, 22))[1:size-22, 1:size-22]
    sums = rectangle(sat, x, y, (1, 1, 22, 22))
    squares = (windows.astype(np.int64)**2).sum(axis=(-2, -1)).ravel()
    d = 484*squares-sums*sums
    if np.any(d < 0) or np.any(d >= 1 << 34):
        raise OverflowError('Variance arithmetic overflow')
    roots = np.array([floor_sqrt(int(v)) for v in d], np.int64)
    alive = d > 484*484*100
    rejected = np.full(len(x), -1, np.int64)
    weak_cycles = stage_cycles = weak_evaluations = stage_evaluations = 0
    trace = []
    first = 0
    for si, count in enumerate(model['counts']):
        ids = np.flatnonzero(alive)
        if not len(ids):
            break
        score = np.zeros(len(ids), np.float64 if floating else np.int64)
        if floating:
            inv = np.float32(1/np.sqrt(d[ids].astype(np.float64)))
        for wi in range(first, first+int(count)):
            feature = np.zeros(len(ids), np.int64)
            mode = int(model['modes'][wi])
            for rect, weight in zip(model['rects'][wi], C['rect_weight_modes'][mode]):
                if weight:
                    feature += weight*rectangle(sat, x[ids], y[ids], rect)
            if np.any(feature < -(1 << 21)) or np.any(feature >= 1 << 21):
                raise OverflowError('Feature exceeds signed 22-bit range')
            branch = (np.float32(np.float32(feature)*inv) < model['nodes'][wi] if floating else
                      (feature << 14) < model['nodes'][wi]*roots[ids])
            score += model['leaves'][wi, (~branch).astype(int)]
            rect_count = 3 if mode == 2 else 2
            weak_cycles += len(ids)*(SCHEDULE['stump_rom']+rect_count*SCHEDULE['rectangle']+SCHEDULE['stump_finalize'])
            weak_evaluations += len(ids)
            if keep_trace:
                trace.append((si, wi, ids.copy(), branch.copy()))
        if not floating and (np.any(score < -(1 << 25)) or np.any(score >= 1 << 25)):
            raise OverflowError('Stage accumulator exceeds signed 26 bits')
        failed = score < model['stages'][si]
        rejected[ids[failed]] = si
        alive[ids[failed]] = False
        first += int(count)
        stage_cycles += len(ids)*SCHEDULE['stage_compare']
        stage_evaluations += len(ids)
    rejected[alive] = 25
    raw = [mapped_box(int(x[i]), int(y[i]), size) for i in np.flatnonzero(alive)]
    cycles = {'resize': 0 if size == 64 else size*size*SCHEDULE['resize_per_pixel'],
              'integral': size*size*SCHEDULE['integral_per_pixel'],
              'normalization': len(x)*(484*SCHEDULE['norm_gray_per_pixel']+4*SCHEDULE['norm_integral_corner']+
                                      SCHEDULE['norm_finalize']+SCHEDULE['sqrt_iterations']),
              'weak': weak_cycles, 'stage': stage_cycles, 'candidate': len(raw)*SCHEDULE['candidate_store']}
    return {'size': size, 'x': x, 'y': y, 'd': d, 'roots': roots, 'rejected': rejected,
            'raw': raw, 'cycles': cycles, 'weak_evaluations': weak_evaluations,
            'stage_evaluations': stage_evaluations, 'trace': trace}


def detect(rgb, model, floating=False, keep_trace=False):
    base = gray_roi(rgb)
    levels = [scan_level(resize_gray(base, size), model, floating, keep_trace) for size in C['pyramid_sizes']]
    raw = [b for level in levels for b in level['raw']]
    grouped, fault, merge_cycles = group_boxes(raw)
    boxes = tuple((512+x, 232+y, 512+x+w-1, 232+y+h-1) for x, y, w, h, _ in grouped)
    counts = {key: sum(level['cycles'][key] for level in levels) for key in levels[0]['cycles']}
    counts['grouping'] = merge_cycles
    return {'boxes': boxes, 'groups': grouped, 'fault': fault, 'raw_count': len(raw),
            'cycles': sum(counts.values()), 'cycle_breakdown': counts, 'gray': base, 'levels': levels}


def scalar_window(gray, model, x, y):
    """Independent bounded loop for future RTL vectors; includes every weak decision."""
    size = len(gray)
    if not (0 <= x <= size-24 and 0 <= y <= size-24):
        raise ValueError('Window outside image')
    sat = [[0]*(size+1) for _ in range(size+1)]
    for row in range(size):
        prefix = 0
        for col in range(size):
            prefix += int(gray[row, col])
            sat[row+1][col+1] = sat[row][col+1]+prefix
    total = squared = 0
    for row in range(y+1, y+23):
        for col in range(x+1, x+23):
            pixel = int(gray[row, col])
            total += pixel
            squared += pixel*pixel
    d = 484*squared-total*total
    root = math.isqrt(d)
    cycles = 484*SCHEDULE['norm_gray_per_pixel']+4*SCHEDULE['norm_integral_corner']+SCHEDULE['norm_finalize']+17
    trace = []
    if d <= 484*484*100:
        return -1, cycles, trace
    first = 0
    for stage, count in enumerate(model['counts']):
        accumulated = 0
        for wi in range(first, first+int(count)):
            feature = 0
            mode = int(model['modes'][wi])
            for rect, weight in zip(model['rects'][wi], C['rect_weight_modes'][mode]):
                if weight:
                    rx, ry, w, h = map(int, rect)
                    left, top = x+rx, y+ry
                    value = sat[top][left]+sat[top+h][left+w]-sat[top][left+w]-sat[top+h][left]
                    feature += weight*value
            take_right = int(not ((feature << 14) < int(model['nodes'][wi])*root))
            leaf = int(model['leaves'][wi, take_right])
            accumulated += leaf
            cycles += 3+(3 if mode == 2 else 2)*12+6
            trace.append((stage, wi, feature, d, root, int(model['nodes'][wi]), take_right, leaf, accumulated, cycles))
        cycles += 4
        if accumulated < int(model['stages'][stage]):
            return stage, cycles, trace
        first += int(count)
    return 25, cycles+2, trace


if __name__ == '__main__':
    print(json.dumps(export_rom(), indent=2))
