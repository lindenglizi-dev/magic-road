`timescale 1ns / 1ps
module tb_ball_epoch;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,early=0,restart=0;reg [3:0] keys=15;
    wire [15:0] epoch,active_epoch;wire clear_history,clear_counts;
    ball_key_control #(.C_DEBOUNCE(2),.C_LONG_PRESS(1000)) dut(.i_clk(clk),.i_rstn(rstn),.i_keys_n(keys),
        .i_early(early),.i_session_restart(restart),.o_count_mode(),.o_strict(),.o_mask(),.o_epoch(epoch),
        .o_active_epoch(active_epoch),.o_clear(clear_history),.o_clear_counts(clear_counts),.o_camera_step());
    reg [15:0] job_epoch=0;integer index,compares=0;
    always @(negedge clk)if(rstn)begin
        if(!clear_history && epoch !== active_epoch)$fatal(1,"uncommitted epoch escaped clear");
        if(((job_epoch == epoch) && !clear_history) !== ((job_epoch == active_epoch) && !clear_history))
            $fatal(1,"retirement qualification changed");
        compares=compares+1;
    end
    task commit;
        begin
            @(posedge clk);#1;early=1;
            @(posedge clk);#1;early=0;restart=0;
        end
    endtask
    initial begin
        repeat(3)@(posedge clk);#1;rstn=1;
        for(index=0;index<4;index=index+1)begin
            keys[index]=0;repeat(10)@(posedge clk);#1;keys=15;repeat(10)@(posedge clk);#1;
            job_epoch=active_epoch;commit;
        end
        restart=1;commit;job_epoch=active_epoch;repeat(4)@(posedge clk);#1;
        keys[3]=0;repeat(10)@(posedge clk);#1;keys=15;repeat(10)@(posedge clk);#1;
        restart=1;job_epoch=active_epoch;commit;
        repeat(3)@(posedge clk);#1;
        if(active_epoch != 5)$fatal(1,"simultaneous restart/clear incremented twice %0d",active_epoch);
        $display("PASS stable epoch retirement equivalence, mode/threshold/clear/restart and simultaneous commit (%0d checks)",compares);$finish;
    end
endmodule
