"""本地字面连接检查的两个负例，不修改网表，不代替RTL门禁。"""
from unittest.mock import patch

import check_replication as checks


work = checks.ROOT / "physical_attempt2"
after = (work / "routed_netlist.v").read_text(encoding="utf-8")
log = (work / "td_launcher.log").read_text(encoding="utf-8")
block = log.split("WE_AFTER_0_BEGIN", 1)[1].split("WE_AFTER_0_END", 1)[0]
write_cell = checks.pins(block, "Driver pin(s):")[0].rsplit(".", 1)[0]
original = checks.cell_fields
assert checks.check_writes(work)["status"].startswith("PASS_")
for cell, field in ((write_cell, "INIT_LUT5B"),
                    ("u_compute/u_stem/cnt_channel_reg[1]_syn_54", "imb")):
    def corrupt(text, name):
        fields = original(text, name)
        if text == after and name == cell:
            fields[field] = "INTENTIONAL_BAD_TEST_VALUE"
        return fields

    with patch.object(checks, "cell_fields", side_effect=corrupt):
        try:
            checks.check_writes(work)
        except AssertionError:
            print("EXPECTED_REJECTION", cell, field)
        else:
            raise AssertionError("Corrupt WE LUT or packed tag escaped the bounded check")
print("BOUNDED_CHECK_NEGATIVES_PASS")
