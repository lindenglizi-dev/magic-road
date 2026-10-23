# Transformer + Croc 双课设工程

当前开发入口：`projects/transformer` 与 `projects/croc`。

在项目根目录运行：

```console
python run_checks.py
```

详细操作、结构、接口和后续任务见 [工程指引](工程指引.md)。

最新汇总为 `reports/local_checks.json`，两个分支的详细结果分别在其 `reports/summary.json`。本地回归只验证独立 RTL；完整 Croc CPU 系统与 ASIC 工艺交付另行验收。

`review_20261023` 保留初次审阅的源码快照和失败证据，用于追溯，不作为当前开发目录。
