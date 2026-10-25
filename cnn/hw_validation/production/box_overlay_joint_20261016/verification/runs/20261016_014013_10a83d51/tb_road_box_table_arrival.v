`timescale 1ns/1ps
// A real publisher/table transfer completes during active video, then waits SOF.
module tb_road_box_table_arrival;
    tb_road_box_overlay_joint chain();
    reg pending_during_active=0;
    initial begin
        force chain.publisher.i_pipeline_start_ready=1'b0;
        wait(chain.video_de && chain.vertical==345 && chain.horizontal==900);
        release chain.publisher.i_pipeline_start_ready;
        wait(chain.dst_pending_valid);
        if(!chain.video_de) $fatal(1,"ARRIVAL_NOT_ACTIVE");
        pending_during_active=1;
        $display("TABLE_ARRIVAL_ACTIVE pending_row=%0d pending_x=%0d",chain.vertical,chain.horizontal);
        wait(chain.dst_update);
        if(!pending_during_active || !chain.dst_sof) $fatal(1,"ARRIVAL_SWITCH_WITHOUT_SOF");
        $display("TABLE_ARRIVAL_SOF_PASS publisher_random_entries active_pending_held_until_blankSOF");
    end
    always @(posedge chain.dst_clk) begin
        if(pending_during_active && !chain.dst_sof && !chain.dst_update && !chain.capturing) begin
            if(chain.dst_active_valid || chain.dst_entry!==97'd0 || chain.dst_metadata!==265'd0)
                $fatal(1,"TABLE_CHANGED_DURING_ACTIVE");
        end
    end
endmodule
