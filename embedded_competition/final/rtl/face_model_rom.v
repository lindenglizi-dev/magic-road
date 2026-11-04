`timescale 1ns / 1ps
// Frozen Haar model / 七种矩形模板无损展开，系数与同步读取周期保持。
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
    localparam C_PACKED_STUMPS={C_STUMPS,".packed"};
    reg [74:0] mem_stumps[0:2912];
    reg [39:0] mem_stages[0:24];
    reg [74:0] reg_packed_weak_o;
    reg [39:0] reg_stage_o;
    wire [4:0] wire_x=reg_packed_weak_o[4:0];
    wire [4:0] wire_y=reg_packed_weak_o[9:5];
    wire [4:0] wire_width=reg_packed_weak_o[14:10];
    wire [4:0] wire_height=reg_packed_weak_o[19:15];
    wire [4:0] wire_half_width={1'b0,wire_width[4:1]};
    wire [4:0] wire_half_height={1'b0,wire_height[4:1]};
    wire [4:0] wire_right_half=wire_x+wire_half_width;
    wire [4:0] wire_bottom_half=wire_y+wire_half_height;
    reg [4:0] dec_third_width,dec_third_height;
    reg [19:0] dec_second,dec_third;
    reg [1:0] dec_mode;
    reg [5:0] dec_reserved;
                                                                               
    always @(*)begin
        case(wire_width)
            3:dec_third_width=1;6:dec_third_width=2;9:dec_third_width=3;12:dec_third_width=4;
            15:dec_third_width=5;18:dec_third_width=6;21:dec_third_width=7;24:dec_third_width=8;
            default:dec_third_width=0;
        endcase
        case(wire_height)
            3:dec_third_height=1;6:dec_third_height=2;9:dec_third_height=3;12:dec_third_height=4;
            15:dec_third_height=5;18:dec_third_height=6;21:dec_third_height=7;24:dec_third_height=8;
            default:dec_third_height=0;
        endcase
    end
    wire [4:0] wire_right_third=wire_x+dec_third_width;
    wire [4:0] wire_bottom_third=wire_y+dec_third_height;
                                                                               
    always @(*)begin
        dec_second=0;dec_third=0;dec_mode=0;dec_reserved=0;
        case(reg_packed_weak_o[22:20])
            0:begin dec_mode=1;dec_second={dec_third_height,wire_width,wire_bottom_third,wire_x};end
            1:begin dec_mode=1;dec_second={wire_height,dec_third_width,wire_y,wire_right_third};end
            2:dec_second={wire_half_height,wire_width,wire_bottom_half,wire_x};
            3:begin
                dec_mode=2;dec_second={wire_half_height,wire_half_width,wire_y,wire_x};
                dec_third={wire_half_height,wire_half_width,wire_bottom_half,wire_right_half};
            end
            4:begin
                dec_mode=2;dec_second={wire_half_height,wire_half_width,wire_y,wire_right_half};
                dec_third={wire_half_height,wire_half_width,wire_bottom_half,wire_x};
            end
            5:dec_second={wire_height,wire_half_width,wire_y,wire_right_half};
            6:dec_second={wire_height,wire_half_width,wire_y,wire_x};
            default:begin dec_mode=3;dec_reserved=6'h3f;end
        endcase
    end
    initial begin $readmemh(C_PACKED_STUMPS,mem_stumps);$readmemh(C_STAGES,mem_stages);end
    always @(posedge i_clk)begin
        if(i_read)begin
            reg_packed_weak_o<=mem_stumps[i_weak_address];reg_stage_o<=mem_stages[i_stage_address];
        end
    end
    assign o_weak={dec_reserved,reg_packed_weak_o[74:23],dec_mode,dec_third,dec_second,reg_packed_weak_o[19:0]};
    assign o_stage=reg_stage_o;
endmodule
