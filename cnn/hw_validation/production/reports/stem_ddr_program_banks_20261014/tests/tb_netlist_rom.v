`timescale 1ns / 1ps
// Focused post-synthesis ROM readout; does not simulate DDR or board operation.
module tb_netlist_rom;
    reg clk = 0;
    reg enable = 0;
    reg [12:0] address = 0;
    reg [63:0] expected [0:8191];
    reg [63:0] held_low, held_high;
    reg held_bank;
    integer index;
    always #5 clk = ~clk;
    road_stem_ddr_board_top dut(.i_rstn(1'b0), .i_sys_clk(1'b0));
    initial begin
        $readmemh("program.hex", expected);
        force dut.\u_sequence/u_core/u_down2/i_clk  = clk;
        force dut.\u_sequence/cnt_program  = address;
        force dut.\u_sequence/flag_command_bank_n2  = enable;
        #101;
        for(index = 0; index < 8192; index = index + 1) begin
            @(negedge clk);
            address = index;
            enable = 1;
            @(posedge clk); #1;
            if(dut.\u_sequence/reg_command_low  !== expected[index & 4095])
                $fatal(1, "MAPPED_LOW_MISMATCH address=%0d actual=%h expected=%h", index, dut.\u_sequence/reg_command_low , expected[index & 4095]);
            if(dut.\u_sequence/reg_command_high  !== expected[(index & 4095) + 4096])
                $fatal(1, "MAPPED_HIGH_MISMATCH address=%0d", index);
            if(dut.\u_sequence/flag_command_bank  !== address[12])
                $fatal(1, "MAPPED_BANK_MISMATCH address=%0d", index);
            held_low = dut.\u_sequence/reg_command_low ;
            held_high = dut.\u_sequence/reg_command_high ;
            held_bank = dut.\u_sequence/flag_command_bank ;
            @(negedge clk);
            enable = 0;
            address = address ^ 13'h1000;
            repeat(2) begin
                @(posedge clk); #1;
                if(dut.\u_sequence/reg_command_low  !== held_low || dut.\u_sequence/reg_command_high  !== held_high || dut.\u_sequence/flag_command_bank  !== held_bank)
                    $fatal(1, "MAPPED_HOLD_MISMATCH address=%0d", index);
            end
        end
        $display("MAPPED_ROM_PASS words=8192 hold_checks=16384");
        $finish;
    end
endmodule
