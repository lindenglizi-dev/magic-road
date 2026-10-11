`timescale 1ns/1ps
module tb_measure_observer;
initial begin
  $dumpfile("E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/evaluation/measurements/svm/signals.vcd");
  $dumpvars(1, tb_hog_linear_svm);
end
endmodule
