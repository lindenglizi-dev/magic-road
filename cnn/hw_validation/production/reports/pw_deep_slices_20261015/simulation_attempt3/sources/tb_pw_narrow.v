`timescale 1ns / 1ps

// 16位独立验证壳自检；使用完整scalar packet、一次公共表装载和真实768项导出。
module tb_pw_narrow(output reg o_test_done);
    reg clk, rstn, rx_valid, tx_ready;
    reg [15:0] rx_data;
    wire rx_ready, tx_valid;
    wire [15:0] tx_data;
    wire busy, done, fault, parameters_ready;

    reg signed [31:0] vector_input[0:767];
    reg [7:0] vector_weight[0:2303];
    reg signed [31:0] vector_bias[0:47];
    reg [31:0] vector_multiplier[0:47];
    reg [7:0] vector_shift[0:47];
    reg [31:0] vector_post[0:1];
    reg signed [7:0] golden_post[0:767];
    reg signed [15:0] silu_table[0:1023];

    integer ticks, index, tx_words, reset_cases, error_reports, report_fd;
    integer fixture_packet_count, fixture_table_entries, fixture_window_start_tick, fixture_window_cycles;
    integer first_core_start_tick, first_core_window_cycles, second_core_start_tick, second_core_window_cycles;
    integer first_export_start_tick, first_export_window_cycles, second_export_start_tick, second_export_window_cycles;
    reg [31:0] first_core_cycles, second_core_cycles;
    reg done_seen, tx_was_stalled, count_fixture_packets;
    reg [15:0] held_tx_data;
    reg [31:0] expected_cycles;
    reg [8*1024-1:0] vector_root, vector_file, report_path;

    road_pw_validation_top #(.PROFILE(0)) dut(
        .i_clk(clk),.i_rstn(rstn),.i_rx_valid(rx_valid),.i_rx_data(rx_data),.o_rx_ready(rx_ready),
        .o_tx_valid(tx_valid),.o_tx_data(tx_data),.i_tx_ready(tx_ready),
        .o_busy(busy),.o_done(done),.o_fault(fault),.o_parameters_ready(parameters_ready)
    );

    always #5 clk=~clk;
    always @(posedge clk)begin
        ticks=ticks+1;
        if(ticks>350000)$fatal(1,"PW48 narrow watchdog timeout");
        if(rstn && done)done_seen=1'b1;
        if(rstn && tx_was_stalled && (!tx_valid || tx_data!==held_tx_data))
            $fatal(1,"PW48 narrow TX payload changed under backpressure");
        tx_was_stalled=rstn && tx_valid && !tx_ready;
        if(tx_was_stalled)held_tx_data=tx_data;
    end

    task reset_top;
        begin
            @(negedge clk); rstn=1'b0; rx_valid=1'b0; tx_ready=1'b0; #1;
            if(rx_ready || tx_valid || busy || done || fault || parameters_ready || dut.domain_rstn ||
               dut.state_current!=4'd0 || dut.u_scheduler.reg_loaded!=0 || dut.u_pp.reg_retire_count!=0)
                $fatal(1,"PW48 narrow asynchronous reset did not cancel state");
            repeat(2)@(negedge clk); rstn=1'b1;
            @(posedge clk); #1;
            if(rx_ready || dut.domain_rstn)$fatal(1,"PW48 narrow accepted before release stage one");
            @(posedge clk); #1;
            if(!rx_ready || !dut.domain_rstn || fault)$fatal(1,"PW48 narrow two-flop release invalid");
            reset_cases=reset_cases+1;
        end
    endtask

    task send_word;
        input [15:0] value;
        begin
            @(negedge clk); rx_valid=1'b1; rx_data=value;
            while(!rx_ready)@(negedge clk);
            @(posedge clk);
            @(negedge clk); rx_valid=1'b0;
        end
    endtask

    task send_packet;
        input [2:0] kind;
        input [11:0] address;
        input [31:0] value;
        begin
            send_word({1'b0,kind,address});
            send_word(value[15:0]);
            send_word(value[31:16]);
            if(count_fixture_packets)fixture_packet_count=fixture_packet_count+1;
        end
    endtask

    task receive_word;
        input [15:0] expected;
        input integer stall_cycles;
        begin
            tx_ready=1'b0;
            wait(tx_valid); #1;
            if(tx_data!==expected)$fatal(1,"PW48 narrow TX got=%h expected=%h word=%0d",tx_data,expected,tx_words);
            repeat(stall_cycles)begin
                @(posedge clk); #1;
                if(!tx_valid || tx_data!==expected)$fatal(1,"PW48 narrow stalled TX changed expected=%h",expected);
            end
            @(negedge clk); tx_ready=1'b1; @(posedge clk); tx_words=tx_words+1; @(negedge clk); tx_ready=1'b0;
        end
    endtask

    task load_full_fixture;
        begin
            // 预装载窗口从8000命令前开始，到3218个scalar packet被核接收且ready置位为止。
            fixture_window_start_tick=ticks; fixture_packet_count=0; fixture_table_entries=0;
            send_word(16'h8000);
            for(index=0;index<1024;index=index+1)begin send_word(silu_table[index]); fixture_table_entries=fixture_table_entries+1; end
            count_fixture_packets=1'b1;
            for(index=0;index<768;index=index+1)send_packet(3'd0,index,vector_input[index]);
            for(index=0;index<48;index=index+1)send_packet(3'd3,index,vector_bias[index]);
            for(index=0;index<48;index=index+1)send_packet(3'd4,index,vector_multiplier[index]);
            for(index=0;index<48;index=index+1)send_packet(3'd5,index,{24'd0,vector_shift[index]});
            send_packet(3'd6,0,vector_post[0]); send_packet(3'd6,1,vector_post[1]);
            for(index=0;index<2304;index=index+1)
                send_packet(3'd2,index,{{24{vector_weight[index][7]}},vector_weight[index]});
            count_fixture_packets=1'b0;
            repeat(2)@(posedge clk); #1;
            if(!parameters_ready || fault || dut.reg_loaded!==6'b111111 || dut.u_scheduler.reg_loaded!==6'b111111)
                $fatal(1,"PW48 narrow full parameters did not become ready");
            fixture_window_cycles=ticks-fixture_window_start_tick;
            if(fixture_packet_count!=3218 || fixture_table_entries!=1024)
                $fatal(1,"PW48 narrow fixture count packets=%0d table=%0d",fixture_packet_count,fixture_table_entries);
        end
    endtask

    task receive_export;
        begin
            for(index=0;index<768;index=index+1)begin
                receive_word(16'ha000|index[9:0],(index%17)==0 ? 3 : 0);
                receive_word({{8{golden_post[index][7]}},golden_post[index]},(index%29)==0 ? 2 : 0);
            end
            receive_word(16'hf000,3);
        end
    endtask

    initial begin
        clk=1'b0; rstn=1'b0; rx_valid=1'b0; rx_data=16'd0; tx_ready=1'b0;
        ticks=0; tx_words=0; reset_cases=0; error_reports=0; done_seen=1'b0; tx_was_stalled=1'b0;
        fixture_packet_count=0; fixture_table_entries=0; count_fixture_packets=1'b0;
        fixture_window_start_tick=0; fixture_window_cycles=0;
        first_core_start_tick=0; first_core_window_cycles=0; second_core_start_tick=0; second_core_window_cycles=0;
        first_export_start_tick=0; first_export_window_cycles=0; second_export_start_tick=0; second_export_window_cycles=0;
        first_core_cycles=0; second_core_cycles=0; o_test_done=1'b0;
        if(!$value$plusargs("VECTORS=%s",vector_root))vector_root=".";
        if(!$value$plusargs("REPORT=%s",report_path))report_path="tb_pw_narrow_cycles.csv";
        report_fd=$fopen(report_path,"w");
        if(report_fd==0)$fatal(1,"PW48 narrow cannot open REPORT=%0s",report_path);
        $sformat(vector_file,"%0s/cls_package_input.hex",vector_root); $readmemh(vector_file,vector_input);
        $sformat(vector_file,"%0s/cls_package_weights.hex",vector_root); $readmemh(vector_file,vector_weight);
        $sformat(vector_file,"%0s/cls_package_bias.hex",vector_root); $readmemh(vector_file,vector_bias);
        $sformat(vector_file,"%0s/cls_package_pre_multiplier.hex",vector_root); $readmemh(vector_file,vector_multiplier);
        $sformat(vector_file,"%0s/cls_package_pre_shift.hex",vector_root); $readmemh(vector_file,vector_shift);
        $sformat(vector_file,"%0s/cls_package_post_params.hex",vector_root); $readmemh(vector_file,vector_post);
        $sformat(vector_file,"%0s/cls_package_post.hex",vector_root); $readmemh(vector_file,golden_post);
        $sformat(vector_file,"%0s/silu_table.hex",vector_root); $readmemh(vector_file,silu_table);

        reset_top;

        // header后的8001属于low payload，不得被解释成start；在high前复位取消partial packet。
        send_word({1'b0,3'd0,12'd0}); send_word(16'h8001); repeat(2)@(posedge clk); #1;
        if(busy || done || fault || dut.flag_start)$fatal(1,"PW48 narrow partial packet executed control data");
        reset_top;

        // 表只装一部分即复位，完整性和隐式地址均取消。
        send_word(16'h8000);
        for(index=0;index<23;index=index+1)send_word(silu_table[index]);
        reset_top;

        // 非法kind完整记录必须返回F001并进入粘滞故障，且不发布结果。
        send_packet(3'd1,12'd0,32'd0); receive_word(16'hf001,2); error_reports=error_reports+1;
        if(!fault || busy || done || parameters_ready || dut.u_scheduler.flag_tile_valid)
            $fatal(1,"PW48 narrow malformed record did not fail closed");
        reset_top;

        // 未定义控制同样只返回F001，不能被当作scalar header。
        send_word(16'h8006); receive_word(16'hf001,1); error_reports=error_reports+1;
        if(!fault || busy || done)$fatal(1,"PW48 narrow bad control did not fault");
        reset_top;

        // 实际值完整scalar packet：header、low16、high16；公共表只在本次成功事务装一次。
        load_full_fixture;

        // 禁止提交后启动，退休队列必须填满并稳定阻塞512拍；8005恢复提交。
        send_word(16'h8004);
        if(dut.flag_commit_ready)$fatal(1,"PW48 narrow commit block command ignored");
        done_seen=1'b0; first_core_start_tick=ticks; send_word(16'h8001); wait(busy);
        wait(dut.u_pp.reg_retire_count==4'd8 && dut.s_pp_output_valid);
        for(index=0;index<512;index=index+1)begin
            @(posedge clk); #1;
            if(dut.u_pp.reg_retire_count!=4'd8 || dut.s_pp_output_ready || dut.u_scheduler.cnt_written!=0 || done || tx_valid)
                $fatal(1,"PW48 narrow queue-full hold escaped cycle=%0d",index);
        end
        send_word(16'h8005);
        if(!dut.flag_commit_ready)$fatal(1,"PW48 narrow commit allow command ignored");
        wait(dut.s_done); #1; first_core_window_cycles=ticks-first_core_start_tick; first_core_cycles=dut.s_cycles;
        repeat(2)@(posedge clk); #1;
        if(fault || !dut.flag_unexported || dut.u_scheduler.cnt_written!=768 || !dut.u_scheduler.flag_tile_valid)
            $fatal(1,"PW48 narrow computation endpoint invalid");

        // 8003只返回冻结core周期的低/高16位。
        expected_cycles=first_core_cycles; send_word(16'h8003);
        receive_word(expected_cycles[15:0],2); receive_word(expected_cycles[31:16],1);

        // 768组A000|index、符号扩展INT8；每17项插入TX stall，末尾仅F000。
        first_export_start_tick=ticks; send_word(16'h8002); receive_export;
        first_export_window_cycles=ticks-first_export_start_tick;
        repeat(2)@(posedge clk); #1;
        if(fault || dut.flag_unexported || dut.u_scheduler.flag_tile_valid || dut.u_scheduler.cnt_export!=767)
            $fatal(1,"PW48 narrow export endpoint invalid");

        // 第二tile复用完整参数；done高电平窗口内8000必须反压，而8002在同一窗口被接受。
        done_seen=1'b0; second_core_start_tick=ticks; send_word(16'h8001); wait(busy); wait(dut.s_done); #1;
        second_core_window_cycles=ticks-second_core_start_tick; second_core_cycles=dut.s_cycles;
        @(negedge clk); rx_valid=1'b1; rx_data=16'h8000; #1;
        if(rx_ready)$fatal(1,"PW48 narrow accepted table begin while done result pending");
        #1; second_export_start_tick=ticks; rx_data=16'h8002; #1;
        if(!rx_ready)$fatal(1,"PW48 narrow rejected export in done cycle");
        @(posedge clk); #1;
        if(dut.state_current!=4'd5 || !dut.flag_export_start)
            $fatal(1,"PW48 narrow done-cycle export command was not captured");
        @(negedge clk); rx_valid=1'b0;
        receive_export;
        second_export_window_cycles=ticks-second_export_start_tick;
        repeat(2)@(posedge clk); #1;
        if(fault || dut.flag_unexported || dut.u_scheduler.flag_tile_valid)
            $fatal(1,"PW48 narrow done-cycle export endpoint invalid");

        if(reset_cases!=5 || error_reports!=2 || tx_words!=3078)
            $fatal(1,"PW48 narrow coverage counters reset=%0d errors=%0d tx_words=%0d",reset_cases,error_reports,tx_words);
        $fwrite(report_fd,"case,table_entries,scalar_packets,fixture_window_cycles,first_core_cycles,first_core_window_cycles,first_export_window_cycles,second_core_cycles,second_core_window_cycles,second_export_window_cycles,commit_stall_cycles,status_words,export_items,tx_words,error_reports,resets\n");
        $fwrite(report_fd,"cls_package,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,512,2,1536,%0d,%0d,%0d\n",
                fixture_table_entries,fixture_packet_count,fixture_window_cycles,first_core_cycles,first_core_window_cycles,
                first_export_window_cycles,second_core_cycles,second_core_window_cycles,second_export_window_cycles,
                tx_words,error_reports,reset_cases);
        $fclose(report_fd);
        o_test_done=1'b1;
        $display("TB_PASS_PW_NARROW scalar_packets=3218 table_words=1024 fixture_window=measured core_windows=2 export_windows=2 partial_packet_reset=1 partial_table_reset=1 malformed_reports=2 commit_block_stall=512 status_words=2 export_pairs=1536 done_cycle_export=1 done_cycle_table_backpressure=1 tx_stalls=enabled terminal=F000 reset_release=two_flop");
        $finish;
    end
endmodule
