# 首次工具启动失败

`run.py simulate` 在 `vlib.exe` 的 CreateProcess 阶段失败，Windows 返回
`WinError 623: 无效的系统 DLL 重定位`。此次没有完成编译或仿真，没有 DUT 通过/失败结论。
目录内 input_manifest.json 和 vlib.log 保留不覆盖。后续重试使用新的 simulation_attempt 目录。

另一次依赖检查从 E:/project/qiansai 运行，因不含项目 AGENTS.md / Git 根而未找到工程上下文。
已改为从当前独立验证目录运行，required_ok=true；未修改工具或依赖规则。
