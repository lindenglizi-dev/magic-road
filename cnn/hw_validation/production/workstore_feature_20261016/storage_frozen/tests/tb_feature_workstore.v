`timescale 1ns / 1ps
// 真实四ERAM端点自检；黄金数组仅在TB，未写内容绝不作为读期望。
module tb_feature_workstore(output o_test_complete);
    reg clk=0, rstn=0, complete=0;
    reg byte_req_valid=0, byte_req_write=0, byte_rsp_ready=0;
    reg [11:0] byte_req_addr=0;
    reg [7:0] byte_req_data=0;
    wire byte_req_ready, byte_rsp_valid, byte_rsp_error;
    wire [7:0] byte_rsp_data;
    reg weight_req_valid=0, weight_req_write=0, weight_rsp_ready=0;
    reg [4:0] weight_req_group=0;
    reg [191:0] weight_req_data=0;
    wire weight_req_ready, weight_rsp_valid, weight_rsp_error;
    wire [191:0] weight_rsp_data;
    wire fault;
    reg [7:0] gold_byte [0:3071];
    reg [191:0] gold_weight [0:23];
    reg [3071:0] byte_written=0;
    reg [23:0] weight_written=0;
    reg byte_pending=0, weight_pending=0;
    reg byte_illegal=0, weight_illegal=0;
    reg saved_byte_write=0, saved_weight_write=0;
    reg [11:0] saved_byte_addr=0;
    reg [4:0] saved_weight_group=0;
    reg [7:0] expected_byte=0;
    reg [191:0] expected_weight=0, saved_weight_data=0;
    reg held_byte=0, held_weight=0;
    reg [8:0] held_byte_payload;
    reg [192:0] held_weight_payload;
    reg expected_fault=0;
    integer byte_native=0, weight_native=0;
    integer accepted_byte=0, accepted_weight=0, retired_byte=0, retired_weight=0;
    integer aborted_byte=0, aborted_weight=0, illegal_byte=0, illegal_weight=0;
    integer native_byte=0, native_weight=0, weight_zero_pads=0;
    integer simultaneous=0, byte_replace=0, weight_replace=0;
    integer held_byte_cycles=0, held_weight_cycles=0, resets=0;
    integer test_case=0, negative_workstore=0, cycles=0, index;
    reg [79:0] expected_word;
    assign o_test_complete=complete;
    always #5 clk=~clk;

    road_feature_workstore dut(
        .i_clk(clk),.i_rstn(rstn),
        .i_byte_req_valid(byte_req_valid),.o_byte_req_ready(byte_req_ready),.i_byte_req_write(byte_req_write),
        .i_byte_req_addr(byte_req_addr),.i_byte_req_data(byte_req_data),
        .o_byte_rsp_valid(byte_rsp_valid),.i_byte_rsp_ready(byte_rsp_ready),.o_byte_rsp_data(byte_rsp_data),.o_byte_rsp_error(byte_rsp_error),
        .i_weight_req_valid(weight_req_valid),.o_weight_req_ready(weight_req_ready),.i_weight_req_write(weight_req_write),
        .i_weight_req_group(weight_req_group),.i_weight_req_data(weight_req_data),
        .o_weight_rsp_valid(weight_rsp_valid),.i_weight_rsp_ready(weight_rsp_ready),.o_weight_rsp_data(weight_rsp_data),.o_weight_rsp_error(weight_rsp_error),
        .o_fault(fault)
    );

    // 每个合法响应必须由native访问完成；非法响应完全不允许访问native。
    always @(posedge clk or negedge rstn)begin
        if(!rstn)begin
            if(byte_pending)aborted_byte=aborted_byte+1;
            if(weight_pending)aborted_weight=aborted_weight+1;
            byte_pending=0; weight_pending=0; held_byte=0; held_weight=0;
            byte_native=0; weight_native=0; expected_fault=0;
            byte_written=0; weight_written=0;
        end else begin
            cycles=cycles+1;
            if(cycles>20000)$fatal(1,"workstore watchdog");
            if(dut.flag_byte_native_enable)begin
                if(!byte_pending || byte_illegal)$fatal(1,"illegal or unsolicited byte native access");
                if(dut.flag_byte_native_write!==saved_byte_write)$fatal(1,"byte native direction mismatch");
                byte_native=byte_native+1; native_byte=native_byte+1;
            end
            if(dut.flag_weight_native_enable)begin
                if(!weight_pending || weight_illegal)$fatal(1,"illegal or unsolicited weight native access");
                if(dut.flag_weight_native_write!==saved_weight_write)$fatal(1,"weight native direction mismatch");
                if(dut.reg_weight_native_addr!==saved_weight_group*3+weight_native)
                    $fatal(1,"weight native word address mismatch");
                if(saved_weight_write)begin
                    case(weight_native)
                        0: expected_word=saved_weight_data[79:0];
                        1: expected_word=saved_weight_data[159:80];
                        2: expected_word={48'd0,saved_weight_data[191:160]};
                        default: $fatal(1,"too many native weight words");
                    endcase
                    if(dut.reg_weight_native_data!==expected_word)$fatal(1,"weight native full-word mismatch");
                    if(weight_native==2)weight_zero_pads=weight_zero_pads+1;
                end
                weight_native=weight_native+1; native_weight=native_weight+1;
            end
            if(held_byte && (!byte_rsp_valid || {byte_rsp_error,byte_rsp_data}!==held_byte_payload))
                $fatal(1,"byte response changed under backpressure");
            if(held_weight && (!weight_rsp_valid || {weight_rsp_error,weight_rsp_data}!==held_weight_payload))
                $fatal(1,"weight response changed under backpressure");
            if(byte_rsp_valid)begin
                if(!byte_pending || byte_rsp_error!==byte_illegal)$fatal(1,"byte response identity/error mismatch");
                if(byte_native!=(byte_illegal ? 0 : 1))$fatal(1,"byte response before native completion");
                if(negative_workstore!=0 && !saved_byte_write && !byte_illegal)begin
                    if(byte_rsp_data!==(expected_byte^8'd1))$fatal(1,"NEGATIVE_WORKSTORE injected data mismatch");
                end else if(byte_rsp_data!==expected_byte)$fatal(1,"byte read/write response mismatch");
            end
            if(weight_rsp_valid)begin
                if(!weight_pending || weight_rsp_error!==weight_illegal)$fatal(1,"weight response identity/error mismatch");
                if(weight_native!=(weight_illegal ? 0 : 3))$fatal(1,"weight response before all native words completed");
                if(weight_rsp_data!==expected_weight)$fatal(1,"weight all192 response mismatch");
            end
            held_byte=byte_rsp_valid&&!byte_rsp_ready;
            held_weight=weight_rsp_valid&&!weight_rsp_ready;
            held_byte_payload={byte_rsp_error,byte_rsp_data}; held_weight_payload={weight_rsp_error,weight_rsp_data};
            if(held_byte)held_byte_cycles=held_byte_cycles+1;
            if(held_weight)held_weight_cycles=held_weight_cycles+1;
            if(byte_rsp_valid && byte_rsp_ready)begin byte_pending=0; retired_byte=retired_byte+1; end
            if(weight_rsp_valid && weight_rsp_ready)begin weight_pending=0; retired_weight=retired_weight+1; end
            if(byte_req_valid && byte_req_ready)begin
                if(byte_pending)$fatal(1,"multiple byte outstanding");
                if(byte_rsp_valid&&byte_rsp_ready)byte_replace=byte_replace+1;
                byte_pending=1; byte_native=0; accepted_byte=accepted_byte+1;
                saved_byte_addr=byte_req_addr; saved_byte_write=byte_req_write;
                byte_illegal=byte_req_addr>=3072; expected_byte=0;
                if(byte_illegal)begin illegal_byte=illegal_byte+1; expected_fault=1; end
                else if(byte_req_write)begin gold_byte[byte_req_addr]=byte_req_data; byte_written[byte_req_addr]=1; end
                else begin
                    if(!byte_written[byte_req_addr])$fatal(1,"TB attempted unwritten byte read");
                    expected_byte=gold_byte[byte_req_addr];
                end
            end
            if(weight_req_valid && weight_req_ready)begin
                if(weight_pending)$fatal(1,"multiple weight outstanding");
                if(weight_rsp_valid&&weight_rsp_ready)weight_replace=weight_replace+1;
                weight_pending=1; weight_native=0; accepted_weight=accepted_weight+1;
                saved_weight_group=weight_req_group; saved_weight_write=weight_req_write; saved_weight_data=weight_req_data;
                weight_illegal=weight_req_group>=24; expected_weight=0;
                if(weight_illegal)begin illegal_weight=illegal_weight+1; expected_fault=1; end
                else if(weight_req_write)begin gold_weight[weight_req_group]=weight_req_data; weight_written[weight_req_group]=1; end
                else begin
                    if(!weight_written[weight_req_group])$fatal(1,"TB attempted unwritten weight read");
                    expected_weight=gold_weight[weight_req_group];
                end
            end
            if(byte_req_valid&&byte_req_ready&&weight_req_valid&&weight_req_ready)simultaneous=simultaneous+1;
        end
    end

    // 在NBA更新后核查粘滞故障及单在途反压。
    always @(negedge clk)if(rstn)begin
        if(fault!==expected_fault)$fatal(1,"fault sticky mismatch");
        if(byte_pending && !byte_rsp_ready && byte_req_ready)$fatal(1,"byte ready while occupied");
        if(weight_pending && !weight_rsp_ready && weight_req_ready)$fatal(1,"weight ready while occupied");
    end

    task common_reset;
        begin
            @(negedge clk); rstn=0; resets=resets+1;
            byte_req_valid=0; weight_req_valid=0; byte_rsp_ready=0; weight_rsp_ready=0;
            repeat(3)@(negedge clk);
            if(byte_rsp_valid || weight_rsp_valid || fault)$fatal(1,"reset retained old response/fault");
            rstn=1; @(negedge clk);
            if(byte_rsp_valid || weight_rsp_valid || fault)$fatal(1,"reset released stale response");
        end
    endtask

    task byte_transaction;
        input write_request;
        input [11:0] address;
        input [7:0] data;
        input integer hold_cycles;
        begin
            @(negedge clk); byte_req_valid=1; byte_req_write=write_request; byte_req_addr=address; byte_req_data=data;
            @(posedge clk); while(!byte_req_ready)@(posedge clk);
            @(negedge clk); byte_req_valid=0;
            while(!byte_rsp_valid)@(negedge clk);
            repeat(hold_cycles)@(negedge clk);
            byte_rsp_ready=1; @(posedge clk); @(negedge clk); byte_rsp_ready=0;
        end
    endtask

    task weight_transaction;
        input write_request;
        input [4:0] group;
        input [191:0] data;
        input integer hold_cycles;
        begin
            @(negedge clk); weight_req_valid=1; weight_req_write=write_request; weight_req_group=group; weight_req_data=data;
            @(posedge clk); while(!weight_req_ready)@(posedge clk);
            @(negedge clk); weight_req_valid=0;
            while(!weight_rsp_valid)@(negedge clk);
            repeat(hold_cycles)@(negedge clk);
            weight_rsp_ready=1; @(posedge clk); @(negedge clk); weight_rsp_ready=0;
        end
    endtask

    // 四个边界和全部权重位，两个请求端点同拍发起。
    task write_then_read;
        begin
            fork
                begin
                    byte_transaction(1,0,8'h81,0); byte_transaction(1,2047,8'h7f,0);
                    byte_transaction(1,2048,8'h55,0); byte_transaction(1,3071,8'haa,0);
                end
                begin
                    for(index=0;index<24;index=index+1)
                        weight_transaction(1,index,{32'h89abcdef^index,32'h76543210^index,32'hfedcba98^index,32'h01234567^index,32'ha55a5aa5^index,32'hc33cc33c^index},0);
                end
            join
            fork
                begin
                    byte_transaction(0,0,0,test_case==1 ? 128 : 0); byte_transaction(0,2047,0,0);
                    byte_transaction(0,2048,0,0); byte_transaction(0,3071,0,0);
                end
                begin
                    for(index=0;index<24;index=index+1)weight_transaction(0,index,0,test_case==1 && index==0 ? 128 : 0);
                end
            join
        end
    endtask

    task replace_responses;
        begin
            fork
                begin
                    @(negedge clk); byte_req_valid=1; byte_req_write=0; byte_req_addr=0;
                    @(posedge clk); while(!byte_req_ready)@(posedge clk);
                    @(negedge clk); byte_req_valid=0;
                    while(!byte_rsp_valid)@(negedge clk);
                    byte_req_valid=1; byte_req_addr=3071;
                    repeat(16)begin @(negedge clk); if(byte_req_ready)$fatal(1,"byte accepted queued request before retirement"); end
                    byte_rsp_ready=1;
                    @(posedge clk); if(!byte_req_ready || !byte_rsp_valid)$fatal(1,"byte simultaneous retirement refused");
                    @(negedge clk); byte_req_valid=0; byte_rsp_ready=0;
                    while(!byte_rsp_valid)@(negedge clk);
                    byte_rsp_ready=1; @(posedge clk); @(negedge clk); byte_rsp_ready=0;
                end
                begin
                    @(negedge clk); weight_req_valid=1; weight_req_write=0; weight_req_group=0;
                    @(posedge clk); while(!weight_req_ready)@(posedge clk);
                    @(negedge clk); weight_req_valid=0;
                    while(!weight_rsp_valid)@(negedge clk);
                    weight_req_valid=1; weight_req_group=23;
                    repeat(16)begin @(negedge clk); if(weight_req_ready)$fatal(1,"weight accepted queued request before retirement"); end
                    weight_rsp_ready=1;
                    @(posedge clk); if(!weight_req_ready || !weight_rsp_valid)$fatal(1,"weight simultaneous retirement refused");
                    @(negedge clk); weight_req_valid=0; weight_rsp_ready=0;
                    while(!weight_rsp_valid)@(negedge clk);
                    weight_rsp_ready=1; @(posedge clk); @(negedge clk); weight_rsp_ready=0;
                end
            join
        end
    endtask

    initial begin
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("NEGATIVE_WORKSTORE=%d",negative_workstore))negative_workstore=0;
        if(test_case<0 || test_case>1)$fatal(1,"unsupported workstore CASE");
        common_reset;
        write_then_read;
        replace_responses;
        fork
            begin byte_transaction(0,3072,0,0); byte_transaction(1,4095,8'hff,0); end
            begin weight_transaction(0,24,0,0); weight_transaction(1,31,{192{1'b1}},0); end
        join
        // 非法写后重新读边界，证明没有破坏合法内容且故障持续。
        fork
            begin byte_transaction(0,0,0,0); byte_transaction(0,3071,0,0); end
            begin weight_transaction(0,0,0,0); weight_transaction(0,23,0,0); end
        join
        if(!fault || illegal_byte!=2 || illegal_weight!=2)$fatal(1,"illegal/sticky coverage incomplete");
        if(test_case==1)begin
            common_reset;
            // 一组权重只提交第一个native word即复位，取消未完成写响应。
            @(negedge clk); byte_req_valid=1; byte_req_write=1; byte_req_addr=3071; byte_req_data=8'hcc;
            weight_req_valid=1; weight_req_write=1; weight_req_group=23; weight_req_data={192{1'b1}};
            @(posedge clk); if(!byte_req_ready || !weight_req_ready)$fatal(1,"independent writes not admitted");
            @(negedge clk); byte_req_valid=0; weight_req_valid=0;
            wait(weight_native==1);
            common_reset;
            write_then_read;
            // 两通道同时读；第一个weight native word后复位，旧响应被共同取消。
            @(negedge clk); byte_req_valid=1; byte_req_write=0; byte_req_addr=2048;
            weight_req_valid=1; weight_req_write=0; weight_req_group=0;
            @(posedge clk); if(!byte_req_ready || !weight_req_ready)$fatal(1,"independent reads not admitted");
            @(negedge clk); byte_req_valid=0; weight_req_valid=0;
            wait(weight_native==1);
            common_reset;
            write_then_read;
            if(aborted_weight!=2 || aborted_byte!=2 || resets!=4 || held_byte_cycles<256 || held_weight_cycles<256)
                $fatal(1,"reset/long-backpressure coverage incomplete");
        end
        if(byte_pending || weight_pending || byte_rsp_valid || weight_rsp_valid)$fatal(1,"unfinished transactions");
        if(accepted_byte!=retired_byte+aborted_byte || accepted_weight!=retired_weight+aborted_weight ||
            simultaneous<4 || byte_replace!=1 || weight_replace!=1 || weight_zero_pads!=(test_case==1 ? 72 : 24))
            $fatal(1,"workstore ledger/coverage mismatch");
        $display("FEATURE_WORKSTORE_PASS case=%0d accepted_byte=%0d retired_byte=%0d accepted_weight=%0d retired_weight=%0d aborted_byte=%0d aborted_weight=%0d illegal_byte=%0d illegal_weight=%0d native_byte=%0d native_weight=%0d zero_pads=%0d simultaneous=%0d byte_replace=%0d weight_replace=%0d held_byte=%0d held_weight=%0d resets=%0d cycles=%0d",
            test_case,accepted_byte,retired_byte,accepted_weight,retired_weight,aborted_byte,aborted_weight,illegal_byte,illegal_weight,native_byte,native_weight,weight_zero_pads,simultaneous,byte_replace,weight_replace,held_byte_cycles,held_weight_cycles,resets,cycles);
        complete=1; $finish;
    end
endmodule
