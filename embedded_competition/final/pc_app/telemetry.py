
import json
from pathlib import Path
import struct

SNAPSHOT_BYTES = 192
PAGE_BYTES = 48
ACQUIRE = 0x50
READ_PAGE = 0x51
ERRORS = {1: '不支持的只读命令', 2: '请求长度错误', 3: '页号越界',
          4: '抓取忙', 5: '当前快照不可用（未就绪、抓取失败或已撤销）', 6: '快照已过期'}


def parse_page(packet, command):
    data = packet.data
    if packet.command not in (0x81, 0x82) or len(data) < 2 or data[0] != command:
        raise ValueError('回复命令不匹配')
    if data[1] or packet.command == 0x82:
        raise RuntimeError(ERRORS.get(data[1], f'FPGA错误{data[1]}'))
    if len(data) != 57 or data[2] != 1 or data[4] != 4 or data[3] >= 4:
        raise ValueError('快照页版本、长度或页号错误')
    token = int.from_bytes(data[5:9], 'little')
    if token == 0:
        raise ValueError('快照ID不能为0')
    return token, data[3], data[9:]


def assemble_pages(pages):
    if len(pages) != 4 or [page[1] for page in pages] != list(range(4)):
        raise ValueError('快照必须按序包含0至3页')
    if len({page[0] for page in pages}) != 1 or any(len(page[2]) != 48 for page in pages):
        raise ValueError('快照ID混用或页长度错误')
    return decode_snapshot(b''.join(page[2] for page in pages), pages[0][0])


def decode_snapshot(raw, snapshot_id):
    if len(raw) != SNAPSHOT_BYTES or raw[0] != 1:
        raise ValueError('快照必须是schema1的192字节')
    u16 = lambda offset: int.from_bytes(raw[offset:offset+2], 'little')
    u32 = lambda offset: int.from_bytes(raw[offset:offset+4], 'little')
    flags = raw[1]
    total = int.from_bytes(raw[32:40], 'little')
    bcd = u32(40)
    if total >= 1 << 34 or bcd >> 28:
        raise ValueError('total34或E_BCD保留位非零')
    digits = [(bcd >> (4*n)) & 15 for n in range(7)]
    if any(digit > 9 for digit in digits):
        raise ValueError('E_BCD不是合法七位BCD')
    if raw[2] > 3 or raw[3] > 4 or raw[44] > 15 or raw[45] > 15 or raw[50] > 127 or raw[53] > 4 or u32(144) >= 1 << 20:
        raise ValueError('状态字段越界')
    boxes = []
    for index in range(4):
        offset = 80+16*index
        valid, color, status = raw[offset:offset+3]
        coords = [u16(offset+n) for n in (4, 6, 8, 10, 12, 14)]
        if valid > 1 or color > 3 or status > 2 or any(value > 4095 for value in coords):
            raise ValueError('目标框字段越界')
        boxes.append(dict(valid=bool(valid), color=color, status=status, good=bool(raw[offset+3] & 1),
                          quality_pending=bool(raw[offset+3] & 2),
                          center=coords[:2], box=coords[2:]))
    face_box = [u16(n) for n in (56, 58, 60, 62)]
    if any(value > 4095 for value in face_box):
        raise ValueError('人脸框坐标越界')
    extension = None
    if raw[148:150] == bytes((0xD1, 1)):
        if (raw[154] | raw[155]) & 0xf0:
            raise ValueError('逐目标质量位保留字段非零')
        reason_names = ('宽度不符', '高度不符', '有效面积不足', '所选形状不符',
                        '颜色不在选择范围', '粗形状/小目标', '轮廓不符', '宽高比/着色填充不符')
        for index, box in enumerate(boxes):
            bits = raw[156+index]
            box['last_observation'] = dict(raw_good=bool(raw[154] & (1 << index)),
                confirmed_good=bool(raw[155] & (1 << index)), reject_bits=bits,
                reject_reasons=[name for bit, name in enumerate(reason_names) if bits & (1 << bit)],
                note='最后一次实际观测；预测框不代表新测量')
        extension = dict(schema=1, result_epoch=u16(150), result_job=u16(152),
                         good=u32(160), bad=u32(164), completed_jobs=u32(168),
                         bad_front_frames=u32(172),
                         note='good/bad与显示框同批冻结；结果批号不是相机或视频frameID')
    return dict(schema=1, snapshot_id=snapshot_id, paused=bool(flags & 1),
                strict=bool(flags & 2), mask=bool(flags & 4),
                epoch=u16(4), input_frame_seq=u32(8),
                face=dict(enabled=bool(raw[55] & 1) if raw[55] in (0x80,0x81) else None,
                          unlocked=bool(flags & 8), busy=bool(flags & 16),
                          fault=bool(flags & 32), pending=bool(flags & 64),
                          box_valid=bool(flags & 128), confirmed=raw[2], roi_id=raw[3],
                          sample=u32(12), result_epoch=u16(6), cycles=u32(16), raw_count=raw[54], box=face_box),
                counts=dict(red=u32(20), green=u32(24), yellow=u32(28),
                            total=total, E_BCD=f'{bcd:07x}',
                            E=sum(digit*10**n for n, digit in enumerate(digits))),
                diagnostic=dict(count=raw[44], reject=raw[45], width=u16(46),
                                height=u16(48), fill=raw[50], gate_state=raw[51],
                                reason=raw[52], live=raw[53], area=u32(144)),
                camera_status=int.from_bytes(raw[64:70], 'little'),
                white=dict(status=raw[70], gain_red=u32(72), gain_blue=u32(76)),
                boxes=boxes,
                diagnostic_extension=extension,
                frame_alignment='input_frame_seq is the OSD commit input sequence; video packet frame ID is separate, exact DDR/result alignment is not encoded')


class JsonlRecorder:
    def __init__(self):
        self.stream = None

    def open(self, path):
        self.close()
        self.stream = Path(path).open('a', encoding='utf-8')

    def write(self, record):
        if self.stream:
            self.stream.write(json.dumps(record, ensure_ascii=False, separators=(',', ':'))+'\n')
            self.stream.flush()

    def close(self):
        if self.stream:
            self.stream.close()
            self.stream = None


def page_request(snapshot_id, page):
    if not 1 <= snapshot_id <= 0xffffffff or not 0 <= page < 4:
        raise ValueError('快照ID或页号越界')
    return struct.pack('<IB', snapshot_id, page)
