`timescale 1ns / 1ps
// 安路同步简单双端口RAM推断模板：不复位存储阵列。
module ball_column_store #(
    parameter C_DEPTH = 320,
    parameter C_ADDR_BITS = 9
)(
    input i_clk,
    input i_read_enable,
    input [C_ADDR_BITS-1:0] i_read_address,
    input i_write_enable,
    input [C_ADDR_BITS-1:0] i_write_address,
    input [49:0] i_write_data,
    output [49:0] o_read_data
);
    reg [49:0] mem_columns [0:C_DEPTH-1]; // 三色各10位、纵坐标极值各10位。
    reg [49:0] reg_read_o;
    // 读写使能独立；RAM内容由采集帧第一行覆盖初始化。
    always @(posedge i_clk)begin
        if(i_write_enable)begin mem_columns[i_write_address] <= i_write_data; end
        if(i_read_enable)begin reg_read_o <= mem_columns[i_read_address]; end
    end
    assign o_read_data = reg_read_o;
endmodule
