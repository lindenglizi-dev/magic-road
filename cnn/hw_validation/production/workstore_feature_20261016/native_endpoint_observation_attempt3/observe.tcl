run 7 ns
for {set sample 0} {$sample < 300} {incr sample} {
    set baccept [examine -radix unsigned /tb_feature_workstore/accepted_byte]
    set bvalid [examine -radix unsigned /tb_feature_workstore/byte_rsp_valid]
    set bnative [examine -radix unsigned /tb_feature_workstore/native_byte]
    set waccept [examine -radix unsigned /tb_feature_workstore/accepted_weight]
    set wvalid [examine -radix unsigned /tb_feature_workstore/weight_rsp_valid]
    set wnative [examine -radix unsigned /tb_feature_workstore/native_weight]
    puts "NATIVE_ENDPOINT sample=$sample baccept=$baccept bvalid=$bvalid bnative=$bnative waccept=$waccept wvalid=$wvalid wnative=$wnative"
    run 10 ns
}
quit -code 0
