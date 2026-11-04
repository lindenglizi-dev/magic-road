`timescale 1ns / 1ps
module tb_ball_components_budget;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,sof=0,eof=0;
    reg [11:0] x=0,y=0;reg [7:0] labels=0;reg [15:0] epoch=0;
    reg [2:0] hits=0;
    wire start,candidate,done,overflow,fault,error;
    wire [15:0] out_epoch;
    wire [3:0] number,rejection;
    wire [11:0] width,height;
    wire [19:0] area,gate_pixels;
    wire [6:0] fill;
    integer cycle=0,start_cycle=0,finished=0,max_queue=0,job,frame,row,group_index,frame_start;
    ball_components dut(.i_clk(clk),.i_rstn(rstn),.i_session_clear(1'b0),.i_valid(valid),.i_sof(sof),.i_eof(eof),
        .i_x(x),.i_y(y),.i_labels(labels),.i_gate_hits(hits),.i_epoch(epoch),
        .o_frame_start(start),.o_candidate_valid(candidate),.o_color(),.o_area(),.o_x_min(),.o_x_max(),.o_y_min(),.o_y_max(),
        .o_frame_done(done),.o_gate_pixels(gate_pixels),.o_epoch(out_epoch),.o_overflow(overflow),.o_fault(fault),.o_error(error),
        .o_diag_count(number),.o_diag_width(width),.o_diag_height(height),.o_diag_area(area),.o_diag_fill(fill),.o_diag_reject(rejection));
    always @(posedge clk)begin
        cycle=cycle+1;#1;
        if(rstn)begin
            if(error || fault || overflow || candidate)$fatal(1,"budget protocol/candidate error");
            if(dut.cnt_queue>max_queue)max_queue=dut.cnt_queue;
            if(start)start_cycle=cycle;
            if(done)begin
                job=out_epoch-4096;
                if(cycle-start_cycle > 40*34560+128 || cycle-start_cycle >= 1725333)$fatal(1,"60fps budget missed");
                if(number != 0)$fatal(1,"unexpected accepted region");
                case(job)
                    0:if(width!=1152 || height!=480 || area!=552960 || fill!=100 || rejection!=6 || gate_pixels!=92160)$fatal(1,"solid frame statistics");
                    1:if(width!=4 || height!=4 || area!=16 || fill!=100 || rejection!=3 || gate_pixels!=92160)$fatal(1,"checker frame statistics");
                    2:if(width!=0 || height!=0 || area!=0 || fill!=0 || rejection!=0 || gate_pixels!=0)$fatal(1,"stale tile after overwrite");
                    default:$fatal(1,"invalid epoch");
                endcase
                $display("BUDGET epoch=%0d cycles=%0d peak_queue=%0d",job,cycle-start_cycle,max_queue);
                finished=finished+1;
            end
        end
    end
    initial begin
        repeat(5)@(negedge clk);rstn=1;
        for(frame=0;frame<3;frame=frame+1)begin
            frame_start=cycle;epoch=4096+frame;
            for(row=0;row<720;row=row+1)begin
                for(group_index=0;group_index<320;group_index=group_index+1)begin
                    x=group_index*4;y=row;labels=0;hits=0;
                    if(x>=64 && x<1216 && y>=160 && y<640 && frame!=2)begin
                        labels=frame==0 || ((group_index+(row>>2))%2==0) ? 8'h55 : 8'hff;
                        if(x>=544 && x<736)hits=4;
                    end
                    valid=1;sof=row==0 && group_index==0;eof=row==719 && group_index==319;
                    @(negedge clk);valid=0;sof=0;eof=0;repeat(6)@(negedge clk);
                end
            end
            while(cycle-frame_start<1725333)@(negedge clk);
        end
        while(finished<3)@(negedge clk);
        $display("PASS 720P60 component budget: solid, alternating single-cell colors, empty; alternating banks during processing");
        $finish;
    end
    initial begin #100000000;$fatal(1,"budget timeout");end
endmodule
