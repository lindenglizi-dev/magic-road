"""固定16位诊断链路参考；实际CNN数值仍由冻结参考提供。"""

PACKETS = {
    0x8000: (1024, 16384),  # 表项直接逐项装入唯一SiLU表。
    0x8001: (1, 4),
    0x8002: (0, 0),
    0x8100: (11, 161),
    0x8101: (29, 463),
    0x8102: (1, 7),
    0xA100: (2, 32),
    0xA101: (2, 22),
    0xA102: (4, 49),
    0xA103: (1, 7),
}


def encode(header, payload=0):
    """输出header与低16位优先payload，拒绝位宽之外数据。"""
    count, width = PACKETS[header]
    if payload < 0 or payload >= 1 << width:
        raise ValueError("payload超出固定字段宽度")
    return [header] + [(payload >> (16 * index)) & 0xFFFF for index in range(count)]


def decode(words):
    """完整包才返回结果；填充位、长度与16位边界全部校验。"""
    if not words or words[0] not in PACKETS:
        raise ValueError("未知header")
    count, width = PACKETS[words[0]]
    if len(words) != count + 1 or any(word < 0 or word > 0xFFFF for word in words):
        raise ValueError("包长度或16位边界错误")
    payload = sum(word << (16 * index) for index, word in enumerate(words[1:]))
    if payload >= 1 << width:
        raise ValueError("填充位非零")
    return words[0], payload


def identity(block, layer, channel=0, group=0, window=0):
    """完整参数身份22位；barrier仅使用低7位。"""
    values = ((block, 4), (layer, 3), (channel, 7), (group, 5), (window, 3))
    if any(value < 0 or value >= 1 << width for value, width in values):
        raise ValueError("身份字段超宽")
    return block | layer << 4 | channel << 7 | group << 14 | window << 19


def parameter_response(ident, weight, data, error=0):
    """192位weight、248位data和故障位逐位保留。"""
    values = ((ident, 22), (weight, 192), (data, 248), (error, 1))
    if any(value < 0 or value >= 1 << width for value, width in values):
        raise ValueError("参数字段超宽")
    return encode(0x8101, ident | weight << 22 | data << 214 | error << 462)


def self_check():
    """对全部包首末位、非零填充、部分包与参数字段作可运行检查。"""
    for header, (_, width) in PACKETS.items():
        for payload in (0, (1 << width) - 1):
            assert decode(encode(header, payload)) == (header, payload)
    ident = identity(9, 5, 111, 23, 6)
    weight = int("a55a" * 12, 16)
    data = (1 << 247) | 0x123456789ABCDEF
    _, payload = decode(parameter_response(ident, weight, data, 1))
    assert payload & ((1 << 22) - 1) == ident
    assert payload >> 22 & ((1 << 192) - 1) == weight
    assert payload >> 214 & ((1 << 248) - 1) == data
    assert payload >> 462 == 1
    for bad in ([0x8001], [0x8001, 0x10], [0x8100] + [0] * 10 + [2], [0xFFFF]):
        try:
            decode(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("非法包被接受")
    print("packet reference self_check PASS")


if __name__ == "__main__":
    self_check()
