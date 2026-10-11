"""Run existing benches with a passive VCD observer; never edit design RTL."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import gzip
import shutil
from pathlib import Path


def summarize_vcd(path: Path, clock: str, reset: str, watched: list[str]) -> dict:
    """Sample final values per VCD timestamp on clock rising edges (post-NBA)."""
    codes, values, samples = {}, {}, {s: [] for s in watched}
    stack = []
    timestamp = 0
    rising = False
    tick = 0
    scale = "unknown"
    def flush():
        nonlocal tick
        if rising:
            tick += 1
            if values.get(reset) == "1":
                for signal in watched:
                    if values.get(signal) == "1":
                        samples[signal].append(tick)
    with path.open(encoding="ascii") as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith("$scope"):
                stack.append(line.split()[2])
            elif line.startswith("$upscope"):
                stack.pop()
            elif line.startswith("$var"):
                parts = line.split()
                if len(stack) == 1:
                    codes.setdefault(parts[3], []).append(parts[4])
            elif line.startswith("#"):
                flush()
                timestamp = int(line[1:])
                rising = False
            elif line and line[0] in "01xz":
                for name in codes.get(line[1:], []):
                    if name == clock and line[0] == "1" and values.get(name) == "0":
                        rising = True
                    values[name] = line[0]
            elif line.startswith("b"):
                bits, code = line[1:].split()
                for name in codes.get(code, []):
                    values[name] = bits
            elif line in {"1ps", "1ns", "10ps", "10ns"}:
                scale = line
    flush()
    summary = {}
    for signal, cycles in samples.items():
        runs = []
        for cycle in cycles:
            if runs and cycle == runs[-1][1] + 1:
                runs[-1][1] = cycle
            else:
                runs.append([cycle, cycle])
        summary[signal] = {"asserted_cycles": len(cycles), "runs": runs}
    return {"sampling": "post-NBA at rising clock edges; cycles local to selected clock",
            "clock": clock, "vcd_timescale": scale, "last_timestamp": timestamp,
            "signals": summary}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench", choices=["video", "roi", "hog", "svm", "bank", "pipeline"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frames", type=Path)
    parser.add_argument("--frame-count", type=int, default=12)
    parser.add_argument("--iverilog", type=Path, default=Path("C:/iverilog/bin/iverilog.exe"))
    parser.add_argument("--vvp", type=Path, default=Path("C:/iverilog/bin/vvp.exe"))
    parser.add_argument("--skip-vcd", action="store_true",
                        help="Video replay only: collect bench CSV receipts without a VCD or cycle metrics")
    args = parser.parse_args()
    if args.skip_vcd and args.bench != "video":
        parser.error("--skip-vcd is only valid for the video replay bench")
    project = Path(__file__).resolve().parents[1]
    local_bin = project.parents[1] / ".tools/iverilog/bin"
    if not args.iverilog.is_file() and (local_bin / "iverilog.exe").is_file():
        args.iverilog = local_bin / "iverilog.exe"
    if not args.vvp.is_file() and (local_bin / "vvp.exe").is_file():
        args.vvp = local_bin / "vvp.exe"
    configurations = {
        "pipeline": ("tb_roi_hog_svm_measure", "clk", "rst_n", ["frame_ready", "rd_req_valid", "rd_rsp_valid", "roi_valid", "feature_valid", "result_valid", "release_frame", "busy"]),
        "video": ("tb_video_replay", "clk", "rst_n", ["analysis_eof", "object_frame_done", "track_frame_done", "core_error"]),
        "roi": ("tb_roi_frame_reader", "clk", "rst_n", ["frame_ready", "boxes_update", "rd_req_valid", "rd_rsp_valid", "roi_valid", "release_frame", "pair_miss", "busy"]),
        "hog": ("tb_hog_frontend", "clk", "rst_n", ["roi_valid", "grad_valid", "feature_valid", "feature_object_done"]),
        "svm": ("tb_hog_linear_svm", "clk", "rst_n", ["feature_valid", "result_valid", "busy"]),
        "bank": ("tb_gray_frame_pingpong", "rd_clk", "rd_rst_n", ["rd_frame_ready", "rd_owned", "rd_release", "rd_req_valid", "rd_rsp_valid", "rd_protocol_error"]),
    }
    top, clock, reset, watched = configurations[args.bench]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    vcd = output / "signals.vcd"
    observer = output / "tb_measure_observer.v"
    if not args.skip_vcd:
        observer.write_text('`timescale 1ns/1ps\nmodule tb_measure_observer;\ninitial begin\n'
                            f'  $dumpfile("{vcd.as_posix()}");\n  $dumpvars(1, {top});\n'
                            'end\nendmodule\n', encoding="ascii")
    sources = sorted((project / "user_source/hdl_source/road_vision").glob("*.v"))
    sources += [project / "tests/ph1p_logic_eram_sim.v", project / f"tests/{top}.v"]
    if not args.skip_vcd:
        sources.append(observer)
    binary = output / "simulation.vvp"
    compile_cmd = [str(args.iverilog), "-g2012", "-Wall", "-s", top]
    if not args.skip_vcd:
        compile_cmd += ["-s", "tb_measure_observer"]
    compile_cmd += ["-o", str(binary), *map(str, sources)]
    compiled = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
    plus = []
    if args.bench == "video":
        if args.frames is None:
            parser.error("--frames required for video")
        plus = [f"+FRAME_DIR={args.frames.resolve().as_posix()}", f"+RESULT_DIR={output.as_posix()}",
                f"+FRAMES={args.frame_count}", "+THRESHOLD=20", "+ROW_GAP=1280"]
    executed = subprocess.run([str(args.vvp), str(binary), *plus], capture_output=True, text=True, check=True, timeout=300)
    (output / "simulation.log").write_text(compiled.stdout + compiled.stderr + executed.stdout + executed.stderr, encoding="utf-8")
    if args.skip_vcd:
        receipt_paths = [output / name for name in
                         ("events.csv", "frame_summary.csv", "objects.csv", "tracks.csv")]
        missing_or_empty = [path.name for path in receipt_paths if not path.is_file() or path.stat().st_size == 0]
        if missing_or_empty:
            raise RuntimeError(f"video replay receipts missing or empty: {missing_or_empty}")
        metrics = {
            "status": "replay_receipts_complete_vcd_skipped",
            "frame_count": args.frame_count,
            "cycle_metrics_measured": False,
            "receipt_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in receipt_paths},
            "limitations": (
                "VCD generation was intentionally skipped to reduce simulation time and storage. "
                "This run supports candidate/track receipt comparison but provides no cycle latency evidence."),
            "source_sha256": {
                str(path.relative_to(project)) if path.is_relative_to(project) else str(path):
                hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
            "command": compile_cmd,
        }
        (output / "measurement.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        print(json.dumps({"bench": args.bench, "output": str(output),
                          "status": metrics["status"], "frame_count": args.frame_count}, indent=2))
        return
    metrics = summarize_vcd(vcd, clock, reset, watched)
    if args.bench == "video":
        eof = [r[0] for r in metrics["signals"]["analysis_eof"]["runs"]]
        rows = []
        for i, start in enumerate(eof):
            end = eof[i + 1] if i + 1 < len(eof) else float("inf")
            row = {"replay_frame": i, "eof_cycle": start}
            for name in ("object_frame_done", "track_frame_done"):
                ends = [r[0] for r in metrics["signals"][name]["runs"] if start <= r[0] < end]
                row[name + "_latency_cycles"] = ends[0] - start if ends else None
            rows.append(row)
        metrics["latencies"] = rows
    if args.bench == "bank":
        other = summarize_vcd(vcd, "wr_clk", "wr_rst_n", ["wr_frame_drop", "wr_sof", "wr_eof"])
        metrics["write_domain"] = other
    if args.bench == "pipeline":
        signal = metrics["signals"]
        start = signal["frame_ready"]["runs"][0][0]
        end = signal["result_valid"]["runs"][-1][0]
        release = signal["release_frame"]["runs"][0][0]
        metrics["pipeline_cycles"] = {"task_to_last_result": end-start,
            "task_to_release": release-start, "release_to_last_result": end-release,
            "clock_period_ns": 10, "weight_model": "synthetic all-one weights"}
    metrics["limitations"] = ("Existing unit fixtures include intentional error injection. Video bench is paced by "
        "row gaps and completion waits, not source-FPS SOF periods. Unit durations must not be summed into "
        "a production throughput or drop rate. Pipeline fixture uses four synthetic boxes and one-cycle "
        "mock RAM at 100 MHz; it excludes CDC, capture and scheduling. Full-size capture-to-release "
        "bank occupancy/wait causes remain unmeasured.")
    metrics["source_sha256"] = {str(p.relative_to(project)) if p.is_relative_to(project) else str(p):
                                hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    metrics["command"] = compile_cmd
    (output / "measurement.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    # Only the dump generated by this run is replaced by its gzip representation.
    with vcd.open("rb") as source, gzip.open(vcd.with_suffix(".vcd.gz"), "wb") as destination:
        shutil.copyfileobj(source, destination)
    vcd.unlink()
    print(json.dumps({"bench": args.bench, "output": str(output), "signals": metrics["signals"],
                      "latencies": metrics.get("latencies")}, indent=2))


if __name__ == "__main__":
    main()
