`timescale 1ns/1ps

// Controlled frame/visibility/identity services around real frozen slot RTL.
module tb_road_dispatch_fixture(
    input i_clk, input i_rstn, input i_job_ready,
    input i_external_done, input [31:0] i_external_done_id,
    output o_job_valid, output [224:0] o_job_descriptor,
    output o_timestamp_mismatch, output o_busy, output o_error,
    output o_wrap_fault, output [1:0] o_free_mask,
    output [1:0] o_ready_mask, output [1:0] o_reading_mask,
    output [1:0] o_quarantine_mask
);
    reg sof=0;
    reg [31:0] frame_id=0;
    reg [63:0] diagnostic_time=0;
    reg capture_end=0;
    reg [18:0] capture_bytes=0;
    reg frame_error=0;
    reg visible=0;
    reg visible_slot=0;
    reg [31:0] visible_epoch=32'h10203040;
    reg [31:0] visible_frame=0;
    reg identity_valid=0;
    reg [127:0] identity_payload=0;
    reg claim_enable=1;
    reg done_valid=0;
    reg [31:0] done_id=0;
    reg last_valid=0;
    reg last_slot=0;
    reg [31:0] last_epoch=32'h10203040;
    reg [31:0] last_frame=0;
    wire identity_ready;
    wire claim_valid;
    wire claim_slot;
    wire [31:0] claim_epoch;
    wire [31:0] claim_frame;
    wire slot_claim_ready;
    wire release_valid;
    wire release_slot;
    wire [31:0] release_epoch;
    wire [31:0] release_frame;
    wire [63:0] slot_epochs;
    wire [63:0] slot_frames;
    wire [127:0] slot_times;
    wire capture_active;
    wire capture_slot;
    wire capture_accepted;
    wire frame_skipped;
    wire slot_error;
    integer claims=0;
    integer jobs=0;
    integer releases=0;
    integer identities=0;
    integer skips=0;
    reg [224:0] accepted_job;
    reg held_claim=0;
    reg [64:0] held_claim_payload;
    reg held_job=0;
    reg owner_loss_probe=0;
    reg [225:0] held_job_payload;

    road_capture_slots slots(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_sof(sof),.i_epoch(32'h10203040),
        .i_frame_id(frame_id),.i_timestamp(diagnostic_time),.i_capture_end(capture_end),
        .i_capture_bytes(capture_bytes),.i_frame_error(frame_error),
        .i_write_visible(visible),.i_visible_slot(visible_slot),.i_visible_epoch(visible_epoch),
        .i_visible_frame_id(visible_frame),.i_read_claim_valid(claim_valid&&claim_enable),
        .i_read_claim_slot(claim_slot),.i_read_claim_epoch(claim_epoch),.i_read_claim_frame_id(claim_frame),
        .i_last_read_consumed(release_valid),.i_release_slot(release_slot),
        .i_release_epoch(release_epoch),.i_release_frame_id(release_frame),
        .o_claim_ready(slot_claim_ready),.o_capture_active(capture_active),.o_capture_slot(capture_slot),
        .o_capture_base(),.o_capture_accepted(capture_accepted),.o_frame_skipped(frame_skipped),
        .o_free_mask(o_free_mask),.o_ready_mask(o_ready_mask),.o_reading_mask(o_reading_mask),
        .o_quarantine_mask(o_quarantine_mask),.o_slot_epochs(slot_epochs),
        .o_slot_frame_ids(slot_frames),.o_slot_timestamps(slot_times),.o_protocol_error(slot_error)
    );

    road_frame_ready_dispatch dispatcher(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_epoch(32'h10203040),.i_model_id(32'hb35d4a66),
        .i_identity_valid(identity_valid),.i_identity_payload(identity_payload),.o_identity_ready(identity_ready),
        .i_slot_free_mask(o_free_mask),.i_slot_ready_mask(o_ready_mask),.i_slot_reading_mask(o_reading_mask),
        .i_slot_quarantine_mask(o_quarantine_mask),.i_slot_epochs(slot_epochs),
        .i_slot_frame_ids(slot_frames),.i_slot_timestamps(slot_times),
        .i_claim_ready(slot_claim_ready&&claim_enable),.o_claim_valid(claim_valid),.o_claim_slot(claim_slot),
        .o_claim_epoch(claim_epoch),.o_claim_frame_id(claim_frame),
        .o_job_valid(o_job_valid),.o_job_descriptor(o_job_descriptor),
        .o_job_timestamp_mismatch(o_timestamp_mismatch),.i_job_ready(i_job_ready),
        .i_task_done(i_external_done||done_valid),.i_task_done_id(i_external_done?i_external_done_id:done_id),
        .i_last_read_valid(last_valid),.i_last_read_slot(last_slot),.i_last_read_epoch(last_epoch),
        .i_last_read_frame_id(last_frame),.o_last_read_consumed(release_valid),
        .o_release_slot(release_slot),.o_release_epoch(release_epoch),.o_release_frame_id(release_frame),
        .o_busy(o_busy),.o_error(o_error),.o_task_wrap_fault(o_wrap_fault)
    );

    always @(posedge i_clk) begin
        if(!i_rstn) begin held_claim=0;held_job=0; end
        else begin
            if(held_claim && (!claim_valid||{claim_epoch,claim_frame,claim_slot}!==held_claim_payload))
                $fatal(1,"claim payload changed under backpressure");
            if(held_job && !owner_loss_probe && (!o_job_valid||{o_timestamp_mismatch,o_job_descriptor}!==held_job_payload))
                $fatal(1,"job payload changed under backpressure");
            held_claim=claim_valid&&!(slot_claim_ready&&claim_enable);
            held_claim_payload={claim_epoch,claim_frame,claim_slot};
            held_job=o_job_valid&&!i_job_ready;
            held_job_payload={o_timestamp_mismatch,o_job_descriptor};
            if(claim_valid&&slot_claim_ready&&claim_enable) claims=claims+1;
            if(o_job_valid&&i_job_ready) begin
                if(!o_reading_mask[o_job_descriptor[0]]) $fatal(1,"job preceded actual slot claim");
                accepted_job=o_job_descriptor;jobs=jobs+1;
                $display("DISPATCH_JOB slot=%0d base=%h epoch=%h task=%0d source=%0d model=%h capture_ms=%0d mismatch=%0d diagnostic_time=%0d",
                    o_job_descriptor[0],o_job_descriptor[32:1],o_job_descriptor[64:33],o_job_descriptor[96:65],
                    o_job_descriptor[128:97],o_job_descriptor[160:129],o_job_descriptor[224:161],
                    o_timestamp_mismatch,o_job_descriptor[0]?slot_times[127:64]:slot_times[63:0]);
            end
            if(release_valid) begin
                if(!o_reading_mask[release_slot]||release_epoch!==last_epoch||release_frame!==last_frame)
                    $fatal(1,"release lacked real pre-edge READING/matching consumed identity");
                releases=releases+1;
            end
            if(identity_valid&&identity_ready) identities=identities+1;
            if(frame_skipped) skips=skips+1;
        end
    end

    task clear_drives;
        begin
            sof=0;capture_end=0;frame_error=0;visible=0;identity_valid=0;claim_enable=1;
            done_valid=0;last_valid=0;visible_epoch=32'h10203040;last_epoch=32'h10203040;
            claims=0;jobs=0;releases=0;identities=0;skips=0;
            owner_loss_probe=0;
        end
    endtask
    task allocate;
        input [31:0] source;
        input [63:0] diagnostic_ms;
        input expected_slot;
        begin
            @(negedge i_clk);frame_id=source;diagnostic_time=diagnostic_ms;sof=1;
            @(posedge i_clk);#0.001;
            if(!capture_accepted||capture_slot!==expected_slot) $fatal(1,"allocation mismatch source=%0d",source);
            @(negedge i_clk);sof=0;
        end
    endtask
    task finish_capture;
        input [18:0] bytes;
        begin
            @(negedge i_clk);capture_bytes=bytes;capture_end=1;
            @(negedge i_clk);capture_end=0;
        end
    endtask
    task write_visible;
        input slot;
        input [31:0] source;
        begin
            @(negedge i_clk);visible_slot=slot;visible_frame=source;visible=1;
            @(negedge i_clk);visible=0;
        end
    endtask
    task send_identity;
        input [31:0] epoch;
        input [31:0] source;
        input [63:0] capture_ms;
        integer watchdog;
        begin
            @(negedge i_clk);identity_payload={epoch,source,capture_ms};identity_valid=1;watchdog=0;
            @(posedge i_clk);
            while(!identity_ready&&watchdog<1000) begin @(posedge i_clk);watchdog=watchdog+1; end
            if(!identity_ready) $fatal(1,"identity handshake timeout source=%0d",source);
            @(negedge i_clk);identity_valid=0;
        end
    endtask
    task last_read;
        input slot;
        input [31:0] epoch;
        input [31:0] source;
        begin
            @(negedge i_clk);last_slot=slot;last_epoch=epoch;last_frame=source;last_valid=1;
            @(negedge i_clk);last_valid=0;
        end
    endtask
    task task_done;
        input [31:0] task_number;
        begin
            @(negedge i_clk);done_id=task_number;done_valid=1;
            @(negedge i_clk);done_valid=0;
        end
    endtask
endmodule
