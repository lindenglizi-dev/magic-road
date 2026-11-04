
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
ART = OUT.parent
ROOT=Path(__file__).resolve().parents[2]
RUN = ROOT / 'build/route'
read = lambda p: Path(p).read_text(encoding='utf-8-sig')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
graph = json.loads(read(OUT / 'clock_graph_evidence.json'))
assert graph['status'] == 'EXTRACTED_REQUIRES_REVIEW'
assert sha(RUN / 'checked.db') == json.loads(read(ART/'checked_binding.json'))['checked_db_sha256']
for path, expected in graph['evidence_sha256'].items():
    assert sha(path) == expected, path
log = read(OUT / 'checked_clock_audit.log')
summary = read(OUT / 'checked_clock_summary.timing')
checks = read(OUT / 'checked_clock_checks.rpt')
assert 'CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED' in log
assert 'Confidence          : Routed' in summary and 'Check Corner        : Both (Slow and Fast)' in summary
assert 'Slow     | yes      yes' in summary and 'Fast     | yes      yes' in summary
assert 'update_timing -mode final -check_corner slow' in log and 'update_timing -mode final -check_corner fast' in log
assert 'start command "update_timing -mode final"' in log
assert min(graph['global_timing_ns'].values()) >= 0
assert graph['global_timing_ns']['STNS'] == graph['global_timing_ns']['HTNS'] == 0

                                                                              
mipi = 'u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.'
ddr = 'u_ph1p35_324_ddr_wrapper/u_ddr2/'
expected_period = dict(ETH_RX_CLK=8, ETH_RX_FABRIC=8, ETH_TX_CLK=8, HDMI_PIXEL_CLK=13.333,
    HDMI_SERIAL_CLK=2.666, MIPI_RX_BYTE_CLK=9.660, PHY_TX_CAPTURE=8, mipi_rx_ck_pad=2.415,
    pll_clk_100m=10, pll_clk_24m=42, sys_clk_50m=20)
expected_period.update({mipi + 'io_clk_pad_p':2.415, mipi + 'tif_c16_in':9.660, mipi + 'tif_c20_in':12.075})
expected_period.update({ddr + 'ctl_clk':7.5, ddr + 'ddr_clk':1.875, ddr + 'mcu_clk':19.687,
                        ddr + 'ref_clk':7.5, ddr + 'usr_clk':7.5})
periods = {}
for match in re.finditer(r'RUN-1002 : start command "report_property ([^"\n]+)"\n(.*?)(?=RUN-1002 : start command|\Z)', log, re.S):
    body = match[2]
    if not re.search(r'^CLASS\s+string\s+true\s+clock\s*$', body, re.M):
        continue
    name = re.search(r'^NAME\s+string\s+true\s+(\S+)', body, re.M)[1]
    assert name == match[1] and name not in periods
    periods[name] = float(re.search(r'^PERIOD\s+double\s+true\s+(\S+)', body, re.M)[1])
assert set(periods) == set(expected_period) and len(periods) == 19
for name, expected in expected_period.items():
    assert abs(periods[name] - expected) < 0.000001, (name, periods[name])
frequency = {m[3]:float(m[1]) for m in re.finditer(r'^\s*clk\d+:\s+([\d.]+)\s+(\d+)\s+(\S+)\s*$', summary, re.M)}
assert set(frequency) == set(expected_period) - {mipi + 'tif_c20_in'} and len(frequency) == 18
for name, actual in frequency.items():
    assert abs(actual - 1000 / expected_period[name]) <= 0.001, (name, actual)

pll_checks = []
for match in re.finditer(r'PLL/buffer inst: (\S+)\n\{(.*?)\n\}', checks, re.S):
    missing = int(re.search(r'There are (\d+) clock pins that have no clock constraints', match[2])[1])
    mismatch = int(re.search(r'There are (\d+) clocks whose clock frequency do not match the PLL setting', match[2])[1])
    assert missing == mismatch == 0
    pll_checks.append(dict(instance=match[1], missing_constraints=missing, frequency_mismatches=mismatch))
