`timescale 1ns / 1ps
// Frozen Haar model / 固定25级2913弱分类器；文件内容由定点模型导出。
module face_model_rom #(
    parameter C_STUMPS="../rtl/face_rom/stumps.mem",
    parameter C_STAGES="../rtl/face_rom/stages.mem"
)(
    input i_clk,
    input i_read,
    input [11:0] i_weak_address,
    input [4:0] i_stage_address,
    output [119:0] o_weak,
    output [39:0] o_stage
);
    reg [119:0] mem_stumps[0:2912];
    reg [39:0] mem_stages[0:24];
    reg [119:0] reg_weak_o;
    reg [39:0] reg_stage_o;
    initial begin $readmemh(C_STUMPS,mem_stumps);$readmemh(C_STAGES,mem_stages);end
    always @(posedge i_clk)begin
        if(i_read)begin
            reg_weak_o<=mem_stumps[i_weak_address];reg_stage_o<=mem_stages[i_stage_address];
        end
    end
    assign o_weak=reg_weak_o;
    assign o_stage=reg_stage_o;
endmodule
