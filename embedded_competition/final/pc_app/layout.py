



from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPlainTextEdit, QProgressBar, QPushButton, QScrollArea, QSlider, QSpinBox,
    QSplitter, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget)

ALGORITHMS = ["原图", "白平衡", "灰度二值化", "中值滤波", "边缘检测", "锐化",
              "伽马矫正", "对比度调节", "亮度调节", "图像编辑（叠加）"]
SUPPORTED_ALGORITHM_IDS = tuple(range(10))

STYLE = """
QWidget { background:#101820; color:#dbe6ef; font-family:'Microsoft YaHei UI'; font-size:13px; }
QGroupBox { border:1px solid #2d4050; border-radius:9px; margin-top:16px; padding:13px 10px 9px; font-weight:bold; }
QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 6px; color:#65d4be; }
QPushButton { background:#263c4d; padding:8px 12px; border:1px solid #3c596a; border-radius:5px; }
QPushButton:hover { background:#31556b; } QPushButton:disabled { color:#60717d; background:#1b2832; }
QPushButton#primary { background:#117c6d; border:1px solid #269e8d; color:white; }
QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox { background:#192731; border:1px solid #385161; border-radius:4px; padding:5px; }
QPlainTextEdit { background:#0c131a; color:#a4b7c5; border:1px solid #243946; }
QProgressBar { border:1px solid #34505f; border-radius:5px; text-align:center; height:19px; }
QProgressBar::chunk { background:#168e7c; }
QCheckBox::indicator { width:15px; height:15px; }
QLabel#title { font-size:23px; font-weight:bold; color:#f0f6fa; }
QLabel#muted { color:#8299ab; } QSplitter::handle { background:#243642; }
"""


