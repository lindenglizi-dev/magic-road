import json
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,
    QPushButton,QSpinBox,QCheckBox,QComboBox,QFileDialog)
from communication.image_protocol import RoiConfig,Capability,COLOR_NAMES
from services.roi_geometry import Roi

class RoiPanel(QWidget):
    def __init__(self,controller,view,log,settings):
        super().__init__();self.controller=controller;self.view=view;self.log=log;self.settings=settings
        self.width,self.height=1280,720
        layout=QVBoxLayout(self);row=QHBoxLayout();layout.addLayout(row)
        self.enabled=QCheckBox('启用ROI');self.enabled.setChecked(True)
        self.traffic=QComboBox();self.traffic.addItem('交通灯（红/黄/绿）',True);self.traffic.addItem('四色检测（含蓝）',False)
        self.strict=QComboBox();self.strict.addItem('原有普通阈值',False);self.strict.addItem('原有严格阈值',True)
        self.overlay=QCheckBox('显示GUI操作框');self.overlay.setChecked(True)
        self.hdmi_border=QCheckBox('显示FPGA ROI边框');self.hdmi_border.setChecked(True)
        for widget in (self.enabled,self.traffic,self.strict,self.overlay,self.hdmi_border):row.addWidget(widget)
        grid=QGridLayout();layout.addLayout(grid);self.coords=[]
        for index,label in enumerate(('X1','Y1','X2（不含）','Y2（不含）')):
            widget=QSpinBox();widget.setRange(0,self.width if index%2==0 else self.height)
            self.coords.append(widget);grid.addWidget(QLabel(label),0,index);grid.addWidget(widget,1,index)
            widget.valueChanged.connect(self._draft_changed)
        self.state=QLabel('固件能力未确认；只能编辑草稿，不能应用');layout.addWidget(self.state)
        self.applied_label=QLabel('FPGA已应用区域：未知');layout.addWidget(self.applied_label)
        self.result=QLabel('FPGA检测结果：等待数据');self.result.setWordWrap(True);layout.addWidget(self.result)
        row=QHBoxLayout();layout.addLayout(row)
        select=QPushButton('框选ROI');clear=QPushButton('清除操作框');self.apply_button=QPushButton('应用ROI')
        self.read_button=QPushButton('读取FPGA参数');save=QPushButton('保存配置');load=QPushButton('加载配置');default=QPushButton('恢复默认ROI')
        for widget in (select,clear,self.apply_button,self.read_button,save,load,default):row.addWidget(widget)
        info=QLabel('坐标原点为FPGA图像左上角；区域为[X1,X2)×[Y1,Y2)，单位为单像素。GUI边框不代表硬件已应用。\n'
                    '颜色判定、最小像素128、优势像素差32沿用现有RTL；不在Python中识别颜色。')
        info.setWordWrap(True);layout.addWidget(info);layout.addStretch()
        select.clicked.connect(self.select);clear.clicked.connect(self.clear)
        self.apply_button.clicked.connect(self.apply);self.read_button.clicked.connect(self.query)
        save.clicked.connect(self.save);load.clicked.connect(self.load);default.clicked.connect(self.defaults)
        self.overlay.toggled.connect(self._overlay)
        self.enabled.toggled.connect(self._draft_changed)
        self.traffic.currentIndexChanged.connect(self._draft_changed)
        self.strict.currentIndexChanged.connect(self._draft_changed)
        self.hdmi_border.toggled.connect(self._draft_changed)
        controller.device_changed.connect(self.device_changed)
        controller.roi.state.connect(self.state.setText);controller.roi.changed.connect(self.received)
        view.roi_selected.connect(self.selected)
        self.defaults();self.device_changed(None)
        self.poll=QTimer(self);self.poll.setInterval(1000);self.poll.timeout.connect(self.poll_status);self.poll.start()

    def config(self):
        return RoiConfig(Roi(*(w.value() for w in self.coords)),self.enabled.isChecked(),
                         bool(self.traffic.currentData()),bool(self.strict.currentData()),self.hdmi_border.isChecked())

    def _draft_changed(self):
        self.view.confirmed=False;self.view.result_text='草稿，未应用'
        try:self.view.roi=self.config().roi.validate(self.width,self.height)
        except ValueError:self.view.roi=None
        self.view.update()

    def _overlay(self,enabled):self.view.overlay_enabled=enabled;self.view.update()

    def defaults(self):
        self.set_coords(Roi(self.width*3//8,self.height//4,self.width*5//8,self.height*3//4))

    def set_coords(self,roi):
        for widget,value in zip(self.coords,(roi.x0,roi.y0,roi.x1,roi.y1)):widget.setValue(value)
        self._draft_changed()

    def selected(self,roi):self.set_coords(roi)

    def select(self):
        try:self.view.geometry_map()
        except ValueError as exc:self.log('ROI：'+str(exc));return
        self.view.selecting=True;self.state.setText('在实际画面内容中拖动；松开后仍需点击应用ROI')

    def clear(self):
        self.view.roi=None;self.view.start=self.view.end=None;self.view.selecting=False;self.view.update()
        self.state.setText('只清除了GUI操作框；FPGA配置未改变')

    def apply(self):
        try:self.controller.roi.apply(self.config())
        except (ValueError,RuntimeError) as exc:self.log('ROI：'+str(exc))

    def query(self):
        try:self.controller.roi.query()
        except (ValueError,RuntimeError) as exc:self.log('ROI：'+str(exc))

    def poll_status(self):
        if self.apply_button.isEnabled() and not self.controller.scheduler.active and not self.controller.scheduler.exclusive:self.query()

    def device_changed(self,status):
        available=bool(status and status.capabilities&Capability.ROI)
        self.apply_button.setEnabled(available);self.read_button.setEnabled(available)
        if status:
            self.width,self.height=status.width,status.height;self.view.source_size=(self.width,self.height)
            for index,widget in enumerate(self.coords):widget.setMaximum(self.width if index%2==0 else self.height)
        else:
            self.view.confirmed=False;self.view.result_text='硬件未确认';self.view.update()
            self.applied_label.setText('FPGA已应用区域：未知');self.result.setText('FPGA检测结果：等待数据')

    def received(self,status):
        r=status.config.roi
        self.applied_label.setText(f'FPGA已应用：({r.x0},{r.y0})→({r.x1},{r.y1})，rev={status.revision}，帧={status.frame}')
        state='已关闭' if not status.config.enabled else ('预热/等待完整帧' if not status.warmed_up else ('检测有效' if status.result else '无有效目标'))
        self.result.setText(f'FPGA结果：{COLOR_NAMES[status.result]} · {state} · {datetime.now():%H:%M:%S}\n'
                            f'像素统计 R/Y/G/B={status.counts}')
        if self.view.roi is not None and self.config()==status.config:
            self.view.roi=r;self.view.confirmed=True;self.view.result_text=COLOR_NAMES[status.result]+'（FPGA）';self.view.update()
        elif self.view.roi is not None:
            self.view.confirmed=False;self.view.result_text='草稿，与FPGA已应用区域不同';self.view.update()

    def save(self):
        filename,_=QFileDialog.getSaveFileName(self,'保存ROI配置','roi_config.json','JSON (*.json)')
        if not filename:return
        try:
            c=self.config();c.roi.validate(self.width,self.height)
            obj={'schema':1,'source_width':self.width,'source_height':self.height,
                 'roi':[c.roi.x0,c.roi.y0,c.roi.x1,c.roi.y1],'enabled':c.enabled,'traffic':c.traffic,'strict':c.strict,'border':c.border}
            Path(filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');self.log('ROI配置已保存：'+filename)
        except (ValueError,OSError) as exc:self.log('ROI：'+str(exc))

    def load(self):
        filename,_=QFileDialog.getOpenFileName(self,'加载ROI配置','','JSON (*.json)')
        if not filename:return
        try:
            data=json.loads(Path(filename).read_text(encoding='utf-8'))
            if data.get('schema')!=1 or (data['source_width'],data['source_height'])!=(self.width,self.height):
                raise ValueError('ROI配置源尺寸与当前FPGA不一致；不会自动缩放应用')
            r=Roi(*data['roi']).validate(self.width,self.height)
            self.enabled.setChecked(bool(data['enabled']));self.traffic.setCurrentIndex(0 if data['traffic'] else 1)
            self.strict.setCurrentIndex(1 if data['strict'] else 0);self.hdmi_border.setChecked(bool(data.get('border',True)));self.set_coords(r)
            self.state.setText('配置已加载为草稿，尚未发送FPGA')
        except (ValueError,KeyError,TypeError,OSError) as exc:self.log('ROI加载失败：'+str(exc))
