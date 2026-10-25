`timescale 1ns/1ps

// Direct protocol guard tests; this controlled endpoint does not measure C8 CDC or ROM.
module tb_road_result_publisher_protocol;
    reg clk = 1'b0;
    reg rstn = 1'b0;
    reg cancel = 1'b0;
    reg start_valid = 1'b0;
    reg [31:0] epoch = 32'd3;
    reg [31:0] task_id = 32'd11;
    reg [31:0] source_frame = 32'd101;
    reg [31:0] model_id = 32'hb35d4a66;
    reg [63:0] capture_ms = 64'd1000;
    reg [63:0] now_ms = 64'd1004;
    reg pipeline_ready = 1'b1;
    reg entry_valid = 1'b0;
    reg [96:0] entry = 97'd0;
    reg [31:0] result_token = 32'd11;
    reg [6:0] result_count = 7'd0;
    reg result_done = 1'b0;
    reg pipeline_fault = 1'b0;
    reg table_entry_ready = 1'b1;
    reg table_meta_ready = 1'b0;
    reg table_ack = 1'b0;
    reg table_busy = 1'b0;
    reg table_error = 1'b0;
    wire start_ready;
    wire pipeline_valid;
    wire [31:0] pipeline_token;
    wire [31:0] pipeline_model;
    wire pipeline_cancel;
    wire entry_ready;
    wire table_entry_valid;
    wire [96:0] table_entry;
    wire table_meta_valid;
    wire [264:0] table_metadata;
    wire table_abort;
    wire busy;
    wire error;
    integer cases = 0;
    integer accepted = 0;
    integer faults = 0;
    integer index;
    integer kind;
    reg [264:0] frozen_metadata;

    road_result_publisher dut(
        .i_clk(clk),.i_rstn(rstn),.i_cancel(cancel),.i_start_valid(start_valid),
        .i_start_epoch(epoch),.i_start_task_id(task_id),.i_start_source_frame_id(source_frame),
        .i_start_model_id(model_id),.i_start_capture_ms(capture_ms),.i_now_ms(now_ms),
        .i_pipeline_start_ready(pipeline_ready),.i_entry_valid(entry_valid),.i_entry(entry),
        .i_result_frame_token(result_token),.i_result_count(result_count),.i_result_done(result_done),
        .i_pipeline_fault(pipeline_fault),.i_table_entry_ready(table_entry_ready),
        .i_table_meta_ready(table_meta_ready),.i_table_copy_ack(table_ack),
        .i_table_busy(table_busy),.i_table_error(table_error),.o_start_ready(start_ready),
        .o_pipeline_start_valid(pipeline_valid),.o_pipeline_frame_token(pipeline_token),
        .o_pipeline_model_id(pipeline_model),.o_pipeline_cancel(pipeline_cancel),
        .o_entry_ready(entry_ready),.o_table_entry_valid(table_entry_valid),.o_table_entry(table_entry),
        .o_table_meta_valid(table_meta_valid),.o_table_metadata(table_metadata),
        .o_table_abort(table_abort),.o_busy(busy),.o_error(error)
    );

    always #5 clk = ~clk;

    always @(posedge clk) begin
        if (rstn && table_entry_valid && table_entry_ready) begin
            if (entry !== table_entry || !entry_ready)
                $fatal(1,"direct FINAL97 forwarding mismatch");
            accepted = accepted+1;
        end
        if (rstn && table_meta_valid && table_entry_valid)
            $fatal(1,"metadata and entry valid overlap");
        #0.001;
        if (error) faults=faults+1;
    end

    task reset_all;
        begin
            @(negedge clk); rstn=0; cancel=0; start_valid=0; entry_valid=0;
            result_done=0; pipeline_fault=0; table_error=0; table_busy=0; table_ack=0;
            table_meta_ready=0; table_entry_ready=1; pipeline_ready=1;
            epoch=3; task_id=11; source_frame=101; model_id=32'hb35d4a66;
            capture_ms=1000; now_ms=1004; result_token=11; result_count=0; accepted=0;
            #1;
            if(busy || table_meta_valid || table_entry_valid || pipeline_valid || table_abort)
                $fatal(1,"common reset did not cancel protocol state");
            repeat(3) @(negedge clk);
            rstn=1; repeat(4) @(negedge clk);
            if(!start_ready || busy) $fatal(1,"idle after reset not ready");
        end
    endtask

    task start_task;
        begin
            @(negedge clk); start_valid=1;
            #1;
            if(!start_ready || !pipeline_valid || pipeline_token!==11 || pipeline_model!==32'hb35d4a66)
                $fatal(1,"atomic start identity mismatch");
            @(negedge clk); start_valid=0;
            epoch=99; task_id=99; source_frame=99; model_id=99; capture_ms=99;
            if(!busy || start_ready) $fatal(1,"start ownership not retained");
        end
    endtask

    task send_entry;
        input integer item;
        begin
            @(negedge clk); entry_valid=1; entry={1'b1,32'hf0e1d2c3,item[31:0],32'h12345678};
            #1;
            if(!entry_ready || !table_entry_valid) $fatal(1,"legal entry blocked item=%0d",item);
            @(negedge clk); entry_valid=0;
        end
    endtask

    task finish_task;
        input [6:0] count;
        begin
            @(negedge clk); result_count=count; result_done=1;
            #1;
            if(table_meta_valid) $fatal(1,"metadata visible in done cycle");
            @(negedge clk); result_done=0;
            #1;
            frozen_metadata={64'd1004,64'd1000,2'd0,count,32'hb35d4a66,32'd101,32'd11,32'd3};
            if(!table_meta_valid || table_metadata!==frozen_metadata || accepted!=count)
                $fatal(1,"completion metadata mismatch count=%0d",count);
        end
    endtask

    task expect_abort;
        integer previous_faults;
        begin
            previous_faults=faults;
            #1;
            if(!table_abort || table_meta_valid || table_entry_valid)
                $fatal(1,"preseal fault did not immediately block publication kind=%0d",kind);
            @(negedge clk);
            if(!error || !table_abort || !pipeline_cancel)
                $fatal(1,"ABORT state missing kind=%0d",kind);
            entry_valid=0;result_done=0;pipeline_fault=0;table_error=0;cancel=0;
            repeat(4) @(negedge clk);
            if(!start_ready || busy || table_abort || error || faults!=previous_faults+1)
                $fatal(1,"ABORT recovery/pulse mismatch kind=%0d",kind);
            cases=cases+1;
        end
    endtask

    task seal_and_ack;
        begin
            repeat(32) begin
                @(negedge clk);
                if(!table_meta_valid || table_metadata!==frozen_metadata || start_ready)
                    $fatal(1,"metadata hold broke");
            end
            table_meta_ready=1;
            @(negedge clk); table_meta_ready=0;table_busy=1;
            cancel=1;pipeline_fault=1;table_error=1;entry_valid=1;result_done=1;
            repeat(32) begin
                @(negedge clk);
                if(!busy || start_ready || table_abort || pipeline_cancel || table_meta_valid ||
                    table_entry_valid || table_metadata!==frozen_metadata)
                    $fatal(1,"postseal cancellation withdrew committed source");
            end
            table_ack=1;
            @(negedge clk);table_ack=0;table_busy=0;cancel=0;pipeline_fault=0;table_error=0;
            entry_valid=0;result_done=0;
            repeat(2) @(negedge clk);
            if(!start_ready || busy || error) $fatal(1,"copy_ack did not retire");
            cases=cases+1;
        end
    endtask

    initial begin
        reset_all;
        // A provider must assert valid without waiting for the consumer's ready.
        pipeline_ready=0;start_valid=1;
        repeat(8) begin
            @(negedge clk);
            if(start_ready || !pipeline_valid || busy) $fatal(1,"upstream valid depends on ready");
        end
        pipeline_ready=1;
        @(negedge clk);start_valid=0;
        if(!busy) $fatal(1,"waiting upstream start not accepted");
        cases=cases+1;

        for(index=0;index<3;index=index+1) begin
            reset_all;start_task;
            if(index==1) send_entry(0);
            if(index==2) begin
                for(kind=0;kind<64;kind=kind+1) send_entry(kind);
            end
            finish_task(index==0 ? 0 : index==1 ? 1 : 64);
            seal_and_ack;
        end

        // Each malformed RUN terminal condition must cancel, never seal a half table.
        for(kind=0;kind<8;kind=kind+1) begin
            reset_all;start_task;send_entry(0);
            @(negedge clk);
            case(kind)
                0: begin entry_valid=1;result_token=12; end
                1: begin result_done=1;result_count=2; end
                2: begin result_done=1;result_count=1;entry_valid=1; end
                3: begin result_done=1;result_count=1;now_ms=999; end
                4: begin result_done=1;result_count=1;result_token=12; end
                5: pipeline_fault=1;
                6: table_error=1;
                7: cancel=1;
            endcase
            expect_abort;
        end

        reset_all;start_task;
        for(index=0;index<64;index=index+1) send_entry(index);
        @(negedge clk);entry_valid=1;kind=8;expect_abort;

        // Same-cycle META ready and cancellation/fault must prefer abort over seal.
        for(kind=9;kind<13;kind=kind+1) begin
            reset_all;start_task;finish_task(0);
            table_meta_ready=1;
            case(kind)
                9: cancel=1;
                10: pipeline_fault=1;
                11: table_error=1;
                12: entry_valid=1;
            endcase
            expect_abort;
        end

        // Source nonempty blocks admission; it is not treated as an empty table.
        reset_all;table_busy=1;start_valid=1;
        repeat(8) begin
            @(negedge clk);
            if(start_ready || pipeline_valid || busy) $fatal(1,"source ownership admission failure");
        end
        cases=cases+1;

        // One common reset cancels each of RUN, META and WAIT_ACK.
        for(index=0;index<3;index=index+1) begin
            reset_all;start_task;
            if(index>0) finish_task(0);
            if(index==2) begin table_meta_ready=1;@(negedge clk);table_meta_ready=0;table_busy=1; end
            reset_all;cases=cases+1;
        end
        $display("TB_PASS_RESULT_PUBLISHER_PROTOCOL cases=%0d abort_pulses=%0d",cases,faults);
        $finish;
    end

    initial begin
        #100000;
        $fatal(1,"publisher protocol watchdog");
    end
endmodule
