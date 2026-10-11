`timescale 1ns / 1ps
`include "counts.vh"
module tb_low_io;
    reg clk=0, rstn=0, rx_valid=0, tx_ready=0;
    reg [15:0] rx_data=0;
    wire rx_ready, tx_valid;
    wire [15:0] tx_data;
    reg [15:0] table_words[0:1023];
    reg [95:0] accum, pre;
    reg [17:0] shifts;
    reg [31:0] post;
    reg [5:0] post_shift;
    reg activate;
    reg [2:0] mask;
    reg [47:0] tags, expected;
    reg [303:0] packet;
    reg [15:0] got_tag, got_data, got_status;
    reg [15:0] held_data;
    reg held=0;
    integer fd, fields, batch, lane, word_index, outputs=0, cycles=0;
    integer seed=42, stalls, noise;
    always #5 clk=!clk;
    always @(posedge clk) begin
        cycles=cycles+1;
        if (cycles>200000) $fatal(1,"watchdog");
        if (!rstn) held=0;
        else begin
            if (held && (!tx_valid || tx_data!==held_data)) $fatal(1,"held payload changed");
            held=tx_valid && !tx_ready; held_data=tx_data;
        end
    end
    road_dynamic_low_io_top dut(clk,rstn,rx_valid,rx_data,rx_ready,tx_valid,tx_data,tx_ready);
    task send;
        input [15:0] value;
        begin
            @(negedge clk); rx_valid=1; rx_data=value;
            begin: wait_rx
                forever begin
                    @(posedge clk);
                    if (rx_ready) disable wait_rx;
                end
            end
            @(negedge clk); rx_valid=0; rx_data=16'hdead;
        end
    endtask
    task receive;
        output [15:0] value;
        begin
            stalls=0;
            begin: wait_tx
                forever begin
                    @(negedge clk); noise=$random(seed)&32'h7fffffff;
                    tx_ready=noise%4!=0;
                    if (tx_valid && stalls<5) begin tx_ready=0; stalls=stalls+1; end
                    @(posedge clk);
                    if (tx_valid && tx_ready) begin value=tx_data; disable wait_tx; end
                end
            end
            @(negedge clk); tx_ready=0;
        end
    endtask
    task reset_load;
        integer address;
        begin
            @(negedge clk); rstn=0; rx_valid=0; tx_ready=0;
            #1; if (rx_ready || tx_valid) $fatal(1,"reset cancel");
            repeat(3) @(negedge clk);
            rstn=1; repeat(3) @(negedge clk);
            send(16'ha000);
            for(address=0;address<1024;address=address+1) send(table_words[address]);
        end
    endtask
    initial begin
        $readmemh("table.hex",table_words);
        fd=$fopen("batches.txt","r"); if(!fd) $fatal(1,"vectors");
        // Partial packet and partial table must be cancelled, never submitted.
        rstn=1; repeat(4) @(negedge clk);
        send(16'hb000); send(16'h1234);
        repeat(20) @(negedge clk);
        if(dut.flag_input_ready || tx_valid || dut.reg_input_count!=0) $fatal(1,"partial packet");
        reset_load;
        for(batch=0;batch<`BATCH_COUNT;batch=batch+1) begin
            fields=$fscanf(fd,"%h %h %h %h %h %h %h %h %h\n",accum,pre,shifts,post,post_shift,activate,mask,tags,expected);
            if(fields!=9) $fatal(1,"parse");
            packet={3'd0,1'b0,tags,mask,activate,post_shift,post,shifts,pre,accum};
            send(16'hb000);
            for(word_index=0;word_index<19;word_index=word_index+1) send(packet[word_index*16+:16]);
            for(lane=0;lane<3;lane=lane+1) if(mask[lane]) begin
                receive(got_tag); receive(got_data); receive(got_status);
                if(got_tag!==tags[lane*16+:16] || got_data!==expected[lane*16+:16] || got_status!=={14'd0,!activate,1'b0})
                    $fatal(1,"shell mismatch batch=%0d lane=%0d",batch,lane);
                outputs=outputs+1;
            end
        end
        send(16'hc000); receive(got_tag); receive(got_data); receive(got_status);
        if(got_tag!=`BATCH_COUNT || got_data!=outputs || got_status!=2) $fatal(1,"counters");
        @(negedge clk); rstn=0;
        repeat(3) @(negedge clk); rstn=1;
        repeat(3) @(negedge clk);
        send(16'ha000); send(table_words[0]);
        @(negedge clk); rstn=0;
        #1; if(tx_valid || rx_ready) $fatal(1,"partial table reset");
        reset_load;
        // Reset after complete packet is submitted: old results must disappear.
        send(16'hb000);
        for(word_index=0;word_index<19;word_index=word_index+1) send(packet[word_index*16+:16]);
        repeat(4) @(negedge clk);
        rstn=0; #1; if(tx_valid || rx_ready) $fatal(1,"running reset");
        reset_load; repeat(60) @(negedge clk);
        if(tx_valid || dut.reg_input_count!=0 || dut.reg_output_count!=0) $fatal(1,"ghost output");
        $display("SHELL_PASS batches=%0d outputs=%0d total_cycles=%0d partial_packet=1 partial_table=1 running_reset=1",`BATCH_COUNT,outputs,cycles);
        $finish;
    end
endmodule
