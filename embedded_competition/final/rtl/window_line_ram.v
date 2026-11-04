`timescale 1ns / 1ps

// 单时钟、同步读、同地址先读后写的行存储器。
// 不复位/循环清零存储阵列，保留推断为片内块RAM的条件。
// ram_style只是综合提示；是否映射为安路ERAM须由TD报告确认。
module window_line_ram #(
    parameter integer DEPTH = 256,
    parameter integer ADDR_WIDTH = 8
)(
    input wire I_clk,
    input wire I_en,
    input wire [ADDR_WIDTH-1:0] I_addr,
    input wire [31:0] I_data,
    output reg [31:0] O_data
);
    (* ram_style = "block" *) reg [31:0] S_mem [0:DEPTH-1];
    always @(posedge I_clk) begin
        if(I_en) begin
            O_data <= S_mem[I_addr]; // 输出覆盖前的旧行，读延迟一级。
            S_mem[I_addr] <= I_data; // 同地址写入新行，非阻塞赋值保留旧值读取。
        end
    end
endmodule
