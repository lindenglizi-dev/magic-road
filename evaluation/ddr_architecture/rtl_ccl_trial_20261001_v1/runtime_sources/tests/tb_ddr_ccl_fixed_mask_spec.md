# `tb_ddr_ccl_fixed_mask` 验证合同

该测试台只验证现有 `rle_ccl_top` 和隔离扫描上界实验，不连接摄像头、DDR、CDC 或显示链。

- 输入为按行优先展开的二值 `readmemb` 文件。首个有效像素携带 SOF；每行像素结束后独立脉冲 EOL；最后一行 `row_done_debug` 后再独立脉冲 EOF。EOL、EOF 均不与 `analysis_valid` 并行。
- 每行 EOL 后等待该行完成，再发送下一行。这是可停顿分析任务的合法驱动，用于排除供数超速；不代表连续相机流吞吐。
- `PIXEL_GAP` 可在有效像素间加入空拍。`WAIT_FRAME_DONE=1` 时，每个正常帧等待 `object_frame_done` 后再发送下一帧。
- `WAIT_FRAME_DONE=0` 是 SOF-busy 故障探针：最后一行完成且 EOF 已发布后，不等待解析/选择完成便发送下一帧。该模式故意违反正常任务所有权，不作为合法输入性能结果。
- 在时钟下降沿记录已经稳定的 `feature_update`、union 请求、对象、父表、最终 feature 与完成状态，避免和上升沿非阻塞赋值竞争。绝对周期单独记录，不参与基线/优化语义日志相等判断。

相对时序：`pixels -> EOL -> row_done -> ... -> final row_done -> EOF -> resolver -> selector -> object_frame_done`。WaveDrom 未渲染；用户已批准使用工程现有 Icarus 执行本地隔离仿真。
