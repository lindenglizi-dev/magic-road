`timescale 1ns / 1ps
// Exhaustive reader trace: one run binds the frozen baseline, one binds ROM-R1.
module tb_rom_reader_cycle_trace(output reg o_test_done);
    reg clk=0;
    always #5 clk=~clk;

    reg rstn=0,request_valid=0,response_ready=0;
    reg [12:0]address=0;
    wire request_ready,response_valid,fault;
    wire [159:0]data;
    reg [159:0]golden[0:7167],held;
    reg [4095:0]words_path,trace_path;
    integer trace_file,cycle=0,location,responses=0,hold_cycles;

    road_numeric_rom_reader dut(
        .i_clk(clk),.i_rstn(rstn),.i_request_valid(request_valid),
        .i_request_addr(address),.o_request_ready(request_ready),
        .o_response_valid(response_valid),.o_response_data(data),
        .i_response_ready(response_ready),.o_fault(fault)
    );

    always @(posedge clk) begin
        #1;
        cycle=cycle+1;
        $fwrite(trace_file,"%0d,%b,%b,%04h,%b,%b,%040h,%b,%b\n",cycle,rstn,
            request_valid,address,request_ready,response_valid,data,response_ready,fault);
    end

    task release_reset;
        begin
            repeat(4) @(negedge clk);
            rstn=1;
        end
    endtask

    task read_word;
        input integer word_location;
        input integer response_hold;
        begin
            @(negedge clk);
            while(!request_ready) @(negedge clk);
            request_valid=1;
            address=word_location;
            @(negedge clk);
            request_valid=0;
            while(!response_valid) @(negedge clk);
            if(fault || data !== golden[word_location])
                $fatal(1,"ROM exhaustive mismatch address=%0d",word_location);
            held=data;
            repeat(response_hold) begin
                @(negedge clk);
                if(!response_valid || request_ready || data !== held)
                    $fatal(1,"ROM response hold changed address=%0d",word_location);
            end
            response_ready=1;
            @(negedge clk);
            response_ready=0;
            if(response_valid) $fatal(1,"ROM response duplicated address=%0d",word_location);
            responses=responses+1;
        end
    endtask

    initial begin
        o_test_done=0;
        if(!$value$plusargs("WORDS=%s",words_path)) $fatal(1,"Missing words path");
        if(!$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"Missing trace path");
        trace_file=$fopen(trace_path,"w");
        if(trace_file==0) $fatal(1,"Cannot open trace path");
        $readmemh(words_path,golden);
        $fwrite(trace_file,"cycle,rstn,request_valid,address,request_ready,response_valid,data,response_ready,fault\n");

        release_reset;

        // Cancel a request while the fixed WAIT interval is active.
        @(negedge clk);request_valid=1;address=13'd37;
        @(negedge clk);request_valid=0;
        repeat(2) @(negedge clk);
        rstn=0;#1;
        if(response_valid || request_ready || fault) $fatal(1,"WAIT reset was not immediate");
        release_reset;
        repeat(15) @(negedge clk);
        if(response_valid || fault) $fatal(1,"WAIT request leaked after reset");

        // Cancel a held response without accepting it.
        @(negedge clk);request_valid=1;address=13'd6795;
        @(negedge clk);request_valid=0;
        while(!response_valid) @(negedge clk);
        held=data;
        repeat(17) begin
            @(negedge clk);
            if(!response_valid || data !== held || request_ready)
                $fatal(1,"RESPONSE backpressure hold failed");
        end
        rstn=0;#1;
        if(response_valid || request_ready || fault) $fatal(1,"RESPONSE reset was not immediate");
        release_reset;
        repeat(15) @(negedge clk);
        if(response_valid || fault) $fatal(1,"RESPONSE leaked after reset");

        // Cover every legal word. Group first/last words receive the long hold.
        for(location=0;location<7168;location=location+1) begin
            if(location[8:0]==9'd0 || location[8:0]==9'd511) hold_cycles=17;
            else hold_cycles=location%4;
            read_word(location,hold_cycles);
        end

        // Group fourteen is absent: address 7168 must fault and never complete.
        @(negedge clk);
        while(!request_ready) @(negedge clk);
        request_valid=1;address=13'd7168;
        @(negedge clk);request_valid=0;
        repeat(4) begin
            @(negedge clk);
            if(!fault || response_valid || request_ready)
                $fatal(1,"Invalid group fabricated completion");
        end
        if(responses!=7168) $fatal(1,"Response count mismatch %0d",responses);

        $fclose(trace_file);
        o_test_done=1;
        $display("TB_PASS_ROM_READER_CYCLE_TRACE words=7168 group_edges=28 wait_reset=1 response_reset=1 max_hold=17 invalid=7168");
        $finish;
    end

    initial begin
        #20000000;
        $fatal(1,"Timeout");
    end
endmodule
