`timescale 1ns / 1ps
module tb_ball_multi;
    reg clk=0,rstn=0,clear=0,clear_counts=0,fault=0,start=0,valid=0,done=0,overflow=0;
    always #5 clk=!clk;
    reg [1:0] color=0;
    reg [11:0] left=0,right=0,top=0,bottom=0;
    wire output_done,busy;
    wire [31:0] red,green,yellow;
    wire [33:0] total;
    wire [2:0] reason,state,live;
    wire [3:0] boxes;
    wire [7:0] colors;
    wire [47:0] bl,br,bt,bb;
    wire [11:0] cx,cy;
    reg [47:0] clean_l,clean_r,clean_t,clean_b;
    reg [7:0] clean_color;
    integer slot;
    always @(*)begin
        clean_l=0;clean_r=0;clean_t=0;clean_b=0;clean_color=0;
        for(slot=0;slot<4;slot=slot+1)begin
            if(boxes[slot])begin
                clean_l[slot*12 +:12]=bl[slot*12 +:12];clean_r[slot*12 +:12]=br[slot*12 +:12];
                clean_t[slot*12 +:12]=bt[slot*12 +:12];clean_b[slot*12 +:12]=bb[slot*12 +:12];
                clean_color[slot*2 +:2]=colors[slot*2 +:2];
            end
        end
    end
    ball_multi_counter dut(.i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_clear_counts(clear_counts),.i_fault(fault),
        .i_frame_start(start),.i_candidate_valid(valid),.i_color(color),.i_x_min(left),.i_x_max(right),.i_y_min(top),.i_y_max(bottom),
        .i_frame_done(done),.i_overflow(overflow),.o_done(output_done),.o_busy(busy),.o_red(red),.o_green(green),.o_yellow(yellow),
        .o_total(total),.o_reason(reason),.o_state(state),.o_active_count(live),.o_center_x(cx),.o_center_y(cy),
        .o_box_valid(boxes),.o_box_color(colors),.o_box_left(bl),.o_box_right(br),.o_box_top(bt),.o_box_bottom(bb));
    reg [332:0] expected[0:110];
    reg [332:0] actual;
    integer fd,rc,n,inj,ov,cl,k,frame=0,cycles,max_cycles=0;
    task four_red;
        input integer center;
        integer index,wait_clocks;
        begin
            start=1;@(negedge clk);start=0;
            for(index=0;index<4;index=index+1)begin
                color=1;left=center-20;right=center+19;top=180+100*index;bottom=219+100*index;
                valid=1;@(negedge clk);valid=0;@(negedge clk);
            end
            done=1;@(negedge clk);done=0;wait_clocks=0;
            while(!output_done)begin @(negedge clk);wait_clocks=wait_clocks+1;if(wait_clocks>500)$fatal(1,"saturation timeout");end
            @(negedge clk);
        end
    endtask
    initial begin
        $readmemh("sim/multi_expected.hex",expected);
        fd=$fopen("sim/multi_inputs.txt","r");if(!fd)$fatal(1,"missing vectors");
        repeat(4)@(negedge clk);rstn=1;
        while(!$feof(fd))begin
            rc=$fscanf(fd,"%d %d %d %d\n",n,inj,ov,cl);if(rc!=4)$fatal(1,"header");
            if(cl!=0)begin
                clear=1;clear_counts=cl==2;@(negedge clk);clear=0;clear_counts=0;
            end else begin
                start=1;@(negedge clk);start=0;
                for(k=0;k<n;k=k+1)begin
                    rc=$fscanf(fd,"%d %d %d %d %d\n",color,left,right,top,bottom);
                    if(rc!=5)$fatal(1,"candidate");valid=1;@(negedge clk);valid=0;@(negedge clk);
                end
                overflow=ov;done=1;@(negedge clk);done=0;overflow=0;cycles=0;
                if(inj==2 || inj==3)begin
                    while(!((inj==2 && dut.state_current==3) || (inj==3 && dut.state_current==8 && dut.cnt_slot==3)))begin
                        @(negedge clk);cycles=cycles+1;if(cycles>500)$fatal(1,"injection timeout");
                    end
                    fault=1;@(negedge clk);fault=0;
                end
                while(!output_done)begin @(negedge clk);cycles=cycles+1;if(cycles>500)$fatal(1,"done timeout frame %d",frame);end
                if(cycles>max_cycles)max_cycles=cycles;
            end
            #1;
            actual={red,green,yellow,reason,state,live,boxes,clean_color,clean_l,clean_r,clean_t,clean_b,cx,cy};
            if(actual!==expected[frame])$fatal(1,"frame %0d actual=%h expected=%h",frame,actual,expected[frame]);
            if(total!==({2'd0,red}+{2'd0,green}+{2'd0,yellow}))$fatal(1,"total mismatch");
            frame=frame+1;@(negedge clk);
        end
        clear=1;clear_counts=1;@(negedge clk);clear=0;clear_counts=0;
        // 仅测试计数器数值边界的显式故障注入，不替代真实目标输入。
        dut.reg_red_o=32'hfffffffe;
        four_red(560);four_red(580);four_red(660);
        if(red!==32'hffffffff || reason!==6)$fatal(1,"four simultaneous counts did not saturate safely");
        $display("PASS multi: %0d frames, max %0d cycles; same-color simultaneous, order shuffle, dropout/reverse dedup, capacity, fault atomicity",frame,max_cycles);
        $finish;
    end
endmodule
