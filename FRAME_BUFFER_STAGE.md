# 双帧灰度缓存阶段说明

## 本阶段结果

已经在官方Lab1总顶层内加入可供后续ROI/HOG分类器使用的双时钟灰度帧缓存，而不是另建一个脱离工程的演示模块。

```text
SC500/ISP AWB旁路（摄像头时钟域）
        │
        ├─ awb96_analysis_adapter ─ 256×144灰度流 ─ CCL/跟踪/事件
        │                                  │
        │                                  └─ gray_frame_pingpong
        │                                       ├─ bank0：18×ERAM20K
        │                                       └─ bank1：18×ERAM20K
        │                                                │
        └─ 原DDR/HDMI显示链保持不变                    100 MHz算法读口
                                                         │
                                                  roi_frame_reader
                                                  （32×32 ROI流）
```

## 文件职责

- `gray_frame_bank_ram.v`：把一帧拆成18个2048×8原生ERAM；摄像头口写，100 MHz口读。
- `gray_frame_pingpong.v`：管理两bank所有权、帧发布CDC、地址/行帧协议校验和冲突丢帧。
- `gray_frame_probe_reader.v`：上一阶段使用的全帧读口验证器，现已由ROI读取器取代并保留作独立诊断模块。
- `design_top_wrapper.v`：把缓存接到真实分析灰度流，并把错误与完成状态接回系统诊断。
- `road_status_overlay.v`：第四个状态块显示读帧校验值；以后可改为分类器状态。
- `tb_gray_frame_pingpong.v`：验证正常读回、错误帧不发布、bank保护、丢帧和恢复。

## 接口约定

写侧沿用分析流：`wr_valid/gray/x/y/sof/eol/eof`。写入地址由坐标生成，不依赖自由递增计数器；计数器只用于协议核验。

读侧采用请求/响应：算法先等待 `rd_frame_ready` 并取得 `rd_frame_bank/frame_id`，持有期间用 `rd_req_valid + rd_req_addr` 发请求，收到 `rd_rsp_valid + rd_rsp_gray`；整帧或所需ROI处理完成后拉高 `rd_release` 一个周期。

## 实测结果

- 六组Icarus RTL回归全部通过。
- Tang Dynasty完整综合、布局、布线成功。
- Slice 16,174 / 21,216（76.23%）。
- ERAM20K 94 / 108（87.04%）。
- DSP 9 / 40（22.50%）。
- Setup SWNS +1.061 ns；Hold HWNS +0.020 ns；均无违例。

## 后续阶段边界

当前已经以候选框为单位读取ROI，不再扫描整帧。单目标读取1024像素，100 MHz下约10.24 μs；四目标约40.96 μs。仅剩14块ERAM，因此后续HOG特征与权重必须采用流式/小缓存结构。
