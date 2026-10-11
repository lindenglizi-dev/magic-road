`timescale 1ns/1ps
module tb_measure_observer;
initial begin
  $dumpfile("E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/evaluation/measurements/virat_000200_f1840_1859/signals.vcd");
  $dumpvars(1, tb_video_replay);
end
endmodule
