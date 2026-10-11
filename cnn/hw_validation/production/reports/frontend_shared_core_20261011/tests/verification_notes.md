# 验证说明

## PH1P ERAM 仿真模型告警

`tb_shared_core_control` 优化阶段出现以下两条 ModelSim 告警：

```text
ph1p_logic_eram.v(165): (vopt-2697) MSB 172095 of part-select into 'INIT_FILE' is out of bounds.
ph1p_logic_eram.v(165): (vopt-2697) LSB 172024 of part-select into 'INIT_FILE' is out of bounds.
```

告警发生在 `Design is being optimized...` 之后、设计加载和仿真 time 0 之前，没有对应运行时刻或 A/B 口地址。172095 和 172024 是厂商加密模型对 `INIT_FILE` 参数的静态 part-select 索引，不是 10 位查表地址。对应唯一实例为：

```text
tb_shared_core_control.dut.u_pp.u_silu.PH1P_LOGIC_ERAM_Inst_silu_table
```

该实例参数为 20 位数据、10 位地址、深度 1024、`INIT_FILE="NONE"`。旧 `stem_down2_handoff_20261011` 仿真中每个 SiLU ERAM 实例也出现同一对告警；旧双实例共四条，共享核单实例为两条。

控制测试随后实际完成两次完整 1024 项顺序装表、写回反压、运行中复位、完整重装和 256 项恢复导出，未观察到运行地址或数值错误。这个结果只界定当前仿真路径，告警仍保留为厂商模型和物理实现风险，不能据此证明硅上 RAM 初始化或碰撞语义。

## 只读协议复核

- `done` 高电平同拍由 `!o_done` 阻止 select/load/start/table，下一拍由 `flag_unexported` 继续阻止，最后导出后才可切换；未见缺口。
- 复位异步清除所有权、未导出和地址故障，并同时复位两个调度器及算术链；逻辑 `table_loaded` 清零，调用者必须重装表；未见旧 valid 泄漏。
- Stem 高地址只在公共 load 握手时置粘滞故障，且不会送入 9 位调度器；故障后 select/load/start/table 均被封锁，属于预期行为。
- 复核曾发现持续 `i_select_valid` 阻止旧主 export 的循环等待；已删除原始选择 valid 对旧主命令的封锁，专项测试保持 valid 直到真实换主成功。
- 复核曾发现持续 `i_table_valid` 阻止共享 PP 排空的循环等待；已仅将实际准入的 table_valid 送入 PP，专项测试覆盖运行中提前请求、旧表保持、导出完成后接受和全表重装。
- select 握手后仍改变 `i_select_down2`、或在一个周期同时要求互斥命令，属于调用者 payload/命令稳定性违约；顶层按握手当拍值采样，没有发现额外状态破坏。

## 首次实际综合暴露的结构闭环

`physical/td_launcher.log` 保留 TMR-2509/2507：空闲→装表使能→PP ready→down2同拍credit/pop→MAC valid→空闲。工具自动切环后的结果不可签核，因此主动停止该诊断，没有使用其后续时序。

局部修复仅从空闲判定删除 `s_mac_valid/d_mac_valid`：Stem 的 load_ready 要求 ST_IDLE、MAC valid 要求 ST_SEND；down2 的 load_ready 要求 ST_IDLE，发射 valid 要求 DW/PW 发射状态。因此两项冗余，删除不改变合法准入。全量 TB 新增逐拍 `load_ready -> !mac_valid` 断言；实际工具必须再次确认无组合环。原源码快照在 `simulation_attempt4/sources`，原失败 manifest/log 不覆盖。
