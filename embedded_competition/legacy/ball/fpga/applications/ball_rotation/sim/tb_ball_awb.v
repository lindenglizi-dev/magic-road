`timescale 1ns / 1ps
// 直接使用原厂ERAM仿真模型，检查原延迟链与新的增益乘法。
module tb_ball_awb;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,early=0;
    reg [95:0] rgb=0;
    wire [95:0] out_rgb;
    wire out_valid,out_last,out_early,ready;
    awb #(.IMG_WIDTH(256),.IMG_HEIGHT(4)) dut(.I_clk(clk),.I_rst_n(rstn),.I_tlast(1'b0),.I_tuser(early),
        .I_tdata(rgb),.I_tvalid(valid),.I_tready(),.O_tlast(out_last),.O_tuser(out_early),
        .O_tdata(out_rgb),.O_tvalid(out_valid),.O_tready(1'b1),.O_wb_ready(ready));
    reg [95:0] queue[0:4095];
    reg [95:0] expected;
    integer written=0,received=0,lines=0,lane,product_red,product_blue;
    always @(posedge clk)begin
        if(rstn && valid)begin
            expected=0;
            for(lane=0;lane<4;lane=lane+1)begin
                product_red=rgb[lane*24+16 +:8]*dut.in_r_r1;
                product_blue=rgb[lane*24 +:8]*dut.in_b_r1;
                expected[lane*24+16 +:8]=product_red >= 16777216 ? 255 : product_red >> 16;
                expected[lane*24+8 +:8]=rgb[lane*24+8 +:8];
                expected[lane*24 +:8]=product_blue >= 16777216 ? 255 : product_blue >> 16;
            end
            queue[written]=expected;written=written+1;
        end
        #1;
        if(rstn)begin
            if(out_early!==early)$fatal(1,"AWB early lead changed");
            if(out_valid)begin
                if(received>=written || out_rgb!==queue[received])$fatal(1,"AWB bytes/order mismatch group%0d expected%h got%h",received,queue[received],out_rgb);
                received=received+1;if(out_last)lines=lines+1;
            end else if(out_rgb!==0)$fatal(1,"AWB invalid data not zero");
        end
    end
    integer frame,row,group_index,channel;
    initial begin
        repeat(5)@(negedge clk);rstn=1;
        for(frame=0;frame<6;frame=frame+1)begin
            early=1;@(negedge clk);early=0;repeat(12)@(negedge clk);
            for(row=0;row<4;row=row+1)begin
                for(group_index=0;group_index<64;group_index=group_index+1)begin
                    for(channel=0;channel<4;channel=channel+1)begin
                        if(frame<2)begin rgb[channel*24 +:24]={8'd180+channel[7:0],8'd20,8'd10};end
                        else begin rgb[channel*24 +:24]=24'h506478;end
                    end
                    valid=1;@(negedge clk);
                end
                valid=0;repeat(85)@(negedge clk);
            end
            repeat(150)@(negedge clk);
            if(received!=written || lines!=(frame+1)*4)$fatal(1,"AWB lost pixels/line tail");
        end
        if(!ready || dut.in_r_r1==65536 || dut.in_b_r1==65536)$fatal(1,"AWB never applied neutral frame estimate");
        $display("PASS AWB: real Anlogic ERAM, six complete frames, %0d four-pixel groups, 24 line tails, exact gains/byte ordering and unchanged early",received);$finish;
    end
    initial begin #10000000;$fatal(1,"AWB timeout");end
endmodule
