# 本地 Git 使用说明

建立日期：2026-10-11。仓库根目录为 `E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision`，不包含上级目录中的其他项目。

## 分支

- `main`：整理时的初始代码基线。
- `work/roadyolo`：初始工作分支，后续改动默认在这里提交。
- 2026-10-25 用户指定上传到 `git@github.com:lindenglizi-dev/magic-road.git`。上传当前 `work/roadyolo` 分支，保留远端已有 `master`；不强制推送、不改远端设置。可以直接向该仓库的 HTTPS 地址推送，不要求修改现有远程配置。

## 纳入版本管理的内容

RTL、Python、测试、脚本、约束、工程配置、文档、较小的标签/清单/验证报告，以及 ROM 初始化和小型数值测试包均保留。`reports/` 内有实际源码和冻结候选，不能整目录忽略。

`.gitattributes` 关闭自动换行转换，保存现有文件字节，避免破坏冻结源码的哈希收据。

## 仍保留在本机的内容

图片、视频、压缩包、训练权重、训练数组/像素缓存、位流、仿真编译结果、波形、TD 数据库、生成网表和完整 `.timing` 报告由 `.gitignore` 排除。既有超过 5 MiB 的数据清单、日志或生成报告逐路径列在 `.gitignore` 末尾；这是初始化快照清单，Git 不会自动忽略未来新增的大文件。原文件没有移动或删除。

历史检查器 `cnn/hw_validation/production/reports/v5_checker_adapter_20261005/retained_test_inputs/` 内有无法读取的临时目录，因此该目录未入库，未改动其权限。

2026-10-25 上传整理沿用上述规则：新增的 242 个超过 5 MiB 的生成报告、轨迹、物理网表和依赖安装包逐路径补入 `.gitignore`，不是忽略整个验证目录。所有原件留在本机，没有删除或修改功能 RTL。具体上传边界见 `GITHUB_UPLOAD_SCOPE.txt`。

Git 是代码与小型证据的版本记录，不是整个约 178 GiB 工作目录的完整备份。新克隆需要另行准备被忽略的数据、权重和构建产物；完整复现实验还可能依赖上级目录、工具安装路径及原始大型报告。已有报告中的状态也不代表本次重新验证了模型或 FPGA。

## 日常操作

在仓库根目录查看改动，再按明确文件提交：

```powershell
git status
git diff
git add -- path/to/changed_file
git commit -m "Describe the change"
```

需要检查文件为何未入库时，使用 `git check-ignore -v -- path/to/file`。提交前核对新增文件体积，避免强制加入被排除的数据、权重或构建产物。当前任务只验证 Git 纳管及文件完整性，没有运行训练、仿真、综合或上板操作。
