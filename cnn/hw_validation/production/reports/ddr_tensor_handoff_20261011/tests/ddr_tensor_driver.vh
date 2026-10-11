// 条件 PAXI 端点；显式建模可见事件，不得用它替代厂商提交证明。
localparam [31:0] TENSOR_BASE=32'h03500000;
reg ddr_rstn=1'b0,ddr_req_valid=1'b0,ddr_write=1'b0,ddr_cancel=1'b0,ddr_result_ready=1'b0;
reg [31:0] ddr_addr=32'd0,ddr_owner=32'd0;
reg [127:0] ddr_write_data=128'd0;
reg [15:0] ddr_mask=16'd0;
wire ddr_req_ready,ddr_result_valid,ddr_result_write,ddr_committed,ddr_drained,ddr_fault;
wire [31:0] ddr_result_owner,ddr_result_epoch,ddr_discarded,ddr_cancelled;
wire [127:0] ddr_read_data;
wire arvalid,awvalid,wvalid;
wire [24:0] araddr,awaddr;
wire [127:0] wdata;
wire [15:0] wmask;
reg arready=1'b0,awready=1'b0,wready=1'b0,rvalid=1'b0,rlast=1'b0,model_commit=1'b0;
reg [127:0] rdata=128'd0;
reg model_commit_enabled=1'b1,model_ar_block=1'b0;
reg model_has_aw=1'b0,model_write_pending=1'b0,model_read_pending=1'b0;
reg [24:0] model_awaddr;
reg [127:0] model_write_payload;
reg [15:0] model_write_mask;
integer model_write_index,model_read_index,model_write_delay,model_read_delay;
reg [127:0] model_memory[0:36863];
reg ddr_seen_write[0:36863],ddr_seen_read[0:36863];
reg [16:0] ddr_random=17'h15ace;
reg ddr_held_aw=1'b0,ddr_held_ar=1'b0,ddr_held_w=1'b0,ddr_held_result=1'b0;
reg [24:0] ddr_previous_aw,ddr_previous_ar;
reg [143:0] ddr_previous_w;
reg [193:0] ddr_previous_result;
integer model_byte,model_addr_index,ddr_beat,ddr_byte,ddr_allow,ddr_start_tick,ddr_write_end;
integer ddr_writes=0,ddr_reads=0,ddr_success=0;
integer ddr_aw_stalls=0,ddr_w_stalls=0,ddr_ar_stalls=0,ddr_hold_cycles=0;
reg ddr_tensor_phase=1'b0;
reg [127:0] transfer_payload,transfer_result;

