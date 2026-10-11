`timescale 1ns / 1ps

module tb_down2_dynamic_overlap;
    reg clk=0; always #5 clk=~clk;
    reg rstn=0,table_valid=0,load_valid=0,start=0,commit_ready=1;
    reg export_start=0,output_ready=1;
    reg [9:0]table_addr=0;
    reg signed [15:0]table_data=0;
    reg [2:0]load_kind=0;
    reg [10:0]load_addr=0;
    reg signed [31:0]load_data=0;
    wire table_ready,table_loaded,load_ready,busy,done,fault;
    wire output_valid,export_done;
    wire signed [7:0]output_data;
    wire [8:0]output_index;
    wire [31:0]core_cycles,preload_writes,export_cycles;
    wire [31:0]pre_cycles,silu_cycles,post_cycles;
    wire [31:0]pre_accept_count,silu_accept_count,post_accept_count,writeback_count;
    reg [15:0]table_mem[0:1023];
    reg [7:0]halo[0:1295],dw_weight[0:143],pw_weight[0:383],expected_out[0:383];
    reg [31:0]dw_bias[0:15],pw_bias[0:23],expected_acc[0:639],expected_commit[0:639];
    reg [31:0]expected_stages[0:1919];
    reg [639:0]seen;
    reg checking=0,random_stalls=0;
    reg [15:0]random_bits=16'hace1;
    reg previous_valid=0,previous_ready=0;
    reg [15:0]previous_tag;
    reg [7:0]previous_data;
    reg [4095:0]vector_dir,report_path,file_path;
    integer ticks=0,start_tick,cycles_seen=0,commits=0,accs=0;
    integer pres=0,silus=0,posts=0,exports=0;
    integer bins[0:7];
    integer dw_ticks,pw_ticks,dw_groups,pw_groups,dw_batches,pw_batches,bin_total;
    integer pre_busy_seen,silu_busy_seen,post_busy_seen,active_overlap;
    integer ingress_highwater,retire_highwater,silu_highwater,capacity_stalls;
    integer i,j,c,idx,lane,ch,position,layer,category;
    integer report;

    down2_dynamic_tile_runner dut(
        .i_clk(clk),.i_rstn(rstn),.i_table_valid(table_valid),.i_table_addr(table_addr),
        .i_table_data(table_data),.o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .o_table_fault(),.i_load_valid(load_valid),.i_load_kind(load_kind),
        .i_load_addr(load_addr),.i_load_data(load_data),.o_load_ready(load_ready),
        .i_start(start),.i_pw_only(1'b0),.i_commit_ready(commit_ready),
        .o_busy(busy),.o_done(done),.o_fault(fault),.i_export_start(export_start),
        .i_output_ready(output_ready),.o_output_valid(output_valid),
        .o_output_data(output_data),.o_output_index(output_index),.o_export_done(export_done),
        .o_debug_valid(),.o_debug_phase(),.o_debug_layer(),.o_debug_position(),
        .o_debug_channel(),.o_debug_value(),.o_preload_writes(preload_writes),
        .o_core_cycles(core_cycles),.o_mac_cycles(),.o_pre_cycles(pre_cycles),
        .o_silu_cycles(silu_cycles),.o_post_cycles(post_cycles),.o_writeback_cycles(),
        .o_storage_wait_cycles(),.o_scheduler_idle_cycles(),.o_export_cycles(export_cycles),
        .o_result_queue_count(),.o_result_reserved(),.o_meta_count(),.o_mac_result_count(),
        .o_pre_accept_count(pre_accept_count),.o_silu_accept_count(silu_accept_count),
        .o_post_accept_count(post_accept_count),.o_writeback_count(writeback_count)
    );

    task resolve_stage_index;
        input [15:0]internal_tag;
        output integer resolved_index;
        reg [47:0]tags;
        reg [15:0]external_tag;
        integer slot_value,lane_value,layer_value,position_value,channel_value;
        begin
            if(internal_tag[15:5]!==11'd0 || internal_tag[1:0]>2)
                $fatal(1,"Invalid internal stage identity %h",internal_tag);
            slot_value=internal_tag[4:2]; lane_value=internal_tag[1:0];
            tags=dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_tags[slot_value];
            external_tag=(tags >> (lane_value*16));
            layer_value=external_tag[15];position_value=external_tag[14:11];
            channel_value=external_tag[10:6];
            resolved_index=layer_value ? 256+position_value*24+channel_value :
                                         position_value*16+channel_value;
            if(resolved_index<0 || resolved_index>639)
                $fatal(1,"Invalid resolved stage identity %h",external_tag);
        end
    endtask

    always @(negedge clk) begin
        if(random_stalls) begin
            random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
            commit_ready=(ticks%257>=48) && random_bits[0];
            output_ready=random_bits[1];
        end
    end

    always @(posedge clk) begin
        ticks=ticks+1;
        if(!rstn) begin
            previous_valid=0;
        end else if(checking) begin
            if(fault) $fatal(1,"Unexpected fault");
            if(previous_valid && !previous_ready &&
               (!dut.pp_output_valid || dut.pp_output_tag!==previous_tag ||
                dut.pp_output_data!==previous_data))
                $fatal(1,"Commit payload changed under backpressure");
            previous_valid=dut.pp_output_valid;
            previous_ready=commit_ready && busy;
            previous_tag=dut.pp_output_tag; previous_data=dut.pp_output_data;
            if(dut.flag_start_accept) start_tick=ticks;

            if(busy) begin
                cycles_seen=cycles_seen+1;
                if(dut.pp_pre_busy) pre_busy_seen=pre_busy_seen+1;
                if(dut.pp_silu_busy) silu_busy_seen=silu_busy_seen+1;
                if(dut.pp_post_busy) post_busy_seen=post_busy_seen+1;
                if((dut.pp_pre_busy && dut.pp_silu_busy) ||
                   (dut.pp_pre_busy && dut.pp_post_busy) ||
                   (dut.pp_silu_busy && dut.pp_post_busy)) active_overlap=active_overlap+1;
                if(dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count>ingress_highwater)
                    ingress_highwater=dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count;
                if(dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count>retire_highwater)
                    retire_highwater=dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count;
                if(dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count>silu_highwater)
                    silu_highwater=dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count;

                if(dut.pp_output_valid && !commit_ready) category=0;
                else if(((dut.state_current==4'd2) && (dut.cnt_mac_group==0) &&
                         !dut.flag_can_reserve) ||
                        (dut.flag_pp_input_valid && !dut.pp_input_ready)) category=1;
                else if(dut.flag_commit_accept) category=2;
                else if(dut.flag_mac_input_accept) category=3;
                else if(dut.state_current==4'd1 || dut.state_current==4'd2) category=4;
                else if(dut.state_current==4'd3 || dut.state_current==4'd9) category=5;
                else if(dut.state_current==4'd4 || dut.state_current==4'd5) category=6;
                else category=7;
                bins[category]=bins[category]+1;
                if(category==1) capacity_stalls=capacity_stalls+1;
                if(dut.flag_layer_pw) pw_ticks=pw_ticks+1; else dw_ticks=dw_ticks+1;
            end

            if(dut.flag_mac_input_accept) begin
                if(dut.flag_layer_pw) pw_groups=pw_groups+1; else dw_groups=dw_groups+1;
            end
            if(dut.flag_pp_input_accept) begin
                if(dut.flag_layer_pw) pw_batches=pw_batches+1; else dw_batches=dw_batches+1;
                for(lane=0;lane<3;lane=lane+1) if(dut.wire_result_lane_mask[lane]) begin
                    layer=dut.flag_layer_pw;position=dut.wire_pp_position;
                    ch=dut.wire_result_channel_base+lane;
                    idx=layer ? 256+position*24+ch : position*16+ch;
                    if($signed(dut.wire_pp_result_data[lane*32+:32])!==$signed(expected_acc[idx]))
                        $fatal(1,"MAC mismatch idx=%0d",idx);
                    accs=accs+1;
                end
            end
            if(dut.road_postprocess_stream_Inst_tile.u_chain.flag_silu_accept) begin
                resolve_stage_index(dut.road_postprocess_stream_Inst_tile.u_chain.pre_result_tag,idx);
                if($signed(dut.road_postprocess_stream_Inst_tile.u_chain.pre_result_data)!==
                   $signed(expected_stages[idx*3])) $fatal(1,"Pre mismatch idx=%0d",idx);
                pres=pres+1;
            end
            if(dut.road_postprocess_stream_Inst_tile.u_chain.flag_post_accept) begin
                resolve_stage_index(
                    dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_tags[
                        dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_read],idx);
                if($signed(dut.road_postprocess_stream_Inst_tile.u_chain.silu_output_data)!==
                   $signed(expected_stages[idx*3+1])) $fatal(1,"SiLU mismatch idx=%0d",idx);
                silus=silus+1;
            end
            if(dut.road_postprocess_stream_Inst_tile.u_chain.flag_post_complete) begin
                resolve_stage_index(dut.road_postprocess_stream_Inst_tile.u_chain.post_result_tag,idx);
                if($signed(dut.road_postprocess_stream_Inst_tile.u_chain.post_result_data)!==
                   $signed(expected_stages[idx*3+2])) $fatal(1,"Post mismatch idx=%0d",idx);
                posts=posts+1;
            end
            if(dut.flag_commit_accept) begin
                layer=dut.pp_output_tag[15];position=dut.pp_output_tag[14:11];
                ch=dut.pp_output_tag[10:6];idx=layer ? 256+position*24+ch : position*16+ch;
                if(idx<0 || idx>639 || seen[idx]) $fatal(1,"Duplicate/invalid commit");
                if($signed(dut.pp_output_data)!==$signed(expected_commit[idx]))
                    $fatal(1,"Commit mismatch idx=%0d",idx);
                seen[idx]=1'b1; commits=commits+1;
            end
        end
        if(ticks>2000000) $fatal(1,"Timeout");
    end

    task reset;
        begin
            checking=0;random_stalls=0;commit_ready=1;output_ready=1;
            @(negedge clk);rstn=0;table_valid=0;load_valid=0;start=0;export_start=0;
            #1;
            if(output_valid || busy || table_loaded || dut.pp_output_valid ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count!=0)
                $fatal(1,"Reset leaked transaction");
            repeat(3) @(negedge clk);rstn=1;
        end
    endtask

    task load_table;
        begin
            for(i=0;i<1024;i=i+1) begin
                @(negedge clk);table_valid=1;table_addr=i;table_data=table_mem[i];
                if(!table_ready) $fatal(1,"Table not ready");
                if(i<1023 && table_loaded) $fatal(1,"Partial table published");
            end
            @(negedge clk);table_valid=0;
            if(!table_loaded) $fatal(1,"Full table not loaded");
        end
    endtask

    task load_value;
        input [2:0]kind;input integer addr;input [31:0]value;
        begin
            @(negedge clk);load_valid=1;load_kind=kind;load_addr=addr;load_data=value;
            if(!load_ready) $fatal(1,"Preload blocked");
        end
    endtask

    task load_fixture;
        begin
            for(j=0;j<1296;j=j+1) load_value(3'd0,j,{{24{halo[j][7]}},halo[j]});
            for(j=0;j<144;j=j+1) load_value(3'd2,j,{{24{dw_weight[j][7]}},dw_weight[j]});
            for(j=0;j<16;j=j+1) load_value(3'd3,j,dw_bias[j]);
            for(j=0;j<384;j=j+1) load_value(3'd4,j,{{24{pw_weight[j][7]}},pw_weight[j]});
            for(j=0;j<24;j=j+1) load_value(3'd5,j,pw_bias[j]);
            @(negedge clk);load_valid=0;
            if(preload_writes!=1864) $fatal(1,"Preload count mismatch");
        end
    endtask

    task load_case_vectors;
        input integer case_index;
        begin
            if(case_index==0) begin
                $sformat(file_path,"%0s/edge_halo.hex",vector_dir);$readmemh(file_path,halo);
                $sformat(file_path,"%0s/edge_output.hex",vector_dir);$readmemh(file_path,expected_out);
                $sformat(file_path,"%0s/edge_acc.hex",vector_dir);$readmemh(file_path,expected_acc);
                $sformat(file_path,"%0s/edge_commit.hex",vector_dir);$readmemh(file_path,expected_commit);
                $sformat(file_path,"%0s/edge_stages.hex",vector_dir);$readmemh(file_path,expected_stages);
            end else if(case_index==1) begin
                $sformat(file_path,"%0s/interior_halo.hex",vector_dir);$readmemh(file_path,halo);
                $sformat(file_path,"%0s/interior_output.hex",vector_dir);$readmemh(file_path,expected_out);
                $sformat(file_path,"%0s/interior_acc.hex",vector_dir);$readmemh(file_path,expected_acc);
                $sformat(file_path,"%0s/interior_commit.hex",vector_dir);$readmemh(file_path,expected_commit);
                $sformat(file_path,"%0s/interior_stages.hex",vector_dir);$readmemh(file_path,expected_stages);
            end else begin
                $sformat(file_path,"%0s/bottom_right_halo.hex",vector_dir);$readmemh(file_path,halo);
                $sformat(file_path,"%0s/bottom_right_output.hex",vector_dir);$readmemh(file_path,expected_out);
                $sformat(file_path,"%0s/bottom_right_acc.hex",vector_dir);$readmemh(file_path,expected_acc);
                $sformat(file_path,"%0s/bottom_right_commit.hex",vector_dir);$readmemh(file_path,expected_commit);
                $sformat(file_path,"%0s/bottom_right_stages.hex",vector_dir);$readmemh(file_path,expected_stages);
            end
        end
    endtask

    task run_case;
        begin
            seen=0;commits=0;accs=0;pres=0;silus=0;posts=0;exports=0;
            cycles_seen=0;previous_valid=0;dw_ticks=0;pw_ticks=0;
            dw_groups=0;pw_groups=0;dw_batches=0;pw_batches=0;
            pre_busy_seen=0;silu_busy_seen=0;post_busy_seen=0;active_overlap=0;
            ingress_highwater=0;retire_highwater=0;silu_highwater=0;capacity_stalls=0;
            for(j=0;j<8;j=j+1) bins[j]=0;
            checking=1;
            @(negedge clk);start=1;@(negedge clk);start=0;
            while(!done) @(negedge clk);
            if(accs!=640 || pres!=640 || silus!=640 || posts!=640 || commits!=640 || !(&seen))
                $fatal(1,"Missing values acc=%0d pre=%0d silu=%0d post=%0d commit=%0d",
                       accs,pres,silus,posts,commits);
            if(pre_accept_count!=640 || silu_accept_count!=640 ||
               post_accept_count!=640 || writeback_count!=640)
                $fatal(1,"Runner stage counter mismatch");
            if(core_cycles!=cycles_seen || ticks-start_tick!=cycles_seen)
                $fatal(1,"Cycle window differs");
            if(dw_ticks+pw_ticks!=core_cycles || dw_groups!=320 || pw_groups!=256 ||
               dw_batches!=256 || pw_batches!=128) $fatal(1,"Task accounting mismatch");
            if(pre_busy_seen!=pre_cycles || silu_busy_seen!=silu_cycles ||
               post_busy_seen!=post_cycles) $fatal(1,"Activity counter mismatch");
            bin_total=0;for(j=0;j<8;j=j+1) bin_total=bin_total+bins[j];
            if(bin_total!=core_cycles) $fatal(1,"Endpoint bins do not close");
            if(active_overlap==0 || retire_highwater<2)
                $fatal(1,"No measurable postprocess overlap");
            if(dut.flag_result_reserved ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count!=0)
                $fatal(1,"Queue not empty at done");
            checking=0;
            @(negedge clk);export_start=1;@(negedge clk);export_start=0;
            while(!export_done) begin
                @(posedge clk);
                if(output_valid && output_ready) begin
                    if(output_index!==exports || output_data!==expected_out[exports])
                        $fatal(1,"Export mismatch idx=%0d",exports);
                    exports=exports+1;
                end
                @(negedge clk);
            end
            if(exports!=384) $fatal(1,"Missing export");
            $fwrite(report,"%0d,%0d",c,core_cycles);
            for(j=0;j<8;j=j+1) $fwrite(report,",%0d",bins[j]);
            $fwrite(report,",%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                    pre_busy_seen,silu_busy_seen,post_busy_seen,active_overlap,
                    ingress_highwater,retire_highwater,silu_highwater,capacity_stalls,
                    accs,pres,silus,posts,commits,exports,dw_groups,pw_groups,dw_batches,pw_batches);
            $fwrite(report,",%0d,%0d,1024,%0d,%0d\n",
                    dw_ticks,pw_ticks,preload_writes,export_cycles);
            $display("LAYER_OVERLAP_PASS case=%0d endpoint=%0d highwater=%0d/%0d/%0d overlap=%0d stalls=%0d",
                     c,core_cycles,ingress_highwater,retire_highwater,silu_highwater,
                     active_overlap,capacity_stalls);
        end
    endtask

    initial begin
        if(!$value$plusargs("VECTORS=%s",vector_dir)) $fatal(1,"Missing VECTORS plusarg");
        if(!$value$plusargs("REPORT=%s",report_path)) $fatal(1,"Missing REPORT plusarg");
        report=$fopen(report_path,"w");
        if(report==0) $fatal(1,"Cannot open report");
        $fwrite(report,"case,endpoint,writeback_stall,capacity_wait,commit_cycle,mac_issue,input_wait,task_close,drain,other,pre_busy,silu_busy,post_busy,active_overlap,ingress_highwater,retire_highwater,silu_highwater,capacity_stall,acc,pre,silu,post,commit,export,dw_groups,pw_groups,dw_batches,pw_batches,dw_endpoint,pw_endpoint,table_writes,preload_writes,export_cycles\n");
        $sformat(file_path,"%0s/silu.hex",vector_dir);$readmemh(file_path,table_mem);
        $sformat(file_path,"%0s/dw_weights.hex",vector_dir);$readmemh(file_path,dw_weight);
        $sformat(file_path,"%0s/dw_biases.hex",vector_dir);$readmemh(file_path,dw_bias);
        $sformat(file_path,"%0s/pw_weights.hex",vector_dir);$readmemh(file_path,pw_weight);
        $sformat(file_path,"%0s/pw_biases.hex",vector_dir);$readmemh(file_path,pw_bias);
        for(c=0;c<6;c=c+1) begin
            load_case_vectors(c%3);reset;load_table;
            @(negedge clk);start=1;@(negedge clk);start=0;
            if(busy) $fatal(1,"Partial preload started");
            load_fixture;random_stalls=(c>=3);run_case;
        end
        load_case_vectors(2);reset;load_table;load_fixture;
        commit_ready=0;@(negedge clk);start=1;@(negedge clk);start=0;
        while(!dut.pp_output_valid) @(negedge clk);
        repeat(32) @(negedge clk);reset;
        repeat(30) begin
            @(negedge clk);
            if(output_valid || dut.pp_output_valid || busy || table_loaded ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count!=0)
                $fatal(1,"Old transaction after reset");
        end
        load_table;load_fixture;c=6;run_case;
        $fclose(report);
        $display("TB_PASS_DOWN2_DYNAMIC_OVERLAP cases=7 reset_stall=1 full_reload=1 queue_empty_done=1");
        $finish;
    end
endmodule
