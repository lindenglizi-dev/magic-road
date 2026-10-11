module minimal_multi_target_fail (
    input wire clk,
    input wire rst_n,
    input wire load,
    input wire data_a,
    input wire data_b,
    output reg value_a,
    output reg value_b
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            value_a <= 1'b0; value_b <= 1'b0;
        end else if (load) begin
            value_a <= data_a; value_b <= data_b;
        end
    end
endmodule
