# croc_gemm_obi：接口和最小修复契约

本轮只修复独立 IP 的 Icarus 展开兼容问题，不改变 OBI/MMIO 功能。
源码仍使用 `croc_pkg::sbr_obi_req_t` 和 `sbr_obi_rsp_t`，真实 SoC
集成必须换用官方包，不能把 `tb/croc_pkg_stub.sv` 放入 SoC。

| 端口 | 方向 | 契约 |
|---|---|---|
| `clk_i` | 输入 | 上升沿采样请求并更新响应 |
| `rst_ni` | 输入 | 低有效异步复位，清除响应寄存器和 leaf 状态 |
| `obi_req_i` | 输入 | 官方请求类型，使用 `req/addr/we/be/wdata/aid` |
| `obi_rsp_o` | 输出 | 官方响应类型，返回 `gnt/rvalid/rdata/rid/err` |

- `req && gnt` 才接受请求；只容许一个在途事务。
- 接受边沿后 `rvalid=1`、`gnt=0`，数据/错误和原 `aid` 保存在响应中。
- 下一上升沿完成响应并恢复 `gnt=1`；选定接口没有 `rready`。
- 地址窗口为 `[0x20001000, 0x20002000)`；只接受对齐的 32 位访问。
- 写入必须 `be=1111`；非法地址/未映射/非对齐/部分写返回 `err=1`
  且不触发 leaf。计算忙时的合法矩阵写是 leaf 的 sticky error，OBI 仍正常响应。
- `CTRL=0x00`：bit0 启动，bit1 清 done/error；`STATUS=0x04`：
  bit0 busy、bit1 done、bit2 error。A/B 行字分别为 `0x10..0x1c`
  和 `0x20..0x2c`，C 的 16 个有符号 INT32 元素为 `0x40..0x7c`。
- A/B 每字低字节对应列 0；输入有符号 INT8，四项乘加累加到 INT32。
  启动后依次清累加器、完成四次 MAC，再置 done，done 保持到清除或下次启动。

## 响应时序

| 时刻 | `req` | `gnt` | `rvalid` | 行为 |
|---|---|---|---|---|
| E0 边沿前 | 1 | 1 | 0 | 请求稳定 |
| E0 边沿后 | 1 | 0 | 1 | 已接受，返回该请求的 `rid/data/err` |
| E1 边沿后 | 可为下一请求 | 1 | 0 | 上一响应完成 |
| E2 边沿 | 1 | 1 | 0 | 接受下一请求 |

WaveJSON（每列表示边沿后的状态；接受事件位于第 2、4 列之前）：

```json
{"signal":[{"name":"clk_i","wave":"p...."},{"name":"req","wave":"01..."},{"name":"gnt","wave":"10101"},{"name":"rvalid","wave":"01010"},{"name":"rid","wave":"x=x=x","data":["ID A","ID B"]}]}
```

修复点仅为：响应寄存器宽度通过 `$bits` 查询真实端口成员，替代
Icarus 不接受的配置结构字段常量；将嵌套 packed struct 的 `we/wdata`
经 1 位/32 位中间 wire 接入现有 leaf，避免错误的 74 位端口展开。
协议端口、复位、req/gnt、rvalid、ID 和响应延迟均保持不变。

## 可运行检查与边界

`python scripts/validate.py --strict`：先运行静态模板集成和独立协议模型，
再分别编译运行功能 TB 和压力 TB。功能 TB 对两次连续任务的 32 个输出
逐项计算黄金值，第二组含非单位矩阵、负数、-128/127 和 65536 累加结果；
压力 TB 检查背压、ID、非法访问、副作用隔离、忙写和严格事务计数。

这些检查没有证明官方 CPU/交叉开关系统集成、随机全覆盖、形式等价、
CDC、综合、ASIC 时序、功耗或板上行为。当前运行结果以
`reports/summary.json` 和同次阶段日志为准。
