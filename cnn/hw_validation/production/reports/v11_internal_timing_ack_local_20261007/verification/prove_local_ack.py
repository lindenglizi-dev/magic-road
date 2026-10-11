"""Exhaustive known-state proof for the proposed runner-local MAC result ready."""
from itertools import product
import json


ST_IDLE = 0
ST_MAC_WAIT = 3


def main() -> None:
    rows = 0
    wait_rows = 0
    table_enabled_rows = 0
    mismatches = []
    for state in range(16):
        for queue_count in range(4):
            for (start, export_start, parent_table_valid, table_loaded, fatal,
                 table_fault, reserved, mac_valid) in product((False, True), repeat=8):
                rows += 1
                is_idle = state == ST_IDLE
                is_wait = state == ST_MAC_WAIT
                table_enable = is_idle and not start and not export_start
                child_table_valid = parent_table_valid and table_enable
                pp_input_ready = (queue_count < 2 and table_loaded and
                                  not table_fault and not child_table_valid and not fatal)
                pp_fault = fatal or table_fault

                old_mac_ready = is_wait and reserved and pp_input_ready
                old_accept = mac_valid and old_mac_ready
                child_input_valid = is_wait and reserved and mac_valid
                old_child_accept = child_input_valid and pp_input_ready

                local_ready = (is_wait and reserved and queue_count < 2 and
                               table_loaded and not pp_fault)
                new_accept = mac_valid and local_ready

                if is_wait:
                    wait_rows += 1
                    assert not table_enable
                    assert not child_table_valid
                if table_enable:
                    table_enabled_rows += 1

                if not (old_mac_ready == local_ready and
                        old_accept == new_accept == old_child_accept):
                    mismatches.append({
                        "state": state,
                        "queue_count": queue_count,
                        "start": start,
                        "export_start": export_start,
                        "parent_table_valid": parent_table_valid,
                        "table_loaded": table_loaded,
                        "fatal": fatal,
                        "table_fault": table_fault,
                        "reserved": reserved,
                        "mac_valid": mac_valid,
                        "table_enable": table_enable,
                        "child_table_valid": child_table_valid,
                        "pp_input_ready": pp_input_ready,
                        "old_mac_ready": old_mac_ready,
                        "local_ready": local_ready,
                        "old_accept": old_accept,
                        "new_accept": new_accept,
                        "old_child_accept": old_child_accept,
                    })

    assert rows == 16384
    assert wait_rows == 1024
    assert table_enabled_rows == 256
    assert not mismatches
    print(json.dumps({
        "status": "KNOWN_STATE_EXHAUSTIVE_PASS",
        "rows": rows,
        "wait_rows": wait_rows,
        "table_enabled_rows": table_enabled_rows,
        "mismatches": len(mismatches),
        "proved": [
            "old_mac_result_ready == proposed_local_ready",
            "old_mac_result_accept == proposed_mac_result_accept",
            "old_child_input_accept == proposed_mac_result_accept",
            "child_table_valid == 0 whenever state == ST_MAC_WAIT",
        ],
        "four_state_boundary":
            "This Boolean proof covers only known 0/1 controls. X/Z behavior is not proved here and must be checked separately by four-state RTL simulation and static review.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
