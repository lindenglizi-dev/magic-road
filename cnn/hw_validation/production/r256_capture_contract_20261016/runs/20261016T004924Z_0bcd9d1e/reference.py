"""固定R256候选：原720p RGB888直接5×5面积平均，不依赖第三方库。"""
from array import array

SOURCE_WIDTH, SOURCE_HEIGHT = 1280, 720
WIDTH, HEIGHT = 256, 144
INPUT_BYTES, OUTPUT_BYTES = 2764800, 110592


def rgb_bytes(data, expected):
    """只接受连续UINT8，拒绝已中心化INT8，防止重复pixel-128。"""
    view = memoryview(data)
    if view.format != 'B' or not view.c_contiguous or view.nbytes != expected:
        raise ValueError(f'expected contiguous uint8 with {expected} bytes')
    return view.cast('B')


def round_sum25(total):
    """非负13位合法和，最近偶数；除数25为奇数，整数和不会落在半点。"""
    if not 0 <= total <= 6375:
        raise ValueError('5x5 unsigned pixel sum outside 0..6375')
    quotient, remainder = divmod(total, 25)
    return quotient + int(2 * remainder > 25 or
                          (2 * remainder == 25 and quotient % 2 == 1))


def resize_rgb888(source):
    """独立二维直接求和；输入RGB/YXC，返回110592个RGB/YXC UINT8字节。"""
    source = rgb_bytes(source, INPUT_BYTES)
    output = bytearray(OUTPUT_BYTES)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            sums = [0, 0, 0]
            for dy in range(5):
                start = ((y * 5 + dy) * SOURCE_WIDTH + x * 5) * 3
                for offset in range(start, start + 15, 3):
                    for channel in range(3):
                        sums[channel] += source[offset + channel]
            start = (y * WIDTH + x) * 3
            output[start:start + 3] = bytes(round_sum25(value) for value in sums)
    return bytes(output)


def centered_int8(rgb):
    """卷积入口才做一次pixel-128；输入槽仍保存原UINT8 RGB。"""
    return array('b', (value - 128 for value in rgb_bytes(rgb, OUTPUT_BYTES)))


def awb96_events(source, *, sof_with_valid=True, bubble_every=0):
    """生成单帧有效事件，lane3最早；不声称RTL周期/缓存或真实AWB blank时序。"""
    source = rgb_bytes(source, INPUT_BYTES)
    if not sof_with_valid:
        yield 0, False, True, False
    for beat in range(SOURCE_HEIGHT * 320):
        if bubble_every and beat % bubble_every == 0:
            yield 0, False, False, False
        offset = beat * 12
        word = int.from_bytes(source[offset:offset + 12], 'big')
        yield word, True, sof_with_valid and beat == 0, beat % 320 == 319


def resize_awb96(events):
    """第二算法：逐lane水平累计、再跨5行累计。异常帧抛错，不返回半帧。"""
    vertical = [[0, 0, 0] for _ in range(WIDTH)]
    horizontal = [0, 0, 0]
    output = bytearray()
    active = complete = False
    row = beat_in_row = 0
    phase_counts = [0] * 5
    completion_lanes = [0] * 4
    for word, valid, sof, eol in events:
        if sof:
            if active or complete:
                raise ValueError('unexpected second SOF in single-frame input')
            active = True
        if not valid:
            if eol:
                raise ValueError('EOL without valid')
            continue
        if not active or complete or not 0 <= word < (1 << 96):
            raise ValueError('valid outside frame or malformed AWB96 word')
        if bool(eol) != (beat_in_row == 319):
            raise ValueError('early/missing EOL')
        phase_counts[(beat_in_row * 4) % 5] += 1
        for position, lane in enumerate((3, 2, 1, 0)):
            pixel = (word >> (lane * 24)) & 0xffffff
            for channel, shift in enumerate((16, 8, 0)):
                horizontal[channel] += (pixel >> shift) & 255
            source_x = beat_in_row * 4 + position
            if source_x % 5 == 4:
                x = source_x // 5
                completion_lanes[lane] += 1
                for channel in range(3):
                    vertical[x][channel] += horizontal[channel]
                    horizontal[channel] = 0
                if row % 5 == 4:
                    output.extend(round_sum25(value) for value in vertical[x])
                    vertical[x] = [0, 0, 0]
        if eol:
            assert horizontal == [0, 0, 0]
            beat_in_row = 0
            row += 1
            if row == SOURCE_HEIGHT:
                active, complete = False, True
        else:
            beat_in_row += 1
    if not complete or active or len(output) != OUTPUT_BYTES:
        raise ValueError('incomplete frame; no tensor publication')
    return bytes(output), {'horizontal_phase_beat_counts': phase_counts,
                           'horizontal_completion_lane_counts_low_to_high': completion_lanes,
                           'source_rows': row, 'output_bytes': len(output)}


def output_records(rgb):
    """候选端点内容，不指定时钟延迟：低byte R/G/B、mask01、内部x/y沿旧9位。"""
    rgb = rgb_bytes(rgb, OUTPUT_BYTES)
    for index in range(WIDTH * HEIGHT):
        offset = index * 3
        word = rgb[offset] | (rgb[offset + 1] << 8) | (rgb[offset + 2] << 16)
        x, y = index % WIDTH, index // WIDTH
        yield {'x': x, 'y': y, 'pixels': word, 'lane_mask': 1,
               'sof': index == 0, 'eol': x == WIDTH - 1,
               'eof': index == WIDTH * HEIGHT - 1}
