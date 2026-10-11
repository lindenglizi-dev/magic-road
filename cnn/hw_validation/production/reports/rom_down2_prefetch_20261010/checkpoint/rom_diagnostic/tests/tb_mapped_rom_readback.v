`timescale 1ns/1ps
module tb_mapped_rom_readback (output reg o_test_done);
    reg i_clk = 1'b0;
    reg [8:0] cnt_word_addr = 9'd0;
    wire i_clk_dup_1 = i_clk;
    wire [2239:0] observed;
    reg [159:0] expected [0:7167];
    integer address;
    integer lane;
    integer word_index;
    integer dump_file;
    always #5 i_clk = ~i_clk;
    // Test-only extraction: parameters and physical data wiring come from TD.
    `include "native_instances.vh"
    initial begin
        o_test_done = 1'b0;
        $readmemh("artifacts/words.dath", expected);
        dump_file = $fopen("native_readback.txt", "w");
        if (dump_file == 0) begin
            $fatal(1, "cannot open native readback file");
        end
        #200;
        for (address = 0; address < 512; address = address + 1) begin
            @(negedge i_clk);
            cnt_word_addr = address;
            @(posedge i_clk);
            #1;
            for (lane = 0; lane < 56; lane = lane + 1) begin
                word_index = (lane / 4) * 512 + address;
                if (observed[lane*40 +: 40] !== expected[word_index][(lane%4)*40 +: 40]) begin
                    $fatal(1, "native mismatch lane=%0d address=%0d actual=%010h expected=%010h",
                        lane, address, observed[lane*40 +: 40], expected[word_index][(lane%4)*40 +: 40]);
                end
                $fdisplay(dump_file, "%0d %0d %010h", lane, address, observed[lane*40 +: 40]);
            end
        end
        $fclose(dump_file);
        o_test_done = 1'b1;
        $display("NATIVE_ROM_PASS: 56 ERAMs x 512 addresses = 143360 bytes");
        $finish;
    end
endmodule
