# 小球 + 人脸位置检测 Python 原型

默认先用传统 Haar 检测人脸，连续 3 次有效结果后开启原有小球追踪/计数。只判断有人脸，不识别身份。
本目录是 Python 算法和数据流实验，尚未加入 FPGA RTL，也未生成新 bit。

## 回退点

完整原工程：`E:\project\ball_checkpoints\ball_before_face_20261019_211252`

逐文件 SHA256 清单：同级 `ball_before_face_20261019_211252_manifest.json`。
创建时 2,922 文件、1,827,391,972 字节，全数校验通过。
原小球源文件和上板文件不作修改；实验全部放在新增的 `python_face` 中。
需要回退时，可直接打开备份目录中的原工程；不要把新旧目录的综合结果混用。

## 运行

依赖已安装的 Python、OpenCV、NumPy；无需额外下载模型，模型和照片已放入 assets。
在本目录终端运行（本机 Python 位于 `D:\Python313\python.exe`）：

```powershell
python main.py
python main.py --mode track
python main.py --source 0 --face-every 1
python main.py --source "D:\path\input.mp4" --record
python main.py --headless --frames 360 --output output\count
python main.py --demo-color-face --mode track
python main.py --simultaneous
python test_face_gate.py
python test_combined.py
```

也可双击 `启动小球与人脸模拟.cmd`。默认运行人脸启动门禁，选 track/count 不会绕过门禁。
按键：1 小球追踪，2 小球计数，M 颜色掩膜，T 分割阈值，C 仅清零，R 复位并重新等待人脸，空格暂停，Q 退出。
普通模式切换、阈值调整和 C 清零均保留解锁状态；重新启动程序或 R 才会要求再次检测人脸。
`--simultaneous` 保留上一版两路同时检测的行为，用于对比回归。
摄像头仅在用户选择 `--source 0` 后打开。

默认输出位于 `output/gate`，包含 `simulation.mp4`、`frame_trace.csv`、`summary.json`、`preview.png`、等待/解锁截图和末帧图。
录像固定 24 fps，只是播放速度；summary 中 host_processing_fps 是本机处理速度，均不是 FPGA 帧率。

## 实际处理通路

```text
1280x720 输入 RGB → 等待人脸（小球分析、追踪和计数全部暂停）
    → 缩小为 320x180 → 灰度 → 实际 Haar 分类器
    → 连续 3 次检测有人脸 → 锁存解锁，下一输入帧开启小球通路
    → 原小球 ROI / 颜色 / 连通域 / 追踪或去重计数
    → 上一完整检测结果画框 → RGB128 打包 → 双帧 DDR 模型 → HDMI 输出
```

人脸默认每 2 帧检测一次（`--face-every`）。只累加实际检测结果，跳过帧不增加次数；任一次实际检测无人脸就清零连续次数。
连续指检测批次，不要求同一张人脸，不含身份识别或活体判断。
解锁后停止调用 Haar，不要求人脸继续留在画面。画面显示 `BALL ENABLED`，等待时显示 `WAIT FACE`。
解锁时清除旧检测状态、坐标及计数；计数模式必须先等门区连续 3 帧为空，才接收新球。
解锁时已在门区的球不会被计数；人脸离开后，小球正常继续计数。
R 复位会清除解锁、坐标、计数以及 DDR 旧画面缓存；程序重新进入等待状态。
每个人脸结果携带输入帧号，CSV 记录实际显示的源帧、小球结果帧、人脸结果帧；框在 DDR 写入前叠加。
复用原小球模型的前一检测帧显示规则和 DDR 一帧延迟，属于功能模型，不是时钟级 RTL 仿真。
人脸是青色框，小球沿用红、绿、黄框。
默认最小人脸窗口 24x24，相当于原图约 96x96；需要看更小人脸可试 `--face-width 640`，处理量随之增加。

## 演示和边界

演示把公共领域真实人脸照片和合成小球放入同一输入帧，算法从像素重新检测，未读取场景真值坐标。
默认门禁演示：前 40 帧无人脸（期间已有红球过线，应保持 0）；第 40～63 帧显示真实照片以触发 Haar，随后人脸离开；从第 70 帧起运行原来的 6 球用例，含停留和短时漏检。
门禁演示默认 430 帧，目标结果为红、绿、黄各 2 次。`--simultaneous` 仍使用原来 360 帧组合用例。
默认照片转成灰度以验证两个分支独立工作；这不代表已解决真实肤色干扰。
`--demo-color-face` 可复现彩色照片情况：Haar 能找到人脸，但原小球颜色算法会把部分肤色当成红/黄候选，可能抢占小球追踪或干扰计数。
视频和摄像头输入保持真实颜色。门禁流程减少两路同时运行，但人脸在解锁后仍留在小球 ROI 内时，肤色干扰仍然存在；应在解锁后让人脸离开检测区域。不能仅凭这份演示宣称已解决肤色误检。
此 Haar 原型主要验证正面人脸，对小脸、侧脸、遮挡、暗光和快速运动没有准确率保证；跳帧缓存也会造成框滞后。
320x180 灰度帧为 57,600 字节，但 FPGA 总存储还取决于积分图、平方和、金字塔、模型和调度。
本轮没有测得新增 FPGA LUT / ERAM / DSP / 时序占用，不能据 Python 结果保证与小球合并后资源足够。

## 测试材料来源

- 分类器来自本机 OpenCV 4.13.0 `cv2/data/haarcascade_frontalface_default.xml`；原 XML 中的 Intel 许可头完整保留。
  [OpenCV 官方分类器说明](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)。
- `astronaut.png` 来自 [scikit-image v0.20.0 官方仓库](https://raw.githubusercontent.com/scikit-image/scikit-image/v0.20.0/skimage/data/astronaut.png)。
  [官方数据说明](https://scikit-image.org/docs/0.20.x/api/skimage.data.html#skimage.data.astronaut) 标明照片源自 NASA，属于公共领域。
- 这里只用照片验证“是否有人脸、位置在哪里”，未提取身份信息。
