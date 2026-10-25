`timescale 1ns / 1ps
// 固定首残差模型常量ROM；显式常量case避免TD忽略数组readmemh初始化。
module road_csp_tile_program(
    input i_clk, // 同域计算时钟
    input i_rstn, // 取消尚未使用的参数响应
    input i_enable, // 描述符IDLE捕获时读取一组参数
    input [5:0]i_weight_index, // 56个稀疏DW/PW权重词
    input [3:0]i_parameter_index, // 16个通道参数词
    output [191:0]o_weight, // 注册权重响应
    output [247:0]o_parameter // 注册参数响应
);
    reg [191:0]reg_weight_o; // 本组固定权重
    reg [247:0]reg_parameter_o; // 本组固定参数
    assign o_weight = reg_weight_o; // 单信号注册输出桥
    assign o_parameter = reg_parameter_o; // 参数随同一次读取保持
    // 真实模型权重按通道复用，未命中不产生未驱动值。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)reg_weight_o <= 192'd0;
        else if(i_enable)begin
            case(i_weight_index)
                6'd0:begin
                    reg_weight_o <= 192'hfb00001a45dc00007ffb00001a45dc00497ffb00001a45dc; // 固定模型的稀疏权重词
                end
                6'd1:begin
                    reg_weight_o <= 192'h00495c1f0000497f0000495c1f000049000000495c1f0000; // 固定模型的稀疏权重词
                end
                6'd2:begin
                    reg_weight_o <= 192'h000000000000000000000000000000005c1f497ffb1a45dc; // 固定模型的稀疏权重词
                end
                6'd3:begin
                    reg_weight_o <= 192'h000000000000000000000000000000000000000000000049; // 固定模型的稀疏权重词
                end
                6'd4:begin
                    reg_weight_o <= 192'hd8000015fd01000081d8000015fd01000781d8000015fd01; // 固定模型的稀疏权重词
                end
                6'd5:begin
                    reg_weight_o <= 192'h000a26140000078100000a26140000070000000a26140000; // 固定模型的稀疏权重词
                end
                6'd6:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000026140781d815fd01; // 固定模型的稀疏权重词
                end
                6'd7:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000000000000000000a; // 固定模型的稀疏权重词
                end
                6'd8:begin
                    reg_weight_o <= 192'h850000f8060a000081850000f8060a000781850000f8060a; // 固定模型的稀疏权重词
                end
                6'd9:begin
                    reg_weight_o <= 192'h000901ea0000078100000901ea0000070000000901ea0000; // 固定模型的稀疏权重词
                end
                6'd10:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000001ea078185f8060a; // 固定模型的稀疏权重词
                end
                6'd11:begin
                    reg_weight_o <= 192'h000000000000000000000000000000000000000000000009; // 固定模型的稀疏权重词
                end
                6'd12:begin
                    reg_weight_o <= 192'h050000ff000c00007f050000ff000c00167f050000ff000c; // 固定模型的稀疏权重词
                end
                6'd13:begin
                    reg_weight_o <= 192'h00e1b7730000167f0000e1b773000016000000e1b7730000; // 固定模型的稀疏权重词
                end
                6'd14:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000b773167f05ff000c; // 固定模型的稀疏权重词
                end
                6'd15:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000000000000000000e1; // 固定模型的稀疏权重词
                end
                6'd16:begin
                    reg_weight_o <= 192'h12000002e9fa00007f12000002e9fa000b7f12000002e9fa; // 固定模型的稀疏权重词
                end
                6'd17:begin
                    reg_weight_o <= 192'h00f105f900000b7f0000f105f900000b000000f105f90000; // 固定模型的稀疏权重词
                end
                6'd18:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000005f90b7f1202e9fa; // 固定模型的稀疏权重词
                end
                6'd19:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000000000000000000f1; // 固定模型的稀疏权重词
                end
                6'd20:begin
                    reg_weight_o <= 192'hc80000f3fa1400007fc80000f3fa1400f47fc80000f3fa14; // 固定模型的稀疏权重词
                end
                6'd21:begin
                    reg_weight_o <= 192'h000bfff30000f47f00000bfff30000f40000000bfff30000; // 固定模型的稀疏权重词
                end
                6'd22:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000fff3f47fc8f3fa14; // 固定模型的稀疏权重词
                end
                6'd23:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000000000000000000b; // 固定模型的稀疏权重词
                end
                6'd24:begin
                    reg_weight_o <= 192'h810000f225f7000059810000f225f700f459810000f225f7; // 固定模型的稀疏权重词
                end
                6'd25:begin
                    reg_weight_o <= 192'h0004ff1f0000f459000004ff1f0000f400000004ff1f0000; // 固定模型的稀疏权重词
                end
                6'd26:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000ff1ff45981f225f7; // 固定模型的稀疏权重词
                end
                6'd27:begin
                    reg_weight_o <= 192'h000000000000000000000000000000000000000000000004; // 固定模型的稀疏权重词
                end
                6'd28:begin
                    reg_weight_o <= 192'hd80000e7082a00007fd80000e7082a001b7fd80000e7082a; // 固定模型的稀疏权重词
                end
                6'd29:begin
                    reg_weight_o <= 192'h0034ece100001b7f000034ece100001b00000034ece10000; // 固定模型的稀疏权重词
                end
                6'd30:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000ece11b7fd8e7082a; // 固定模型的稀疏权重词
                end
                6'd31:begin
                    reg_weight_o <= 192'h000000000000000000000000000000000000000000000034; // 固定模型的稀疏权重词
                end
                6'd32:begin
                    reg_weight_o <= 192'hfb00001ef007000081fb00001ef007002181fb00001ef007; // 固定模型的稀疏权重词
                end
                6'd33:begin
                    reg_weight_o <= 192'h002006f80000218100002006f80000210000002006f80000; // 固定模型的稀疏权重词
                end
                6'd34:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000006f82181fb1ef007; // 固定模型的稀疏权重词
                end
                6'd35:begin
                    reg_weight_o <= 192'h000000000000000000000000000000000000000000000020; // 固定模型的稀疏权重词
                end
                6'd36:begin
                    reg_weight_o <= 192'h6f0000d9373700007f6f0000d9373700f77f6f0000d93737; // 固定模型的稀疏权重词
                end
                6'd37:begin
                    reg_weight_o <= 192'h004d2ad90000f77f00004d2ad90000f70000004d2ad90000; // 固定模型的稀疏权重词
                end
                6'd38:begin
                    reg_weight_o <= 192'h000000000000000000000000000000002ad9f77f6fd93737; // 固定模型的稀疏权重词
                end
                6'd39:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000000000000000004d; // 固定模型的稀疏权重词
                end
                6'd40:begin
                    reg_weight_o <= 192'hd200000d1de50000ddd200000d1de500f1ddd200000d1de5; // 固定模型的稀疏权重词
                end
                6'd41:begin
                    reg_weight_o <= 192'h007f50dc0000f1dd00007f50dc0000f10000007f50dc0000; // 固定模型的稀疏权重词
                end
                6'd42:begin
                    reg_weight_o <= 192'h0000000000000000000000000000000050dcf1ddd20d1de5; // 固定模型的稀疏权重词
                end
                6'd43:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000000000000000007f; // 固定模型的稀疏权重词
                end
                6'd44:begin
                    reg_weight_o <= 192'h080000021505000081080000021505001481080000021505; // 固定模型的稀疏权重词
                end
                6'd45:begin
                    reg_weight_o <= 192'h000afaf60000148100000afaf60000140000000afaf60000; // 固定模型的稀疏权重词
                end
                6'd46:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000faf6148108021505; // 固定模型的稀疏权重词
                end
                6'd47:begin
                    reg_weight_o <= 192'h00000000000000000000000000000000000000000000000a; // 固定模型的稀疏权重词
                end
                6'd48:begin
                    reg_weight_o <= 192'hf6691cc3d6f8be11814d28ee08e9f0ee3908ac08d0d20331; // 固定模型的稀疏权重词
                end
                6'd49:begin
                    reg_weight_o <= 192'h000000007f2bd11b00000000f2ff0eeb00000000ff18ea7f; // 固定模型的稀疏权重词
                end
                6'd50:begin
                    reg_weight_o <= 192'hb7ff1b81f966c4c120a82a815c5bb52619d91cf2c9378ece; // 固定模型的稀疏权重词
                end
                6'd51:begin
                    reg_weight_o <= 192'h00000000ef23039400000000ea62c42e00000000ff067ff8; // 固定模型的稀疏权重词
                end
                6'd52:begin
                    reg_weight_o <= 192'h339f6627dade117fd8f7cd27ef317fba9ef0c2149dcb2aa0; // 固定模型的稀疏权重词
                end
                6'd53:begin
                    reg_weight_o <= 192'h00000000d82ab76700000000ee4209d800000000de415d81; // 固定模型的稀疏权重词
                end
                6'd54:begin
                    reg_weight_o <= 192'h5b0be489d337b67f0dfcee880b81e413b7090f89811de71f; // 固定模型的稀疏权重词
                end
                6'd55:begin
                    reg_weight_o <= 192'h00000000f698f4c50000000000a2cf4200000000f9562014; // 固定模型的稀疏权重词
                end
                default:begin
                    reg_weight_o <= 192'd0; // 非法ROM地址不沿用旧权重
                end
            endcase
        end
    end
    // 偏置与双重定标原样来自同一冻结数值包。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)reg_parameter_o <= 248'd0;
        else if(i_enable)begin
            case(i_parameter_index)
                4'd0:begin
                    reg_parameter_o <= 248'h8d99115f1e186148d80f6548d80f6548d80f65fffffd41fffffd41fffffd41; // 逻辑输出通道的量化参数词
                end
                4'd1:begin
                    reg_parameter_o <= 248'h8d99115f1df7df7849b84a7849b84a7849b84a000000d3000000d3000000d3; // 逻辑输出通道的量化参数词
                end
                4'd2:begin
                    reg_parameter_o <= 248'h8d99115f1de79e5153921b5153921b5153921b000001280000012800000128; // 逻辑输出通道的量化参数词
                end
                4'd3:begin
                    reg_parameter_o <= 248'h8d99115f1df7df480a9c21480a9c21480a9c21ffffff83ffffff83ffffff83; // 逻辑输出通道的量化参数词
                end
                4'd4:begin
                    reg_parameter_o <= 248'h8d99115f1dd75d5115dc685115dc685115dc68ffffffcdffffffcdffffffcd; // 逻辑输出通道的量化参数词
                end
                4'd5:begin
                    reg_parameter_o <= 248'h8d99115f1df7df7dc42cd17dc42cd17dc42cd1ffffffc8ffffffc8ffffffc8; // 逻辑输出通道的量化参数词
                end
                4'd6:begin
                    reg_parameter_o <= 248'h8d99115f1e08204540947a4540947a4540947a000001fa000001fa000001fa; // 逻辑输出通道的量化参数词
                end
                4'd7:begin
                    reg_parameter_o <= 248'h8d99115f1e18617bd2694c7bd2694c7bd2694c0000011b0000011b0000011b; // 逻辑输出通道的量化参数词
                end
                4'd8:begin
                    reg_parameter_o <= 248'h8d99115f1e082067855e8b67855e8b67855e8b000000eb000000eb000000eb; // 逻辑输出通道的量化参数词
                end
                4'd9:begin
                    reg_parameter_o <= 248'h8d99115f1de79e427c722e427c722e427c722efffffe29fffffe29fffffe29; // 逻辑输出通道的量化参数词
                end
                4'd10:begin
                    reg_parameter_o <= 248'h8d99115f1e082053ad418453ad418453ad4184000000090000000900000009; // 逻辑输出通道的量化参数词
                end
                4'd11:begin
                    reg_parameter_o <= 248'h8d99115f1de79e618ced04618ced04618ced04ffffffd1ffffffd1ffffffd1; // 逻辑输出通道的量化参数词
                end
                4'd12:begin
                    reg_parameter_o <= 248'h91b5dfbdba28215a9d78646e05ae864665938bfffffd8a0000013800000236; // 逻辑输出通道的量化参数词
                end
                4'd13:begin
                    reg_parameter_o <= 248'h91b5dfbdba18a342d7441750986407790ea4c900000440000000c300000492; // 逻辑输出通道的量化参数词
                end
                4'd14:begin
                    reg_parameter_o <= 248'h91b5dfbdba5862505adfb272666d3a6321a5cffffff28ffffffe22fffffdf9; // 逻辑输出通道的量化参数词
                end
                4'd15:begin
                    reg_parameter_o <= 248'h91b5dfbdba28e1728fe53949b0582f6b1a870a000009af000007a7000001eb; // 逻辑输出通道的量化参数词
                end
                default:begin
                    reg_parameter_o <= 248'd0; // 不发布未定义参数
                end
            endcase
        end
    end
endmodule
