"""固定SPPF单16B行缓存读次数；只计算逻辑请求序列，不代表DDR或RTL周期。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAPH = ROOT.parents[1] / "graph_artifacts/graph.json"


def physical(base, channels, y, x, channel):
    return base + (((y // 4) * 8 + x // 4) * 16 + (y % 4) * 4 + x % 4) * channels + channel


def read_count(stage, bases):
    previous, count = None, 0
    for ty in range(0, 18, 4):
        for tx in range(0, 32, 4):
            pool = stage in (1, 2, 3)
            span, offset, channels = (8, -2, 24) if pool else (4, 0, 96)
            for local_y in range(span):
                for local_x in range(span):
                    y, x = ty + local_y + offset, tx + local_x + offset
                    if not (0 <= y < 18 and 0 <= x < 32):
                        continue
                    for channel in range(channels):
                        if stage == 4:
                            base, stored, local_channel = bases[channel // 24], 24, channel % 24
                        else:
                            base, stored, local_channel = bases[0], channels, channel
                        line = physical(base, stored, y, x, local_channel) & ~15
                        if line != previous:
                            count += 1
                            previous = line
    return count


def main():
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {node["name"]: node for node in graph["nodes"]}
    names = ["csp4.out.conv", "sppf.squeeze.conv", "pool.00", "pool.01", "pool.02"]
    sources = [[nodes[name]["storage"]["base"]] for name in names[:4]]
    sources.append([nodes[name]["storage"]["base"] for name in names[1:]])
    counts = [read_count(stage, base) for stage, base in enumerate(sources)]
    assert counts[0] == 18 * 32 * 96 // 16
    assert counts[4] == 18 * 32 * 4 * 2
    # 单源24B像素会跨两条16B行；切换四个不同源使每段都必须重新读取。
    assert physical(100, 24, 0, 1, 0) == 124
    assert physical(100, 24, 4, 0, 0) == 100 + 8 * 16 * 24
    report = dict(status="PASS_FIXED_SPPF_READ_SCHEDULE", stage_reads=counts,
        policy="tile then row then column then channel; one persistent16B line per stage; stage boundary invalidates",
        pool_algorithm_padding=-128, physical_tail_fill=0, actual_DDR=False, RTL_cycles="UNKNOWN",
        graph_sha256=hashlib.sha256(GRAPH.read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT / "schedule_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(report["status"], counts)


if __name__ == "__main__":
    main()
