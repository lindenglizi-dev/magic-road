# ROI 证据与人工审阅包

打开 `index.html` 查看三对已存 ROI 与 27 项人工待审面板。六张 32×32 ROI 已嵌入 HTML；待审面板作为包内文件引用。

页面导出的 `review.json` 会保留 schema/version、27 个 review ID、每张面板的原始 SHA-256，以及来源清单和 receipt 哈希。未选择项保持 `pending`。保护对照不得填写背景子类。

本包没有解码视频、重裁剪、重提特征、重评分、训练或阈值扫描。人工确认尚未完成。
