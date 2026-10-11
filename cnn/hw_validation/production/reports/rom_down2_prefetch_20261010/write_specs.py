"""使用既有formatter和规范生成入口，记录本次三个新增模块。"""
import json
from pathlib import Path
import shutil
import sys

from run import ROOT, SKILL, tools, save
sys.path.insert(0, str(SKILL))
from scripts.python.quality.formatter_backend import VerilogFormatterEngine


def main():
    work = tools.fresh("s")
    engine = VerilogFormatterEngine({"formatter":{"indent_style":"tab","indent_size":4}})
    targets = [ROOT / "rtl" / name for name in ("road_numeric_rom_reader.v","road_down2_parameter_prefetch.v","road_rom_down2_top.v")]
    targets += [ROOT / "tests" / name for name in ("tb_rom_down2.v","tb_rom_reader.v","tb_parameter_prefetch.v")]
    modules=[]
    for source in targets:
        name, _, ports, _ = engine._parse_module(source.read_text(encoding="utf-8"))
        declared=[]
        for port in ports:
            width=1
            if port.width:
                high,low=port.width.strip("[]").split(":")
                width=abs(int(high)-int(low))+1
            declared.append({"name":port.name,"direction":port.direction,"width":width,
                "role":port.name,"description":port.name,"clock_domain":"i_clk"})
        behavior={
            "road_numeric_rom_reader":["一个在途请求；13位word地址0..7167，四路40bit拼接、14组，20字节小端。",
                "接受请求后8个上升沿形成response；下一沿可被消费者接收。response等待ready时保持；不接第二个请求。越界锁故障直到复位。"],
            "road_down2_parameter_prefetch":["固定13个manifest字段，共652笔runner load和1024项SiLU表，2946字节。",
                "单个160bit缓存，按字节组装1/2/4字节；未对齐字段和跨词尾不丢字节。数值符号/shift0..62校验后才发布。",
                "field/request/wait/byte/emit/advance状态计时；反压期间不改变kind/address/data。复位从字段零重新完整装载。"],
            "road_rom_down2_top":["顶层50个I/O位：2个全局+24个控制/输入负载+24个输出，精确统计以io_bits.json为准。",
                "外部异步断言、两级同步释放；最早第三个上升沿开始ROM预取。所有内部模块共享domain_rstn。",
                "pref_done、SiLU table_loaded且无故障前，外部ready/busy/output_valid为零；提前start忽略。",
                "只通过窄并口装9x9x16 halo，1296笔顺序。最后一笔握手后的下一拍方可start，不同拍抢跑。",
                "原样实例化down2 runner/MAC/RNE/SiLU/动态乘积。运行参数驻留原runner，不新增全量参数RAM。",
                "故障阻止start/commit/export，输出取消；复位取消旧事务、重新装满1024项SiLU表。"],
        }.get(name,["测试平台逐项检查字段和数值，带复位、长反压、非法地址；不作为综合源。"])
        modules.append({"name":name,"feature":"r","rtl_path":str(source.relative_to(ROOT)).replace("\\","/"),
            "description":"独立schema2 TEST参数接入，不是训练模型部署或整网性能证明。",
            "interfaces":{"protocol":"discrete","ports":declared},"parameters":[],
            "clock":{"name":"i_clk","edge":"posedge","frequency_hz":100000000},
            "reset":{"name":"i_rstn","active":"low","synchronous":False,"values":"取消全部旧事务和装载有效状态；top同步释放后重装1024表项。"},
            "behavior":behavior,"constraints":["不改原核接口、II、数值、复位合同；不增时序例外。","不训练、不改生产、不生成位流、不上板。"],
            "corner_cases":["跨20字节词、物理bank边界、未对齐层尾、非法地址。","装载和计算受阻时复位，不泄漏旧输出。"],
            "verification_cases":["厂商PH1P模型、1676笔字段逐项比较、MAC/pre/SiLU/post/写回/导出对拍。","原64项同向量回归；TD资源和时序单列。"],
            "timing_diagrams":[{"id":"boot","title":"装载屏障与运行","scenario":"boot","description":"事件示意，长预取与运行压缩，不按每格推算周期。",
            "wavejson":{"signal":[{"name":"i_clk","wave":"p........."},{"name":"i_rstn","wave":"01........"},
                {"name":"domain_rstn","wave":"0..1......"},{"name":"parameters_ready","wave":"0.....1..."},
                {"name":"halo_complete","wave":"0......1.."},{"name":"start","wave":"0.......10"}]}}]})
    save(work / "spec.json", {"modules":modules})
    entry=f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    tools.command([sys.executable,"-B","-X","utf8","-c",entry,"write-spec","--spec",work / "spec.json",
        "--out-dir",work / "generated","--no-state"],work,"write",allowed=(0,1,2))
    for source in targets:
        companion=work / "generated/spec/r" / ("tests" if source.parent.name == "tests" else "") / (source.stem + "_spec.md")
        assert companion.exists(),companion
        shutil.copy2(companion,source.with_name(companion.name))
        shutil.copytree(companion.parent / "waveforms", source.parent / "waveforms", dirs_exist_ok=True)
    top=next(m for m in modules if m["name"]=="road_rom_down2_top")
    save(ROOT / "io_bits.json",{"total":sum(p["width"] for p in top["interfaces"]["ports"]),"ports":top["interfaces"]["ports"]})
    save(ROOT / "specification_current.json",{"work":str(work)})


if __name__=="__main__":
    main()
