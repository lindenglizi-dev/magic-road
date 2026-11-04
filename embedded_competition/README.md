# 嵌赛多算法视觉与彩球分检项目

本目录整理本次安路 FPGA 嵌赛的最终成品、独立功能工程和开发参考资料。所有目录均从已有工程复制，保留原始文件字节；不改硬件逻辑、协议、约束或已有位流。仓库原有世界模型项目继续保留在根目录，RoadYOLO 研究继续保留在 [work/roadyolo 分支](https://github.com/lindenglizi-dev/magic-road/tree/work/roadyolo)。

## 首次使用

从 [最终成品](final/README.md) 开始：安路 PH1P35，模式 0～9 图像处理、模式 10 彩球分检、以太网上位机。

- TD 工程：[final/td_project/ball_face.al](final/td_project/ball_face.al)。
- 上位机：[安装环境.cmd](final/安装环境.cmd)，然后运行 [启动上位机.cmd](final/启动上位机.cmd)。
- 位流：[ball_algorithm_gui_managed.bit](final/output/ball_algorithm_gui_managed.bit)。
- [操作手册](final/docs/操作手册.md)、[构建说明](final/docs/构建说明.md)、[资源与时序证据](final/docs/implementation_20261102/README.md)。

最终成品来源于 `lindenglizi-dev/qiansai_anlu_fpga-vision-ethernet` 的 `main@c4eb773fe23394d7882e4e8497499175a5102bbf`，与 2026-11-02 整理包的 351 个发布文件逐字节一致。该版本新位流尚未上板验证，setup 最差裕量仅 +0.001 ns；发布不代表实板验收完成。

## 独立成果

| 工程 | 用途与状态 |
| --- | --- |
| [独立四球计数](legacy/ball/ball_counter/README.md) | TRACK/COUNT4、按颜色跨线去重计数；保留原发布固件与测试。 |
| [人脸门禁与小球](legacy/ball/ball_face_standalone/README.md) | 人脸位置检测解锁后进入彩球检测；保留独立工程及原发布证据。 |
| [旋转检测](legacy/ball/fpga/applications/ball_rotation/release/README.md) | 单标记、固定轴条件下测方向、RPM与圈数。以 release/manifest.json 为准：已有候选 bit，SWNS +0.103 ns、HWNS +0.020 ns，待上板验证。根 README 中“无新 bit”等段落为较早历史。 |
| [旧 UART 算法与图片回放](legacy/ball/fpga/applications/stage3_7_uart/README.md) | 保存 UART V2、静态图上传/DDR重放的独立功能；不能与最终以太网版本混配协议或固件。 |
| [颜色与交通灯](legacy/ball/fpga/applications/color_traffic/README.md) | 独立颜色/交通灯算法历史。 |

这些工程保留各自的厂商 IP、ROM、约束与依赖路径。相同文件的不同依赖路径没有合并成共享库；Git 会复用相同内容对象。独立工程的历史说明、测试结果与已知限制继续保留，不将它们合并解释为最终成品的验收结论。

## 参考模型与工具

- [小球 Python 模型](legacy/ball/python_sim/README.md)、[人脸模型](legacy/ball/python_face/README.md)、[定点人脸模型](legacy/ball/python_face_fixed/README.md)。
- [静态人脸参考工具](research/pc_face_detection/README.md)、[SVM/YOLOX 诊断程序](research/svm_video_detector/)、[模型到 RTL 导出示例](research/nn_rtl_bridge/README.md)。
- [早期接口与审计说明](research/integration_notes/)。其中示例接口和绝对路径属于相应历史阶段，不是当前部署承诺。
- [工程报告原稿](docs/工程报告_竞赛指标版.docx)、[可编辑框架图及配图](docs/figures/)、[报告补充证据](docs/report_evidence/)。报告原稿只做原样归档，本次未编辑版式。

## 完整性与验证

在仓库根目录运行：

```powershell
python embedded_competition/verify_snapshot.py
python embedded_competition/final/scripts/verify_package.py
```

[source_manifest.csv](source_manifest.csv) 记录逐文件来源、大小和 SHA256；[发布核验记录](validation.json)区分本轮检查与原构建证据。测试依赖和命令见各工程说明。历史工程有部分机器绝对路径和失效的历史报告链接；本次只检查实际发布文件、显式 TD 工程依赖及选定回归，不声称所有历史脚本均已适配新电脑。

可再生成的仿真采集帧、预期帧、运行缓存、数据库、原始视频、全部训练检查点和重复日期快照未收录。UART 的 sim/make_vectors.py、交通灯的 sim/make_osd_vectors.py、四球的 sim/test_multi.py 负责生成对应测试输入。六套工程源码和主要依赖保留；完整物理重建、GUI离线回归和上板状态以发布核验记录为准。

第三方声明、许可证、原厂加密代码与保护指令保留：[最终成品第三方说明](final/THIRD_PARTY_NOTICES.md)、[人脸资源说明](legacy/ball/ball_face_standalone/docs/第三方资源.md)。本次不为第三方代码另设统一许可证。

## 大文件恢复

[公开资源获取与自有权重备份](recovery/README.md)记录数据/工具来源、原下载校验值、环境版本和训练检查点恢复入口。未核实可恢复的人工标签、旧版工具及原工程依赖继续保留；链接清单不等于已完成数据恢复测试。
