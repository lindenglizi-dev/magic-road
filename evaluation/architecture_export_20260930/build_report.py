"""Build the architecture report from verified local evidence; no RTL changes."""
from pathlib import Path
import hashlib
import json
from html import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, NextPageTemplate, Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/pdf/road_vision_architecture_report_20260930.pdf'
pdfmetrics.registerFont(TTFont('CN', 'C:/Windows/Fonts/msyh.ttc', subfontIndex=0))
INK = colors.HexColor('#173451')
BLUE = colors.HexColor('#3872b8')
styles = {
    'title': ParagraphStyle('title', fontName='CN', fontSize=27, leading=39, textColor=INK, spaceAfter=18),
    'h1': ParagraphStyle('h1', fontName='CN', fontSize=20, leading=29, textColor=INK, spaceAfter=15),
    'h2': ParagraphStyle('h2', fontName='CN', fontSize=13, leading=20, textColor=BLUE, spaceBefore=11, spaceAfter=6),
    'body': ParagraphStyle('body', fontName='CN', fontSize=10.5, leading=17, textColor=INK, spaceAfter=9, wordWrap='CJK'),
    'small': ParagraphStyle('small', fontName='CN', fontSize=8.4, leading=12.5, textColor=colors.HexColor('#586a7b'), spaceAfter=6, wordWrap='CJK'),
    'cell': ParagraphStyle('cell', fontName='CN', fontSize=9.1, leading=14, textColor=INK, wordWrap='CJK'),
}
story = []

def p(s, kind='body'):
    return Paragraph(escape(s).replace('\n', '<br/>'), styles[kind])

def add(s, kind='body'):
    story.append(p(s, kind))

def table(headers, rows, widths):
    data = [[p(v, 'cell') for v in headers]] + [[p(str(v), 'cell') for v in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8f1ff')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f7fa')]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LINEBELOW', (0,0), (-1,0), .7, colors.HexColor('#b8cbe0')),
    ]))
    story.extend([t, Spacer(1,10)])

def page(title):
    story.append(PageBreak())
    add(title, 'h1')

def chrome(c, doc):
    w, h = c._pagesize
    c.setFont('CN', 8)
    c.setFillColor(colors.HexColor('#637488'))
    if doc.page != 2:
        c.drawString(42, h-27, '道路视觉项目  /  架构与验证状态')
    c.drawString(42, 23, '2026-09-30  |  工程诊断报告，非正式验收结论')
    c.drawRightString(w-42, 23, str(doc.page))

doc = BaseDocTemplate(str(OUT), pagesize=A4, title='道路视觉项目：整体架构与验证报告', author='项目工程报告', leftMargin=42, rightMargin=42, topMargin=52, bottomMargin=43)
doc.addPageTemplates([
    PageTemplate(id='portrait', frames=Frame(42,43,A4[0]-84,A4[1]-95, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0), onPage=chrome, pagesize=A4),
    PageTemplate(id='diagram', frames=Frame(25,35,landscape(A4)[0]-50,landscape(A4)[1]-48, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0), onPage=chrome, pagesize=landscape(A4)),
])

add('道路视觉项目\n整体架构与验证报告', 'title')
add('FPGA 视频链 · 运动候选定位 · HOG / SVM · Python 诊断', 'h2')
add('版本：2026-09-30　｜　范围：当前实现、历史验证、待完成接口与改进顺序', 'small')
add('报告结论', 'h2')
add('现有工程已形成摄像头、显示、运动检测、四目标跟踪及 ROI/HOG64 特征支路。训练分类模型尚未完成正式顶层闭环；HDMI 框颜色当前来自几何规则。HOG324 是 Python 中的诊断模型，不能视为 FPGA 已运行的分类器。')
add('当前优先问题是候选定位质量：目标信息可能在前景分割、Run 清理、连通域容量和 Top4 选择中损失。独立真值框分类也显示行人适配不足，因此需要分开验证定位与分类，不能用一个整体“正确率”掩盖原因。')
table(['状态', '本报告采用的口径'], [
    ['已实现', 'RTL 源码和模块链路存在；不自动等同于全系统板级验证通过。'],
    ['历史验证', '既有文档或报告记录的回归、综合、时序结果；本次没有重跑。'],
    ['当前诊断', '局部 Python 回放和用户确认样本所得结果，注明分母和边界。'],
    ['待完成', '真实分类接入、完整整数 HOG324、CDC/bank 完整测量和独立测试。'],
], [90,421])
add('阅读路径', 'h2')
add('第2页：整体架构图；第3-5页：前端、跨域与模型；第6-7页：数据及错误定位；第8页：重要选择；第9页：资源与验证；第10页：实施顺序和证据入口。')
add('本次仅生成文档。生产 RTL、训练权重、人工原始标注和历史结果保持不变。旧架构文档中“稳定”“不会错配”等措辞在本报告中作为设计目标处理，不替代尚未完成的系统证据。', 'small')

