`timescale 1ns / 1ps
// Single actual reader and PH1P ERAM models; no behavioral ROM endpoint.
module tb_real_model_rom_reader;
    reg clk=0, rstn=0, request_valid=0, response_ready=0; // 驱动共同复位与读握手。
    always #5 clk=~clk; // 生成100MHz仿真时钟。
    reg [12:0] address=0; // 真实reader物理词号。
    wire request_ready,response_valid,fault; // reader许可、完整响应与故障。
    wire [159:0] data; // 实际厂商ERAM返回的完整词。
    reg [159:0] golden[0:7167],held; // 独立physical参考词与反压快照。
    reg [4095:0] words_path,trace_path; // 运行时参考输入和逐词收据路径。
    integer trace_file,cycle=0,location,byte_lane,responses=0,hold_cycles; // 文件、循环和事务计数。
    integer accepted_cycle,response_cycle,min_latency=999,max_latency=0; // 实际接受到响应周期统计。
    road_numeric_rom_reader dut( // 仅实例化一个未改动reader。
        .i_clk(clk),.i_rstn(rstn),.i_request_valid(request_valid),
        .i_request_addr(address),.o_request_ready(request_ready),
        .o_response_valid(response_valid),.o_response_data(data),
        .i_response_ready(response_ready),.o_fault(fault)
    );
    always @(posedge clk) begin #1; cycle=cycle+1; end // NBA后记录全局上升沿编号。
    task release_reset; // 共同复位保持四拍后释放。
        begin repeat(4) @(negedge clk); rstn=1; end
    endtask
    task read_word; // 单次真实读：逐byte比较、反压保持和消费检查。
        input integer word_location; // 本次需要验证的合法物理词号。
        input integer response_hold; // 消费前保持响应的拍数。
        begin
            @(negedge clk);
            while(!request_ready) @(negedge clk);
            request_valid=1; address=word_location; accepted_cycle=cycle+1;
            @(negedge clk); request_valid=0;
            while(!response_valid) @(negedge clk);
            response_cycle=cycle;
            if(fault || data !== golden[word_location])
                $fatal(1,"TB_FAIL word mismatch address=%0d",word_location);
            for(byte_lane=0;byte_lane<20;byte_lane=byte_lane+1) begin
                if(data[byte_lane*8+:8] !== golden[word_location][byte_lane*8+:8])
                    $fatal(1,"TB_FAIL byte mismatch address=%0d lane=%0d",word_location,byte_lane);
                if(word_location*20+byte_lane>=140522 && data[byte_lane*8+:8] !== 8'd0)
                    $fatal(1,"TB_FAIL nonzero padding byte=%0d",word_location*20+byte_lane);
            end
            if(response_cycle-accepted_cycle<min_latency) min_latency=response_cycle-accepted_cycle;
            if(response_cycle-accepted_cycle>max_latency) max_latency=response_cycle-accepted_cycle;
            held=data;
            repeat(response_hold) begin
                @(negedge clk);
                if(!response_valid || request_ready || data !== held || fault)
                    $fatal(1,"TB_FAIL held response address=%0d",word_location);
            end
            response_ready=1;
            $fwrite(trace_file,"%0d,%0d,%0d,%0d,%0d,%040h\n",word_location,accepted_cycle,response_cycle,
                response_cycle-accepted_cycle,response_hold,data);
            @(negedge clk); response_ready=0;
            if(response_valid) $fatal(1,"TB_FAIL duplicate response");
            responses=responses+1;
        end
    endtask
    initial begin // 顺序覆盖复位、全部物理词与非法地址。
        if(!$value$plusargs("WORDS=%s",words_path)) $fatal(1,"TB_FAIL missing WORDS");
        if(!$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"TB_FAIL missing TRACE");
        trace_file=$fopen(trace_path,"w");
        if(trace_file==0) $fatal(1,"TB_FAIL cannot open trace");
        $readmemh(words_path,golden);
        $fwrite(trace_file,"word,accepted_cycle,response_cycle,latency_cycles,hold_cycles,data\n");
        release_reset;
        @(negedge clk); request_valid=1;address=37;
        @(negedge clk); request_valid=0;
        repeat(2) @(negedge clk);
        rstn=0;#1;
        if(response_valid || request_ready || fault) $fatal(1,"TB_FAIL WAIT reset");
        release_reset;
        repeat(15) @(negedge clk);
        if(response_valid || fault) $fatal(1,"TB_FAIL WAIT leaked");
        @(negedge clk);request_valid=1;address=6795;
        @(negedge clk);request_valid=0;
        while(!response_valid) @(negedge clk);
        held=data;
        repeat(37) begin
            @(negedge clk);
            if(!response_valid || data !== held || request_ready) $fatal(1,"TB_FAIL held reset setup");
        end
        rstn=0;#1;
        if(response_valid || request_ready || fault) $fatal(1,"TB_FAIL RESPONSE reset");
        release_reset;
        repeat(15) @(negedge clk);
        if(response_valid || fault) $fatal(1,"TB_FAIL RESPONSE leaked");
        for(location=0;location<7168;location=location+1) begin
            if(location%512==0 || location%512==511 || location==7026) hold_cycles=37;
            else hold_cycles=location%4;
            read_word(location,hold_cycles);
        end
        @(negedge clk);request_valid=1;address=7168;
        @(negedge clk);request_valid=0;
        repeat(37) begin
            @(negedge clk);
            if(!fault || response_valid || request_ready) $fatal(1,"TB_FAIL invalid address fabricated response");
        end
        if(responses!=7168) $fatal(1,"TB_FAIL response count");
        $fclose(trace_file);
        $display("METRIC words=7168 bytes=143360 group_edges=28 valid_tail_word=7026 valid_tail_bytes=2 padding_bytes=2838 latency_min=%0d latency_max=%0d max_hold=37 invalid_address=7168 invalid_observation_cycles=37",min_latency,max_latency);
        $display("TB_PASS_REAL_MODEL_ROM_READER");$finish;
    end
    initial begin #20000000; $fatal(1,"TB_FAIL watchdog"); end // 全局超时终止挂起测试。
endmodule
