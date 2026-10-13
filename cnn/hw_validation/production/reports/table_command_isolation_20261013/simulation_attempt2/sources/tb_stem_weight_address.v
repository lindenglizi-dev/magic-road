`timescale 1ns / 1ps

// 白盒穷举组合地址；完整握手/复位由未修改的前端回归覆盖。
module tb_stem_weight_address;
    reg clk=1'b0;
    reg rstn=1'b0;
    integer pattern, address, position, channel, group, lane, output_lane, term, expected, checked;
    road_frontend_shared_core dut(
        .i_clk(clk),.i_rstn(rstn),.i_select_valid(1'b0),.i_select_down2(1'b0),
        .i_table_valid(1'b0),.i_table_addr(10'd0),.i_table_data(16'sd0),
        .i_load_valid(1'b0),.i_load_kind(3'd0),.i_load_addr(11'd0),.i_load_data(32'sd0),
        .i_start(1'b0),.i_commit_ready(1'b0),.i_export_start(1'b0),.i_output_ready(1'b0)
    );
    initial begin
        checked=0;
        #1; rstn=1'b1;
        // 低字节和高字节指纹组合能区分全部432地址，不受8位别名影响。
        for(pattern=0;pattern<2;pattern=pattern+1)begin
            for(address=0;address<432;address=address+1)
                dut.u_stem.reg_weight[address]=pattern==0 ? address[7:0] : address>>8;
            for(position=0;position<16;position=position+1)begin
                for(channel=0;channel<16;channel=channel+3)begin
                    for(group=0;group<4;group=group+1)begin
                        dut.u_stem.cnt_position=position[3:0];
                        dut.u_stem.cnt_channel=channel[3:0];
                        dut.u_stem.cnt_group=group[1:0];
                        #1;
                        for(lane=0;lane<8;lane=lane+1)begin
                            term=group*8+lane;
                            for(output_lane=0;output_lane<3;output_lane=output_lane+1)begin
                                expected=0;
                                if(term<27 && channel+output_lane<16)begin
                                    address=(channel+output_lane)*27+term;
                                    expected=pattern==0 ? (address & 255) : address>>8;
                                end
                                if(dut.u_stem.next_weight[(output_lane*8+lane)*8+:8] !== expected[7:0])begin
                                    $display("TB_FAIL_ADDRESS pattern=%0d c=%0d g=%0d lane=%0d out=%0d",pattern,channel,group,lane,output_lane);
                                    $fatal(1);
                                end
                                checked=checked+1;
                            end
                        end
                    end
                end
            end
        end
        if(checked!=18432) $fatal(1,"address count mismatch");
        $display("TB_PASS_STEM_WEIGHT_ADDRESS checks=%0d",checked);
        $finish;
    end
endmodule