story.extend([NextPageTemplate('diagram'), PageBreak()])
story.append(Image(str(ROOT/'evaluation/architecture_export_20260930/current_architecture.png'), width=724, height=724*1640/2200))
story.append(NextPageTemplate('portrait'))

page('01  视频主链与运动检测前端')
add('显示与分析各自承担什么', 'h2')
add('SC500 输出 MIPI RAW10，经解包、ISP、去马赛克及 AWB 得到 1280×720 RGB。显示主链经过视频打包和 DDR 帧缓存，再叠加框与状态输出 HDMI。分析旁路从 AWB 抽样，不把 256×144 分析图直接作为 HDMI 画面。')
table(['环节', '当前规则', '检查重点'], [
    ['抽样与灰度', '横纵各每5像素取点；灰度=(R>>2)+(G>>1)+(B>>2)，输出256×144。', '点采样会改变细小目标信息；不能假设与面积缩小等价。'],
    ['背景模型', '前4帧学习；差分阈值20；缓慢更新，前景可冻结背景更新。', '阴影、停车线附近变化与持续前景；必须保护真实运动目标。'],
    ['3×3 清理', '边界补零；中心必须为前景，邻域前景点数至少3。', '孤立噪声减少时，细肢体或断裂目标是否同时丢失。'],
    ['Run 提取', '最短水平连续长度2；每行最多64个 run。', '细窄信号消失、连通形状变化和行容量。'],
    ['RLE-CCL', '8连通；标签合并和框/面积统计；每帧最多32标签。', '标签在面积筛选之前分配；小碎片也占用容量。'],
    ['Top4 与跟踪', '面积至少16，按面积选择最多4框；临时几何分类后提交对象表。', '面积大不等于完整目标；检查同帧竞争和错误帧处理。'],
], [82,230,199])
add('当前容量风险', 'h2')
add('已选典型 Mask 的组件数为48、70、81、78、80，均大于32。源码中标签只在帧清除时重置，帧内分配后不回收；最终组件数还可能低于临时标签需求。这说明容量存在风险，但本轮默认容量 RTL 回放尚无完成报告，不能据此直接给出板上漏检数量。')
add('对应模块：awb96_analysis_adapter、background_model、binary_cleanup_3x3、run_detector、label_manager、rle_ccl_top、top4_selector、object_frame_store。来源：[S1][S3]。', 'small')

