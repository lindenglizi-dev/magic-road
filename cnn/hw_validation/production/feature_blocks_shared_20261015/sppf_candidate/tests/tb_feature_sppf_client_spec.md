# tb_feature_sppf_client

## 固定意图

一个road_feature_blocks_client和一个旧road_csp_first_probe，在同一次装表后连续执行真实CSP4→SPPF。顶层仅o_test_complete，内部时钟100MHz，共同低有效异步复位。

CSP4原始source来自冻结reference/csp4，七层输出由DUT真实写回。SPPF block5从0376B000的CSP4输出读取；block切换只更换golden/参数，绝不清除live_memory、written或visible，绝不CPU注入SPPFsource。共同复位清控制、pending、written/visible后重装SiLU并重跑整链。

## 数值和地址

CSP4七阶段沿用acc/pre/SiLU/post/sum/output和地址全幅检查。SPPF H18W32：
- stage0 PW96→24，dst0377A000，13824个输出及四类算术中间值。
- stage1/2/3 signed maxpool5×5，dst0377E000/03782000/03786000，每层13824个输出。算法边界-128，物理尾行padding0；sum必须为poolmax符号扩展至signed9，三层均不得发参数或核组。
- stage4四路concat→PW96→96，dst0378A000，55296个输出及四类算术中间值；实际核心activation逐组对concat.03.hex，因32个输出三通道组重复读取，共1769472个byte比较。

内存采用绝对地址flat映射0372C000..03799000，共446464个TB字节。只有最初CSP4source由CPU提供。真实中间字节在匹配block/layer屏障后才可见；所有物理y18/19禁止写。

应用接口block4、channel7/group5/layer3/window3位；原核心端口和II不变。DUT唯一3072byte工作缓存由DUT写，TB不做初始化。

## 场景和覆盖

+CASE=0正常整链；+CASE=1随机参数/读/core/write/屏障反压；+CASE=2在SPPF stage2至少128写后共同复位重装表，再完整重跑CSP4→SPPF；+CASE=3将第一个pool写连续阻塞64周期，保持写payload并扰动busy输入ID/start。

wrapper99实际+CASE=0 +NEGATIVE_POOL=1，使第一次真实pool写与golden XOR1比较，必须Fatal且含NEGATIVE_POOL injected pool mismatch，不能出现PASS。

完整链outputs331776，acc/pre/SiLU/post各290304，pool41472，负pool输出1628，groups746496/tasks110592/reads41832/parameters69120/barriers12。SPPF stage_reads独立枚举为3456/3060/3060/3060/4608。

所有场景busy中扰动输入ID/start并检查o_block_id固定、shape/address不变；最终标记报告实际busy_id_perturb_cycles与busy_start_cycles，均须大于零。

## 周期账本和时序

FEAT_SPPF_STAGE/STATE/RUN包含block/case/run。20状态ID0..19；新增17=POOL_READ、18=POOL_COMPARE、19=POOL_WRITE。逐块计数从接受start至进入DONE，含端点；stage周期和/state周期和均等于cycles/accounted。

CASE2原始前缀CSP4仍做全部数值和周期核验，但prefix_mode禁止发出完整RUN/STAGE/STATE，也不累加clean totals。FEAT_SPPF_ABORT单列到实际rstn=0的完整前缀及部分SPPF，clean只计算重跑的两块。初次LUT加载不计clean；sequence包含切换/复位额外开销，overhead=sequence-clean-aborted。clean<100M，唯一watchdog130M。

```json
{"signal":[
{"name":"clk","wave":"p.........."},
{"name":"block","wave":"=....=.....","data":["4","5"]},
{"name":"CSP4 final write","wave":"010........"},
{"name":"CSP4 barrier accept","wave":"0.10......."},
{"name":"CSP4 done busy","wave":"0..10......"},
{"name":"SPPF start accept","wave":"0....10...."},
{"name":"SPPF live source read","wave":"0.....10..."},
{"name":"pool write valid","wave":"0.......1.."},
{"name":"pool write ready","wave":"1.......0.1"}
]}
```

## 执行边界

必须+VECTORS_ROOT=<frozen/reference>，其中csp4/sppf按已冻结文件布局提供。唯一成功标记FEATURE_SPPF_PASS；预留FEATURE_SPPF_EXPECTED_FAULT但本阶段不靠fault通关。tb_contract.json声明真实runner cases、精确字段和计数。

本角色不运行ModelSim/TD；总协调封存和统一执行。组件测试不证明更早CPU down3/down4已接RTL，不证明物理DDR/ERAM、资源/时序、整网FPS、QAT、准确率或板卡。
