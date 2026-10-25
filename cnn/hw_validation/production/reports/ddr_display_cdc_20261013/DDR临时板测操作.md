# HX1P35A：DDR 临时 SRAM/JTAG 自检

这次测真实 DDR，不是之前的三套 CNN 算术自检。电脑端已完成独立实现及位流生成；尚未替你连接或操作开发板。

## 1. 选择正确文件

新测试文件：

`E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/ddr_display_cdc_20261013/diagnostic_bitgen_attempt2/HX1P35A_C7_DDR_DIAG.bit`

大小 1,789,542 字节；SHA256：

`9250eadc204e53da4bf4d211dc7d662c3937c251b49433875be869e2a0b3ffdc`

不要选旧 `HX1P35A_C7_SELFTEST.bit`：两者通过时都可能显示绿色 TEST，必须按文件名区分。

## 2. 加载与观察

1. 断电接好 JTAG、HDMI1 和显示器，再正常供电。暂时不需要摄像头。
2. 打开你上次使用的安路下载工具，检测到同一块 PH1P35 器件后，选择 **SRAM / JTAG 临时下载**，载入上述新 `.bit`。不要选择 Program Flash、Erase Flash 或修改启动配置。
3. 完成下载后观察：左上角 TEST；运行中背景黄色，成功为绿色，失败为红色；右上角蓝色心跳应持续变化。顶部黑白条是诊断数据，不是花屏。
4. 成功状态表示本次两套互补数据的 **8 次写入、8 次读回比较**成功。测试结束后背景保持绿色；蓝色心跳继续，不代表 DDR 一直循环压力测试。
5. 按板上 **K4 复位**三次，每次松开后应重新测试并回到绿色。随后保持供电和显示 10 分钟，记录是否花屏、失去心跳或状态异常。
6. 给我一张新绿色画面照片，最好附一段包含 K4 复位、恢复绿色和心跳的视频，并说明“3 次复位通过 / 保持 10 分钟稳定”。我再登记实际板测，不提前填写通过。

如果红色、一直黄色超过约 10 秒，或无显示：不要反复换工程、写 Flash。拍下完整画面，告诉我下载文件、等待时间、K4 后状态；红色诊断条用于定位首个错误。该异常不自动等于 DDR 芯片损坏。

## 3. 恢复之前的计算自检

仍用 **SRAM/JTAG** 重新加载原文件：

`E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/board_test_20261010/HX1P35A_C7_SELFTEST.bit`

旧文件 SHA256：`57e675018a96fb3e360733c84bc56bacf3cd29f4806843f2d39d77c09dd293c7`。旧文件未覆盖。

SRAM 临时配置掉电不保留，既有 Flash 内容本轮没有修改。

## 4. 通过意味着什么

只证明这个小范围、独占 DDR 的实际写读测试成功。不证明全容量、CNN 保留区、视频与 DMA 并发、完整 CNN 识别、5 FPS 或精度达标。外部接口时序与严格代码门禁仍单列未签核；详细数据见 `DDR显示CDC_时序闭合与板测交付报告.md`。
