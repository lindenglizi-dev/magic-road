# tb_feature_blocks_client

## 任务和接口

同一个 `road_feature_blocks_client` 和同一个旧 `road_csp_first_probe`，依次接受固定块 ID 2、3、4。顶层仅输出 `o_test_complete`，内部时钟 100MHz、共同低有效异步复位。测试台没有形状配置端口；DUT 根据握手锁存的 4 位 ID 选择固定图。

CSP2 为 72×128、half12、五阶段，CSP3 为 36×64、half24、七阶段，CSP4 为 18×32、half48、七阶段。块间只更换 CPU source、参数和 golden，不复位 DUT 或算术 owner。down3/down4 仍由 CPU 生成，因此顺序运行不是连续 RTL 骨干。

参数 channel/group/layer/window 位宽为 7/5/3/3，参数响应 block 与屏障 block 都为 4 位。旧核心端口保持原样。工作缓存/权重不由 TB 预填；完整覆盖是否正确由每块全幅数值比较证明。

## 可观察行为

- 每块 acc/pre/SiLU/post/sum/output 及地址逐项比较；每个逻辑位置唯一覆盖。
- live memory 只接收 DUT 的真实写，匹配 block/layer 的屏障之后才允许读取；屏障不能用等待拍数替代。
- 单在途、16B 对齐、128 位读；返回地址必须匹配。CSP4 物理 y18/19 返回零且禁止写，不能当作真实输出覆盖。
- CSP2 PW12 末组 mask 为 0f；DW 三点/尾单点和未使能输入、输出 lane 均核验。
- busy 中扰动输入 ID/start，检查输出 ID、固定形状与地址保持；DONE 仍 busy 且 start_ready=0，下一拍 IDLE 才可接受新块。
- 非法 ID15、错参数 responseblock、第一层全部输出后的错 barrierblock 都必须 fault，占有保持且无后续流量。
- 每块输出 17 个互斥状态账本及 5/7/7 个阶段账本；实际读、参数、任务、组、输出、屏障和契约精确一致。

## 场景

`+CASE=0`：一次完整 2→3→4；`+CASE=1`：同序列随机参数/读请求延迟及核/写反压；`+CASE=2`：CSP2 stage2 至少写 128 字节后共同复位、撤销未完成响应、重装 SiLU，再完整 2→3→4。中止片段单列 `FEAT_BLOCK_ABORT`，不计入 clean 完整块。

`+CASE=3`：非法 ID15；`+CASE=4`：第一参数响应携带错误块 ID；`+CASE=5`：完整 stage0 后错误屏障块 ID，不发布该层可见性。

runner case99 实际调用 `+CASE=0 +NEGATIVE_ACC=1`，把第一次真实 acc 检查的期望 XOR1，必须 Fatal 并出现 `NEGATIVE_ACC injected acc mismatch`，不得出现 PASS。

必须传 `+VECTORS_ROOT=<frozen/reference>`；目录下 `csp2/csp3/csp4` 各含 `parameters/` 和 `vectors/`。所有精确字段及 runner 场景见根 `tb_contract.json`。

## 计数和周期端点

完整序列 blocks/runs=3，output/acc/pre/SiLU/post 各 1327104，groups=1612800，tasks=520704，reads=190858，parameters=193920，barriers=19。

逐块 cycles 从接受 start 的上升沿至进入 DONE 的上升沿，含两端；17 状态之和与阶段周期之和均等于 accounted/cycles，接受 start 的 IDLE 拍归 stage0。初次 LUT 加载不计入逐块周期。clean 三块总周期必须小于 100M。

sequence_cycles 从第一次接受 start 至最终 clean IDLE 检查，包含块间控制开销；CASE2 另含中止及重装表。overhead=sequence-clean-aborted，禁止重复相加。唯一 watchdog 为总 130M 周期，覆盖正常三块及复位额外片段。

唯一终局标记为 `FEATURE_BLOCKS_PASS` 或 `FEATURE_BLOCKS_EXPECTED_FAULT`；逐块为 `FEAT_BLOCK_STAGE/STATE/RUN`，都有 block/case/run 归属。

## 时序示意

长计算和中间层省略；DONE 拍的 start 不被接受，下一 IDLE 的 ready 才允许不同块。

```json
{"signal":[
  {"name":"clk","wave":"p........."},
  {"name":"rstn","wave":"1........."},
  {"name":"i_block_id","wave":"=...=...=.","data":["2","15 busy扰动","3"]},
  {"name":"final_barrier_accept","wave":"0...10...."},
  {"name":"o_done","wave":"0....10..."},
  {"name":"o_busy","wave":"1.....01.."},
  {"name":"o_start_ready","wave":"0.....10.."},
  {"name":"i_start","wave":"0....1110."},
  {"name":"o_block_id","wave":"=......=..","data":["2","3"]}
]}
```

## 验证边界

测试作者不运行 ModelSim/TD，由总协调冻结完整源与向量后执行 `python run.py prepare --name <frozen>`、`gate`、`execute --name <frozen> --case <0..5|99>`，不传 -g 参数。

已执行严格静态诊断，原始报告保留在 `tests/gate/` 与实际包含 TB 的 `tests/gate_with_tb/`；后者失败，不能以默认跳过 TB 的 AST/compile 状态宣称静态通过。同名规范 canonical JSON 在 `tests/tb_spec_contract.json`；registered write-spec 在当前受限调用中读取该路径返回 WinError5，需由总协调生成规范化图件。

本测试不证明真实 DDR、4ERAM 映射、资源/时序、完整网络 FPS、QAT/准确率、位流或板卡。
