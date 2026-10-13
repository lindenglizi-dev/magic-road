`timescale 1ns / 1ps
// Controllable word endpoint checks loader backpressure and invalid parameter rejection.
module tb_parameter_prefetch(output reg o_test_done);
    reg clk=0; always #5 clk=~clk;
    reg rstn=0,rom_ready=0,rom_valid=0,load_ready=0,table_ready=0;
    reg [159:0]rom_data=0,words[0:7167];
    wire request_valid,response_ready,load_valid,table_valid,done,fault;
    wire [12:0]rom_address;
    wire [2:0]kind;
    wire [10:0]address;
    wire signed [31:0]data;
    wire [9:0]table_address;
    wire signed [15:0]table_data;
    wire [31:0]cycles;
    reg [7:0]expected_kind[0:1675],expected_table[0:1675];
    reg [15:0]expected_address[0:1675];
    reg [31:0]expected_data[0:1675];
    reg [15:0]random_bits=16'hace1;
    reg stalled=0;
    reg [74:0]held;
    integer tick=0,count=0,mode=0;
    reg [4095:0]vectors;
    road_down2_parameter_prefetch dut(.i_clk(clk),.i_rstn(rstn),.o_rom_valid(request_valid),
        .o_rom_addr(rom_address),.i_rom_ready(rom_ready),.i_rom_valid(rom_valid),.i_rom_data(rom_data),
        .o_rom_ready(response_ready),.o_load_valid(load_valid),.o_load_kind(kind),.o_load_addr(address),
        .o_load_data(data),.i_load_ready(load_ready),.o_table_valid(table_valid),.o_table_addr(table_address),
        .o_table_data(table_data),.i_table_ready(table_ready),.o_done(done),.o_fault(fault),.o_cycles(cycles));
    always @(negedge clk) begin
        random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
        rom_ready=!rom_valid && random_bits[0];
        load_ready=(tick%197>=61) && random_bits[1];
        table_ready=(tick%223>=87) && random_bits[2];
    end
    always @(posedge clk) begin
        tick=tick+1;
        if(!rstn) begin rom_valid<=0; count=0; stalled=0; end
        else begin
            if(rom_valid && response_ready) rom_valid<=0;
            if(request_valid && rom_ready) begin
                rom_valid<=1; rom_data<=words[rom_address];
                if(mode==1 && rom_address==13'd42) rom_data[104+:8]<=8'd63;
                if(mode==2 && rom_address==13'd39) rom_data[96+:8]<=8'h80;
            end
            if(stalled && {load_valid,kind,address,data,table_valid,table_address,table_data} !== held)
                $fatal(1,"Loader changed held payload");
            stalled=(load_valid && !load_ready) || (table_valid && !table_ready);
            held={load_valid,kind,address,data,table_valid,table_address,table_data};
            if(load_valid && load_ready) begin
                if(expected_table[count] || kind!==expected_kind[count][2:0] ||
                   address!==expected_address[count][10:0] || data!==expected_data[count]) $fatal(1,"Load mismatch %0d",count);
                count=count+1;
            end
            if(table_valid && table_ready) begin
                if(!expected_table[count] || table_address!==expected_address[count][9:0] ||
                   table_data!==expected_data[count][15:0]) $fatal(1,"Table mismatch %0d",count);
                count=count+1;
            end
        end
    end
    task reset;
        begin
            @(negedge clk);rstn=0;#1;
            if(load_valid || table_valid || request_valid || response_ready || done) $fatal(1,"Reset not masked");
            repeat(4) @(negedge clk);rstn=1;
        end
    endtask
    initial begin
        o_test_done=0;
        if(!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"Missing vectors");
        $readmemh({vectors,"/rom_words.hex"},words);$readmemh({vectors,"/table.hex"},expected_table);
        $readmemh({vectors,"/kind.hex"},expected_kind);$readmemh({vectors,"/address.hex"},expected_address);
        $readmemh({vectors,"/data.hex"},expected_data);
        reset;while(count<43) @(negedge clk);reset;
        while(!done && !fault) @(negedge clk);
        if(!done || fault || count!=1676) $fatal(1,"Stalled load incomplete");
        $display("PREFETCH_STALL_PASS count=%0d cycles=%0d",count,cycles);
        mode=1;reset;while(!fault && !done) @(negedge clk);
        if(!fault || done || count!=608) $fatal(1,"Shift63 not rejected before publication count=%0d",count);
        mode=2;reset;while(!fault && !done) @(negedge clk);
        if(!fault || done || count!=568) $fatal(1,"Negative multiplier not rejected count=%0d",count);
        mode=0;reset;while(!done && !fault) @(negedge clk);
        if(!done || fault || count!=1676) $fatal(1,"Recovery incomplete");
        o_test_done=1;$display("TB_PASS_PARAMETER_PREFETCH stalled=2 reset_cancel=1 shift63=1 negative_multiplier=1");$finish;
    end
    initial begin #5000000;$fatal(1,"Timeout");end
endmodule
