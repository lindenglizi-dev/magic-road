
import struct

CONFIGURE, CLEAR, READ = 0x52, 0x53, 0x54
SET_VIEW, READ_VIEW = 0x55, 0x56
RAW_VIEW, BALL_VIEW = 0, 1
CONFIG = struct.Struct('<4B10H')
DEFAULT = (1, 1, 1, 2, 64, 160, 1216, 640, 24, 384, 24, 384, 640, 64)


class PanelError(RuntimeError):
    def __init__(self, code):
        self.code = code
        super().__init__({1: '板端不支持工业参数协议', 2: '参数长度错误', 3: '参数范围错误',
            4: '板端仍有待提交事务，请稍后读取确认', 5: '等待帧界超时，事务可能随后生效，请先查询',
            6: '板端版本已变化，请读取实际参数后重新应用', 7: '请求ID已被其他参数使用',
            8: '原图模式不提供小球参数或结果'}.get(code, f'板端错误{code}'))


def view_payload(request_id, revision, target):
    if type(target) is not int or target not in (RAW_VIEW, BALL_VIEW) or not 0 <= revision < 16384 or not 0 <= request_id <= 0xffffffff:
        raise ValueError('显示模式、版本或请求ID越界')
    return struct.pack('<IHB', request_id, revision, target)


def parse_view(packet, command):
    data = packet.data
    if packet.command not in (0x81, 0x82) or len(data) < 2 or data[0] != command:
        raise ValueError('显示模式回复不匹配')
    if data[1] == 1:
        raise RuntimeError('此bit不支持原图/小球切换，请使用本目录配套的新bit')
    if data[1] or packet.command == 0x82:
        raise PanelError(data[1])
    if len(data) != 11:
        raise ValueError('显示模式回复长度错误')
    _, _, schema, view, caps, revision, request_id = struct.unpack('<5BHI', data)
    if schema != 1 or view not in (RAW_VIEW, BALL_VIEW) or caps != 3 or revision >= 16384:
        raise ValueError('显示模式能力或版本错误')
    return dict(view=view, revision=revision, request_id=request_id)


def pack_config(values, capability=7):
    values = tuple(values)
    if len(values) not in (14, 16) or any(type(value) is not int for value in values):
        raise ValueError('检测参数必须包含14或16个整数')
    if capability not in (1, 7) or (capability == 1 and (len(values) == 16 or values[1] == 0)):
        raise ValueError('此bit仅支持单色及原有检测参数')
    enabled, color, shape, flags, x0, y0, x1, y1, low_w, high_w, low_h, high_h, line, area = values[:14]
    if (enabled not in (0, 1) or color not in (0, 1, 2, 3) or shape not in (0, 1, 2) or flags not in range(4) or
        not 64 <= x0 < x1 <= 1216 or not 160 <= y0 < y1 <= 640 or
        not 4 <= low_w <= high_w <= 1152 or not 4 <= low_h <= high_h <= 480 or
        not x0 + 16 <= line or not line + 16 < x1 or not 16 <= area <= 65535):
        raise ValueError('检测参数越界：检查ROI、宽高上下限、计数线两侧16像素空间及最小面积')
    if len(values) == 16:
        side, effective_area = values[14:]
        if not 4 <= side <= 64 or not 16 <= effective_area <= 1008 or effective_area % 16:
            raise ValueError('最小有效短边须为4..64，最小有效面积须为16..1008且为16的倍数')
        enabled |= side << 1
        color |= (effective_area // 16) << 2
    return CONFIG.pack(enabled, color, *values[2:14])


def unpack_config(raw, capability=7):
    encoded = CONFIG.unpack(raw)
    side = encoded[0] >> 1
    if side and not 4 <= side <= 64:
        raise ValueError('板端最小有效短边编码越界')
    values = (encoded[0] & 1, encoded[1] & 3, *encoded[2:], side or 12, (encoded[1] >> 2)*16 or 64)
    if capability == 1:
        if encoded[0] > 1 or encoded[1] not in (1, 2, 3):
            raise ValueError('旧bit返回了未声明的扩展参数')
        pack_config(values[:14], capability)
    else:
        pack_config(values, capability)
    return values


def write_payload(request_id, revision, config=None, capability=7, previous=None):
    if not 0 <= request_id <= 0xffffffff or not 0 <= revision <= 0xffff:
        raise ValueError('请求ID或版本越界')
    raw = bytearray(pack_config(config, capability)) if config is not None else bytearray()
    if previous is not None and len(config or ()) == 16:
                                                                                          
        if previous['raw_config'][0] >> 1 == 0 and config[14] == previous['config'][14]:
            raw[0] &= 1
        if previous['raw_config'][1] >> 2 == 0 and config[15] == previous['config'][15]:
            raw[1] &= 3
    return struct.pack('<IH', request_id, revision) + raw


def parse_reply(packet, command):
    data = packet.data
    if packet.command not in (0x81, 0x82) or len(data) < 2 or data[0] != command:
        raise ValueError('工业参数回复命令不匹配')
    if data[1] or packet.command == 0x82:
        raise PanelError(data[1])
    if len(data) != 42 or data[2] != 1 or data[3] not in (1, 7):
        raise ValueError('工业参数能力、版本或长度不匹配')
    config = unpack_config(data[10:34], data[3])
    return dict(schema=1, capability=data[3], revision=int.from_bytes(data[4:6], 'little'),
        request_id=int.from_bytes(data[6:10], 'little'), config=config, raw_config=CONFIG.unpack(data[10:34]),
        good=int.from_bytes(data[34:38], 'little'), bad=int.from_bytes(data[38:42], 'little'))
