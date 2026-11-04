# ball_components 模块规范

> RTL: `rtl/ball_components.v`

## 1. 模块目的

四像素采集与双帧4x4同色区域分离，输出有界候选及拒绝诊断。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_WIDTH | 1280 | 每行像素数，必须为16的倍数 |
| C_HEIGHT | 720 | 帧有效像素行数 |
| C_X_MIN | 64 | ROI左边界，包含 |
| C_Y_MIN | 160 | ROI上边界，包含 |
| C_X_END | 1216 | ROI右边界，不包含 |
| C_Y_END | 640 | ROI下边界，不包含 |
| C_GATE_MIN | 544 | 计数门左边界，包含；运行层传给占用检测 |
| C_GATE_END | 736 | 计数门右边界，不包含；运行层传给占用检测 |
| C_MIN_AREA | 128 | 连通区域有效同色像素最小面积，也用于疑似门占用 |
| C_MIN_SIZE | 12 | 候选框宽高最小像素数 |
| C_MAX_SIZE | 384 | 候选框宽高最大像素数 |
| C_MAX_CANDIDATES | 8 | 每帧可接受候选上限，超限整帧无效 |
| C_QUEUE_BITS | 12 | 四邻域队列地址位宽，深度为2的此值次方 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_rstn` | input | 1 | i_clk | reset | asynchronous active-low reset |
| `i_valid` | input | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `i_sof` | input | 1 | i_clk | native | first valid group of a frame |
| `i_eof` | input | 1 | i_clk | native | last valid group of a frame |
| `i_x` | input | (11)-(0)+1 | i_clk | native | Native application interface field i_x; see module behavior and source connections |
| `i_y` | input | (11)-(0)+1 | i_clk | native | Native application interface field i_y; see module behavior and source connections |
| `i_labels` | input | (7)-(0)+1 | i_clk | native | four exclusive two-bit labels, lane zero in bits 1:0; 0 unknown,1 red,2 yellow,3 green |
| `i_gate_hits` | input | (2)-(0)+1 | i_clk | native | Native application interface field i_gate_hits; see module behavior and source connections |
| `i_epoch` | input | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_frame_start` | output | 1 | i_clk | native | start collecting metadata for a completed capture frame scan |
| `o_candidate_valid` | output | 1 | i_clk | native | one candidate on this clock; frame_done follows all candidates |
| `o_color` | output | (1)-(0)+1 | i_clk | native | 0 unknown,1 red,2 yellow,3 green |
| `o_area` | output | (19)-(0)+1 | i_clk | native | number of classified pixels in the candidate |
| `o_x_min` | output | (11)-(0)+1 | i_clk | native | inclusive left edge of candidate |
| `o_x_max` | output | (11)-(0)+1 | i_clk | native | inclusive right edge of candidate |
| `o_y_min` | output | (11)-(0)+1 | i_clk | native | inclusive top edge of candidate |
| `o_y_max` | output | (11)-(0)+1 | i_clk | native | inclusive bottom edge of candidate |
| `o_frame_done` | output | 1 | i_clk | native | complete statistics pulse, including frames with no candidates |
| `o_gate_pixels` | output | (19)-(0)+1 | i_clk | native | classified raw pixel count in the full rectangular counting gate |
| `o_epoch` | output | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_overflow` | output | 1 | i_clk | native | more than eight accepted segments in this frame |
| `o_fault` | output | 1 | i_clk | native | dropped or overlapping statistics event; must not count as empty gate |
| `o_error` | output | 1 | i_clk | native | sticky video/statistics protocol diagnostic |
| `o_diag_count` | output | 4 | i_clk | native | Accepted candidate count, <=8 |
| `o_diag_width` | output | 12 | i_clk | native | Width of the largest completed same-color region |
| `o_diag_height` | output | 12 | i_clk | native | Height of the largest completed same-color region |
| `o_diag_area` | output | 20 | i_clk | native | Retained winning-color pixel area of the largest region |
| `o_diag_fill` | output | 7 | i_clk | native | Floor of 100*area/bbox_area, 0..100 |
| `o_diag_reject` | output | 4 | i_clk | native | Rejection bitmask:1 area,2 dimensions,4 aspect,8 fill |
| `o_gate_occupied` | output | 1 | i_clk | native | Completed-frame gate footprint: at least one same-color connected region with classified area >= C_MIN_AREA and bbox overlapping [C_GATE_MIN,C_GATE_END), including shape/size-rejected regions. Read only with frame_done/epoch; overflow/fault has priority. |

## 5. 周期行为与延迟

- Four labels per valid clock are accumulated into cropped 4x4 ROI cells. Retain the winning color only with >=4 pixels and >=75% of colored support. Store 2-bit color plus 5-bit winning count.
- Synchronous row histogram RAM and two frame RAMs have no array reset. Each full capture overwrites every ROI cell; coordinates advance only with input valid.
- Begin analysis after the last ROI cell write, not necessarily global EOF. Four-neighbor BFS clears each cell when queued, processes each retained cell once, and scans seeds in row-major order.
- The 4096-entry queue is finite; queue overflow or >8 accepted regions sets frame overflow. All partial candidates become invalid at frame_done. Busy bank/request collision emits fault and sticky error.
- Bounds cover occupied cells and clamp to ROI. Area sums winning-color pixels. Keep existing minimum area, size, 2:1 aspect and >=25% fill filters. Same-color touching objects remain merged.
- All region statistics and largest-region diagnostics belong to one captured epoch. Fill is integer percentage from bounded repeated subtraction at the end of analysis.
- Raw o_gate_pixels is unchanged. New o_gate_occupied resets on scan start, latches during ST_REGION_FILTER for a region area>=C_MIN_AREA and bbox gate overlap, irrespective of shape/size rejection. Isolated sub-threshold regions never add together to assert it. Gate Y equals ROI Y; runtime propagates gate X parameters.

## 6. WaveDrom 时序图

### ROI capture and region-result ordering

Compressed logical frame events only, not measured clock timing. Multicandidate frame blocks; three subsequent sparse-only complete frames release; two upstream matches then downstream count once. Rejected substantial regions hold occupied.

![ROI capture and region-result ordering](waveforms/ball_components_compressed-event-order.svg)

- WaveJSON：[ball_components_compressed-event-order.json5](waveforms/ball_components_compressed-event-order.json5)

## 7. 边界、反压与错误

- Partial first/last ROI cells and final incomplete image row must be written once.
- Invalid bubbles do not duplicate gate counts or cell input. Raw gate occupancy remains unchanged.
- A bad/overflow frame cannot provide new counting events or empty-gate evidence.
- A cleared processing bank may only be reused after its job ends; dropped capture frames cannot overwrite it.

## 8. CDC 与综合约束

- Anlogic PH1P35MDG324/-3, synthesizable Verilog-2001; no video backpressure or pixel-path latency change.
- W>=16 and divisible by16; valid ROI within 12-bit image bounds. ROI cell count <=65536 and ROI pixel area <2^20. Default ROI64,160..1216,640 has34560 cells.
- C_QUEUE_BITS>=1, default12; C_MAX_CANDIDATES in1..8. Four-connected cells quantize occupied-cell edges by up to3 pixels; support filtering may remove small tips.
- Worst-case processing bound <=40*ROI_cells+128 clocks. At103.520MHz and720P60, default budget is1725333 clocks; measured stress traces are separate evidence. Dense frames may miss the immediately following display boundary.
- C_GATE_MIN/C_GATE_END define gate X; gate Y is the whole ROI. Occupancy uses bounding-box intersection conservatively, not exact in-gate area. No new RAM/scan cycles/video pipeline stages.

## 9. 验证与验收

- sim/test_gate_recovery.py + tb_ball_gate_recovery.v:45frames; old frame6 staysGATE4/ERR2, new releases after3sparse128pxframes; rejected192pxregion holds, dropout/dedup/samecolor nextball, wrongcolor/overflow block.
- Existing 16component masks, partialROI/queue/collision, 6frameoverflow,206framemotion,28frameruntime and720P60 budget rerun.
- tb_ball_count_hdmi.v + check_count_hdmi.py:7full720Pframes, persistent sparse noise, yellow upstream/downstream counts1; actual capture and COUNT2 glyph.

## 10. 可追溯性

- 规格模块：`ball_components`
- RTL 路径：`rtl/ball_components.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
