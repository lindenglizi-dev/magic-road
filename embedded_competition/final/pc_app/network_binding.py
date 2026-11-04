




from dataclasses import dataclass
import ipaddress
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
INVENTORY = r'''
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false)
$items=@(Get-NetAdapter -Physical | Where-Object {$_.Status -eq 'Up' -and $_.InterfaceType -eq 6 -and $_.PhysicalMediaType -eq '802.3'} | ForEach-Object {
 $nic=$_
 $ips=@(Get-NetIPAddress -InterfaceIndex $nic.ifIndex -AddressFamily IPv4 -PolicyStore ActiveStore -ErrorAction SilentlyContinue |
  Where-Object {$_.AddressState -in @('Preferred','Deprecated')} | ForEach-Object {
   [pscustomobject]@{address=$_.IPAddress;prefix=$_.PrefixLength}
  })
 [pscustomobject]@{name=$nic.Name;index=$nic.ifIndex;mac=$nic.MacAddress;addresses=$ips}
})
ConvertTo-Json -InputObject $items -Depth 5 -Compress
'''


@dataclass(frozen=True)
class Binding:
    address: str
    interface_index: int
    interface_name: str


def powershell(arguments, timeout=25):
    return subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', *arguments],
                          capture_output=True, encoding='utf-8-sig', errors='replace',
                          timeout=timeout, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))


def ethernet_adapters():
    result = powershell(['-Command', INVENTORY])
    if result.returncode:
        raise RuntimeError('读取物理以太网网卡失败：'+result.stderr.strip())
    return json.loads(result.stdout.strip() or '[]')


def select_binding(adapters, peer, requested='0.0.0.0'):
    target = ipaddress.IPv4Address(peer)
    explicit = requested != '0.0.0.0'
    candidates = []
    for nic in adapters:
        for entry in nic['addresses']:
            address = ipaddress.IPv4Address(entry['address'])
            network = ipaddress.IPv4Interface(f"{address}/{entry['prefix']}").network
            if address == target:
                raise ValueError('电脑地址与 FPGA 地址相同，请为两端使用不同地址')
            if (explicit and str(address) == requested) or (not explicit and target in network):
                candidates.append(Binding(str(address), int(nic['index']), nic['name']))
    if len(candidates) > 1:
        raise ValueError('多块有线网卡可到达 FPGA，请在现有“本机绑定”框指定直连网卡 IP')
    if candidates:
        return candidates[0]
    if explicit:
        raise ValueError(f'绑定地址 {requested} 不属于已连接的物理以太网卡；使用 0.0.0.0 可自动配置和选择')
    return None


def configure_adapter(nic, peer, log):
    network = ipaddress.IPv4Network(f'{peer}/24', strict=False)
    local = str(next(host for host in network.hosts() if str(host) != peer))
    log(f"网卡 {nic['name']} 缺少 FPGA 网段地址，将添加 {local}/24；Windows 将请求一次管理员授权")
    with tempfile.TemporaryDirectory(prefix='hx1p35a-network-') as directory:
        report = Path(directory)/'result.json'
                                                                                      
        report.write_text('{}', encoding='utf-8')
        result = powershell(['-ExecutionPolicy', 'Bypass', '-File', str(HERE/'setup_network.ps1'),
                             '-InterfaceIndex', str(nic['index']), '-LocalAddress', local,
                             '-BoardAddress', peer, '-Report', str(report)], timeout=180)
        try:
            evidence = json.loads(report.read_text(encoding='utf-8-sig')) if report.is_file() else {}
        except OSError:
                                                                                 
                                                                             
            if result.returncode == 0:
                evidence = {'ok': select_binding(ethernet_adapters(), peer) is not None}
            else:
                evidence = {}
        if result.returncode == 0 and not evidence.get('ok'):
            evidence['ok'] = select_binding(ethernet_adapters(), peer) is not None
        if result.returncode or not evidence.get('ok'):
            message = evidence.get('error') or result.stderr.strip() or '管理员授权被取消或网络配置未完成'
            raise RuntimeError('直连网卡配置失败：'+message)
    log(f"已保存 {nic['name']} 的 {local}/24 地址，重启后仍保留；WLAN、代理和默认网关未修改")


def resolve_binding(peer, requested='0.0.0.0', log=lambda message: None, configure=True):
    ipaddress.IPv4Address(peer)
    ipaddress.IPv4Address(requested)
    if os.name != 'nt':
        if requested != '0.0.0.0':
            return Binding(requested, 0, 'explicit')
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as route:
            route.connect((peer, 6002))
            return Binding(route.getsockname()[0], 0, 'system route')
    log('正在查找 FPGA 直连的物理以太网卡…')
    adapters = ethernet_adapters()
    binding = select_binding(adapters, peer, requested)
    if binding:
        return binding
    if not adapters:
        raise RuntimeError('没有已连接的物理以太网卡，请检查网线和板卡上电')
    if len(adapters) != 1:
        raise RuntimeError('有多块物理以太网卡且没有 FPGA 同网段地址，请先指定直连网卡的本机 IP')
    if not configure:
        raise RuntimeError('直连网卡缺少 FPGA 同网段地址，请运行 setup_network.ps1 配置后重试')
    configure_adapter(adapters[0], peer, log)
    binding = select_binding(ethernet_adapters(), peer)
    if binding is None:
        raise RuntimeError('网卡地址尚未就绪，请稍后重新连接')
    return binding


def pin_interface(sock, binding):
    if os.name == 'nt' and binding.interface_index:
                                                                                  
        sock.setsockopt(socket.IPPROTO_IP, getattr(socket, 'IP_UNICAST_IF', 31),
                        struct.pack('!I', binding.interface_index))
