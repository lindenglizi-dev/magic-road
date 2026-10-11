`timescale 1ns / 1ps
module tb_down2_dynamic_tile;
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
    reg [15:0]table_mem[0:1023];
    reg [7:0]halo[0:1295],dw_weight[0:143],pw_weight[0:383],expected_out[0:383];
    reg [31:0]dw_bias[0:15],pw_bias[0:23],expected_acc[0:639],expected_commit[0:639];
    reg [31:0]expected_stages[0:1919];
    reg [639:0]seen;
    reg checking=0,random_stalls=0;
    reg [15:0]random_bits=16'hace1;
    integer ticks=0,start_tick,cycles_seen=0,commits=0,accs=0,stages=0;
    integer bins[0:9];
    integer i,j,c,idx,lane,ch,position,layer,category,exports;
    reg previous_valid=0,previous_ready=0;
    reg [15:0]previous_tag;
    reg [7:0]previous_data;
    integer report;
    down2_dynamic_tile_runner dut(
        .i_clk(clk),.i_rstn(rstn),.i_table_valid(table_valid),.i_table_addr(table_addr),
        .i_table_data(table_data),.o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .i_load_valid(load_valid),.i_load_kind(load_kind),.i_load_addr(load_addr),
        .i_load_data(load_data),.o_load_ready(load_ready),.i_start(start),.i_pw_only(1'b0),
        .i_commit_ready(commit_ready),.o_busy(busy),.o_done(done),.o_fault(fault),
        .i_export_start(export_start),.i_output_ready(output_ready),
        .o_output_valid(output_valid),.o_output_data(output_data),.o_output_index(output_index),
        .o_export_done(export_done),.o_core_cycles(core_cycles),
        .o_preload_writes(preload_writes),.o_export_cycles(export_cycles)
    );
    always @(negedge clk) begin
        if(random_stalls) begin
            random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
            commit_ready=(ticks%257>=48) && random_bits[0];
            output_ready=random_bits[1];
        end
    end
    always @(posedge clk) begin
        ticks=ticks+1;
        if(!rstn) begin previous_valid=0; end
        else if(checking) begin
            if(fault) $fatal(1,"Unexpected fault");
            if(previous_valid && !previous_ready &&
                (!dut.pp_output_valid || dut.pp_output_tag!==previous_tag || dut.pp_output_data!==previous_data))
                $fatal(1,"Commit payload changed under backpressure");
            previous_valid=dut.pp_output_valid;
            previous_ready=commit_ready && busy;
            previous_tag=dut.pp_output_tag; previous_data=dut.pp_output_data;
            if(dut.flag_start_accept) start_tick=ticks;
            if(busy) begin
                cycles_seen=cycles_seen+1;
                if(dut.pp_output_valid && !commit_ready) category=0;
                else if(dut.flag_commit_accept) category=1;
                else case(dut.road_postprocess_stream_Inst_tile.u_chain.state_current)
                    4'd2,4'd3: category=2;
                    4'd4,4'd5: category=3;
                    4'd6,4'd7: category=4;
                    4'd1: category=5;
                    default: begin
                        if(dut.state_current==4'd1) category=6;
                        else if(dut.state_current==4'd2 || dut.state_current==4'd3 || dut.state_current==4'd9) category=7;
                        else category=8;
                    end
                endcase
                bins[category]=bins[category]+1;
            end
            if(dut.flag_pp_input_accept) begin
                for(lane=0;lane<3;lane=lane+1) if(dut.wire_result_lane_mask[lane]) begin
                    layer=dut.flag_layer_pw; position=dut.wire_pp_position;
                    ch=dut.wire_result_channel_base+lane;
                    idx=layer ? 256+position*24+ch : position*16+ch;
                    if($signed(dut.wire_pp_result_data[lane*32+:32])!==$signed(expected_acc[idx]))
                        $fatal(1,"MAC mismatch idx=%0d",idx);
                    accs=accs+1;
                end
            end
            if(dut.road_postprocess_stream_Inst_tile.u_chain.flag_quant_valid &&
               dut.road_postprocess_stream_Inst_tile.u_chain.state_current==4'd3) begin
                layer=dut.road_postprocess_stream_Inst_tile.u_chain.wire_selected_tag[15];
                position=dut.road_postprocess_stream_Inst_tile.u_chain.wire_selected_tag[14:11];
                ch=dut.road_postprocess_stream_Inst_tile.u_chain.wire_selected_tag[10:6];
                idx=layer ? 256+position*24+ch : position*16+ch;
                if($signed(dut.road_postprocess_stream_Inst_tile.u_chain.wire_quant_data)!==$signed(expected_stages[idx*3]))
                    $fatal(1,"Pre mismatch idx=%0d",idx);
                stages=stages+1;
            end
            if(dut.road_postprocess_stream_Inst_tile.u_chain.flag_silu_valid &&
               dut.road_postprocess_stream_Inst_tile.u_chain.state_current==4'd5) begin
                if($signed(dut.road_postprocess_stream_Inst_tile.u_chain.wire_silu_data)!==$signed(expected_stages[idx*3+1]))
                    $fatal(1,"SiLU mismatch idx=%0d",idx);
                stages=stages+1;
            end
            if(dut.road_postprocess_stream_Inst_tile.u_chain.flag_quant_valid &&
               dut.road_postprocess_stream_Inst_tile.u_chain.state_current==4'd7) begin
                if($signed(dut.road_postprocess_stream_Inst_tile.u_chain.wire_quant_data)!==$signed(expected_stages[idx*3+2]))
                    $fatal(1,"Post mismatch idx=%0d",idx);
                stages=stages+1;
            end
            if(dut.flag_commit_accept) begin
                layer=dut.pp_output_tag[15];position=dut.pp_output_tag[14:11];ch=dut.pp_output_tag[10:6];
                idx=layer ? 256+position*24+ch : position*16+ch;
                if(idx<0 || idx>639 || seen[idx]) $fatal(1,"Duplicate/invalid commit");
                if($signed(dut.pp_output_data)!==$signed(expected_commit[idx])) $fatal(1,"Commit mismatch idx=%0d",idx);
                seen[idx]=1'b1; commits=commits+1;
            end
        end
        if(ticks>1000000) $fatal(1,"Timeout");
    end
    task reset;
        begin
            checking=0;random_stalls=0;commit_ready=1;output_ready=1;
            @(negedge clk); rstn=0;table_valid=0;load_valid=0;start=0;export_start=0;
            #1;if(output_valid || busy || table_loaded) $fatal(1,"Reset leaked transaction");
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
    task run_case;
        begin
            seen=0;commits=0;accs=0;stages=0;cycles_seen=0;previous_valid=0;
            for(j=0;j<10;j=j+1) bins[j]=0;
            checking=1;
            @(negedge clk);start=1;
            @(negedge clk);start=0;
            while(!done) @(negedge clk);
            if(commits!=640 || accs!=640 || stages!=1920 || !(&seen)) $fatal(1,"Missing values");
            if(core_cycles!=cycles_seen || ticks-start_tick!=cycles_seen) $fatal(1,"Cycle window differs");
            $display("LAYER_CASE_PASS case=%0d preload=1864 table=1024 endpoint=%0d core=%0d acc=%0d stages=%0d commits=%0d",c,ticks-start_tick,core_cycles,accs,stages,commits);
            $fwrite(report,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",c,core_cycles,bins[0],bins[1],bins[2],bins[3],bins[4],bins[5],bins[6],bins[7],bins[8]);
            checking=0;exports=0;
            @(negedge clk);export_start=1;
            @(negedge clk);export_start=0;
            while(!export_done) begin
                @(posedge clk);
                if(output_valid && output_ready) begin
                    if(output_index!==exports || output_data!==expected_out[exports]) $fatal(1,"Export mismatch");
                    exports=exports+1;
                end
                @(negedge clk);
            end
            if(exports!=384) $fatal(1,"Missing export");
            $display("EXPORT_PASS case=%0d count=%0d cycles=%0d",c,exports,export_cycles);
        end
    endtask
    initial begin
        report=$fopen("layer_cycles.csv","w");
        $fwrite(report,"case,core,commit_stall,commit,pre,silu,post,select,storage,mac_or_wait,drain_done\n");
        $readmemh("vectors/silu.hex",table_mem);
        $readmemh("vectors/dw_weights.hex",dw_weight);$readmemh("vectors/dw_biases.hex",dw_bias);
        $readmemh("vectors/pw_weights.hex",pw_weight);$readmemh("vectors/pw_biases.hex",pw_bias);
        for(c=0;c<6;c=c+1) begin
            case(c%3)
                0:begin
                    $readmemh("vectors/edge_halo.hex",halo);$readmemh("vectors/edge_output.hex",expected_out);
                    $readmemh("vectors/edge_acc.hex",expected_acc);$readmemh("vectors/edge_commit.hex",expected_commit);
                    $readmemh("vectors/edge_stages.hex",expected_stages);
                end
                1:begin
                    $readmemh("vectors/interior_halo.hex",halo);$readmemh("vectors/interior_output.hex",expected_out);
                    $readmemh("vectors/interior_acc.hex",expected_acc);$readmemh("vectors/interior_commit.hex",expected_commit);
                    $readmemh("vectors/interior_stages.hex",expected_stages);
                end
                2:begin
                    $readmemh("vectors/bottom_right_halo.hex",halo);$readmemh("vectors/bottom_right_output.hex",expected_out);
                    $readmemh("vectors/bottom_right_acc.hex",expected_acc);$readmemh("vectors/bottom_right_commit.hex",expected_commit);
                    $readmemh("vectors/bottom_right_stages.hex",expected_stages);
                end
            endcase
            reset;load_table;
            @(negedge clk);start=1;@(negedge clk);start=0;
            if(busy) $fatal(1,"Partial preload started");
            load_fixture;random_stalls=(c>=3);run_case;
        end
        // Cancel a held result, then reload all data/table and rerun.
        reset;load_table;load_fixture;
        commit_ready=0;@(negedge clk);start=1;@(negedge clk);start=0;
        while(!dut.pp_output_valid) @(negedge clk);
        repeat(32) @(negedge clk);reset;
        repeat(30) begin @(negedge clk);if(output_valid || dut.pp_output_valid || busy || table_loaded) $fatal(1,"Old result after reset");end
        load_table;load_fixture;c=6;run_case;
        $fclose(report);$display("TB_PASS_DOWN2_DYNAMIC_TILE cases=7 reset_hold=1 full_reload=1 partial_preload=6");$finish;
    end
endmodule
