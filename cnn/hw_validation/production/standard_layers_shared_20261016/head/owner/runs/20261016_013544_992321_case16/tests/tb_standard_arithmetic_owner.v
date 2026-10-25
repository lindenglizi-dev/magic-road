`timescale 1ns / 1ps

//原五核的单任务owner独立数值、退休、复位及身份损坏检查
module tb_standard_arithmetic_owner(output o_test_complete);
    reg clk = 1'b0;                           // 百兆夹具时钟
    reg rstn = 1'b0;                          // 共同复位原核和owner
    reg table_valid = 1'b0;                   // 表项保持有效
    reg [9:0]table_addr = 10'd0;              // 顺序装载位置
    reg signed [15:0]table_data = 16'sd0;     // 原冻结表项
    reg input_valid = 1'b0;                   // 输入组有效
    reg first = 1'b0;                         // 归约首组
    reg last = 1'b0;                          // 归约末组
    reg [7:0]lane_mask = 8'd0;                // 八路输入尾掩码
    reg [63:0]activation_data = 64'd0;        // 当前八输入组
    reg [191:0]weight_data = 192'd0;          // 当前二十四权重
    reg [95:0]bias_data = 96'd0;              // 首组偏置
    reg [2:0]output_mask = 3'd0;              // 三路输出许可
    reg [47:0]tags = 48'd0;                   // 不透明输出标识
    reg [95:0]addresses = 96'd0;              // 输出字节地址
    reg [95:0]pre_multipliers = 96'd0;        // 前比例
    reg [17:0]pre_shifts = 18'd0;             // 前移位
    reg [31:0]post_multiplier = 32'd0;        // 后比例
    reg [5:0]post_shift = 6'd0;               // 后移位
    reg activate = 1'b0;                     // 首组数值类型
    reg input_fault = 1'b0;                  // 故障注入
    reg output_ready = 1'b0;                 // 随机写端反压
    wire table_ready, table_loaded;          // 原表握手和装满状态
    wire input_ready, output_valid;          // 外部组与逐路结果握手
    wire signed [15:0]output_data;           // 完整有符号输出
    wire output_int16;                       // raw类型属性
    wire [15:0]output_tag;                    // 输出不透明身份
    wire [31:0]output_address;                // 输出逻辑地址
    wire fault, busy;                         // 错误和完整生存期占有
    reg complete = 1'b0;                     // 唯一结束标志
    reg [2:0]masks [0:11];                   // 参考有效输出集合
    reg modes [0:11];                        // 参考数值模式
    reg [3:0]groups [0:11];                  // 参考归约组数
    reg [95:0]biases [0:11];                 // 参考偏置三元组
    reg [95:0]multipliers [0:11];            // 参考前乘数三元组
    reg [17:0]shifts [0:11];                 // 参考前三路移位
    reg [31:0]postmultipliers [0:11];        // 参考后乘数
    reg [5:0]postshifts [0:11];              // 参考后移位
    reg [63:0]activations [0:47];            // 各任务四组以内输入
    reg [191:0]weights [0:47];               // 各任务原权重
    reg [7:0]lanemasks [0:47];               // 尾组真实掩码
    reg [31:0]expected_acc [0:35];           // Python最终累加
    reg [15:0]expected_pre [0:35];           // Python前重定标
    reg [15:0]expected_silu [0:35];          // Python激活值
    reg [15:0]expected_post [0:35];          // Python后重定标饱和INT16
    reg [15:0]expected_output [0:35];        // Python最终输出
    reg [15:0]silu_table [0:1023];           // 原模型完整表
    reg [4095:0]vectors;                      // 输入向量目录
    integer test_case = 0;                    // 当前隔离仿真场景
    integer current_task = 0;                // 真实正在执行的参考任务
    integer task_number;                     // 正常序列游标
    integer group_number;                    // 当前任务组游标
    integer index;                           // 表装载游标
    integer lane;                            // 数值检查当前输出路
    integer written = 0;                     // 已退休输出数量
    integer acc_seen = 0;                    // 完整累加交接次数
    integer pre_seen = 0;                    // 前重定标完成次数
    integer silu_seen = 0;                   // SiLU输出次数
    integer post_seen = 0;                   // 后重定标完成次数
    integer cycles = 0;                      // 真实夹具时钟拍数
    integer seed = 20261016;                 // 确定性反压随机种子
    integer stall_left = 0;                  // 连续背压预算
    reg check_numeric = 1'b0;                // 数值场景开启逐级对拍
    reg random_ready = 1'b0;                 // 自动反压开启
    reg [2:0]seen_mask = 3'd0;               // 外部已消费路防重复
    reg held_valid = 1'b0;                   // 上拍输出被阻塞
    reg [64:0]held_payload = 65'd0;          // 类型地址身份数值联合保持
    reg [64:0]payload;                        // 当前联合输出字段
    integer expected_count;                  // 本任务有效路数量

    assign o_test_complete = complete;        // 验证终态桥接
    always #5 clk = ~clk;                    // 100MHz时钟

    road_standard_arithmetic_owner dut(
        .i_clk(clk), .i_rstn(rstn),
        .i_table_valid(table_valid), .i_table_addr(table_addr), .i_table_data(table_data),
        .i_input_valid(input_valid), .i_first(first), .i_last(last),
        .i_lane_mask(lane_mask), .i_activation_data(activation_data), .i_weight_data(weight_data), .i_bias_data(bias_data),
        .i_output_mask(output_mask), .i_tags(tags), .i_addresses(addresses),
        .i_pre_multipliers(pre_multipliers), .i_pre_shifts(pre_shifts),
        .i_post_multiplier(post_multiplier), .i_post_shift(post_shift), .i_activate(activate),
        .i_input_fault(input_fault), .i_output_ready(output_ready),
        .o_table_ready(table_ready), .o_table_loaded(table_loaded), .o_input_ready(input_ready),
        .o_output_valid(output_valid), .o_output_data(output_data), .o_output_int16(output_int16),
        .o_output_tag(output_tag), .o_output_address(output_address), .o_fault(fault), .o_busy(busy)
    );

    //表顺序装载直接来自冻结CSP数值收据
    task load_table;
        begin
            for (index=0; index<1024; index=index+1) begin
                @(negedge clk);
                table_valid = 1'b1;
                table_addr = index;
                table_data = silu_table[index];
                @(posedge clk);
                while (!table_ready) @(posedge clk);
            end
            @(negedge clk);
            table_valid = 1'b0;
            if (!table_loaded) $fatal(1,"OWNER_FAIL table not loaded");
        end
    endtask

    //配置只在任务首组送出，后续组故意改变所有固定属性
    task setup_task;
        input integer number;
        begin
            current_task=number;
            output_mask=masks[number]; tags={16'd109,16'd71,16'd37};
            addresses={32'h34567890,32'h12345678,32'h01234567};
            pre_multipliers=multipliers[number]; pre_shifts=shifts[number];
            post_multiplier=postmultipliers[number]; post_shift=postshifts[number];
            bias_data=biases[number]; activate=modes[number]; input_fault=1'b0;
        end
    endtask

    //一个组只在真实ready沿接受，valid等待时操作数保持
    task send_group;
        input integer group_index;
        input first_group;
        input last_group;
        begin
            @(negedge clk);
            input_valid=1'b1; first=first_group; last=last_group;
            activation_data=activations[current_task*4+group_index];
            weight_data=weights[current_task*4+group_index];
            lane_mask=lanemasks[current_task*4+group_index];
            @(posedge clk);
            while (!input_ready) @(posedge clk);
            @(negedge clk);
            input_valid=1'b0;
            if (first_group) begin
                activate=~activate; output_mask=3'd0; tags=48'hffffffffffff;
                addresses=96'd0; pre_multipliers=96'hffffffffffffffffffffffff;
                pre_shifts=18'h3ffff; post_multiplier=32'hffffffff; post_shift=6'd63;
                bias_data=96'h7fffffff7fffffff7fffffff;
            end
        end
    endtask

    //每个任务的最后路反压证明owner不会从MACdone提前释放
    task run_task;
        input integer number;
        begin
            @(negedge clk);
            setup_task(number);
            seen_mask=3'd0; written=0; acc_seen=0; pre_seen=0; silu_seen=0; post_seen=0;
            held_valid=1'b0; check_numeric=1'b1; output_ready=1'b0;
            random_ready=1'b0;
            for (group_number=0; group_number<groups[number]; group_number=group_number+1)
                send_group(group_number,group_number==0,group_number==groups[number]-1);
            wait(output_valid);
            repeat (9) begin
                @(posedge clk);
                if (!busy || input_ready || table_ready) $fatal(1,"OWNER_FAIL released before real output");
            end
            @(negedge clk);
            random_ready=1'b1;
            wait(!busy);
            @(negedge clk);
            random_ready=1'b0; output_ready=1'b0; check_numeric=1'b0; held_valid=1'b0;
            expected_count=masks[number][0]+masks[number][1]+masks[number][2];
            if (written!=expected_count || acc_seen!=1 || pre_seen!=expected_count || seen_mask!=masks[number])
                $fatal(1,"OWNER_FAIL retirement/intermediate counts task=%0d written=%0d acc=%0d pre=%0d",number,written,acc_seen,pre_seen);
            if (silu_seen!=(modes[number]?expected_count:0) || post_seen!=(modes[number]?expected_count:0))
                $fatal(1,"OWNER_FAIL raw path accidentally activated");
        end
    endtask

    //复位立即撤销旧结果且必须重新装表，owner无旧任务成功出口
    task common_reset;
        begin
            @(negedge clk);
            rstn=1'b0; input_valid=1'b0; output_ready=1'b0; random_ready=1'b0;
            check_numeric=1'b0; held_valid=1'b0; table_valid=1'b0;
            #1;
            if (busy || output_valid || input_ready || table_loaded) $fatal(1,"OWNER_FAIL reset cancellation");
            repeat(3) @(negedge clk);
            rstn=1'b1;
            @(posedge clk); #1;
            if (input_ready || table_ready || output_valid) $fatal(1,"OWNER_FAIL first release edge admitted");
            @(negedge clk);
            load_table;
        end
    endtask

    //非成功故障必须保持占有直到共同reset，不得漏出旧结果
    task expect_fault;
        begin
            wait(fault);
            repeat(8) begin
                @(posedge clk);
                if (!busy || input_ready || output_valid || table_ready) $fatal(1,"OWNER_FAIL fault ownership leak");
            end
            $display("OWNER_PASS case=%0d expected_fault=1 busy_held=1",test_case);
            complete=1'b1;
            $finish;
        end
    endtask

    //数值及元数据只按真实握手逐级检查
    always @(posedge clk) begin
        cycles=cycles+1;
        if (cycles>200000) $fatal(1,"OWNER_FAIL timeout");
        if (rstn && check_numeric) begin
            payload={output_int16,output_address,output_tag,output_data};
            if (held_valid && (!output_valid || payload!==held_payload)) $fatal(1,"OWNER_FAIL stalled payload changed");
            held_valid=output_valid && !output_ready;
            held_payload=payload;
            if (dut.flag_acc_accept) begin
                acc_seen=acc_seen+1;
                for (lane=0; lane<3; lane=lane+1) begin
                    if (test_case==99 && lane==0) begin
                        if (dut.wire_mac_data[31:0] !== (expected_acc[current_task*3]^32'd1))
                            $fatal(1,"OWNER_FAIL injected numerical mismatch");
                    end else if (dut.wire_mac_data[lane*32+:32] !== expected_acc[current_task*3+lane])
                        $fatal(1,"OWNER_FAIL ACC task=%0d lane=%0d actual=%h expected=%h",current_task,lane,dut.wire_mac_data[lane*32+:32],expected_acc[current_task*3+lane]);
                end
                if (!busy) $fatal(1,"OWNER_FAIL MAC handoff released owner");
            end
            if (dut.road_dynamic_postprocess_Inst.flag_pre_complete) begin
                lane=dut.road_dynamic_postprocess_Inst.pre_result_tag[1:0];
                pre_seen=pre_seen+1;
                if (dut.road_dynamic_postprocess_Inst.pre_result_data !== expected_pre[current_task*3+lane])
                    $fatal(1,"OWNER_FAIL PRE task=%0d lane=%0d",current_task,lane);
            end
            if (dut.road_dynamic_postprocess_Inst.flag_post_accept) begin
                lane=dut.road_dynamic_postprocess_Inst.reg_meta_tags[dut.road_dynamic_postprocess_Inst.reg_meta_read][1:0];
                silu_seen=silu_seen+1;
                if (dut.road_dynamic_postprocess_Inst.silu_output_data !== expected_silu[current_task*3+lane])
                    $fatal(1,"OWNER_FAIL SILU task=%0d lane=%0d actual=%h expected=%h",current_task,lane,dut.road_dynamic_postprocess_Inst.silu_output_data,expected_silu[current_task*3+lane]);
            end
            if (dut.road_dynamic_postprocess_Inst.flag_post_complete) begin
                lane=dut.road_dynamic_postprocess_Inst.post_result_tag[1:0];
                post_seen=post_seen+1;
                if (dut.road_dynamic_postprocess_Inst.post_result_data !== expected_post[current_task*3+lane])
                    $fatal(1,"OWNER_FAIL POST task=%0d lane=%0d",current_task,lane);
            end
            if (output_valid && output_ready) begin
                case(output_tag)
                    16'd37: lane=0;
                    16'd71: lane=1;
                    16'd109: lane=2;
                    default: $fatal(1,"OWNER_FAIL wrong output tag");
                endcase
                if (seen_mask[lane] || !masks[current_task][lane] || output_int16!==!modes[current_task] || output_data!==expected_output[current_task*3+lane])
                    $fatal(1,"OWNER_FAIL output value/type/duplicate task=%0d lane=%0d",current_task,lane);
                if ((lane==0 && output_address!==32'h01234567) || (lane==1 && output_address!==32'h12345678) || (lane==2 && output_address!==32'h34567890))
                    $fatal(1,"OWNER_FAIL fixed address changed");
                if (!busy) $fatal(1,"OWNER_FAIL last output lacked ownership");
                seen_mask[lane]=1'b1; written=written+1;
            end
            if (fault) $fatal(1,"OWNER_FAIL unexpected numeric fault");
        end
    end

    //确定性随机背压，覆盖多拍阻塞及连续接收
    always @(negedge clk) begin
        if (random_ready) begin
            if (stall_left>0) begin
                output_ready=1'b0; stall_left=stall_left-1;
            end else if (($random(seed)&7)==0) begin
                stall_left=4; output_ready=1'b0;
            end else begin
                output_ready=1'b1;
            end
        end
    end

    //每次仿真隔离一个场景，全部源与输入由runner不可变封存
    initial begin
        if (!$value$plusargs("CASE=%d",test_case)) test_case=0;
        if (!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"OWNER_FAIL vectors absent");
        $readmemh({vectors,"/mask.hex"},masks); $readmemh({vectors,"/activate.hex"},modes);
        $readmemh({vectors,"/groups.hex"},groups); $readmemh({vectors,"/bias.hex"},biases);
        $readmemh({vectors,"/mul.hex"},multipliers); $readmemh({vectors,"/shift.hex"},shifts);
        $readmemh({vectors,"/postmul.hex"},postmultipliers); $readmemh({vectors,"/postshift.hex"},postshifts);
        $readmemh({vectors,"/activation.hex"},activations); $readmemh({vectors,"/weight.hex"},weights); $readmemh({vectors,"/lanemask.hex"},lanemasks);
        $readmemh({vectors,"/acc.hex"},expected_acc); $readmemh({vectors,"/pre.hex"},expected_pre);
        $readmemh({vectors,"/silu.hex"},silu_table); $readmemh({vectors,"/post.hex"},expected_post);
        $readmemh({vectors,"/output.hex"},expected_output);
        $readmemh({vectors,"/activation_expected.hex"},expected_silu);
        repeat(4) @(negedge clk);
        rstn=1'b1;
        load_table;
        if (test_case==0 || test_case==99) begin
            for (task_number=0; task_number<12; task_number=task_number+1) run_task(task_number);
            $display("OWNER_PASS case=%0d tasks=12 intermediate=acc_pre_silu_post masks=1_3_7 modes=raw_int8 cycles=%0d",test_case,cycles);
            complete=1'b1; $finish;
        end else if (test_case>=1 && test_case<=3) begin
            @(negedge clk); setup_task(0); output_ready=1'b0;
            send_group(0,1'b1,test_case!=1);
            if (test_case==3) wait(output_valid);
            common_reset;
            run_task(0);
            $display("OWNER_PASS case=%0d reset_phase=%0d recovery=1",test_case,test_case);
            complete=1'b1; $finish;
        end else begin
            @(negedge clk); setup_task(test_case==17?1:2); output_ready=1'b0;
            if (test_case==10) tags={16'd37,16'd37,16'd37};
            if (test_case==13) input_fault=1'b1;
            if (test_case==19) pre_multipliers=96'h800000008000000080000000;
            if (test_case==14) begin
                bias_data=96'h7fffffff7fffffff7fffffff;
                activations[current_task*4]=64'h0101010101010101;
                weights[current_task*4]=192'h010101010101010101010101010101010101010101010101;
            end
            send_group(0,test_case!=11,test_case!=12);
            if (test_case==12) send_group(1,1'b1,1'b1);
            if (test_case>=15 && test_case<=18) begin
                wait(output_valid); @(negedge clk);
                if (test_case==15) force dut.wire_pp_tag=16'd999;
                if (test_case==16) force dut.flag_pp_int16=1'b0;
                if (test_case==17) force dut.wire_pp_data=16'h0100;
                if (test_case==18) begin
                    output_ready=1'b1; @(posedge clk); @(negedge clk); output_ready=1'b0;
                    force dut.wire_pp_tag=16'd37;
                end
            end
            expect_fault;
        end
    end
endmodule
