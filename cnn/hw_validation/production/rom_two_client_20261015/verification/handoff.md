# 第六批 C2 双客户 ROM 验证交接

角色：verify；分支实查 `work/roadyolo`。只新增本 verification 目录，未改 DUT、训练、生产、TD、约束、位流、板卡或 Flash，未 commit/push。

最终结果：两类真实厂商模型仿真 PASS；TB 严格门禁仍失败，不能描述为八门全通过。最终稳定输入为 `reports/20261015_231451_881312_observed_stream_final/inputs/`，收据为同目录上一级 `summary.json`（SHA256 `098bf27eba702f925e23fa2c9f4f415cfa44a92349f9645ff79d3b63710c915d`）。收据包含所有源/模型/数值输入、工具路径/哈希、命令、失败、警告、日志哈希；快照未变且当前 DUT/数值源仍匹配。

## 实际客户集成

`tb_rom_two_client_real` 例化实际 top，其内部原 down2 预取和原 LUT 服务共用唯一 G10 reader。模型 payload SHA256 为 `b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145`，physical 为 `bab36c254dfeb21ad21f4c600018be962f9352ddde79dcb08e64e7bd117ec417`。

652 项真实 down2 参数和 1024 项 SiLU 均逐条对拍；动态 sigmoid1024/exp256 交错查询，417 项在预取竞争窗内（sigmoid209/exp208）。完整响应比较 kind/address/tag/frame_token/model_id/data/error；输入接受后主动改变空闲字段，输出随机保持 0～7 拍并检查整组稳定。load/table 两消费者各有 LFSR 反压和有界长停顿。

| 实测端点 | 初始完整窗口 |
|---|---:|
| 参数 admission / 物理接受 / 返回 | 160 / 160 / 160 |
| LUT admission / 物理接受 / 返回 | 1280 / 1280 / 1280 |
| 原预取报告完成周期 | 15,739 |
| 完成的全局观测周期 | 15,745 |
| 1280 查询窗口 | cycle9→48536，48,527 拍 |
| 接受→完整响应 valid | 30～41 拍，合计38,654 |
| 竞争查询最大延迟 | 41 拍 |
| 参数/LUT 最长连续 admission 等待 | 10 / 11 拍 |

取消前未进入仲裁的请求没有 ROM admission；另一次取消精确位于 LUT arbiter admission 后、physical reader acceptance 前。后者仍产生恰好一次物理读/一次返回，由 DRAIN 丢弃，排空9拍，之后新 token 响应正确。真实读等待及客户端响应保持期间共同复位均恢复；最终再次完整加载1676项。原预取仅 boot down2 DW16/PW16→24＋SiLU，不能冒充67层运行时参数客户。

## 仲裁边界

`tb_rom_arbiter_boundary` 只例化一个 arbiter 和一个实际 reader。测试用 `reader_gate` 同时门控物理 request valid/ready，控制实际接受机会；没有改 ROM 数据、响应延迟或驱动/强制其 fault。正常阶段两客户各41次完整读（双方连续32次＋各单边9次），82次接受/返回逐词对拍；两方持续请求期间检查62次交替。第一返回把 owner ready 拉低43拍，同时非 owner ready 为1，期间归属/返回载荷保持、没有提前 admission 或退休。其他返回采用 LFSR ready。

正常阶段参数/LUT 最长等待64/53拍；事务 admission→消费11～52拍，含受控物理接受停顿与返回反压，不是原 reader 物理延迟。加入排队未物理接受的 reset、真实返回保持时 reset 后恢复，最终CSV共90个完整返回。公平仅保证两方持续请求的 admission 次序；周期等待必须依赖 reader 最终 ready/返回和 owner 最终 ready，无无条件有限周期上界。

## 原始观测与独立复核

最终 query CSV 的 data 来自响应 valid 时锁存的 `rsp_data`，不再把 expected 写作实际值。新增 `param_stream.csv` 每条记录实际 valid&&ready 的47位打包输出，带 reset_epoch/index/cycle；SiLU INT16 按黄金 JSON 的 signed32 约定扩展。

| 日志 | SHA256 |
|---|---|
| param_stream.csv | `2d03e3bfa59547502e639a1a95ac8e4d4de9889ce5ccd0aba1871f81828df882` |
| tb_rom_two_client_real.csv | `d810e254c59685617787f03cba34c8f0fe1da46fedd06d42196926917421e6fb` |
| tb_rom_arbiter_boundary.csv | `f5405178cff631c1aee82fa3e727015d6c9cf8352399ae64089d291925906327` |

只读 stdlib CSV 复核 PASS：参数 epoch0=1676、epoch1=3（reset中断）、epoch2=1676，所有3355条观测均匹配冻结黄金前缀；1283条实际 LUT 返回值均匹配其动态索引表。协调者可独立使用 epoch0 的完整1676条复核。

## 运行、门禁与边界

本机执行 `D:/Python313/python.exe verification/run_two_client.py --attempt-label observed_stream_final`（从候选目录的完整脚本路径启动）。脚本为每次新建 inputs 快照，复用第五批实际 PH1P_LOGIC_ERAM/PH1P_PHY_GSR 和 ModelSim `-lib work`，cwd 含冻结 artifacts。两top各恰好一个 reader。每top112条厂商模型 `vopt-2697 INIT_FILE` 边界警告完整保留，未改厂商模型或抑制警告。

严格门禁明确使用 `--include-testbench`，每份确实扫描1个TB。`gates/boundary.json` 为277 errors，最终 `gates/real_final.json` 为389 errors：compile/ast/readability/comment/naming/profile failed；testbench passed；静态 toolchain not_requested。formatter 对当前无端口TB形式报 “only single module sources are currently supported”，另有头部、注释、命名/格式失败；真实 ModelSim 编译与执行 PASS 属独立外部证据。默认门禁会跳过TB，0 files 不能算本验证通过。DUT闭包八门由协调者单独汇报。readable-python/script companion skill 路径不存在，未安装、未声称通过。两个同名 TB spec 是人工验证合同和示意 WaveJSON，不冒充自动 write-spec/渲染成功。

失败及旧PASS全部保留：初次TB晚 wire 声明编译失败；第二次TB对 signed SiLU 错用零扩展；第三次两类PASS但 query CSV 写expected（比较确实已用实际输出）；最终只修日志观测，不改刺激、RTL或黄金值，重新两类PASS。

未测真实ROM fault注入/非法状态；原prefetch没有 ROM fault输入，系统须观察全局fault并共同复位，不能伪造成功返回。单reader/无新增ERAM或DSP只属源码结构目标，无TD资源或物理时序签核；不涉及旧7168全审、head13、DDR、全网、摄像头、显示、1FPS、板/Flash。AGE2000不在本任务实现。

下一角色读取：本文件、`final_summary.json`、最终attempt的`summary.json`、两个原始CSV及`param_stream.csv`；DUT/参考源与门禁差异须以各自绑定快照为准。
