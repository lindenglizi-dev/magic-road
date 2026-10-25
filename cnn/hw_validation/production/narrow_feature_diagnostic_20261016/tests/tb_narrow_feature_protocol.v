`timescale 1ns/1ps
// Parser faults and reset cancellation use only public narrow pins.
module tb_narrow_feature_protocol(output o_test_complete);
    reg clk=0, rstn=0, rx_valid=0, tx_ready=0;
    reg [15:0] rx_data=0;
    wire rx_ready, tx_valid, busy, done, fault, table_loaded;
    wire [15:0] tx_data;
    reg complete=0;
    integer index, total_cycles=0;
    reg [15:0] held_data;
    assign o_test_complete=complete;
    always #5 clk=~clk;
    road_narrow_feature_top dut(.i_clk(clk),.i_rstn(rstn),
        .i_rx_valid(rx_valid),.i_rx_data(rx_data),.o_rx_ready(rx_ready),
        .o_tx_valid(tx_valid),.o_tx_data(tx_data),.i_tx_ready(tx_ready),
        .o_busy(busy),.o_done(done),.o_fault(fault),.o_table_loaded(table_loaded));
    always @(posedge clk)begin
        total_cycles=total_cycles+1;
        if(total_cycles>30000)$fatal(1,"NARROW_PROTOCOL watchdog");
    end
    task reset_host;
        begin
            @(negedge clk); rx_valid=0; rstn=0; tx_ready=0;
            repeat(3)@(negedge clk); rstn=1;
            repeat(3)@(negedge clk);
            if(busy || done || fault || table_loaded || tx_valid)
                $fatal(1,"NARROW_PROTOCOL reset retained ownership");
        end
    endtask
    task send_word;
        input [15:0] value;
        begin
            @(negedge clk); rx_valid=1; rx_data=value;
            @(posedge clk); while(!rx_ready)@(posedge clk);
            @(negedge clk); rx_valid=0;
        end
    endtask
    task expect_fault;
        begin
            wait(fault);
            repeat(4)begin @(negedge clk);
                if(!fault || done)$fatal(1,"NARROW_PROTOCOL fault not sticky");
            end
        end
    endtask
    task load_table;
        begin
            send_word(16'h8000);
            for(index=0;index<1024;index=index+1)send_word(index[15:0]);
            wait(table_loaded);
        end
    endtask
    initial begin
        reset_host;
        send_word(16'hffff); expect_fault;
        reset_host;
        send_word(16'h8100); expect_fault;
        reset_host;
        send_word(16'h8001); send_word(16'h0010); expect_fault;
        reset_host;
        send_word(16'h8001); send_word(16'd2);
        repeat(5)@(negedge clk);
        if(busy || table_loaded || fault || tx_valid)$fatal(1,"NARROW_PROTOCOL start before LUT");
        send_word(16'h8000);
        for(index=0;index<7;index=index+1)send_word(index[15:0]);
        repeat(3)@(negedge clk);
        if(table_loaded || busy || tx_valid)$fatal(1,"NARROW_PROTOCOL partial LUT");
        reset_host;
        load_table;
        send_word(16'h8001);
        repeat(5)@(negedge clk);
        if(busy || tx_valid)$fatal(1,"NARROW_PROTOCOL partial start");
        reset_host;
        load_table;
        send_word(16'h8001); send_word(16'd2);
        wait(tx_valid); held_data=tx_data;
        repeat(16)begin @(negedge clk);
            if(!tx_valid || tx_data!==held_data)$fatal(1,"NARROW_PROTOCOL TX stability");
        end
        // Reset cancels a stalled output packet and invalidates the actual LUT.
        reset_host;
        load_table;
        tx_ready=1;
        send_word(16'h8001); send_word(16'd2);
        // Read has highest priority; capture the complete real request before reply.
        @(posedge clk); while(!(tx_valid && tx_ready && tx_data==16'ha100))@(posedge clk);
        repeat(2)@(posedge clk);
        send_word(16'h8100);
        for(index=0;index<5;index=index+1)send_word(16'd0);
        reset_host;
        load_table;
        send_word(16'h8001); send_word(16'd2);
        wait(busy); send_word(16'h8002); expect_fault;
        reset_host;
        $display("NARROW_PROTOCOL_PASS malformed=3 early_start=1 partial_lut=1 partial_start=1 reset_stalled_tx=1 reset_partial_response=1 cancel=1");
        complete=1; $finish;
    end
endmodule