page('02  帧缓存、跨时钟域与显示一致性')
table(['时钟域', '主要职责', '跨域对象'], [
    ['S_csi_rx_clk', '视频分析、背景、CCL、跟踪及事件。', '源帧灰度、候选框、跟踪表。'],
    ['S_100m_clk', '灰度 RAM 读口、ROI 读取、Sobel 与 HOG。', '候选任务及对应 bank / 源帧号。'],
    ['S_hdmi_pixel_clk', '完整视频画面、框与状态叠加。', '冻结后的跟踪或分类结果表。'],
], [108,209,194])
add('已有结构与必须继续验证的边界', 'h2')
add('双 bank 灰度缓存保存256×144×8 bit帧。ROI快照携带候选框和源帧编号，读取器执行帧号配对，再把每个框缩放成1024像素的32×32 ROI。已有所有权、错误帧、非法释放等检查逻辑，但这些局部保护不能替代连续采集下的完整事务验证。')
add('必须记录：写入开始、EOF、候选完成、Tracker完成、任务发布、目的端元数据复制、最后一次RAM返回数据捕获、ack及源端释放。完整占用时间包含等待候选、跨域同步和读访问，不能只使用HOG/SVM计算周期。')
add('后续最小协议方向（尚未冻结或接入）', 'h2')
add('采用单任务串行：源端发布 {source_frame_id, bank_id, bank_generation, boxes}，保持 payload 与 bank 内容稳定；目的端检测请求后复制元数据并读取ROI。ack只在最后一次同步RAM读数据已被捕获后产生，表达“本任务不会再读取该bank”；不等待后续HOG/SVM分类完成。')
add('源端收到同步后的ack并核对事务身份后才释放bank。还需验证复位、重复事务、帧号回绕、同步延迟和同拍事件；不采用未经测量的N+2超时。只有连续吞吐证据不足时，才评估排队或独立释放通道。')
add('HDMI 表一致性与同帧对齐是两个问题', 'h2')
add('目标方案是结果快照携带source_frame_id，显示端完整复制后在下一次HDMI VSYNC生效，整幅画面冻结。与此同时记录生效HDMI帧号及与源帧的差值。只在VSYNC切表，可以避免一帧内表撕裂，却不能证明框与视频天然同帧。')
add('本页协议是后续接口评审的方向，不是当前RTL已经满足所有不变量的声明。来源：[S1][S2]及本轮已确定的协议约束。', 'small')

page('03  ROI、HOG 与线性分类模型')
table(['分支', '特征及计算', '当前状态'], [
    ['RTL HOG64', '32×32 ROI；30×30有效Sobel梯度；幅值近似|Gx|+|Gy|；4×4 cells，每cell 4方向，共64维。', '特征模块存在；历史确定性向量对拍记录为64项一致。'],
    ['RTL SVM64', '逐特征串行有符号乘加，再加偏置；已有独立内积核。', '训练权重ROM、HOG流正式连接、类别回写尚未闭环。'],
    ['Python HOG324', 'OpenCV HOG；描述子输出Q1.12，线性权重量化为int16。内部HOG仍有浮点计算。', '诊断模型；不是完整整数HOG，不能作为RTL等价证明。'],
], [88,251,172])
add('训练约束', 'h2')
add('64维与324维分别训练，不迁移权重。共同基线使用360个已审计真值框ROI：000201场景32 ped / 73 vehicle；000206场景128 ped / 127 vehicle。StandardScaler仅在train上拟合，LinearSVC采用C=1、class_weight=balanced，并将标准化代数折叠进线性权重和偏置。')
add('当前线性分类器强制输出ped或vehicle。没有拒识时，任何被作为输入的invalid都会被接受为其中一类，因此invalid误接受率基线为100%。分数是分类margin，不是置信概率。')
add('三种一致性不可混用', 'h2')
add('浮点与量化线性层：开发门禁允许标签差异率≤1%，各类召回下降≤1个百分点，符号翻转必须落在观测误差加一个LSB的margin范围内。此条件不等同于硬件位精确。')
add('浮点HOG与未来整数HOG：需分别定义梯度、方向桶、归一化及特征误差界。整数Python与RTL：ROI、特征、乘积、累加、分数和类别都要求逐级bit-exact，不能用分类比例容忍替代。')
add('后备路线', 'h2')
add('只有补充后的真实候选证据显示HOG324不足，或整数化代价不合适，才启动受限tiny-CNN：32×32灰度，三层步长2卷积1→8→16→24，全局均值池化和三分类。它是待评估路线，当前没有训练收益或FPGA资源结论。')
add('来源：[S1][S2][S6]。本轮不更新模型参数。', 'small')

