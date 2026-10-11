# VG153 动态 unpacked array 驱动事实闭合

## Assumption

本修复把 VG153 保持为声明根级的 `read_without_driver` 门禁，不把它扩展为逐元素初始化、控制流覆盖或通用 Verilog 编译器。动态 unpacked array 元素写入可证明“该声明根存在过程驱动”，但不能证明每个元素在每条路径上均已初始化；通过信息和测试 JSON 均显式保留这一边界。

目标目录不是 Git 仓库，因此没有当前分支可记录。本轮只修改 checker overlay、目标测试和本说明，没有修改 RTL、全局 skill 或原 checker overlay。

## 旧行为复现

真实 `down2_overlap_tile_runner.v` 的 formatter AST 已提供以下事实：

- `reg_halo`、`reg_dw_cache`、`reg_output_cache` 都是带 `unpacked` 范围的 `reg` 声明；
- `reg_dw_cache[wire_dw_cache_write_address]` 与 `reg_halo[i_load_addr]` 进入 `comb_expressions`，并携带 `dynamic lvalue selection is not a static endpoint`；
- 嵌套选择的 `reg_output_cache[pp_output_tag[14:11] * 24 + pp_output_tag[10:6]]` 已存在于 formatter 的 `always.lvalues`，对应声明根存在于 `always.targets`；
- 旧 VG153 的驱动集合却只保存完整左值字符串，三个声明根均不在驱动集合，而读取集合包含三个声明根，因此产生假 `undriven`。

旧实现复现实收据为 `tests/array_driver_original.json`。其中动态数组与真实 runner 三个目标根均未满足目标断言；该收据只用于旧行为对照，不代表原目录的全门禁状态。

## Changed

`vg_contract_liveness.py` 新增一个局部归一化步骤，完全消费既有 formatter AST：

1. 只接受声明事实明确带 `unpacked` 的对象；packed bus 不适用。
2. 使用同一 `always` 的 `targets` 和 `lvalues` 绑定元素写入与声明根，不按信号名白名单。
3. 只有单一 unpacked 维度且左值恰好是完整元素时才考虑提升；元素内 packed select 和多维选择均保留旧诊断。
4. selector 复用既有常量与 expression 事实：based literal、parameter/localparam 常量只记录对应元素；只有已确认含运行期信号的完整 selector 才作为动态根驱动。
5. 静态全覆盖使用边界、去重计数、最小值和最大值验证，不按声明深度构造可能巨大的完整 range 集合。
6. 未写 array、只写一个常量元素却读另一个元素、packed partial write、未知模块接口、多实例输出冲突以及模块间同名信号仍由原规则阻断。

没有新增 parser、依赖、RTL 修改或门禁豁免。

## Verified

执行命令：

```text
python -B -X utf8 tests/check_array_driver.py --overlay checker_overlay --output tests/array_driver_results_v2.json
```

结果：退出码 0，`all_passed=true`，`cases` 含 14 个 `{passed, result}` 对象。旧 `array_driver_results.json` 保留未覆盖；v2 JSON 同时记录每个 fixture、真实源文件、测试脚本和实际导入模块的 SHA256。

| 目标语义 | 结果 |
|---|---|
| 动态 unpacked element 写入 + 动态索引读取 | 通过；声明根不再误报 |
| 静态范围内全部常量元素写入 | 通过 |
| 完全未写 array | VG153 failed |
| 仅写 `array[0]`、读取 `array[1]` | VG153 failed |
| packed `[7:0]` 只写 `[3:0]`、读取整总线 | VG153 failed |
| array 索引由未驱动内部信号提供 | array 根通过，索引信号 VG153 failed |
| 未知子模块输出 | VG153 failed |
| 两个已知子模块同时驱动同一 actual | VG153 failed，保留 `unresolved_instance_output` |
| 不同 module 内同名 array，仅一处有驱动 | 未驱动 module 继续 failed |
| based constant 只写一个 array element | VG153 failed |
| parameter constant 只写一个 array element | VG153 failed |
| 动态 array element 的 packed 部分写 | VG153 failed |
| 多维 array 的局部写 | VG153 failed |
| 真实 runner 的三个目标 array | 三个目标符号均不再出现；整体 VG153 仍因其他符号 failed |

本测试只断言 VG153 目标语义。`compile`、`ast`、`readability`、`comment`、`naming`、`profile`、`testbench`、`toolchain` 八项公开交付矩阵未在此窄测试中重跑，不能据此宣称严格门禁或部署通过。未运行训练、仿真、综合、TD 或板级流程。

## Remaining risk

动态索引根事实不等价于逐元素初始化覆盖；需要该证明时应新增独立的数据流/控制流规则，而不是扩大 VG153。当前测试已保留可确认的常量元素错配负例，防止声明根归一化掩盖显式未驱动元素。
