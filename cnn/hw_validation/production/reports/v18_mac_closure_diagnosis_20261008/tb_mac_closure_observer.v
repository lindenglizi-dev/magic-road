`timescale 1ns / 1ps
`define MAC tb_down2_overlap_tile_runner.down2_overlap_tile_runner_Inst_tb.road_mac_probe_Inst_tile

// 只读取冻结核；所有年龄以last在时钟沿前完成握手为零点。
module tb_mac_closure_observer;
    integer cycle = 0; // 观测时钟沿计数
    integer last_cycle = 0; // 当前任务末组接受的时钟沿
    integer age = 0; // 距离末组接受的周期数
    integer jobs = 0; // 已开始观测的任务数
    integer acknowledgements = 0; // 已接受的终态数
    integer errors = 0; // 逐拍契约违例计数
    reg tracking = 1'b0; // 当前存在待观测的末组
    reg [95:0] final_data; // A5三路原子安全终态快照
    reg final_fault; // 与安全终态同时捕获的故障

    always @(posedge `MAC.i_clk or negedge `MAC.i_rstn) begin // 只读观测，不驱动计算链
        if (!`MAC.i_rstn) begin
            tracking = 1'b0;
        end else begin
            cycle = cycle + 1;
            if (`MAC.flag_input_accept && `MAC.i_last) begin
                if (tracking) begin
                    $display("CLOSURE_ERROR overlapping task");
                    errors = errors + 1;
                end
                tracking = 1'b1;
                last_cycle = cycle;
                jobs = jobs + 1;
            end
            if (tracking && `MAC.flag_result_accept) begin
                age = cycle - last_cycle;
                if (age < 10) begin
                    $display("CLOSURE_ERROR early acknowledgement age=%0d", age);
                    errors = errors + 1;
                end
                acknowledgements = acknowledgements + 1;
                if ((jobs <= 2) || (tb_down2_overlap_tile_runner.case_index == 3 && acknowledgements % 128 == 1))
                    $display("CLOSURE_ACK case=%0d job=%0d age=%0d errors=%0d", tb_down2_overlap_tile_runner.case_index, jobs, age, errors);
                tracking = 1'b0;
            end
            // NBA后检查发布；不能把发布和下一时钟沿的消费混为一拍。
            #1;
            if (tracking && `MAC.i_rstn) begin
                age = cycle - last_cycle;
                if (jobs <= 2)
                    $display("CLOSURE_TRACE job=%0d age=%0d final_valid=%b%b%b%b output_valid=%b ready=%b", jobs, age, `MAC.flag_final_valid_stage3, `MAC.flag_final_valid_stage2, `MAC.flag_final_valid_stage1, `MAC.flag_final_valid_stage0, `MAC.result_valid_o, `MAC.i_result_ready);
                if (age == 5) begin
                    final_data = `MAC.reg_final_data_stage0;
                    final_fault = `MAC.flag_final_fault_stage0;
                end
                if ((age == 5 && `MAC.flag_final_valid_stage0 !== 1'b1) ||
                    (age == 6 && (`MAC.flag_final_valid_stage1 !== 1'b1 || `MAC.reg_final_data_stage1 !== final_data || `MAC.flag_final_fault_stage1 !== final_fault)) ||
                    (age == 7 && (`MAC.flag_final_valid_stage2 !== 1'b1 || `MAC.reg_final_data_stage2 !== final_data || `MAC.flag_final_fault_stage2 !== final_fault)) ||
                    (age == 8 && (`MAC.flag_final_valid_stage3 !== 1'b1 || `MAC.reg_final_data_stage3 !== final_data || `MAC.flag_final_fault_stage3 !== final_fault)) ||
                    (age >= 9 && (`MAC.result_valid_o !== 1'b1 || `MAC.result_data_o !== final_data || `MAC.fault_o !== final_fault))) begin
                    $display("CLOSURE_ERROR job=%0d age=%0d", jobs, age);
                    errors = errors + 1;
                end
                if (age == 9 && `MAC.i_result_ready && (jobs <= 2))
                    $display("CLOSURE_PUBLISH job=%0d age=9 next_edge_ack=10", jobs);
            end
        end
    end
endmodule
`undef MAC
