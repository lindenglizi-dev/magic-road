`timescale 1ns / 1ps
// 写回边界逐拍检查：仅本测试强制MAC/PP边界；真实核心另由17项回归证明。
module tb_csp_writeback_trace(output o_test_complete);
    reg flag_complete_o = 0; // 全部逐拍记录通过后发布完成
    assign o_test_complete = flag_complete_o; // 完成观察口不参与被测计算
    reg clk = 0; // 100MHz测试时钟
    reg [311:0] row; // Python边沿前契约记录
    reg [210:0] drive; // 所有输入及首组元数据
    reg [100:0] expected; // 边沿前输出和有效流水观察值
    reg [4095:0] trace_path; // 独立冻结向量文件路径
    integer file_handle; // 流式读取避免保存完整测试轨迹
    integer scanned; // 完整行解析结果
    integer cycles = 0; // 已验证边沿数
    wire rstn = drive[0]; // 异步共同复位
    wire loaded = drive[1]; // 本测试抽象完整装表事件
    wire external_fault = drive[2]; // 边沿前核心故障
    wire task_start = drive[3]; // 已获准的首组输入
    wire pp_valid = drive[4]; // 边沿前PP输出valid
    wire rawmode = drive[5]; // 非INT8模式错误注入
    wire output_ready = drive[6]; // 实际写端接受许可
    wire residual = drive[7]; // 首组残差模式
    wire [2:0] mask = drive[10:8]; // 三路预留掩码
    wire [47:0] tags = drive[58:11]; // 低位为甲路tag
    wire [95:0] addresses = drive[154:59]; // 低位为甲路字节地址
    wire [23:0] bypass = drive[178:155]; // 三路signed8旁路
    wire [15:0] pp_data = drive[194:179]; // PP符号扩展值
    wire [15:0] pp_tag = drive[210:195]; // PP外部标识
    wire ready; // 写回PP准入
    wire valid; // 实际外部写valid
    wire signed [7:0] data; // 最终饱和值
    wire [15:0] tag; // 最终tag
    wire [31:0] address; // 最终写地址
    wire signed [8:0] sum; // 精确残差和
    wire fault; // 粘滞故障

    always #5 clk = ~clk; // 固定10ns周期

    road_csp_first_probe dut(
        .i_clk(clk), .i_rstn(rstn), .i_table_valid(1'b0), .i_table_addr(10'd0), .i_table_data(16'sd0),
        .i_input_valid(task_start), .i_first(task_start), .i_last(task_start), .i_lane_mask(8'd0),
        .i_activation_data(64'd0), .i_weight_data(192'd0), .i_bias_data(96'd0),
        .i_output_mask(mask), .i_tags(tags), .i_addresses(addresses),
        .i_pre_multipliers(96'd0), .i_pre_shifts(18'd0), .i_post_multiplier(32'd0), .i_post_shift(6'd0),
        .i_residual(residual), .i_bypass_data(bypass), .i_input_fault(1'b0),
        .i_output_ready(output_ready), .o_table_ready(), .o_table_loaded(), .o_input_ready(),
        .o_output_valid(valid), .o_output_data(data), .o_output_tag(tag), .o_output_address(address),
        .o_output_sum(sum), .o_fault(fault)
    );

    // 强制仅限定本测试的语义边界，不改变候选RTL或实际核心回归。
    initial begin
        drive = 0;
        force dut.table_loaded_o = loaded;
        force dut.flag_mac_ready = 1'b1;
        force dut.flag_mac_valid = 1'b0;
        force dut.mac_fault = external_fault;
        force dut.pp_fault = 1'b0;
        force dut.flag_pp_valid = pp_valid;
        force dut.flag_pp_rawmode = rawmode;
        force dut.pp_data = pp_data;
        force dut.pp_tag = pp_tag;
        if (!$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"TRACE missing");
        file_handle = $fopen(trace_path,"r");
        if (!file_handle) $fatal(1,"TRACE cannot open");
        while (!$feof(file_handle)) begin
            @(negedge clk);
            scanned = $fscanf(file_handle,"%h\n",row);
            if (scanned != 1) $fatal(1,"TRACE malformed row=%0d",cycles);
            drive = row[210:0];
            expected = row[311:211];
            #1;
            if ({fault,dut.flag_owned,valid,dut.flag_pp_output_ready} !== expected[3:0])
                $fatal(1,"TRACE control cycle=%0d got=%b expected=%b",cycles,
                    {fault,dut.flag_owned,valid,dut.flag_pp_output_ready},expected[3:0]);
            if (valid && {address,tag,sum,data} !== {expected[72:41],expected[40:25],expected[24:16],expected[15:8]})
                $fatal(1,"TRACE payload cycle=%0d",cycles);
            if ({dut.reg_remaining,dut.reg_seen} !== expected[78:73])
                $fatal(1,"TRACE ownership cycle=%0d",cycles);
            if ({dut.flag_compare_valid,dut.flag_add_valid,dut.flag_select_valid,dut.flag_match_valid} !== expected[82:79])
                $fatal(1,"TRACE pipeline valids cycle=%0d",cycles);
            if (dut.flag_add_valid && dut.reg_add_sum !== expected[91:83])
                $fatal(1,"TRACE A sum cycle=%0d",cycles);
            if (dut.flag_compare_valid && dut.reg_compare_sum !== expected[100:92])
                $fatal(1,"TRACE C sum cycle=%0d",cycles);
            @(posedge clk);
            #1;
            cycles = cycles + 1;
        end
        $fclose(file_handle);
        flag_complete_o = 1'b1;
        $display("CSP_WRITEBACK_TRACE_PASS cycles=%0d",cycles);
        $finish;
    end
endmodule
