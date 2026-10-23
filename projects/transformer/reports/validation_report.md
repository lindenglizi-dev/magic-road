# Lesson 15 门禁实测报告（2026-10-23）

| 门禁项 | 状态 | 说明 |
|---|---|---|
| reference | PASS | 从 X/W 重算 QKV，再算 Attention/FFN，573 个值；`reference.log` |
| contracts | PASS | 源文本结构、稀疏 Bank 镜像；不证明 HDL 声明；`contracts.log` |
| check_contracts | PASS | 84 个布局断言；`check_contracts.log` |
| mac_compile / mac_rtl | PASS | 实际 Icarus 编译，定向与 120 拍随机/停顿；`mac_rtl.log` |
| top_compile | PASS | 实际 Icarus elaboration 与编译，返回码 0；`top_compile.log` |
| rtl_demo | PASS | L=2 D=4 F=6，7 次 GEMM，244 cycles；`rtl_demo.log` |
| rtl_edge_5x7 | PASS | L=5 D=7 F=9，7 次 GEMM，1178 cycles；`rtl_edge_5x7.log` |
| rtl_random_00 | PASS | L=1 D=9 F=5，7 次 GEMM，486 cycles；`rtl_random_00.log` |
| rtl_sat_1x1 | PASS | L=1 D=1 F=3，7 次 GEMM，139 cycles；`rtl_sat_1x1.log` |

**最终：`RTL_PASS`**，以 `summary.json` 的命令、返回码、UTC 时间为准。执行环境：Windows 宿主进程，Python 3.13，Icarus 12.0 (devel) / vvp。

运行命令（工作区根目录）：`python projects/transformer/scripts/validate.py --strict`。Windows 沙箱执行曾出现 Icarus 驱动崩溃；宿主执行同一命令返回 0。先前失败的源码编译日志保存在 `before_repair/`，不作为通过证据。没有忽略编译返回码或使用崩溃遗留产物跳过编译。

本轮修复：TB 三组输出数据未声明；GEMM 双维动态数组索引触发 Icarus 内部断言，现用 `16*bank+offset` 等价索引；静态检查澄清名字出现不代表有效声明。补 Q/Key 最终物理 Bank 对拍、X/W 到 QKV 的独立参考重算；无需修改控制 FSM 或定点规则。

覆盖：原始四组小例中，QKV 原始值和量化值、Score、P、PV、ACT、Hidden、Final、7 次发射顺序、写回次数、地址范围以及 Q/Key/V/ACT/Hidden 物理 Bank。周期统计从释放复位开始，含启动前空拍，不是物理时钟证据。

边界：固定一周期读响应、写入始终接受。未证明任意存储延迟/反压、维度上界、完整系统多任务/复位中断、部署精度、ASIC SRAM 映射、频率、面积、功耗、DRC/LVS 或 GDSII；风格门禁另行报告，不能用本功能通过替代。
