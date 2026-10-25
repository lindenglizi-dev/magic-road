`timescale 1ns / 1ps
// TB只供应源和表、外部反压及检查；没有任务发射、操作数返回或完成事件替身。
module tb_csp_tile_integrated(output o_test_complete);
    reg clk = 0; // 固定100MHz时钟
    reg rstn = 0; // 共同复位
    reg table_valid = 0; // 真实表装载源
    reg [9:0]table_address = 0; // 装载索引
    reg [15:0]table_data = 0; // 冻结模型表值
    wire table_ready; // 真实表接受许可
    wire table_loaded; // 完整装表状态
    reg source_begin = 0; // 源重建请求
    wire source_begin_ready; // 上一tile已退休
    reg source_valid = 0; // 原始源字节valid
    reg [9:0]source_address = 0; // halo/旁路装载位置
    reg [7:0]source_data = 0; // 当前源字节
    wire source_ready; // 装载接受许可
    wire source_loaded; // 全源完整性
    reg start = 0; // 每run一次启动
    wire start_ready; // 完整启动许可
    reg cancel = 0; // 边沿前外部取消
    reg output_ready = 1; // 实际外部写背压
    wire output_valid; // 整体输出valid
    wire [7:0]output_data; // 实际写字节
    wire [15:0]output_tag; // 实际写标识
    wire [31:0]output_address; // 实际字节地址
    wire signed [8:0]output_sum; // 精确残差中间值
    wire busy; // 全部硬件控制器忙
    wire done; // 来自真实末次写的完成
    wire fault; // 粘滞故障
    reg flag_complete_o = 0; // 仅所有检查完成后拉高
    reg active = 0; // 数值监控有效期
    reg [4095:0]vector_path; // 冻结输入和golden目录
    reg [7:0]source_bytes [0:623]; // 供给硬件的源字节
    reg [15:0]silu_table [0:1023]; // 供给硬件的同模型表
    reg [31:0]golden_acc [0:383]; // INT32黄金累加
    reg [15:0]golden_pre [0:383]; // INT16黄金前重定标
    reg [15:0]golden_silu [0:383]; // INT16黄金SiLU
    reg [7:0]golden_post [0:383]; // INT8黄金后重定标
    reg [15:0]golden_sum [0:383]; // signed9和的INT16保存
    reg [7:0]golden_output [0:383]; // 最终黄金写字节
    reg [31:0]golden_address [0:383]; // 真实图地址
    reg [127:0]group_indices [0:319]; // 仅检查操作数映射
    reg [191:0]group_weights [0:319]; // 仅检查紧凑权重恢复
    reg [95:0]group_biases [0:319]; // 仅检查偏置及尾路清零
    reg [63:0]expected_activation; // 本组独立拼装的检查值
    reg [7:0]actual_dw [0:191]; // 只记录硬件已实际写入的DW值
    reg [383:0]seen_output; // 禁止重复或漏写
    reg [383:0]seen_acc; // 禁止重复累加结果
    reg [383:0]seen_pre; // 禁止重复前重定标
    reg [383:0]seen_silu; // 禁止重复激活
    reg [383:0]seen_post; // 禁止重复后重定标
    reg held = 0; // 上拍输出处于反压
    reg [64:0]held_payload; // 上拍完整写载荷
    reg [31:0]lfsr = 32'h12345678; // 确定性反压序列
    integer test_case; // 独立场景选择
    integer cycles = 0; // 全测试时钟数
    integer run_start; // 当前run端点开始
    integer groups; // 实际核心组接受数
    integer tasks; // 实际末路写退休数
    integer outputs; // 外部写接受数
    integer accumulators; // 累加结果比较数
    integer pres; // 前重定标比较数
    integer silus; // SiLU比较数
    integer posts; // 后重定标比较数
    integer dw_writes; // 缓存真实写数
    integer pw_reads; // 缓存真实请求数
    integer starts = 0; // 顶层启动真实接受数
    integer table_loads = 0; // 全表重载完成次数
    integer runs = 0; // 完整run次数
    integer generation = 0; // 复位代数
    integer index; // 固定源装载索引
    integer lane; // 独立数值检查路
    integer tag_value; // 当前中间值tag
    integer group_index; // 当前组在320组中的索引
    integer source_index; // 检查用源索引
    integer stalls; // 已施加长背压拍数
    integer held_cycles; // 实际valid下保持拍数
    integer final_cycles; // 最后完整run端点周期
    assign o_test_complete = flag_complete_o; // 对外测试完成桥接
    always #5 clk = ~clk; // 十纳秒计算周期

    road_csp_tile_integrated #(.C_WEIGHT_FILE("../vectors/weight_program.hex"),.C_PARAMETER_FILE("../vectors/parameter_program.hex")) dut(
        .i_clk(clk),.i_rstn(rstn),.i_table_valid(table_valid),.i_table_addr(table_address),.i_table_data(table_data),
        .o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .i_source_begin(source_begin),.o_source_begin_ready(source_begin_ready),
        .i_source_valid(source_valid),.i_source_address(source_address),.i_source_data(source_data),
        .o_source_ready(source_ready),.o_source_loaded(source_loaded),.i_start(start),.o_start_ready(start_ready),
        .i_cancel(cancel),.i_output_ready(output_ready),.o_output_valid(output_valid),
        .o_output_data(output_data),.o_output_tag(output_tag),.o_output_address(output_address),.o_output_sum(output_sum),
        .o_busy(busy),.o_done(done),.o_fault(fault)
    );

    // 数值与因果性检查均观察真实模块事件，不驱动内部信号。
    always @(posedge clk)begin
        cycles = cycles + 1;
        if(cycles > 500000)$fatal(1,"CSP TILE watchdog case=%0d",test_case);
        if(rstn)lfsr <= {lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
        if(rstn && table_valid && table_ready && table_address == 1023)table_loads = table_loads + 1;
        if(rstn && start && start_ready)starts = starts + 1;
        if(rstn && active)begin
            if(fault && test_case < 8)$fatal(1,"CSP TILE unexpected fault case=%0d",test_case);
            if(dut.flag_group_accept)begin
                group_index = dut.schedule_task * 2 + dut.schedule_last;
                expected_activation = 64'd0;
                for(lane=0;lane<8;lane=lane+1)begin
                    source_index = (group_indices[group_index]>>(16*lane))&65535;
                    if(source_index != 65535)begin
                        if(dut.schedule_pw)begin
                            if(!seen_output[source_index])$fatal(1,"PW used uncommitted DW");
                            expected_activation[lane*8 +: 8] = actual_dw[source_index];
                        end else expected_activation[lane*8 +: 8] = source_bytes[source_index];
                    end
                end
                if(dut.reg_activation !== expected_activation || dut.reg_weight !== group_weights[group_index] ||
                    dut.arithmetic_Inst.i_bias_data !== group_biases[group_index])
                    $fatal(1,"CSP TILE operand mismatch group=%0d",group_index);
                if(dut.schedule_pw && !dut.cache_loaded)$fatal(1,"PW began before192 unique DW writes");
                groups = groups + 1;
            end
            if(dut.flag_task_done)tasks = tasks + 1;
            if(dut.cache_Inst.flag_write_store)dw_writes = dw_writes + 1;
            if(dut.cache_Inst.flag_read_accept)pw_reads = pw_reads + 1;
            if(dut.arithmetic_Inst.flag_acc_accept)begin
                for(lane=0;lane<3;lane=lane+1)begin
                    if(dut.arithmetic_Inst.reg_output_mask[lane])begin
                        tag_value = (dut.arithmetic_Inst.reg_tags>>(lane*16))&65535;
                        if(tag_value>=384 || seen_acc[tag_value] || dut.arithmetic_Inst.mac_data[lane*32 +: 32] !== golden_acc[tag_value])
                            $fatal(1,"CSP TILE acc mismatch tag=%0d",tag_value);
                        seen_acc[tag_value] = 1'b1;
                        accumulators = accumulators + 1;
                    end
                end
            end
            if(dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_silu_accept)begin
                tag_value = (dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[4:2]] >>
                    (dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[1:0]*16))&65535;
                if(tag_value>=384 || seen_pre[tag_value] || dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_data !== golden_pre[tag_value])
                    $fatal(1,"CSP TILE pre mismatch tag=%0d",tag_value);
                seen_pre[tag_value] = 1'b1; pres = pres + 1;
            end
            if(dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_accept)begin
                tag_value = (dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][4:2]] >>
                    (dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][1:0]*16))&65535;
                if(tag_value>=384 || seen_silu[tag_value] || dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.silu_output_data !== golden_silu[tag_value])
                    $fatal(1,"CSP TILE silu mismatch tag=%0d",tag_value);
                seen_silu[tag_value] = 1'b1; silus = silus + 1;
            end
            if(dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_complete)begin
                tag_value = (dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[4:2]] >>
                    (dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[1:0]*16))&65535;
                if(tag_value>=384 || seen_post[tag_value] || dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.wire_post_saturated !== $signed(golden_post[tag_value]))
                    $fatal(1,"CSP TILE post mismatch tag=%0d",tag_value);
                seen_post[tag_value] = 1'b1; posts = posts + 1;
            end
            if(held && {output_sum,output_address,output_tag,output_data} !== held_payload)$fatal(1,"CSP TILE output changed under backpressure");
            held = output_valid && !output_ready;
            held_payload = {output_sum,output_address,output_tag,output_data};
            if(held)held_cycles = held_cycles + 1;
            if(output_valid && output_ready)begin
                if(output_tag>=384 || seen_output[output_tag] || output_data !== golden_output[output_tag] ||
                    output_address !== golden_address[output_tag] || $signed(output_sum) !== $signed(golden_sum[output_tag]))
                    $fatal(1,"CSP TILE output mismatch tag=%0d got=%h sum=%0d",output_tag,output_data,$signed(output_sum));
                seen_output[output_tag] = 1'b1;
                if(output_tag < 192)actual_dw[output_tag] = output_data;
                outputs = outputs + 1;
            end
        end
    end

    // 只在外部写端施加反压，内部所有ready均由硬件决定。
    always @(negedge clk)begin
        if(active)begin
            if(test_case == 6 && generation == 1)output_ready = 0;
            else if(test_case == 1)output_ready = lfsr[0] || lfsr[2];
            else if((test_case == 2 && outputs == 0 || test_case == 3 && dut.schedule_pw) && stalls < 512)begin
                output_ready = 0; stalls = stalls + 1;
            end else output_ready = 1;
        end
    end

    task clear_scoreboard;
        begin
            groups=0; tasks=0; outputs=0; accumulators=0; pres=0; silus=0; posts=0;
            dw_writes=0; pw_reads=0; seen_output=0; seen_acc=0; seen_pre=0; seen_silu=0; seen_post=0;
            held=0; stalls=0; held_cycles=0;
        end
    endtask

    task load_vectors;
        input integer variant;
        begin
            if(variant == 0)begin
                $readmemh({vector_path,"/source_0.hex"},source_bytes);
                $readmemh({vector_path,"/golden_0_acc.hex"},golden_acc);
                $readmemh({vector_path,"/golden_0_pre.hex"},golden_pre);
                $readmemh({vector_path,"/golden_0_silu.hex"},golden_silu);
                $readmemh({vector_path,"/golden_0_post.hex"},golden_post);
                $readmemh({vector_path,"/golden_0_sum.hex"},golden_sum);
                $readmemh({vector_path,"/golden_0_output.hex"},golden_output);
                $readmemh({vector_path,"/golden_0_address.hex"},golden_address);
            end else begin
                $readmemh({vector_path,"/source_1.hex"},source_bytes);
                $readmemh({vector_path,"/golden_1_acc.hex"},golden_acc);
                $readmemh({vector_path,"/golden_1_pre.hex"},golden_pre);
                $readmemh({vector_path,"/golden_1_silu.hex"},golden_silu);
                $readmemh({vector_path,"/golden_1_post.hex"},golden_post);
                $readmemh({vector_path,"/golden_1_sum.hex"},golden_sum);
                $readmemh({vector_path,"/golden_1_output.hex"},golden_output);
                $readmemh({vector_path,"/golden_1_address.hex"},golden_address);
            end
        end
    endtask

    task reset_reload;
        begin
            active=0; held=0; start=0; cancel=0; source_valid=0; table_valid=0; source_begin=0;
            @(negedge clk); rstn=0;
            repeat(3)@(negedge clk);
            rstn=1; generation=generation+1;
            repeat(3)@(negedge clk);
            if(table_loaded || start_ready || output_valid || fault)$fatal(1,"CSP TILE reset stale state");
            for(index=0;index<1024;index=index+1)begin
                @(negedge clk); table_valid=1; table_address=index; table_data=silu_table[index];
                #1;if(!table_ready)$fatal(1,"CSP TILE LUT load blocked");
                @(posedge clk);
            end
            @(negedge clk); table_valid=0;
            #1;if(!table_loaded)$fatal(1,"CSP TILE LUT not loaded");
        end
    endtask

    task load_source;
        begin
            @(negedge clk); source_begin=1;
            #1;if(!source_begin_ready)$fatal(1,"CSP TILE source begin blocked");
            @(posedge clk); @(negedge clk); source_begin=0;
            #1;if(source_loaded || start_ready)$fatal(1,"CSP TILE stale source loaded");
            for(index=0;index<624;index=index+1)begin
                @(negedge clk); source_valid=1; source_address=index; source_data=source_bytes[index];
                if(test_case == 0 && index == 100)start=1;
                #1;if(!source_ready || (index<623 && start_ready))$fatal(1,"CSP TILE partial source admitted");
                @(posedge clk);
                @(negedge clk); source_valid=0; start=0;
            end
            #1;if(!source_loaded || !start_ready)$fatal(1,"CSP TILE complete source not admitted");
        end
    endtask

    task launch;
        begin
            clear_scoreboard;
            @(negedge clk); start=1; output_ready=1;
            #1;if(!start_ready)$fatal(1,"CSP TILE start blocked");
            run_start=cycles; active=1;
            @(posedge clk); @(negedge clk); start=0;
        end
    endtask

    task finish_run;
        begin
            wait(done); @(negedge clk); #1;
            if(fault || busy || outputs!=384 || groups!=320 || tasks!=160 || accumulators!=384 ||
                pres!=384 || silus!=384 || posts!=384 || dw_writes!=192 || pw_reads!=128 || seen_output !== {384{1'b1}})
                $fatal(1,"CSP TILE incomplete run groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d dw=%0d pw=%0d",
                    groups,tasks,outputs,accumulators,pres,silus,posts,dw_writes,pw_reads);
            final_cycles=cycles-run_start; runs=runs+1; active=0;
            repeat(8)@(negedge clk);
            if(done || output_valid || busy || fault)$fatal(1,"CSP TILE duplicate completion/output");
        end
    endtask

    initial begin
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("VECTORS=%s",vector_path))$fatal(1,"CSP TILE VECTORS missing");
        $readmemh({vector_path,"/silu.hex"},silu_table);
        $readmemh({vector_path,"/group_halo_indices.hex"},group_indices);
        $readmemh({vector_path,"/group_weight.hex"},group_weights);
        $readmemh({vector_path,"/group_bias.hex"},group_biases);
        load_vectors(0); clear_scoreboard; reset_reload;
        if(test_case==8 || test_case==9)begin
            @(negedge clk); source_valid=1; source_address=test_case==8 ? 10'd624 : 10'd0; source_data=8'd1;
            @(posedge clk); @(negedge clk);
            if(test_case==9)begin
                @(posedge clk); @(negedge clk);
            end
            source_valid=0;
            repeat(8)@(negedge clk);
            if(!fault || start_ready || source_ready || output_valid || done)$fatal(1,"CSP TILE bad source not sticky");
            $display("CSP_TILE_EXPECTED_FAULT case=%0d outputs=%0d",test_case,outputs);
        end else begin
            load_source; launch;
            if(test_case>=4 && test_case<=6)begin
                if(test_case==4)wait(dut.state_current==4'd3);
                if(test_case==5)wait(dut.arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_silu_accept);
                if(test_case==6)begin
                    output_ready=0; wait(output_valid); @(negedge clk); active=0; output_ready=0;
                end
                reset_reload; load_source; launch;
            end
            if(test_case==10)begin
                wait(outputs>=20); @(negedge clk); cancel=1;
                #1;if(output_valid || start_ready)$fatal(1,"CSP TILE cancel committed same-edge write");
                @(posedge clk); @(negedge clk); cancel=0; active=0;
                repeat(16)@(negedge clk);
                if(!fault || output_valid || start_ready || done)$fatal(1,"CSP TILE cancel silently resumed");
                $display("CSP_TILE_EXPECTED_FAULT case=%0d outputs=%0d",test_case,outputs);
            end else begin
                finish_run;
                if(test_case==7)begin
                    if(table_loads!=1 || !table_loaded)$fatal(1,"CSP TILE first run table lost");
                    load_vectors(1); load_source;
                    if(table_loads!=1 || !table_loaded)$fatal(1,"CSP TILE local clear reset arithmetic table");
                    launch; finish_run;
                    if(table_loads!=1 || starts!=2)$fatal(1,"CSP TILE reuse restarted core/table");
                end
                $display("CSP_TILE_PASS case=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d dw_writes=%0d pw_reads=%0d runs=%0d table_loads=%0d cycles=%0d held=%0d",
                    test_case,groups,tasks,outputs,accumulators,pres,silus,posts,dw_writes,pw_reads,runs,table_loads,final_cycles,held_cycles);
            end
        end
        flag_complete_o=1; $finish;
    end
endmodule
