`timescale 1ns / 1ps
// Actual boot prefetch and actual LUT service share the only vendor-model reader.
module tb_rom_two_client_real;
    localparam [31:0] MODEL_ID=32'hB35D4A66;
    reg clk=0,rstn=0,cancel=0,req_valid=0,req_kind=0,rsp_ready=0,load_ready=0,table_ready=0;
    reg [9:0] req_address=0;
    reg [15:0] req_tag=0;
    reg [31:0] req_token=0,req_model=MODEL_ID;
    wire req_ready,rsp_valid,rsp_kind,rsp_error,fault,load_valid,table_valid,prefetch_done;
    wire [9:0] rsp_address,table_addr;
    wire [15:0] rsp_tag,rsp_data,table_data;
    wire [31:0] rsp_token,rsp_model,load_data,prefetch_cycles;
    wire [2:0] load_kind;
    wire [10:0] load_addr;
    reg [46:0] expected_prefetch[0:1675];
    reg [15:0] sigmoid_expected[0:1023],exp_expected[0:255];
    reg [4095:0] prefetch_path,sigmoid_path,exp_path,trace_path;
    reg [15:0] random_bits=16'hBEEF;
    reg [107:0] held_response;
    reg [45:0] held_load;
    reg [25:0] held_table;
    reg load_held=0,table_held=0,owner=0,outstanding=0,physical_seen=0,done_seen=0;
    integer cycle=0,prefetch_count=0,load_count=0,table_count=0,prefetch_done_cycle=0;
    integer param_admissions=0,lut_admissions=0,param_reads=0,lut_reads=0,param_returns=0,lut_returns=0;
    integer param_wait=0,lut_wait=0,param_wait_max=0,lut_wait_max=0;
    integer accepted_cycle,response_cycle,queries=0,latency_min=999999,latency_max=0,latency_sum=0;
    integer competing_sigmoid=0,competing_exp=0,competing_queries=0,competing_latency_max=0;
    integer index,trace_file,window_start,window_end,reads_before,returns_before,admissions_before,drain_cycles=0;
    reg [12:0] expected_rom_address=0;
    road_rom_two_client_top dut(
        .i_clk(clk),.i_rstn(rstn),.i_cancel(cancel),.i_lut_req_valid(req_valid),.i_lut_req_kind(req_kind),
        .i_lut_req_address(req_address),.i_lut_req_tag(req_tag),.i_lut_req_frame_token(req_token),.i_lut_req_model_id(req_model),
        .o_lut_req_ready(req_ready),.o_lut_rsp_valid(rsp_valid),.o_lut_rsp_kind(rsp_kind),.o_lut_rsp_address(rsp_address),
        .o_lut_rsp_tag(rsp_tag),.o_lut_rsp_frame_token(rsp_token),.o_lut_rsp_model_id(rsp_model),.o_lut_rsp_data(rsp_data),
        .o_lut_rsp_error(rsp_error),.i_lut_rsp_ready(rsp_ready),.o_fault(fault),
        .o_load_valid(load_valid),.o_load_kind(load_kind),.o_load_addr(load_addr),.o_load_data(load_data),.i_load_ready(load_ready),
        .o_table_valid(table_valid),.o_table_addr(table_addr),.o_table_data(table_data),.i_table_ready(table_ready),
        .o_prefetch_done(prefetch_done),.o_prefetch_cycles(prefetch_cycles));
    always #5 clk=~clk;
    always @(negedge clk) begin
        random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
        load_ready=rstn && (cycle%197>=61) && random_bits[1];
        table_ready=rstn && (cycle%223>=87) && random_bits[2];
    end
    // Passive event scoreboard: it never drives the arbiter/reader internal nets.
    always @(posedge clk) begin
        cycle=cycle+1;
        if(!rstn) begin
            prefetch_count=0;load_count=0;table_count=0;load_held=0;table_held=0;
            outstanding=0;physical_seen=0;done_seen=0;param_wait=0;lut_wait=0;
        end else begin
            if(fault) $fatal(1,"TB_FAIL unexpected real-model fault");
            if(load_held && (!load_valid || {load_kind,load_addr,load_data}!==held_load)) $fatal(1,"TB_FAIL load payload hold");
            if(table_held && (!table_valid || {table_addr,table_data}!==held_table)) $fatal(1,"TB_FAIL table payload hold");
            load_held=load_valid && !load_ready;held_load={load_kind,load_addr,load_data};
            table_held=table_valid && !table_ready;held_table={table_addr,table_data};
            if(load_valid && load_ready) begin
                if(prefetch_count>=1676 || expected_prefetch[prefetch_count]!=={1'b0,load_kind,load_addr,load_data})
                    $fatal(1,"TB_FAIL true parameter index=%0d kind=%0d addr=%0d data=%h expected=%h",prefetch_count,load_kind,load_addr,load_data,expected_prefetch[prefetch_count]);
                prefetch_count=prefetch_count+1;load_count=load_count+1;
            end
            if(table_valid && table_ready) begin
                if(prefetch_count>=1676 || expected_prefetch[prefetch_count]!=={1'b1,3'd0,1'b0,table_addr,{16{table_data[15]}},table_data})
                    $fatal(1,"TB_FAIL true SiLU index=%0d addr=%0d data=%h expected=%h",prefetch_count,table_addr,table_data,expected_prefetch[prefetch_count]);
                prefetch_count=prefetch_count+1;table_count=table_count+1;
            end
            if(prefetch_done && !done_seen) begin
                if(prefetch_count!=1676 || load_count!=652 || table_count!=1024) $fatal(1,"TB_FAIL prefetch completion count");
                done_seen=1;prefetch_done_cycle=cycle;
                $display("METRIC prefetch_complete_global_cycle=%0d prefetch_reported_cycles=%0d parameters=%0d silu=%0d",cycle,prefetch_cycles,load_count,table_count);
            end
            if(dut.param_request_valid && !dut.param_request_ready) param_wait=param_wait+1; else param_wait=0;
            if(dut.lut_rom_request_valid && !dut.lut_rom_request_ready) lut_wait=lut_wait+1; else lut_wait=0;
            if(param_wait>param_wait_max) param_wait_max=param_wait;
            if(lut_wait>lut_wait_max) lut_wait_max=lut_wait;
            if((dut.param_request_valid && dut.param_request_ready)||(dut.lut_rom_request_valid && dut.lut_rom_request_ready)) begin
                if(outstanding) $fatal(1,"TB_FAIL second admission before return");
                owner=dut.lut_rom_request_valid && dut.lut_rom_request_ready;
                expected_rom_address=owner?dut.lut_rom_request_addr:dut.param_request_addr;
                outstanding=1;physical_seen=0;
                if(owner) lut_admissions=lut_admissions+1; else param_admissions=param_admissions+1;
            end
            if(dut.rom_request_valid && dut.rom_request_ready) begin
                if(!outstanding || physical_seen || dut.rom_request_addr!==expected_rom_address) $fatal(1,"TB_FAIL physical request owner/address");
                physical_seen=1;if(owner) lut_reads=lut_reads+1; else param_reads=param_reads+1;
            end
            if(dut.param_response_valid && dut.lut_rom_response_valid) $fatal(1,"TB_FAIL broadcast return");
            if(outstanding && (owner ? dut.param_response_data!==160'd0 : dut.lut_rom_response_data!==160'd0)) $fatal(1,"TB_FAIL nonowner data leakage");
            if(dut.rom_response_valid && dut.rom_response_ready) begin
                if(!outstanding || !physical_seen || !(owner?dut.lut_rom_response_valid:dut.param_response_valid)) $fatal(1,"TB_FAIL response ownership");
                if(owner) lut_returns=lut_returns+1; else param_returns=param_returns+1;
                outstanding=0;physical_seen=0;
            end
        end
    end
    task common_reset;
        begin
            @(negedge clk);rstn=0;req_valid=0;cancel=0;rsp_ready=0;#1;
            if(req_ready || rsp_valid || load_valid || table_valid || prefetch_done || fault) $fatal(1,"TB_FAIL reset not immediate");
            repeat(4) @(negedge clk);rstn=1;
            repeat(4) @(negedge clk);
            if(rsp_valid || fault) $fatal(1,"TB_FAIL reset old response");
        end
    endtask
    task start_request;
        input kind;
        input [9:0] address;
        input [15:0] tag;
        input [31:0] token,model;
        begin
            while(!req_ready) @(negedge clk);
            @(negedge clk);req_valid=1;req_kind=kind;req_address=address;req_tag=tag;req_token=token;req_model=model;
            accepted_cycle=cycle+1;
            @(negedge clk);req_valid=0;
            req_kind=~kind;req_address=~address;req_tag=~tag;req_token=~token;req_model=~model;
        end
    endtask
    task query;
        input kind;
        input [9:0] address;
        input [15:0] tag;
        input [31:0] token;
        input [15:0] expected;
        integer hold_cycles,reads_at_start;
        reg competed;
        begin
            reads_at_start=lut_reads;competed=!prefetch_done;
            start_request(kind,address,tag,token,MODEL_ID);
            while(!rsp_valid) @(negedge clk);
            response_cycle=cycle;
            if({rsp_kind,rsp_address,rsp_tag,rsp_token,rsp_model,rsp_data,rsp_error}!=={kind,address,tag,token,MODEL_ID,expected,1'b0})
                $fatal(1,"TB_FAIL LUT value/identity kind=%0d address=%0d data=%h expected=%h",kind,address,rsp_data,expected);
            if(lut_reads-reads_at_start!=1) $fatal(1,"TB_FAIL LUT physical read count");
            held_response={rsp_kind,rsp_address,rsp_tag,rsp_token,rsp_model,rsp_data,rsp_error};
            hold_cycles=random_bits[5:3];
            repeat(hold_cycles) begin
                @(negedge clk);
                if(!rsp_valid || req_ready || held_response!=={rsp_kind,rsp_address,rsp_tag,rsp_token,rsp_model,rsp_data,rsp_error}) $fatal(1,"TB_FAIL full LUT response hold");
            end
            rsp_ready=1;@(negedge clk);rsp_ready=0;
            if(rsp_valid) $fatal(1,"TB_FAIL duplicate LUT response");
            queries=queries+1;latency_sum=latency_sum+response_cycle-accepted_cycle;
            if(response_cycle-accepted_cycle<latency_min) latency_min=response_cycle-accepted_cycle;
            if(response_cycle-accepted_cycle>latency_max) latency_max=response_cycle-accepted_cycle;
            if(competed) begin
                competing_queries=competing_queries+1;
                if(kind) competing_exp=competing_exp+1; else competing_sigmoid=competing_sigmoid+1;
                if(response_cycle-accepted_cycle>competing_latency_max) competing_latency_max=response_cycle-accepted_cycle;
            end
            $fwrite(trace_file,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%h,%h,%h\n",kind,address,accepted_cycle,response_cycle,response_cycle-accepted_cycle,hold_cycles,competed,tag,token,expected);
        end
    endtask
    initial begin
        if(!$value$plusargs("PREFETCH=%s",prefetch_path)||!$value$plusargs("SIGMOID=%s",sigmoid_path)||!$value$plusargs("EXP=%s",exp_path)||!$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"TB_FAIL paths");
        $readmemh(prefetch_path,expected_prefetch);$readmemh(sigmoid_path,sigmoid_expected);$readmemh(exp_path,exp_expected);
        trace_file=$fopen(trace_path,"w");if(!trace_file) $fatal(1,"TB_FAIL trace open");
        $fwrite(trace_file,"kind,address,accept_cycle,response_cycle,latency,hold,competing,tag,token,data\n");
        common_reset;window_start=cycle;
        for(index=0;index<1024;index=index+1) begin
            repeat(random_bits[7:6]) @(negedge clk);
            query(0,index,16'h1000^index,32'h20000000+index,sigmoid_expected[index]);
            if(index<256) query(1,index,16'h4000^index,32'h30000000+index,exp_expected[index]);
        end
        window_end=cycle;while(!prefetch_done) @(negedge clk);
        if(competing_sigmoid==0 || competing_exp==0 || lut_admissions!=1280 || lut_reads!=1280 || lut_returns!=1280 || param_admissions!=param_reads || param_reads!=param_returns) $fatal(1,"TB_FAIL concurrent exhaustive coverage");
        $display("METRIC exhaustive_queries=1280 sigmoid=1024 exp=256 window_start=%0d window_end=%0d window_cycles=%0d prefetch_done_cycle=%0d competing_queries=%0d competing_sigmoid=%0d competing_exp=%0d latency_min=%0d latency_max=%0d latency_sum=%0d competing_latency_max=%0d param_admissions=%0d param_reads=%0d param_returns=%0d lut_admissions=%0d lut_reads=%0d lut_returns=%0d param_wait_max=%0d lut_wait_max=%0d",window_start,window_end,window_end-window_start,prefetch_done_cycle,competing_queries,competing_sigmoid,competing_exp,latency_min,latency_max,latency_sum,competing_latency_max,param_admissions,param_reads,param_returns,lut_admissions,lut_reads,lut_returns,param_wait_max,lut_wait_max);
        admissions_before=lut_admissions;start_request(0,31,16'hCA01,32'hCA000001,MODEL_ID);
        cancel=1;@(negedge clk);cancel=0;
        while(!req_ready) begin if(rsp_valid) $fatal(1,"TB_FAIL early cancel leak");@(negedge clk);end
        if(lut_admissions!=admissions_before) $fatal(1,"TB_FAIL early cancellation reached arbiter");
        // Cancel exactly after logical arbiter admission and before physical reader acceptance.
        admissions_before=lut_admissions;reads_before=lut_reads;returns_before=lut_returns;
        start_request(0,32,16'hCA02,32'hCA000002,MODEL_ID);
        while(lut_admissions==admissions_before) @(negedge clk);
        if(lut_reads!=reads_before) $fatal(1,"TB_FAIL queued cancel did not precede physical acceptance");
        cancel=1;@(negedge clk);cancel=0;
        while(!req_ready) begin
            if(rsp_valid) $fatal(1,"TB_FAIL canceled old token leaked");drain_cycles=drain_cycles+1;@(negedge clk);
        end
        if(lut_returns!=returns_before+1 || lut_reads!=reads_before+1 || drain_cycles==0) $fatal(1,"TB_FAIL queued cancellation did not drain");
        query(0,33,16'hCA03,32'hCA000003,sigmoid_expected[33]);
        reads_before=lut_reads;start_request(0,41,16'h5200,32'h52000000,MODEL_ID);
        while(lut_reads==reads_before) @(negedge clk);
        common_reset;query(0,42,16'h5201,32'h52000001,sigmoid_expected[42]);
        start_request(0,43,16'h5202,32'h52000002,MODEL_ID);
        while(!rsp_valid) @(negedge clk);
        repeat(11) @(negedge clk);common_reset;
        query(1,73,16'h5203,32'h52000003,exp_expected[73]);
        while(!prefetch_done) @(negedge clk);
        if(prefetch_count!=1676) $fatal(1,"TB_FAIL post-reset true prefetch");
        $display("METRIC cancel_before_admission=1 cancel_queued_before_physical=1 late_return_drained=1 drain_cycles=%0d new_token_isolation=1 physical_wait_reset=1 held_client_response_reset=1 final_prefetch_entries=%0d actual_reader_instances=1",drain_cycles,prefetch_count);
        $fclose(trace_file);$display("TB_PASS_ROM_TWO_CLIENT_REAL");$finish;
    end
    initial begin #20000000;$fatal(1,"TB_FAIL real integration watchdog");end
endmodule
