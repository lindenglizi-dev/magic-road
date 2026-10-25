# 第五批真实ROM验证交接

角色：verify。目录边界：仅写本批 `verification/`，未改功能RTL、冻结初始化包、旧目录、分支或提交。

实际功能结果：两项本机 ModelSim SE-64 2020.4 厂商模型仿真通过。最终机器入口 `final_summary.json`；完整命令、工具/RTL/TB/全部初始化文件/厂商模型SHA及不可变副本在 `reports/20261015_220747_038075_final/summary.json` 和相邻 `inputs/`。当前两TB与runner逐文件hash已核对等于该最终snapshot，snapshot执行前后不变。

## 真实ROM覆盖与周期

`tb_real_model_rom_reader.v` 只实例化一个实际 `road_numeric_rom_reader`。全部7168词/143360byte与冻结physical对照，28个14组首末边界，word7026两有效byte和18个padding byte，全部2838零padding，37拍长hold，WAIT/RESPONSE共同复位均通过。非法地址7168在37拍观察窗口持续fault、不返回、不再ready。真实接受上升沿至首次valid上升沿固定8拍；7168行逐词记录在 `tb_real_model_rom_reader.csv`。

`tb_real_model_lut.v` 只实例化主代理纯接线top，内部唯一实际reader、14组56个ERAM厂商模型。全部1024 sigmoid+256 exp逐值/完整动态kind/address/tag/frame/model/error对拍，握手后主动改变空闲请求字段确认身份锁定。全部1280条各一次真实ROM读，客户端接受上升沿至首次完整响应上升沿固定29拍，合计37120拍（该合计仅各条响应延迟，不是整个仿真窗口）；客户端37拍hold，错误model/exp256/exp1023均0读；读前取消、读后取消真实晚返回8拍DRAIN并重启、真实WAIT共同reset、客户端held response共同reset通过。全部场景1287次读/1286次返回，差额是WAIT共同reset故意终止的一条已接受读；实际reader WAIT累计10289拍。1284个合法查询加3个错误查询共1287行记录于 `tb_real_model_lut.csv`。不强制任何ROM ready/data/fault，不随机注入真实ROM故障。

源包严格绑定payload `b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145`、physical `bab36c254dfeb21ad21f4c600018be962f9352ddde79dcb08e64e7bd117ec417`；140522+2838=143360字节。runner在snapshot前逐文件核对冻结package，再由独立physical参考生成字序并反向重建全部byte。

## 收据与未关闭项

最终compile返回0、0errors/0warnings；两simulation均返回0、0errors，每top 112条厂商 `ph1p_logic_eram.v:165 vopt-2697 INIT_FILE part-select` warning全部保留。summary warnings数组包含114行，其中另两行只是ModelSim计数汇总，不能算114个warning事件。没有编辑厂商源码或抑制警告。厂商模型仿真通过不等于硅片保证。

失败保留：`reports/20261015_220321_258395_sandbox/` 在vlib创建前遭遇WinError623系统DLL重定位，原summary遗留STARTED，`reports/sandbox_failure.md`补充明确PROCESS_LAUNCH_FAILED；`reports/20261015_220416_076918_escalated/` compile通过但runner错误地把绝对library路径作为vsim -lib名称，vopt-2253加载失败。修正runner为snapshot cwd内work库且 `-lib work` 后 `reports/20261015_220510_055624_library_fix/` 双通过，补TB语义注释后最终snapshot双通过。失败均未计PASS。

TB八门状态逐项以 `gates/reader_final.json`、`gates/lut_final.json` 为准：compile/ast/readability/naming/profile报告passed，但默认TB排除导致files/modules=0，不据此声称已有效完成TB AST/quality分析；comment分别failed(2/3个task纯前置目的注释要求)；testbench/toolchain为not_requested。真实ModelSim编译/执行作为独立toolchain证据已通过且带上述warning。初始17/35项注释失败留 `*_initial`。主代理要求停止非关键注释/格式改动，本交付不继续重写TB。根 `../gates/closure.json` 为主代理生产RTL门禁（1610 errors/10 warnings），与TB门独立，整组件不标全绿。

readable-python-generator/readable-script-generator当前不可用，采用最小stdlib runner；未安装、未伪报相应门禁。两个同名TB spec是意图文档，未执行受管WaveDrom渲染。

旧 `../../shared_lut_service_1fps_20261015/verification/reports/final_summary.json` 只列为先前受控端点故障/奇地址跨词分支证据，SHA `0cd604838dbc9db58c3d9e060fae4a3dff4a3983a60b781e157ab15b9fc2b5b`，不得冒充本次真实ROM执行。

重跑入口：在本批package根执行 `python verification/run_real_rom.py --attempt-label <new-label>`；普通沙箱曾有系统DLL启动故障，已授权同源本机提升执行。每次建立独立输入snapshot及报告目录，不覆盖旧失败。

未覆盖物理资源/时序、真实DDR可见性、CNN共享仲裁、完整后处理联调、整网精度或1FPS、板/Flash。100MHz/100M整网与2M总后处理仅预算；500ms契约未改。
