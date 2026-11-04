# 大文件获取与训练权重恢复

本目录保存公开资源获取入口、原始下载收据中的校验值、本机环境版本记录，以及自有学生模型训练检查点的去重备份。数据集本体、厂商软件安装包、许可证和第三方教师权重没有重新上传。来源见 [sources.json](sources.json)。

链接不是已完成的恢复测试：公开站点可能要求登录、旧版本可能变化，人工改过的标签也不能从原始数据集自动找回。删除原文件前须落实该文件对应的恢复方式。

## 自有训练权重

[weights_manifest.csv](weights_manifest.csv)记录原路径、SHA256、大小与备份对象。对象按内容只保存一份，多份冻结包或last/epoch别名通过清单恢复。没有反序列化或执行任何检查点，没有新训练，也不代表这些研发检查点已通过部署验收。

在本目录执行以下命令，仅验证备份，不修改原项目：

```powershell
python restore_weights.py
```

需要恢复时，指定一个新的目录：

```powershell
python restore_weights.py --restore-to E:/restored_roadyolo
```

脚本将按原有cnn/runs和cnn/releases相对路径恢复。存在同哈希文件会保留，存在不同内容则停止，禁止覆盖；本目录不包含运行模型所需的全部数据集。RoadYOLO源码与实验记录见 [work/roadyolo](https://github.com/lindenglizi-dev/magic-road/tree/work/roadyolo)；训练环境版本记录不是已经测试通过的重装锁文件。

## 公开资源获取入口

| 资源 | 获取入口与现有记录 | 清理条件 |
| --- | --- | --- |
| COCO 2017 | [官方页面](https://cocodataset.org/#download)，sources.json记录train2017/val2017原下载URL、大小与历史SHA256 | 原始包可在不再使用时清理；人工标签、分组、映射和转换配置必须另外备份；本轮未重下载核验。 |
| VisDrone VID train/val | [作者仓库](https://github.com/VisDrone/VisDrone-Dataset)，原Google文件ID与作者README匹配 | 保存版本、原始SHA256与转换配置；Google下载未在本轮执行。 |
| Intersection-Flow-5K | [作者仓库](https://github.com/AstronZh/Intersection-Flow-5K)链接到[Kaggle数据页](https://www.kaggle.com/datasets/starsw/intersection-flow-5k) | 本地v4文件与Kaggle对应版本尚未实下载核验，先保留；按作者许可获取。 |
| Tang Dynasty | [安路工具下载](https://www.anlogic.com/support/tools-downloads?tp=2)，本项目使用6.2.168116 | 官方入口需要权限且本轮直接访问超时；精确旧版安装包未核实可重新获取，因此先保留安装包。 |
| Python/PyTorch | [Python](https://www.python.org/downloads/)、[PyTorch历史版本](https://pytorch.org/get-started/previous-versions/) | 版本记录见training_environment_inventory.json；重建并跑通对应检查后再清理旧环境。 |
| Icarus Verilog | [官方文档](https://steveicarus.github.io/iverilog/) | 原安装为12.0开发版本；替代二进制尚未验证，且旧脚本有固定工具路径，先保留。 |

其他小规模来源，如VIRAT、PETS、MOT、EPFL、MIO及原始私有/人工数据，本轮尚未逐版本落实恢复入口，保持保留，不因本表存在就整体删除cnn/data。

## 保留边界

- 人工修订标签、裁剪/排除列表、训练/验证划分、类别映射及不可再生成的样本，必须有独立备份；官方数据入口不能替代它们。
- 原工程的厂商IP、ROM初始化文件、引脚/时钟约束和被旧绝对路径引用的源码继续保留。工具下载链接不能替代工程依赖。
- 五个约10GiB的rgb.bin路径是同一个文件的硬链接。删除其中四个链接不会释放约40GiB，也会改变历史路径可用性。
- 训练检查点备份不含所有教师文件，也不含训练数据。下载链接当前可见不等于已有逐文件恢复成功证明。
- 当前最终成品仍以final目录的说明、位流和验证记录为准，未上板状态保持。本次未删除任何本地原文件。
