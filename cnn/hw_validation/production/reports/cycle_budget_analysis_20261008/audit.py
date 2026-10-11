"""Read frozen v19 evidence; reconstruct the conditional ledger, not FPS."""
import collections
import hashlib
import json
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    production = here.parents[1]
    paths = {
        'base': production / 'reports/v10_postprocess_overlap_20261007/verification/budget/shape_budget.json',
        'budget': production / 'reports/v19_mac_short_closure_20261008/verification/layer_cycle_budget.json',
        'generator': production / 'reports/v19_mac_short_closure_20261008/reference/generate_layer_budget.py',
        'log': production / 'reports/v19_mac_short_closure_20261008/verification/tile_final.log',
        'graph': production / 'graph_artifacts/graph.json',
    }
    hashes = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}
    base = json.loads(paths['base'].read_text(encoding='utf-8'))
    budget = json.loads(paths['budget'].read_text(encoding='utf-8'))
    graph = json.loads(paths['graph'].read_text(encoding='utf-8'))
    nodes = {node['name']: node for node in graph['nodes']}
    totals = collections.Counter()
    kinds = collections.Counter()
    blocks = collections.Counter()
    rows = []
    tile_boundaries = 0
    for old, current in zip(base['layers'], budget['layers'], strict=True):
        assert old['name'] == current['name']
        jobs = current['conditional_mac_jobs']
        groups = old['mac_input_groups_per_job']
        if old['kind'] == 'depthwise':
            groups = 2 if nodes[old['name']]['stride'] == [1, 1] else 3
        send = jobs * groups
        storage = send - (jobs if old['kind'] == 'pointwise' and old['input_hwc'][2] == 16 else 0)
        wait = 7 * jobs
        dw_post = 4 * current['spatial_triplets']
        boundary = old['conditional_layer_boundary_cycles'] + int(old['activated_silu'])
        components = dict(storage=storage, send=send, wait=wait, dw_post=dw_post, boundary=boundary)
        cycles = sum(components.values())
        assert cycles == current['v19_conditional_cycles'], old['name']
        height, width, _ = old['output_hwc']
        tiles = ((height + 3) // 4) * ((width + 3) // 4)
        tile_boundaries += boundary * tiles
        totals.update(components)
        kinds[old['kind']] += cycles
        blocks[old['name'].split('.')[0]] += cycles
        rows.append(dict(name=old['name'], kind=old['kind'], cin=old['input_hwc'][2],
                         shape=old['output_hwc'], groups=groups, jobs=jobs, cycles=cycles,
                         tiles=tiles, **components))
    total = sum(totals.values())
    assert len(rows) == 67 and total == budget['v19_conditional_cycles'] == 42628794
    assert totals == dict(storage=10714752, send=10788480, wait=18930240, dw_post=2193408, boundary=1914)
    assert 512 + 640 + 1792 + 256 + 56 + 1 == 3257
    assert 128 + 256 + 896 + 29 + 1 == 1310
    assert sum(row['jobs'] for row in rows) == 2704320
    lines = ['# v19 周期占比清单与合理性分析', '',
             '本报告只重建冻结账本。42,628,794 拍是条件外推，不是整网仿真、板测或严格上下界。未修改 RTL 或旧报告。', '',
             '## 一 互斥周期分类', '', '| 类别 | 周期 | 占比 | 来源 |', '|---|---:|---:|---|']
    descriptions = {
        'storage': '任务操作数准备；默认每组一拍，仅 Cin16 PW 预取少一拍。不是 DDR 等待。',
        'send': 'MAC 输入握手；每任务 G 组，每组一拍，无输入反压。',
        'wait': '每任务末组接受至结果 ACK 的 7 拍；已删除 3 拍纯延迟，不等于剩余全可删。',
        'dw_post': '每四点段的三点任务与尾任务，额外串行交付 3+1 拍；不是全部 SiLU 忙周期。',
        'boundary': '沿旧账本每层固定尾部，再为激活层加一拍；只计每层一次。',
    }
    for key, value in totals.items():
        lines.append(f'| {key} | {value:,} | {value / total:.2%} | {descriptions[key]} |')
    lines += ['', '## 二 卷积类别及网络块', '', '| 卷积类别 | 周期 | 占比 |', '|---|---:|---:|']
    for key, value in kinds.items():
        lines.append(f'| {key} | {value:,} | {value / total:.2%} |')
    lines += ['', '| 网络块 | 周期 | 占比 |', '|---|---:|---:|']
    for key, value in blocks.most_common():
        lines.append(f'| {key} | {value:,} | {value / total:.2%} |')
    lines += ['', '## 三 实测校准与适用范围', '',
              '- down2 DW→PW 4×4 无停顿小块：512 准备 + 640 发射 + 1,792 收尾等待 + 256 DW 串行交付 + 56 排空 + 1 完成 = 3,257 拍。预装载 2,894 拍、导出 449 拍另计。',
              '- PW 独立小块：128 准备 + 256 发射 + 896 收尾等待 + 29 排空 + 1 完成 = 1,310 拍；组合链中的 PW 端点为 1,309，计时边界差一拍，不能混用。',
              '- PW 随机输入反压额外 284 拍，实际 1,594；完整小块随机提交反压实际 3,259。这些等待未添加到无停顿帧预算。',
              '- 完整小块 MAC/pre/SiLU/post/writeback 忙计数分别 3,200/2,690/1,920/2,561/640。这些区间重叠，不能相加到核心总周期。不能仅由忙周期推断模块 II。',
              '- 当前真正校准的是 down2 stride2 DW16 和 PW16→24。其余形状，包括 stride1 DW、Stem、深通道 PW、预测头和真实动态量化参数，仍是外推。', '',
              '## 四 合理性与预算缺口', '',
              f'- 算术量 214,465,536 MAC / 24 = 8,936,064 理想拍，实际发射账本 {totals["send"]:,} 拍。差异来自分组、尾路和 DW 稀疏打包空槽；峰值 MAC 拍数不包含准备、收尾和数据搬运。',
              '- 当前问题主要是任务粒度与单任务周转：2,704,320 个任务各付 7 拍，累计 18,930,240。MAC 组内 II=1 不代表任务之间 II=1。剩余 7 拍含真实计算、结果发布/确认，不能按纯空拍直接删除。',
              '- 准备与发射仍分开。账本假定全部层能沿小块同节拍取数，没有证实 ROM/片上端口或 DDR 能支持。先量出真正输入等待，再决定小范围预取/复用，避免堆通用缓存。',
              '- 层尾只计 1,914 拍，不是逐 tile 排空证明。如果每个 4×4 tile 都复用这种独立探针启动/排空，成本会明显增大；连续图执行可能隐藏部分开销，但目前没有证明。',
              f'- 敏感性示例：逐输出 tile 重复当前每层尾常数将为 {tile_boundaries:,} 拍，比账本多 {tile_boundaries - totals["boundary"]:,} 拍。这不是已测开销，也不强行加入原预算；说明只计每层一次的假设不能用于吞吐验收。',
              '- 未计：DDR/权重等待、tile 装卸与 DMA、池化/残差/视图操作、解码/Top-K/NMS、真实动态量化与 INT16 预测、视频竞争及层间屏障。不能把 42,628,794 拍解释为含这些环节的上界。',
              '- 100 MHz 下条件账本为 426.288 ms，倒数约 2.346 FPS；不是实际 FPS。5 FPS 预算 20,000,000 拍，当前条件账本已超 22,628,794 拍。',
              '- 下一项决策优先看任务周转和占比最大的 head2，不在小比例层尾上投入大量结构。先补参数链并测代表层；任务重叠若需改核契约另行决定。H24 是单一备选，不能凭当前外推宣称足够达标。', '',
              '## 五 67 层清单', '',
              '普通/PW：G=ceil(Kh×Kw×Cin/8)，J=H×W×ceil(Cout/3)，周期=J×(2G+7−Cin16预取标志)+层尾。',
              'DW：T=H×(W/4)×C，J=2T；stride1 G=2，stride2 G=3；周期=T×[2×(2G+7)+4]+层尾。stride2 尾任务也沿当前调度保留 G3。', '',
              '| 层名 | 输出 H×W×C | Cin | G | 任务 | 准备 | 发射 | 等待 | DW交付 | 层尾 | 总拍 | 占比 |',
              '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        shape = '×'.join(map(str, row['shape']))
        lines.append(f'| {row["name"]} | {shape} | {row["cin"]} | {row["groups"]} | {row["jobs"]:,} | {row["storage"]:,} | {row["send"]:,} | {row["wait"]:,} | {row["dw_post"]:,} | {row["boundary"]} | {row["cycles"]:,} | {row["cycles"]/total:.2%} |')
    lines += ['', '## 六 来源与绑定', '']
    for key, path in paths.items():
        lines.append(f'- [{key}]({path.as_posix()})；SHA256 `{hashes[key]}`。')
    lines += ['', '总结：账本算术可逐层复核，但仅两种 down2 形状有小块校准。主要成本是收尾周转以及分离的操作数准备/发射，不是所有模块忙周期相加。真实整网调度、带宽和参数链完成前，不能用该账本宣布 5 FPS。', '']
    assert hashes == {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}
    (here / '周期占比与合理性报告.md').write_text('\n'.join(lines), encoding='utf-8')
    (here / 'cycle_breakdown.json').write_text(json.dumps(dict(total=total, components=totals, kinds=kinds,
        blocks=blocks, rows=rows, source_hashes=hashes, naive_tile_boundary_sensitivity=tile_boundaries), indent=2), encoding='utf-8')
    print(json.dumps(dict(total=total, components=totals, kinds=kinds, blocks=blocks,
                         tile_boundaries_sensitivity=tile_boundaries, checks='67 rows match; source hashes unchanged'), indent=2))


if __name__ == '__main__':
    main()
