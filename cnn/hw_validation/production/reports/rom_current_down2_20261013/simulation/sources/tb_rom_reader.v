`timescale 1ns / 1ps
module tb_rom_reader(output reg o_test_done);
    reg clk=0; always #5 clk=~clk;
    reg rstn=0,request_valid=0,response_ready=0;
    reg [12:0]address=0;
    wire request_ready,response_valid,fault;
    wire [159:0]data;
    reg [159:0]golden[0:7167],held;
    integer group,index,checks=0;
    reg [4095:0]path;
    road_numeric_rom_reader dut(.i_clk(clk),.i_rstn(rstn),.i_request_valid(request_valid),
        .i_request_addr(address),.o_request_ready(request_ready),.o_response_valid(response_valid),
        .o_response_data(data),.i_response_ready(response_ready),.o_fault(fault));
    task read;
        input integer location;
        begin
            @(negedge clk);request_valid=1;address=location;
            while(!request_ready) @(negedge clk);
            @(negedge clk);request_valid=0;
            while(!response_valid) @(negedge clk);
            if(data !== golden[location] || fault) $fatal(1,"ROM boundary mismatch %0d",location);
            held=data;
            repeat(17) begin @(negedge clk);if(!response_valid || data!==held || request_ready) $fatal(1,"ROM hold failed"); end
            response_ready=1;@(negedge clk);response_ready=0;
            if(response_valid) $fatal(1,"ROM response duplicated");
            checks=checks+1;
        end
    endtask
    initial begin
        o_test_done=0;
        if(!$value$plusargs("WORDS=%s",path)) $fatal(1,"Missing words path");
        $readmemh(path,golden);
        repeat(4) @(negedge clk);rstn=1;
        for(group=0;group<14;group=group+1) begin read(group*512);read(group*512+511); end
        read(29);read(36);read(43);read(73);read(6795);read(6898);
        @(negedge clk);request_valid=1;address=512;@(negedge clk);request_valid=0;
        repeat(2) @(negedge clk);rstn=0;#1;
        if(response_valid || request_ready) $fatal(1,"Reset output not masked");
        repeat(4) @(negedge clk);rstn=1;repeat(15) @(negedge clk);
        if(response_valid) $fatal(1,"Old read leaked");
        read(7167);
        @(negedge clk);request_valid=1;address=7168;@(negedge clk);request_valid=0;
        if(!fault || response_valid || request_ready) $fatal(1,"Invalid ROM address not rejected");
        o_test_done=1;$display("TB_PASS_ROM_READER words=%0d bank_boundaries=28 reset_cancel=1 hold=17 invalid=1",checks);$finish;
    end
    initial begin #5000000; $fatal(1,"Timeout"); end
endmodule
