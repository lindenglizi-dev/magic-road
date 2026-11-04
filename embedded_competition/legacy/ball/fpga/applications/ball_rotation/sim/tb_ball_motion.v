`timescale 1ns / 1ps
// 逐时钟对照功能模型，候选可连续到达；done独立提交完整帧。
module tb_ball_motion;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,clear=0,start=0,candidate=0,done=0,overflow=0;
    reg [1:0] color=0;
    reg [19:0] area=0;
    reg [11:0] left=0,right=0,top=0,bottom=0;
    wire valid;
    wire [1:0] status,out_color;
    wire [11:0] out_left,out_right,out_top,out_bottom,center_x,center_y;
`ifdef OLD_TRACKER
    ball_target_tracker dut(
`else
    ball_target_tracker #(.C_X_MIN(64),.C_Y_MIN(160),.C_X_END(1216),.C_Y_END(640)) dut(
`endif
        .i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_frame_start(start),.i_candidate_valid(candidate),
        .i_color(color),.i_area(area),.i_x_min(left),.i_x_max(right),.i_y_min(top),.i_y_max(bottom),
        .i_frame_done(done),.i_overflow(overflow),.o_valid(valid),.o_status(status),.o_color(out_color),
        .o_x_min(out_left),.o_x_max(out_right),.o_y_min(out_top),.o_y_max(out_bottom),
        .o_center_x(center_x),.o_center_y(center_y));
    integer file_handle,rc,cycles=0,frames=0;
    integer c,s,v,d,o,col,a,l,r,t,b,ev,es,ec,el,et,er,eb,ex,ey;
    initial begin
        repeat(3)@(negedge clk);
        rstn=1;
        file_handle=$fopen("sim/motion_vectors.txt","r");
        if(file_handle == 0)$fatal(1,"motion vectors missing");
        while(!$feof(file_handle))begin
            rc=$fscanf(file_handle,"%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",
                c,s,v,d,o,col,a,l,r,t,b,ev,es,ec,el,et,er,eb,ex,ey);
            if(rc != 20)$fatal(1,"motion vector field count %0d",rc);
            @(negedge clk);
            clear=c;start=s;candidate=v;done=d;overflow=o;color=col;area=a;left=l;right=r;top=t;bottom=b;
            @(posedge clk);#1;
            cycles=cycles+1;
            if(d)frames=frames+1;
            if(valid !== ev[0] || status !== es[1:0])
                $fatal(1,"motion state cycle=%0d got=%0d/%0d expected=%0d/%0d",cycles,valid,status,ev,es);
            if(valid && (out_color !== ec[1:0] || out_left !== el[11:0] || out_top !== et[11:0] ||
                out_right !== er[11:0] || out_bottom !== eb[11:0] || center_x !== ex[11:0] || center_y !== ey[11:0]))
                $fatal(1,"motion geometry cycle=%0d frame=%0d got=%0d,%0d..%0d,%0d center=%0d,%0d expected=%0d,%0d..%0d,%0d center=%0d,%0d",
                    cycles,frames,out_left,out_top,out_right,out_bottom,center_x,center_y,el,et,er,eb,ex,ey);
        end
        $fclose(file_handle);
        $display("PASS motion tracker: %0d frames, %0d cycle snapshots",frames,cycles);
        $finish;
    end
endmodule
