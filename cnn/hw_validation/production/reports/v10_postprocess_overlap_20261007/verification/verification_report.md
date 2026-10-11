# v10 后处理重叠流水功能验证报告

## 结论

候选 RTL 的功能回归通过；20M cycle/frame 条件预算未满足。最终可信日志是 runner `vsim_attempt4.log` 和 standalone `vsim_postprocess_attempt4.log`。旧失败与覆盖不足日志均保留，不计入通过证据。

## 候选功能覆盖

- standalone：连续 5 组、固定气泡 3 组、固定种子随机 48 组/96 scalar、长固定反压、满信用、表重载、末组故障、通道系数切换、24 个真实 pipeline age 复位全部通过。
- 随机流：gap seed `0x1d0f`，ready seed `0xace1`，实际输入空拍 175、输出 not-ready 67；源在握手前稳定，tag-indexed scoreboard 无丢失、重复或逐值错误。
- 反压空流水窗口：ready 撤销 edge 2140，最后新增组接受 edge 2167，响应 28 edges；新增 10 组/30 scalar，随后连续拒绝 43 拍直到 release。
- 已有 tail-valid 窗口：edge 4632 到最后新增组 edge 4650，响应 19 edges；新增 7 组/21 scalar，连续拒绝 52 拍。
- 两窗口最大占用均为 result FIFO 2、pre 9、meta 6、post 9；最大 scalar obligations 分别 30/29；held output 保持稳定。
- 标量时序：pre accept 在 t，`o_output_valid` 在 t+23 posedge 的 NBA 更新后可见；ready 时首次合法 transfer 是 t+24 edge。两段 round 各 9 stage，SiLU 6 stage，忙周期相互重叠不能相加。
- 原 SiLU 65536 测试的 `latency=5` 是其 after-NBA 采样口径，对应 6 个注册推进 edge，与本设计 6-stage 定义不冲突。
- 表重载请求可以在 `global empty && table_ready` 成立的同一 edge forward，无需额外多等一拍；已接受的旧表结果先完全排空，无混表。

## 同向量 runner 结果

| 版本 | full | DW | PW |
|---|---:|---:|---:|
| v8 原串行 | 27393 | 13312 | 14081 |
| v9 MAC + 原串行 runner | 23937 | 11008 | 12929 |
| v10 overlap，无停顿 | 5431 | 3611 | 1820 |

v10 的 384 个 G=2 job 在 MAC 状态窗口内是 5376 cycles。前四个 job 逐拍都为 `2 ST_STORAGE + 2 ST_MAC_SEND + 10 ST_MAC_WAIT = 14`，每个接受两组。互斥端点恒等式是 `5376 MAC + 54 drain + 1 start = 5431`。`storage_wait=0` 只表示没有 commit/credit 等待；每 job 的两个 ST_STORAGE 已包含在 5376 中。pre=3712、SiLU=2560、post=3712、writeback=640 是并行忙观察，绝不能与 MAC 相加。

case 2 使用 seed `0x5eed` 的随机 commit-ready：ready-low 1300 cycles，其中 212 cycles 与有效输出相撞；所有 640 个阶段值和最终值仍通过。无停顿计时只取 case 0/1，不与随机 case 混合。

## 原回归复跑

- v9 MAC：123 vectors、17 results、9 faults、II1 97、9 bubbles、9 resets，PASS，0 errors/0 warnings。
- v9 低 IO：原 14 项 PASS；reset 6 项 PASS。
- round：7042 cases、14084 intermediate、1278 stalls、5 faults、checksum `00014ec4`，PASS。
- SiLU：65536 inputs、latency 5、II1、3072 legal writes、0 stale output errors，PASS。
- v8 四层与 v9-serial 同向量四层均 PASS。所有复制输入逐文件 SHA-256 一致；ModelSim 仅有两条既有 PH1P INIT_FILE part-select warning，无 readmem/fopen 缺失。

## 67 层条件预算

冻结图共 67 个 conv：61 个 SiLU-active、6 个 bypass；激活值 6,833,664，旁路值 84,672。以实测 G=2 job 拟合 `2G+10` 后，job cadence 外推为 63,660,672 cycles；按 DW 27、PW/stem 28 的实测边界条件外推增加 1,853，合计 63,662,525，超过 20M 预算 43,662,525。

这不是整帧实测或硬下界：只有 down2 DW/PW、G=2 实测；G>2、6 个 activation bypass 层的边界均是条件外推，且不含 DDR、非卷积、decode、NMS、preload、export。

下一项推荐的单变量实验是 wrapper product/shift/tag 边界增加一级弹性寄存，以先处理物理实现的 setup 风险；它不降低上述 frame-cycle 外推，会增加 1 拍 latency，最大 scalar obligation 必须重新测定并证明（可能由 30 升到 31），同时重证 tag、反压和全部复位年龄。本轮没有实现或证明该方案。runner 连续 group issue 的条件收益约 9,024,192 cycles/frame，但会改变调度/接口时序，暂后置。MAC 末组单 context 周转涉及算术核；三通道 DW 打包则需让共享 8 输入跨多组覆盖 27 个通道专属激活项，并适配对角权重、调度和存储，不能当免费三 lane 并行，也不在本轮改动内。

## 保留的非通过证据

- runner attempt1：TB 负沿观察与 ready 更新竞争，post 仅计 605/640；修复仅在 TB。
- standalone attempt1：NBA 可见时刻和合法同拍 table forward 的断言口径错误。
- standalone attempt2：共享全局 index 使 24-age 循环覆盖失真，已降级；attempt3 修复真实复位，但尚无随机气泡；attempt4 才是最终证据。
- Python reference 初版错误钳位 SiLU address 1024；最终版直接读取冻结表并对该点返回 2047。
