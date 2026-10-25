`timescale 1ns / 1ps
// One production wiring top: its only reader uses the actual PH1P ERAM model.
module tb_real_model_lut;
    localparam [31:0] MODEL_ID=32'hB35D4A66;
    reg i_clk=0,i_rstn=0,i_cancel=0,i_lut_req_valid=0,i_lut_req_kind=0,i_lut_rsp_ready=0;
    always #5 i_clk=~i_clk;
    reg [9:0] i_lut_req_address=0;
    reg [15:0] i_lut_req_tag=0;
    reg [31:0] i_lut_req_frame_token=0,i_lut_req_model_id=MODEL_ID;
    wire o_lut_req_ready,o_lut_rsp_valid,o_lut_rsp_kind,o_lut_rsp_error,o_fault;
    wire [9:0] o_lut_rsp_address;
    wire [15:0] o_lut_rsp_tag,o_lut_rsp_data;
    wire [31:0] o_lut_rsp_frame_token,o_lut_rsp_model_id;
    reg [15:0] sigmoid_expected[0:1023],exp_expected[0:255];
    reg [107:0] held_response;
    reg [4095:0] sigmoid_path,exp_path,trace_path;
    integer trace_file,cycle=0,rom_reads=0,rom_returns=0,rom_wait_cycles=0;
    integer index,reads_before,returns_before,accepted_cycle,response_cycle;
    integer min_latency=999,max_latency=0,latency_sum=0,queries=0,drain_cycles=0;
    road_real_model_lut_top dut(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_cancel(i_cancel),
        .i_lut_req_valid(i_lut_req_valid),.i_lut_req_kind(i_lut_req_kind),
        .i_lut_req_address(i_lut_req_address),.i_lut_req_tag(i_lut_req_tag),
        .i_lut_req_frame_token(i_lut_req_frame_token),.i_lut_req_model_id(i_lut_req_model_id),
        .o_lut_req_ready(o_lut_req_ready),.o_lut_rsp_valid(o_lut_rsp_valid),
        .o_lut_rsp_kind(o_lut_rsp_kind),.o_lut_rsp_address(o_lut_rsp_address),
        .o_lut_rsp_tag(o_lut_rsp_tag),.o_lut_rsp_frame_token(o_lut_rsp_frame_token),
        .o_lut_rsp_model_id(o_lut_rsp_model_id),.o_lut_rsp_data(o_lut_rsp_data),
        .o_lut_rsp_error(o_lut_rsp_error),.i_lut_rsp_ready(i_lut_rsp_ready),.o_fault(o_fault)
    );
    // Passive observations only: these wires are never forced or driven by the TB.
    always @(posedge i_clk) begin
        if(i_rstn) begin
            if(dut.rom_request_valid && dut.rom_request_ready) rom_reads=rom_reads+1;
            if(dut.rom_response_valid && dut.rom_response_ready) rom_returns=rom_returns+1;
            if(!dut.rom_request_ready && !dut.rom_response_valid) rom_wait_cycles=rom_wait_cycles+1;
        end
        #1;cycle=cycle+1;
    end
    task common_reset;
        begin
            @(negedge i_clk);i_rstn=0;i_lut_req_valid=0;i_cancel=0;i_lut_rsp_ready=0;#1;
            if(o_lut_rsp_valid || o_lut_req_ready || o_fault) $fatal(1,"TB_FAIL reset not immediate");
            repeat(4) @(negedge i_clk);i_rstn=1;
            repeat(15) @(negedge i_clk);
            if(o_lut_rsp_valid || o_fault) $fatal(1,"TB_FAIL reset leaked response");
        end
    endtask
    task start_request;
        input kind;
        input [9:0] address;
        input [15:0] tag;
        input [31:0] frame_token,model_id;
        begin
            while(!o_lut_req_ready) @(negedge i_clk);
            @(negedge i_clk);
            i_lut_req_valid=1;i_lut_req_kind=kind;i_lut_req_address=address;
            i_lut_req_tag=tag;i_lut_req_frame_token=frame_token;i_lut_req_model_id=model_id;
            accepted_cycle=cycle+1;
            @(negedge i_clk);i_lut_req_valid=0;
            // Deliberately change all idle request fields: response must use latched identity.
            i_lut_req_kind=~kind;i_lut_req_address=~address;i_lut_req_tag=~tag;
            i_lut_req_frame_token=~frame_token;i_lut_req_model_id=~model_id;
        end
    endtask
    task query;
        input kind;
        input [9:0] address;
        input [15:0] tag;
        input [31:0] frame_token,model_id;
        input [15:0] expected_data;
        input expected_error;
        input integer hold_cycles;
        integer reads_at_start;
        begin
            reads_at_start=rom_reads;
            start_request(kind,address,tag,frame_token,model_id);
            while(!o_lut_rsp_valid) @(negedge i_clk);
            response_cycle=cycle;
            if({o_lut_rsp_kind,o_lut_rsp_address,o_lut_rsp_tag,o_lut_rsp_frame_token,
                o_lut_rsp_model_id,o_lut_rsp_data,o_lut_rsp_error} !==
                {kind,address,tag,frame_token,model_id,expected_data,expected_error} || o_fault)
                $fatal(1,"TB_FAIL LUT identity/value kind=%0d address=%0d data=%h expected=%h",kind,address,o_lut_rsp_data,expected_data);
            if(rom_reads-reads_at_start != (expected_error ? 0 : 1)) $fatal(1,"TB_FAIL ROM read count");
            held_response={o_lut_rsp_kind,o_lut_rsp_address,o_lut_rsp_tag,o_lut_rsp_frame_token,
                o_lut_rsp_model_id,o_lut_rsp_data,o_lut_rsp_error};
            repeat(hold_cycles) begin
                @(negedge i_clk);
                if(!o_lut_rsp_valid || o_lut_req_ready || held_response !==
                    {o_lut_rsp_kind,o_lut_rsp_address,o_lut_rsp_tag,o_lut_rsp_frame_token,
                    o_lut_rsp_model_id,o_lut_rsp_data,o_lut_rsp_error}) $fatal(1,"TB_FAIL LUT held response");
            end
            $fwrite(trace_file,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%04h,%08h,%08h,%04h\n",
                kind,address,accepted_cycle,response_cycle,response_cycle-accepted_cycle,
                hold_cycles,rom_reads-reads_at_start,expected_error,tag,frame_token,model_id,o_lut_rsp_data);
            i_lut_rsp_ready=1;@(negedge i_clk);i_lut_rsp_ready=0;
            if(o_lut_rsp_valid) $fatal(1,"TB_FAIL duplicate LUT response");
            if(!expected_error) begin
                if(response_cycle-accepted_cycle<min_latency) min_latency=response_cycle-accepted_cycle;
                if(response_cycle-accepted_cycle>max_latency) max_latency=response_cycle-accepted_cycle;
                latency_sum=latency_sum+response_cycle-accepted_cycle;queries=queries+1;
            end
        end
    endtask
    initial begin
        if(!$value$plusargs("SIGMOID=%s",sigmoid_path) || !$value$plusargs("EXP=%s",exp_path) ||
            !$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"TB_FAIL missing input paths");
        $readmemh(sigmoid_path,sigmoid_expected);$readmemh(exp_path,exp_expected);
        trace_file=$fopen(trace_path,"w");if(trace_file==0) $fatal(1,"TB_FAIL trace open");
        $fwrite(trace_file,"kind,address,accepted_cycle,response_cycle,latency_cycles,hold_cycles,rom_reads,error,tag,frame_token,model_id,data\n");
        common_reset;
        reads_before=rom_reads;
        for(index=0;index<1024;index=index+1) begin
            repeat(index%4) @(negedge i_clk);
            query(0,index,16'h1000^index,32'h20000000+index,MODEL_ID,sigmoid_expected[index],0,index%5);
        end
        for(index=0;index<256;index=index+1) begin
            repeat(index%4) @(negedge i_clk);
            query(1,index,16'h4000^index,32'h21000000+index,MODEL_ID,exp_expected[index],0,index%5);
        end
        if(rom_reads-reads_before!=1280) $fatal(1,"TB_FAIL exhaustive reads");
        $display("METRIC exhaustive_entries=1280 rom_reads=1280 latency_min=%0d latency_max=%0d latency_sum=%0d",min_latency,max_latency,latency_sum);
        query(0,17,16'h55AA,32'h12345678,MODEL_ID,sigmoid_expected[17],0,37);
        reads_before=rom_reads;
        query(0,9,16'hDEAD,32'hCAFEBABE,32'hA55A1234,0,1,9);
        query(1,256,16'h0100,32'h100,MODEL_ID,0,1,0);
        query(1,1023,16'h03FF,32'h3FF,MODEL_ID,0,1,0);
        if(rom_reads!=reads_before) $fatal(1,"TB_FAIL invalid reached ROM");
        // Cancel while the real service is still dividing the byte address.
        reads_before=rom_reads;start_request(0,31,16'hCA01,32'hCA000001,MODEL_ID);
        i_cancel=1;@(negedge i_clk);
        if(o_lut_req_ready || o_lut_rsp_valid || dut.rom_request_valid) $fatal(1,"TB_FAIL early cancel");
        i_cancel=0;while(!o_lut_req_ready) @(negedge i_clk);
        if(rom_reads!=reads_before) $fatal(1,"TB_FAIL early cancel read ROM");
        // Accepted real ROM read returns late. No client may reuse ownership during DRAIN.
        reads_before=rom_reads;returns_before=rom_returns;
        start_request(0,32,16'hCA02,32'hCA000002,MODEL_ID);
        while(rom_reads==reads_before) @(negedge i_clk);
        i_cancel=1;@(negedge i_clk);i_cancel=0;
        while(!o_lut_req_ready) begin
            if(o_lut_rsp_valid) $fatal(1,"TB_FAIL canceled response leaked");
            drain_cycles=drain_cycles+1;@(negedge i_clk);
        end
        if(rom_returns!=returns_before+1 || rom_reads!=reads_before+1 || drain_cycles==0)
            $fatal(1,"TB_FAIL drain failed to consume exactly one late return");
        query(0,33,16'hCA03,32'hCA000003,MODEL_ID,sigmoid_expected[33],0,0);
        reads_before=rom_reads;start_request(0,41,16'h5200,32'h52000000,MODEL_ID);
        while(rom_reads==reads_before) @(negedge i_clk);
        common_reset;
        query(0,42,16'h5201,32'h52000001,MODEL_ID,sigmoid_expected[42],0,0);
        start_request(0,43,16'h5202,32'h52000002,MODEL_ID);
        while(!o_lut_rsp_valid) @(negedge i_clk);
        repeat(11) @(negedge i_clk);common_reset;
        query(1,73,16'h5203,32'h52000003,MODEL_ID,exp_expected[73],0,0);
        $display("METRIC total_rom_reads=%0d total_rom_returns=%0d reader_wait_cycles=%0d drain_cycles=%0d valid_queries=%0d cancel_before_accept=1 cancel_accepted=1 wait_reset=1 held_response_reset=1 invalid_no_read=3 max_client_hold=37",rom_reads,rom_returns,rom_wait_cycles,drain_cycles,queries);
        $fclose(trace_file);$display("TB_PASS_REAL_MODEL_LUT");$finish;
    end
    initial begin #20000000;$fatal(1,"TB_FAIL watchdog");end
endmodule
