# 第十四课：从算子拼装到真正的任务完成边界

## 为什么不是实例化 FFN 两层顶层？

Lesson 13 的 `ffn_two_layer_top.sv` 内部已经有一个独立 GEMM。如果在 Lesson 12 外面直接串接它，整系统就会实例化 **两个 GEMM**。为了满足课程资源复用目标，本版把 FFN1、FFN2 变成 Lesson 12 原顶层内部的两个新 `phase`，所有任务共用唯一的 `u_gemm`。

## 唯一新数据通路

1. `PH_PV` 写出 32 位 `o_wr_data`，同时送进 `u_attn_requant`（移位、饱和）。
2. `act_valid` 表示量化结果连同地址标签已经到达 `Attention Activation` Bank 的写入口。
3. `DRAIN` 检查 `act_valid==0` 后才从 `PH_PV` 切到 `PH_FFN1`。
4. FFN1 从四 Bank 读取 Attention Activation，乘以 W1，生成 INT32。
5. `u_ffn_requant` 对 FFN1 输出执行算术右移→ReLU→127 饱和，写入 Hidden 四 Bank。
6. `DRAIN` 确认 `h_valid` 已消失后切到 FFN2。
7. FFN2 从 Hidden 读取特征，与 W2 相乘，输出最终 INT32 Y。

## 周期与状态

对一个输出 Tile，仍沿用 GEMM 内部的 CLEAR、RUN、STORE、NEXT；**本课没有改这些内部状态**。
外层 `ISSUE` 通常 1 个周期，`WAIT_GEMM` 由底层 K Tile 数量决定，`DRAIN` 主要保护一级写回寄存器。此处真正容易出错的是**最后一笔数据的非阻塞赋值何时被对端 SRAM 采样**，不是增加两个 FFN 乘法阶段本身。

## 输出写回为什么要同时携带标签？

若在 FFN1 最后一个 INT32 输出到达的同一拍将 `phase` 变为 FFN2，则量化流水线的 `h_data` 仍属于 FFN1。行/列标签必须和数据一同寄存，而不能在写回时重新采样已经切换的输入阶段。

## 源码阅读顺序

`rtl/transformer_block_top.sv` 中的 (a) phase 选择 → (b) `u_gemm` 参数 → (c) Attention Quant → (d) FFN ReLU Quant → (e) DRAIN；之后读 `tb/tb_transformer_block.sv`，检查为什么 Testbench 要按 bank 物理地址初始化 SRAM，以及怎样对拍 FFN 的真正输出。
