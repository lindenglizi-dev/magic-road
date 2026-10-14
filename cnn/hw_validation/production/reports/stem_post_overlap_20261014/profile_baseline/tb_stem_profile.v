`timescale 1ns / 1ps

// 与原完整前端TB共同展开，只观察其首tile；原逐阶段黄金值和导出检查仍执行。
module tb_stem_profile(output reg o_test_done);
    integer core=0, prepare=0, send=0, mac_wait=0, advance=0, drain=0;
    integer pre_busy=0, silu_busy=0, post_busy=0, commit=0, overlap=0, ingress_wait=0;
    initial o_test_done=1'b0;
    always @(posedge tb_frontend_shared.clk)begin
        if(tb_frontend_shared.rstn && tb_frontend_shared.dut.s_busy)begin
            core=core+1;
            case(tb_frontend_shared.dut.u_stem.state_current)
                4'd1:prepare=prepare+1;
                4'd2:send=send+1;
                4'd3:mac_wait=mac_wait+1;
                4'd4:drain=drain+1;
                4'd5:advance=advance+1;
                default:$fatal(1,"Unexpected busy state");
            endcase
            if(tb_frontend_shared.dut.pp_pre_busy)pre_busy=pre_busy+1;
            if(tb_frontend_shared.dut.pp_silu_busy)silu_busy=silu_busy+1;
            if(tb_frontend_shared.dut.pp_post_busy)post_busy=post_busy+1;
            if(tb_frontend_shared.dut.s_pp_output_valid && tb_frontend_shared.dut.s_pp_output_ready)commit=commit+1;
            if(tb_frontend_shared.dut.s_pp_valid && !tb_frontend_shared.dut.s_pp_ready)ingress_wait=ingress_wait+1;
            if(tb_frontend_shared.dut.u_stem.state_current!=4'd4 && tb_frontend_shared.dut.pp_pending_count!=0)overlap=overlap+1;
        end
        if(tb_frontend_shared.rstn && tb_frontend_shared.dut.s_export_done)begin
            if(core!=tb_frontend_shared.dut.s_core_cycles || prepare+send+mac_wait+advance+drain!=core || commit!=256)
                $fatal(1,"Profile accounting mismatch");
            o_test_done=1'b1;
            $display("TB_PASS_STEM_PROFILE core=%0d prepare=%0d send=%0d mac_wait=%0d advance=%0d final_drain=%0d pre_busy=%0d silu_busy=%0d post_busy=%0d commits=%0d overlap=%0d ingress_wait=%0d",
                     core,prepare,send,mac_wait,advance,drain,pre_busy,silu_busy,post_busy,commit,overlap,ingress_wait);
            $finish;
        end
    end
    initial begin #1000000;$fatal(1,"Profile timeout");end
endmodule
