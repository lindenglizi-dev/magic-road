from datetime import datetime
import os
from pathlib import Path
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLabel, QPlainTextEdit, QGroupBox, QGridLayout)

class MainWindow(QMainWindow):
    def __init__(self, controller, config):
        super().__init__()
        font_path = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/msyh.ttc'
        if font_path.is_file():
            font_id = QFontDatabase.addApplicationFont(str(font_path))
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                self.setFont(QFont(families[0], 10))
        self.controller = controller
        self.setWindowTitle('FPGA 图像模式控制 — ' + config['profile'])
        self.resize(920, 800)
        root = QWidget(); self.setCentralWidget(root); layout = QVBoxLayout(root)
        row = QHBoxLayout(); layout.addLayout(row)
        self.ports = QComboBox(); self.ports.setEditable(True)
        self.baud = QComboBox()
        for value in config['baudrates']:
            self.baud.addItem(str(value), value)
        self.refresh = QPushButton('刷新串口'); self.connect_button = QPushButton('连接')
        for widget in (QLabel('串口'), self.ports, self.refresh, QLabel('波特率'), self.baud, self.connect_button):
            row.addWidget(widget)
        self.status = QLabel('已断开'); layout.addWidget(self.status)
        note = QLabel('协议 V2 · 115200 / 8N1。编号 0 为原图，1～11 从左到右排列。参数为固件默认值；切换结果请查看 HDMI。')
        note.setWordWrap(True); layout.addWidget(note)
        source_grid = None
        if any(item.get('role') == 'source' for item in config['modes']):
            source_group = QGroupBox('基础输出')
            source_grid = QGridLayout(source_group)
            layout.addWidget(source_group)
        group = QGroupBox('图像处理模式'); grid = QGridLayout(group); layout.addWidget(group)
        self.mode_buttons = []
        source_index, algorithm_index = 0, 0
        for item in config['modes']:
            button = QPushButton(item['name'] + ('\n' + item['english'] if item.get('english') else ''))
            button.setMinimumHeight(54)
            button.setToolTip(item.get('description', ''))
            button.clicked.connect(lambda checked=False, mode_id=item['id']: self.select_mode(mode_id))
            button.setEnabled(False); self.mode_buttons.append(button)
            if item.get('role') == 'source':
                source_grid.addWidget(button, source_index // 3, source_index % 3)
                source_index += 1
            else:
                grid.addWidget(button, algorithm_index // 3, algorithm_index % 3)
                algorithm_index += 1
        self.mode = QLabel('尚未发送；FPGA 当前模式未确认'); self.mode.setWordWrap(True); layout.addWidget(self.mode)
        self.description = QLabel('将鼠标放在算法按钮上查看处理说明。原图和各算法以官方 AWB 校正图像为输入。')
        self.description.setWordWrap(True); layout.addWidget(self.description)
        self.logs = QPlainTextEdit(); self.logs.setReadOnly(True); self.logs.setMaximumBlockCount(1500); layout.addWidget(self.logs)
        clear = QPushButton('清空日志'); clear.clicked.connect(self.logs.clear); layout.addWidget(clear)
        self.refresh.clicked.connect(self.scan)
        self.connect_button.clicked.connect(self.toggle_connection)
        controller.serial.state_changed.connect(self.update_state)
        controller.request_changed.connect(self.mode.setText)
        controller.log.connect(self.append_log)
        self.scan()

    def append_log(self, text):
        self.logs.appendPlainText(datetime.now().strftime('%H:%M:%S.%f')[:-3] + '  ' + text)

    def scan(self):
        current = self.current_port()
        self.ports.clear()
        for port, description in self.controller.serial.scan():
            self.ports.addItem(f'{port} — {description}', port)
        if current:
            index = self.ports.findData(current)
            if index >= 0: self.ports.setCurrentIndex(index)
            else: self.ports.setEditText(current)

    def current_port(self):
        text = self.ports.currentText().strip()
        if text == self.ports.itemText(self.ports.currentIndex()):
            return self.ports.currentData() or text
        return text

    def toggle_connection(self):
        manager = self.controller.serial
        if manager.worker is not None:
            manager.close()
        else:
            try:
                manager.open(self.current_port(), self.baud.currentData())
            except (ValueError, RuntimeError) as exc:
                self.append_log(str(exc))

    def select_mode(self, mode_id):
        try:
            self.controller.set_mode(mode_id)
            self.description.setText(self.mode_description(self.controller.modes[mode_id]))
        except (ValueError, RuntimeError) as exc: self.append_log(str(exc))

    def mode_description(self,item):
        device=getattr(self.controller,'device',None)
        key='description_pc' if device and device.source==1 else 'description'
        return item.get(key,item.get('description',''))

    def update_state(self, state):
        manager = self.controller.serial
        self.status.setText(state)
        self.connect_button.setText('断开' if manager.worker else '连接')
        self.connect_button.setEnabled(not manager.closing)
        for widget in (self.ports, self.baud, self.refresh): widget.setEnabled(manager.worker is None)
        for button in self.mode_buttons: button.setEnabled(manager.connected)

    def closeEvent(self, event):
        manager = self.controller.serial
        if manager.worker is not None:
            manager.close()
            # Close after the bounded serial read/write finishes, without destroying a live QThread.
            manager.worker.finished.connect(self.close)
            event.ignore()
        else: event.accept()