assert len(pll_checks) == 4

                                                                                                
for label, item in graph['feedback_branches'].items():
    assert item['native_route_type'] == 'global' and item['own_pll_output_feedback_verified']
    assert item['gclk']['ports']['clkout'] == item['sclk']['ports']['clkin']
    assert item['sclk']['ports']['clkout'] == item['net'] == item['pll']['ports']['fbclk']
    assert item['pll']['ports']['clkc'].strip('{}').split(',')[-1] in item['gclk']['ports']['clkin'].strip('{}').split(',')

route_log = read(ART / 'route_auto_native.log')
warning_rows = []
for candidate_log in [route_log, log]:
    rows = re.findall(r'RUN-1001 :\s+(pll_clk_24m)\s*\|\s*AL_PHY_SCLK\s*\|\s*(\d+)/(\d+)\s*\|\s*(\d+)\s*\|\s*(\S+)\s*\|\s*true', candidate_log)
    assert rows
    warning_rows.extend(rows)
assert len(set(warning_rows)) == 1
clock, clock_loads, total_loads, local_wires, warning_net = warning_rows[0]
assert int(total_loads) == int(clock_loads) + 1 and int(local_wires) == 3
assert warning_net == graph['camera_pad']['ports']['doq'].strip('{}').split(',')[-1]
camera_buffer = graph['camera_sclk_ancestor']['inst']
assert warning_net == camera_buffer + '_sclk_outnet'
assert {p['inst'] for p in graph['local_tree_pins']} == {graph['camera_pad_name'], graph['system_input_pad_name']}
tree = ET.parse(OUT / 'checked_clock_main_tree.rpt').getroot()
assert any(p.get('name') == camera_buffer + '.clkin' and p.get('route') == 'global' for p in tree.iter('pin'))
assert graph['camera_pad']['ports']['opad'] == 'O_cam_24m'
assert graph['camera_pad_latency'] and all({'slow_corner','fast_corner'} <= set(row) for row in graph['camera_pad_latency'])

                                                                           
                                                                                  
cascade = route_log.split('Analyze Clock Net Cascade Without Buffer Summary', 1)[1].split('start command "export_sdc', 1)[0]
cascade_rows = [line for line in cascade.splitlines() if re.match(r'RUN-1001 :\s*\d+\s*\|', line)]
expected_cascade = {'ddr_user', 'ethernet'}
assert len(cascade_rows) == len(expected_cascade)
reviewed_cascade = {}
for row in cascade_rows:
    columns = [part.strip() for part in row.split('|')]
    matches = [label for label in expected_cascade
        if columns[3] == graph['feedback_branches'][label]['sink'].removesuffix('.fbclk') + '(AL_PHY_PLL)']
    assert len(matches) == 1, row
    label = matches[0]
    assert label not in reviewed_cascade
    branch = graph['feedback_branches'][label]
    assert columns[1] == 'AL_PHY_SCLK' and columns[-1] == 'AL_PHY_GCLK'
    assert branch['net'].startswith(columns[2].removesuffix('...'))
    assert columns[4] in branch['pll']['ports']['clkc'].strip('{}').split(',')
    assert columns[4] in branch['gclk']['ports']['clkin'].strip('{}').split(',')
    assert branch['own_pll_output_feedback_verified'] and branch['native_route_type'] == 'global'
    reviewed_cascade[label] = dict(row=row, sink=branch['sink'], feedback_net=branch['net'], output_net=columns[4])
assert set(reviewed_cascade) == expected_cascade
for contents in [route_log, log]:
    counts = re.findall(r'Clock_Analyzer: (\d+) clock-net\(s\) because they drive other clock net', contents)
    assert counts and set(map(int, counts)) == {len(expected_cascade)}

logs = [ART / 'route_auto_native.log', ART / 'qualification_native.log', OUT / 'checked_clock_audit.log']
diagnostics = {}
for path in logs:
    contents = read(path)
    assert not re.search(r'(?m)^USR-6135\b', contents), path
    diagnostics[str(path)] = dict(USR6135_count=0,
        retained_clock_warning_lines=[line for line in contents.splitlines() if re.match(r'PHY-(?:5079|5088)\b', line)],
        other_retained_warning_lines=[line for line in contents.splitlines() if 'WARNING' in line and not re.match(r'PHY-(?:5079|5088)\b', line)])
