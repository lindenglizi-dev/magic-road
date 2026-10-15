`timescale 1ns / 1ps
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Fixed CSP scheduler checks
// Module Name: tb_csp_tile_schedule
// Description: Frozen descriptor, handshake, reset and cancellation checks
// Simulations: ModelSim
// Referrences: tb_csp_tile_schedule_spec.md
// Dependencies: road_csp_tile_schedule
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 Codex Create file
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: CSP固定调度自检
// 模块名称: tb_csp_tile_schedule
// 模块说明: 只验证顺序控制，不把模拟完成延迟当真实计算周期
// 仿真工程: ModelSim
// 参考资料: tb_csp_tile_schedule_spec.md
// 依赖文件: road_csp_tile_schedule
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 Codex 创建文件
module tb_csp_tile_schedule(output reg o_test_done);
    reg clk = 1'b0; // 仿真100MHz时钟
    reg rstn = 1'b0; // 共同取消
    reg start = 1'b0; // 启动请求
    reg table_loaded = 1'b0; // 测试完整装表许可，不执行装表
    reg group_ready = 1'b0; // 可停顿组接受
    reg task_done = 1'b0; // 模拟本地末路提交事件
    reg core_fault = 1'b0; // 故障注入
    wire start_ready; // 启动许可
    wire group_valid; // 当前描述符有效
    wire first; // 首组
    wire last; // 末组
    wire pw; // PW阶段
    wire [1:0]y; // tile行
    wire [1:0]x; // tile列或三点起点
    wire [3:0]channel; // 逻辑通道
    wire [2:0]output_mask; // 有效输出路
    wire [7:0]input_mask; // 有效输入槽
    wire [7:0]task_index; // 固定任务索引
    wire busy; // tile占有
    wire done; // 完整tile结束
    wire fault; // 粘滞故障
    wire [24:0]descriptor; // 与Python逐项比较的完整载荷
    reg [24:0]golden [0:319]; // 冻结320组描述符
    reg [7:0]golden_mask [0:319]; // 冻结输入掩码
    reg [4095:0]vectors; // 受控向量目录
    integer phase; // 复位位置
    integer idle_cycles; // 准入检查计数
    always #5 clk = ~clk;
    assign descriptor = {task_index,pw,y,x,channel,first,last,output_mask,3'b000};
    road_csp_tile_schedule u_dut(
        .i_clk(clk),.i_rstn(rstn),.i_start(start),.i_table_loaded(table_loaded),
        .i_group_ready(group_ready),.i_task_done(task_done),.i_core_fault(core_fault),
        .o_start_ready(start_ready),.o_group_valid(group_valid),.o_first(first),.o_last(last),
        .o_pw(pw),.o_y(y),.o_x(x),.o_channel(channel),.o_output_mask(output_mask),
        .o_input_mask(input_mask),.o_task_index(task_index),.o_busy(busy),.o_done(done),.o_fault(fault)
    );

    task reset_common;
        begin
            @(negedge clk);
            rstn = 1'b0;
            start = 1'b0;
            table_loaded = 1'b0;
            group_ready = 1'b0;
            task_done = 1'b0;
            core_fault = 1'b0;
            #1;
            if (group_valid || start_ready || busy || done || fault) $fatal(1,"reset leaked transaction");
            repeat (3) @(negedge clk);
            rstn = 1'b1;
            repeat (3) @(negedge clk);
        end
    endtask

    task launch;
        begin
            @(negedge clk);
            table_loaded = 1'b1;
            start = 1'b1;
            #1;
            if (!start_ready) $fatal(1,"loaded idle start blocked");
            @(posedge clk); #1;
            if (!group_valid || descriptor !== golden[0]) $fatal(1,"start did not publish first descriptor");
            @(negedge clk);
            start = 1'b0;
        end
    endtask

    task run_complete;
        input integer case_id;
        input integer mode;
        integer row;
        integer pending;
        integer cycles;
        integer sent;
        integer wait_cycles;
        integer stalled_cycles;
        integer completed;
        integer random_state;
        reg held;
        reg [24:0]held_descriptor;
        reg [7:0]held_mask;
        begin
            row = 0;
            pending = 0;
            cycles = 0;
            sent = 0;
            wait_cycles = 0;
            stalled_cycles = 0;
            completed = 0;
            random_state = 42;
            held = 1'b0;
            launch;
            while (!done && cycles < 20000) begin
                // 当前处于negedge，所有驱动在下个有效沿之前固定。
                group_ready = mode == 0 ? 1'b1 : mode == 2 && cycles < 512 ? 1'b0 : (($random(random_state) & 3) != 0);
                task_done = pending == 1;
                start = mode == 1; // 忙时重复启动不得扰乱顺序
                @(posedge clk);
                if (fault) $fatal(1,"unexpected fault case=%0d row=%0d",case_id,row);
                if (held && (!group_valid || descriptor !== held_descriptor || input_mask !== held_mask))
                    $fatal(1,"descriptor changed under backpressure case=%0d row=%0d",case_id,row);
                held = group_valid && !group_ready;
                held_descriptor = descriptor;
                held_mask = input_mask;
                cycles = cycles + 1;
                if (group_valid && group_ready) begin
                    if (row >= 320 || descriptor !== golden[row] || input_mask !== golden_mask[row])
                        $fatal(1,"descriptor mismatch case=%0d row=%0d got=%h",case_id,row,descriptor);
                    if (pending != 0) $fatal(1,"new group before local completion");
                    if (last) pending = mode == 0 ? 1 : (cycles % 7) + 1;
                    row = row + 1;
                    sent = sent + 1;
                end else if (group_valid) begin
                    stalled_cycles = stalled_cycles + 1;
                end else begin
                    wait_cycles = wait_cycles + 1;
                    if (!busy) $fatal(1,"idle before all tasks submitted");
                    if (task_done) begin
                        completed = completed + 1;
                        pending = 0;
                    end else if (pending > 0) pending = pending - 1;
                end
                #1;
                if (fault) $fatal(1,"post-edge completion falsely raised fault case=%0d row=%0d",case_id,row);
                if (!done) @(negedge clk);
            end
            if (!done || row != 320 || completed != 160 || sent + stalled_cycles + wait_cycles != cycles)
                $fatal(1,"incomplete schedule case=%0d row=%0d commits=%0d cycles=%0d",case_id,row,completed,cycles);
            $display("CSP_SCHEDULE_CASE=%0d groups=%0d tasks=%0d cycles=%0d send=%0d group_stall=%0d local_commit_wait=%0d",case_id,row,completed,cycles,sent,stalled_cycles,wait_cycles);
            @(negedge clk);
            group_ready = 1'b0;
            task_done = 1'b0;
            start = 1'b0;
            @(posedge clk); #1;
            if (done || busy || group_valid) $fatal(1,"done must be pulse with no duplicate groups");
        end
    endtask

    initial begin
        o_test_done = 1'b0;
        if (!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"VECTORS missing");
        $readmemh({vectors,"/descriptor.hex"},golden);
        $readmemh({vectors,"/input_mask.hex"},golden_mask);
        reset_common;
        start = 1'b1;
        group_ready = 1'b1;
        for (idle_cycles = 0; idle_cycles < 8; idle_cycles = idle_cycles + 1) begin
            @(posedge clk); #1;
            if (start_ready || group_valid || busy) $fatal(1,"partial/unloaded table admitted start");
        end
        @(negedge clk);
        start = 1'b0;
        group_ready = 1'b0;
        run_complete(0,0);
        run_complete(1,1); // 无复位连续启动，所有坐标重新从零开始
        run_complete(2,2);
        for (phase = 0; phase < 3; phase = phase + 1) begin
            reset_common;
            launch;
            group_ready = 1'b0;
            if (phase > 0) begin
                group_ready = 1'b1;
                @(posedge clk); #1;
                @(negedge clk);
            end
            if (phase > 1) begin
                @(posedge clk); #1;
                @(negedge clk);
                if (group_valid || !busy) $fatal(1,"WAIT not reached for reset");
            end
            reset_common;
            if (group_valid || busy || done) $fatal(1,"cancelled tile leaked after release");
            run_complete(3 + phase,0);
        end
        reset_common;
        launch;
        task_done = 1'b1;
        group_ready = 1'b1;
        #1;
        if (group_valid || !fault) $fatal(1,"early completion did not immediately cancel");
        @(posedge clk); #1;
        @(negedge clk);
        task_done = 1'b0;
        if (!fault || group_valid || start_ready) $fatal(1,"protocol fault not sticky");
        $display("CSP_SCHEDULE_FAULT=early_completion PASS");
        reset_common;
        launch;
        group_ready = 1'b1;
        repeat (2) begin @(posedge clk); #1; @(negedge clk); end
        core_fault = 1'b1;
        #1;
        if (!fault || group_valid || done) $fatal(1,"core fault did not cancel WAIT");
        @(posedge clk); #1;
        @(negedge clk);
        core_fault = 1'b0;
        if (!fault || start_ready || done) $fatal(1,"core fault not sticky");
        $display("CSP_SCHEDULE_FAULT=core_wait PASS");
        reset_common;
        run_complete(6,0);
        o_test_done = 1'b1;
        $display("TB_PASS_CSP_TILE_SCHEDULE complete_runs=7 groups_per_run=320 tasks_per_run=160 reset_positions=3 fault_cases=2");
        $finish;
    end
    initial begin
        #2000000;
        $fatal(1,"scheduler test timeout");
    end
endmodule
