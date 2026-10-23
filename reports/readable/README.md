# 此处的门禁原始输出不可作为通过证明

两个门禁目录扫描实际均为 `files=0`、`modules=0`，未扫描本工程的 SystemVerilog `.sv`。原始 `delivery_ready=true` 是空扫描结果，本工程将其记为不适用。

2026-10-24 新增两个单元 TB 的单文件门禁仍为零扫描，判定摘要见 `projects/transformer/reports/unit_style_gate.json`。`gemm_unit_deliverable_gate.*` 与 `softmax_unit_deliverable.*` 原始工具输出仅保留在本地，不能作为 compile、AST 或风格通过的依据。

真实外部编译与仿真以根目录 `reports/local_checks.json` 及两项目各自的 `reports/summary.json` 为准。