page('04  数据、评估与证据边界')
add('评估单位必须保持一致', 'h2')
add('原片、摄像机scene、派生片段、帧号、原始类别、框坐标、许可及文件哈希共同定义样本。按scene划分集合，同机位连续片段和转码版本不得跨集合；时间相关帧不能当作大量独立样本。')
table(['数据 / 用途', '范围与约束'], [
    ['当前主要人工证据', 'intersection_2415171：用户已确认32帧，本轮只评移动人车；57次目标观测=46 ped+11 vehicle，来自4条相关轨迹。'],
    ['独立训练审核包', 'intersection_3785878：12个完整帧和24个去重候选已制作审核入口。现有状态记录仍待人工标签、来源许可和scene族确认；不自动导入训练。'],
    ['开发验证场景', 'VIRAT 000200 / 000203及显式扩展010107；旧候选部分含AI预标注，不能整体称为人工金标。'],
    ['历史候选实验', 'internal8只用于失败类型与回归证据；fill-only/T100保留历史收据，已不作为当前部署候选。'],
    ['独立测试保留', '010106 / 010108_01本轮未读取。历史广域检索存在标注文件访问记录，若要求操作系统级从未读取，需要另选未访问场景。'],
], [120,391])
add('本轮报告什么，不报告什么', 'h2')
add('定位使用类别无关的一对一匹配，主口径IoU≥0.5；正确定位且分类正确才算端到端命中。按ped、vehicle及阶段给出原始分子/分母。32帧仅支持抽样帧描述，不能代表整段视频、跨场景准确率或独立轨迹召回。')
add('缺少完整背景真值时，无法可靠给出整场景precision或invalid FAR。用户观察到移动阴影和停车线相关响应，可作为机制假设；没有逐框审核时不能把所有背景候选都归因于这两类。骑自行车者保持ignore，不混入ped、vehicle或invalid分母。')
add('冻结门禁', 'h2')
add('建议目标仍未冻结：Person Recall≥85%、Vehicle Recall≥90%、invalid FAR≤10%、整数Python/RTL分类不一致为0。模型冻结前需扩展至少3个独立验证scene，每类至少100个唯一时间组；参与逐scene判断的类别每scene至少20组，报告原始计数和Wilson区间。')
add('来源：[S2][S4][S5]。历史候选pilot的高分不能替代当前人审样本或正式测试。', 'small')

page('05  当前错误定位：问题在哪一层')
add('相同32帧、同一批移动目标；IoU≥0.5。以下是Python诊断，非本轮RTL容量回放。', 'small')
diag = json.loads((ROOT/'evaluation/local_scene_pilots/intersection_2415171_diagnostic_summary_v2/summary.json').read_text(encoding='utf-8'))
rows = []
for key, label in [('raw_all','原始前景：全部组件'),('clean_all','3×3清理后：全部组件'),('run_all','Run长度≥2后：全部组件'),('area16_all','面积≥16后：全部组件'),('top4','最终面积Top4'),('top8','扩大至Top8（诊断）')]:
    by = diag['stage_primary_iou05'][key]['by_class']
    rows.append([label] + [f"{by[c]['matched']}/{by[c]['targets']} ({by[c]['recall']:.1%})" for c in ['ped','vehicle']])
table(['定位阶段', '行人覆盖', '车辆覆盖'], rows, [245,133,133])
add('结论一：候选框质量是当前首要问题', 'h2')
add('原始前景全部组件也仅覆盖17/46个行人观测；Run后降至12/46，Top4再降至11/46。把Top4改成Top8只多覆盖一个行人，不能解释或补回主要损失。前景中存在变化信号，也不意味着连通域框满足目标定位要求。')
add('结论二：直接放宽Run不能作为修复', 'h2')
table(['固定其他环节的对照', '行人', '车辆'], [
    ['Run最短2→1：定位覆盖', '11/46 → 15/46', '3/11 → 5/11'],
    ['定位且HOG324分类正确', '7/46 → 4/46', '2/11 → 4/11'],
], [245,133,133])
add('行人正确数变化可分解为：新增命中+2，定位丢失−2，分类翻转−3，合计−3。三个翻转在浮点和量化模型中都存在，不能归因于量化独有错误；因此不直接部署min_run=1。')
add('结论三：分类器也需要独立适配', 'h2')
add('使用分析图上的人工真值框裁ROI，HOG324仍仅正确13/46个行人，车辆10/11。前端修复不能自动解决分类问题；但分类训练也不能补回未产生的目标框。当前Top4端到端正确为行人7/46、车辆2/11。')
add('来源：[S4][S5]。96个Mask的Python/OpenCV与独立DFS比较零差异，只证明软件组件实现间一致。', 'small')

