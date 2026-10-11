`timescale 1ns/1ps
module tb_measure_observer;
initial begin
  $dumpfile("E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/evaluation/measurements/pipeline/signals.vcd");
  $dumpvars(1, tb_roi_hog_svm_measure);
end
endmodule
