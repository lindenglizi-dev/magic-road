
import struct

CONFIGURE_APPLICATION, CURVE_CHUNK, READ_APPLICATION = 0x60, 0x61, 0x62
CONFIG = struct.Struct('<BBHhHHH12x')


def config_bytes(mode, gamma=100, contrast=100, saturation=100, brightness=0, commit=0):
    if (mode not in range(11) or not 20 <= gamma <= 300 or
            not 0 <= contrast <= 300 or not 0 <= saturation <= 300 or
            not -128 <= brightness <= 128 or commit not in range(4)):
        raise ValueError('合并模式或图像参数越界')
    return CONFIG.pack(mode, commit, round(contrast*256/100), brightness,
                       round(saturation*256/100), gamma, 0)


def parse_application(packet, command):
    data = packet.data
    if packet.command == 0x82:
        raise RuntimeError(f'板端拒绝合并控制 {command:02x}：{data[1] if len(data)>1 else "缺少错误码"}')
    if (packet.command != 0x81 or len(data) != 42 or data[0] != command or
            data[1] != 0 or data[2] != 2 or data[3] > 10):
        raise ValueError('未收到匹配的合并工程回执；保持算法控制禁用')
    revision, request_id = struct.unpack_from('<HI', data, 4)
    if command == READ_APPLICATION:
        mode, flags, contrast, brightness, saturation, gamma = struct.unpack_from('<BBHhHH',data,10)
        if (mode != data[3] or flags != 0 or contrast > 768 or saturation > 768 or
                not -128 <= brightness <= 128 or not 20 <= gamma <= 300 or any(data[20:34])):
            raise ValueError('板端合并模式或实际参数回读越界')
    return dict(revision=revision, request_id=request_id, mode=data[3], config=data[10:34])


def write_payload(request_id, revision, content):
    if len(content) != 24:
        raise ValueError('合并配置内容必须为24字节')
    return struct.pack('<IH', request_id, revision)+content


def gamma_curve(percent):
    if not 20 <= percent <= 300:
        raise ValueError('Gamma 范围为0.20～3.00')
    return bytes(min(255, int(255*(v/255)**(percent/100)+.5)) for v in range(256))


def editor_curve(gamma, contrast, brightness):
    config_bytes(9, gamma, contrast, 100, brightness)
    coefficient=round(contrast*256/100)
    curve=gamma_curve(gamma)
    return bytes(curve[min(255,max(0,min(255,max(0,((v-128)*coefficient+32768)//256))+brightness))]
                 for v in range(256))


def curve_chunks(kind, curve):
    if kind not in (0,1) or len(curve)!=256:
        raise ValueError('曲线种类或长度无效')
    for offset in range(0,256,16):
        yield bytes((kind,offset,16))+curve[offset:offset+16]+bytes(5)
