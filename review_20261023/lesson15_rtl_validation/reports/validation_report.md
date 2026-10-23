# Lesson 15 门禁实测报告

| 门禁项 | 状态 | 说明 |
|---|---|---|
| reference | PASS | 日志: `reference.log` |
| contracts | PASS | 日志: `contracts.log` |
| check_contracts | PASS | 日志: `check_contracts.log` |
| rtl | SKIP (no iverilog/vvp available) | 当前无工具，未执行 |

**最终：RTL_UNVERIFIED**

没有 HDL 仿真器、工艺综合与后端工具，因此不报告 RTL 通过、频率、面积、功耗或 GDSII。

静态检查定位并修复的验证脚本错误：`reference/check_contracts.py` 仍读取旧顶层 `full_attention_top.sv`。详见 `validation/check_contracts_fix.patch`。