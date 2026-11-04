
import ctypes
import errno
import hashlib
import os
import tempfile
from pathlib import Path


class ClientSession:
    def __init__(self, fpga_ip):
        self.handle = None
        self.file = None
        token = hashlib.sha256(fpga_ip.encode('ascii')).hexdigest()[:20]
        message = f'板卡 {fpga_ip} 已被另一个本机连接使用；请先断开其他上位机或诊断窗口（包括仅以太网预览）'
        if os.name == 'nt':
            from ctypes import wintypes
            self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
            self.kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
            self.kernel.CreateMutexW.restype = wintypes.HANDLE
            self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
            self.kernel.CloseHandle.restype = wintypes.BOOL
            ctypes.set_last_error(0)
            handle = self.kernel.CreateMutexW(None, False, 'Local\\HX1P35A_Ethernet_' + token)
            error = ctypes.get_last_error()
            if not handle:
                raise ctypes.WinError(error)
            if error == 183:                                                                   
                self.kernel.CloseHandle(handle)
                raise OSError(errno.EBUSY, message)
            self.handle = handle
        else:
            import fcntl
            self.file = (Path(tempfile.gettempdir()) / ('hx1p35a_' + token + '.lock')).open('a+b')
            try:
                fcntl.flock(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                self.file.close()
                self.file = None
                raise OSError(errno.EBUSY, message)

    def close(self):
        if self.handle is not None:
            self.kernel.CloseHandle(self.handle)
            self.handle = None
        if self.file is not None:
            self.file.close()
            self.file = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
