`timescale 1ns / 1ps
`define RUN dut.down2_dynamic_tile_runner_Inst_compute
`define PP `RUN.road_postprocess_stream_Inst_tile.u_chain
module tb_rom_down2(output reg o_test_done);
    reg clk=0; always #5 clk=~clk;
    reg rstn=0, load_valid=0, start=0, commit_ready=1, export_start=0, output_ready=1;
    reg [10:0]load_addr=0;
    reg signed [7:0]load_data=0;
    wire load_ready, parameters_ready, busy, done, fault, output_valid, export_done;
    wire signed [7:0]output_data;
    wire [8:0]output_index;
    reg [7:0]expected_kind[0:1675], expected_table[0:1675];
    reg [15:0]expected_address[0:1675];
    reg [31:0]expected_data[0:1675], expected_acc[0:639], expected_stages[0:1919];
    reg [7:0]halo[0:1295], expected_output[0:383];
    reg [639:0]seen;
    reg checking=0, random_stalls=0;
    reg [15:0]random_bits=16'hace1;
    reg previous_valid=0, previous_ready=0;
    reg [16:0]previous_output;
    reg previous_parameter_valid=0, previous_parameter_ready=0;
    reg [46:0]previous_parameter_payload;
    integer parameter_count=0, ticks=0, case_id=0;
    integer i,j,idx,lane,layer,position,channel,accs,pres,silus,posts,commits,exports;
    integer bins[0:5], category, report, observed_core;
    reg [47:0]tags;
    reg [15:0]external_tag;
    reg [4095:0]vectors, path, report_path;
    road_rom_down2_top dut(
        .i_clk(clk),.i_rstn(rstn),.i_load_valid(load_valid),.i_load_addr(load_addr),.i_load_data(load_data),
        .o_load_ready(load_ready),.i_start(start),.i_commit_ready(commit_ready),.i_export_start(export_start),
        .i_output_ready(output_ready),.o_parameters_ready(parameters_ready),.o_busy(busy),.o_done(done),
        .o_fault(fault),.o_output_valid(output_valid),.o_output_data(output_data),
        .o_output_index(output_index),.o_export_done(export_done)
    );
    task resolve_index;
        input [15:0]tag;
        output integer resolved;
        begin
            if(tag[15:5] !== 11'd0 || tag[1:0] > 2) $fatal(1,"Bad stage tag");
            tags=`PP.reg_retire_tags[tag[4:2]];
            external_tag=tags >> (tag[1:0]*16);
            resolved=external_tag[15] ? 256+external_tag[14:11]*24+external_tag[10:6] :
                                       external_tag[14:11]*16+external_tag[10:6];
            if(resolved<0 || resolved>639) $fatal(1,"Bad resolved stage identity");
        end
    endtask
    always @(negedge clk) begin
        if(random_stalls) begin
            random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
            commit_ready=(ticks%257>=72) && random_bits[0];
            output_ready=random_bits[1];
        end
    end
    always @(posedge clk) begin
        ticks=ticks+1;
        if(!rstn) begin parameter_count=0; previous_valid=0; previous_parameter_valid=0; end
        else begin
            if(!parameters_ready && (busy || output_valid || load_ready)) $fatal(1,"Partial boot opened interface");
            if(previous_valid && !previous_ready &&
               (!output_valid || {output_index,output_data} !== previous_output)) $fatal(1,"Export changed under stall");
            previous_valid=output_valid; previous_ready=output_ready; previous_output={output_index,output_data};
            if(previous_parameter_valid && !previous_parameter_ready &&
                (!dut.pref_load_valid || {dut.pref_load_kind,dut.pref_load_address,dut.pref_load_data} !== previous_parameter_payload))
                $fatal(1,"Parameter payload changed under stall");
            previous_parameter_valid=dut.pref_load_valid; previous_parameter_ready=dut.runner_load_ready;
            previous_parameter_payload={dut.pref_load_kind,dut.pref_load_address,dut.pref_load_data};
            if(dut.pref_load_valid && dut.runner_load_ready) begin
                if(parameter_count>=1676 || expected_table[parameter_count] ||
                   dut.pref_load_kind !== expected_kind[parameter_count][2:0] ||
                   dut.pref_load_address !== expected_address[parameter_count][10:0] ||
                   dut.pref_load_data !== expected_data[parameter_count]) $fatal(1,"Parameter mismatch %0d",parameter_count);
                parameter_count=parameter_count+1;
            end
            if(dut.pref_table_valid && dut.runner_table_ready) begin
                if(parameter_count>=1676 || !expected_table[parameter_count] ||
                   dut.pref_table_address !== expected_address[parameter_count][9:0] ||
                   dut.pref_table_data !== expected_data[parameter_count][15:0]) $fatal(1,"Table mismatch %0d",parameter_count);
                parameter_count=parameter_count+1;
            end
            if(checking) begin
                if(fault) $fatal(1,"Unexpected compute fault");
                if(busy) begin
                    observed_core=observed_core+1;
                    if(`RUN.pp_output_valid && !commit_ready) category=0;
                    else if((`RUN.flag_pp_input_valid && !`RUN.pp_input_ready) ||
                            ((`RUN.state_current==4'd2) && (`RUN.cnt_mac_group==0) && !`RUN.flag_can_reserve)) category=1;
                    else if(`RUN.flag_commit_accept) category=2;
                    else if(`RUN.flag_mac_input_accept) category=3;
                    else if(`RUN.state_current==4'd1 || `RUN.state_current==4'd2) category=4;
                    else category=5;
                    bins[category]=bins[category]+1;
                end
                if(`RUN.flag_pp_input_accept) begin
                    for(lane=0;lane<3;lane=lane+1) if(`RUN.wire_result_lane_mask[lane]) begin
                        idx=`RUN.flag_layer_pw ? 256+`RUN.wire_pp_position*24+`RUN.wire_result_channel_base+lane :
                                                `RUN.wire_pp_position*16+`RUN.wire_result_channel_base+lane;
                        if(`RUN.wire_pp_result_data[lane*32+:32] !== expected_acc[idx]) $fatal(1,"MAC mismatch %0d",idx);
                        accs=accs+1;
                    end
                end
                if(`PP.flag_silu_accept) begin
                    resolve_index(`PP.pre_result_tag,idx);
                    if($signed(`PP.pre_result_data) !== $signed(expected_stages[idx*3])) $fatal(1,"Pre mismatch %0d",idx);
                    pres=pres+1;
                end
                if(`PP.flag_post_accept) begin
                    resolve_index(`PP.reg_meta_tags[`PP.reg_meta_read],idx);
                    if($signed(`PP.silu_output_data) !== $signed(expected_stages[idx*3+1])) $fatal(1,"SiLU mismatch %0d",idx);
                    silus=silus+1;
                end
                if(`PP.flag_post_complete) begin
                    resolve_index(`PP.post_result_tag,idx);
                    if($signed(`PP.post_result_data) !== $signed(expected_stages[idx*3+2])) $fatal(1,"Post mismatch %0d",idx);
                    posts=posts+1;
                end
                if(`RUN.flag_commit_accept) begin
                    idx=`RUN.pp_output_tag[15] ? 256+`RUN.pp_output_tag[14:11]*24+`RUN.pp_output_tag[10:6] :
                                               `RUN.pp_output_tag[14:11]*16+`RUN.pp_output_tag[10:6];
                    if(idx>639 || seen[idx] || $signed(`RUN.pp_output_data) !== $signed(expected_stages[idx*3+2]))
                        $fatal(1,"Commit mismatch/duplicate %0d",idx);
                    seen[idx]=1'b1; commits=commits+1;
                end
                if(output_valid && output_ready) begin
                    if(output_index !== exports || output_data !== expected_output[exports]) $fatal(1,"Export mismatch %0d",exports);
                    exports=exports+1;
                end
            end
        end
    end
    task reset;
        begin
            @(negedge clk); rstn=0; checking=0; load_valid=0; start=0; export_start=0; random_stalls=0;
            commit_ready=1; output_ready=1; #1;
            if(parameters_ready || busy || output_valid || load_ready) $fatal(1,"Reset did not cancel immediately");
            repeat(3) @(negedge clk); rstn=1;
        end
    endtask
    task wait_boot;
        begin
            while(!parameters_ready) begin @(negedge clk); if(fault) $fatal(1,"Boot fault"); end
            if(parameter_count != 1676) $fatal(1,"Incomplete boot count %0d",parameter_count);
            $display("BOOT_PASS cycles=%0d writes=%0d",dut.pref_cycles,parameter_count);
        end
    endtask
    task fixture;
        input integer which;
        begin
            if(which==0) $sformat(path,"%0s/interior",vectors);
            else if(which==1) $sformat(path,"%0s/edge",vectors);
            else $sformat(path,"%0s/bottom_right",vectors);
            $readmemh({path,"_halo.hex"},halo);
            $readmemh({path,"_output.hex"},expected_output);
            $readmemh({path,"_dw_acc.hex"},expected_acc,0,255);
            $readmemh({path,"_pw_acc.hex"},expected_acc,256,639);
            $readmemh({path,"_stages.hex"},expected_stages);
            for(i=0;i<1296;i=i+1) begin
                @(negedge clk); load_valid=1; load_addr=i; load_data=halo[i];
                while(!load_ready) @(negedge clk);
                if(random_stalls && (i%7==0)) begin @(negedge clk); load_valid=0; repeat(2) @(negedge clk); end
            end
            @(negedge clk);load_valid=0;
        end
    endtask
    task run_tile;
        begin
            accs=0;pres=0;silus=0;posts=0;commits=0;exports=0;seen=640'd0;observed_core=0;
            for(j=0;j<6;j=j+1) bins[j]=0;
            checking=1;
            @(negedge clk);start=1;@(negedge clk);start=0;
            while(!done) @(negedge clk);
            if(accs!=640 || pres!=640 || silus!=640 || posts!=640 || commits!=640 || !(&seen))
                $fatal(1,"Incomplete intermediate comparison");
            if(observed_core !== dut.runner_core_cycles) $fatal(1,"Cycle window mismatch");
            @(negedge clk);export_start=1;@(negedge clk);export_start=0;
            while(!export_done) @(negedge clk);
            if(exports!=384) $fatal(1,"Incomplete export");
            $fwrite(report,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",case_id,dut.pref_cycles,
                observed_core,dut.runner_export_cycles,bins[0],bins[1],bins[2],bins[3],bins[4],bins[5]);
            $display("ROM_DOWN2_PASS case=%0d core=%0d export=%0d",case_id,observed_core,dut.runner_export_cycles);
            checking=0;
        end
    endtask
    initial begin
        o_test_done=0;
        if(!$value$plusargs("VECTORS=%s",vectors) || !$value$plusargs("REPORT=%s",report_path)) $fatal(1,"Missing paths");
        $readmemh({vectors,"/table.hex"},expected_table);$readmemh({vectors,"/kind.hex"},expected_kind);
        $readmemh({vectors,"/address.hex"},expected_address);$readmemh({vectors,"/data.hex"},expected_data);
        report=$fopen(report_path,"w");
        $fwrite(report,"case,boot,core,export,commit_stall,capacity_stall,commit,mac_issue,issue_wait,drain_other\n");
        reset; repeat(80) @(negedge clk);start=1;repeat(4) @(negedge clk);start=0;
        if(busy || parameters_ready) $fatal(1,"Early start accepted");
        reset;
        while(parameter_count<800) @(negedge clk);
        reset; wait_boot;
        // Parameters complete alone must not permit computation without a full halo.
        @(negedge clk);start=1;@(negedge clk);start=0;
        if(busy) $fatal(1,"Missing halo accepted");
        for(case_id=0;case_id<6;case_id=case_id+1) begin
            random_stalls=case_id>=3; fixture(case_id%3); run_tile;
            random_stalls=0;commit_ready=1;output_ready=1;
        end
        fixture(0);commit_ready=0;
        @(negedge clk);start=1;@(negedge clk);start=0;repeat(160) @(negedge clk);
        reset;wait_boot;
        repeat(30) @(negedge clk);
        if(output_valid || done || `RUN.cnt_pw_meta!=0 || `PP.reg_meta_count!=0) $fatal(1,"Old result leaked after reset");
        case_id=6;fixture(0);run_tile;
        @(negedge clk);load_valid=1;load_addr=1296;load_data=8'sd1;
        @(negedge clk);load_valid=0;
        if(!fault || load_ready || parameters_ready) $fatal(1,"Invalid halo address not rejected");
        $fclose(report);o_test_done=1;$display("TB_PASS_ROM_DOWN2 tiles=7 resets=boot_table_busy invalid_address=checked");$finish;
    end
    initial begin #50000000; $fatal(1,"Timeout"); end
endmodule
`undef RUN
`undef PP
