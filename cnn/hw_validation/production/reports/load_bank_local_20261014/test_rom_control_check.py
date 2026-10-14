"""本布局连接量测的负例；不修改网表或历史67端检查器。"""
from unittest.mock import patch

import check_rom_control as checks

after = (checks.ROOT / "physical/routed_netlist.v").read_text(encoding="utf-8")
original_driver, original_pins = checks.driver, checks.pins
checks.check()


def wrong_lut(text, pin):
    fields, output = original_driver(text, pin)
    if text == after:
        fields["INIT_LUT5B"] = "INTENTIONAL_BAD_LUT"
    return fields, output


def repeated_sink(block, section):
    result = original_pins(block, section)
    if section == "Load pin(s):" and "Net:" not in block and result:
        return result + result[:1]
    return result


for name, replacement in (("driver", wrong_lut), ("pins", repeated_sink)):
    with patch.object(checks, name, side_effect=replacement):
        try:
            checks.check()
        except AssertionError:
            print("EXPECTED_REJECTION", name)
        else:
            raise AssertionError("Corrupt LUT or duplicate sink escaped check")
print("ROM_CONTROL_NEGATIVES_PASS")
