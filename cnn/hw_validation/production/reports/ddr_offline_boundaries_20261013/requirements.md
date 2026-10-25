# DDR 离线边界与排空验证

本轮只给冻结的单请求桥补验证，不改桥、计算核、生产工程或旧板测位流。真实 DDR 写完成和容量仍等待板测。

## 顺序和通过条件

1. 冻结旧基线和生产源码；Python 生成地址与 mask 参考，先通过自检。
2. 对新 testbench 执行严格八项门禁并保留结果；诊断仿真与生产交付分开。
3. 原桥回归复跑。新测试逐项对拍：无停顿、固定种子随机停顿、长停顿三种模式；合法地址全部写完后逆序读，互补数据再跑一轮；非法地址不允许产生控制器请求。
4. 定向取消覆盖各请求及返回阶段；已呈现 VALID 必须保持直到接受，取消不能提前释放所有权。延迟返回只能被原 owner 排空，不能冒充新结果。
5. 整理 CNN 接入表，区分可直接复用的接口与真实控制器尚未闭合的写完成条件。

## 冻结合同

- 范围 `[0x03400000,0x04000000)`、16 字节对齐、128 位单拍、native 地址为 byte 地址右移 1。
- little endian，mask 位 1 表示禁止该 byte lane 写入。
- req valid/ready 只接受一个 owner/epoch；AW/W 各自遵守 ready，AW 接受后下一拍呈现 W。
- 模拟端点确实应用写入之后，才发独立 commit 事件。该事件只是测试假设，不是实际厂商信号。
- 读返回不早于 AR 接受的下一拍；单拍 RLAST 必须为 1；保留一个完整返回槽。
- result 无 cancel 时在 ready 前保持；cancel 是上下游共同放弃结果的显式 flush。
- 硬复位只模拟桥与端点协调复位；不证明桥单独复位后可吞掉真实 DDR 晚返回。
- 沿用已有模块接口，不增加 DMA、UART、FIFO、动态量化参数、时序例外。

## 文件与工具

`reference.py` 产生向量；`tests/tb_paxi_boundary_mask.v` 驱动原桥；`run.py` 复用前轮本地命令与日志工具。所有工作和输出目录限定在本目录，每次仿真新建 attempt 目录，不覆盖失败记录。

Verilog 任务类别为 generate testbench 和 validate unchanged RTL。八门为 compile、ast、readability、comment、naming、profile、testbench、toolchain。严格结果原样保留，不以 ModelSim 通过替代格式及交付门；不为端口为空的 testbench 伪造端口以迎合规范工具。

当前环境没有 readable-python-generator 和 readable-script-generator；Python 使用标准库 AST、自检和真实执行验证，不宣称缺失的技能门已通过。没有新增运行依赖。功能成功仍不等于真实 DDR、资源时序或完整 CNN 验收。
