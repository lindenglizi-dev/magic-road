`timescale 1ns / 1ps
// Bounded real-reader test. The request gate controls acceptance, not ROM latency.
module tb_rom_arbiter_boundary;
    reg clk=0,rstn=0,pvalid=0,lvalid=0,pready=0,lready=0,reader_gate=0;
    reg [12:0] paddr=0,laddr=0;
    wire paccept,laccept,presponse,lresponse,rv,rr,sv,sr,fault,reader_fault,reader_ready;
    wire [12:0] ra;
    wire [159:0] pd,ld,sd;
    reg [159:0] words[0:7167];
    reg [4095:0] words_path,trace_path;
    reg [15:0] random_bits=16'hACE1;
    reg outstanding=0,owner=0,physical_seen=0,last_owner=0,last_both=0;
    reg [12:0] expected_address=0,held_address=0;
    reg [159:0] held_data=0;
    reg hold_pending=0,hold_active=0,request_held=0,response_held=0;
    integer cycle=0,pa=0,la=0,pr=0,lr=0,reads=0,returns=0;
    integer trace_file,admit_cycle=0,physical_cycle=0,hold_left=0,hold_checks=0;
    integer p_wait=0,l_wait=0,p_wait_max=0,l_wait_max=0;
    integer admitted_before,returned_before,base_pa,base_la,target_pa,target_la;
    integer latency_min=99999,latency_max=0,latency_sum=0,rr_checks=0;
    always #5 clk=~clk;
    road_rom_two_client_arbiter dut(
        .i_clk(clk),.i_rstn(rstn),.i_param_request_valid(pvalid),.i_param_request_addr(paddr),
        .o_param_request_ready(paccept),.o_param_response_valid(presponse),.o_param_response_data(pd),.i_param_response_ready(pready),
        .i_lut_request_valid(lvalid),.i_lut_request_addr(laddr),.o_lut_request_ready(laccept),
        .o_lut_response_valid(lresponse),.o_lut_response_data(ld),.i_lut_response_ready(lready),
        .o_rom_request_valid(rv),.o_rom_request_addr(ra),.i_rom_request_ready(rr),
        .i_rom_response_valid(sv),.i_rom_response_data(sd),.o_rom_response_ready(sr),.i_rom_fault(reader_fault),.o_fault(fault));
    // Exactly one actual reader and its unchanged 14-group/56-lane ROM closure.
    road_numeric_rom_reader reader(.i_clk(clk),.i_rstn(rstn),
        .i_request_valid(rv && reader_gate),.i_request_addr(ra),.o_request_ready(reader_ready),
        .o_response_valid(sv),.o_response_data(sd),.i_response_ready(sr),.o_fault(reader_fault));
    assign rr=reader_ready && reader_gate;
    always @(posedge clk) begin
        cycle=cycle+1;
        if(!rstn) begin
            outstanding=0;physical_seen=0;request_held=0;response_held=0;last_both=0;p_wait=0;l_wait=0;
        end else begin
            if(paccept && laccept) $fatal(1,"TB_FAIL both clients ready");
            if(outstanding && (owner ? pd!==160'd0 : ld!==160'd0)) $fatal(1,"TB_FAIL nonowner data");
            if(pvalid && !paccept) p_wait=p_wait+1; else p_wait=0;
            if(lvalid && !laccept) l_wait=l_wait+1; else l_wait=0;
            if(p_wait>p_wait_max) p_wait_max=p_wait;
            if(l_wait>l_wait_max) l_wait_max=l_wait;
            if(request_held && (!rv || ra!==held_address)) $fatal(1,"TB_FAIL registered request changed");
            request_held=rv && !rr;held_address=ra;
            if(response_held && (!(owner?lresponse:presponse) || (owner?ld:pd)!==held_data)) $fatal(1,"TB_FAIL held response changed");
            response_held=(presponse && !pready)||(lresponse && !lready);held_data=owner?ld:pd;
            if((pvalid && paccept)||(lvalid && laccept)) begin
                if(outstanding) $fatal(1,"TB_FAIL admitted before owner retired");
                if(rv) $fatal(1,"TB_FAIL unregistered admission forwarded same cycle");
                owner=lvalid && laccept;expected_address=owner?laddr:paddr;
                if(last_both && pvalid && lvalid) begin
                    if(owner==last_owner) $fatal(1,"TB_FAIL round robin did not alternate");
                    rr_checks=rr_checks+1;
                end
                last_both=pvalid && lvalid;last_owner=owner;outstanding=1;physical_seen=0;admit_cycle=cycle;
                if(owner) la=la+1; else pa=pa+1;
            end
            if(rv && rr) begin
                if(!outstanding || physical_seen || ra!==expected_address || cycle<=admit_cycle) $fatal(1,"TB_FAIL physical acceptance ownership");
                reads=reads+1;physical_seen=1;physical_cycle=cycle;
            end
            if(presponse || lresponse) begin
                if(!outstanding || !physical_seen || (owner?presponse:lresponse) || (owner?ld:pd)!==words[expected_address])
                    $fatal(1,"TB_FAIL response owner/value address=%0d",expected_address);
            end
            if((presponse && pready)||(lresponse && lready)) begin
                if(!sv || !sr) $fatal(1,"TB_FAIL owner retired without reader handshake");
                returns=returns+1;if(owner) lr=lr+1; else pr=pr+1;
                if(cycle-admit_cycle<latency_min) latency_min=cycle-admit_cycle;
                if(cycle-admit_cycle>latency_max) latency_max=cycle-admit_cycle;
                latency_sum=latency_sum+cycle-admit_cycle;
                $fwrite(trace_file,"%0d,%0d,%0d,%0d,%0d,%0d\n",owner,expected_address,admit_cycle,physical_cycle,cycle,cycle-admit_cycle);
                outstanding=0;physical_seen=0;
            end
        end
    end
    task common_reset;
        begin
            @(negedge clk);rstn=0;pvalid=0;lvalid=0;pready=0;lready=0;reader_gate=0;hold_pending=0;hold_active=0;#1;
            if(paccept || laccept || presponse || lresponse || rv || sr || fault) $fatal(1,"TB_FAIL reset masking");
            repeat(4) @(negedge clk);rstn=1;
            @(negedge clk);if(paccept || laccept || rv) $fatal(1,"TB_FAIL release first edge");
            @(negedge clk);reader_gate=1;
        end
    endtask
    task batch;
        input integer pcount,lcount,do_hold;
        begin
            base_pa=pa;base_la=la;target_pa=pa+pcount;target_la=la+lcount;hold_pending=do_hold;reader_gate=0;
            while(pa<target_pa || la<target_la || outstanding) begin
                @(negedge clk);
                random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
                pvalid=pa<target_pa;lvalid=la<target_la;
                paddr=(pa*509+29)%7168;laddr=(la*257+6898)%7168;
                reader_gate=(cycle%17)>=7;
                pready=random_bits[0];lready=random_bits[1];
                if(hold_pending && (presponse || lresponse)) begin hold_pending=0;hold_active=1;hold_left=43;admitted_before=pa+la;returned_before=returns;end
                if(hold_active) begin
                    pready=owner;lready=!owner;
                    if(pa+la!=admitted_before || returns!=returned_before) $fatal(1,"TB_FAIL nonowner ready released ownership");
                    hold_checks=hold_checks+1;hold_left=hold_left-1;
                    if(hold_left==0) begin hold_active=0;pready=1;lready=1;end
                end
            end
            @(negedge clk);pvalid=0;lvalid=0;pready=0;lready=0;
            if(pa!=target_pa || la!=target_la) $fatal(1,"TB_FAIL batch request count");
        end
    endtask
    initial begin
        if(!$value$plusargs("WORDS=%s",words_path)||!$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"TB_FAIL missing vectors");
        $readmemh(words_path,words);trace_file=$fopen(trace_path,"w");
        if(!trace_file) $fatal(1,"TB_FAIL trace open");
        $fwrite(trace_file,"owner,address,admission,physical_accept,response_consume,transaction_cycles\n");
        common_reset;batch(32,32,1);batch(9,0,0);batch(0,9,0);
        if(rr_checks<25 || hold_checks!=43 || pa!=pr || la!=lr || reads!=returns) $fatal(1,"TB_FAIL boundary coverage");
        $display("METRIC completed_parameter=%0d completed_lut=%0d physical_reads=%0d returns=%0d rr_checks=%0d hold_checks=%0d param_wait_max=%0d lut_wait_max=%0d transaction_min=%0d transaction_max=%0d transaction_sum=%0d",pa,la,reads,returns,rr_checks,hold_checks,p_wait_max,l_wait_max,latency_min,latency_max,latency_sum);
        // Common reset while admitted but not yet physically accepted.
        reader_gate=0;pvalid=1;paddr=13'd73;
        while(!(pvalid && paccept)) @(negedge clk);
        @(negedge clk);pvalid=0;if(!outstanding || physical_seen) $fatal(1,"TB_FAIL queued reset setup");
        common_reset;batch(2,2,0);
        // Common reset with the real reader response held by its owner.
        pvalid=1;paddr=13'd6795;reader_gate=1;pready=0;lready=1;
        while(!(pvalid && paccept)) @(negedge clk);
        @(negedge clk);pvalid=0;
        while(!presponse) @(negedge clk);
        repeat(11) @(negedge clk);common_reset;batch(2,2,0);
        $display("METRIC queued_common_reset=1 held_response_common_reset=1 actual_reader_instances=1 physical_latency_model=unchanged request_ready_interposer=1");
        $fclose(trace_file);$display("TB_PASS_ROM_ARBITER_BOUNDARY");$finish;
    end
    initial begin #20000000;$fatal(1,"TB_FAIL boundary watchdog");end
endmodule
