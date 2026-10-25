"""Check retained operands and classify visible TD undriven warnings, without waivers."""
import json
import re
import run


def main():
    run.check()
    root = run.ROOT
    netlist = root / 'physical/gate_netlist.v'
    text = netlist.read_text(encoding='utf-8')
    dsps = re.findall(r'PH1P_PHY_DSPSIOU_V2 #\(.*?\);', text, re.S)
    mac = [block for block in dsps if '/u_mac/i_activation_data' in block]
    assert len(dsps) == 30 and len(mac) == 24
    assert all('/u_mac/i_weight_data' in block and '.ce(' in block for block in mac)
    rams = re.findall(r'PH1P_PHY_ERAM_V2 #\(.*?\);', text, re.S)
    assert len(rams) == 13
    silu = [block for block in rams if 'PH1P_LOGIC_ERAM_Inst_silu_table_syn_1' in block]
    assert len(silu) == 1
    assert all(token in silu[0] for token in ('wire_table_address', 'flag_pipeline_enable',
                                             'reg_table_data', 'flag_table_write'))
    log = (root / 'physical/td.log').read_text(encoding='utf-8')
    undriven = re.findall(r'SYN-5013 WARNING: Undriven net:.*?/ net "([^"]+)"', log)
    assert undriven and all('/u_ddr_phy/cal_apb_prdata[' in item for item in undriven)
    receipt = {'limited_structural_check_passed': True, 'gate_level_numeric_simulation': False,
        'netlist_sha256': run.sha(netlist), 'dsp_total': len(dsps), 'dynamic_mac_operand_pairs': len(mac),
        'eram_total': len(rams), 'silu_table_dynamic_address_data_enable': True,
        'requant_dsp_instances': [re.search(r'\)\)\s*(\S+)\s*\(', block)[1] for block in dsps if block not in mac],
        'visible_syn5013_nets': undriven, 'syn5013_suppression_present': 'SYN-5013 Similar messages will be suppressed.' in log,
        'syn5025_count': log.count('SYN-5025 WARNING'),
        'limits': ['Visible warnings are unused calibration APB readback with APB disabled in this diagnostic.',
                   'Suppressed additional messages and dummy primitive endpoints are not declared fully closed.',
                   'Structural preservation is not a full post-synthesis numerical proof.',
                   'Functional bias/weight/activation/RAM path proof is in actual RTL intermediate-value tests.']}
    run.save(root / 'netlist_check.json', receipt)
    print(json.dumps({key: receipt[key] for key in ('dsp_total', 'dynamic_mac_operand_pairs', 'eram_total', 'syn5025_count')}))
    run.check()


if __name__ == '__main__':
    main()
