`timescale 1ns / 1ps
// 同步简单双端口存储；阵列由采集数据覆盖，不对ERAM作全阵列复位。
module ball_component_store #(
    parameter C_DEPTH=1024,
    parameter C_ADDR_BITS=10,
    parameter C_DATA_BITS=7
)(
    input i_clk,
    input i_read_enable,
    input [C_ADDR_BITS-1:0] i_read_address,
    input i_write_enable,
    input [C_ADDR_BITS-1:0] i_write_address,
    input [C_DATA_BITS-1:0] i_write_data,
    output [C_DATA_BITS-1:0] o_read_data
);
    reg [C_DATA_BITS-1:0] mem_cells[0:C_DEPTH-1]; // 帧单元、行统计或队列项。
    reg [C_DATA_BITS-1:0] reg_read_o;
    always @(posedge i_clk)begin
        if(i_write_enable)begin mem_cells[i_write_address]<=i_write_data;end
        if(i_read_enable)begin reg_read_o<=mem_cells[i_read_address];end
    end
    assign o_read_data=reg_read_o;
endmodule
