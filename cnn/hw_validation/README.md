# RoadYOLO 首批硬件验证

本目录与生产工程隔离。测试权重不证明识别精度；代表算术不证明整网5 FPS。
不启动训练、不修改生产RTL/模型/厂商IP、不执行配置Flash写入。

## 当前范围与复现

使用项目已有的 road_yolo_venv Python；运行 `baseline.py self-check`、
`baseline.py prepare`、`baseline.py verify`。第一次 prepare 冻结生产输入哈希，
复制已适配720p的独立顶层、生成独立TD项目和布局布线/bitgen脚本。
再次 prepare 不覆盖既有输入。生产IP仅被只读引用。

在 `baseline/` 运行 `td_commands_prompt.exe build.tcl`（工具命令以实测为准）。
工具退出码不等于综合通过：必须检查最终面积、时序、错误日志及位流是否实际生成。
既有模板严格风格门禁的失败记录不能替换成新探针的通过记录。

`settings.json` 由技能默认设置派生，只显式选择本计划批准的本地Icarus/Anlogic工具，
不连接SSH。策略键 `allow_implicit_local_external_validation=true` 是此处工具的
执行开关；本次本地执行来自用户明确指定，不能把它当通用隐式降级许可。
WaveDrom及erie-remote-ssh已获安装许可；推荐依赖和Python/脚本配套技能缺项另记。

## 独立证据

- `reports/production_before.json` 与 `production_after.json`：生产输入是否变化。
- `baseline/`：H0重新实现证据；没有实际观察记录时，10分钟显示/恢复仍未通过。
- `rom/`：H1-A完整测试包、物理ROM、仿真与映射证据。
- `ddr/`：H1-B可控端点协议证据，不等于厂商控制器或板上DDR证明。
- `mac/`：H2小算术参考和对拍，不等于完整层、量化、SiLU或CNN调度通过。
- `td/`：新增探针的独立TD运行；失败日志也保留，进程退出码0不能代替通过。

## 新探针TD放行

`td_probe.py --self-check` 检查失败关闭行为。布局布线前，生产RTL闭包必须通过
严格门禁，且门禁staging副本、原RTL、冻结哈希三者一致；不通过时禁止继续。
工具只读引用厂商原语的接口提取文件用于静态检查，绝不把该文件加入仿真或综合。
`interfaces_extract.py` 修复标准提取器遗漏后置参数的输入排列问题：从官方公开
声明生成清单、机械重排声明并用标准提取器输出，复核全部30个参数值及端口宽度
不变。完整静态接口为`interfaces/ph1p_eram_interface_complete.v`；它仍不包含
加密行为，也没有制造时钟或输出状态边界证明。

裸MAC核心1031组对拍与严格静态检查已通过。直接顶层有465个IO，TD门映射
实际报错超过160个IO；24个乘法宏保留只证明RTL优化结果，不是24个DSP的证据。
新增140-IO动态封装用于后续资源与时序测试，12个32-bit命令字提供全部动态
激活、权重、偏置及控制。封装不代表完整CNN调度，也不能据其周期推算整网5 FPS。

`td_probe.py --gate <闭包门禁.json> --binding <源码绑定.json> --component rom|mac`
生成独立实现输入；ROM另需将构建目录的`artifacts`目录连接到已冻结ROM初始化目录。
脚本目前不生成CNN位流、不含下载命令；部分ROM/MAC通过不能替代67层CNN通过。

## 上板前必须确认

用户已确认板卡暂时不在手上，因此本批不执行任何JTAG下载。
电脑USB枚举不是读取板卡内容；TD布局布线与位流生成也不是板测。

请连接板卡独立供电、JTAG USB、摄像头和HDMI，核对实物丝印型号和JTAG器件。
先确认已生成可恢复720p位流的哈希及其实际显示；只允许JTAG临时加载。
保存至少10分钟HDMI观察记录（开始/结束时间、花屏/错位/中断情况），并实际
重新加载基线确认恢复。未确认连接和恢复之前，不自动下载位流。

DDR仍需厂商确认：PAXI写完成与写后读可见性、NORMAL返回顺序、取消/复位排空、
匹配DDR2 CL7/BL8仿真模型。不能用固定等待拍数、FIFO空或AW/W接受代替提交屏障。
52–64 MiB地址、地址单位和容量末端须实测后才能做视频并发或发布输入READY。