def build_layout(self, algorithm, combined=False):
    self.setWindowTitle("HX1P35A · " + ("算法展示" if algorithm else "小球工业检测") + " · Gigabit Vision")
    self.resize(1400, 920)
    root = QWidget()
    layout = QVBoxLayout(root)
    title = QLabel("FPGA VISION  /  HX1P35A")
    title.setObjectName("title")
    layout.addWidget(title)
    self.subtitle = QLabel("UART 控制 / 千兆以太网图像 · 算法展示" if algorithm else "千兆以太网图像与结果 · 小球工业检测")
    subtitle = self.subtitle
    subtitle.setObjectName("muted")
    layout.addWidget(subtitle)
    self.splitter = QSplitter()
    splitter = self.splitter
    layout.addWidget(splitter, 1)
    left = QWidget()
    controls = QVBoxLayout(left)
    controls.setContentsMargins(0, 0, 8, 0)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(left)
    scroll.setMinimumWidth(350)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    splitter.addWidget(scroll)

    connection = QGroupBox("01  连接")
    form = QFormLayout(connection)
    self.ports = QComboBox()
    self.ports.addItem("仅以太网预览", "")
    row = QHBoxLayout()
    row.addWidget(self.ports, 1)
    refresh = QPushButton("刷新")
    if algorithm: refresh.clicked.connect(self.refresh_ports)
    else: refresh.setEnabled(False)
    row.addWidget(refresh)
    form.addRow("UART · 115200", row)
    self.ip = QLineEdit("192.168.137.2")
    form.addRow("FPGA IP", self.ip)
    self.bind = QLineEdit("0.0.0.0")
    self.bind.setToolTip("默认监听所有本地接口；多网卡时可指定以太网卡 IPv4 地址")
    form.addRow("本地监听", self.bind)
    self.connect_button = QPushButton("连接")
    self.connect_button.setObjectName("primary")
    self.connect_button.clicked.connect(self.toggle_connection)
    form.addRow(self.connect_button)
    self.network_label = QLabel("PHY：等待连接")
    self.network_label.setWordWrap(True)
    form.addRow(self.network_label)
    controls.addWidget(connection)

    self.algorithm_box = QGroupBox("02  算法与输入源 · UART")
    form = QFormLayout(self.algorithm_box)
    self.algorithms = QComboBox()
    for i in SUPPORTED_ALGORITHM_IDS:
        self.algorithms.addItem(f"{i:02d}  {ALGORITHMS[i]}", i)
    form.addRow(self.algorithms)
    adjustment_enabled=algorithm or combined
    if combined:
        self.algorithms.addItem("10  小球检测／计数",10)
        self.algorithms.setCurrentIndex(10)
    apply_mode = QPushButton("应用算法")
    if adjustment_enabled: apply_mode.clicked.connect(lambda: self.apply_selected_mode())
    form.addRow(apply_mode)
    form.addRow(QLabel("图像编辑 · 四项叠加"))
    self.gamma_slider = adjustment_row(self, adjustment_enabled, form, "Gamma", 20, 300, 100, 100)
    self.contrast_slider = adjustment_row(self, adjustment_enabled, form, "对比度", 0, 300, 100, 100)
    self.saturation_slider = adjustment_row(self, adjustment_enabled, form, "饱和度", 0, 300, 100, 100)
    self.brightness_slider = adjustment_row(self, adjustment_enabled, form, "亮度", -128, 128, 0, 1)
    tone_apply = QPushButton("开始 / 恢复叠加编辑")
    if adjustment_enabled: tone_apply.clicked.connect(self.apply_tone)
    form.addRow(tone_apply)
    edit_row = QHBoxLayout()
    reset_edit = QPushButton("恢复默认")
    if adjustment_enabled: reset_edit.clicked.connect(self.reset_editor)
    original = QPushButton("查看原图")
    if adjustment_enabled: original.clicked.connect(self.show_original)
    edit_row.addWidget(reset_edit)
    edit_row.addWidget(original)
    form.addRow(edit_row)
    self.tone_label = QLabel("拖动滑块自动进入叠加编辑；原图按钮可对照")
    self.tone_label.setWordWrap(True)
    form.addRow(self.tone_label)
    source_row = QHBoxLayout()
    for text, value in [("Camera", 0), ("PC Image", 1)]:
        button = QPushButton(text)
        if adjustment_enabled and (not combined or value==0): button.clicked.connect(lambda checked=False, v=value: self.submit("source", v))
        if combined and value==1: button.setEnabled(False)
        source_row.addWidget(button)
    form.addRow(source_row)
    self.state_label = QLabel("实际模式 / 输入源：等待硬件确认")
    self.state_label.setWordWrap(True)
    form.addRow(self.state_label)
    controls.addWidget(self.algorithm_box)

    self.roi_box = QGroupBox("03  工业检测与计数 · UART")
    form = QFormLayout(self.roi_box)
    self.roi_enable = QCheckBox("启用流水线检测（从左向右）")
    form.addRow(self.roi_enable)
    self.target_color = QComboBox()
    for name, value in [("红色", 1), ("黄色", 2), ("绿色", 3)]:
        self.target_color.addItem(name, value)
    if not algorithm:
        self.target_color.addItem("红黄绿全部", 0)
        self.target_color.model().item(self.target_color.findData(0)).setEnabled(False)
    form.addRow("良品颜色", self.target_color)
    self.target_shape = QComboBox()
    for name, value in [("圆形 / 小球", 1), ("实心矩形", 2), ("不限形状（调试）", 0)]:
        self.target_shape.addItem(name, value)
    form.addRow("良品形状", self.target_shape)
    self.strict, self.border = QCheckBox("严格颜色阈值"), QCheckBox("显示检测框与计数线")
    self.border.setChecked(True)
    form.addRow(self.strict)
    form.addRow(self.border)
    self.coords = []
    for label, value, minimum, maximum in [("区域 x0", 64, 64, 1215), ("区域 y0", 160, 160, 639),
            ("区域 x1", 1216, 65, 1216), ("区域 y1", 640, 161, 640)]:
        spin = QSpinBox(); spin.setRange(minimum, maximum); spin.setValue(value)
        self.coords.append(spin); form.addRow(label, spin)
    self.size_limits = []
    for label, value, minimum, maximum in [("良品最小宽度 px", 24, 4, 1152), ("良品最大宽度 px", 384, 4, 1152),
            ("良品最小高度 px", 24, 4, 480), ("良品最大高度 px", 384, 4, 480),
            ("计数线 x", 640, 96 if algorithm else 80, 1183 if algorithm else 1199), ("良品最小面积 px", 64, 16, 65535)]:
        spin = QSpinBox(); spin.setRange(minimum, maximum); spin.setValue(value)
        self.size_limits.append(spin); form.addRow(label, spin)
    if not algorithm:
        self.discovery_side = QSpinBox(); self.discovery_side.setRange(4, 64); self.discovery_side.setValue(12)
        self.discovery_area = QSpinBox(); self.discovery_area.setRange(16, 1008); self.discovery_area.setSingleStep(16); self.discovery_area.setValue(64)
        self.discovery_side.setEnabled(False); self.discovery_area.setEnabled(False)
        form.addRow("最小有效短边 px", self.discovery_side)
        form.addRow("最小有效面积 px", self.discovery_area)
    hint = QLabel("仅统计选定颜色，其他颜色忽略；最多同时跟踪4个目标。\n同一目标越线计一次。\n框：绿=良品，红=次品，灰=暂时失联。\n尺寸单位为像素，需固定机位标定。参数变化会开始新一批计数。")
    hint.setWordWrap(True); form.addRow(hint)
    self.inspection_hint = hint
    roi_apply = QPushButton("应用检测参数")
    self.roi_apply = roi_apply
    form.addRow(roi_apply)
    clear_counts = QPushButton("清零计数与轨迹")
    self.clear_counts_button = clear_counts
    form.addRow(clear_counts)
    self.roi_label = QLabel("算法展示：等待板端确认" if algorithm else "小球工业检测：等待板端结果")
    self.roi_label.setWordWrap(True)
    controls.addWidget(self.roi_box)

    self.upload_box = QGroupBox("04  图片上传 · Ethernet")
    form = QVBoxLayout(self.upload_box)
    hint = QLabel("自动转为 1920×1080 RGB565\nFPGA 回放适配至现有 1280×720 算法链")
    hint.setObjectName("muted")
    form.addWidget(hint)
    self.upload_button = QPushButton("选择图片并上传")
    if algorithm: self.upload_button.clicked.connect(self.choose_image)
    form.addWidget(self.upload_button)
    self.progress = QProgressBar()
    form.addWidget(self.progress)
    self.cancel_button = QPushButton("取消上传")
    self.cancel_button.setEnabled(False)
    if algorithm: self.cancel_button.clicked.connect(lambda: self.worker and self.worker.cancel_event.set())
    form.addWidget(self.cancel_button)
    controls.addWidget(self.upload_box)
    self.application_box = QGroupBox("05  小球工业检测 · 板端状态")
    application_layout = QVBoxLayout(self.application_box)
    self.profile_notice = QLabel("算法展示工程：启用原算法切换、图像编辑和上传；人脸、小球与工业参数区不可用。" if algorithm else
        "等待工业参数能力确认；新协议握手后可在03区通过Ethernet应用参数并回读。旧bit保持只读。")
    self.profile_notice.setWordWrap(True); application_layout.addWidget(self.profile_notice)
    self.application_status = QLabel("本工程不含人脸解锁与小球计数功能" if algorithm else "当前模式：等待板端确认")
    self.application_status.setWordWrap(True); application_layout.addWidget(self.application_status)
    self.keys_hint = QLabel("等待板端能力确认；旧bit按其原操作说明使用按键。")
    keys = self.keys_hint
    keys.setWordWrap(True); application_layout.addWidget(keys)
    self.application_box.setEnabled(not algorithm)
    controls.addWidget(self.application_box)
    if combined:
        self.view_switch_button = QPushButton("切换到小球识别")
        self.view_switch_button.clicked.connect(self.toggle_view)
        self.view_switch_button.setEnabled(False)
        controls.addWidget(self.view_switch_button)
    controls.addStretch()

    right = QWidget()
    preview_layout = QVBoxLayout(right)
    preview_layout.setContentsMargins(8, 0, 0, 0)
    self.preview_label = QLabel("等待 FPGA 图像\n\n连接千兆网线，确认 PHY 为 1000M 全双工\n图像来自 FPGA HDMI 输出，无需 HDMI 采集卡")
    self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.preview_label.setMinimumSize(640, 360)
    self.preview_label.setStyleSheet("background:#090f15;border:1px solid #29414f;border-radius:8px;color:#728c9e;")
    preview_layout.addWidget(self.preview_label, 1)
    self.stats_label = QLabel("0.0 fps  ·  0.0 Mb/s  ·  等待图像")
    preview_layout.addWidget(self.stats_label)
    self.video_info = QLabel("视频frameID：—"); preview_layout.addWidget(self.video_info)
    inspection_banner = QGroupBox("板端结果 · FPGA")
    banner_layout = QVBoxLayout(inspection_banner)
    self.roi_label.setStyleSheet("color:#a8ead8;font-size:14px;padding:3px;")
    self.summary = self.roi_label
    self.summary.setMinimumHeight(self.summary.fontMetrics().lineSpacing()*2+10)
    banner_layout.addWidget(self.roi_label)
    self.face_label = QLabel("人脸与小球：本工程未启用" if algorithm else "板端状态：等待确认")
    self.face_label.setWordWrap(True)
    self.face_label.setMinimumHeight(self.face_label.fontMetrics().lineSpacing()*2+4)
    banner_layout.addWidget(self.face_label)
    self.targets = QTableWidget(4,5)
    self.targets.setHorizontalHeaderLabels(["槽位","颜色","状态","中心 (x,y)","边界 (左,上,右,下)"])
    self.targets.verticalHeader().hide()
    self.targets.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.targets.setSelectionMode(QAbstractItemView.NoSelection)
    self.targets.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    self.targets.horizontalHeader().setMinimumSectionSize(50)
    self.targets.horizontalHeader().setStretchLastSection(True)
    self.targets.verticalHeader().setDefaultSectionSize(22)
    self.targets.setFixedHeight(116); self.targets.setEnabled(not algorithm)
    for row in range(4):
        for column in range(5):
            self.targets.setItem(row,column,QTableWidgetItem(str(row+1) if column==0 else "—"))
    banner_layout.addWidget(self.targets)
    preview_layout.addWidget(inspection_banner)
    buttons = QHBoxLayout()
    self.preview_check = QCheckBox("显示实时图像")
    self.preview_check.setChecked(True)
    self.preview_check.setToolTip("取消后仅冻结本机画面，网络接收和结果更新继续")
    buttons.addWidget(self.preview_check)
    self.record = QCheckBox("记录JSONL")
    if not algorithm: self.record.toggled.connect(self.toggle_recording)
    self.record.setEnabled(not algorithm)
    self.record.setToolTip("记录板端结构化检测结果；算法展示工程请使用 PNG 保存")
    buttons.addWidget(self.record)
    buttons.addStretch()
    self.screenshot = QPushButton("保存当前完整帧")
    self.screenshot.clicked.connect(self.save_frame)
    self.screenshot.setEnabled(False)
    buttons.addWidget(self.screenshot)
    self.query = QPushButton("查询硬件状态")
    self.query.clicked.connect(self.query_state)
    self.query.setEnabled(False); buttons.addWidget(self.query)
    preview_layout.addLayout(buttons)
    self.notice = QLabel("视频编号和状态序号分别计数；不代表视频与检测结果逐帧对应。")
    self.notice.setWordWrap(True); preview_layout.addWidget(self.notice)
    tabs = QTabWidget(); tabs.setMaximumHeight(95)
    self.log_view = QPlainTextEdit()
    self.log_view.setReadOnly(True)
    self.log_view.setMaximumBlockCount(300)
    self.log_view.setMaximumHeight(160)
    tabs.addTab(self.log_view,"运行日志")
    self.details = QPlainTextEdit(); self.details.setReadOnly(True)
    tabs.addTab(self.details,"完整结果 JSON"); preview_layout.addWidget(tabs)
    splitter.addWidget(right)
    splitter.setStretchFactor(1, 1)
    splitter.setSizes([410, 970])
    if combined:
        self.setWindowTitle("HX1P35A · 合并候选／尚无配套bit")
        self.subtitle.setText("千兆以太网 · 算法展示 / 小球工业检测（帧边界切换）")
        self.algorithm_box.setTitle("02  算法与输入源 · Ethernet")
    self.setCentralWidget(root)
    self.setStyleSheet(STYLE)
    self.roi_box.setEnabled(False)
    self.roi_box.setToolTip("保留原工业检测参数布局；这两套工程不提供工业参数写入")
    if not algorithm:
        self.ports.setEnabled(False)
        self.ports.setToolTip("本版通过以太网接收视频和结果；此串口行仅保留原页面布局")
        self.algorithm_box.setEnabled(False); self.upload_box.setEnabled(False)
        self.algorithm_box.setToolTip("本版不支持算法切换与图像编辑；实际模式见下方板端状态区域")
        self.upload_box.setToolTip("本版不支持图片上传或 PC Image 回放")
        self.state_label.setText("实际模式 / 输入源：本版未提供原算法控制")


def adjustment_row(self, algorithm, form, label, low, high, initial, scale):
    row = QHBoxLayout()
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(low, high)
    slider.setValue(initial)
    spin = QDoubleSpinBox()
    spin.setRange(low / scale, high / scale)
    spin.setDecimals(2 if scale == 100 else 0)
    spin.setSingleStep(1 / scale)
    spin.setValue(initial / scale)
    spin.setFixedWidth(78)
    def changed(value):
        spin.blockSignals(True)
        spin.setValue(value / scale)
        spin.blockSignals(False)
        if algorithm: self.tone_timer.start()
    slider.valueChanged.connect(changed)
    spin.valueChanged.connect(lambda value: slider.setValue(round(value * scale)))
    row.addWidget(slider, 1)
    row.addWidget(spin)
    form.addRow(label, row)
    return slider