paxi_single_outstanding_bridge ddr_bridge(
    .i_clk(clk),.i_rstn(ddr_rstn),.i_req_valid(ddr_req_valid),.i_req_write(ddr_write),
    .i_req_byte_addr(ddr_addr),.i_req_write_data(ddr_write_data),.i_req_write_mask(ddr_mask),
    .i_req_epoch(32'd42),.i_req_owner(ddr_owner),.i_cancel(ddr_cancel),.o_req_ready(ddr_req_ready),
    .i_commit_confirmed(model_commit),.i_result_ready(ddr_result_ready),.o_result_valid(ddr_result_valid),
    .o_result_write(ddr_result_write),.o_result_committed(ddr_committed),.o_result_epoch(ddr_result_epoch),
    .o_result_owner(ddr_result_owner),.o_result_read_data(ddr_read_data),
    .o_paxi_accepted_valid(),.o_paxi_accepted_write(),.o_paxi_accepted_epoch(),.o_paxi_accepted_owner(),
    .o_drain_done(ddr_drained),.o_protocol_fault(ddr_fault),.o_late_discard_count(ddr_discarded),
    .o_cancelled_drain_count(ddr_cancelled),.i_paxi_arready(arready),.o_paxi_arvalid(arvalid),.o_paxi_araddr(araddr),
    .i_paxi_awready(awready),.o_paxi_awvalid(awvalid),.o_paxi_awaddr(awaddr),
    .i_paxi_wready(wready),.o_paxi_wvalid(wvalid),.o_paxi_wdata(wdata),.o_paxi_wmask(wmask),
    .i_paxi_rvalid(rvalid),.i_paxi_rlast(rlast),.i_paxi_rdata(rdata)
);

always @(negedge clk) begin
    ddr_random={ddr_random[15:0],ddr_random[16]^ddr_random[13]};
    awready=ddr_rstn && (mode!="stalls" || (ddr_random[0] && ticks%337>=39));
    wready=ddr_rstn && (mode!="stalls" || (ddr_random[1] && ticks%251>=57));
    arready=ddr_rstn && !model_ar_block && (mode!="stalls" || (ddr_random[2] && ticks%193>=31));
end

// 无 RREADY 的返回仅一拍；写入在模型可见事件时更新存储，而非在 W 接受时更新。
always @(posedge clk) begin
    if(!ddr_rstn) begin
        model_has_aw<=1'b0;model_write_pending<=1'b0;model_read_pending<=1'b0;
        model_commit<=1'b0;rvalid<=1'b0;rlast<=1'b0;
        ddr_held_aw=1'b0;ddr_held_ar=1'b0;ddr_held_w=1'b0;ddr_held_result=1'b0;
    end else begin
        model_commit<=1'b0;rvalid<=1'b0;rlast<=1'b0;
        if(ddr_fault) $fatal(1,"DDR bridge fault owner=%0d",ddr_owner);
        if(ddr_held_aw && (!awvalid || awaddr!==ddr_previous_aw)) $fatal(1,"AW not held");
        if(ddr_held_ar && (!arvalid || araddr!==ddr_previous_ar)) $fatal(1,"AR not held");
        if(ddr_held_w && (!wvalid || {wmask,wdata}!==ddr_previous_w)) $fatal(1,"W not held");
        if(ddr_held_result && !ddr_cancel && (!ddr_result_valid ||
            {ddr_result_write,ddr_committed,ddr_result_epoch,ddr_result_owner,ddr_read_data}!==ddr_previous_result))
            $fatal(1,"DDR result not held");
        ddr_held_aw=awvalid&&!awready;ddr_previous_aw=awaddr;
        ddr_held_ar=arvalid&&!arready;ddr_previous_ar=araddr;
        ddr_held_w=wvalid&&!wready;ddr_previous_w={wmask,wdata};
        ddr_held_result=ddr_result_valid&&!ddr_result_ready;
        ddr_previous_result={ddr_result_write,ddr_committed,ddr_result_epoch,ddr_result_owner,ddr_read_data};
        if(ddr_tensor_phase) begin
            if(ddr_held_aw) ddr_aw_stalls=ddr_aw_stalls+1;
            if(ddr_held_w) ddr_w_stalls=ddr_w_stalls+1;
            if(ddr_held_ar) ddr_ar_stalls=ddr_ar_stalls+1;
            if(ddr_held_result) ddr_hold_cycles=ddr_hold_cycles+1;
        end
        if(awvalid&&awready) begin
            if(model_has_aw||model_write_pending||model_read_pending) $fatal(1,"AW exceeds single outstanding");
            model_awaddr<=awaddr;model_has_aw<=1'b1;
        end
        if(wvalid&&wready) begin
            if(!model_has_aw||model_write_pending) $fatal(1,"W without prior AW");
            model_addr_index=({model_awaddr,1'b0}-TENSOR_BASE)/16;
            if(model_addr_index<0||model_addr_index>=36864||model_awaddr[2:0]!==0) $fatal(1,"Invalid write address");
            model_write_index<=model_addr_index;model_write_payload<=wdata;model_write_mask<=wmask;
            model_has_aw<=1'b0;model_write_pending<=1'b1;
            model_write_delay<=mode=="stalls" ? 3+ddr_random[5:3] : 3;
            if(ddr_tensor_phase) begin
                if(ddr_seen_write[model_addr_index]||wmask!==16'd0) $fatal(1,"Duplicate/masked tensor write");
                ddr_seen_write[model_addr_index]=1'b1;ddr_writes=ddr_writes+1;
            end
        end
        if(model_write_pending) begin
            if(model_write_delay>0) model_write_delay<=model_write_delay-1;
            else if(model_commit_enabled) begin
                for(model_byte=0;model_byte<16;model_byte=model_byte+1)
                    if(!model_write_mask[model_byte]) model_memory[model_write_index][model_byte*8+:8]<=model_write_payload[model_byte*8+:8];
                model_commit<=1'b1;model_write_pending<=1'b0;
            end
        end
        if(arvalid&&arready) begin
            if(model_has_aw||model_write_pending||model_read_pending) $fatal(1,"AR exceeds single outstanding");
            model_addr_index=({araddr,1'b0}-TENSOR_BASE)/16;
            if(model_addr_index<0||model_addr_index>=36864||araddr[2:0]!==0) $fatal(1,"Invalid read address");
            model_read_index<=model_addr_index;model_read_pending<=1'b1;
            model_read_delay<=mode=="stalls" ? 5+ddr_random[6:3] : 5;
            if(ddr_tensor_phase) begin
                if(ddr_seen_read[model_addr_index]) $fatal(1,"Duplicate tensor read");
                ddr_seen_read[model_addr_index]=1'b1;ddr_reads=ddr_reads+1;
            end
        end
        if(model_read_pending) begin
            if(model_read_delay>0) model_read_delay<=model_read_delay-1;
            else begin
                rdata<=model_memory[model_read_index];rvalid<=1'b1;rlast<=1'b1;model_read_pending<=1'b0;
            end
        end
        if(ddr_result_valid&&ddr_result_ready) ddr_success=ddr_success+1;
    end
end

task ddr_submit;
    input write_request;
    input integer beat;
    input [127:0] data;
    begin
        wait(ddr_req_ready);@(negedge clk);
        ddr_write=write_request;ddr_addr=TENSOR_BASE+beat*16;ddr_write_data=data;ddr_owner=beat+1;ddr_req_valid=1'b1;
        @(negedge clk);ddr_req_valid=1'b0;
    end
endtask

task ddr_transfer;
    input write_request;
    input integer beat;
    input [127:0] data;
    output [127:0] returned;
    begin
        ddr_submit(write_request,beat,data);
        wait(ddr_result_valid);
        if(mode=="stalls") repeat(1+ddr_random[4:2]) @(negedge clk);
        @(negedge clk);ddr_result_ready=1'b1;
        @(posedge clk);
        if(!ddr_result_valid||ddr_result_owner!==beat+1||ddr_result_epoch!==32'd42||
           ddr_result_write!==write_request||ddr_committed!==write_request) $fatal(1,"DDR result attribution");
        returned=ddr_read_data;
        @(negedge clk);ddr_result_ready=1'b0;
    end
endtask

task run_ddr_tensor;
    begin
        if(!$value$plusargs("ALLOW_CONDITIONAL_MODEL=%d",ddr_allow)||ddr_allow!=1)
            $fatal(1,"Explicit conditional-model opt-in required");
        repeat(3) @(negedge clk);ddr_rstn=1'b1;
        // 缺少可见事件时，接受不能发布完成，取消也不得提前释放。
        model_commit_enabled=1'b0;
        ddr_submit(1'b1,0,128'h0123456789abcdef_fedcba9876543210);
        wait(model_write_pending);repeat(32) @(negedge clk);
        if(ddr_result_valid||ddr_drained||ddr_req_ready) $fatal(1,"Write accepted was treated as visible");
        ddr_cancel=1'b1;@(negedge clk);ddr_cancel=1'b0;
        repeat(32) @(negedge clk);
        if(ddr_result_valid||ddr_drained||ddr_req_ready) $fatal(1,"Cancelled write released before drain");
        model_commit_enabled=1'b1;wait(ddr_drained);@(negedge clk);
        if(ddr_discarded!==32'd1||ddr_cancelled!==32'd1||ddr_success!=0) $fatal(1,"Cancelled write accounting");
        // AR呈现后取消：必须保持到真实接受，再丢弃晚返。
        model_ar_block=1'b1;ddr_submit(1'b0,0,128'd0);wait(arvalid);@(negedge clk);
        ddr_cancel=1'b1;@(negedge clk);ddr_cancel=1'b0;
        repeat(8) @(negedge clk);
        if(!arvalid||ddr_drained) $fatal(1,"Cancelled AR withdrawn");
        model_ar_block=1'b0;wait(ddr_drained);@(negedge clk);
        if(ddr_discarded!==32'd2||ddr_cancelled!==32'd2||ddr_success!=0) $fatal(1,"Cancelled read accounting");
        // 全张量仅使用上一段真实Stem导出的input_tensor。
        for(ddr_beat=0;ddr_beat<36864;ddr_beat=ddr_beat+1) begin
            ddr_seen_write[ddr_beat]=1'b0;ddr_seen_read[ddr_beat]=1'b0;
        end
        ddr_start_tick=ticks;ddr_tensor_phase=1'b1;
        for(ddr_beat=0;ddr_beat<36864;ddr_beat=ddr_beat+1) begin
            for(ddr_byte=0;ddr_byte<16;ddr_byte=ddr_byte+1)
                transfer_payload[ddr_byte*8+:8]=input_tensor[ddr_beat*16+ddr_byte];
            ddr_transfer(1'b1,ddr_beat,transfer_payload,transfer_result);
        end
        ddr_write_end=ticks;
        // 强制覆盖中间数组，防止直接复用原值掩盖读搬运错误。
        for(ddr_beat=0;ddr_beat<589824;ddr_beat=ddr_beat+1) input_tensor[ddr_beat]=8'hxx;
        for(ddr_beat=0;ddr_beat<36864;ddr_beat=ddr_beat+1) begin
            ddr_transfer(1'b0,ddr_beat,128'd0,transfer_result);
            for(ddr_byte=0;ddr_byte<16;ddr_byte=ddr_byte+1) begin
                if(transfer_result[ddr_byte*8+:8]!==expected_stem[ddr_beat*16+ddr_byte]) $fatal(1,"DDR readback byte mismatch");
                input_tensor[ddr_beat*16+ddr_byte]=transfer_result[ddr_byte*8+:8];
            end
        end
        ddr_tensor_phase=1'b0;
        for(ddr_beat=0;ddr_beat<36864;ddr_beat=ddr_beat+1)
            if(!ddr_seen_write[ddr_beat]||!ddr_seen_read[ddr_beat]) $fatal(1,"DDR address hole");
        if(ddr_writes!=36864||ddr_reads!=36864||ddr_success!=73728||!ddr_drained)
            $fatal(1,"DDR tensor accounting");
        $display("PAXI_TENSOR_PASS mode=%0s endpoint=CONDITIONAL bytes=589824 writes=%0d reads=%0d success=%0d cancelled=2 no_commit_guard=PASS write_cycles=%0d read_cycles=%0d aw_stall=%0d w_stall=%0d ar_stall=%0d result_hold=%0d",mode,
            ddr_writes,ddr_reads,ddr_success,ddr_write_end-ddr_start_tick,ticks-ddr_write_end,
            ddr_aw_stalls,ddr_w_stalls,ddr_ar_stalls,ddr_hold_cycles);
    end
endtask