domain_rows = {}
for line in summary.splitlines():
    values = line.split()
    if len(values) >= 16 and re.fullmatch(r'clk\d+', values[0]):
        domain_rows[values[0]] = dict(setup_wns_ns=float(values[-9]), setup_tns_ns=float(values[-8]),
            hold_wns_ns=float(values[-7]), hold_tns_ns=float(values[-6]), skew_ns=float(values[-5]),
            fanout=int(values[-4]), max_logic_level=int(values[-3]))
assert len(domain_rows) == 18 and all(row['setup_tns_ns'] == row['hold_tns_ns'] == 0 for row in domain_rows.values())
evidence = dict(graph['evidence_sha256'])
for path in [OUT / 'inspect_checked_clocks.py', OUT / 'clock_graph_evidence.json', Path(__file__),
             OUT / 'checked_restored_both_status.timing', OUT / 'checked_clock_status.timing',
             OUT / 'checked_clock_audit.tcl', ROOT / 'td_project/camera_to_dsi_display.sdc']:
    evidence[str(path)] = sha(path)
report = dict(status='PASS_CLOCK_REVIEW_WITH_RETAINED_NATIVE_WARNINGS', clock='PASS',
    created_utc=datetime.now(timezone.utc).isoformat(), root=str(ROOT), reviewer='本地验证工具',
    checked_db_sha256=sha(RUN / 'checked.db'), native_TD_launched_by_reviewer=False,
    active_clock_objects=dict(count=19, native_period_ns=periods, original_frequency_rows=frequency,
        tif_c20_note='Actual12.075ns native period retained; no fabricated summary frequency row.'),
    feedback_branches=graph['feedback_branches'], native_pll_frequency_checks=pll_checks,
    reviewed_PHY5079_PHY5088=dict(status='REVIEWED_AND_CLOSED_FOR_THIS_CHECKED_DB',
        actual_warning_clock=clock, reported_local_wire_segments=int(local_wires), warning_branch=warning_net,
        branch_clock_loads=int(clock_loads), branch_total_loads=int(total_loads),
        actual_camera_pad=graph['camera_pad_name'], actual_system_input_pad=graph['system_input_pad_name'],
        local_tree_pins=graph['local_tree_pins'], actual_camera_ports=graph['camera_pad']['ports'],
        camera_pad_latency=graph['camera_pad_latency'],
        explanation='Exactly one non-clock load is the camera-clock output PIO doq[0]->opad->O_cam_24m. Current XML has only that local output leaf and the system input-pad leaf; its regional SCLK input remains global. Three local segments do not denote three fabric FF sinks. All three actual PLL.fbclk sink nets separately prove native global routing and own-PLL feedback graph.',
        cascade_warning=dict(native_entries=len(reviewed_cascade), branches=reviewed_cascade, actual_loop='Each DDR-user/Ethernet PLL output->GCLK->SCLK->same PLL.fbclk; exact native rows matched to current extracted physical graphs'),
        warnings_cleared=False),
    native_diagnostics=diagnostics, global_routed_both_corner_timing_ns=graph['global_timing_ns'],
    domain_timing_and_skew=domain_rows, coverage_percent=float(re.search(r'STA coverage\s*:\s*([\d.]+)%', summary)[1]),
    evidence_sha256=evidence, unresolved=[],
    limits=['Clock/retained-native-warning evidence review only; no bit generation or whole-source/pad/POR approval.',
            'PHY5079/5088 remain emitted; their actual current sinks and feedback routes were reviewed, not silenced.',
            'Native buffer/pad clock slack infinity and max-int marker are not claimed as setup/hold measurements.',
            'No PHY readback, camera raw capture, board timing measurement or Flash operation.',
            'Placement get_param metadata issue is separately recorded in placement selection review, not a clock-signoff failure.'])
(OUT / 'checked_clock_warning_review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(report['status'])
print('checked.db SHA256', report['checked_db_sha256'])
print('CURRENT_ROUTED_BOTH_CORNER_TIMING_NS', graph['global_timing_ns'])
