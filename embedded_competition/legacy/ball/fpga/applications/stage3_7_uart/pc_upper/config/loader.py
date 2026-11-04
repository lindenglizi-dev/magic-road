import json

def load_config(path):
    config = json.loads(path.read_text(encoding='utf-8'))
    if config.get('schema_version') != 1 or config.get('protocol_version') != 2:
        raise ValueError('不支持的配置或协议版本')
    modes = config.get('modes')
    if not isinstance(modes, list) or not modes:
        raise ValueError('modes 必须是非空列表')
    ids, commands = set(), set()
    for item in modes:
        if not isinstance(item.get('id'), str) or not item['id'] or item['id'] in ids:
            raise ValueError('算法 id 必须是唯一非空字符串')
        if not isinstance(item.get('name'), str) or not item['name'].strip():
            raise ValueError('算法名称不能为空')
        command = item.get('command')
        if type(command) is not int or not 0 <= command <= 255 or command in commands:
            raise ValueError('command 必须是唯一的 0..255 整数')
        ids.add(item['id']); commands.add(command)
    if not config.get('baudrates') or any(type(b) is not int or b <= 0 for b in config['baudrates']):
        raise ValueError('baudrates 必须包含有效波特率')
    return config