page('06  重要架构选择与保留理由')
table(['选择', '证据与判断', '当前落点'], [
    ['保留官方视频主链', '显示与分析解耦，能独立观察原画面与算法输出。', '不因模型实验重构ISP/DDR/HDMI。'],
    ['先Python再RTL', '真实数据暴露候选和分类两种失效；过早固定接口会固化错误假设。', '协议、算法先可复现，再冻结整数合同。'],
    ['HOG64扩展到HOG324诊断', '历史真值框诊断中HOG324优于64维；HOG144准确率更低且维度更高。', '继续诊断HOG324，但未证明跨场景可部署。'],
    ['拒绝内部8统一排序直接上线', '开发实验曾提高行人几何覆盖，却挤掉已有车辆主候选。', 'internal8保留为失败证据，不进入训练或阈值选择。'],
    ['停止继续微调T100规则', 'fill-only人审裁剪可用率不足；新开发scene出现大量无效候选。', '不把透视阈值当作通用解法，不冻结该RTL接口。'],
    ['不直接移除Run过滤', '定位数量增加，但行人端到端正确数7→4。', '保留基线，先找框形状与选择机制变化。'],
    ['前端优先、分类随后', '主要漏检在Top4之前已存在，真值框分类也弱。', '先对拍实现，再做一次背景分割对照。'],
], [108,252,151])
add('不把“背景更干净”当成优化验收', 'h2')
add('每个候选改动必须同时报告无效框减少、原有目标损失、新目标增加及实际ROI分类变化。观察图像更整洁，不足以证明检测质量提高。也不新增一个“有效目标SVM”来掩盖候选质量问题：其训练需要独立且可靠的invalid标注。')
add('受限候选窗口仅作为条件触发的实验', 'h2')
add('如果变化位置可找到、完整框却持续不合格，再验证“CCL位置线索＋少量受限窗口”。预先限定候选数和搜索范围，比较配对收益与损失；不继续堆叠面积、扩框或持续性筛选规则。')
add('来源：[S2][S4][S5]以及本轮确定的前端优先策略。本页记录选择依据，不意味着新增模型或接口已实施。', 'small')

page('07  资源、周期与验证成熟度')
add('历史综合结果：仅作为旧基线参考', 'h2')
table(['资源 / 时序', '文档记录', '解读'], [
    ['LUT6', '15,693 / 21,216（73.97%）', '不是HOG324新增后的占用。'],
    ['Slice', '18,003 / 21,216（84.86%）', '逻辑空间偏紧。'],
    ['Slice Register', '19,323 / 42,432（45.54%）', '不能单独据此推断整体可扩展性。'],
    ['ERAM20K', '94 / 108（87.04%）', '灰度双bank文档记载共36块；总BRAM余量有限。'],
    ['DSP', '9 / 40（22.50%）', 'DSP余量不等于布局和存储有余量。'],
    ['Setup / Hold', 'SWNS +0.110 ns / HWNS +0.020 ns', '历史静态时序余量小；本次未复跑实现。'],
], [112,226,173])
add('不使用计算夹具推断连续吞吐', 'h2')
add('已有四对象4176周期 / 41.76 μs记录只表示100 MHz计算夹具结果，不含实际采集、候选等待、CDC和bank占用，不能据此判定双bank够用。最终需要EOF→CCL→Tracker、任务等待、读完RAM、释放及丢帧的完整时间线。')
add('已知验证与尚缺证据', 'h2')
table(['证据', '可支持的结论'], [
    ['历史模块回归 / 合成向量', '文档记录10组RTL回归及HOG64、SVM自测；只说明对应夹具覆盖。'],
    ['24侧真实诊断向量', '12对ROI乘积和累加重算一致；观测峰值333,740,320在int32内。'],
    ['全局范围检查', '既有保守界17,092,089,828超过int32；不能用观测样本替代位宽证明。'],
    ['本轮缺口', '新Mask默认容量RTL报告、MOG2固定对照完成报告、整数HOG324逐级RTL对拍、连续bank占用及板级验证。'],
], [150,361])
add('来源：[S1][S2][S5]。资源数字为旧文档转录，未重新核验原始工具报告与当前源码哈希是否一致。', 'small')

