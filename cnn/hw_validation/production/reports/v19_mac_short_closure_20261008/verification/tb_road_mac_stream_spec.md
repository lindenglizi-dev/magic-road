# tb_road_mac_stream 诊断规格

无端口仿真根，参数MAX_VECTORS=160，内部10ns时钟与异步低有效复位，实例为真实候选road_mac_probe。读取冻结123行`stream_vectors.txt`，在输入握手时登记，在接受后c4检查dot、c5检查signed34 candidate与signed33反馈、c6检查安全保持结果，输出消费后检查ready重新开放。

数值期望不变；只将发布断言9→6，并将删除的三项内部valid观察替换为常量0，不为DUT添加兼容寄存器。边界覆盖最大24组/192乘积、正负暂时INT32超界恢复、最终正负溢出、偏置一次、first重建历史、尾mask、输入气泡、blocked-input、输出保持与原子故障。

增补reset offset0，保留offset1..9，共10次即时取消；恢复后每次15拍无旧结果。`+LONG_HOLD`把17项终态的等待统一延至64拍，输入数值与期望不变。分别保留正常与长反压日志，并与旧核trace按event/case/beat/fault/data比较，忽略时刻和合法延迟差异，不忽略结果。

周期图：[road_mac_probe_stream-terminal.svg](../spec/mac_stream/waveforms/road_mac_probe_stream-terminal.svg)，为DUT契约示意，非采集波形；新核last→发布6拍，最早确认7拍。无端口TB不符合技能write-spec的非空端口要求，本文人工配套，不编造端口，不宣称工具生成的TB规格通过。

本地Icarus行为测试，不替代亚稳态、RAM厂商模型或物理STA；测试结束要求TB_PASS并且零TB_ERROR/TB_FAIL。
