`timescale 1ns / 1ps

// PROFILE2窄口最小闭环：真实scalar装载、状态周期和192项带反压导出。
module tb_pw_deep_narrow(output reg o_test_done);
    localparam integer INPUT_WORDS=3072;
    localparam integer OUTPUT_WORDS=192;
    localparam integer COUT=12;
    localparam integer FIXTURE_PACKETS=5414;

    reg clk, rstn, rx_valid, tx_ready;
    reg [15:0] rx_data;
    wire rx_ready, tx_valid;
    wire [15:0] tx_data;
    wire busy, done, fault, parameters_ready;

    reg signed [31:0] vector_input[0:3071];
    reg [7:0] vector_weight[0:2303];
    reg signed [31:0] vector_bias[0:11];
    reg [31:0] vector_multiplier[0:11];
    reg [7:0] vector_shift[0:11];
    reg [31:0] vector_post[0:1];
    reg signed [7:0] golden_post[0:191];
    reg signed [15:0] silu_table[0:1023];

    integer ticks, index, tx_words, report_fd, fixture_packets;
    integer load_start_tick, load_window_cycles, core_start_tick, core_window_cycles;
    integer export_start_tick, export_window_cycles;
    reg tx_was_stalled;
    reg [15:0] held_tx_data;
    reg [31:0] expected_cycles, reported_cycles;
    reg [8*1024-1:0] vector_root, vector_file, report_path;

    road_pw_validation_top #(.PROFILE(2)) dut(
        .i_clk(clk),.i_rstn(rstn),.i_rx_valid(rx_valid),.i_rx_data(rx_data),.o_rx_ready(rx_ready),
        .o_tx_valid(tx_valid),.o_tx_data(tx_data),.i_tx_ready(tx_ready),
        .o_busy(busy),.o_done(done),.o_fault(fault),.o_parameters_ready(parameters_ready)
    );

    always #5 clk=~clk;
    always @(posedge clk)begin
        ticks=ticks+1;
        if(ticks>500000)$fatal(1,"PW192 narrow watchdog timeout");
        if(rstn && tx_was_stalled && (!tx_valid || tx_data!==held_tx_data))
            $fatal(1,"PW192 narrow TX payload changed under backpressure");
        tx_was_stalled=rstn && tx_valid && !tx_ready;
        if(tx_was_stalled)held_tx_data=tx_data;
    end

    task reset_top;
        begin
            @(negedge clk); rstn=1'b0; rx_valid=1'b0; tx_ready=1'b0; #1;
            if(rx_ready || tx_valid || busy || done || fault || parameters_ready || dut.domain_rstn ||
               dut.state_current!=4'd0 || dut.u_scheduler.reg_loaded!=0 || dut.u_pp.reg_retire_count!=0)
                $fatal(1,"PW192 narrow reset retained ownership");
            repeat(2)@(negedge clk); rstn=1'b1;
            @(posedge clk); #1;
            if(rx_ready || dut.domain_rstn)$fatal(1,"PW192 narrow accepted before release stage one");
            @(posedge clk); #1;
            if(!rx_ready || !dut.domain_rstn || fault)$fatal(1,"PW192 narrow two-flop release invalid");
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
            fixture_packets=fixture_packets+1;
        end
    endtask

    task receive_word;
        input [15:0] expected;
        input integer stall_cycles;
        begin
            tx_ready=1'b0;
            wait(tx_valid); #1;
            if(tx_data!==expected)$fatal(1,"PW192 narrow TX got=%h expected=%h word=%0d",tx_data,expected,tx_words);
            repeat(stall_cycles)begin
                @(posedge clk); #1;
                if(!tx_valid || tx_data!==expected)$fatal(1,"PW192 narrow stalled TX changed expected=%h",expected);
            end
            @(negedge clk); tx_ready=1'b1; @(posedge clk); tx_words=tx_words+1; @(negedge clk); tx_ready=1'b0;
        end
    endtask

    initial begin
        clk=1'b0; rstn=1'b0; rx_valid=1'b0; rx_data=16'd0; tx_ready=1'b0;
        ticks=0; tx_words=0; fixture_packets=0; tx_was_stalled=1'b0; o_test_done=1'b0;
        load_start_tick=0; load_window_cycles=0; core_start_tick=0; core_window_cycles=0;
        export_start_tick=0; export_window_cycles=0; expected_cycles=0; reported_cycles=0;
        if(!$value$plusargs("VECTORS=%s",vector_root))vector_root=".";
        if(!$value$plusargs("REPORT=%s",report_path))report_path="tb_pw_deep_narrow.csv";
        report_fd=$fopen(report_path,"w");
        if(report_fd==0)$fatal(1,"PW192 narrow cannot open REPORT=%0s",report_path);
        $sformat(vector_file,"%0s/p192_slice00_input.hex",vector_root); $readmemh(vector_file,vector_input);
        $sformat(vector_file,"%0s/p192_slice00_weights.hex",vector_root); $readmemh(vector_file,vector_weight);
        $sformat(vector_file,"%0s/p192_slice00_bias.hex",vector_root); $readmemh(vector_file,vector_bias);
        $sformat(vector_file,"%0s/p192_slice00_pre_multiplier.hex",vector_root); $readmemh(vector_file,vector_multiplier);
        $sformat(vector_file,"%0s/p192_slice00_pre_shift.hex",vector_root); $readmemh(vector_file,vector_shift);
        $sformat(vector_file,"%0s/p192_slice00_post_params.hex",vector_root); $readmemh(vector_file,vector_post);
        $sformat(vector_file,"%0s/p192_slice00_post.hex",vector_root); $readmemh(vector_file,golden_post);
        $sformat(vector_file,"%0s/silu_table.hex",vector_root); $readmemh(vector_file,silu_table);

        reset_top;
        load_start_tick=ticks;
        send_word(16'h8000);
        for(index=0;index<1024;index=index+1)send_word(silu_table[index]);
        for(index=0;index<INPUT_WORDS;index=index+1)send_packet(3'd0,index,vector_input[index]);
        for(index=0;index<COUT;index=index+1)send_packet(3'd3,index,vector_bias[index]);
        for(index=0;index<COUT;index=index+1)send_packet(3'd4,index,vector_multiplier[index]);
        for(index=0;index<COUT;index=index+1)send_packet(3'd5,index,{24'd0,vector_shift[index]});
        send_packet(3'd6,0,vector_post[0]); send_packet(3'd6,1,vector_post[1]);
        for(index=0;index<2304;index=index+1)
            send_packet(3'd2,index,{{24{vector_weight[index][7]}},vector_weight[index]});
        repeat(2)@(posedge clk); #1;
        load_window_cycles=ticks-load_start_tick;
        if(!parameters_ready || fault || dut.reg_loaded!==6'b111111 || dut.u_scheduler.reg_loaded!==6'b111111 ||
           fixture_packets!=FIXTURE_PACKETS)
            $fatal(1,"PW192 narrow fixture endpoint packets=%0d expected=%0d",fixture_packets,FIXTURE_PACKETS);

        core_start_tick=ticks; send_word(16'h8001); wait(busy); wait(done); #1;
        core_window_cycles=ticks-core_start_tick; expected_cycles=dut.s_cycles;
        if(fault || !dut.flag_unexported || dut.u_scheduler.cnt_written!=OUTPUT_WORDS || !dut.u_scheduler.flag_tile_valid)
            $fatal(1,"PW192 narrow computation endpoint invalid");

        send_word(16'h8003);
        receive_word(expected_cycles[15:0],2); reported_cycles[15:0]=expected_cycles[15:0];
        receive_word(expected_cycles[31:16],1); reported_cycles[31:16]=expected_cycles[31:16];
        if(reported_cycles!==expected_cycles)$fatal(1,"PW192 narrow status cycles mismatch");

        export_start_tick=ticks; send_word(16'h8002);
        for(index=0;index<OUTPUT_WORDS;index=index+1)begin
            receive_word(16'ha000|index[9:0],(index%17)==0 ? 3 : 0);
            receive_word({{8{golden_post[index][7]}},golden_post[index]},(index%29)==0 ? 2 : 0);
        end
        receive_word(16'hf000,3);
        export_window_cycles=ticks-export_start_tick;
        repeat(2)@(posedge clk); #1;
        if(fault || dut.flag_unexported || dut.u_scheduler.flag_tile_valid ||
           dut.u_scheduler.cnt_export!=OUTPUT_WORDS-1 || tx_words!=2*OUTPUT_WORDS+3)
            $fatal(1,"PW192 narrow export endpoint tx_words=%0d",tx_words);

        $fwrite(report_fd,"profile,table_entries,scalar_packets,load_window_cycles,core_cycles,core_window_cycles,export_window_cycles,status_words,export_items,tx_words\n");
        $fwrite(report_fd,"2,1024,%0d,%0d,%0d,%0d,%0d,2,%0d,%0d\n",fixture_packets,load_window_cycles,
                expected_cycles,core_window_cycles,export_window_cycles,OUTPUT_WORDS,tx_words);
        $fclose(report_fd); o_test_done=1'b1;
        $display("TB_PASS_PW_DEEP_NARROW profile=2 scalar_packets=%0d table_words=1024 output_items=%0d status_matches_direct=1 tx_backpressure=1 terminal=F000 reset_release=two_flop",
                 fixture_packets,OUTPUT_WORDS);
        $finish;
    end
endmodule
