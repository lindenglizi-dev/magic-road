# 基础校验结果

> 仓库范围说明（2026-10-16）：本文是原始技术/验证记录，正文保留。其引用的原始日志、历史bit、第三方PDF或个人DOCX仅保留在本地，不随源仓库提交；这些本地附件不能视为GitHub中的可下载文件。历史结果不替代当前版本的实板验收。

日期：2026-10-04 16:42（新增识别结果文字、统一帧状态后的版本）。原工程保留不变，应用目录为 `applications/color_traffic`。

| 项目 | 结果 |
|---|---|
| Vivado 2022.2 RTL 编译、展开 | 通过 |
| 16帧原检测功能仿真 | 通过 |
| 8帧1280×720 OSD集成仿真 | 通过，逐字比较1382400个DDR字 |
| 工程依赖/三份源清单/引脚检查 | 通过 |
| TD 6.2.168116 原厂整工程综合 | 通过 |
| TD 布局布线、保持时间修复、bitgen | 通过 |
| 最终建立时间 SWNS / STNS | +0.120 ns / 0.000 ns |
| 最终保持时间 HWNS / HTNS | +0.020 ns / 0.000 ns |
| 上板摄像头实测 | 尚未执行 |

仿真在160×64图像、ROI `[40,160)×[8,64)` 上运行，每个全色目标期望命中6720像素，覆盖了末拍累计。每帧检查10240像素、1920个DDR字、64行、1个帧首和帧末，并逐字比对打包顺序；输入含行内空拍。序列覆盖红、绿、黄、白、黑、蓝，验证三帧投票、目标消失、交通灯排除蓝色、模式改变清空历史、严格阈值。另进行8帧1280×720 OSD集成仿真，逐字检查从未知到“识别为：红灯”、模式切换后清空到未知、再次积累后“识别为：红色”，同时检查logo、中英文名称、原状态块与ROI、DDR数据及行帧标记。KEY0在帧中请求切换，下一帧才更新模式和显示；旧结果不会带入新模式。未进行实拍准确率评估或按键/OSD穷举测试。

仿真证据：`../sim/result.log`，结尾为 `PASS color traffic: 16 frames, ROI counts, voting, presets, blanking, markers and DDR bytes`。

OSD证据：`../sim/osd_result.log`，结尾 `PASS OSD runtime`。`osd_actual_preview.png`（红灯）和 `osd_color_preview.png`（红色）来自RTL实际DDR输出的顶部160行，已目视检查。核心增加 `O_display_result` / `O_display_traffic` 输出，文字与原色块共用同一帧快照；runtime移除重复的模式寄存器。按键消抖、阈值、投票和计数逻辑保持不变。

首次8帧仿真全部断言通过后，Vivado仿真器在退出阶段发生一次 `EXCEPTION_ACCESS_VIOLATION`；未修改RTL，对同一快照复跑后再次全部通过并以退出码0正常结束，最终日志已保存。未把异常退出当作通过。

工程检查证据：`source_audit.json` 保存新增 RTL 的 SHA256 及相对原工程修改清单。三个 TD 文件清单都包含新增模块且各出现一次，所有引用均位于应用目录内。原工程仅修改 `isp_top.v`、`design_top_wrapper.v`、`pin.adc` 的副本。

综合报告新增 `u_application` 层级：1233 logic LUT、338 ripple、945 seq、4 ERAM、0 DSP；这些是综合估计数，不是独立布局资源占用。

最终报告：`../td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_pr.timing`。STA coverage 为95.27%，沿用原工程约束；正裕量表示在这些约束覆盖的路径上通过，不能代替板级实测。OSD沿用原三级流水同步传递数据和行帧标记；提前帧通知仍单独延迟一拍，原约束未修改。

TD 日志仍包含 PLL 非时钟IO、部分时钟使用局部布线及原IP RAM未驱动端口等警告，本次未更改原时钟/IP结构，也未通过放宽时序约束掩盖问题。完整日志保存在 syn_1/phy_1 的 `console.log`。

下载文件（16:42:25生成）：

- `../td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.bit`，1789539字节。
- `../td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_compress.bit`，1361841字节。

本次只做基础功能仿真、依赖检查和一次正常实现，没有进行强对抗测试。真实目标、曝光、阈值和按键手感按《上板演示记录》留待上板确认。
