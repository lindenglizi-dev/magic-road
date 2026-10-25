`timescale 1ns/1ps

// Protocol regression with actual slot state transitions; services remain controlled.
module tb_road_frame_ready_dispatch;
    reg i_clk=0;
    reg i_rstn=0;
    reg job_ready=0;
    wire job_valid;
    wire [224:0] descriptor;
    wire mismatch;
    wire busy;
    wire error;
    wire wrap_fault;
    wire [1:0] free_mask;
    wire [1:0] ready_mask;
    wire [1:0] reading_mask;
    wire [1:0] quarantine_mask;
    integer cases=0;
    integer index;
    integer watchdog;
    integer before_identity;
    reg [224:0] expected_job;

    tb_road_dispatch_fixture fixture(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_job_ready(job_ready),.i_external_done(1'b0),
        .i_external_done_id(32'd0),.o_job_valid(job_valid),.o_job_descriptor(descriptor),
        .o_timestamp_mismatch(mismatch),.o_busy(busy),.o_error(error),.o_wrap_fault(wrap_fault),
        .o_free_mask(free_mask),.o_ready_mask(ready_mask),.o_reading_mask(reading_mask),
        .o_quarantine_mask(quarantine_mask)
    );
    always #5 i_clk=~i_clk;

    task reset_all;
        begin
            @(negedge i_clk);i_rstn=0;job_ready=0;fixture.clear_drives;
            repeat(3) @(negedge i_clk);i_rstn=1;
            repeat(4) @(negedge i_clk);
            if(free_mask!==2'b11||ready_mask||reading_mask||busy||job_valid||wrap_fault||error)
                $fatal(1,"common reset did not cancel dispatcher and real slots");
        end
    endtask
    task expect_no_job;
        input integer clocks;
        begin
            repeat(clocks) begin @(negedge i_clk);if(job_valid) $fatal(1,"ineligible frame produced job"); end
        end
    endtask
    task prepare_frame;
        input slot;
        input [31:0] source;
        input [63:0] capture_ms;
        begin
            fixture.allocate(source,capture_ms+7,slot);
            fixture.send_identity(32'h10203040,source,capture_ms);
            fixture.finish_capture(19'd442368);
            fixture.write_visible(slot,source);
        end
    endtask
    task accept_job;
        input slot;
        input [31:0] source;
        input [31:0] task_number;
        input [63:0] capture_ms;
        begin
            watchdog=0;
            while(!job_valid&&watchdog<1000) begin @(negedge i_clk);watchdog=watchdog+1;end
            expected_job={capture_ms,32'hb35d4a66,source,task_number,32'h10203040,
                slot?32'h03480000:32'h03400000,slot};
            if(!job_valid||descriptor!==expected_job||!mismatch||!reading_mask[slot])
                $fatal(1,"job descriptor mismatch source=%0d task=%0d",source,task_number);
            repeat(16) begin
                @(negedge i_clk);
                if(fixture.dispatcher.cnt_next_task!==task_number)
                    $fatal(1,"next-task counter advanced before actual job acceptance");
            end
            job_ready=1;@(posedge i_clk);
            if(!job_valid) $fatal(1,"valid depended on ready");
            @(negedge i_clk);job_ready=0;
            if(fixture.dispatcher.cnt_next_task!==(task_number==32'hffffffff?32'hffffffff:task_number+32'd1))
                $fatal(1,"next-task counter failed actual job acceptance update");
        end
    endtask
    task finish_task;
        input slot;
        input [31:0] source;
        input [31:0] task_number;
        begin
            fixture.task_done(task_number);
            repeat(4) @(negedge i_clk);
            if(!reading_mask[slot]||free_mask[slot]) $fatal(1,"NNdone released input slot");
            fixture.last_read(slot,32'h10203040,source);
            repeat(3) @(negedge i_clk);
            if(!free_mask[slot]) $fatal(1,"matching last response consumption did not release");
        end
    endtask

    initial begin
        reset_all;
        // Identity can arrive during capture, but complete bytes alone are not READY.
        fixture.allocate(100,107,0);fixture.send_identity(32'h10203040,100,100);
        expect_no_job(8);fixture.finish_capture(442368);expect_no_job(8);
        if(ready_mask||free_mask[0]) $fatal(1,"WAIT_VISIBLE was treated as READY/FREE");
        fixture.write_visible(0,100);accept_job(0,100,1,100);finish_task(0,100,1);cases=cases+1;

        reset_all;
        fixture.allocate(200,207,0);fixture.finish_capture(442368);fixture.write_visible(0,200);
        expect_no_job(8);fixture.send_identity(32'h10203040,200,200);
        accept_job(0,200,1,200);finish_task(0,200,1);cases=cases+1;

        reset_all;
        fixture.allocate(10,17,0);fixture.send_identity(32'h10203040,10,10);fixture.finish_capture(442368);
        prepare_frame(1,11,11);accept_job(1,11,1,11);finish_task(1,11,1);
        fixture.write_visible(0,10);accept_job(0,10,2,10);finish_task(0,10,2);cases=cases+1;

        reset_all;
        fixture.allocate(1,8,0);fixture.send_identity(32'h10203040,1,1);fixture.finish_capture(221184);
        expect_no_job(8);if(!quarantine_mask[0]||free_mask[0]) $fatal(1,"half frame escaped quarantine");
        prepare_frame(1,2,2);accept_job(1,2,1,2);finish_task(1,2,1);
        if(!quarantine_mask[0]) $fatal(1,"dispatcher released quarantine");cases=cases+1;

        reset_all;fixture.claim_enable=0;
        prepare_frame(0,20,20);prepare_frame(1,21,21);
        @(negedge i_clk);fixture.frame_id=22;fixture.sof=1;
        @(posedge i_clk);#0.001;if(!fixture.frame_skipped||fixture.capture_accepted) $fatal(1,"full slots did not skip whole frame");
        @(negedge i_clk);fixture.sof=0;
        repeat(16) @(negedge i_clk);
        if(ready_mask!==2'b11||reading_mask||fixture.claims!=0) $fatal(1,"claim backpressure bypassed");
        fixture.claim_enable=1;accept_job(0,20,1,20);finish_task(0,20,1);
        accept_job(1,21,2,21);finish_task(1,21,2);cases=cases+1;

        reset_all;
        fixture.send_identity(32'h10203041,99,99);fixture.send_identity(32'h10203040,99,99);
        fixture.allocate(30,37,0);fixture.send_identity(32'h10203040,30,30);
        fixture.send_identity(32'h10203040,30,999);fixture.finish_capture(442368);fixture.write_visible(0,30);
        accept_job(0,30,1,30);if(!error) $fatal(1,"bad/duplicate identity lacked diagnostic");
        finish_task(0,30,1);cases=cases+1;

        reset_all;
        fixture.allocate(7,14,0);fixture.finish_capture(442368);fixture.write_visible(0,7);
        fixture.allocate(7,14,1);fixture.finish_capture(442368);fixture.write_visible(1,7);
        fixture.send_identity(32'h10203040,7,7);expect_no_job(16);
        if(!error||fixture.claims!=0) $fatal(1,"ambiguous double-slot identity was selected");cases=cases+1;

        reset_all;
        fixture.allocate(40,47,0);fixture.send_identity(32'h10203040,40,40);
        fixture.last_read(0,32'h10203040,40);if(free_mask[0]) $fatal(1,"early read released capture");
        fixture.finish_capture(442368);fixture.write_visible(0,40);
        wait(job_valid);fixture.last_read(0,32'h10203040,40);
        if(!reading_mask[0]||fixture.releases!=0) $fatal(1,"prejob read release accepted");
        accept_job(0,40,1,40);
        fixture.last_read(1,32'h10203040,40);fixture.last_read(0,32'h10203041,40);
        fixture.last_read(0,32'h10203040,41);fixture.task_done(99);
        if(fixture.releases!=0||!reading_mask[0]) $fatal(1,"wrong lastread/done released owner");
        fixture.task_done(1);fixture.task_done(1);
        if(fixture.releases!=0||!reading_mask[0]||!busy) $fatal(1,"duplicate NNdone fabricated input release or retirement");
        finish_task(0,40,1);fixture.last_read(0,32'h10203040,40);
        if(fixture.releases!=1||!error||fixture.slot_error) $fatal(1,"duplicate release leaked to slot owner");cases=cases+1;

        reset_all;prepare_frame(0,50,50);accept_job(0,50,1,50);
        fixture.last_read(0,32'h10203040,50);
        if(!free_mask[0]||!busy) $fatal(1,"lastread-first owner semantics wrong");
        fixture.allocate(51,58,0);
        before_identity=fixture.identities;
        @(negedge i_clk);fixture.identity_payload={32'h10203040,32'd51,64'd51};fixture.identity_valid=1;
        repeat(16) begin @(negedge i_clk);if(fixture.identity_ready) $fatal(1,"third context silently admitted");end
        fixture.task_done(1);
        while(fixture.identities==before_identity) @(negedge i_clk);
        fixture.identity_valid=0;
        fixture.finish_capture(442368);fixture.write_visible(0,51);
        accept_job(0,51,2,51);finish_task(0,51,2);cases=cases+1;

        // A later alias cannot turn a previously cached identity into a legal candidate.
        reset_all;
        fixture.allocate(80,87,0);fixture.send_identity(32'h10203040,80,80);
        fixture.finish_capture(442368);
        fixture.allocate(80,87,1);fixture.finish_capture(442368);fixture.write_visible(1,80);
        fixture.write_visible(0,80);expect_no_job(16);
        if(fixture.claims!=0||ready_mask!==2'b11||!error)
            $fatal(1,"late duplicate identity bypassed cached candidate eligibility");cases=cases+1;

        reset_all;fixture.claim_enable=0;prepare_frame(0,81,81);wait(fixture.claim_valid);
        @(negedge i_clk);fixture.ambiguous_identity_probe=1;
        fixture.allocate(81,88,1);fixture.finish_capture(442368);fixture.write_visible(1,81);
        fixture.claim_enable=1;expect_no_job(16);
        if(fixture.claims!=0||reading_mask||ready_mask!==2'b11||!error)
            $fatal(1,"late duplicate identity bypassed preclaim guard");cases=cases+1;

        // Task exhaustion is explicit register-state injection, not billions of claimed runs.
        reset_all;@(negedge i_clk);fixture.dispatcher.cnt_next_task=32'hffffffff;
        prepare_frame(0,60,60);accept_job(0,60,32'hffffffff,60);finish_task(0,60,32'hffffffff);
        prepare_frame(0,61,61);expect_no_job(16);
        if(!wrap_fault||fixture.claims!=1||fixture.dispatcher.cnt_next_task!==32'hffffffff)
            $fatal(1,"task counter silently wrapped or claimed after exhaustion");cases=cases+1;

        reset_all;prepare_frame(0,65,65);wait(job_valid);
        @(negedge i_clk);job_ready=1;fixture.done_valid=1;fixture.done_id=1;
        fixture.last_valid=1;fixture.last_slot=0;fixture.last_epoch=32'h10203040;fixture.last_frame=65;
        @(negedge i_clk);job_ready=0;fixture.done_valid=0;fixture.last_valid=0;
        repeat(4) @(negedge i_clk);
        if(!reading_mask[0]||fixture.releases!=0||!busy||!error)
            $fatal(1,"JOB-handshake same-edge early done/read was accepted");
        finish_task(0,65,1);cases=cases+1;

        // Explicit owner-state corruption probes the fail-stop guard, not normal slot behavior.
        reset_all;prepare_frame(0,66,66);wait(job_valid);
        @(negedge i_clk);fixture.owner_loss_probe=1;
        force fixture.slots.slot_bank[0].state_current=3'd0;
        repeat(3) @(negedge i_clk);release fixture.slots.slot_bank[0].state_current;
        if(job_valid||fixture.releases!=0||!busy||!error||fixture.dispatcher.state_current!==3'd4)
            $fatal(1,"JOB owner loss did not stop until common reset");cases=cases+1;
        reset_all;prepare_frame(0,67,67);accept_job(0,67,1,67);
        @(negedge i_clk);fixture.owner_loss_probe=1;
        force fixture.slots.slot_bank[0].frame_store=32'd999;
        repeat(3) @(negedge i_clk);
        fixture.last_read(0,32'h10203040,67);fixture.task_done(1);
        release fixture.slots.slot_bank[0].frame_store;
        if(fixture.releases!=0||!reading_mask[0]||!busy||fixture.dispatcher.state_current!==3'd4)
            $fatal(1,"RUN owner loss fabricated release or retirement");cases=cases+1;

        for(index=0;index<3;index=index+1) begin
            reset_all;if(index==0) fixture.claim_enable=0;
            prepare_frame(0,70,70);
            if(index==0) wait(fixture.claim_valid);
            else if(index==1) wait(job_valid);
            else accept_job(0,70,1,70);
            reset_all;cases=cases+1;
        end
        $display("TB_PASS_FRAME_READY_DISPATCH cases=%0d boundary=real_slots_controlled_identity_visibility_NN_lastconsume",cases);
        $finish;
    end
    initial begin #200000;$fatal(1,"dispatcher protocol watchdog");end
endmodule
