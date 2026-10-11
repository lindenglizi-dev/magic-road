`timescale 1ns / 1ps

module tb_down2_dynamic_overlap();
    reg clk=0; always #5 clk=~clk;
    reg rstn=0,table_valid=0,load_valid=0,start=0,commit_ready=1;
    reg export_start=0,output_ready=1,pw_only=0;
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
    reg [31:0]multipliers[0:39],controls[0:43];
    reg [639:0]seen;
    reg checking=0,checking_dw_fault=0,dw_fault_allow_older=0;
    reg immediate_start=0;
    reg random_stalls=0,pw_long_stall=0,dw_long_stall=0;
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
    integer i,j,c,idx,lane,ch,position,layer,category,checkpoint;
    integer report;
    // Observation only: sample beside the original scoreboard, before DUT NBA updates.
    integer trace;
    reg [4095:0]trace_path;
    integer windows;
    reg [4095:0]windows_path;
    integer table_accepted=0,load_accepted=0,export_accepted=0;
    integer table_first,table_last,load_first,load_last,export_samples=0;
    integer pw_state_ticks[0:9];
    integer pw_no_result,pw_result_blocked,pw_firsts,last_first_tick,first_gap_min,first_gap_max,first_gap_sum;
    reg previous_mac_valid=0,previous_mac_ready=0;
    reg [361:0]previous_mac_payload;
    reg previous_dw_active_wait=0,previous_dw_pp_wait=0,previous_dw_result_accept=0;
    reg [8:0]previous_dw_active_meta,previous_dw_result_meta;
    reg [1:0]previous_dw_active_lane;
    reg [95:0]previous_dw_active_result;
    reg [113:0]previous_dw_pp_payload;
    integer dw_meta_highwater,dw_first_result_pop_same,dw_active_replace,dw_post_blocked;
    integer dw_firsts,dw_lasts,dw_results,dw_active_posts;
    integer dw_fault_firsts,dw_fault_pp_accepts,dw_fault_commits,dw_fault_pops;
    integer dw_fault_conflict_seen,dw_fault_held_meta,dw_fault_writes_at_pop;
    integer dw_fault_commits_at_pop;

    down2_dynamic_tile_runner dut(
        .i_clk(clk),.i_rstn(rstn),.i_table_valid(table_valid),.i_table_addr(table_addr),
        .i_table_data(table_data),.o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .o_table_fault(),.i_load_valid(load_valid),.i_load_kind(load_kind),
        .i_load_addr(load_addr),.i_load_data(load_data),.o_load_ready(load_ready),
        .i_start(start),.i_pw_only(pw_only),.i_commit_ready(commit_ready),
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
            commit_ready=(cycles_seen%257>=48) && random_bits[0];
            output_ready=random_bits[1];
        end else if(pw_long_stall) begin
            commit_ready=!(dut.flag_layer_pw && pw_ticks>=8 && pw_ticks<264);
        end else if(dw_long_stall) begin
            commit_ready=!((!dut.flag_layer_pw) && dw_ticks>=8 && dw_ticks<264);
        end
    end

    always @(posedge clk) begin
        ticks=ticks+1;
        if(!rstn) begin
            previous_valid=0;
            previous_mac_valid=0;
            previous_dw_active_wait=0;
            previous_dw_pp_wait=0;
            previous_dw_result_accept=0;
            table_accepted=0;load_accepted=0;export_accepted=0;export_samples=0;
        end else begin
            if(table_valid && table_ready) begin
                if(table_accepted==0) table_first=ticks;
                table_last=ticks;table_accepted=table_accepted+1;
            end
            if(dut.flag_load_accept) begin
                if(load_accepted==0) load_first=ticks;
                load_last=ticks;load_accepted=load_accepted+1;
            end
            if(dut.state_current==4'd8) begin
                export_samples=export_samples+1;
                if(output_valid && output_ready) export_accepted=export_accepted+1;
            end
        end
        if(rstn && checking) begin
            if(fault) $fatal(1,"Unexpected fault");
            if(previous_valid && !previous_ready &&
               (!dut.pp_output_valid || dut.pp_output_tag!==previous_tag ||
                dut.pp_output_data!==previous_data))
                $fatal(1,"Commit payload changed under backpressure");
            previous_valid=dut.pp_output_valid;
            previous_ready=commit_ready && busy;
            previous_tag=dut.pp_output_tag; previous_data=dut.pp_output_data;
            if(previous_mac_valid && !previous_mac_ready &&
               (!dut.flag_mac_input_valid || previous_mac_payload!==
                {dut.reg_mac_activation,dut.reg_mac_weight,dut.reg_mac_bias,dut.reg_mac_mask,
                 (dut.cnt_mac_group==0),dut.flag_mac_last_group}))
                $fatal(1,"MAC input changed before handshake");
            previous_mac_valid=dut.flag_mac_input_valid;previous_mac_ready=dut.mac_input_ready;
            previous_mac_payload={dut.reg_mac_activation,dut.reg_mac_weight,dut.reg_mac_bias,dut.reg_mac_mask,
                                  (dut.cnt_mac_group==0),dut.flag_mac_last_group};
            if(previous_dw_active_wait &&
               (!dut.flag_result_reserved || dut.reg_dw_active_meta!==previous_dw_active_meta ||
                dut.cnt_dw_post_lane!==previous_dw_active_lane ||
                dut.reg_dw_triplet_result!==previous_dw_active_result))
                $fatal(1,"DW active ownership changed while waiting");
            if(previous_dw_pp_wait &&
               (!dut.flag_pp_input_valid ||
                {dut.wire_pp_result_data,dut.wire_result_lane_mask,dut.wire_pp_position,
                 dut.wire_result_channel_base,dut.wire_parameter_base}!==previous_dw_pp_payload))
                $fatal(1,"DW postprocess payload changed under backpressure");
            if(previous_dw_result_accept &&
               (!dut.flag_result_reserved || dut.reg_dw_active_meta!==previous_dw_result_meta))
                $fatal(1,"DW result and descriptor identity diverged");
            previous_dw_active_wait=(!dut.flag_layer_pw) && dut.flag_result_reserved &&
                                    !dut.flag_dw_post_accept;
            previous_dw_active_meta=dut.reg_dw_active_meta;
            previous_dw_active_lane=dut.cnt_dw_post_lane;
            previous_dw_active_result=dut.reg_dw_triplet_result;
            previous_dw_pp_wait=(!dut.flag_layer_pw) && dut.flag_pp_input_valid &&
                                !dut.pp_input_ready;
            previous_dw_pp_payload={dut.wire_pp_result_data,dut.wire_result_lane_mask,
                                    dut.wire_pp_position,dut.wire_result_channel_base,
                                    dut.wire_parameter_base};
            previous_dw_result_accept=(!dut.flag_layer_pw) && dut.flag_dw_result_accept;
            previous_dw_result_meta=dut.reg_pw_task_meta[dut.ptr_pw_meta_read];
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
                if(!dut.flag_layer_pw) begin
                    if(dut.cnt_pw_meta!==dut.road_mac_probe_Inst_tile.cnt_reserved)
                        $fatal(1,"DW descriptor/MAC credit mismatch meta=%0d mac=%0d",
                               dut.cnt_pw_meta,dut.road_mac_probe_Inst_tile.cnt_reserved);
                    if(dut.cnt_pw_meta>3'd4) $fatal(1,"DW credit exceeded four");
                    if(dut.cnt_pw_meta>dw_meta_highwater) dw_meta_highwater=dut.cnt_pw_meta;
                    if(dut.flag_shared_meta_push!==dut.flag_dw_first_accept)
                        $fatal(1,"DW descriptor push did not match accepted first");
                    if(dut.flag_shared_meta_pop!==dut.flag_dw_result_accept)
                        $fatal(1,"DW descriptor pop did not match accepted result");
                    if(dut.flag_dw_first_accept) dw_firsts=dw_firsts+1;
                    if(dut.flag_dw_last_accept) dw_lasts=dw_lasts+1;
                    if(dut.flag_dw_result_accept) dw_results=dw_results+1;
                    if(dut.flag_dw_post_accept) dw_active_posts=dw_active_posts+1;
                    if(dut.flag_dw_first_accept && dut.flag_dw_result_accept)
                        dw_first_result_pop_same=dw_first_result_pop_same+1;
                    if(dut.flag_dw_active_last_accept && dut.flag_dw_result_accept)
                        dw_active_replace=dw_active_replace+1;
                    if(dut.flag_result_reserved && !dut.flag_dw_post_accept &&
                       ((dut.pp_result_queue_count>=2) || !dut.pp_input_ready))
                        dw_post_blocked=dw_post_blocked+1;
                end

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
                $fwrite(trace,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                    c,cycles_seen,dut.flag_layer_pw,dut.state_current,dut.cnt_position,
                    dut.cnt_output,dut.cnt_mac_group,dut.cnt_dw_post_lane,
                    dut.wire_dw_post_count,dut.flag_can_reserve);
                $fwrite(trace,",%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                    dut.flag_mac_input_valid,dut.mac_input_ready,dut.flag_mac_input_accept,
                    dut.flag_mac_last_group,dut.mac_result_valid,dut.flag_mac_result_accept,
                    dut.flag_mac_result_ready_local,dut.road_mac_probe_Inst_tile.cnt_reserved,
                    dut.road_mac_probe_Inst_tile.cnt_result_count);
                $fwrite(trace,",%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                    dut.flag_pp_input_valid,dut.pp_input_ready,dut.flag_pp_input_accept,
                    dut.wire_result_lane_mask,dut.wire_pp_position,dut.wire_result_channel_base,
                    dut.pp_output_valid,commit_ready,dut.flag_commit_accept,dut.pp_output_tag);
                $fwrite(trace,",%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                    dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count,
                    dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count,
                    dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count,
                    dut.pp_pre_accept,dut.pp_silu_accept,dut.pp_post_accept,
                    dut.road_postprocess_stream_Inst_tile.u_chain.flag_post_complete,
                    dut.pp_pre_busy,dut.pp_silu_busy,dut.pp_post_busy,
                    dut.cnt_dw_writes,dut.cnt_pw_writes,category);
                $fwrite(trace,",%0d,%0d\n",dut.flag_result_reserved,dut.cnt_pw_meta);
                if(dut.flag_layer_pw) begin
                    pw_ticks=pw_ticks+1;
                    pw_state_ticks[dut.state_current]=pw_state_ticks[dut.state_current]+1;
                    if(dut.o_result_reserved) begin
                        if(!dut.mac_result_valid) pw_no_result=pw_no_result+1;
                        else if(!dut.flag_mac_result_accept) pw_result_blocked=pw_result_blocked+1;
                    end
                end else dw_ticks=dw_ticks+1;
            end

            if(dut.flag_mac_input_accept) begin
                if(dut.flag_layer_pw) pw_groups=pw_groups+1; else dw_groups=dw_groups+1;
                if(dut.flag_layer_pw && dut.cnt_mac_group==0) begin
                    if(pw_firsts>0) begin
                        if(ticks-last_first_tick<first_gap_min) first_gap_min=ticks-last_first_tick;
                        if(ticks-last_first_tick>first_gap_max) first_gap_max=ticks-last_first_tick;
                        first_gap_sum=first_gap_sum+ticks-last_first_tick;
                    end
                    last_first_tick=ticks;pw_firsts=pw_firsts+1;
                end
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
        if(rstn && checking_dw_fault) begin
            if(dut.flag_dw_first_accept) dw_fault_firsts=dw_fault_firsts+1;
            if(dut.flag_dw_fault_pop) begin
                dw_fault_pops=dw_fault_pops+1;
                if(dw_fault_allow_older) begin
                    if(!dut.flag_result_reserved || !dut.pp_output_valid || !commit_ready ||
                       dut.flag_dw_post_accept || dut.flag_commit_accept ||
                       dut.flag_dw_cache_commit_write)
                        $fatal(1,"DW fault conflict did not block active/PP publication atomically");
                    dw_fault_writes_at_pop=dut.cnt_dw_writes;
                    dw_fault_commits_at_pop=dw_fault_commits;
                    dw_fault_conflict_seen=dw_fault_conflict_seen+1;
                end
            end
            if((!dut.flag_layer_pw) && dut.flag_pp_input_accept) begin
                dw_fault_pp_accepts=dw_fault_pp_accepts+1;
                if(!dw_fault_allow_older || dw_fault_pops!=0)
                    $fatal(1,"Faulting or younger DW task entered postprocess");
            end
            if(dut.flag_commit_accept && !dut.pp_output_tag[15]) begin
                dw_fault_commits=dw_fault_commits+1;
                if(!dw_fault_allow_older || dw_fault_pops!=0)
                    $fatal(1,"Faulting or younger DW task was published");
            end
            if(dut.mac_result_valid && dut.mac_fault && dut.mac_result_data!==96'd0)
                $fatal(1,"DW fault result is not atomic zero");
        end
        if(ticks>2000000) $fatal(1,"Timeout");
    end

    task reset;
        begin
            checking=0;checking_dw_fault=0;dw_fault_allow_older=0;
            random_stalls=0;pw_long_stall=0;dw_long_stall=0;
            commit_ready=1;output_ready=1;pw_only=0;
            @(negedge clk);rstn=0;table_valid=0;load_valid=0;start=0;export_start=0;
            #1;
            if(output_valid || busy || table_loaded || dut.pp_output_valid ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_ingress_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count!=0 ||
               dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_count!=0 ||
               dut.flag_result_reserved || dut.cnt_pw_meta!=0 ||
               dut.road_mac_probe_Inst_tile.cnt_reserved!=0 ||
               dut.road_mac_probe_Inst_tile.cnt_result_count!=0)
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
            @(negedge clk);start=1;@(negedge clk);start=0;
            if(busy) $fatal(1,"Missing runtime parameters started");
            for(j=0;j<40;j=j+1) load_value(3'd6,j,multipliers[j]);
            @(negedge clk);load_valid=0;start=1;@(negedge clk);start=0;
            if(busy) $fatal(1,"Partial runtime parameters started");
            for(j=0;j<44;j=j+1) load_value(3'd7,j,controls[j]);
            @(negedge clk);load_valid=0;
            if(preload_writes!=1948) $fatal(1,"Runtime preload count mismatch");
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

    // Exercise the new registered memory boundary without forcing DUT state or operands.
    task weight_load_boundary;
        reg [7:0]saved_weight;
        begin
            reset;
            for(checkpoint=0;checkpoint<144;checkpoint=checkpoint+1)
                load_value(3'd2,checkpoint,checkpoint-72);
            @(negedge clk);load_valid=0;
            if(!dut.flag_dw_weight_write_pending || !dut.flag_dw_weight_loaded)
                $fatal(1,"Last DW load was not queued");
            @(negedge clk);
            for(checkpoint=0;checkpoint<144;checkpoint=checkpoint+1)
                if($signed(dut.reg_dw_weight[checkpoint])!==checkpoint-72)
                    $fatal(1,"Continuous DW load lost address/data %0d",checkpoint);
            // Restart at zero and bubbles preserve accepted order and delayed data.
            for(checkpoint=0;checkpoint<12;checkpoint=checkpoint+1) begin
                load_value(3'd2,checkpoint,120-checkpoint);
                @(negedge clk);load_valid=0;
                repeat(checkpoint%3) @(negedge clk);
            end
            @(negedge clk);
            for(checkpoint=0;checkpoint<12;checkpoint=checkpoint+1)
                if(dut.reg_dw_weight[checkpoint]!==120-checkpoint)
                    $fatal(1,"Bubble/restart DW load mismatch %0d",checkpoint);
            // Cancel between acceptance and RAM commit. Retained old data must not be overwritten.
            saved_weight=dut.reg_dw_weight[0];
            load_value(3'd2,0,32'd17);
            @(negedge clk);load_valid=0;rstn=0;#1;
            if(dut.flag_dw_weight_write_pending || dut.flag_dw_weight_loaded)
                $fatal(1,"Reset failed to cancel pending DW write");
            repeat(3) @(negedge clk);rstn=1;
            repeat(3) @(negedge clk);
            if(dut.reg_dw_weight[0]!==saved_weight)
                $fatal(1,"Canceled DW write leaked after reset");
            load_value(3'd2,1,32'd19);@(negedge clk);load_valid=0;
            if(!fault || dut.flag_dw_weight_write_pending)
                $fatal(1,"Out-of-order DW load queued a write");
            reset;
            load_value(3'd2,256,32'd19);@(negedge clk);load_valid=0;
            if(!fault || dut.flag_dw_weight_write_pending)
                $fatal(1,"High address was truncated before validation");
            // Full recovery: load DW weights last so the next edge is both commit and start.
            reset;load_table;
            for(j=0;j<1296;j=j+1) load_value(3'd0,j,{{24{halo[j][7]}},halo[j]});
            for(j=0;j<16;j=j+1) load_value(3'd3,j,dw_bias[j]);
            for(j=0;j<384;j=j+1) load_value(3'd4,j,{{24{pw_weight[j][7]}},pw_weight[j]});
            for(j=0;j<24;j=j+1) load_value(3'd5,j,pw_bias[j]);
            for(j=0;j<40;j=j+1) load_value(3'd6,j,multipliers[j]);
            for(j=0;j<44;j=j+1) load_value(3'd7,j,controls[j]);
            for(j=0;j<144;j=j+1) load_value(3'd2,j,{{24{dw_weight[j][7]}},dw_weight[j]});
            @(negedge clk);load_valid=0;immediate_start=1;
            if(!dut.flag_dw_weight_write_pending || !dut.flag_dw_weight_loaded)
                $fatal(1,"Immediate-start boundary was not covered");
            c=0;run_case;
            if(core_cycles!=1687) $fatal(1,"Write boundary increased core latency");
            $display("DW_LOAD_BOUNDARY_PASS continuous=144 bubbles=12 reset_pending=1 guards=2 immediate_start_golden=1");
        end
    endtask

    task run_case;
        begin
            seen=0;commits=0;accs=0;pres=0;silus=0;posts=0;exports=0;
            cycles_seen=0;previous_valid=0;dw_ticks=0;pw_ticks=0;
            dw_groups=0;pw_groups=0;dw_batches=0;pw_batches=0;
            pre_busy_seen=0;silu_busy_seen=0;post_busy_seen=0;active_overlap=0;
            ingress_highwater=0;retire_highwater=0;silu_highwater=0;capacity_stalls=0;
            pw_no_result=0;pw_result_blocked=0;pw_firsts=0;last_first_tick=0;
            first_gap_min=1000000;first_gap_max=0;first_gap_sum=0;
            random_bits=16'hace1;previous_mac_valid=0;
            previous_dw_active_wait=0;previous_dw_pp_wait=0;previous_dw_result_accept=0;
            dw_meta_highwater=0;dw_first_result_pop_same=0;dw_active_replace=0;dw_post_blocked=0;
            dw_firsts=0;dw_lasts=0;dw_results=0;dw_active_posts=0;
            for(j=0;j<8;j=j+1) bins[j]=0;
            for(j=0;j<10;j=j+1) pw_state_ticks[j]=0;
            checking=1;
            if(!immediate_start) @(negedge clk);
            start=1;immediate_start=0;@(negedge clk);start=0;
            while(!done) @(negedge clk);
            if(accs!=640 || pres!=640 || silus!=640 || posts!=640 || commits!=640 || !(&seen))
                $fatal(1,"Missing values acc=%0d pre=%0d silu=%0d post=%0d commit=%0d",
                       accs,pres,silus,posts,commits);
            if(pre_accept_count!=640 || silu_accept_count!=640 ||
               post_accept_count!=640 || writeback_count!=640)
                $fatal(1,"Runner stage counter mismatch");
            if(core_cycles!=cycles_seen || ticks-start_tick!=cycles_seen)
                $fatal(1,"Cycle window differs");
            if(dw_ticks+pw_ticks!=core_cycles || dw_groups!=384 || pw_groups!=256 ||
               dw_batches!=256 || pw_batches!=128) $fatal(1,"Task accounting mismatch");
            if(dw_firsts!=128 || dw_lasts!=128 || dw_results!=128 || dw_active_posts!=256)
                $fatal(1,"DW ownership accounting mismatch first=%0d last=%0d result=%0d post=%0d",
                       dw_firsts,dw_lasts,dw_results,dw_active_posts);
            if(dw_meta_highwater!=4 || dw_first_result_pop_same==0 || dw_active_replace==0)
                $fatal(1,"DW overlap coverage missing highwater=%0d pushpop=%0d replace=%0d",
                       dw_meta_highwater,dw_first_result_pop_same,dw_active_replace);
            if(dw_long_stall && dw_post_blocked==0)
                $fatal(1,"DW long commit backpressure did not block active postprocess");
            if(pre_busy_seen!=pre_cycles || silu_busy_seen!=silu_cycles ||
               post_busy_seen!=post_cycles) $fatal(1,"Activity counter mismatch");
            bin_total=0;for(j=0;j<8;j=j+1) bin_total=bin_total+bins[j];
            if(bin_total!=core_cycles) $fatal(1,"Endpoint bins do not close");
            if(active_overlap==0 || retire_highwater<2)
                $fatal(1,"No measurable postprocess overlap");
            if(pw_long_stall && (retire_highwater!=8 || capacity_stalls==0))
                $fatal(1,"PW long stall did not fill result storage");
            if(dut.o_result_reserved || dut.flag_result_reserved || dut.cnt_pw_meta!=0 ||
               dut.road_mac_probe_Inst_tile.cnt_reserved!=0 ||
               dut.road_mac_probe_Inst_tile.cnt_result_count!=0 ||
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
            if(table_accepted!=1024 || load_accepted!=1948 || export_accepted!=384 ||
               export_samples!=export_cycles) $fatal(1,"Phase window accounting mismatch");
            $fwrite(windows,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",c,
                    table_accepted,table_last-table_first+1,load_accepted,load_last-load_first+1,
                    core_cycles,export_accepted,export_samples);
            $fwrite(report,"%0d,%0d",c,core_cycles);
            for(j=0;j<8;j=j+1) $fwrite(report,",%0d",bins[j]);
            $fwrite(report,",%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                    pre_busy_seen,silu_busy_seen,post_busy_seen,active_overlap,
                    ingress_highwater,retire_highwater,silu_highwater,capacity_stalls,
                    accs,pres,silus,posts,commits,exports,dw_groups,pw_groups,dw_batches,pw_batches);
            $fwrite(report,",%0d,%0d,1024,%0d,%0d",
                    dw_ticks,pw_ticks,preload_writes,export_cycles);
            for(j=0;j<10;j=j+1) $fwrite(report,",%0d",pw_state_ticks[j]);
            $fwrite(report,",%0d,%0d,%0d,%0d,%0d,%0d\n",pw_no_result,pw_result_blocked,
                    pw_firsts,first_gap_min,first_gap_max,first_gap_sum);
            $display("LAYER_OVERLAP_PASS case=%0d endpoint=%0d highwater=%0d/%0d/%0d overlap=%0d stalls=%0d",
                     c,core_cycles,ingress_highwater,retire_highwater,silu_highwater,
                     active_overlap,capacity_stalls);
        end
    endtask

    task reset_recovery_case;
        input integer checkpoint;
        begin
            reset;load_table;load_fixture;
            if(checkpoint==3) commit_ready=0;
            @(negedge clk);start=1;@(negedge clk);start=0;
            case(checkpoint)
                0: while(!((!dut.flag_layer_pw) && dut.flag_mac_input_valid &&
                          (dut.cnt_mac_group==0))) @(negedge clk);
                1: while(!((!dut.flag_layer_pw) && dut.flag_mac_input_valid &&
                          dut.flag_mac_last_group)) @(negedge clk);
                2: while(!((!dut.flag_layer_pw) && dut.flag_result_reserved)) @(negedge clk);
                3: while(!((!dut.flag_layer_pw) && dut.flag_result_reserved &&
                          !dut.flag_dw_post_accept &&
                          ((dut.pp_result_queue_count>=2) || !dut.pp_input_ready))) @(negedge clk);
                4: while(!((!dut.flag_layer_pw) && (dut.cnt_pw_meta==3'd4))) @(negedge clk);
                default: $fatal(1,"Invalid reset checkpoint");
            endcase
            rstn=0;#1;
            if(busy || output_valid || dut.pp_output_valid || dut.flag_result_reserved ||
               dut.cnt_pw_meta!=0 || dut.road_mac_probe_Inst_tile.cnt_reserved!=0 ||
               dut.road_mac_probe_Inst_tile.cnt_result_count!=0)
                $fatal(1,"DW overlap reset did not cancel immediately checkpoint=%0d",checkpoint);
            reset;load_table;load_fixture;c=10+checkpoint;run_case;
        end
    endtask

    initial begin
        if(!$value$plusargs("VECTORS=%s",vector_dir)) $fatal(1,"Missing VECTORS plusarg");
        if(!$value$plusargs("REPORT=%s",report_path)) $fatal(1,"Missing REPORT plusarg");
        if(!$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"Missing TRACE plusarg");
        if(!$value$plusargs("WINDOWS=%s",windows_path)) $fatal(1,"Missing WINDOWS plusarg");
        windows=$fopen(windows_path,"w");
        if(windows==0) $fatal(1,"Cannot open windows");
        $fwrite(windows,"case,table_accepted,table_span,load_accepted,load_span,core,export_accepted,export_span\n");
        trace=$fopen(trace_path,"w");
        if(trace==0) $fatal(1,"Cannot open trace");
        $fwrite(trace,"case,cycle,layer,state,position,channel,group,post_lane,post_count,can_reserve,mac_valid,mac_ready,mac_accept,mac_last,mac_result_valid,mac_result_accept,mac_result_ready,mac_reserved,mac_queued,pp_valid,pp_ready,pp_accept,pp_mask,pp_position,pp_channel,commit_valid,commit_ready,commit_accept,commit_tag,ingress,retire,meta,pre_accept,silu_accept,post_accept,post_complete,pre_busy,silu_busy,post_busy,dw_writes,pw_writes,legacy_category,active_valid,task_meta_count\n");
        report=$fopen(report_path,"w");
        if(report==0) $fatal(1,"Cannot open report");
        $fwrite(report,"case,endpoint,writeback_stall,capacity_wait,commit_cycle,mac_issue,input_wait,task_close,drain,other,pre_busy,silu_busy,post_busy,active_overlap,ingress_highwater,retire_highwater,silu_highwater,capacity_stall,acc,pre,silu,post,commit,export,dw_groups,pw_groups,dw_batches,pw_batches,dw_endpoint,pw_endpoint,table_writes,preload_writes,export_cycles,pw_idle,pw_storage,pw_send,pw_wait,pw_dw_drain,pw_drain,pw_done,pw_fault,pw_export,pw_dw_post,pw_no_result,pw_result_blocked,pw_firsts,first_gap_min,first_gap_max,first_gap_sum\n");
        $sformat(file_path,"%0s/silu.hex",vector_dir);$readmemh(file_path,table_mem);
        $sformat(file_path,"%0s/dw_weights.hex",vector_dir);$readmemh(file_path,dw_weight);
        $sformat(file_path,"%0s/dw_biases.hex",vector_dir);$readmemh(file_path,dw_bias);
        $sformat(file_path,"%0s/pw_weights.hex",vector_dir);$readmemh(file_path,pw_weight);
        $sformat(file_path,"%0s/pw_biases.hex",vector_dir);$readmemh(file_path,pw_bias);
        $sformat(file_path,"%0s/multipliers.hex",vector_dir);$readmemh(file_path,multipliers);
        $sformat(file_path,"%0s/controls.hex",vector_dir);$readmemh(file_path,controls);
        if($test$plusargs("LOAD_BOUNDARY")) begin
            load_case_vectors(0);weight_load_boundary;
            $fclose(report);$fclose(trace);$fclose(windows);
            $finish;
        end
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
        // Cancel at PW first/last send and result wait, then demand full reload.
        for(c=0;c<3;c=c+1) begin
            reset;load_table;load_fixture;
            @(negedge clk);start=1;@(negedge clk);start=0;
            while(!(dut.flag_layer_pw &&
                    ((c==0 && dut.state_current==2 && dut.cnt_mac_group==0) ||
                     (c==1 && dut.state_current==2 && dut.cnt_mac_group==1) ||
                     (c==2 && dut.mac_result_valid)))) @(negedge clk);
            // Assert now, not one edge later after the selected state advances.
            rstn=0;#1;
            if(busy || output_valid || dut.pp_output_valid || dut.mac_result_valid)
                $fatal(1,"PW reset did not cancel immediately");
            reset;
            repeat(30) begin
                @(negedge clk);
                if(busy || output_valid || dut.pp_output_valid || dut.mac_result_valid)
                    $fatal(1,"PW cancellation leaked result");
            end
        end
        load_table;load_fixture;c=7;run_case;
        reset;load_table;load_fixture;pw_long_stall=1;c=8;run_case;
        // Cancel while PW result capacity is exhausted and a MAC result is held.
        reset;load_table;load_fixture;
        @(negedge clk);start=1;@(negedge clk);start=0;
        while(!dut.flag_layer_pw) @(negedge clk);
        commit_ready=0;
        while(!(dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_count==8 &&
                dut.mac_result_valid && !dut.flag_mac_result_accept)) @(negedge clk);
        rstn=0;#1;
        if(busy || output_valid || dut.pp_output_valid || dut.mac_result_valid)
            $fatal(1,"Full PW queue leaked after cancellation");
        reset;load_table;load_fixture;c=9;run_case;
        // Reset every new DW ownership position, then reload and run a complete clean block.
        for(checkpoint=0;checkpoint<5;checkpoint=checkpoint+1)
            reset_recovery_case(checkpoint);
        reset;load_table;load_fixture;dw_long_stall=1;c=15;run_case;
        // First DW task faults on its INT32 final group after a younger task was accepted.
        reset;load_table;load_fixture;
        for(j=0;j<1296;j=j+1) load_value(3'd0,j,32'd127);
        for(j=0;j<144;j=j+1) load_value(3'd2,j,32'd127);
        for(j=0;j<16;j=j+1) load_value(3'd3,j,(j==0)?32'h7fffffff:32'd0);
        @(negedge clk);load_valid=0;
        dw_fault_firsts=0;dw_fault_pp_accepts=0;dw_fault_commits=0;dw_fault_pops=0;
        checking_dw_fault=1;
        @(negedge clk);start=1;@(negedge clk);start=0;
        while(!fault) @(negedge clk);
        if(dw_fault_firsts<2 || dw_fault_pops!=1)
            $fatal(1,"DW fault lacked accepted younger task or atomic pop firsts=%0d pops=%0d",
                   dw_fault_firsts,dw_fault_pops);
        repeat(40) begin
            @(negedge clk);
            if(busy || done || output_valid || dut.flag_mac_input_valid || dut.flag_tile_valid ||
               dw_fault_pp_accepts!=0 || dw_fault_commits!=0)
                $fatal(1,"DW fault published faulting/younger work");
        end
        checking_dw_fault=0;
        // Later DW fault collides with an older active and a held PP output.
        reset;load_table;load_fixture;
        for(j=0;j<1296;j=j+1) load_value(3'd0,j,32'd127);
        for(j=0;j<144;j=j+1) load_value(3'd2,j,32'd127);
        for(j=0;j<16;j=j+1) load_value(3'd3,j,(j==8)?32'h7fffffff:32'd0);
        @(negedge clk);load_valid=0;commit_ready=1;
        dw_fault_firsts=0;dw_fault_pp_accepts=0;dw_fault_commits=0;dw_fault_pops=0;
        dw_fault_conflict_seen=0;dw_fault_writes_at_pop=-1;dw_fault_commits_at_pop=-1;
        dw_fault_allow_older=1;checking_dw_fault=1;
        @(negedge clk);start=1;@(negedge clk);start=0;
        while(!fault) @(negedge clk);
        if(dw_fault_firsts<10 || dw_fault_pops!=1 || dw_fault_conflict_seen!=1)
            $fatal(1,"DW conflict fault coverage missing firsts=%0d pops=%0d conflict=%0d",
                   dw_fault_firsts,dw_fault_pops,dw_fault_conflict_seen);
        if(dut.flag_result_reserved || dut.cnt_pw_meta==0 ||
           dut.cnt_pw_meta!==dut.road_mac_probe_Inst_tile.cnt_reserved)
            $fatal(1,"DW fault did not clear active or preserve younger ownership");
        if(dut.cnt_dw_writes!=dw_fault_writes_at_pop ||
           dw_fault_commits!=dw_fault_commits_at_pop)
            $fatal(1,"DW write/commit count advanced on fault collision");
        dw_fault_held_meta=dut.cnt_pw_meta;
        repeat(40) begin
            @(negedge clk);
            if(busy || done || output_valid || dut.flag_tile_valid ||
               dut.flag_dw_post_accept || dut.flag_commit_accept ||
               dut.cnt_pw_meta!=dw_fault_held_meta ||
               dut.cnt_dw_writes!=dw_fault_writes_at_pop ||
               dw_fault_commits!=dw_fault_commits_at_pop)
                $fatal(1,"DW conflict fault reused or published younger ownership");
        end
        checking_dw_fault=0;dw_fault_allow_older=0;
        reset;
        if(dut.cnt_pw_meta!=0 || dut.road_mac_probe_Inst_tile.cnt_reserved!=0 ||
           dut.road_mac_probe_Inst_tile.cnt_result_count!=0)
            $fatal(1,"Public reset did not release fault-held younger ownership");
        // Deterministic final-lane overflow: three-result atomic rejection.
        reset;load_table;load_fixture;
        for(j=0;j<256;j=j+1) load_value(3'd1,j,32'd127);
        for(j=0;j<384;j=j+1) load_value(3'd4,j,32'd127);
        load_value(3'd5,0,32'd0);
        for(j=1;j<24;j=j+1) load_value(3'd5,j,(j==23)?32'h7fffffff:32'd0);
        @(negedge clk);load_valid=0;pw_only=1;start=1;@(negedge clk);start=0;
        while(!fault) begin
            @(negedge clk);
            if(dut.mac_result_valid && dut.mac_fault && dut.mac_result_data!==96'd0)
                $fatal(1,"Fault result is not atomic zero");
        end
        repeat(40) begin
            @(negedge clk);
            if(busy || done || output_valid || dut.flag_mac_input_valid || dut.flag_tile_valid)
                $fatal(1,"Fault published partial tile or launched next task");
        end
        // Parameter memories may retain bits, but reset must invalidate both banks.
        reset;load_table;
        load_value(3'd6,0,32'h80000000);@(negedge clk);load_valid=0;
        if(!fault) $fatal(1,"Negative multiplier accepted");
        reset;load_table;
        load_value(3'd7,0,32'd63);@(negedge clk);load_valid=0;
        if(!fault) $fatal(1,"Illegal shift accepted");
        reset;load_table;
        load_value(3'd6,1,multipliers[1]);@(negedge clk);load_valid=0;
        if(!fault) $fatal(1,"Out of order parameter accepted");
        $fclose(report);
        $fclose(trace);
        $fclose(windows);
        $display("TB_PASS_DOWN2_DYNAMIC_OVERLAP cases=16 reset_stall=1 dw_reset_positions=5 dw_long_stall=256 dw_fault_with_younger=2 dw_fault_active_pp_conflict=1 pw_reset_positions=4 pw_long_stall=256 final_lane_fault=1 full_reload=1 queue_empty_done=1 runtime_guards=3");
        $finish;
    end
endmodule
