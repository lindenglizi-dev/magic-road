# VIRAT 010107 开发验证扩展协调复核

日期：2026-09-27

## 结论

`VIRAT_S_010107_02_000282_000312` 已作为显式的 `dev_validation_extension` 完成输入校验、因果候选回放、冻结模型首轮评分和人工审核包生成。本批不修改历史 catalog，不进入训练，不用于阈值选择，也不构成 blind test 或 RTL 接入许可。

## 输入身份与映射 QA

- 视频：3,871,156 bytes，1280×720，479 帧，23.97 FPS；SHA-512 为 `a65ff0da41b340ba85033e8e9423b239377151b7a133203f4328e0f69756644107b731ee5ec78377b3804ff4cd12677f4720d8d8ea421aecc7ff63955de07ecd`。
- 标注：423,085 bytes，15,344 行，帧号覆盖 0–478；SHA-512 为 `1d045de5fc97c0f823e2fb91880f30f80929f688b6c9e8d2054cd2c90265a62f1e10114b12b572474edd43d58f988b233b60f56bba4a096341b14f2f4dd7c468`。
- 视频与标注分别匹配官方 Kitware item `56f587b88d777f753209cb94` 和 `56f57eeb8d777f753209c28f`。
- 协调者目视复核 frame 0、239、478：三帧视角、固定物和画幅一致，没有观察到平移或缩放；行人、车辆及 ignore 框与画面坐标对齐。该判断只覆盖抽查帧，不替代逐帧标注审计。
- QA 图见 `mapping_qa/contact_sheet_first_middle_last.jpg`，SHA-256 为 `a3b17484e06db048cc237ba10c91df0e0beff5621e9b02884b6fd5ea6d9056d7`。

## 因果回放与审核批次

- 背景模型从 frame 0 连续运行，前 120 帧作为 5.006 秒预热，不在三个区间重新初始化。
- 评分区间为 120–239、240–359、360–478，共 359 帧。
- baseline 产生 1,127 个候选；`fill_only_T100` 产生 1,401 个候选，其中 274 个为新增 small，所有 baseline 主候选均保留，单帧输出不超过 4。
- 按同一标注轨迹或确定性短时几何轨迹抽样，每条轨迹的代表间隔至少 30 个源帧，得到 83 个审核代表：main 53、small 30，覆盖 34 个时序轨迹。
- `review_manifest.csv` 是唯一权威人工输入。83 行的人工字段均为空；联系表 14 页、逐框全帧图 83 张、实际 32×32 ROI 83 张。`candidate_condition` 使用 `complete/truncated/merged/background_fragment/other`。
- 每张审核图同时显示同帧 baseline、fill-only 最终框、当前选中框、原组件框和实际分类 ROI。官方框只作提示；IoU < 0.1 时提示对象、类别和 IoU 均留空。

## 冻结边界与首轮评分

- 本轮固定 `experiment_roi_contract_v1`、T100、HOG64/HOG324 模型和依赖脚本哈希，详见 `receipt.json`。
- 没有重新训练、修改 SVM C、选择拒识阈值或改写历史 split。
- 对全部 1,401 个 fill-only 候选，HOG64 输出 ped/vehicle 为 1,127/274；HOG324 浮点与量化输出均为 799/602，二者标签不一致为 0。这些是未人工标注候选上的输出分布，不是准确率。
- VIRAT 标注并不穷尽所有目标；几何覆盖率不能当作检测召回。二分类 margin 不是概率，也没有 invalid 拒识能力。

## 未完成门禁

人工审核仍需为 83 个代表填写 `review_class`、`crop_usable`、遮挡/截断/粘连/背景碎片等字段。完成前不计算本场景分类指标、不改变 T100/HOG 选择、不导入训练、不冻结候选接口，也不编写生产 RTL。

最终 `virat_010107_02_t100/receipt.json` 的 SHA-256：`b25b7df3d24d051de6a0bad693871314334ad4ccef8aa8bd9e977a09ef261337`。