page('08  下一步执行顺序与证据入口')
table(['顺序', '工作和停止条件'], [
    ['1. 短段RTL对拍', '仅用保存的典型Mask，先用正式32标签容量对run、CCL、框与溢出；扩大容量只能作为隔离原因的诊断。无需重跑整段视频。'],
    ['2. 一次背景对照', '其他参数固定，连续背景状态从frame0保持；固定MOG2方案与基线配对比较合格框、新增和丢失目标。失败也保留结果，不追加参数扫描。'],
    ['3. 必要时受限窗口', '仅在变化位置存在、组件框持续不合格时启动；设定候选预算，报告每个已有目标的得失。'],
    ['4. 独立分类适配', '确认独立训练标注和来源后，做一次固定C=1的HOG324适配。32帧开发验证不进入训练，不联动调整候选和拒识阈值。'],
    ['5. 冻结并最小接入', '数据与模型证据合格后，冻结候选、整数格式和阈值；Python协议不变量通过后评审接口，再写RTL。正式测试只在冻结后进行。'],
], [106,405])
add('可复现证据索引', 'h2')
refs = [
    ('S1', 'CURRENT_ARCHITECTURE.md', '模块职责、历史回归及资源记录；其中后续计划已由新证据更新。'),
    ('S2', 'evaluation/status.json', '当前状态与历史决策汇总；本轮前端优先级以最新用户约定补充。'),
    ('S3', 'user_source/hdl_source/road_vision/label_manager.v', '默认MAX_LABEL=32及帧内分配行为。'),
    ('S4', 'evaluation/local_scene_pilots/intersection_2415171_diagnostic_summary_v2/summary.json', '32帧逐阶段定位计数、真值框与候选ROI诊断。'),
    ('S5', 'evaluation/local_scene_pilots/intersection_2415171_crop_change_v2/summary.json', '候选变化及错误归因；量化细节另见同目录族margin_change_v1。'),
    ('S6', 'external_reference_exploration/results/opencv_hog_diagnostic/model_parameters.json', '已固定诊断模型参数；本次不重新训练。'),
]
for key, path, note in refs:
    add(f'[{key}] {path}\n{note}', 'small')
add('上述路径均相对于 lab1_sc500_road_vision。随报告生成 evidence_receipt.json，记录本次实际读取来源与架构图的SHA-256；该收据仅用于追溯，不代表重新执行了所有历史实验。', 'small')

doc.build(story)
reader = PdfReader(str(OUT))
assert len(reader.pages) == 10, f'Unexpected page count: {len(reader.pages)}'
for n, pg in enumerate(reader.pages):
    if n != 1:
        assert len(pg.extract_text() or '') > 100, f'Empty text page {n+1}'
assert float(reader.pages[1].mediabox.width) > float(reader.pages[1].mediabox.height)
files = [path for _, path, _ in refs] + ['evaluation/architecture_export_20260930/current_architecture.png', 'evaluation/architecture_export_20260930/build_report.py']
receipt = {'as_of':'2026-09-30', 'purpose':'architecture_document_only', 'pages':10, 'production_rtl_changed':False, 'sources':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files if (ROOT/f).is_file()}, 'output_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()}
(OUT.parent/'evidence_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'pdf':str(OUT),'pages':len(reader.pages),'bytes':OUT.stat().st_size}, ensure_ascii=False))
