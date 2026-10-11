`timescale 1ns / 1ps

// Narrow-port protocol check; every result is exported, never checksum-only.
module tb_runtime_layer_shell();
    reg clk=0; always #5 clk=~clk;
    reg rstn=0,rx_valid=0,tx_ready=0;
    reg [15:0]rx_data=0;
    wire rx_ready,tx_valid;
    wire [15:0]tx_data;
    reg [15:0]table_words[0:1023],status_words[0:30];
    reg [7:0]halo[0:1295],dw_weight[0:143],pw_weight[0:383],expected[0:383];
    reg [31:0]dw_bias[0:15],pw_bias[0:23],multipliers[0:39],controls[0:43];
    reg [4095:0]vector_dir,path;
    reg [15:0]word;
    integer ticks=0,i,j,c,polls,total=0;
    reg held=0;
    reg [15:0]held_data;

    road_dynamic_overlap_low_io_top dut(.i_clk(clk),.i_rstn(rstn),
        .i_rx_valid(rx_valid),.i_rx_data(rx_data),.o_rx_ready(rx_ready),
        .o_tx_valid(tx_valid),.o_tx_data(tx_data),.i_tx_ready(tx_ready));

    always @(posedge clk) begin
        ticks=ticks+1;
        if(ticks>250000) $fatal(1,"Shell timeout");
        if(!rstn) held=0;
        else begin
            if(held && (!tx_valid || tx_data!==held_data)) $fatal(1,"TX changed under stall");
            held=tx_valid && !tx_ready;held_data=tx_data;
        end
    end

    task send;
        input [15:0]value;
        begin
            @(negedge clk);rx_data=value;rx_valid=1;
            @(posedge clk);while(!rx_ready) @(posedge clk);
            @(negedge clk);rx_valid=0;
        end
    endtask

    task receive;
        output [15:0]value;
        begin
            // Leave arbitrary bubbles while checking output ownership above.
            repeat(ticks%5) @(negedge clk);
            @(negedge clk);tx_ready=1;
            @(posedge clk);while(!tx_valid) @(posedge clk);
            value=tx_data;
            @(negedge clk);tx_ready=0;
        end
    endtask

    task load;
        input [2:0]kind;input integer address;input [31:0]value;
        begin
            send(16'h2000);send((kind<<13)|address);
            send(value[15:0]);send(value[31:16]);
        end
    endtask

    task status;
        begin
            send(16'h5000);
            for(i=0;i<31;i=i+1) receive(status_words[i]);
            if(status_words[0][12:11]!=0) $fatal(1,"Shell/runner fault %h",status_words[0]);
        end
    endtask

    initial begin
        if(!$value$plusargs("VECTORS=%s",vector_dir)) $fatal(1,"Missing VECTORS");
        $sformat(path,"%0s/silu.hex",vector_dir);$readmemh(path,table_words);
        $sformat(path,"%0s/dw_weights.hex",vector_dir);$readmemh(path,dw_weight);
        $sformat(path,"%0s/pw_weights.hex",vector_dir);$readmemh(path,pw_weight);
        $sformat(path,"%0s/dw_biases.hex",vector_dir);$readmemh(path,dw_bias);
        $sformat(path,"%0s/pw_biases.hex",vector_dir);$readmemh(path,pw_bias);
        $sformat(path,"%0s/multipliers.hex",vector_dir);$readmemh(path,multipliers);
        $sformat(path,"%0s/controls.hex",vector_dir);$readmemh(path,controls);
        for(c=0;c<3;c=c+1) begin
            if(c==0) begin
                $sformat(path,"%0s/edge_halo.hex",vector_dir);$readmemh(path,halo);
                $sformat(path,"%0s/edge_output.hex",vector_dir);$readmemh(path,expected);
            end else if(c==1) begin
                $sformat(path,"%0s/interior_halo.hex",vector_dir);$readmemh(path,halo);
                $sformat(path,"%0s/interior_output.hex",vector_dir);$readmemh(path,expected);
            end else begin
                $sformat(path,"%0s/bottom_right_halo.hex",vector_dir);$readmemh(path,halo);
                $sformat(path,"%0s/bottom_right_output.hex",vector_dir);$readmemh(path,expected);
            end
            @(negedge clk);rstn=0;rx_valid=0;tx_ready=0;
            repeat(4) @(negedge clk);rstn=1;
            send(16'h1000);for(j=0;j<1024;j=j+1) send(table_words[j]);
            for(j=0;j<1296;j=j+1) load(0,j,{{24{halo[j][7]}},halo[j]});
            for(j=0;j<144;j=j+1) load(2,j,{{24{dw_weight[j][7]}},dw_weight[j]});
            for(j=0;j<16;j=j+1) load(3,j,dw_bias[j]);
            for(j=0;j<384;j=j+1) load(4,j,{{24{pw_weight[j][7]}},pw_weight[j]});
            for(j=0;j<24;j=j+1) load(5,j,pw_bias[j]);
            send(16'h3000);status;
            if(status_words[0][10:9]!=0) $fatal(1,"Incomplete parameters started");
            for(j=0;j<40;j=j+1) load(6,j,multipliers[j]);
            for(j=0;j<44;j=j+1) load(7,j,controls[j]);
            send(16'h6001);send(16'h3000);
            polls=0;status;
            while(!status_words[0][10]) begin
                polls=polls+1;if(polls>100) $fatal(1,"No completion");status;
            end
            if({status_words[4],status_words[3]}!==32'd2607) $fatal(1,"Task-stream cycles differ from same-vector runner");
            send(16'h4000);
            for(j=0;j<384;j=j+1) begin
                receive(word);if(word!==(16'h8000|j)) $fatal(1,"Export index %0d",j);
                receive(word);if(word!==(16'h9000|expected[j])) $fatal(1,"Export value %0d",j);
                total=total+1;
            end
            receive(word);if(word!==16'hc000) $fatal(1,"Export completion %h",word);
        end
        $display("TB_PASS_RUNTIME_LAYER_SHELL tiles=3 exported=%0d guards=3 core_cycles=2607",total);
        $finish;
    end
endmodule
