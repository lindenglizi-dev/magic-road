`timescale 1ns/1ps
module tb_ddr_pipeline;
    localparam WIDTH = 17, HEIGHT = 4;
    reg clk = 0, rst_n = 0;
    reg task_valid = 0, in_valid = 0, in_pixel = 0, in_last = 0, in_frame_last = 0;
    reg [31:0] task_id = 0, task_frame_id = 0, in_task_id = 0;
    reg [2:0] in_y = 0;
    reg cancel = 0, candidate_release = 0, read_valid = 0, response_ready = 0;
    reg [1:0] read_index = 0;
    reg processed_valid = 0, processed_error = 0;
    reg [31:0] processed_task_id = 0, processed_frame_id = 0;
    reg [2:0] processed_count = 0, accepted_count = 0;
    reg display_commit_ack = 0, failure_ack = 0;
    reg commit_ready = 1;
    reg [31:0] display_ack_task_id = 0, display_ack_frame_id = 0;
    reg object_done_valid = 0, object_accepted = 0;
    reg [31:0] object_task_id = 0, object_frame_id = 0;
    reg [1:0] object_done_index = 0;
    wire object_done_ready, commit_valid;
    wire task_ready, in_ready, rejected_input;
    wire candidate_valid, candidate_success, candidate_release_blocked;
    wire [7:0] candidate_reason, final_reason;
    wire [2:0] candidate_count, final_candidate_count, final_processed_count, final_accepted_count;
    wire [31:0] candidate_task_id, candidate_frame_id, response_task_id, response_frame_id;
    wire [31:0] final_task_id, final_frame_id;
    wire read_ready, response_valid, processed_ready, final_valid, final_success;
    wire [1:0] response_index;
    wire [5:0] response_label;
    wire [4:0] response_xmin, response_xmax;
    wire [2:0] response_ymin, response_ymax;
    wire [15:0] response_area;
    wire algorithm_release, banks_empty, abort_active, core_reset_active;
    integer checks = 0, tasks = 0, terminals = 0, resets = 0, frame_ends = 0;
    integer row, col, slot, held_count, saved_ends;
    reg [31:0] saved_task;
    reg [15:0] saved_area;

    always #5 clk = !clk;
    ccl_pipeline_trial_top #(.WIDTH(WIDTH), .HEIGHT(HEIGHT), .X_WIDTH(5), .Y_WIDTH(3),
        .LABEL_WIDTH(6), .MAX_LABEL(32)) dut (
        .clk(clk), .rst_n(rst_n), .task_valid(task_valid), .task_ready(task_ready),
        .task_id(task_id), .task_frame_id(task_frame_id), .in_valid(in_valid), .in_ready(in_ready),
        .in_task_id(in_task_id), .in_y(in_y), .in_pixel(in_pixel), .in_last(in_last),
        .in_frame_last(in_frame_last), .cancel(cancel), .rejected_input(rejected_input),
        .candidate_valid(candidate_valid), .candidate_success(candidate_success),
        .candidate_reason(candidate_reason), .candidate_count(candidate_count),
        .candidate_task_id(candidate_task_id), .candidate_frame_id(candidate_frame_id),
        .candidate_release(candidate_release), .candidate_release_blocked(candidate_release_blocked),
        .read_valid(read_valid), .read_ready(read_ready), .read_index(read_index),
        .response_valid(response_valid), .response_ready(response_ready), .response_index(response_index),
        .response_label(response_label), .response_xmin(response_xmin), .response_xmax(response_xmax),
        .response_ymin(response_ymin), .response_ymax(response_ymax), .response_area(response_area),
        .response_task_id(response_task_id), .response_frame_id(response_frame_id),
        .processed_valid(processed_valid), .processed_ready(processed_ready),
        .processed_task_id(processed_task_id), .processed_frame_id(processed_frame_id),
        .processed_count(processed_count), .accepted_count(accepted_count), .processed_error(processed_error),
        .object_done_valid(object_done_valid), .object_done_ready(object_done_ready),
        .object_task_id(object_task_id), .object_frame_id(object_frame_id),
        .object_done_index(object_done_index), .object_accepted(object_accepted),
        .final_valid(final_valid), .final_success(final_success), .final_reason(final_reason),
        .final_candidate_count(final_candidate_count), .final_processed_count(final_processed_count),
        .final_accepted_count(final_accepted_count), .final_task_id(final_task_id), .final_frame_id(final_frame_id),
        .display_commit_ack(display_commit_ack), .failure_ack(failure_ack), .algorithm_release(algorithm_release),
        .display_ack_task_id(display_ack_task_id), .display_ack_frame_id(display_ack_frame_id),
        .commit_valid(commit_valid), .commit_ready(commit_ready),
        .banks_empty(banks_empty), .abort_active(abort_active), .core_reset_active(core_reset_active)
    );
    always @(posedge clk) begin
        if (rst_n && task_valid && task_ready) tasks = tasks + 1;
        if (rst_n && algorithm_release) terminals = terminals + 1;
        if (rst_n && core_reset_active) resets = resets + 1;
        if (rst_n && dut.u_core.analysis_eof) frame_ends = frame_ends + 1;
    end
    task check;
        input condition;
        input [8*100-1:0] message;
        begin
            checks = checks + 1;
            if (!condition) $fatal(1,"check %0d: %0s",checks,message);
        end
    endtask
    task start;
        input integer identity;
        begin
            @(negedge clk); task_id = identity; task_frame_id = identity + 100;
            task_valid = 1;
            while (!task_ready) @(negedge clk);
            @(negedge clk); task_valid = 0;
            $display("START task=%0d",identity);
        end
    endtask
    task pixel;
        input integer identity, y, x, pattern;
        begin
            @(negedge clk); in_valid = 1; in_task_id = identity; in_y = y;
            in_pixel = (pattern == 2) ? 0 :
                       ((pattern == 3) ? ((x == 3) || (x == 6)) :
                       ((pattern == 1) ? ((x % 2) == 0) : ((x >= 3) && (x <= 6))));
            in_last = (x == WIDTH-1); in_frame_last = in_last && (y == HEIGHT-1);
            #1;
            while (!in_ready) begin
                @(negedge clk); #1;
                check(!task_ready,"no next task while input waits");
            end
            @(negedge clk); in_valid = 0;
        end
    endtask
    task frame;
        input integer identity, pattern;
        begin
            for (row = 0; row < HEIGHT; row = row + 1)
                for (col = 0; col < WIDTH; col = col + 1)
                    pixel(identity,row,col,pattern);
        end
    endtask
    task await_candidate;
        begin
            wait(candidate_valid); @(negedge clk);
            check(!task_ready,"candidate ownership blocks new source task");
        end
    endtask
    task read_table;
        input integer identity, pattern;
        begin
            held_count = candidate_count;
            repeat (4) begin
                @(negedge clk);
                check(candidate_task_id == identity && candidate_count == held_count,
                      "descriptor stable while consumer delays");
            end
            for (slot = 0; slot < held_count; slot = slot + 1) begin
                @(negedge clk); read_index = slot; read_valid = 1;
                #1; check(read_ready,"ordered table request accepted");
                @(negedge clk); read_valid = 0; candidate_release = 1;
                #1; check(candidate_release_blocked && !task_ready,
                           "release rejected before last return is accepted");
                wait(response_valid); @(negedge clk);
                saved_task = response_task_id; saved_area = response_area;
                repeat (3) begin
                    check(response_valid && response_task_id == saved_task && response_area == saved_area,
                          "read response stable under backpressure");
                    check(candidate_release_blocked && candidate_valid,"held return retains table");
                    @(negedge clk);
                end
                check(response_task_id == identity && response_frame_id == identity+100,
                      "table response preserves source identity");
                check(response_index == slot,"table response preserves index");
                if (pattern == 0) begin
                    check(response_area == 16 && response_xmin == 3 && response_xmax == 6 &&
                          response_ymin == 0 && response_ymax == 3,"rectangle gold");
                end else if (pattern == 1) begin
                    check(response_area == 4 && response_xmin == slot*2 && response_xmax == slot*2 &&
                          response_label == slot+1,"four area ties retain ascending labels");
                end
                candidate_release = (slot == held_count-1); response_ready = 1;
                @(negedge clk); response_ready = 0;
            end
            @(negedge clk); candidate_release = 1;
            @(negedge clk); candidate_release = 0;
            check(processed_ready && !task_ready,"table release does not release full task");
        end
    endtask
    task complete_object;
        input integer identity, index, kept;
        begin
            @(negedge clk); object_task_id=identity; object_frame_id=identity+100;
            object_done_index=index; object_accepted=kept; object_done_valid=1;
            #1; check(object_done_ready,"object completion accepted by the serial contract");
            @(negedge clk); object_done_valid=0;
        end
    endtask
    task report_process;
        input integer identity, completed, kept, error;
        begin
            @(negedge clk); processed_task_id = identity; processed_frame_id = identity+100;
            processed_count = completed; accepted_count = kept; processed_error = error; processed_valid = 1;
            @(negedge clk); processed_valid = 0; processed_error = 0;
            check(final_valid,"processed terminal is observable");
        end
    endtask
    task process;
        input integer identity, completed, kept, error;
        integer index;
        begin
            for(index=0;index<completed;index=index+1)
                complete_object(task_id,index,index<kept);
            report_process(identity,completed,kept,error);
        end
    endtask
    task finish;
        input integer success;
        begin
            check(final_valid && final_success == success,"final qualification");
            check(final_task_id == task_id && final_frame_id == task_frame_id,"final identity preserved end to end");
            repeat (3) begin
                @(negedge clk); check(!task_ready && final_valid,"final waits commit or failure acknowledgement");
            end
            display_ack_task_id = task_id; display_ack_frame_id=task_frame_id;
            display_commit_ack = success; failure_ack = !success;
            @(negedge clk); display_commit_ack = 0; failure_ack = 0;
            check(task_ready,"task released after its qualified terminal acknowledgement");
        end
    endtask
    task finish_abort;
        begin
            await_candidate();
            check(!candidate_success && candidate_count == 0 && candidate_reason != 0,
                  "abort has explicit failed candidate and no public objects");
            check(banks_empty && !core_reset_active,"abort returned only after cache drain and reset recovery");
            candidate_release = 1;
            @(negedge clk); candidate_release = 0;
            check(final_valid,"failed candidate becomes full task failure");
            finish(0);
        end
    endtask
    initial begin
        repeat(3) @(posedge clk); @(negedge clk); rst_n = 1;
        // Normal table/processing/commit, including all candidates rejected normally.
        start(1); frame(1,0);
        check(dut.state==1 && dut.input_complete && !in_ready,
              "last source handshake seals input while CCL still RUNs");
        await_candidate();
        check(!in_ready,"final input handshake stops any extra source rows");
        check(candidate_success && candidate_count == 1,"normal candidate success");
        read_table(1,0); process(1,1,0,0); finish(1);
        // Partial downstream processing cannot publish a normal full-frame result.
        start(2); frame(2,1); await_candidate();
        check(candidate_success && candidate_count == 4,"four candidates");
        read_table(2,1); process(2,2,2,1); finish(0);
        // Cancel when two banks are occupied. No EOF is required for recovery.
        start(3); saved_ends = frame_ends;
        for (row=0;row<HEIGHT;row=row+1)
            for (col=0;col<WIDTH;col=col+1) pixel(3,row,col,1);
        @(negedge clk);
        wait(dut.u_lines.bank_state[0] != 0 && dut.u_lines.bank_state[1] != 0);
        check(!banks_empty,"both banks occupied at cancellation");
        cancel = 1; @(negedge clk); cancel = 0;
        finish_abort(); check(frame_ends == saved_ends,"half-frame cancel never waited for normal EOF");
        // Late A events keep A's ID and are rejected before and during B.
        @(negedge clk); in_valid=1; in_task_id=3; in_y=0; in_last=0; in_frame_last=0;
        #1; check(!in_ready && rejected_input,"late A while idle rejected");
        @(negedge clk); in_valid=0;
        start(4);
        @(negedge clk); in_valid=1; in_task_id=3;
        #1; check(!in_ready && rejected_input,"late A never relabelled to B");
        @(negedge clk); in_valid=0;
        frame(4,0); await_candidate(); read_table(4,0); process(4,1,1,0); finish(1);
        // A malformed partial row causes controlled reset rather than waiting for CCL done.
        start(5); pixel(5,0,0,0);
        @(negedge clk); in_valid=1; in_task_id=5; in_y=0; in_last=1; in_frame_last=0;
        @(negedge clk); in_valid=0;
        finish_abort();
        // Cancellation coincides with the pending RAM return of a last pixel.
        start(6);
        for(col=0;col<WIDTH;col=col+1) pixel(6,0,col,0);
        wait(dut.u_lines.read_pending && dut.u_lines.pending_last);
        @(negedge clk); cancel=1;
        @(negedge clk); cancel=0;
        finish_abort();
        // Recovery remains usable after protocol error and cancellation.
        start(7); frame(7,0); await_candidate(); read_table(7,0); process(7,1,1,0); finish(1);
        // Preasserted table release cannot skip the candidate stage; empty is successful.
        start(8); candidate_release = 1; frame(8,2); await_candidate();
        check(candidate_success && candidate_count == 0,"empty candidate has success qualification");
        @(negedge clk); candidate_release=0;
        check(processed_ready,"empty table release needs no read");
        process(8,0,0,0); finish(1);
        // Identity and count checks independently fail even without processed_error.
        start(9); frame(9,0); await_candidate(); read_table(9,0); process(99,1,1,0); finish(0);
        start(10); frame(10,0); await_candidate(); read_table(10,0); process(10,0,0,0); finish(0);
        start(11); frame(11,0); await_candidate(); read_table(11,0); process(11,1,2,0); finish(0);
        // Duplicate object 0 cannot replace missing object 1 with a matching count.
        start(12); frame(12,3); await_candidate();
        check(candidate_count==2,"duplicate-completion case has two candidates");
        read_table(12,3); complete_object(12,0,1); complete_object(12,0,1);
        report_process(12,2,2,0); finish(0);
        // A residual/high or late A ACK cannot confirm a newly published B.
        display_commit_ack=1;display_ack_task_id=1;display_ack_frame_id=101;
        commit_ready=0;
        start(13); frame(13,0); await_candidate();read_table(13,0);
        @(negedge clk);
        object_done_valid=1;object_task_id=13;object_frame_id=113;
        object_done_index=0;object_accepted=1;
        processed_valid=1;processed_task_id=13;processed_frame_id=113;
        processed_count=1;accepted_count=1;processed_error=0;
        #1;check(object_done_ready&&!processed_ready,
                 "last object completion precedes simultaneous aggregate report");
        @(negedge clk);object_done_valid=0;
        #1;check(processed_ready,"aggregate report accepted after recorded completion");
        @(negedge clk);processed_valid=0;
        check(final_valid&&final_success,"same-cycle VALIDs preserve successful completion");
        repeat(3) begin @(negedge clk);check(final_valid&&!task_ready&&!dut.commit_published,
            "preasserted ACK before publication cannot release B");end
        cancel=1;commit_ready=1;
        @(negedge clk);cancel=0;
        check(dut.commit_published&&final_valid&&!abort_active,
              "cancel simultaneous with commit publication cannot revoke it");
        display_commit_ack=0;@(negedge clk);display_commit_ack=1;
        @(negedge clk);check(final_valid&&!task_ready,"fresh late A ACK identity rejected");
        display_ack_task_id=13;display_ack_frame_id=113;
        @(negedge clk);check(final_valid&&!task_ready,"relabelled held ACK is not a fresh event");
        display_commit_ack=0;@(negedge clk);display_commit_ack=1;
        @(negedge clk);display_commit_ack=0;
        check(task_ready,"fresh matching published B ACK releases B exactly once");
        check(tasks == terminals && tasks == 13,"accepted/terminal task conservation");
        check(resets == 3,"three explicit abort reset transactions");
        $display("PASS pipeline checks=%0d tasks=%0d terminals=%0d resets=%0d eof=%0d",
                 checks,tasks,terminals,resets,frame_ends);
        $finish;
    end
    initial begin
        #10000000; $fatal(1,"pipeline timeout task=%0d state=%0d feed=%0d rows=%0d/%0d banks=%0d/%0d row=%0d col=%0d",
                         dut.active_task,dut.state,dut.feed_state,dut.committed_rows,dut.completed_rows,
                         dut.u_lines.bank_state[0],dut.u_lines.bank_state[1],row,col);
    end
endmodule
