// 仿真专用驱动：实际缓存读口填充下游 testbench 存储，不是 DDR 实现。
reg stem_rstn=1'b0, stem_table_valid=1'b0, stem_load_valid=1'b0;
reg stem_start=1'b0, stem_export_start=1'b0, stem_checking=1'b0;
reg [9:0] stem_table_addr=10'd0;
reg [15:0] stem_table_data=16'd0;
reg [2:0] stem_load_kind=3'd0;
reg [8:0] stem_load_addr=9'd0;
reg [31:0] stem_load_data=32'd0;
wire stem_table_ready,stem_loaded,stem_load_ready,stem_busy,stem_done,stem_fault;
wire sm_valid,sm_ready,sm_first,sm_last,sm_result_valid,sm_result_ready,sm_fault;
wire [7:0] sm_mask;
wire [63:0] sm_activation;
wire [191:0] sm_weight;
wire [95:0] sm_bias,sm_result;
wire sp_valid,sp_ready,sp_output_valid,sp_output_ready,sp_int16,sp_fault;
wire [95:0] sp_acc,sp_mul;
wire [17:0] sp_shifts;
wire [31:0] sp_post_mul,stem_cycles;
wire [5:0] sp_post_shift;
wire [2:0] sp_mask;
wire [47:0] sp_tags;
wire [15:0] sp_data,sp_tag;
wire stem_output_valid,stem_export_done;
wire [7:0] stem_output_data,stem_output_index;
reg [7:0] rgb_mem[0:442367],stem_weights[0:431];
reg [31:0] stem_biases[0:15],stem_mul[0:15],stem_shifts[0:15],stem_post[0:1];
reg [31:0] stem_acc[0:589823],stem_stages[0:1769471];
reg stem_seen[0:255];
reg stem_hold_mac=1'b0,stem_hold_export=1'b0,stem_hold_commit=1'b0;
reg [361:0] stem_previous_mac;
reg [15:0] stem_previous_export;
reg [31:0] stem_previous_commit;
integer st=0,sj,si,sy,sx,sc,sa,sl,ss,sp,stage_addr;
integer stem_acc_count,stem_pre_count,stem_silu_count,stem_post_count,stem_commits,stem_exports;
integer stem_core_seen,stem_bins[0:7],stem_category,stem_bin_sum;
integer stem_total_core=0,stem_total_export=0,stem_padding=0,stem_export_begin,stem_report;
reg [4095:0] stem_report_path;

