# 道路视频离线 RTL 回放指南

## 1. 视频采集要求

- 回放转换器只接受1280×720，以逐位复用 FPGA 的移位灰度和每5像素抽样。其他分辨率先通过 `tools/prepare_public_video.py` 生成可追溯的720p派生视频。
- 25 fps 或 30 fps，正式跟踪测试应保留原始帧率，不要抽帧。
- 每段 10～20 秒，镜头和焦距固定，不要剪辑、变焦或切换机位。
- 开头至少保留 1～2 秒完全空场景，让背景模型稳定。
- 人或车辆应从画外进入并完整离开，而不是第一帧就停在画面中央。
- 行人高度建议至少 50 个原视频像素；车辆宽度建议至少 50 个像素。目标太小，缩到 256×144 后不足以分类。
- 尽量保留地面、道路和固定参照物；避免大面积拍摄天空。
- 每段只突出一个变量，并记录场景名称、时间、天气、目标数量和运动方向。

建议准备以下六段：

1. `A_empty`：空场景，测试背景稳定性和误检。
2. `B_person`：单人横穿，完整进出画面。
3. `C_vehicle`：单车横穿，完整进出画面。
4. `D_person_vehicle`：人车同时出现或路径交叉。
5. `E_occlusion`：目标被树、柱子或另一目标短暂遮挡。
6. `F_interference`：树叶、阴影、亮度变化等干扰。

## 2. 视频转换

在工程根目录执行：

```powershell
python .\tools\video_to_gray_frames.py D:\videos\B_person.mp4 .\video_cases\B_person
```

快速检查可以限制帧数：

```powershell
python .\tools\video_to_gray_frames.py D:\videos\B_person.mp4 .\video_cases\B_person_smoke --max-frames 30
```

正式跟踪测试不要设置较低的 `--target-fps`，否则相邻帧目标位移会变大，测试条件与板上实时视频不一致。

转换器不会用 OpenCV 通用灰度或面积缩放，也不会在 FPS 缺失时猜测30 fps。输出目录包含：

- `frame_0000.hex` 等256×144灰度帧；
- `manifest.json`，记录源文件 SHA-256、原分辨率、帧率、预处理版本、导出帧数以及回放帧到源帧的映射。

## 3. RTL 回放

```powershell
.\tests\run_video_replay.ps1 -FrameDir .\video_cases\B_person -Threshold 20
```

脚本默认在分析行之间插入1280个空闲时钟，用来模拟5倍纵向降采样时跳过的4个源图行。不要为了加速正式验证而把 `-RowGap` 改成0，否则可能得到板上不会出现的CCL处理超时。

可先只运行前60帧：

```powershell
.\tests\run_video_replay.ps1 -FrameDir .\video_cases\B_person -Frames 60 -Threshold 20
```

默认结果写入视频帧目录下的 `rtl_results`：

- `frame_summary.csv`：每帧目标数、背景状态、溢出和协议错误；
- `objects.csv`：CCL和几何分类结果；
- `tracks.csv`：轨迹ID、类别、框、速度和确认状态；
- `events.csv`：越线、进入区域和滞留事件；
- `mask_XXXX.hex`：每帧前景二值图。

## 4. 生成带框视频

```powershell
python .\tools\render_rtl_results.py `
  .\video_cases\B_person `
  .\video_cases\B_person\rtl_results `
  .\video_cases\B_person_rtl.mp4
```

颜色约定：行人绿色、车辆青色、未知类别洋红色；细框表示暂未确认，粗框表示已确认轨迹。

## 5. 第一轮验收标准

- 空场景连续100帧不应持续产生有效目标。
- `core_error` 和各 `protocol_error` 必须始终为0。
- `run_overflow`、`label_overflow`、`raw_overrun` 不应频繁出现。
- 单目标连续出现时，轨迹ID应保持一致，框不应随机跳跃。
- 人车分类允许暂时不准，但必须能看到稳定目标框，之后再调整几何阈值或替换分类器。

当前离线回放直接测试 `foreground_ccl_top`，不包含MIPI、ISP、DDR和HDMI物理链路；这些部分需要拿到板卡后验证。
