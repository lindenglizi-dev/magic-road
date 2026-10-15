`timescale 1ns / 1ps
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Fixed DW cache checks
// Module Name: tb_csp_dw_cache
// Description: tb_csp_dw_cache_spec.md
// Simulations: ModelSim
// Referrences: tb_csp_dw_cache_spec.md
// Dependencies: road_csp_dw_cache
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Create cache checks
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: DW缓存完整性与响应自检
// 模块名称: tb_csp_dw_cache
// 模块说明: tb_csp_dw_cache_spec.md
// 仿真工程: ModelSim
// 参考资料: tb_csp_dw_cache_spec.md
// 依赖文件: road_csp_dw_cache
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 创建缓存自检
module tb_csp_dw_cache(output reg o_test_done);
    reg clk = 1'b0; // 仿真工作时钟
    reg rstn = 1'b0; // 缓存共同取消
    reg write_valid = 1'b0; // 写请求
    reg [7:0]write_index = 8'd0; // HWC写索引
    reg [7:0]write_data = 8'd0; // 写数据
    reg read_valid = 1'b0; // 读请求
    reg [3:0]read_pixel = 4'd0; // 读像素
    reg read_group = 1'b0; // 读组号
    reg output_ready = 1'b0; // 响应接受
    wire write_ready; // 写准入
    wire loaded; // 完整采集
    wire [7:0]write_count; // 唯一写计数
    wire fault; // 粘滞错误
    wire read_ready; // 读准入
    wire output_valid; // 响应有效
    wire [63:0]output_data; // 八路响应
    wire [7:0]output_mask; // 尾lane掩码
    wire [3:0]output_pixel; // 响应像素
    wire output_group; // 响应组号
    reg [7:0]dw [0:191]; // 真实DW参考值，仅供测试驱动和比较
    reg [63:0]pw_reads [0:31]; // Python独立打包结果
    reg [4095:0]vectors; // 指定的独立向量目录
    integer word_index; // 读组遍历
    integer burst_count; // 连续输出接受数
    integer bad_index; // 非法索引覆盖
    always #5 clk = ~clk;
    road_csp_dw_cache u_dut(
        .i_clk(clk),.i_rstn(rstn),.i_clear(1'b0),.i_write_valid(write_valid),.i_write_index(write_index),.i_write_data(write_data),
        .o_write_ready(write_ready),.o_loaded(loaded),.o_write_count(write_count),.o_fault(fault),
        .i_read_valid(read_valid),.i_read_pixel(read_pixel),.i_read_group(read_group),.o_read_ready(read_ready),
        .i_output_ready(output_ready),.o_output_valid(output_valid),.o_output_data(output_data),
        .o_output_mask(output_mask),.o_output_pixel(output_pixel),.o_output_group(output_group)
    );

    task reset_cache;
        begin
            @(negedge clk);
            rstn = 1'b0;
            write_valid = 1'b0;
            read_valid = 1'b0;
            output_ready = 1'b0;
            #1;
            if (write_ready || loaded || fault || read_ready || output_valid || write_count != 0)
                $fatal(1,"cache reset leaked old state");
            repeat (2) @(negedge clk);
            rstn = 1'b1;
            #1;
            if (!write_ready || loaded || read_ready || output_valid) $fatal(1,"empty cache read admitted");
        end
    endtask

    task fill_cache;
        input integer count;
        input [7:0]xor_value;
        integer n;
        integer index;
        begin
            for (n = 0; n < count; n = n + 1) begin
                @(negedge clk);
                index = (n * 73) % 192; // 与顺序不同的全排列写入
                write_valid = 1'b1;
                write_index = index[7:0];
                write_data = dw[index] ^ xor_value;
                @(posedge clk);
                if (!write_ready || loaded || fault) $fatal(1,"capture handshake missing n=%0d",n);
                #1;
                if (write_count != n + 1 || loaded !== (n == 191)) $fatal(1,"unique completion count n=%0d",n);
            end
            @(negedge clk);
            write_valid = 1'b0;
        end
    endtask

    task check_response;
        input integer index;
        input [7:0]xor_value;
        reg [63:0]expected;
        integer lane;
        begin
            expected = pw_reads[index];
            for (lane = 0; lane < 8; lane = lane + 1) begin
                if ((index % 2) == 0 || lane < 4) expected[lane*8 +: 8] = expected[lane*8 +: 8] ^ xor_value;
            end
            if (!output_valid || fault || output_data !== expected || output_pixel !== index/2 ||
                output_group !== (index%2) || output_mask !== ((index%2) == 0 ? 8'hff : 8'h0f))
                $fatal(1,"cache response mismatch index=%0d got=%h expected=%h",index,output_data,expected);
        end
    endtask

    task read_one;
        input integer index;
        input integer stalls;
        input [7:0]xor_value;
        begin
            @(negedge clk);
            read_valid = 1'b1;
            read_pixel = index/2;
            read_group = index%2;
            output_ready = 1'b0;
            @(posedge clk);
            if (!read_ready || output_valid) $fatal(1,"cache read request not accepted");
            #1;
            check_response(index,xor_value);
            @(negedge clk);
            read_valid = 1'b0;
            repeat (stalls) begin
                @(posedge clk); #1;
                check_response(index,xor_value);
                if (read_ready) $fatal(1,"occupied response slot admitted overwrite");
            end
            @(negedge clk);
            output_ready = 1'b1;
            @(posedge clk);
            check_response(index,xor_value);
            #1;
            if (output_valid) $fatal(1,"accepted response repeated");
            @(negedge clk);
            output_ready = 1'b0;
        end
    endtask

    task illegal_write;
        input [7:0]index;
        begin
            @(negedge clk);
            write_valid = 1'b1;
            write_index = index;
            write_data = 8'h5a;
            @(posedge clk);
            if (!write_ready) $fatal(1,"invalid write must be observed at acceptance");
            #1;
            if (!fault || loaded || read_ready || output_valid || write_ready) $fatal(1,"invalid write did not close cache");
            @(negedge clk);
            write_valid = 1'b0;
            repeat (3) begin @(posedge clk); #1; if (!fault) $fatal(1,"cache fault not sticky"); end
        end
    endtask

    initial begin
        o_test_done = 1'b0;
        if (!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"VECTORS missing");
        $readmemh({vectors,"/dw.hex"},dw);
        $readmemh({vectors,"/pw_read.hex"},pw_reads);
        reset_cache;
        read_valid = 1'b1;
        repeat (5) begin @(posedge clk); #1; if (read_ready || output_valid) $fatal(1,"unwritten read admitted"); end
        reset_cache; // 未接受请求只能共同取消，不伪装成已消费
        fill_cache(191,8'd0);
        read_valid = 1'b1;
        repeat (5) begin @(posedge clk); #1; if (loaded || read_ready || output_valid) $fatal(1,"one missing byte accepted"); end
        reset_cache;
        fill_cache(192,8'd0);
        for (word_index = 0; word_index < 32; word_index = word_index + 1)
            read_one(word_index,word_index == 17 ? 512 : word_index%7,8'd0);
        // 连续请求与上一响应同沿出入，验证一槽不会丢失或重复。
        burst_count = 0;
        for (word_index = 0; word_index < 32; word_index = word_index + 1) begin
            @(negedge clk);
            read_valid = 1'b1;
            read_pixel = word_index/2;
            read_group = word_index%2;
            output_ready = 1'b1;
            @(posedge clk);
            if (!read_ready) $fatal(1,"continuous read stalled unexpectedly");
            if (word_index > 0) begin check_response(word_index-1,8'd0); burst_count = burst_count + 1; end
            #1;
            check_response(word_index,8'd0);
        end
        @(negedge clk);
        read_valid = 1'b0;
        @(posedge clk);
        check_response(31,8'd0);
        burst_count = burst_count + 1;
        #1;
        if (burst_count != 32 || output_valid) $fatal(1,"continuous output count mismatch");
        // 在待消费响应中复位，RAM仍保留旧数据，但不得发布任何旧值。
        @(negedge clk);
        output_ready = 1'b0;
        read_valid = 1'b1;
        read_pixel = 4'd0;
        read_group = 1'b0;
        @(posedge clk); #1;
        if (!output_valid) $fatal(1,"reset test had no pending response");
        reset_cache;
        fill_cache(192,8'h5a);
        for (word_index = 0; word_index < 32; word_index = word_index + 1) read_one(word_index,0,8'h5a);
        // 完成采集后不能意外覆盖已经用于PW的值；挂起写由复位取消。
        @(negedge clk);
        write_valid = 1'b1;
        write_index = 8'd0;
        write_data = 8'hff;
        repeat (3) begin @(posedge clk); #1; if (write_ready || write_count != 192 || !loaded) $fatal(1,"loaded cache overwritten"); end
        reset_cache;
        fill_cache(1,8'd0);
        illegal_write(8'd0);
        if (write_count != 1) $fatal(1,"duplicate inflated unique count");
        for (bad_index = 0; bad_index < 2; bad_index = bad_index + 1) begin
            reset_cache;
            illegal_write(bad_index == 0 ? 8'd192 : 8'd255);
            if (write_count != 0) $fatal(1,"invalid address stored data");
        end
        reset_cache;
        o_test_done = 1'b1;
        $display("TB_PASS_CSP_DW_CACHE reads=96 continuous=32 long_stall=512 invalid=3 reset_pending=1 partial_191_blocked=1");
        $finish;
    end
    initial begin
        #1000000;
        $fatal(1,"cache unit timeout");
    end
endmodule