road_stem_tile_scheduler stem_dut(
    .i_clk(clk),.i_rstn(stem_rstn),.i_table_loaded(stem_loaded),
    .i_load_valid(stem_load_valid),.i_load_kind(stem_load_kind),.i_load_addr(stem_load_addr),
    .i_load_data(stem_load_data),.o_load_ready(stem_load_ready),.i_start(stem_start),
    .o_busy(stem_busy),.o_done(stem_done),.o_fault(stem_fault),.o_core_cycles(stem_cycles),
    .o_mac_valid(sm_valid),.i_mac_ready(sm_ready),.o_mac_first(sm_first),.o_mac_last(sm_last),
    .o_mac_mask(sm_mask),.o_mac_activation(sm_activation),.o_mac_weight(sm_weight),.o_mac_bias(sm_bias),
    .i_mac_result_valid(sm_result_valid),.o_mac_result_ready(sm_result_ready),.i_mac_result(sm_result),.i_mac_fault(sm_fault),
    .o_pp_valid(sp_valid),.i_pp_ready(sp_ready),.o_pp_acc(sp_acc),.o_pp_multipliers(sp_mul),
    .o_pp_shifts(sp_shifts),.o_pp_post_multiplier(sp_post_mul),.o_pp_post_shift(sp_post_shift),
    .o_pp_mask(sp_mask),.o_pp_tags(sp_tags),.i_pp_valid(sp_output_valid),.o_pp_ready(sp_output_ready),
    .i_pp_data(sp_data),.i_pp_tag(sp_tag),.i_pp_int16(sp_int16),.i_pp_fault(sp_fault),
    .i_commit_ready(commit_ready),.i_export_start(stem_export_start),.o_output_valid(stem_output_valid),
    .i_output_ready(output_ready),.o_output_data(stem_output_data),.o_output_index(stem_output_index),.o_export_done(stem_export_done)
);
road_mac_probe stem_mac(
    .i_clk(clk),.i_rstn(stem_rstn),.i_input_valid(sm_valid),.o_input_ready(sm_ready),
    .i_first(sm_first),.i_last(sm_last),.i_lane_mask(sm_mask),.i_activation_data(sm_activation),
    .i_weight_data(sm_weight),.i_bias_data(sm_bias),.i_result_ready(sm_result_ready),
    .o_result_valid(sm_result_valid),.o_result_data(sm_result),.o_fault(sm_fault)
);
road_dynamic_postprocess stem_pp(
    .i_clk(clk),.i_rstn(stem_rstn),.i_table_valid(stem_table_valid),.i_table_addr(stem_table_addr),
    .i_table_data(stem_table_data),.o_table_ready(stem_table_ready),.o_table_loaded(stem_loaded),
    .i_input_valid(sp_valid),.o_input_ready(sp_ready),.i_accumulators(sp_acc),.i_pre_multipliers(sp_mul),
    .i_pre_shifts(sp_shifts),.i_post_multiplier(sp_post_mul),.i_post_shift(sp_post_shift),.i_activate(1'b1),
    .i_lane_mask(sp_mask),.i_tags(sp_tags),.i_input_fault(1'b0),.i_output_ready(sp_output_ready),
    .o_output_valid(sp_output_valid),.o_output_data(sp_data),.o_output_tag(sp_tag),.o_output_int16(sp_int16),
    .o_fault(sp_fault),.o_queue_count(),.o_pending_count(),.o_meta_count(),
    .o_pre_busy(),.o_silu_busy(),.o_post_busy(),.o_pre_accept(),.o_silu_accept(),.o_post_accept()
);

task stem_resolve;
    input [15:0] internal_tag;
    output integer result_address;
    reg [47:0] tags;
    reg [15:0] tag_value;
    begin
        if(internal_tag[15:5]!==11'd0 || internal_tag[1:0]>2) $fatal(1,"Stem internal tag");
        tags=stem_pp.reg_retire_tags[internal_tag[4:2]];
        tag_value=tags>>(internal_tag[1:0]*16);
        if(tag_value[15:8]!==8'd0) $fatal(1,"Stem external tag");
        result_address=st*256+tag_value[7:0];
    end
endtask

always @(posedge clk) begin
    if(stem_rstn && stem_fault) $fatal(1,"Stem fault tile=%0d",st);
    if(stem_checking) begin
        if(stem_hold_mac && (!sm_valid || {sm_first,sm_last,sm_mask,sm_activation,sm_weight,sm_bias}!==stem_previous_mac))
            $fatal(1,"Stem MAC input not held");
        stem_hold_mac=sm_valid&&!sm_ready;
        stem_previous_mac={sm_first,sm_last,sm_mask,sm_activation,sm_weight,sm_bias};
        if(stem_hold_commit && (!sp_output_valid || {sp_tag,sp_data}!==stem_previous_commit)) $fatal(1,"Stem commit not held");
        stem_hold_commit=sp_output_valid&&!sp_output_ready; stem_previous_commit={sp_tag,sp_data};
        if(stem_hold_export && (!stem_output_valid || {stem_output_index,stem_output_data}!==stem_previous_export)) $fatal(1,"Stem export not held");
        stem_hold_export=stem_output_valid&&!output_ready; stem_previous_export={stem_output_index,stem_output_data};
        if(stem_busy) begin
            stem_core_seen=stem_core_seen+1;
            if(sp_output_valid&&!sp_output_ready) stem_category=0;
            else if(sp_valid&&!sp_ready) stem_category=1;
            else if(sp_output_valid&&sp_output_ready) stem_category=2;
            else if(sm_valid&&sm_ready) stem_category=3;
            else if(stem_dut.state_current==4'd1 || stem_dut.state_current==4'd2) stem_category=4;
            else if(stem_dut.state_current==4'd3) stem_category=5;
            else if(stem_dut.state_current==4'd4) stem_category=6;
            else stem_category=7;
            stem_bins[stem_category]=stem_bins[stem_category]+1;
        end
        if(sm_valid&&sm_ready) begin
            if(sm_mask !== (sm_last ? 8'h07 : 8'hff)) $fatal(1,"Stem tail input mask");
            if(sm_first !== (stem_dut.cnt_group==0)) $fatal(1,"Stem first group");
        end
        if(sp_valid&&sp_ready) begin
            if(sp_mask !== (stem_dut.cnt_channel==15 ? 3'b001 : 3'b111)) $fatal(1,"Stem tail output mask");
            for(sl=0;sl<3;sl=sl+1) if(sp_mask[sl]) begin
                sa=st*256+stem_dut.cnt_position*16+stem_dut.cnt_channel+sl;
                if(sm_result[sl*32+:32]!==stem_acc[sa]) $fatal(1,"Stem MAC mismatch tile=%0d addr=%0d",st,sa);
                stem_acc_count=stem_acc_count+1;
            end
        end
        if(stem_pp.flag_silu_accept) begin
            stem_resolve(stem_pp.pre_result_tag,stage_addr);
            if($signed(stem_pp.pre_result_data)!==$signed(stem_stages[stage_addr*3])) $fatal(1,"Stem pre mismatch %0d",stage_addr);
            stem_pre_count=stem_pre_count+1;
        end
        if(stem_pp.flag_post_accept) begin
            stem_resolve(stem_pp.reg_meta_tags[stem_pp.reg_meta_read],stage_addr);
            if($signed(stem_pp.silu_output_data)!==$signed(stem_stages[stage_addr*3+1])) $fatal(1,"Stem SiLU mismatch %0d",stage_addr);
            stem_silu_count=stem_silu_count+1;
        end
        if(stem_pp.flag_post_complete) begin
            stem_resolve(stem_pp.post_result_tag,stage_addr);
            if($signed(stem_pp.post_result_data)!==$signed(stem_stages[stage_addr*3+2])) $fatal(1,"Stem post mismatch %0d",stage_addr);
            stem_post_count=stem_post_count+1;
        end
        if(sp_output_valid&&sp_output_ready) begin
            sa=sp_tag[7:0];
            if(sp_tag[15:8]!==0 || stem_seen[sa]) $fatal(1,"Stem duplicate/invalid commit");
            if($signed(sp_data)!==$signed(stem_stages[(st*256+sa)*3+2])) $fatal(1,"Stem commit mismatch");
            stem_seen[sa]=1'b1; stem_commits=stem_commits+1;
        end
        if(stem_output_valid&&output_ready) begin
            if(stem_output_index!==stem_exports || stem_exports>=256) $fatal(1,"Stem export sequence");
            sa=st*256+stem_output_index;
            if(stem_output_data!==expected_stem[sa]) $fatal(1,"Stem export mismatch %0d",sa);
            input_tensor[sa]=stem_output_data; // 下游唯一数据来源：真实 Stem 输出读口。
            stem_exports=stem_exports+1;
        end
    end
end

task stem_load;
    input [2:0] kind;
    input integer address;
    input [31:0] value;
    begin
        @(negedge clk); stem_load_valid=1'b1;stem_load_kind=kind;stem_load_addr=address;stem_load_data=value;
        if(!stem_load_ready) $fatal(1,"Stem load blocked addr=%0d",address);
    end
endtask

task run_stem;
    begin
        $sformat(file_path,"%0s/rgb.hex",vector_dir);$readmemh(file_path,rgb_mem);
        $sformat(file_path,"%0s/stem_weights.hex",vector_dir);$readmemh(file_path,stem_weights);
        $sformat(file_path,"%0s/stem_biases.hex",vector_dir);$readmemh(file_path,stem_biases);
        $sformat(file_path,"%0s/stem_multipliers.hex",vector_dir);$readmemh(file_path,stem_mul);
        $sformat(file_path,"%0s/stem_shifts.hex",vector_dir);$readmemh(file_path,stem_shifts);
        $sformat(file_path,"%0s/stem_post.hex",vector_dir);$readmemh(file_path,stem_post);
        $sformat(file_path,"%0s/stem_acc.hex",vector_dir);$readmemh(file_path,stem_acc);
        $sformat(file_path,"%0s/stem_stages.hex",vector_dir);$readmemh(file_path,stem_stages);
        $sformat(stem_report_path,"%0s.stem.csv",report_path);stem_report=$fopen(stem_report_path,"w");
        if(!stem_report) $fatal(1,"Stem report open");
        $fwrite(stem_report,"tile,core,preload,export_cycles,acc,pre,silu,post,commits,exports,bin0,bin1,bin2,bin3,bin4,bin5,bin6,bin7\n");
        repeat(8) @(negedge clk);stem_rstn=1'b1;
        for(si=0;si<1024;si=si+1) begin
            @(negedge clk);stem_table_valid=1'b1;stem_table_addr=si;stem_table_data=table_mem[si];
            if(!stem_table_ready || (si<1023 && stem_loaded)) $fatal(1,"Stem table loading");
        end
        @(negedge clk);stem_table_valid=1'b0;
        if(!stem_loaded) $fatal(1,"Stem table incomplete");
        for(si=0;si<432;si=si+1) stem_load(3'd2,si,{{24{stem_weights[si][7]}},stem_weights[si]});
        for(si=0;si<16;si=si+1) stem_load(3'd3,si,stem_biases[si]);
        for(si=0;si<16;si=si+1) stem_load(3'd4,si,stem_mul[si]);
        for(si=0;si<16;si=si+1) stem_load(3'd5,si,stem_shifts[si]);
        for(si=0;si<2;si=si+1) stem_load(3'd6,si,stem_post[si]);
        @(negedge clk);stem_load_valid=1'b0;
        for(st=0;st<2304;st=st+1) begin
            for(sj=0;sj<243;sj=sj+1) begin
                sy=st/64*8+sj/27-1;sx=st%64*8+(sj/3)%9-1;sc=sj%3;
                if(sy<0||sy>=288||sx<0||sx>=512) begin stem_load(3'd1,sj,32'd0);stem_padding=stem_padding+1;end
                else stem_load(3'd0,sj,{24'd0,rgb_mem[(sy*512+sx)*3+sc]});
                if(sj==241) begin
                    @(negedge clk);stem_load_valid=1'b0;stem_start=1'b1;
                    @(negedge clk);stem_start=1'b0;
                    if(stem_busy) $fatal(1,"Stem partial halo admitted");
                end
            end
            @(negedge clk);stem_load_valid=1'b0;
            for(si=0;si<256;si=si+1) stem_seen[si]=1'b0;
            for(si=0;si<8;si=si+1) stem_bins[si]=0;
            stem_acc_count=0;stem_pre_count=0;stem_silu_count=0;stem_post_count=0;stem_commits=0;stem_exports=0;stem_core_seen=0;
            stem_checking=1'b1;
            @(negedge clk);stem_start=1'b1;@(negedge clk);stem_start=1'b0;
            wait(stem_done);@(negedge clk);
            if(stem_acc_count!=256||stem_pre_count!=256||stem_silu_count!=256||stem_post_count!=256||stem_commits!=256)
                $fatal(1,"Stem incomplete stages tile=%0d",st);
            stem_bin_sum=0;for(si=0;si<8;si=si+1) stem_bin_sum=stem_bin_sum+stem_bins[si];
            if(stem_bin_sum!=stem_cycles||stem_core_seen!=stem_cycles) $fatal(1,"Stem cycle accounting");
            for(si=0;si<256;si=si+1) if(!stem_seen[si]) $fatal(1,"Stem commit hole");
            stem_total_core=stem_total_core+stem_cycles;
            wait(stem_dut.state_current==4'd0);@(negedge clk);
            stem_export_begin=ticks;stem_export_start=1'b1;@(negedge clk);stem_export_start=1'b0;
            wait(stem_export_done);@(negedge clk);
            if(stem_exports!=256) $fatal(1,"Stem missing export");
            stem_total_export=stem_total_export+ticks-stem_export_begin;
            stem_checking=1'b0;
            $fwrite(stem_report,"%0d,%0d,243,%0d,%0d,%0d,%0d,%0d,%0d,%0d",st,stem_cycles,ticks-stem_export_begin,
                    stem_acc_count,stem_pre_count,stem_silu_count,stem_post_count,stem_commits,stem_exports);
            for(si=0;si<8;si=si+1) $fwrite(stem_report,",%0d",stem_bins[si]);
            $fwrite(stem_report,"\n");
            if(st%256==255) $display("STEM_PROGRESS mode=%0s completed=%0d/2304",mode,st+1);
        end
        for(si=0;si<589824;si=si+1) if(input_tensor[si]!==expected_stem[si]) $fatal(1,"Stem tensor/handoff mismatch %0d",si);
        $fclose(stem_report);
        $display("STEM_TOTAL mode=%0s tiles=2304 bytes=589824 each_stage=589824 duplicates=0 holes=0 core=%0d export_window=%0d preload_halo=559872 preload_params=482 table=1024 padding=%0d",mode,stem_total_core,stem_total_export,stem_padding);
    end
endtask
