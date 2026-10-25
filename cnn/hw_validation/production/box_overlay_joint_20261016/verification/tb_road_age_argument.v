`timescale 1ns/1ps
// Tool-input diagnostic: preserve the decimal failure and exact hex replacement.
module tb_road_age_argument;
    reg [63:0] decimal_age=0,hex_age=0;
    initial begin
        if(!$value$plusargs("AGE=%d",decimal_age) || !$value$plusargs("AGE_HEX=%h",hex_age))
            $fatal(1,"MISSING_AGE_ARGUMENTS");
        $display("AGE_ARGUMENT_DIAGNOSTIC decimal_format_hex=%h hex_format_hex=%h",decimal_age,hex_age);
        if(hex_age!==64'hffffffffffffffff) $fatal(1,"HEX_ARGUMENT_NOT_UINT64_MAX");
        $finish;
    end
endmodule
