`timescale 1ns / 1ps
// Boundary test for the registered ROM parameter ingress and external handoff.
module tb_rom_ingress(output reg o_test_done);
    reg clk=0;
    always #5 clk=~clk;

    reg rstn=0, load_valid=0, start=0, commit_ready=1, export_start=0, output_ready=1;
    reg [10:0]load_addr=0;
    reg signed [7:0]load_data=0;
    wire load_ready, parameters_ready, busy, done, fault, output_valid, export_done;
    wire signed [7:0]output_data;
    wire [8:0]output_index;

    reg [7:0]source_kind[0:1675], source_table[0:1675];
    reg [15:0]source_address[0:1675];
    reg [31:0]source_data[0:1675];
    reg [2:0]load_kind_expected[0:651];
    reg [10:0]load_address_expected[0:651];
    reg [31:0]load_data_expected[0:651];
    reg [9:0]table_address_expected[0:1023];
    reg [15:0]table_data_expected[0:1023];

    integer capture_count=0, consume_count=0, table_count=0, external_count=0;
    integer load_vector_count=0, table_vector_count=0;
    integer i;
    reg previous_owner=0, previous_pref_done=0, previous_table_loaded=0;
    reg previous_pending=0, previous_fault=0;
    reg [2:0]held_kind;
    reg [10:0]held_address;
    reg [31:0]held_data;
    reg [4095:0]vectors;

    road_rom_down2_top dut(
        .i_clk(clk), .i_rstn(rstn), .i_load_valid(load_valid),
        .i_load_addr(load_addr), .i_load_data(load_data), .o_load_ready(load_ready),
        .i_start(start), .i_commit_ready(commit_ready), .i_export_start(export_start),
        .i_output_ready(output_ready), .o_parameters_ready(parameters_ready),
        .o_busy(busy), .o_done(done), .o_fault(fault), .o_output_valid(output_valid),
        .o_output_data(output_data), .o_output_index(output_index), .o_export_done(export_done)
    );

    always @(posedge clk) begin
        if(!dut.domain_rstn) begin
            capture_count=0;
            consume_count=0;
            table_count=0;
            external_count=0;
            previous_owner=0;
            previous_pref_done=0;
            previous_table_loaded=0;
            previous_pending=0;
            previous_fault=0;
        end else begin
            if(dut.flag_pref_capture) begin
                if(capture_count>=652 ||
                   dut.pref_load_kind !== load_kind_expected[capture_count] ||
                   dut.pref_load_address !== load_address_expected[capture_count] ||
                   dut.pref_load_data !== load_data_expected[capture_count])
                    $fatal(1,"Prefetch capture mismatch %0d",capture_count);
                capture_count=capture_count+1;
            end
            if(dut.flag_pref_consume) begin
                if(consume_count>=capture_count || consume_count>=652 ||
                   dut.runner_load_kind !== load_kind_expected[consume_count] ||
                   dut.runner_load_address !== load_address_expected[consume_count] ||
                   dut.runner_load_data !== load_data_expected[consume_count])
                    $fatal(1,"Registered egress mismatch/duplicate %0d",consume_count);
                consume_count=consume_count+1;
            end
            if(dut.pref_table_valid && dut.runner_table_ready) begin
                if(table_count>=1024 ||
                   dut.pref_table_address !== table_address_expected[table_count] ||
                   dut.pref_table_data !== table_data_expected[table_count])
                    $fatal(1,"Table mismatch %0d",table_count);
                table_count=table_count+1;
            end
            if(dut.flag_external_owner && dut.runner_load_valid && dut.runner_load_ready) begin
                if(dut.runner_load_kind !== 3'd0 ||
                   dut.runner_load_address !== external_count[10:0] ||
                   $signed(dut.runner_load_data) !== $signed(load_data))
                    $fatal(1,"External halo was not passed through %0d",external_count);
                external_count=external_count+1;
            end
            if(dut.flag_external_owner && !previous_owner) begin
                if(!previous_pref_done || !previous_table_loaded || previous_pending || previous_fault)
                    $fatal(1,"External ownership opened before the registered boundary drained");
            end
            if(dut.flag_external_owner && (dut.flag_pref_capture || dut.flag_pref_consume))
                $fatal(1,"Prefetch write occurred after external ownership");
            if(!dut.flag_external_owner && (load_ready || parameters_ready))
                $fatal(1,"External interface opened before ownership");
            if(dut.flag_fault_any && (dut.pref_load_ready || dut.runner_load_valid ||
               dut.flag_pref_capture || dut.flag_pref_consume || dut.flag_external_open ||
               load_ready || parameters_ready || output_valid || export_done))
                $fatal(1,"Fault did not close reception/publication");
            if(previous_fault && dut.flag_pref_pending)
                $fatal(1,"Pending parameter survived a fault clock");
            previous_owner=dut.flag_external_owner;
            previous_pref_done=dut.pref_done;
            previous_table_loaded=dut.runner_table_loaded;
            previous_pending=dut.flag_pref_pending;
            previous_fault=dut.flag_fault_any;
        end
    end

    task apply_reset;
        begin
            @(negedge clk);
            rstn=0;
            load_valid=0;
            start=0;
            export_start=0;
            #1;
            if(dut.flag_pref_pending || dut.flag_external_owner || load_ready ||
               parameters_ready || busy || output_valid || export_done)
                $fatal(1,"Reset did not cancel ingress immediately");
            repeat(3) @(negedge clk);
            rstn=1;
            wait(dut.domain_rstn);
            @(negedge clk);
        end
    endtask

    task check_pending_stable;
        input integer cycles;
        begin
            held_kind=dut.reg_pref_kind;
            held_address=dut.reg_pref_address;
            held_data=dut.reg_pref_data;
            repeat(cycles) begin
                @(negedge clk);
                if(!dut.flag_pref_pending || dut.pref_load_ready ||
                   dut.reg_pref_kind !== held_kind ||
                   dut.reg_pref_address !== held_address ||
                   dut.reg_pref_data !== held_data)
                    $fatal(1,"Pending parameter changed under endpoint stall");
            end
        end
    endtask

    task wait_external_owner;
        begin
            wait(dut.flag_external_owner);
            @(negedge clk);
            if(!parameters_ready || capture_count!=652 || consume_count!=652 || table_count!=1024)
                $fatal(1,"Incomplete handoff capture=%0d consume=%0d table=%0d",
                       capture_count,consume_count,table_count);
        end
    endtask

    initial begin
        o_test_done=0;
        if(!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"Missing VECTORS path");
        $readmemh({vectors,"/table.hex"},source_table);
        $readmemh({vectors,"/kind.hex"},source_kind);
        $readmemh({vectors,"/address.hex"},source_address);
        $readmemh({vectors,"/data.hex"},source_data);
        for(i=0;i<1676;i=i+1) begin
            if(source_table[i]) begin
                table_address_expected[table_vector_count]=source_address[i][9:0];
                table_data_expected[table_vector_count]=source_data[i][15:0];
                table_vector_count=table_vector_count+1;
            end else begin
                load_kind_expected[load_vector_count]=source_kind[i][2:0];
                load_address_expected[load_vector_count]=source_address[i][10:0];
                load_data_expected[load_vector_count]=source_data[i];
                load_vector_count=load_vector_count+1;
            end
        end
        if(load_vector_count!=652 || table_vector_count!=1024)
            $fatal(1,"Unexpected vector split load=%0d table=%0d",load_vector_count,table_vector_count);

        // Test injection: hold only the runner load endpoint low; no DUT arithmetic is changed.
        apply_reset;
        force dut.runner_load_ready=1'b0;
        wait(dut.flag_pref_pending);
        load_valid=1;
        load_addr=11'd77;
        load_data=-8'sd12;
        start=1;
        check_pending_stable(80);
        if(load_ready || parameters_ready || busy || capture_count!=1 || consume_count!=0)
            $fatal(1,"Pre-phase halo/start isolation failed");
        // Test injection: hold a source fault high until reset to check cancellation.
        force dut.rom_fault=1'b1;
        #1;
        if(!fault || dut.runner_load_valid || dut.pref_load_ready || load_ready || parameters_ready)
            $fatal(1,"Fault did not immediately mask the full ingress entry");
        @(posedge clk);
        #1;
        if(dut.flag_pref_pending) $fatal(1,"Fault did not clear pending on the next clock");
        repeat(8) begin
            @(negedge clk);
            if(!fault || dut.runner_load_valid || load_ready || parameters_ready || busy)
                $fatal(1,"Injected source fault was not terminal before reset");
        end
        @(negedge clk);
        rstn=0;
        load_valid=0;
        start=0;
        #1;
        release dut.rom_fault;
        release dut.runner_load_ready;
        repeat(3) @(negedge clk);
        rstn=1;
        wait(dut.domain_rstn);
        @(negedge clk);

        // A full registered entry is also cancelled directly by reset.
        force dut.runner_load_ready=1'b0;
        wait(dut.flag_pref_pending);
        apply_reset;
        release dut.runner_load_ready;

        // Reset in the middle of real 1024-entry table loading, then restart from zero.
        wait(table_count==400);
        if(dut.flag_external_owner || parameters_ready) $fatal(1,"Opened during table load");
        apply_reset;

        // Block exactly the final parameter. The table may finish, but ownership must not open.
        wait(consume_count==651);
        @(negedge clk);
        force dut.runner_load_ready=1'b0;
        wait(capture_count==652 && dut.flag_pref_pending);
        wait(dut.pref_done && dut.runner_table_loaded);
        check_pending_stable(40);
        if(dut.flag_external_owner || parameters_ready || consume_count!=651 || table_count!=1024)
            $fatal(1,"Last blocked parameter incorrectly opened ownership");
        release dut.runner_load_ready;
        apply_reset;

        // Complete a clean boot and prove every registered ingress exits exactly once.
        wait_external_owner;
        for(i=0;i<1296;i=i+1) begin
            @(negedge clk);
            load_valid=1;
            load_addr=i[10:0];
            load_data=i[7:0];
            while(!load_ready) @(negedge clk);
        end
        @(negedge clk);
        load_valid=0;
        if(external_count!=1296) $fatal(1,"Incomplete external halo pass-through %0d",external_count);

        // Invalid external address latches a terminal fault and blocks a later valid request/start.
        @(negedge clk);
        load_valid=1;
        load_addr=11'd1296;
        load_data=8'sd1;
        start=0;
        @(posedge clk);
        #1;
        if(!fault || load_ready || parameters_ready || dut.flag_pref_pending)
            $fatal(1,"Invalid address did not terminate ingress");
        @(negedge clk);
        load_addr=11'd0;
        start=1;
        repeat(8) begin
            @(negedge clk);
            if(!fault || load_ready || parameters_ready || busy || output_valid || export_done)
                $fatal(1,"Fault did not remain terminal before reset");
        end
        apply_reset;
        wait(capture_count==1);
        o_test_done=1;
        $display("TB_PASS_ROM_INGRESS parameters=652 table=1024 halo=1296 resets=full_table_last fault=sticky");
        $finish;
    end

    initial begin
        #50000000;
        $fatal(1,"Timeout");
    end
endmodule
