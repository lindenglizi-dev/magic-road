"""在置零优化之前查询两份ROM定义的无驱动连接，输出仅限当前候选。"""
from run import ROOT, TOP, tools, save, scope, frozen, digest

frozen()
scope()
work = tools.fresh("prezero_query")
sources = sorted((ROOT / "rtl").glob("*.v"))
records = {}
for module in (TOP, "road_yolo_numeric_rom_group"):
    directory = work / module
    directory.mkdir()
    project = tools.project(directory, "layer_shell", sources)
    content = (directory / project).read_text()
    for tag in ("LABEL", "MODULE"):
        content = content.replace(f"<{tag}>road_dynamic_overlap_low_io_top</{tag}>", f"<{tag}>{module}</{tag}>")
    (directory / project).write_text(content, encoding="utf-8")
    script = f"""import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project {project} -single_run
elaborate -top {module}
set dead [get_nets -hier -full_hier -filter {{DRIVER_COUNT == 0}} *]
puts "PREZERO_MODULE {module} COUNT [llength $dead]"
foreach net $dead {{
    puts "PREZERO_NET [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}}
report_nets $dead -connection -pin_display_limit 100
puts "PREZERO_QUERY_DONE"
close_project
"""
    (directory / "inspect.tcl").write_text(script, encoding="utf-8")
    log = tools.command([tools.TD, "inspect.tcl"], directory, "td", timeout=120)
    assert "PREZERO_QUERY_DONE" in log and "ERROR:" not in log
    found = [line for line in log.splitlines() if line.startswith("PREZERO_NET ")]
    records[module] = found
    assert all("PINS 0 DRIVER 0" in line for line in found), found
save(work / "receipt.json", {"no_loaded_undriven_nets": True, "stage": "elaboration before optimize_rtl zeroing",
    "records": records, "sources": {str(p): digest(p) for p in sources}, "td_sha256": digest(tools.TD),
    "boundary": "net query, not all raw primitive mode-pin proof; unsupported and unused physical pins still need mode-specific interpretation"})
save(ROOT / "prezero_current.json", {"work": str(work)})
frozen()
print("PREZERO_LOADED_UNDRIVEN_ZERO", records)
