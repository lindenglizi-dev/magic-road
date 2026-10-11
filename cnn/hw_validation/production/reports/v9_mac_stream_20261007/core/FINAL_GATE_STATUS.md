# road_mac_probe 最终门禁状态

冻结源码 SHA256：`04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51`

## readable-verilog 八项公开状态

来源：`strict_gate_final.json` / `strict_gate_final.md`，`delivery_ready=false`，431 errors，0 strict warnings。

| 门禁 | 状态 | 说明 |
|---|---|---|
| compile | passed | formatter AST/静态解析通过，1 文件、1 模块、0 parse error |
| ast | failed | 11 个 formatter error |
| readability | failed | 420 个 error |
| comment | passed | 0 error，0 warning |
| naming | failed | 125 个 error；与 readability finding 有重叠，不应与总数相加 |
| profile | passed | Erie profile/rulebook 成功加载 |
| testbench | not_requested | 本次 strict 调用未包含 TB；独立 ModelSim 结果见下 |
| toolchain | not_requested | strict 调用未请求外部工具；独立 ModelSim 结果见下 |

主要 finding 计数：VG015=93、VG020=10、VG060=1、VG061=32、VG062=190、VG066=20、VG068=1、VG070=3、VG088 inconclusive=1、VG138=3、VG145=10、VG146=44、VG156=12。规则未放宽，详细分类见 `SEMANTIC_RISK_CLASSIFICATION.md`。

## 独立执行证据

- ModelSim stream：`TB_PASS_MAC_STREAM vectors=123 accepts=123 dots=123 candidates=123 results=17 faults=9 ii1=97 bubbles=9 resets=9 ghost_window=135 latency=9`，0 error / 0 warning。
- ModelSim layer：正确读入冻结候选，`TB_PASS_DOWN2_TILE cases=4`，0 error / 0 warning；case 0..2 的 `dw_core=11008`、`pw_core=12929`、`core=23937`，case 3 仅 pointwise `core=12929`。
- 接口静态比较：`interface_consistent=true`，模块名和 14 个端口的方向/宽度未改变。
- Python reference：自检 PASS。

## 证据边界

功能回归支持该隔离候选的数值、II=1、9 周期终态、背压、reset 和 layer 读入行为；strict 仍失败，且尚无本候选的综合、布局布线、Fmax、bitstream 或板级证据，因此不声明 production-ready。

