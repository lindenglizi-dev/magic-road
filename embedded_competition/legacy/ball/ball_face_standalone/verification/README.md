# 整理检查

validation.json记录源码token一致性、工程引用、ROM、引脚和约束检查；安路原生工具已从本目录展开design_top_wrapper并加载三个相对路径ROM。仅三个ROM路径字面量进行了位置调整，硬件运算和控制逻辑保持一致。

files.sha256记录随包文件校验值，不包含其自身。release/SHA256.txt用于单独检查下载文件。

本次未重新布局布线或上板测试。README中的资源和时序属于原样保留的已发布bit，不是新目录重新布线的测量值。
